from django.apps import AppConfig


class FilesConsultantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files_consultant'

    def ready(self):
        print("FilesConsultantConfig ready")
        import files_consultant.signals  # noqa