from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . import models


def home(request):
    return render(request, 'budge/home.html',
                  {'budgets': models.Budget.objects.all()})


def children(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id)
    return render(request, 'budge/children.html',
                  {'budget': category.budget, 'category': category,
                   'children': category.children})
