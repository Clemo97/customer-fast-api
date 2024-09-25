import os
import secrets
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from jose.exceptions import JWTError
import requests

# Load environment variables
load_dotenv()

# Environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
API_AUDIENCE = os.getenv("API_AUDIENCE")
CALLBACK_URL = os.getenv("CALLBACK_URL")
ALGORITHMS = os.getenv("ALGORITHMS")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://{AUTH0_DOMAIN}/authorize",
    tokenUrl=f"https://{AUTH0_DOMAIN}/oauth/token",
)

def get_auth0_public_key():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    return jwks["keys"][0]

public_key = get_auth0_public_key()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_token_from_code(code: str):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": CALLBACK_URL
    }
    response = requests.post(token_url, json=payload)
    return response.json()