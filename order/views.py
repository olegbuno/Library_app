from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import MakeOrderForm, UpdateOrderForm
from .models import Order

from book.models import Book
from authentication.models import CustomUser


def orders_listing_view(request):
    template_name = "orders_listing.html"
    orders = Order.get_all()[::-1]
    paginator = Paginator(orders, 10)
    page = request.GET.get('page', 1)
    try:
        context_orders = paginator.page(page)
    except PageNotAnIntegers:
        context_orders = paginator.page(1)
    except EmptyPage:
        context_orders = paginator.page(paginator.num_pages)

    return render(request, template_name, {"orders": context_orders, "page_title": "Orders history"})


def order_detail_view(request, pk):
    template_name = "order_detail.html"
    order = Order.get_by_id(pk)
    return render(request, template_name, {"order": order, "page_title": f"Order #{order.id}"})


def lended_books_views(request):
    template_name = "open-orders.html"
    context = {}
    orders = Order.get_not_returned_books()
    if len(orders) == 0:
        return render(request, template_name, {"orders": 0, "page_title": "Lended books"})

    paginator = Paginator(orders, 10)
    page = request.GET.get('page', 1)
    try:
        context["orders"] = paginator.page(page)
    except PageNotAnInteger:
        context["orders"] = paginator.page(1)
    except EmptyPage:
        context["orders"] = paginator.page(paginator.num_pages)

    context["page_title"] = "Lended books"
    context["page"] = page
    return render(request, template_name, context)


def book_autocomplete(request):
    from django.http import JsonResponse

    if "term" in request.GET:
        books = Book.objects.filter(name__contains=request.GET.get('term'))
        books_names = []

        for book in books:
            books_names.append(f'{book.name}//{book.id}')

        return JsonResponse(books_names, safe=False)


def user_autocomplete(request):
    from django.http import JsonResponse

    if "term" in request.GET:
        users = CustomUser.objects.filter(
            Q(first_name__contains=request.GET.get('term')) |
            Q(middle_name__contains=request.GET.get('term')) |
            Q(last_name__contains=request.GET.get('term')) |
            Q(email__contains=request.GET.get('term')))
        users_name = []
        for user in users:
            users_name.append(f'{user.first_name} {user.middle_name} {user.last_name}//{user.id}')

        return JsonResponse(users_name, safe=False)


def make_order_view(request):
    context = {}
    template_name = "make_order.html"
    user = CustomUser.get_by_id(request.user.id)

    if request.method == "GET":
        form = MakeOrderForm(request.GET)
        if form.is_valid():
            book = Book.get_by_id(request.GET.get("book").split("//")[1])
            date = form.data["plated_end_at"]
            new_order = Order.create(
                user=user,
                book=book,
                plated_end_at=date
            )
            return redirect("order_details", pk=new_order.id)
    else:
        form = MakeOrderForm()
    context["page_title"] = "Make order"
    context["form"] = form
    return render(request, template_name, context)


def delete_order_view(request, pk):
    Order.delete_by_id(pk)
    return redirect("order_listing")


def update_order_view(request, pk):
    context = {}
    template_name = "update_order.html"
    order = Order.get_by_id(pk)
    if request.method == "POST":
        form = UpdateOrderForm(request.POST)
        if form.is_valid():
            order.update(
                plated_end_at=form.data["plated_end_at"],
                end_at=form.data["end_at"]
            )
            return redirect("order_details", pk=order.id)
    else:
        form = UpdateOrderForm()
    context["form"] = form
    context["page_title"] = "Update order"
    context["order"] = order
    return render(request, template_name, context)


def find_order(request):
    context = {}
    orders = None
    template_name = "order-search.html"
    target_book = request.GET.get('book')
    if target_book:
        target_book = target_book.split("//")[-1]
    target_user = request.GET.get('user')
    if target_user:
        target_user = target_user.split("//")[-1]
    if request.method == "GET":
        if target_book:
            orders = Order.objects.filter(book=Book.get_by_id(target_book))
        if target_user:
            orders = Order.objects.filter(user=CustomUser.get_by_id(target_user))

        context["page_title"] = "Find order"
        context["orders"] = orders
    return render(request, template_name, context)



# def find_order(request):
#     context = {}
#     orders = None
#     template_name = "order-search.html"
#     target_book = request.GET.get('book')
#     if target_book:
#         target_book = target_book.split("//")[-1]
#     target_user = request.GET.get('user')
#     if target_user:
#         target_user = target_user.split("//")[-1]
#     if request.method == "GET":
#         if target_book:
#             orders = Order.objects.filter(book=Book.get_by_id(target_book))
#         if target_user:
#             orders = Order.objects.filter(user=CustomUser.get_by_id(target_user))
#
#         context["page_title"] = "Find order"
#         context["orders"] = orders
#     return render(request, template_name, context)