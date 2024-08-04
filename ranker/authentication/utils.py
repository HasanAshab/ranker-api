from django.conf import settings
from django.core.signing import TimestampSigner


login_token_signer = TimestampSigner(salt=settings.TOKEN_LOGIN_SALT)


def generate_login_token(user):
    return login_token_signer.sign(user.username)
