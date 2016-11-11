from django import template
from datetime import date, timedelta
from cryptopp import passwordXor
from password_manager.models import UserExtension
import base64

register = template.Library()


@register.inclusion_tag("hidden-password.html")
def hidePassword(encryptedPassword, masterPassword):
    algorithm = UserExtension.objects.get(user=encryptedPassword.user).encryption_algorithm
    tag = "<span real='"
    if algorithm == 'xor':
        hidden = str(base64.b64encode(passwordXor(encryptedPassword.password, masterPassword).encode()).decode("utf-8") )
    else:
        hidden = str(base64.b64encode(encryptedPassword.password.encode()).decode("utf-8") )
    return {'encoded': hidden}

