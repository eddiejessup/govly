from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import (Sphere, Quantification, Category, BreakdownMethod,
                     Breakdown, Quantifiable, Unit)


@admin.register(Quantifiable)
class QuantifiableAdmin(admin.ModelAdmin):
    pass


@admin.register(Sphere)
class SphereAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Quantification)
class QuantificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
        pass


@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakdownMethod)
class BreakdownMethodAdmin(admin.ModelAdmin):
    pass
