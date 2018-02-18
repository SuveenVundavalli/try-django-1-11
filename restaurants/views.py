import random
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# Create your views here.
# function based view


def home(request):
    num = random.randint(0, 10000000000)
    some_list = [num, random.randint(0, 10000000000), random.randint(0, 10000000000)]
    context = {'html_var': True, 'num': num, 'some_list': some_list}
    return render(request, 'home.html', context)  # response


def about(request):
    return render(request, 'about.html')  # response


def contact(request):
    return render(request, 'contact.html')  # response


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        # Getting predefined context from TemplateView
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        num = random.randint(0, 10000000000)
        some_list = [random.randint(0, 10000000000), random.randint(0, 10000000000), random.randint(0, 10000000000)]
        context = {'html_var': True, 'num': num, 'some_list': some_list}
        return context

