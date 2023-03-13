from django.shortcuts import render, redirect, reverse
from . forms import ArticleForm
from django.forms import formset_factory
import datetime
def index(request):
    ArticleFormSet = formset_factory(ArticleForm, extra=3, can_delete=True)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES, prefix='article')
        if formset.is_valid():
            print('Validate passed, congratulations!!!')
            data = formset.cleaned_data
            print(type(data))
            print(data)
            return redirect(reverse('frms:index'))
        else:
            return redirect(reverse('frms:index'))
    else:
        formset = ArticleFormSet(prefix='article')
    return render(request, 'frms/index.html', context=dict(formset=formset, name='Harry'))
