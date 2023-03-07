from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from . models import *
from django.db.models import F
from django.views import generic
from django.views.generic.edit import FormView
from . forms import UploadFileForm, ContactForm, FileFieldForm
import os
# class FileFieldFormView(FormView):
#     form_class = FileFieldForm
#     template_name = 'polls/form_upload.html'
#     success_url = reverse('polls:upload')
#     print('Success URL is : ', success_url)
#     def post(self, request, *args, **kwargs):
#         # form_class = self.get_form_class()
#         # form = self.get_form(form_class)
#         # files = request.FILES.getlist('file_field')
#         # if form.is_valid():
#         #     # for f in files:
#         #     #     print('file upload...')
#         #     return self.form_valid(form)
#         # else:
#         #     return self.form_invalid(form)
#         pass
def handle_uploaded_file(file=None):
    if file:
        # 文件上传路径
        upload_path = os.path.join(os.path.abspath('.'), 'attachments/files')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        file_to_upload = os.path.join(upload_path, file.name)
        # 执行上传
        with open(file_to_upload, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    else:
        print('No file to upload ...')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            print('Subject is : ', subject)
            print('Message is : ', message)
            print('Sender is : ', sender)
            print('CC myself is : ', cc_myself)
            return redirect(reverse('polls:contact'))
    else:
        form = ContactForm()
    return render(request, 'polls/contact.html', dict(form=form.render('polls/form_template.html')))

def upload_files(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for file in files:
                handle_uploaded_file(file)
            return redirect(reverse('polls:uploads'))
    else:
        form = FileFieldForm()
    return render(request, 'polls/uploads.html', {'form': form.render('polls/form_template.html')})
def upload_file(request):
    # handle_uploaded_file()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            handle_uploaded_file(file)
            return redirect(reverse('polls:upload'))
    else:
        form = UploadFileForm()
    return render(request, 'polls/upload.html', {'form': form.render('polls/form_template.html')})

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
    latest_questions = Question.objects.order_by('-pub_date')[:5]
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
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist!')
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.bizchoice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
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
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'