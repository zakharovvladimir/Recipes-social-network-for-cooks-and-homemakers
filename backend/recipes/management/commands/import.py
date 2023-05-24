"""Import.py."""
import csv

from django.core.management import BaseCommand
from recipes.models import Ingredients

SOURCES = {
    Ingredients: 'ingredients.csv',
}


class Command(BaseCommand):
    """A subclass of Django's BaseCommand."""

    help = 'CSV Import'

    def handle(self, *args, **options):
        """Import CSVs when the command is entered."""
        for model, source in SOURCES.items():
            with open(
                f'/app/static/data/{source}',
                    encoding='utf-8') as f:
                """Reading object as a dictionary."""
                reader = csv.DictReader(f)
                model.objects.bulk_create(
                    model.create(**data) for data in reader
                    )
