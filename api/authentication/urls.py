from django.urls import path, include
from allauth.headless.constants import Client
from allauth.headless.account import views as account_views
from allauth.headless.mfa import views as mfa_views

from allauth.headless.socialaccount import views as socialaccount_views

client = Client.APP
mfa_urlpatterns = [
    path(
        "authenticate/",
        mfa_views.AuthenticateView.as_api_view(client=client),
        name="authenticate",
    ),
    path(
        "reauthenticate/",
        mfa_views.ReauthenticateView.as_api_view(client=client),
        name="reauthenticate",
    ),
    path(
        "authenticators/",
        mfa_views.AuthenticatorsView.as_api_view(client=client),
        name="authenticators",
    ),
    path(
        "authenticators/totp/",
        mfa_views.ManageTOTPView.as_api_view(client=client),
        name="manage_totp",
    ),
    path(
        "authenticators/recovery-codes/",
        mfa_views.ManageRecoveryCodesView.as_api_view(client=client),
        name="manage_recovery_codes",
    ),
]

social_urlpatterns = [
    path(
        "providers/",
        socialaccount_views.ManageProvidersView.as_api_view(client=client),
        name="manage_providers",
    ),
    path(
        "provider/signup/",
        socialaccount_views.ProviderSignupView.as_api_view(client=client),
        name="provider_signup",
    ),
    path(
        "provider/token/",
        socialaccount_views.ProviderTokenView.as_api_view(client=client),
        name="provider_token",
    ),
]

urlpatterns = [
    path(
        "auth/signup/",
        account_views.SignupView.as_api_view(client=client),
        name="signup",
    ),
    path(
        "auth/login/",
        account_views.LoginView.as_api_view(client=client),
        name="login",
    ),
    path(
        "auth/reauthenticate/",
        account_views.ReauthenticateView.as_api_view(client=client),
        name="reauthenticate",
    ),
    path(
        "auth/session/",
        account_views.SessionView.as_api_view(client=client),
        name="current-session",
    ),
    path(
        "auth/email/verify/",
        account_views.VerifyEmailView.as_api_view(client=client),
        name="verify-email",
    ),
    path(
        "auth/password/reset/request/",
        account_views.RequestPasswordResetView.as_api_view(client=client),
        name="request-reset-password",
    ),
    path(
        "auth/password/reset/confirm/",
        account_views.ResetPasswordView.as_api_view(client=client),
        name="confirm-reset-password",
    ),
    path("auth/two-factor/", include(mfa_urlpatterns)),
    path("auth/social/", include(social_urlpatterns)),
]
