# -*- coding: utf-8 -*-
# Copyright 2018, CS Systemes d'Information, http://www.c-s.fr
#
# This file is part of EODAG project
#     https://www.github.com/CS-SI/EODAG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import unicode_literals

import re
from datetime import datetime
from string import Formatter

from dateutil.tz import tzutc
from lxml import etree
from lxml.etree import XPathEvalError
from shapely import geometry
from six import string_types

from eodag.utils import get_timestamp

SEP = r"#"
INGEST_CONVERSION_REGEX = re.compile(
    r"^{(?P<path>[^#]*)" + SEP + r"(?P<converter>[^\d\W]\w*)}$"
)
NOT_AVAILABLE = "Not Available"
NOT_MAPPED = "Not Mapped"


def get_metadata_path(map_value):
    """Return the jsonpath or xpath to the value of a EO product metadata in a provider
    search result.

    The path is retrieved depending on if the metadata is queryable (the value
    associated to it in the provider search config metadata mapping is a list) or not
    (the value is directly the string corresponding to the path).

    Assume we have the following provider config::

        provider:
            ...
            search:
                ...
                metadata_mapping:
                    productType:
                        - productType
                        - $.properties.productType
                    id: $.properties.id
                    ...
                ...
            ...

    Then the metadata `id` is not queryable for this provider meanwhile `productType`
    is queryable. The first value of the `metadata_mapping.productType` is how the
    eodag search parameter `productType` is interpreted in the
    :class:`~eodag.plugins.search.base.Search` plugin implemented by `provider`, and is
    used when eodag delegates search process to the corresponding plugin.

    :param map_value: The value originating from the definition of `metadata_mapping`
                      in the provider search config. For example, it is the list
                      `['productType', '$.properties.productType']` with the sample
                      above
    :type map_value: str (Python 3) or unicode (Python 2) or list(str or unicode)
    :return: The value of the path to the metadata value in the provider search result
    :rtype: str (Python 3) or unicode (Python 2)
    """
    path = map_value[1] if isinstance(map_value, list) else map_value
    match = INGEST_CONVERSION_REGEX.match(path)
    if match:
        g = match.groupdict()
        return g["converter"], g["path"]
    return None, path


def get_search_param(map_value):
    """See :func:`~eodag.api.product.metadata_mapping.get_metadata_path`

    :param map_value: The value originating from the definition of `metadata_mapping`
                      in the provider search config
    :type map_value: list
    :return: The value of the search parameter as defined in the provider config
    :rtype: str (Python 3) or unicode (Python 2)
    """
    # Assume that caller will pass in the value as a list
    return map_value[0]


