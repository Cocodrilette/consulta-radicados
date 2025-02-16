from django.contrib import admin
from files_consultant import models as files_consultant_models

@admin.register(files_consultant_models.Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('file_number', 'open_date', 'plaintiff', 'defendant', 'procurator')
    search_fields = ('file_number', 'plaintiff', 'defendant', 'procurator')
    list_filter = ('open_date',)
    fieldsets = (
        (None, {
            'fields': ('file_number', 'open_date')
        }),
        ('Parties', {
            'fields': ('plaintiff', 'defendant', 'procurator')
        }),
    )

@admin.register(files_consultant_models.ProcessSnapshot)
class ProcessSnapshotAdmin(admin.ModelAdmin):
    list_display = ('process', 'snapshot_date', 'last_update')
    search_fields = ('process__file_number',)
    list_filter = ('snapshot_date', 'last_update')
    fieldsets = (
        (None, {
            'fields': ('process', 'last_update')
        }),
    )