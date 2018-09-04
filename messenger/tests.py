from django.test import TestCase
from .models import User, Message, Threads
# Create your tests here.


class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')


        self.thread = Threads.objects.create()

    def test_add_users_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()), 2)

    def test_find_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Threads.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    def test_non_existent_thread(self):
        threads = Threads.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1,content='Hola como estas')
        message2 = Message.objects.create(user=self.user2,content='Hola como estas')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2)

        for message in self.thread.messages.all():
            print('({}) Escribio: "{}"'.format(message.user, message.content))

    def test_add_messages_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hola como estas')
        message2 = Message.objects.create(user=self.user2, content='Hola como estas')
        message3 = Message.objects.create(user=self.user3, content='Soy un espia')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)

        for message in self.thread.messages.all():
            print('({}) Escribio: "{}"'.format(message.user, message.content))

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Threads.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, threads)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Threads.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, threads)
        thread = Threads.objects.find_or_create(self.user3, self.user1)
        self.assertIsNotNone(thread)
