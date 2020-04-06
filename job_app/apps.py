from django.apps import AppConfig


class JobAppConfig(AppConfig):
    name = 'job_app'
    def ready(self):
        import job_app.signals
    
    
