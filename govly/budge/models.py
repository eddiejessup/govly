from django.db import models
from djangoyearlessdate.models import YearField


class Category(models.Model):
    name = models.CharField(max_length=200)
    mega_pounds = models.DecimalField(max_digits=8, decimal_places=1)
    parent = models.ForeignKey('self', blank=True, null=True)

    @classmethod
    def all_roots(cls):
        return cls.objects.filter(parent__isnull=True)

    @property
    def children(self):
        return self.__class__.objects.filter(parent__pk=self.pk)

    @property
    def root(self):
        category = self
        while True:
            if category.parent is None:
                return category
            category = category.parent

    @property
    def budget(self):
        root = self.root
        return Budget.objects.get(root_category=root)

    def __str__(self):
        return u'{}: £{} mil'.format(self.name, self.mega_pounds)


class Budget(models.Model):
    name = models.CharField(max_length=200)
    year = YearField()
    is_in_real_terms = models.BooleanField()
    root_category = models.ForeignKey(Category, blank=True, null=True)

    @property
    def real_terms_str(self):
        return u'adjusted' if self.is_in_real_terms else u'unadjusted'

    def __str__(self):
        return u'{} in {} ({})'.format(self.name, self.year,
                                       self.real_terms_str)
