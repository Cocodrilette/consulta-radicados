from django.contrib import admin

from files_consultant import models as files_consultant_models
from files_consultant.actions import process as process_actions


@admin.register(files_consultant_models.Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = (
        "file_number",
        "last_update",
        "open_date",
        "plaintiff",
        "defendant",
        "procurator",
    )
    search_fields = ("file_number", "plaintiff", "defendant", "procurator")
    list_filter = ("open_date",)
    fieldsets = (
        (None, {"fields": ("file_number", "open_date")}),
        ("Parties", {"fields": ("plaintiff", "defendant", "procurator")}),
    )

    def last_update(self, obj):
        return (
            obj.processsnapshot_set.last().last_update
            if obj.processsnapshot_set.exists()
            else None
        )

    @admin.action(description="Consultar Radicado")
    def query_file_number(self, request, queryset):
        """
        Admin action to process selected snapshots.
        """
        try:
            process_actions.query_file_number(self, request, queryset)
        except Exception as e:
            self.message_user(
                request, f"Error processing snapshots: {str(e)}", level="error"
            )
            return

    actions = [query_file_number]


@admin.register(files_consultant_models.ProcessSnapshot)
class ProcessSnapshotAdmin(admin.ModelAdmin):
    list_display = ("process", "snapshot_date", "last_update")
    search_fields = ("process__file_number",)
    list_filter = ("snapshot_date", "last_update")
    fieldsets = ((None, {"fields": ("process", "last_update")}),)
