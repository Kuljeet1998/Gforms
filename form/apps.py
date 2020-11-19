from django.apps import AppConfig


class FormConfig(AppConfig):
    name = 'form'

    def ready(self):
    	import form.signals