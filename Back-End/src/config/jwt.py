from jwt import encode
from os import getenv
from datetime import datetime, timedelta

def expiracionToken(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

def create_token(user):
    try:
        expiration_time = expiracionToken(1)
        payload = {
            "id": str(user['_id']),
            "email": user['email'],
            "role": user["role"],
            "exp": expiration_time
        }
        token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
        return token
    except Exception as err:
        print(err)
        return err