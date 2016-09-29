import decimal
from django.core.management.base import BaseCommand
import yaml
from budge.models import (Quantification, Breakdown,
                          BreakdownMethod, Category)

DATA_FIELDS = ('description', 'f', 'n')


def create_descendants(data, name, parent, total=None):
    # If the actual fraction is stated, use that
    if 'n' in data:
        fraction = decimal.Decimal(data['n']) / total
    else:
        fraction = None
    description = data.get('description')

    category = Category.objects.create(name=name, fraction=fraction,
                                       description=description,
                                       parent=parent)
    categories = [category]
    for key in data:
        if key in DATA_FIELDS:
            continue
        child_categories = create_descendants(data=data[key], name=key,
                                              parent=category, total=total)
        categories.extend(child_categories)
    return categories


def get_total(data):
    if 'n' in data:
        return data['n']
    else:
        return sum(get_total(child) for child in data.values()
                   if child not in DATA_FIELDS)


class Command(BaseCommand):
    help = 'Create a category tree from a file'

    def add_arguments(self, parser):
        parser.add_argument('file_name')
        parser.add_argument('root_name')

    def handle(self, **options):
        with open(options['file_name']) as f:
            data = yaml.safe_load(f)
        total = decimal.Decimal(get_total(data))
        print('total: {}'.format(total))
        create_descendants(data=data, name=options['root_name'], parent=None,
                           total=total)
