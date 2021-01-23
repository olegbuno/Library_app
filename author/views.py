from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import AddAuthorForm, UpdateAuthorForm

from author.models import Author
from book.models import Book


def author_listing_view(request):
    template_name = "author/author_listing.html"
    context = {}
    authors = Author.get_all()
    paginator = Paginator(authors, 10)
    page = request.GET.get('page', 1)
    try:
        context["authors"] = paginator.page(page)
    except PageNotAnInteger:
        context["authors"] = paginator.page(1)
    except EmptyPage:
        context["authors"] = paginator.page(paginator.num_pages)

    context["page"] = page
    context["page_title"] = "Authors"

    return render(request, template_name, context)


def author_detail_view(request, pk):
    template_name = "author/author_detail.html"
    author = Author.get_by_id(pk)
    books = list(Book.objects.filter(authors__id=pk))

    return render(request, template_name, {"books":books, "author":author, "page_title": str(author.name) + " " + str(author.surname)}) 


def author_add_new_view(request):
    context = {}
    template_name = "author/author_add_new.html"
    context["page_title"] = "New author"
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_listing")
    else:
        context["form"] = AddAuthorForm()
    return render(request, template_name, context)

def author_delete(request, pk):
    Author.delete_by_id(pk)
    return redirect("author_listing")

def author_update(request, pk):
    template_name = "author/author_update.html"
    author = Author.get_by_id(pk)
    context = {}
    context["author"] = author
    context["page_title"] = "Update author"
    context["title"] = "Update authors meta"
    if request.method == "POST":
        form = UpdateAuthorForm(request.POST)
        if form.is_valid():
            author.update(request.POST.get("name"),
                            request.POST.get("surname"),
                            request.POST.get("patronymic"))
            return redirect("author_listing")
    else:
        context["form"] = UpdateAuthorForm()
    return render(request, template_name, context)

def author_find(request):
    template_name = "author/author_find.html"
    context = {}
    context["page_title"] = "Find authors"
    if request.method == "POST":
        form = UpdateAuthorForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            patronymic = request.POST.get("patronymic")
            authors = Author.objects.filter()
            if name:
                authors = authors.filter(name__contains=name)
                context["name"] = name
            if surname:
                authors = authors.filter(surname__contains=surname)
                context["surname"] = surname
            if patronymic:
                authors = authors.filter(patronymic__contains=patronymic)
                context["patronymic"] = patronymic
            context["authors"] = authors
    else:
        context["form"] = UpdateAuthorForm()
    return render(request, template_name, context)
    
