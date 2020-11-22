from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404

# Create your views here.
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # output = ', '.join([q.question_text for q in latest_question_list])
    return render(request=request, template_name='polls/index.html', context=context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("The Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request=request, template_name='polls/detail.html', context=context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    return render(request=request, template_name='polls/results.html', context=context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # re-display the question voting form
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request=request, template_name='polls/detail.html', context=context)
    else:
        selected_choice.votes += 1
        selected_choice.save()

        '''
        Always return an HttpResponseRedirect after a succesful POST operation. 
        This prevents data from being posted twice if a user hits the back button in their browser.
        '''
        return HttpResponseRedirect(reverse(viewname='polls:results', args=(question_id,)))
