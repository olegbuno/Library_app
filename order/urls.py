from django.urls import path
from .views import orders_listing_view, order_detail_view, lended_books_views, \
                    make_order_view, delete_order_view, update_order_view, book_autocomplete, \
                        find_order, user_autocomplete

urlpatterns = [
    path('', orders_listing_view, name="order_listing"),
    path('<int:pk>/', order_detail_view, name="order_details"),
    path('open-orders', lended_books_views, name="lended_books"),
    path('make-order/', make_order_view, name="make_order"),
    path('<int:pk>/delete-order/', delete_order_view, name="delete_order"),
    path('<int:pk>/update-order/', update_order_view, name="update_order"),
    path('book-autocomplete/', book_autocomplete, name="book_autocomplete"),
    path('user-autocomplete/', user_autocomplete, name="user_autocomplete"),
    path('find-order/', find_order, name="find_order"),
]
