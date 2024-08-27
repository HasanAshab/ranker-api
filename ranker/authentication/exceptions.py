from rest_framework.exceptions import ValidationError


class InvalidTokenException(ValidationError):
    default_detail = "Invalid token."
    default_code = "invalid_token"


class TokenExpiredException(ValidationError):
    default_detail = "Token expired."
    default_code = "token_expired"
