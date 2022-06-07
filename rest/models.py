from helpers.models import TrackingModel
from django.db import models
from authentication.models import User


class Ticket(TrackingModel):

    STATUS_CHOICES = [
        (1, "OK"),
        (2, "NO"),
        (3, "Frozen"),
    ]

    title = models.CharField(max_length=255)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Support(TrackingModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Answer')
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
