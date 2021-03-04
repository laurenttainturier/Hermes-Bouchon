import random
import re
from datetime import datetime
from typing import Sequence

from jsonschema import ValidationError


def optional_type(opt_type: dict):
    return {
        "anyOf": [
            opt_type,
            {
                TYPE: "null"
            }
        ]
    }


TYPE = "type"
OBJECT = "object"
ARRAY = "array"
PROPERTIES = "properties"
NUMBER = "number"
STRING = "string"
BOOLEAN = "boolean"
INTEGER = "integer"
ITEMS = "items"
FORMAT = "format"
DATE_TIME = "date-time"
REQUIRED = "required"
ADDITIONAL_PROPERTIES = "additionalProperties"

STRING_TYPE = {
    "type": STRING
}

OPTIONAL_STRING_TYPE = optional_type(STRING_TYPE)

BOOLEAN_TYPE = {
    "anyOf": [
        {
            "type": BOOLEAN
        }, {
            "enum": ["true", "false"]
        }
    ]
}

OPTIONAL_BOOLEAN_TYPE = optional_type(STRING_TYPE)

INTEGER_TYPE = {
    "anyOf": [
        {
            "type": INTEGER
        }, {
            "type": STRING,
            "pattern": "^\\d+$"
        }
    ]
}

DATE_TIME_TYPE = {
    **STRING_TYPE,
    "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.?\\d*Z?$"
}

HERMES_STATUT = (
    "Proposé",
    "Refusé",
    "A lotir",
    "Loti",
    "Invendu",
    "Vendu à régler",
    "Vendu à enlever",
    "Enlevé",
    "Recevable à récoler",
    "Détruit",
    "Manquant",
    "Restitué",
    "En cours de transfert",
    "Archivé intermédiaire",
    "En attente de complément",
    "En cours de vente",
)


def random_string(length: int, seq: Sequence[str]):
    return "".join(random.choice(seq) for _ in range(length))


def extract_datetime(value: str) -> datetime:
    datetime_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    match = re.search(datetime_pattern, value)
    if match:
        return datetime.strptime(match.group(0), "%Y-%m-%dT%H:%M:%S")

    raise ValidationError(f"Value {value} cannot be converted into datetime")
