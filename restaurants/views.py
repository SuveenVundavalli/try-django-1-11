import random
from django.shortcuts import render


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
