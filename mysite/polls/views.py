from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Test view. You`re at the polls index.')

def detail(request, question_id):
    return HttpResponse(f'You`re currently at the question {question_id}')

def results(request, question_id):
    return HttpResponse(f'You`re currently at the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You`re voting on question {question_id}')