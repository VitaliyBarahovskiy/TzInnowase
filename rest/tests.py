from django.http import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest.models import Ticket


class TicketsAPITestCase(APITestCase):

    def create_ticket(self):
        sample_ticket = {'title': "Hello", "desc": "Test"}
        response = self.client.post(reverse('tickets'), sample_ticket)
        return response

    def authenticate(self):
        self.client.post(reverse("register"), {
                         'username': "username", "email": "email@gmail.com", "password": "password"})

        response = self.client.post(
            reverse('login'), {"email": "email@gmail.com", "password": "password"})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


class TestListCreateTickets(TicketsAPITestCase):

    def test_should_not_create_ticket_with_no_auth(self):
        response = self.create_ticket()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_ticket(self):
        previous_todo_count = Ticket.objects.all().count()
        self.authenticate()

        response = self.create_ticket()
        self.assertEqual(Ticket.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Hello')
        self.assertEqual(response.data['desc'], 'Test')

    def test_retrieves_all_tickets(self):
        self.authenticate()
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        self.create_ticket()
        res = self.client.get(reverse('tickets'))
        self.assertIsInstance(res.data['count'], int)
        self.assertEqual(res.data['count'], 1)


class TestTicketDetailAPIView(TicketsAPITestCase):

    def test_retrieves_one_item(self):
        self.authenticate()
        response = self.create_ticket()

        res = self.client.get(
            reverse("ticket", kwargs={'id': response.data['id']}))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ticket = Ticket.objects.get(id=response.data['id'])

        self.assertEqual(ticket.title, res.data['title'])

    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_ticket()

        res = self.client.patch(
            reverse("ticket", kwargs={'id': response.data['id']}), {
                "title": "New one", 'is_complete': True
            })

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_ticket = Ticket.objects.get(id=response.data['id'])
        self.assertEqual(updated_ticket.is_complete, True)
        self.assertEqual(updated_ticket.title, 'New one')

    def test_deletes_one_item(self):
        self.authenticate()
        res = self.create_ticket()
        prev_db_count = Ticket.objects.all().count()

        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(
            reverse("ticket", kwargs={'id': res.data['id']}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Ticket.objects.all().count(), 0)