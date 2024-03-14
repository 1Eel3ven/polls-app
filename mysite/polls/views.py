from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, 'polls/results.html', {'question': question})



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