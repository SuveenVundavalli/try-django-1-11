from .models import Profile
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, View
from restaurants.models import RestaurantLocation
from menus.models import Item

# Create your views here.
User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_toggle = request.POST.get('username')
        print(user_to_toggle)
        profile_, is_following = Profile.objects.toggle_follow(request.user, user_to_toggle)
        print(is_following)
        return redirect(f"/profile/{profile_.user.username}/")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        item_exist = Item.objects.filter(user=user).exists()
        query = self.request.GET.get('q')
        qs = RestaurantLocation.objects.filter(owner=user).search(query)
        if item_exist and qs.exists():
            context['location'] = qs

        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following

        return context


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return HttpResponseRedirect("/login")
    # invalid code
    return HttpResponseRedirect("/login")
