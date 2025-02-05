# middleware.py
from rest_framework_simplejwt.tokens import RefreshToken

class AttachResponseMiddleware:
    """
    Middleware to intercept the final response and set JWT cookies
    if the user is authenticated.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request and get the response
        response = self.get_response(request)

        # If the user is authenticated and JWT cookies are not set, add them
        if request.user.is_authenticated and "access_token" not in request.COOKIES:
            refresh = RefreshToken.for_user(request.user)
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=False,
                secure=True,  # Use True in production
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=False,
                secure=True,  
                # Use True in production
                samesite="Lax"
            )

        return response
