from jsonschema import Draft7Validator

from utils import *

SCHEMA_ENLEVEMENT_VEHICULE = {
    TYPE: OBJECT,
    PROPERTIES: {
        "trigrammeSIP": STRING_TYPE,
        "dateEnlevement": STRING_TYPE,
    },
    REQUIRED: [
        "trigrammeSIP",
        "dateEnlevement",
    ],
    ADDITIONAL_PROPERTIES: False
}

Draft7Validator.check_schema(SCHEMA_ENLEVEMENT_VEHICULE)
