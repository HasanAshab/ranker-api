from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from knox.models import get_token_model
from ranker.users.models import User
from .exceptions import InvalidTokenException, TokenExpiredException

AuthToken = get_token_model()
login_token_signer = TimestampSigner(salt=settings.TOKEN_LOGIN_SALT)


def generate_login_token(user):
    signature = login_token_signer.sign(user.username)
    token = urlsafe_base64_encode(signature.encode("utf-8"))
    return token


def login_using_token(token):
    try:
        signature = urlsafe_base64_decode(token).decode("utf-8")
    except ValueError:
        raise InvalidTokenException

    try:
        username = login_token_signer.unsign(
            signature, max_age=settings.LOGIN_TOKEN_MAX_AGE
        )
    except SignatureExpired:
        raise TokenExpiredException
    except BadSignature:
        raise InvalidTokenException

    user = User.objects.get(username=username)
    _, api_token = AuthToken.objects.create(user)
    return user, api_token
