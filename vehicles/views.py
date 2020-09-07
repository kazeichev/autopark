from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from vehicles.models import Enterprise


@login_required
def manager(request):
    user = request.user
    enterprises = Enterprise.objects.filter(
        manager=user
    )

    return render(request, 'manager.html', {
        'enterprises': enterprises,
        'user': user
    })
