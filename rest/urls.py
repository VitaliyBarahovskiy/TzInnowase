from rest.views import TicketsAPIView, TicketDetailAPIView
from django.urls import path

urlpatterns = [
    path("", TicketsAPIView.as_view(), name="tickets"),
    path("<int:id>", TicketDetailAPIView.as_view(), name="ticket")
]