# signals.py

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib import messages

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    messages.success(request, "Has iniciado sesión satisfactoriamente.")
    logger.info(f"El usuario {user.username} ha iniciado sesión.")

@receiver(user_login_failed)
def log_user_login_failed(sender,request, user=None, **kwargs):
    """ log user login to user log """
    if user:
        logger.info('%s falló al iniciar sesión', user)
    else:
        logger.error('Fallo al iniciar sesión; usuario desconocido')
    
    messages.warning(request, "Error al iniciar sesión. Por favor, revisa tus credenciales.")
        

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """ log user logout to user log """
    logger.info('%s ha cerrado sesión', user)

    messages.success(request, "Has cerrado sesión satisfactoriamente.")