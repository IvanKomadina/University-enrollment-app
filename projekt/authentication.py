from django.contrib.auth.hashers import check_password
from app.models import Korisnici

class Authentication(object):
    def authenticate(self, username=None, password=None):
        try:
            user = Korisnici.objects.get(username=username)
        except:
            return None
        password_valid = check_password(password, user.password)
        if username and password_valid:
            user = Korisnici.objects.get(username=username)
            return user
        return None