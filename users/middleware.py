from social_django.middleware import SocialAuthExceptionMiddleware


class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        # Customize the message that will be shown to the user
        return f"Custom error: {str(exception)}"

    def get_redirect_uri(self, request, exception):
        # Customize the URL where the user should be redirected after an error
        return "/custom-error-url/"  # Replace with your desired redirect URL
