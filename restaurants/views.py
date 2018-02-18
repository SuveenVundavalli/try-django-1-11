from django.shortcuts import render
from .models import RestaurantLocation


# Create your views here.

def restaurant_listview(request):
    template_name = 'restaurants/restaurant_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {'object_list': queryset}
    return render(request, template_name, context)
