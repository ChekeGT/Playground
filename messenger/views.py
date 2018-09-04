from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Threads,User,Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from  django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

# Create your views here.
@method_decorator(login_required(), name='dispatch')
class ThreadListView(TemplateView):
    template_name = 'messenger/thread_list.html'

@method_decorator(login_required(), name='dispatch')
class ThreadDetailView(DetailView):
    model = Threads
    template_name = 'messenger/thread_detail.html'

    def get_object(self, queryset=None):
        obj = super(ThreadDetailView, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404
        return obj
@login_required()
def add_message(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content')
        if content:
            thread = get_object_or_404(Threads, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            if len(thread.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404('El usuario no esta identificado')
    return JsonResponse(json_response)

@login_required()
def start_thread(request, username):
    user1 = get_object_or_404(User, username=username)
    thread = Threads.objects.find_or_create(user1,request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
