from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic


# Create your views here.
# note that generic view require u to pass 'pk' explicitly from poll.url instead of question_id....

class IndexView(generic.ListView):
    template_name= 'polls/index.html' # default value overridden to redirect to template of choice
    context_object_name = 'latest_question_list' #literal is identifier in template
    def get_queryset(self):#probably overridden too
        from django.utils import timezone
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]# is given the context_object_name attribute before
       

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))




class DetailView(generic.DetailView):
    model = Question #since we’re using a Django model (Question), Django is able to determine an appropriate name for the context variable, as against a queryset that can be anything e.g. a list of objects attribute value
    template_name='polls/detail.html'
    
    def get_queryset(self):
        from django.utils import timezone
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())# but why return a query set(an iterable) with out providing context_obj_name  


def detail(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice.get(pk=int(request.POST['choice']))
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    


    