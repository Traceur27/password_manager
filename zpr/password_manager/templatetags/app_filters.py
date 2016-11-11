from django import template
from datetime import date, timedelta
from cryptopp import passwordXor
from password_manager.models import UserExtension
import base64

register = template.Library()

@register.simple_tag
def hidePassword(encryptedPassword, masterPassword):
    print(masterPassword)
    algorithm = UserExtension.objects.get(user=encryptedPassword.user).encryption_algorithm
    decodedPass = base64.b64decode(encryptedPassword.password)
    if algorithm == 'xor':
        return passwordXor(decodedPass, masterPassword)
    else:
        hidden = str(base64.b64encode(decodedPass.decode('ascii')).decode("ascii") )
    return hidden

