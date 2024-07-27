import csv
import logging
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        model = None

        logger.info(f"Starting import for model {model_name} from file {file_path}")

        # Find the model
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            error_message = f'Model "{model_name}" not found in any app!'
            logger.error(error_message)
            raise CommandError(error_message)

        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        logger.info(f"Model fields: {model_fields}")

        # Open and read the CSV file
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                csv_header = reader.fieldnames
                logger.info(f"CSV header: {csv_header}")

                if set(csv_header) != set(model_fields):
                    error_message = f"CSV file doesn't match with the {model_name} table fields."
                    logger.error(error_message)
                    raise DataError(error_message)

                for row in reader:
                    model.objects.create(**row)
                    logger.info(f"Inserted row: {row}")

            self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
            logger.info("Data inserted successfully")

        except Exception as e:
            error_message = f"Error during import: {e}"
            logger.error(error_message)
            raise CommandError(error_message)
