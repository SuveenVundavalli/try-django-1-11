from .models import RestaurantLocation
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from django.http import HttpResponseRedirect


# Create your views here.

def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            model_instance = form.save(commit=False)
            model_instance.owner = request.user
            form.save()
            return HttpResponseRedirect("/restaurants/")
        else:
            return HttpResponseRedirect("/login/")
    if form.errors:
        errors = form.errors


    template_name = 'restaurants/form.html'
    context = {'form': form, 'errors':errors}
    return render(request, template_name, context)


def restaurant_listview(request):
    template_name = 'restaurants/restaurant_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {'object_list': queryset}
    return render(request, template_name, context)


class RestaurantListView(ListView):
    template_name = 'restaurants/restaurant_list.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            queryset = RestaurantLocation.objects.filter(
                Q(category__icontains=slug) |
                Q(name__icontains=slug)
            )
        else:
            queryset = RestaurantLocation.objects.all()
        return queryset


class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()


class RestaurantCreateView(CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = '/restaurants/'

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.owner = self.request.user
        # form.save()
        return super(RestaurantCreateView, self).form_valid(form)
