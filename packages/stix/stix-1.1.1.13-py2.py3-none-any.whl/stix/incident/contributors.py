# Copyright (c) 2016, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

from mixbox import fields

# external
from cybox.common import Contributor

# internal
import stix
import stix.utils
import stix.bindings.incident as incident_binding


class Contributors(stix.EntityList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = _binding.ContributorsType

    contributors = fields.TypedField("Contributor", Contributor, multiple=True, key_name="contributors")