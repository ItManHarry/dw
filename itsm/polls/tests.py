from django.test import TestCase
import datetime
from django.utils import timezone
from . models import *
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        f_q = BizQuestion(pub_date=time)
        self.assertIs(f_q.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        o_q = BizQuestion(pub_date=time)
        self.assertIs(o_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        r_q = BizQuestion(pub_date=time)
        self.assertIs(r_q.was_published_recently(), True)