from django.shortcuts import render
from django.db.models import Subquery, OuterRef, IntegerField, CharField, F
from .models import PollingUnit, AnnouncedPuResults, Lga
from django.db.models.functions import Cast

# Create your views here.

def home(request):
    polling_units = PollingUnit.objects.all()
    context = {
        "polling_units": polling_units
    }
    return render(request, 'election/home.html', context)

def polling_unit(request, uniqueid):
    polling_unit = PollingUnit.objects.get(uniqueid=uniqueid)
    announced_pu_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=uniqueid)
    context = {
        "polling_unit": polling_unit,
        'announced_pu_results': announced_pu_results
    }
    return render(request, 'election/polling_unit.html', context)

def lga(request, uniqueid):
    lga = Lga.objects.get(uniqueid=uniqueid)
    polling_units = PollingUnit.objects.filter(lga_id=lga.uniqueid).annotate(
        result=Subquery(
            AnnouncedPuResults.objects.annotate(
                polling_unit_uniqueid_int=Cast('polling_unit_uniqueid', output_field=IntegerField())
            )
        )).filter(
            polling_unit_uniqueid_int=OuterRef('uniqueid')
        ).values('party_score')

    # polling_units = PollingUnit.objects.filter(lga_id=lga.uniqueid)
    # print(polling_units)
    # results = AnnouncedPuResults.objects.annotate(
    #     pu=Subquery(polling_units.values("uniqueid"))
    # ).filter(polling_unit_uniqueid=)
    context = {
        "lga": lga,
        "polling_units": polling_units
    }
    return render(request, 'election/lga.html', context)