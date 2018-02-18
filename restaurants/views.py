from django.shortcuts import render
from .models import RestaurantLocation
from django.views.generic import ListView
from django.db.models import Q


# Create your views here.

def restaurant_listview(request):
    template_name = 'restaurants/restaurant_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {'object_list': queryset}
    return render(request, template_name, context)


class RestaurantListView(ListView):
    template_name = 'restaurants/restaurant_list.html'
    queryset = RestaurantLocation.objects.all()


class SearchRestaurantListView(ListView):
    template_name = 'restaurants/restaurant_list.html'

    def get_queryset(self):
        print('in slug')
        print(self.kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            queryset = RestaurantLocation.objects.filter(
                Q(category__icontains=slug) |
                Q(name__icontains=slug)
            )
        else:
            queryset = RestaurantLocation.objects.none()
        return queryset

