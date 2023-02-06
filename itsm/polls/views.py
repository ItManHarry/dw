from django.shortcuts import render, reverse, redirect

from django.http import HttpResponse, JsonResponse
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
    return HttpResponse('Hello, you are in the polls index pages!')
def detail(request, question_id):
    return HttpResponse('You are looking at question %s.' % question_id)
def results(request, question_id):
    return HttpResponse('You are looking at question results %s.' % question_id)
def vote(request, question_id):
    return HttpResponse('You are voting on question %s.' % question_id)
def reg_demo(request, num):
    return HttpResponse('Number is : %s' % num)
def reverse_handler(request):
    print('Poll index is : ', reverse('polls:index'))
    print('Poll reg is : ', reverse('polls:reg_demo', args=('12',)))
    return HttpResponse('Reverse')