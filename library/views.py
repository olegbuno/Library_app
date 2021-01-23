from django.shortcuts import render
from authentication.models import CustomUser
from book.models import Book
from order.models import Order

def home_view(request):
    template_name = "home.html"
    context = {}
    context["count_of_users"] = CustomUser.get_count()
    context["count_of_books"] = Book.get_count()
    context["count_of_orders"] = Order.get_count()
    context["page_title"] = "Home"

    return render(request, template_name, context)