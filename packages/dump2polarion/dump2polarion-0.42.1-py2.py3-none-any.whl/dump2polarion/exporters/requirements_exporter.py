# -*- coding: utf-8 -*-
"""
Creates a Requirement XML file for submitting to the Polarion Importer.

Example of input requirements_data:
requirements_data = [
    {
        "title": "requirement_complete",
        "description": "Complete Requirement",
        "approver-ids": "mkourim:approved",
        "assignee-id": "mkourim",
        "category-ids": "category_id1, category_id2",
        "due-date": "2018-09-30",
        "planned-in-ids": "planned_id1, planned_id2",
        "initial-estimate": "1/4h",
        "priority-id": "high",
        "severity-id": "should_have",
        "status-id": "status_id",
        "reqtype": "functional",
    },
    {
        "title": "requirement_minimal",
    },
]
"""

from __future__ import absolute_import, unicode_literals

import datetime
import logging

import six
from lxml import etree

from dump2polarion import utils
from dump2polarion.exceptions import Dump2PolarionException, NothingToDoException
from dump2polarion.exporters import transform_projects

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


class RequirementTransform(object):
    """Transforms requirement data and fills in default keys and values."""

    REQ_DATA = {
        "approver-ids": None,
        "assignee-id": None,
        "category-ids": None,
        "due-date": None,
        "initial-estimate": None,
        "planned-in-ids": None,
        "priority-id": "high",
        "severity-id": "should_have",
        "status-id": None,
    }

    FIELD_MAPPING = {
        "assignee-id": "assignee",
        "initial-estimate": "initialEstimate",
        "priority-id": "priority",
        "severity-id": "severity",
        "status-id": "status",
    }

    CUSTOM_FIELDS = {"reqtype": "functional"}

    def __init__(self, config, transform_func=None):
        self.config = config
        self._transform_func = transform_func or transform_projects.get_requirements_transform(
            config
        )

    def _run_transform_func(self, result):
        """Calls transform function on result."""
        if self._transform_func:
            result = self._transform_func(result)
        return result or None

    def _fill_polarion_fields(self, req_data):
        """Sets importer field value from polarion field if available."""
        for importer_field, polarion_field in six.iteritems(self.FIELD_MAPPING):
            polarion_value = req_data.get(polarion_field)
            xml_value = req_data.get(importer_field)
            if polarion_value and not xml_value:
                req_data[importer_field] = polarion_value
        return req_data

    def _fill_defaults(self, req_data):
        for defaults in self.REQ_DATA, self.CUSTOM_FIELDS:
            for key, value in six.iteritems(defaults):
                if value and not req_data.get(key):
                    req_data[key] = value
        return req_data

    def transform(self, req_data):
        """Transforms requirement data."""
        req_data = self._fill_polarion_fields(req_data)
        req_data = self._run_transform_func(req_data)
        if not req_data:
            return None

        title = req_data.get("title")
        if not title:
            logger.warning("Skipping requirement, title is missing")
            return None

        req_data = self._fill_defaults(req_data)
        return req_data


class RequirementExport(object):
    """Exports requirements data into XML representation."""

    def __init__(self, requirements_data, config, transform_func=None):
        self.requirements_data = requirements_data
        self.config = config
        self._lookup_prop = ""
        self.requirement_transform = RequirementTransform(config, transform_func)

    def _top_element(self):
        """Returns top XML element."""
        attrs = {"project-id": self.config["polarion-project-id"]}
        document_relative_path = self.config.get("requirements-document-relative-path")
        if document_relative_path:
            attrs["document-relative-path"] = document_relative_path
        top = etree.Element("requirements", utils.sorted_dict(attrs))
        return top

    def _properties_element(self, parent_element):
        """Returns properties XML element."""
        requirements_properties = etree.SubElement(parent_element, "properties")

        req_properties_conf = self.config.get("requirements_import_properties") or {}
        for name, value in sorted(six.iteritems(req_properties_conf)):
            if name == "lookup-method":
                lookup_prop = str(value).lower()
                if lookup_prop not in ("id", "name"):
                    raise Dump2PolarionException(
                        "Invalid value '{}' for the 'lookup-method' property".format(str(value))
                    )
                self._lookup_prop = lookup_prop
            else:
                etree.SubElement(
                    requirements_properties, "property", {"name": name, "value": str(value)}
                )

        return requirements_properties

    def _fill_lookup_prop(self, requirements_properties):
        """Fills the polarion-lookup-method property."""
        if not self._lookup_prop:
            raise Dump2PolarionException("Failed to set the 'polarion-lookup-method' property")

        etree.SubElement(
            requirements_properties,
            "property",
            {"name": "lookup-method", "value": self._lookup_prop},
        )

    def _check_lookup_prop(self, req_id):
        """Checks that selected lookup property can be used for this testcase."""
        if self._lookup_prop:
            if not req_id and self._lookup_prop == "id":
                return False
        else:
            if req_id:
                self._lookup_prop = "id"
            else:
                self._lookup_prop = "name"
        return True

    def _classify_data(self, req_data):
        attrs, custom_fields = {}, {}

        for key, value in six.iteritems(req_data):
            if not value:
                continue
            conv_key = key.replace("_", "-")  # convert pythonic key_param to polarion 'key-param'
            if conv_key in self.requirement_transform.REQ_DATA:
                attrs[conv_key] = value
            elif conv_key in self.requirement_transform.CUSTOM_FIELDS:
                custom_fields[conv_key] = value

        return attrs, custom_fields

    @staticmethod
    def _fill_custom_fields(parent, custom_fields):
        if not custom_fields:
            return

        custom_fields_el = etree.SubElement(parent, "custom-fields")
        for field, content in six.iteritems(custom_fields):
            etree.SubElement(
                custom_fields_el,
                "custom-field",
                utils.sorted_dict({"id": field, "content": content}),
            )

    def _requirement_element(self, parent_element, req_data):
        """Adds requirement XML element."""
        req_data = self.requirement_transform.transform(req_data)
        if not req_data:
            return

        title = req_data.get("title")

        req_id = req_data.get("id")
        if not self._check_lookup_prop(req_id):
            logger.warning(
                "Skipping requirement `%s`, data missing for selected lookup method", title
            )
            return

        attrs, custom_fields = self._classify_data(req_data)

        # For testing purposes, the order of fields in resulting XML
        # needs to be always the same.
        attrs = utils.sorted_dict(attrs)
        custom_fields = utils.sorted_dict(custom_fields)

        requirement = etree.SubElement(parent_element, "requirement", attrs)

        title_el = etree.SubElement(requirement, "title")
        title_el.text = utils.get_unicode_str(title)

        description = req_data.get("description")
        if description:
            description_el = etree.SubElement(requirement, "description")
            description_el.text = utils.get_unicode_str(description)

        self._fill_custom_fields(requirement, custom_fields)

    def _fill_requirements(self, parent_element):
        if not self.requirements_data:
            raise NothingToDoException("Nothing to export")
        for req_data in self.requirements_data:
            self._requirement_element(parent_element, req_data)

    def export(self):
        """Returns requirements XML."""
        top = self._top_element()
        properties = self._properties_element(top)
        self._fill_requirements(top)
        self._fill_lookup_prop(properties)
        return utils.prettify_xml(top)

    @staticmethod
    def write_xml(xml, output_file=None):
        """Outputs the XML content into a file."""
        gen_filename = "requirements-{:%Y%m%d%H%M%S}.xml".format(datetime.datetime.now())
        utils.write_xml(xml, output_loc=output_file, filename=gen_filename)
