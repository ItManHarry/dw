from django.shortcuts import render, redirect, reverse
from .forms import AuthorForm, BookForm
from .models import Author, Book
def index(request):
    return render(request, 'mfms/index.html', context=dict(name='Harry'))
def author_index(request):
    authors = Author.objects.all()
    return render(request, 'mfms/author/index.html', context=dict(authors=authors))
def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mfms:author_add'))
    else:
        form = AuthorForm()
    return render(request, 'mfms/author/edit.html', context=dict(form=form, title='新增作者'))
def author_edit(request, id):
    author = Author.objects.get(pk=id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect(reverse('mfms:author_edit', args=(id,)))
    else:
        form = AuthorForm(instance=author)
    return render(request, 'mfms/author/edit.html', context=dict(form=form, title='编辑作者'))
def book_index(request):
    books = Book.objects.all()
    for book in books:
        for author in book.authors.all():
            print('Author name is : ', author)
    return render(request, 'mfms/book/index.html', context=dict(books=books))
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mfms:book_add'))
    else:
        form = BookForm()
    return render(request, 'mfms/book/edit.html', context=dict(form=form, title='新增图书'))