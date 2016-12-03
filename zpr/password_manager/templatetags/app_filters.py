from django import template
from datetime import date, timedelta
from cryptopp import passwordXor
from password_manager.models import UserExtension
import base64

register = template.Library()


@register.simple_tag
def hidePassword(encryptedPassword, masterPassword):
    encryptedPassword.decrypt(masterPassword)
    return base64.b64encode(encryptedPassword.password)
