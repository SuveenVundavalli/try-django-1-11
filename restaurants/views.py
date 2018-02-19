from .models import RestaurantLocation
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required()
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
    context = {'form': form, 'errors': errors}
    return render(request, template_name, context)


def restaurant_listview(request):
    template_name = 'restaurants/restaurant_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {'object_list': queryset}
    return render(request, template_name, context)


class RestaurantListView(ListView):
    template_name = 'restaurants/restaurant_list.html'

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantDetailView(DetailView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    success_url = '/restaurants/'

    # login_url = '/login/'

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.owner = self.request.user
        # form.save()
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = f'Update Restaurant - {name}'
        return context
