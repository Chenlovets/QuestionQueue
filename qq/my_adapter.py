import re

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.shortcuts import render


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data['email'].lower()
        if not re.match('.*cmu.edu$', email):
            messages.warning(request, 'You must log in with CMU account.')
            raise ImmediateHttpResponse(render(request, 'qq/index.html'))
        else:
            return