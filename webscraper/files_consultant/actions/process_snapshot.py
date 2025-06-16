from django.contrib import messages
from django.utils.timezone import datetime

from files_consultant import models as files_consultant_models
from files_consultant.utils import rama_judicial as rama_judicial_utils


def query_file_number(
    _, request, queryset: list[files_consultant_models.ProcessSnapshot]
):
    """
    Admin action to process selected snapshots.
    """
    if queryset.count() == 0:
        messages.error(request, "No snapshots selected.")
        return

    processed_snapshots = []
    for snapshot in queryset:
        data_list = rama_judicial_utils.get_radicado_data(
            [snapshot.process.file_number]
        )

        if data_list and len(data_list) > 0:
            radicado_data = data_list[0]

            snapshot.process.open_date = datetime.strptime(
                radicado_data.open_date, "%Y-%m-%d"
            ).date()

            parties = rama_judicial_utils.extract_legal_parties(
                radicado_data.legal_parties_str
            )
            snapshot.process.plaintiff = (
                parties.plaintiff.title() if parties.plaintiff else None
            )
            snapshot.process.defendant = (
                parties.defendant.title() if parties.defendant else None
            )
            snapshot.process.procurator = (
                parties.procurator.title() if parties.procurator else None
            )

            snapshot.save()

            files_consultant_models.ProcessSnapshot.objects.create(
                process=snapshot.process,
                last_update=datetime.strptime(
                    f"{radicado_data.last_update_date}", "%Y-%m-%d"
                ),
            )

            processed_snapshots.append(snapshot.process.file_number)

    if processed_snapshots:
        messages.success(
            request,
            f"Snapshots processed successfully for processes: {', '.join(processed_snapshots)}",
        )
    else:
        messages.error(request, "No snapshots were processed. Please check the data.")
