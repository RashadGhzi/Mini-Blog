from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache


@receiver(user_logged_in, sender=User)
def login_post(sender, request, user, **kwargs):
    print("sender is : ", sender)
    print("request is : ", request)
    print('user is : ', user)
    loginCacheGet = cache.get(user.username, default=0, version=user.id)
    loginCount = loginCacheGet + 1
    cache.set(user.username, loginCount, timeout=None, version=user.id)
    print(loginCount)
    ip = request.META.get('REMOTE_ADDR')
    print('ip is : ', ip)
    request.session['ip'] = ip
    print(request.session.get('ip', False))
