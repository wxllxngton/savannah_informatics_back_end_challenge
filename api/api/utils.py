import os
import json
import jwt
import requests
from django.contrib.auth import authenticate
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_api_identifier = os.getenv("AUTH0_API_ID")

def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username

def jwt_decode_token(token):
    # API Domain
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(auth0_domain)).json()
    # jwks = requests.get('https://{}/.well-known/jwks.json'.format(auth0_domain)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format(auth0_domain)
    return jwt.decode(token, public_key, audience=auth0_api_identifier, issuer=issuer, algorithms=['RS256'])
