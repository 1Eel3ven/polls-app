from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''Testing if was_published_recently() returns False for questions with pub_date set in the future.'''
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''Testing if was_published_recently() returns False for questions with pub_date older than 1 day.'''
        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''Testing if was_published_recently() returns True for questions with pub_date within last day.'''
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    '''Creates a question that is published the given number of days (negative or positive) offset to now;
    Negative for questions published in the past; Positive for questions published in the future.'''
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''Testing if an appropriate message displayed when no questions exist'''
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available currently.')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''Testing if questions with pub_date in the past are displayed'''
        question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        '''Testing if questions with pub_date in the future arent displayed'''
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, 'No polls are available currently.')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        '''Testing if only past questions are displayed if both past and future exist'''
        question = create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(response.context['latest_question_list'], [question],)

    def test_two_past_questions(self):
        '''Testing if index page can display multiple questions'''
        question1 = create_question(question_text='Past question 1', days=-30)
        question2 = create_question(question_text='Past question 2', days=-10)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1],)
