import re
import difflib
import string
import pandas as pd

from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError, FormatChecker

from enlevement_vehicule import SCHEMA_ENLEVEMENT_VEHICULE
from entite_remettante import SCHEMA_ENTITE_REMETTANTE
from lieu_depot import SCHEMA_LIEU_DEPOT
from recuperation_bien import SCHEMA_RECUPERATION_BIEN
from remise_domaine import SCHEMA_REMISE_DOMAINE
from utils import random_string, HERMES_STATUT, extract_datetime

app = Flask(__name__)


def process_request(old_func):
    @wraps(old_func)
    def new_func(*args, **kwargs):
        try:
            raw_response = old_func(*args, **kwargs)
            app.logger.info("Returning response: " + str(raw_response))
            return jsonify(raw_response)
        except ValidationError as e:
            return jsonify({
                "code": 400,
                "message": "La requête transmise est incorrecte (voir section détail). Veuillez vérifier et soumettre à nouveau votre demande.",
                "horodatage": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "detail": [{
                    "id": random_string(10, string.digits),
                    "errors": [{
                        "code": "Invalid json: " + e.message,
                        "message": re.sub('\n+', '\n', str(e))
                    }]
                }]
            }), 400

    return new_func


def validate_body(schema: dict):
    def decorator(old_func):
        @wraps(old_func)
        def new_func(*args, **kwargs):
            request_data = request.json
            app.logger.info("Receiving body: " + str(request_data))
            validate(instance=request_data, schema=schema, format_checker=FormatChecker())
            return old_func(request_data, *args, **kwargs)

        return new_func

    return decorator


@app.route('/hmsa/api/v1/referentiels/entitesremettantes', methods=['POST'])
@process_request
@validate_body(SCHEMA_ENTITE_REMETTANTE)
def entite_remettante(data):
    return [{
        "idCorrelation": entite['idCorrelation'],
        "id": random_string(10, string.digits)
    } for entite in data]


@app.route('/hmsa/api/v1/referentiels/lieux-de-depot', methods=['POST'])
@process_request
@validate_body(SCHEMA_LIEU_DEPOT)
def lieu_depot(data):
    return [{
        "idCorrelation": entite['idCorrelation'],
        "id": random_string(10, string.digits)
    } for entite in data]


@app.route('/hmsa/api/v1/vehicules', methods=['POST'])
@process_request
@validate_body(SCHEMA_REMISE_DOMAINE)
def remise_domaine(data):
    new_bien = {
        "id_correlation": data['idCorrelation'],
        "id": int(random_string(10, string.digits))
    }
    dataframe = read_dataframe()
    dataframe = dataframe.append(new_bien, ignore_index=True)
    save_dataframe(dataframe)

    return {
        **new_bien,
        "dateDemandePriseEnCharge": datetime.now().isoformat(),
    }


@app.route('/hmsa/api/v1/vehicules/_search', methods=['POST'])
@process_request
@validate_body(SCHEMA_RECUPERATION_BIEN)
def recuperation_biens(data):
    date_debut = extract_datetime(data['dateDebut'])
    date_fin = extract_datetime(data['dateFin'])

    df = read_dataframe()
    df['dateMaj'] = pd.to_datetime(df['dateMaj'])

    mask = (df['dateMaj'] > date_debut) & (df['dateMaj'] < date_fin)
    df = df.loc[mask]

    return [{
        "idCorrelation": row['id_correlation'],
        "id": row['id'],
        "statut": row['statut'],
        "dateReception": datetime.now().isoformat(),
        "dateQualification": "2021-03-04",
        "dateVente": "2021-03-04",
        "datePaiement": "2021-03-04",
        "raisonSocialeSociete": None,
        "prenomClient": None,
        "nomClient": None,
        "prixFrappe": "1000.00",
    } for _, row in df.iterrows()]


@app.route('/hmsa/api/v1/vehicules/<id_bien>/enlevement', methods=['PUT'])
@process_request
@validate_body(SCHEMA_ENLEVEMENT_VEHICULE)
def enlevement_vehicule(data, id_bien: str):
    return ""


@app.route('/bien/<id_correlation_dossier>/update', methods=['GET'])
def update_bien(id_correlation_dossier: str):
    new_statut = request.args.get('statut')
    if new_statut not in HERMES_STATUT:
        most_similar = ", ".join(difflib.get_close_matches(new_statut, HERMES_STATUT))
        return f"Le statut n'a pas été reconnu. Les statuts les plus similaires sont : {most_similar}", 422

    dataframe = read_dataframe()
    row_with_same_id = dataframe['id_correlation'] == f"SIF{id_correlation_dossier}"
    match_df = dataframe[row_with_same_id]

    if match_df.shape[0] == 0:
        return f"Le dossier avec pour id de corrélation {id_correlation_dossier} n'a pas été remis au domaine", 422

    now = datetime.now().isoformat()
    dataframe.loc[row_with_same_id, ['statut', 'dateMaj']] = new_statut, now
    save_dataframe(dataframe)

    return f"Le bien avec l'id {id_correlation_dossier} a été mis à jour à {now} avec le statut {new_statut}."


@app.route('/reset', methods=['GET'])
def reset():
    dataframe = create_dataframe()
    save_dataframe(dataframe)

    return "Le bouchon a été réinitialisé"


def read_dataframe() -> pd.DataFrame:
    try:
        return pd.read_csv("static/biens.csv", header=0)
    except FileNotFoundError:
        create_dataframe()


def save_dataframe(df: pd.DataFrame):
    df.to_csv("static/biens.csv", header=True, index=False)


def create_dataframe() -> pd.DataFrame:
    return pd.DataFrame(columns=['id_correlation', 'id', 'statut', 'dateMaj'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
