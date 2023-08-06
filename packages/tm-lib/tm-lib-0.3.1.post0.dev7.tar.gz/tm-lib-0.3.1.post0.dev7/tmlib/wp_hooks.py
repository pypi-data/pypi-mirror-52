import jwt
import requests
from tmlib.settings import Settings
from connexion import NoContent, request
from tmlib.models import WPJWT

wp_url = f"{Settings.WP_HOST}/wp-json/"

def request_auth_token():
    url = f"{wp_url}jwt-auth/v1/token"
    response = requests.request(
        "POST", 
        url, 
        data={
            "username": Settings.WP_USER, "password": Settings.WP_PASSWORD
        }
    )
    reponse_json = response.json()
    return reponse_json.get("token")

def execute_request():
    pass

def get_auth_token():
    token = WPJWT.objects(username=Settings.WP_USER).first()
    try:
        print(token.token)
        jwt.decode(token.token.encode('utf-8'), Settings.WP_JWT_SECRET)
    except Exception as e:
        print(e)
        token = request_auth_token()
        WPJWT.objects(username=Settings.WP_USER).update_one(set__token=token, upsert=True)
    decoded_token = jwt.decode(token.token.encode('utf-8'), Settings.WP_JWT_SECRET)
    print(decoded_token)
    return decoded_token

def trigger():
    print(request.headers)
    print(request.json)
    print(request.args)
    token = get_auth_token()
    print(token)
    return NoContent, 200
