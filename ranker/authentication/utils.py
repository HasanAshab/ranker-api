from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.signing import TimestampSigner
from knox.models import get_token_model
from ranker.users.models import User


AuthToken = get_token_model()
login_token_signer = TimestampSigner(salt=settings.TOKEN_LOGIN_SALT)


def generate_login_token(user):
    signature = login_token_signer.sign(user.username)
    token = urlsafe_base64_encode(signature)
    return token


def login_using_token(token):
    signature = urlsafe_base64_decode(token)
    username = login_token_signer.unsign(
        signature, max_age=settings.TOKEN_LOGIN_MAX_AGE
    )
    user = User.objects.get(username=username)
    _, api_token = AuthToken.objects.create(user)
    return user, api_token