def format_metadata(search_param, *args, **kwargs):
    """Format a string of form {<field_name>#<conversion_function>}

    The currently understood converters are:
        - ``to_timestamp_milliseconds``: converts a utc date string to a timestamp in
          milliseconds
        - ``to_wkt``: converts a geometry to its well known text representation
        - ``to_iso_utc_datetime_from_milliseconds``: converts a utc timestamp in given
          milliseconds to a utc iso datetime
        - ``to_iso_utc_datetime``: converts a UTC datetime string to ISO UTC datetime
          string
        - ``to_iso_date``: removes the time part of a iso datetime string
        - ``remove_extension``: on a string that contains dots, only take the first
          part of the list obtained by splitting the string on dots

    :param search_param: The string to be formatted
    :type search_param: str or unicode
    :param args: (optional) Additional arguments to use in the formatting process
    :type args: tuple
    :param kwargs: (optional) Additional named-arguments to use when formatting
    :type kwargs: dict
    :returns: The formatted string
    :rtype: str or unicode

    .. versionadded::
        1.0

            * Added the ``remove_extension`` metadata converter
    """

    class MetadataFormatter(Formatter):
        CONVERSION_REGEX = re.compile(
            r"^(?P<field_name>.+)" + SEP + r"(?P<converter>[^\d\W]\w*)$"
        )

        def __init__(self):
            self.custom_converter = None

        def get_field(self, field_name, args, kwargs):
            conversion_func_spec = self.CONVERSION_REGEX.match(field_name)
            # Register a custom converter if any for later use (see convert_field)
            # This is done because we don't have the value associated to field_name at
            # this stage
            if conversion_func_spec:
                field_name = conversion_func_spec.groupdict()["field_name"]
                converter = conversion_func_spec.groupdict()["converter"]
                self.custom_converter = getattr(self, "convert_{}".format(converter))
            return super(MetadataFormatter, self).get_field(field_name, args, kwargs)

        def convert_field(self, value, conversion):
            # Do custom conversion if any (see get_field)
            if self.custom_converter is not None:
                converted = self.custom_converter(value) if value is not None else ""
                # Clear this state variable in case the same converter is used to
                # resolve other named arguments
                self.custom_converter = None
                return converted
            return super(MetadataFormatter, self).convert_field(value, conversion)

        @staticmethod
        def convert_to_timestamp_milliseconds(value):
            return int(1e3 * get_timestamp(value))

        @staticmethod
        def convert_to_wkt(value):
            return geometry.box(
                *[
                    float(v)
                    for v in "{lonmin} {latmin} {lonmax} {latmax}".format(
                        **value
                    ).split()
                ]
            ).to_wkt()

        @staticmethod
        def convert_to_iso_utc_datetime_from_milliseconds(timestamp):
            try:
                return datetime.fromtimestamp(timestamp / 1e3, tzutc()).isoformat()
            except TypeError:
                return timestamp

        @staticmethod
        def convert_to_iso_utc_datetime(dt):
            for idx, fmt in enumerate(("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S")):
                try:
                    return (
                        datetime.strptime(dt, fmt)
                        .replace(tzinfo=tzutc())
                        .isoformat()
                        .replace("+00:00", "Z")
                    )
                except ValueError:
                    if idx == 1:
                        raise

        @staticmethod
        def convert_to_iso_date(datetime_string):
            return datetime_string[:10]

        @staticmethod
        def convert_remove_extension(string):
            parts = string.split(".")
            if parts:
                return parts[0]
            return ""

    return MetadataFormatter().vformat(search_param, args, kwargs)


def properties_from_json(json, mapping):
    """Extract properties from a provider json result.

    :param json: the representation of a provider result as a json object
    :type json: dict
    :param mapping: a mapping between :class:`~eodag.api.product.EOProduct`'s metadata
                    keys and the location of the values of these properties in the json
                    representation, expressed as a
                    `jsonpath <http://goessner.net/articles/JsonPath/>`_
    :return: the metadata of the :class:`~eodag.api.product.EOProduct`
    :rtype: dict
    """
    properties = {}
    templates = {}
    for metadata, value in mapping.items():
        # Treat the case when the value is from a queryable metadata
        if isinstance(value, list):
            conversion_or_none, path_or_text = value[1]
        else:
            conversion_or_none, path_or_text = value
        if isinstance(path_or_text, string_types):
            if re.search(r"({[^{}]+})+", path_or_text):
                templates[metadata] = path_or_text
            else:
                properties[metadata] = path_or_text
        else:
            match = path_or_text.find(json)
            extracted_value = match[0].value if len(match) == 1 else NOT_AVAILABLE
            if extracted_value is None:
                properties[metadata] = None
            else:
                if conversion_or_none is None:
                    properties[metadata] = extracted_value
                else:
                    properties[metadata] = format_metadata(
                        "{%s%s%s}" % (metadata, SEP, conversion_or_none),
                        **{metadata: extracted_value}
                    )
    # Resolve templates
    for metadata, template in templates.items():
        properties[metadata] = template.format(**properties)
    return properties


