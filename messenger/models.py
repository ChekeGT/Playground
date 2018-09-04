from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']


class ThreadsManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0 :
            return  queryset[0]
        return  None

    def find_or_create(self, user1, user2):
        queryset = self.find(user1, user2)
        if queryset is None:
            queryset = self.create()
            queryset.users.add(user1,user2)
        return queryset


class Threads(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadsManager()
    class Meta:
        ordering = ['-updated']


def messages_changed(sender, **kwargs):
    instace = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action is 'pre_add':
        false_pk_set = set()
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instace.users.all():
                false_pk_set.add(msg_pk)
        pk_set.difference_update(false_pk_set)
        #Forzar la actualizacion haciendo save
        instace.save()

m2m_changed.connect(messages_changed, sender=Threads.messages.through)