from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from files_consultant import models as files_consultant_models
from files_consultant.utils import rama_judicial as rama_judicial_utils


@receiver(post_save, sender=files_consultant_models.Process)
def fetch_process_data(sender, instance, created, **kwargs):
    """
    Signal to fetch process data from Rama Judicial when a new Process is created
    """
    print(f"Signal received for Process {instance.file_number}")

    if created:
        print(f"Fetching data for process {instance.file_number}...")
        try:
            # Get data from Rama Judicial
            radicado_data_list = rama_judicial_utils.get_radicado_data([instance.file_number])
            print(f"Data fetched for process {instance.file_number}: {radicado_data_list}")
            
            if radicado_data_list and len(radicado_data_list) > 0:
                radicado_data = radicado_data_list[0]
                
                # Update Process instance
                instance.open_date = datetime.strptime(radicado_data.open_date, '%d/%m/%Y').date()
                print(f"Open date updated to {instance.open_date}")
                
                # Extract plaintiff and defendant from legal_parties_str
                parties = rama_judicial_utils.extract_legal_parties(radicado_data.legal_parties_str)
                print(f"Plaintiff: {parties.plaintiff}\nDefendant: {parties.defendant}\nProcurator: {parties.procurator}")
                instance.plaintiff = parties.plaintiff
                instance.defendant = parties.defendant
                instance.procurator = parties.procurator

                # Save the updated Process instance
                instance.save()
                
                # Create ProcessSnapshot
                files_consultant_models.ProcessSnapshot.objects.create(
                    process=instance,
                    last_update=datetime.strptime(f"{radicado_data.last_update_date}", '%d/%m/%Y'),
                )
                print(f"ProcessSnapshot created for process {instance.file_number}")
                
        except Exception as e:
            print(f"Error fetching data for process {instance.file_number}: {e}")