from jsonschema import Draft7Validator

from utils import *

SCHEMA_ENTITE_REMETTANTE = {
    TYPE: ARRAY,
    ITEMS: {
        TYPE: OBJECT,
        PROPERTIES: {
            "trigrammeSIP": STRING_TYPE,
            "idCorrelation": STRING_TYPE,
            "denomination": STRING_TYPE,
            "indicateurActif": OPTIONAL_BOOLEAN_TYPE,
            "telephone": STRING_TYPE,
            "courriel": STRING_TYPE,
            "fax": OPTIONAL_STRING_TYPE,
            "codeTypologieNiveau1": STRING_TYPE,
            "codeTypologieNiveau2": OPTIONAL_STRING_TYPE,
            "conditionEnlevementBien": OPTIONAL_STRING_TYPE,
            "adresse": {
                TYPE: OBJECT,
                PROPERTIES: {
                    "codePostal": STRING_TYPE,
                    "ville": STRING_TYPE,
                    "numVoie": STRING_TYPE,
                    "indiceDeRepetition": OPTIONAL_STRING_TYPE,
                    "libelleVoie": STRING_TYPE,
                    "complementAdresse": OPTIONAL_STRING_TYPE,
                    "estEnFrance": BOOLEAN_TYPE,
                    "paysEtranger": OPTIONAL_STRING_TYPE,
                },
                REQUIRED: [
                    "codePostal",
                    "ville",
                    "numVoie",
                    "libelleVoie",
                    "estEnFrance",
                ],
                ADDITIONAL_PROPERTIES: False,
            },
        },
        REQUIRED: [
            "trigrammeSIP",
            "idCorrelation",
            "denomination",
            "telephone",
            "courriel",
            "codeTypologieNiveau1",
            "adresse",
        ],
        ADDITIONAL_PROPERTIES: False,
    },
}

Draft7Validator.check_schema(SCHEMA_ENTITE_REMETTANTE)
