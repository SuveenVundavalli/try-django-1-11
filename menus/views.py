from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Item
from .forms import ItemForm


# Create your views here.
class ItemListView(ListView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


# Create your views here.
class ItemDetailView(DetailView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


# Create your views here.
class ItemCreateView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name = 'form.html'
    success_url = '/items/'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        # form.save()
        return super(ItemCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Item'
        return context


# Create your views here.
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ItemForm
    template_name = 'form.html'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context