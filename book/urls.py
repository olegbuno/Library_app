from django.urls import path
from .views import book_detail_view, book_listing_view, book_add_new_view, \
                book_delete, book_update, search_book, make_order


urlpatterns = [
    path('', book_listing_view, name="book_listing"),
    path('<int:pk>/', book_detail_view, name="book_details"),
    path('<int:pk>/delete/', book_delete, name="book_delete"),
    path('<int:pk>/update/', book_update, name="book_update"),
    path('<int:pk>/make-order/', make_order, name="make_order"),
    path('add-new/', book_add_new_view, name="add_new_book"),
    path('search/', search_book, name="search_book"),
]
