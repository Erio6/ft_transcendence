# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.utils.http import http_date

@receiver(user_logged_in)
def set_jwt_cookies_on_login(sender, request, user, **kwargs):
    """
    Generate JWT tokens and set them in the cookies after user logs in.
    """
    print("Signal triggered for user:", user)
    refresh = RefreshToken.for_user(user)

    # Add tokens to the response cookies
    response = request.__dict__.get("_response", None)
    if response:
        # Set the access and refresh tokens as secure HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=False,
            secure=True,  # Ensure this is True in production for HTTPS
            samesite="Lax",
            expires=http_date(refresh.access_token.lifetime.total_seconds() + now().timestamp())
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=False,
            secure=True,
            samesite="Lax",
            expires=http_date(refresh.lifetime.total_seconds() + now().timestamp())
        )
