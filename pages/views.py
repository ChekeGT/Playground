from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from  django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import  reverse_lazy
from django.utils.text import slugify
from .models import Page
from .forms import FormPage

# Create your views here.


class PagesListView(ListView):
    model = Page
    template_name = 'pages/pages.html'


class PagesDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'


@method_decorator(staff_member_required ,name='dispatch')
class PageCreateView(CreateView):
    model = Page
    template_name = 'pages/create_form.html'
    form_class = FormPage
    success_url = reverse_lazy('pages')


@method_decorator(staff_member_required ,name='dispatch')
class PageUpdateView(UpdateView):
    model = Page
    template_name = 'pages/update_form.html'
    form_class = FormPage
    def get_success_url(self):
            return reverse_lazy('page', args=[self.object.id,slugify(self.object.title)]) + '?ok'

@method_decorator(staff_member_required ,name='dispatch')
class PageDeleteView(DeleteView):
    model = Page
    template_name = 'pages/page_delete.html'
    success_url = reverse_lazy('pages')