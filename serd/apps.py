from tabnanny import verbose
from django.apps import AppConfig

class serdConfig(AppConfig):
    name = 'serd'
    verbose_name = 'SERD'
    def ready(self) -> None:
        from .signals import  delete_handler, save_handler
