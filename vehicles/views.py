from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from vehicles.forms import VehicleEditForm, VehicleCreateForm
from vehicles.models import Enterprise, Vehicle, Track, Report, VehicleMileageReport

import json


@login_required
def manager(request):
    user = request.user
    enterprises = Enterprise.objects.filter(
        manager=user
    )

    return render(request, 'manager.html', {
        'enterprises': enterprises
    })


@login_required
@require_http_methods(["GET"])
def enterprise_view(request, enterprise_id):
    enterprise = get_object_or_404(Enterprise, pk=enterprise_id)
    vehicles = Vehicle.objects.filter(enterprise=enterprise)
    paginator = Paginator(vehicles, 20)

    page_number = request.GET.get('page')
    pagination = paginator.get_page(page_number)

    return render(request, 'enterprise/view.html', {
        'enterprise': enterprise,
        'vehicles': pagination
    })


@login_required
@require_http_methods(['GET', 'POST'])
def vehicle_create(request, enterprise_id):
    enterprise = Enterprise.objects.get(id=enterprise_id)
    vehicle = Vehicle(enterprise=enterprise)
    form = VehicleCreateForm(request.POST or None, instance=vehicle)

    if form.is_valid():
        vehicle = form.save()
        return redirect('vehicle-view', enterprise_id=enterprise_id, vehicle_id=vehicle.id)

    return render(request, 'vehicle/edit.html', {'form': form, 'enterprise': enterprise})


@login_required
@require_http_methods(['GET', 'POST'])
def vehicle_edit(request, enterprise_id, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    form = VehicleEditForm(request.POST or None, instance=vehicle)

    if form.is_valid():
        form.save()
        return redirect('vehicle-view', enterprise_id=enterprise_id, vehicle_id=vehicle_id)

    return render(request, 'vehicle/edit.html', {'form': form, 'enterprise': vehicle.enterprise})


@login_required
@require_http_methods(['GET'])
def vehicle_view(request, enterprise_id, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    tracks = Track.objects.filter(vehicle=vehicle)
    return render(request, 'vehicle/view.html', {'vehicle': vehicle, 'tracks': tracks})


@login_required
@require_http_methods(['GET'])
def vehicle_delete(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    enterprise_id = vehicle.enterprise.id

    vehicle.delete()
    return redirect('enterprise-view', id=enterprise_id)


@login_required
@require_http_methods(['GET'])
def track_view(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    route = []

    for point in track.route:
        p = GEOSGeometry(point).coords
        route.append([*p])

    return render(
        request,
        'track/view.html',
        {
            'track': track,
            'route': json.dumps(route)
        })


@login_required
@require_http_methods(['GET'])
def reports_list(request):
    vehicleMileageReports = VehicleMileageReport.objects.all()
    return render(request, 'report/list.html', {'vehicleMileageReports': vehicleMileageReports})
