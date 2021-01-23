from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .form import AddBookForm, UpdateBookForm
from .models import Book

from order.models import Order
from author.models import Author
from order.forms import MakeOrderForm


def book_listing_view(request):
    template_name = "books_listing.html"
    context = {}
    books = Book.get_all()[::-1]
    paginator = Paginator(books, 10)
    page = request.GET.get('page', 1)
    try:
        context["books"] = paginator.page(page)
    except PageNotAnInteger:
        context["books"] = paginator.page(1)
    except EmptyPage:
        context["books"] = paginator.page(paginator.num_pages)

    context["page_title"] = "Books in stock"
    context["page"] = page

    return render(request, template_name, context)


def book_detail_view(request, pk):
    template_name = "book_detail.html"
    book = Book.get_by_id(pk)

    return render(request, template_name, {"book":book, "page_title":book.name})


def book_add_new_view(request):
    context = {}
    template_name = "book_add_new.html"
    context["page_title"] = "New book"
    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            authors = []
            for author_id in form.data["authors"]:
                authors.append(Author.get_by_id(author_id))
            new_book = Book.create(
                name=form.data["name"],
                description=form.data["description"],
                count=form.data["count"],
                authors=authors
            )
            return redirect("book_details", pk=new_book.id)
    else:
        context["form"] = AddBookForm
    return render(request, template_name, context)

def book_delete(request, pk):
    Book.delete_by_id(pk)
    return redirect("book_listing")

def book_update(request, pk):
    template_name = "book_update.html"
    book = Book.get_by_id(pk)
    context = {}
    context["book"] = book
    context["page_title"] = "Update book"
    context["title"] = "Update books meta"
    if request.method == "POST":
        form = UpdateBookForm(request.POST)
        if form.is_valid():
            book.update(
                name=form.data["name"],
                description=form.data["description"],
                count=form.data["count"],
            )
            authors = list(form.cleaned_data.get("authors"))
            if authors:
                book.remove_authors(book.get_authors)
                book.add_authors(authors)
            return redirect("book_details", pk=book.id)
    else:
        context["form"] = UpdateBookForm()
    return render(request, template_name, context)


def search_book(request):
    template_name = "book_find.html"
    context = {}
    context["page_title"] = "Find books"

    if request.method == "POST":
        form = UpdateBookForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            authors = list(form.cleaned_data.get("authors"))

            books = Book.objects.filter()

            if name:
                books = books.filter(name__contains=name)
                context["name"] = name

            if authors:
                for author in authors:
                    books = books.filter(authors=author)
            
            context["authors"] = authors
            context["books"] = books

    else:
        context["form"] = UpdateBookForm()
    return render(request, template_name, context)


def make_order(request, pk):
    context = {}
    template_name = "b_make_order.html"
    book = Book.get_by_id(pk)

    if request.method == "POST":
        form = MakeOrderForm(request.POST)
        if form.is_valid():
            new_order = Order.create(
                user=request.user,
                book=book,
                plated_end_at=form.data["plated_end_at"]
            )
            return redirect('order_details', pk=new_order.id)
    else:
        form = MakeOrderForm
    context["page_title"] = "Make order"
    context["form"] = form
    context["book"] = book

    return render(request, template_name, context)