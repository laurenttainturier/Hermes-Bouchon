from jsonschema import Draft7Validator

from utils import *

SCHEMA_RECUPERATION_BIEN = {
    TYPE: OBJECT,
    PROPERTIES: {
        "trigrammeSIP": STRING_TYPE,
        "dateDebut": STRING_TYPE,
        "dateFin": STRING_TYPE,
        "idEntitesRemettantes": optional_type({
            TYPE: ARRAY,
            ITEMS: INTEGER_TYPE
        }),
    },
    REQUIRED: [
        "trigrammeSIP",
        "dateDebut",
        "dateFin",
    ],
    ADDITIONAL_PROPERTIES: False
}

Draft7Validator.check_schema(SCHEMA_RECUPERATION_BIEN)
