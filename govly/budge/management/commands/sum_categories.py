import decimal
import yaml
from django.core.management.base import BaseCommand
from ._utils import get_total


class Command(BaseCommand):
    help = 'Add a category tree of numbers in a file'

    def add_arguments(self, parser):
        parser.add_argument('file_name')

    def handle(self, **options):
        with open(options['file_name']) as f:
            data = yaml.safe_load(f)
        print('total: {}'.format(decimal.Decimal(get_total(data))))
