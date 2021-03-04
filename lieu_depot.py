from jsonschema import Draft7Validator

from utils import *

SCHEMA_LIEU_DEPOT = {
    TYPE: ARRAY,
    ITEMS: {
        TYPE: OBJECT,
        PROPERTIES: {
            "trigrammeSIP": STRING_TYPE,
            "idCorrelation": STRING_TYPE,
            "idEntiteRemettante": INTEGER_TYPE,
            "nomOrganisme": STRING_TYPE,
            "coordonneesGPS": STRING_TYPE,
            "courriel": STRING_TYPE,
            "telephone": STRING_TYPE,
            "telephoneMobile": STRING_TYPE,
            "horaireAppel": STRING_TYPE,
            "horaireAccueilPhysique": STRING_TYPE,
            "adresse": {
                TYPE: OBJECT,
                PROPERTIES: {
                    "codePostal": STRING_TYPE,
                    "ville": STRING_TYPE,
                    "numVoie": INTEGER_TYPE,
                    "indiceDeRepetition": STRING_TYPE,
                    "libelleVoie": STRING_TYPE,
                    "complementAdresse": STRING_TYPE,
                    "estEnFrance": BOOLEAN_TYPE,
                    "paysEtranger": STRING_TYPE,
                },
                REQUIRED: [
                    "codePostal",
                    "ville",
                    "numVoie",
                    "libelleVoie",
                    "estEnFrance",
                ],
                ADDITIONAL_PROPERTIES: False
            },
            "nomResponsable": STRING_TYPE,
            "telephoneResponsable": STRING_TYPE,
            "telephoneMobileResponsable": STRING_TYPE,
            "horaireAppelResponsable": STRING_TYPE,
            "horaireAccueilPhysiqueResponsable": STRING_TYPE,
            "courrielResponsable": STRING_TYPE,
        },
        REQUIRED: [
            "trigrammeSIP",
            "idCorrelation",
            "idEntiteRemettante",
            "courriel",
            "telephone",
            "horaireAppel",
            "horaireAccueilPhysique",
            "adresse",
            "nomResponsable",
            "telephoneResponsable",
            "horaireAppelResponsable",
            "horaireAccueilPhysiqueResponsable",
            "courrielResponsable",
        ],
        ADDITIONAL_PROPERTIES: False
    },

}

Draft7Validator.check_schema(SCHEMA_LIEU_DEPOT)
