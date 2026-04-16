from django.shortcuts import render
from django.db.models import Count
from .models import Student


def students_per_city(request):
    city_counts = Student.objects.values('address__city').annotate(
        num_students=Count('id')
    ).order_by('address__city')

    return render(request, 'usermodule/students_per_city.html', {
        'city_counts': city_counts
    })