import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Create a question with given `question_text` and published the
    given number of `days` offset to now.

    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """
        If no question exist. an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are avaluable!')
        self.assertQuerysetEqual(response.context['last_question_list'], [])

    def test_past_question(self):
        """
        Question with pub_date in the past are displayed on the index page.
        """
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], ['<Question: Past question>'])

    def test_future_queston(self):
        """
        Question with pub_date in the future aren't displayed on the index page.
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], [])
        self.assertContains(response, 'No polls are avaluable!')

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['last_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_question(self):
        """
        The questions index page may display multiple question.
        """
        create_question(question_text="Past question1", days=-30)
        create_question(question_text="Past question2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['last_question_list'],
            ['<Question: Past question2>', '<Question: Past question1>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        :returns a 404 not found
        """
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of question with a pub_date in the past displayed a question text.
        """
        past_question = create_question(question_text='Past question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
