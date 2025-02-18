from django.db import models


class Process(models.Model):
    file_number = models.CharField(max_length=100, unique=True)
    open_date = models.DateField(null=True, blank=True)
    plaintiff = models.CharField(
        max_length=300, null=True, blank=True, help_text="Demandante")
    defendant = models.CharField(
        max_length=300, null=True, blank=True, help_text="Demandado")
    procurator = models.CharField(
        max_length=300, null=True, blank=True, help_text="Procurador")

    def __str__(self):
        return self.file_number


class ProcessSnapshot(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    snapshot_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField()

    def __str__(self):
        return f'{self.process.file_number} - {self.snapshot_date}'
