from django.test import TestCase

# Create your tests here.
from gameidl.models import GameIdlReply


one_reply = GameIdlReply.objects.get(id=20)

print one_reply.reviewId