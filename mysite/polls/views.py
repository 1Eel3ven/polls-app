from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # returns last 5 published questions
        # Those questions that set to be published in the future and those that have no choices are ignored
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct().order_by('-pub_date')[:5]
    


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # Excludes any questions that arent published yet or have no choices;
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct()


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        # Excludes any questions that arent published yet or have no choices;
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct()


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay voting form with error message
        context = {'question': question, 'error_message': 'You didnt select a choice.'}

        return render(request, 'polls/detail.html', context)
    
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        
        # HttpResponseRedirect to prevent double-post if a user hits back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))