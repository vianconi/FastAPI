from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
import os

from project.database import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')


def create_access_token(user, days=30):
    data = {
        'user_id': user.id,
        'username': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(days=days)
    }

    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


def get_current_user(token: str = Depends(oauth2_schema)):
    data = decode_access_token(token)

    return User.select().where(User.id == data['user_id']).first()
