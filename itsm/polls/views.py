from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from . models import *
from django.db.models import F
from django.views import generic
def json_resp(request):
    return JsonResponse({
        'name': 'Harry-程国前',
        'age': 40,
        'hobbies': ['PingPang', 'Movies'],
    }, json_dumps_params={'ensure_ascii': False})
def home(request):
    return redirect(reverse('polls:detail', args=(100, )))
def index(request):
    print(request.method)
    print(request.path)
    try:
        print(request.GET['name'])
    except KeyError:
        print('None')
    latest_questions = BizQuestion.objects.order_by('-pub_date')[:5]
    out_put = ','.join([q.question_text for q in latest_questions])
    # return HttpResponse(out_put)
    context = {
        'latest_questions': latest_questions
    }
    '''use template loader to load the html'''
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    '''use render to load html'''
    return render(request, 'polls/index.html', context)
def detail(request, question_id):
    # try:
    #     question = BizQuestion.objects.get(pk=question_id)
    # except BizQuestion.DoesNotExist:
    #     raise Http404('Question does not exist!')
    question = get_object_or_404(BizQuestion, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(BizQuestion, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
def vote(request, question_id):
    question = get_object_or_404(BizQuestion, pk=question_id)
    try:
        choice = question.bizchoice_set.get(pk=request.POST['choice'])
    except (KeyError, BizChoice.DoesNotExist):
        return render(request, 'polls/detail.html', {'bizquestion': question,
                                                     'error_message': 'You did not select a choice!'})
    else:
        '''
        The code for our vote() view does have a small problem. It first gets the selected_choice 
        object from the database, then computes the new value of votes, and then saves it back to 
        the database. If two users of your website try to vote at exactly the same time, this might go wrong: 
        The same value, let’s say 42, will be retrieved for votes. Then, for both users the new value 
        of 43 is computed and saved, but 44 would be the expected value.
        This is called a race condition. If you are interested, you can read Avoiding race conditions 
        using F() to learn how you can solve this issue.
        '''
        choice.votes = F('votes') + 1
        choice.save()
        return redirect(reverse('polls:results', args=(question.id, )))
    # return HttpResponse('You are voting on question %s.' % question_id)
def reg_demo(request, num):
    return HttpResponse('Number is : %s' % num)
def reverse_handler(request):
    print('Poll index is : ', reverse('polls:index'))
    print('Poll reg is : ', reverse('polls:reg_demo', args=('12',)))
    return HttpResponse('Reverse')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        print(reverse('polls:vote', args=(8, )))
        return BizQuestion.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = BizQuestion
    template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = BizQuestion
    template_name = 'polls/results.html'