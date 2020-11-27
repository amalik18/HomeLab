import json

from django.test import TestCase

# Create your tests here.
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whose pub_date is in the future
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day
        :return:
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of 'days'
    offset to now (negative for questions published in the past, positive for questions that
    have yet to be published)
    :param question_text: text of the question
    :param days: day when posted
    :return:
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    """
    Create a choice for the provided Question object
    :param question:
    :param choice_text:
    :return:
    """
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If there are no questions, an appropriate message is displayed
        :return:
        """
        response = self.client.get(reverse('polls:index'))
        logger.info(f"Here is the response: {response}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text='No polls are available.')
        self.assertQuerysetEqual(qs=response.context['latest_question_list'], values=[])

    def test_past_question(self):
        """
        Questions with the pub_date in the past are displayed on the index page
        :return:
        """
        past_question = create_question(question_text='Past Question.', days=-30)
        create_choice(question=past_question, choice_text="Yes")
        response = self.client.get(reverse('polls:index'))
        response_log = {
            'context': response.context['latest_question_list'],
            'code': response.status_code,
            'request': response.request,
            'content': response.content,

        }
        logger.info(f"Here is the response: {json.dumps(response_log, indent=2, default=str, sort_keys=True)}")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(qs=response.context['latest_question_list'],
                                 values=['<Question: Past Question.>'])

    def test_future_question(self):
        """
        Questions with the pub_date in the future are NOT displayed on the index page
        :return:
        """
        create_question(question_text='Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        logger.info(f"Here is the response: {response}")
        self.assertContains(response=response, text='No polls are available.')
        self.assertQuerysetEqual(qs=response.context['latest_question_list'], values=[])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exists only past questions are displayed
        :return:
        """
        past_question = create_question(question_text='Past question.', days=-30)
        future_question = create_question(question_text='Future question.', days=30)
        create_choice(question=past_question, choice_text="Yes")
        create_choice(question=future_question, choice_text="No")
        response = self.client.get(reverse('polls:index'))
        response_log = {
            'context': response.context['latest_question_list'],
            'code': response.status_code,
            'request': response.request,
            'content': response.content,

        }
        logger.info(f"Here is the response: {json.dumps(response_log, indent=2, default=str, sort_keys=True)}")
        self.assertQuerysetEqual(qs=response.context['latest_question_list'],
                                 values=['<Question: Past question.>'])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple question
        :return:
        """
        past_question_1 = create_question(question_text='Past question 1.', days=-23)
        past_question_2 = create_question(question_text='Past question 2.', days=-12)
        create_choice(question=past_question_1, choice_text="Yes")
        create_choice(question=past_question_2, choice_text="Yes")
        response = self.client.get(reverse('polls:index'))
        response_log = {
            'context': response.context['latest_question_list'],
            'code': response.status_code,
            'request': response.request,
            'content': response.content,

        }
        logger.info(f"Here is the response: {json.dumps(response_log, indent=2, default=str, sort_keys=True)}")
        self.assertQuerysetEqual(qs=response.context['latest_question_list'],
                                 values=['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 Not Found
        :return:
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse(viewname='polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        logger.info(f"Here is the response: {response}")
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        :return:
        """
        past_question = create_question(question_text='Past question.', days=-14)
        create_choice(question=past_question, choice_text="Yes")
        url = reverse(viewname='polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        response_log = {
            'context': response.context,
            'code': response.status_code,
            'request': response.request,
            'content': response.content,

        }
        logger.info(f"Here is the response: {json.dumps(response_log, indent=2, default=str, sort_keys=True)}")
        self.assertContains(response=response, text=past_question.question_text)


class QuestionResultsViewTest(TestCase):
    def test_past_question(self):
        """
        The results view of a question with a pub_date in the future returns a 404
        :return:
        """
        future_question = create_question(question_text="Future question", days=3)
        url = reverse(viewname='polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        logger.info(f"Here's the response: {response}")
        self.assertEqual(response.status_code, 404)
