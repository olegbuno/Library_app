from django.urls import path
from .views import author_listing_view, author_detail_view, \
                    author_add_new_view, author_delete, author_update, \
                        author_find


urlpatterns = [
    path('', author_listing_view, name="author_listing"),
    path('<int:pk>/', author_detail_view, name="author_details"),
    path('add-new/', author_add_new_view, name="add_new_author"),
    path('<int:pk>/delete/', author_delete, name="delete_author"),
    path('<int:pk>/update/', author_update, name="update_author"),
    path('find/', author_find, name="find_author"),
]
