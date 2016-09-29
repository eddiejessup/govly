from decimal import Decimal
from django.db import models
from djangoyearlessdate.models import YearField
from mptt.models import MPTTModel, TreeForeignKey


def all_same(items):
    return len(set(items)) == 1


class Quantifiable(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BreakdownMethod(models.Model):

    attribute = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute


class Sphere(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def quantified(self):
        return set(quantification.quantifiable
                   for quantification in self.quantification_set.all())

    def quantify(self, quantifiable):
        return self.quantification_set.filter(quantifiable=quantifiable)

    def quantify_then_breakdown(self, quantifiable, attribute):
        for quantification in self.quantify(quantifiable):
            try:
                yield quantification.breakdown(attribute)
            except Breakdown.DoesNotExist:
                continue

    def breakdown_methods_for(self, quantifiable):
        breakdown_methods = set()
        for quantification in self.quantify(quantifiable):
            breakdown_methods.update(quantification.breakdown_methods)
        return breakdown_methods


class Quantification(models.Model):

    sphere = models.ForeignKey(Sphere)
    quantifiable = models.ForeignKey(Quantifiable)
    unit = models.ForeignKey(Unit)
    number = models.DecimalField(max_digits=8, decimal_places=1)
    year = YearField()

    def __str__(self):
        return "{} in {} ({}): {} {}".format(self.quantifiable, self.sphere,
                                             self.year, self.number, self.unit)

    def breakdown(self, breakdown_method_id):
        return self.breakdown_set.get(breakdown_method=breakdown_method_id)

    @property
    def breakdown_methods(self):
        breakdown_methods = set()
        for breakdown in self.breakdown_set:
            breakdown_methods.add(breakdown.breakdown_method)
        return breakdown_methods


class Category(MPTTModel):

    name = models.CharField(max_length=100)
    fraction = models.DecimalField(max_digits=5, decimal_places=3,
                                   null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children_set', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.path_name

    @property
    def percentage(self):
        return self.fraction * Decimal(100.0)

    @property
    def children(self):
        return self.get_children().all()

    @property
    def descendants(self):
        return self.get_descendants().all()

    @property
    def root(self):
        return self.get_root()

    @property
    def is_root(self):
        return self.is_root_node()

    @property
    def is_leaf(self):
        return self.is_leaf_node()

    @property
    def breakdown(self):
        return Breakdown.objects.get(root_category=self.root)

    @property
    def accounted_fraction(self):
        return sum(child.fraction for child in self.children)

    @property
    def unaccounted_fraction(self):
        if self.fraction is not None:
            return self.fraction - self.accounted_fraction
        else:
            return Decimal(0.0)

    @property
    def path_name(self):
        ancs = self.get_ancestors()
        names = [anc.name for anc in ancs] + [self.name]
        return '/'.join(names)

    @property
    def other_treemap_data(self):
        other_data = {}
        other_data['data'] = {'name': 'Other',
                              'fraction': self.unaccounted_fraction,
                              'description': ''}
        other_data['children'] = []
        return other_data

    @property
    def treemap_data(self):
        data = {}
        data['data'] = {'name': self.name,
                        'fraction': self.fraction,
                        'description': self.description}
        data['children'] = [child.treemap_data for child in self.children]
        if self.unaccounted_fraction > 0.0:
            data['children'].append(self.other_treemap_data)
        return data

    @staticmethod
    def multi_other_treemap_data(categories):
        other_data = {}
        other_data['data'] = {'name': 'Other',
                              'fraction': [category.unaccounted_fraction
                                           for category in categories],
                              'description': ''}
        other_data['children'] = []
        return other_data

    @staticmethod
    def collect_children(categories):
        children_sets = {}
        for category in categories:
            for child in category.children:
                children_sets.setdefault(child.name, [])
                children_sets[child.name].append(child)
        return children_sets.values()

    @classmethod
    def multi_treemap_data(cls, categories):
        categories = list(categories)
        data = {}
        # Root nodes *can* have different names to identify them
        is_roots = all(c.is_root for c in categories)
        if not is_roots and not all_same(category.name for category in categories):
            raise ValueError('Can only merge treemaps with the same names {}'.format(list(category.name for category in categories)))
        name = next(iter(categories)).name
        if not all_same(category.description for category in categories):
            raise ValueError('Can only merge treemaps with the same description')
        description = next(iter(categories)).description
        fractions = [category.fraction for category in categories]
        data['data'] = {'name': name,
                        'fraction': fractions,
                        'description': description}
        data['children'] = [cls.multi_treemap_data(children)
                            for children in cls.collect_children(categories)]
        unaccounted_fractions = [category.unaccounted_fraction
                                 for category in categories]
        if max(unaccounted_fractions) > 0.0:
            data['children'].append(cls.multi_other_treemap_data(categories))
        return data


class Breakdown(models.Model):

    quantification = models.ForeignKey(Quantification)
    root_category = models.OneToOneField(Category, blank=True, null=True)
    breakdown_method = models.ForeignKey(BreakdownMethod)

    def __str__(self):
        return 'Breakdown of {} by {}'.format(self.quantification,
                                              self.breakdown_method.attribute)

    @property
    def treemap_data(self):
        return {
            'breakdown_attribute': self.breakdown_method.attribute,
            'quantifiable': self.quantification.quantifiable.name,
            'unit': self.quantification.unit,
            'number': self.quantification.number,
            'year': self.quantification.year,
            'sphere': self.quantification.sphere.name,
            'treemap_data': self.root_category.treemap_data
            }

    @staticmethod
    def multi_treemap_data(breakdowns):
        breakdowns = list(breakdowns)
        if not all_same(b.breakdown_method.attribute for b in breakdowns):
            raise ValueError('Can only merge breakdowns by the same attribute')
        breakdown_attribute = next(iter(breakdowns)).breakdown_method.attribute
        if not all_same(b.quantification.quantifiable.name
                        for b in breakdowns):
            raise ValueError('Can only merge breakdowns of the same quantifiable')
        quantifiable_name = next(iter(breakdowns)).quantification.quantifiable.name
        if not all_same(b.quantification.unit for b in breakdowns):
            raise ValueError('Can only merge breakdowns using the same unit')
        quantification_unit = next(iter(breakdowns)).quantification.unit

        quantification_numbers = [b.quantification.number for b in breakdowns]
        quantification_years = [b.quantification.year for b in breakdowns]
        sphere_names = [b.quantification.sphere.name for b in breakdowns]
        root_categories = [breakdown.root_category for breakdown in breakdowns]
        multi_treemap_data = Category.multi_treemap_data(root_categories)
        return {
            'breakdown_attribute': breakdown_attribute,
            'quantifiable': quantifiable_name,
            'unit': quantification_unit.name,
            'number': quantification_numbers,
            'year': quantification_years,
            'sphere': sphere_names,
            'treemap_data': multi_treemap_data
        }
