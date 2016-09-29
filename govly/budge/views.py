from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . import models


def spheres(request):
    return render(request, 'budge/spheres.html',
                  {'spheres': models.Sphere.objects.all()})


def sphere_quantifiables(request, sphere_id):
    sphere = get_object_or_404(models.Sphere, pk=sphere_id)
    quantifiables = sphere.quantified
    quantifiables_info = []
    for quantifiable in quantifiables:
        quantifiable_info = {
            {'quantifiable': quantifiable,
             'breakdown_methods': sphere.breakdown_methods_for(quantifiable),
             }
        }
        quantifiables_info.append(quantifiable_info)
    return render(request, 'budge/sphere_quantifiables.html',
                  {'quantifiables_info': quantifiables_info,
                   'sphere': sphere})


def sphere_quantifications(request, sphere_id, quantifiable_id):
    sphere = get_object_or_404(models.Sphere, pk=sphere_id)
    quantifiable = get_object_or_404(models.Quantifiable, pk=quantifiable_id)
    quantifications = sphere.quantify(quantifiable_id)
    return render(request, 'budge/sphere_quantifications.html',
                  {'quantifications': quantifications,
                   'quantifiable': quantifiable,
                   'sphere': sphere})


def sphere_breakdowns_treemap(request, sphere_id, quantifiable_id,
                              breakdown_method_id):
    sphere = get_object_or_404(models.Sphere, pk=sphere_id)
    quantifiable = get_object_or_404(models.Quantifiable, pk=quantifiable_id)
    breakdown_method = get_object_or_404(models.BreakdownMethod,
                                         pk=breakdown_method_id)
    breakdowns = sphere.quantify_then_breakdown(quantifiable_id,
                                                breakdown_method_id)
    return render(request, 'budge/sphere_breakdowns_treemap.html',
                  {'sphere': sphere,
                   'quantifiable': quantifiable,
                   'breakdown_method': breakdown_method,
                   'breakdowns': breakdowns,
                   })


def category(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id)
    return render(request, 'budge/category.html',
                  {'category': category})


def quantification(request, quantification_id):
    quantification = get_object_or_404(models.Quantification,
                                       pk=quantification_id)
    return render(request, 'budge/quantification.html',
                  {'quantification': quantification})


def breakdown_treemap_data(request, breakdown_id):
    breakdown = get_object_or_404(models.Breakdown, pk=breakdown_id)
    return JsonResponse(breakdown.treemap_data)


def breakdown_treemap(request, breakdown_id):
    breakdown = get_object_or_404(models.Breakdown, pk=breakdown_id)
    return render(request, 'budge/breakdown_treemap.html',
                  {'breakdown': breakdown})


def sphere_breakdowns_treemap_data(request, sphere_id, quantifiable_id,
                                   breakdown_method_id):
    sphere = get_object_or_404(models.Sphere, pk=sphere_id)
    breakdowns = sphere.quantify_then_breakdown(quantifiable_id,
                                                breakdown_method_id)
    multi_treemap_data = models.Breakdown.multi_treemap_data(breakdowns)
    return JsonResponse(multi_treemap_data)


def sphere_breakdowns_column(request, sphere_id, quantifiable_id,
                             breakdown_method_id):
    sphere = get_object_or_404(models.Sphere, pk=sphere_id)
    quantifiable = get_object_or_404(models.Quantifiable, pk=quantifiable_id)
    breakdown_method = get_object_or_404(models.BreakdownMethod,
                                         pk=breakdown_method_id)
    breakdowns = sphere.quantify_then_breakdown(quantifiable_id,
                                                breakdown_method_id)
    return render(request, 'budge/sphere_breakdowns_column.html',
                  {'sphere': sphere,
                   'quantifiable': quantifiable,
                   'breakdown_method': breakdown_method,
                   'breakdowns': breakdowns,
                   })
