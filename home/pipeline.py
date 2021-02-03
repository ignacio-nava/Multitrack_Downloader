from django.contrib.auth.models import User
from .models import SocialUser

def add_avatar(backend, user, response, *args, **kwargs):
    u = User.objects.get(username=user)
    if backend.name == 'google-oauth2' and u.is_authenticated:
        if not hasattr(u, 'socialuser'):
            social_u = SocialUser.objects.create(user=u)
        else:
            social_u = SocialUser.objects.get(pk=u.socialuser.id)
        social_u.avatar_url = response['picture']
        social_u.save()
