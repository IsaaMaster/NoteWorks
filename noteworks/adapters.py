from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the social account is already linked, no further action needed
        if sociallogin.is_existing:
            return

        # Try to match an existing user by email
        email = sociallogin.user.email
        if email:
            try:
                existing_user = self.get_user_by_email(email)
                sociallogin.connect(request, existing_user)
                raise ImmediateHttpResponse(HttpResponseRedirect(""))
            except:
                pass

    def get_user_by_email(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.get(email=email)
