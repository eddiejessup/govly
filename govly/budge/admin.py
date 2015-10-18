from django.contrib import admin

from .models import Budget, Category


class CategoryInline(admin.TabularInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass
