from django.db import models


class Process(models.Model):
    file_number = models.CharField(max_length=20, unique=True)
    open_date = models.DateField()
    plaintiff = models.CharField(max_length=100)
    defendant = models.CharField(max_length=100)
    procurator = models.CharField(max_length=100)

    def __str__(self):
        return self.file_number
    

class ProcessSnapshot(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    snapshot_date = models.DateField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f'{self.process.file_number} - {self.snapshot_date}'
