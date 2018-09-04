from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from registration.models import Profile

# Create your views here.


class ProfileListView(ListView):
    model = Profile
    template_name = 'Profiles/profile_list.html'
    paginate_by = 5


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'Profiles/profile_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])