from django.db import models


class Process(models.Model):
    class Meta:
        verbose_name = "Proceso"
        verbose_name_plural = "Procesos"
        ordering = ["-open_date", "file_number"]

    file_number = models.CharField(
        verbose_name="Radicado",
        help_text="Número de radicado del proceso",
        max_length=100,
        unique=True,
    )
    open_date = models.DateField(
        verbose_name="Fecha de apertura",
        help_text="Fecha en que se abrió el proceso",
        null=True,
        blank=True,
    )
    plaintiff = models.CharField(
        verbose_name="Demandante",
        help_text="Nombre del demandante del proceso",
        max_length=300,
        null=True,
        blank=True,
    )
    defendant = models.CharField(
        verbose_name="Demandado",
        help_text="Nombre del demandado del proceso",
        max_length=300,
        null=True,
        blank=True,
    )
    procurator = models.CharField(
        verbose_name="Procurador",
        help_text="Nombre del procurador del proceso",
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.file_number


class ProcessSnapshot(models.Model):
    class Meta:
        verbose_name = "Captura de Proceso"
        verbose_name_plural = "Capturas de Procesos"
        ordering = ["-snapshot_date", "process__file_number"]

    process = models.ForeignKey(
        Process,
        verbose_name="Proceso",
        help_text="Proceso relacionado",
        on_delete=models.CASCADE,
    )
    snapshot_date = models.DateField(
        verbose_name="Fecha de captura",
        help_text="Fecha en que se tomó la captura del proceso",
        auto_now_add=True,
    )
    last_update = models.DateTimeField(
        verbose_name="Última actualización",
        help_text="Fecha y hora de la última actualización del proceso",
        auto_now=True,
    )

    def __str__(self):
        return f"{self.process.file_number} - {self.snapshot_date}"