def properties_from_xml(xml_as_text, mapping, empty_ns_prefix="ns"):
    """Extract properties from a provider xml result.

    :param xml_as_text: the representation of a provider result as xml
    :type xml_as_text: str or unicode
    :param mapping: a mapping between :class:`~eodag.api.product.EOProduct`'s metadata
                    keys and the location of the values of these properties in the xml
                    representation, expressed as a
                    `xpath <https://www.w3schools.com/xml/xml_xpath.asp>`_
    :param empty_ns_prefix: the name to give to the default namespace of `xml_as_text`.
                            This is a technical workaround for the limitation of lxml
                            not supporting empty namespace prefix (default: ns). The
                            xpath in `mapping` must use this value to be able to
                            correctly reach empty-namespace prefixed elements
    :type empty_ns_prefix: str or unicode
    :return: the metadata of the :class:`~eodag.api.product.EOProduct`
    :rtype: dict
    """
    properties = {}
    templates = {}
    root = etree.XML(xml_as_text)
    for metadata, value in mapping.items():
        # Treat the case when the value is from a queryable metadata
        if isinstance(value, list):
            conversion_or_none, path_or_text = value[1]
        else:
            conversion_or_none, path_or_text = value
        try:
            extracted_value = root.xpath(
                path_or_text,
                namespaces={k or empty_ns_prefix: v for k, v in root.nsmap.items()},
            )
            if len(extracted_value) == 1:
                if conversion_or_none is None:
                    properties[metadata] = extracted_value[0]
                else:
                    properties[metadata] = format_metadata(
                        "{%s%s%s}" % (metadata, SEP, conversion_or_none),
                        **{metadata: extracted_value[0]}
                    )
            # If there are multiple matches, consider the result as a list, doing a
            # formatting if any
            elif len(extracted_value) > 1:
                if conversion_or_none is None:
                    properties[metadata] = extracted_value
                else:
                    properties[metadata] = [
                        format_metadata(
                            "{%s%s%s}"
                            % (
                                metadata,
                                SEP,
                                conversion_or_none,
                            ),  # Re-build conversion format identifier
                            **{metadata: extracted_value_item}
                        )
                        for extracted_value_item in extracted_value
                    ]
            # If there is no matched value (empty list), mark the metadata as not
            # available
            else:
                properties[metadata] = NOT_AVAILABLE
        except XPathEvalError:
            # Assume the mapping is to be passed as is, in which case we readily
            # register it, or is a template, in which case we register it for later
            # formatting resolution using previously successfully resolved properties
            # Ignore any transformation specified. If a value is to be passed as is,
            # we don't want to transform it further
            if re.search(r"({[^{}]+})+", path_or_text):
                templates[metadata] = path_or_text
            else:
                properties[metadata] = path_or_text
    # Resolve templates
    for metadata, template in templates.items():
        properties[metadata] = template.format(**properties)
    return properties


