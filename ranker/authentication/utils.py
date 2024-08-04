from django.conf import settings
from django.core.signing import TimestampSigner
from knox.models import get_token_model
from ranker.users.models import User


AuthToken = get_token_model()
login_token_signer = TimestampSigner(salt=settings.TOKEN_LOGIN_SALT)


def generate_login_token(user):
    return login_token_signer.sign(user.username)


def login_using_token(token):
    username = login_token_signer.unsign(
        token, max_age=settings.TOKEN_LOGIN_MAX_AGE
    )
    user = User.objects.get(username=username)
    _, api_token = AuthToken.objects.create(user)
    return user, api_token