# Keys taken from http://docs.opengeospatial.org/is/13-026r8/13-026r8.html
# For a metadata to be queryable, The way to query it must be specified in the
# provider metadata_mapping configuration parameter. It will be automatically
# detected as queryable by eodag when this is done
DEFAULT_METADATA_MAPPING = {
    # Opensearch resource identifier within the search engine context (in our case
    # within the context of the data provider)
    "uid": "$.uid",
    # OpenSearch Parameters for Collection Search (Table 3)
    "productType": "$.properties.productType",
    "doi": "$.properties.doi",
    "platform": "$.properties.platform",
    "platformSerialIdentifier": "$.properties.platformSerialIdentifier",
    "instrument": "$.properties.instrument",
    "sensorType": "$.properties.sensorType",
    "compositeType": "$.properties.compositeType",
    "processingLevel": "$.properties.processingLevel",
    "orbitType": "$.properties.orbitType",
    "spectralRange": "$.properties.spectralRange",
    "wavelengths": "$.properties.wavelengths",
    "hasSecurityConstraints": "$.properties.hasSecurityConstraints",
    "dissemination": "$.properties.dissemination",
    # INSPIRE obligated OpenSearch Parameters for Collection Search (Table 4)
    "title": "$.properties.title",
    "topicCategory": "$.properties.topicCategory",
    "keyword": "$.properties.keyword",
    "abstract": "$.properties.abstract",
    "resolution": "$.properties.resolution",
    "organisationName": "$.properties.organisationName",
    "organisationRole": "$.properties.organisationRole",
    "publicationDate": "$.properties.publicationDate",
    "lineage": "$.properties.lineage",
    "useLimitation": "$.properties.useLimitation",
    "accessConstraint": "$.properties.accessConstraint",
    "otherConstraint": "$.properties.otherConstraint",
    "classification": "$.properties.classification",
    "language": "$.properties.language",
    "specification": "$.properties.specification",
    # OpenSearch Parameters for Product Search (Table 5)
    "parentIdentifier": "$.properties.parentIdentifier",
    "productionStatus": "$.properties.productionStatus",
    "acquisitionType": "$.properties.acquisitionType",
    "orbitNumber": "$.properties.orbitNumber",
    "orbitDirection": "$.properties.orbitDirection",
    "track": "$.properties.track",
    "frame": "$.properties.frame",
    "swathIdentifier": "$.properties.swathIdentifier",
    "cloudCover": "$.properties.cloudCover",
    "snowCover": "$.properties.snowCover",
    "lowestLocation": "$.properties.lowestLocation",
    "highestLocation": "$.properties.highestLocation",
    "productVersion": "$.properties.productVersion",
    "productQualityStatus": "$.properties.productQualityStatus",
    "productQualityDegradationTag": "$.properties.productQualityDegradationTag",
    "processorName": "$.properties.processorName",
    "processingCenter": "$.properties.processingCenter",
    "creationDate": "$.properties.creationDate",
    "modificationDate": "$.properties.modificationDate",
    "processingDate": "$.properties.processingDate",
    "sensorMode": "$.properties.sensorMode",
    "archivingCenter": "$.properties.archivingCenter",
    "processingMode": "$.properties.processingMode",
    # OpenSearch Parameters for Acquistion Parameters Search (Table 6)
    "availabilityTime": "$.properties.availabilityTime",
    "acquisitionStation": "$.properties.acquisitionStation",
    "acquisitionSubType": "$.properties.acquisitionSubType",
    "startTimeFromAscendingNode": "$.properties.startTimeFromAscendingNode",
    "completionTimeFromAscendingNode": "$.properties.completionTimeFromAscendingNode",
    "illuminationAzimuthAngle": "$.properties.illuminationAzimuthAngle",
    "illuminationZenithAngle": "$.properties.illuminationZenithAngle",
    "illuminationElevationAngle": "$.properties.illuminationElevationAngle",
    "polarizationMode": "$.properties.polarizationMode",
    "polarisationChannels": "$.properties.polarisationChannels",
    "antennaLookDirection": "$.properties.antennaLookDirection",
    "minimumIncidenceAngle": "$.properties.minimumIncidenceAngle",
    "maximumIncidenceAngle": "$.properties.maximumIncidenceAngle",
    "dopplerFrequency": "$.properties.dopplerFrequency",
    "incidenceAngleVariation": "$.properties.incidenceAngleVariation",
    # Custom parameters (not defined in the base document referenced above)
    # id differs from uid. The id is an identifier by which a product which is
    # distributed by many providers can be retrieved (a property that it has in common
    # in the catalogues of all the providers on which it is referenced)
    "id": "$.id",
    # The geographic extent of the product
    "geometry": "$.geometry",
    # The url of the quicklook
    "quicklook": "$.properties.quicklook",
    # The url to download the product "as is" (literal or as a template to be completed
    # either after the search result is obtained from the provider or during the eodag
    # download phase)
    "downloadLink": "$.properties.downloadLink",
    # custom field, can contain several parameters : "key1=value1&key2=value2"
    "custom": "$.properties.custom",
}
