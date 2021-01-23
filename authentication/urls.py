from django.urls import path
from .views import user_detail_view, users_listing_view, sign_in, sign_up, \
                    user_logout, user_delete, user_update, user_find

urlpatterns = [
    path('', users_listing_view, name="users_listing"),
    path('<int:pk>/', user_detail_view, name="user_details"),
    path('sign-in/', sign_in, name="user_sign_in"),
    path('sign-up/', sign_up, name="user_sign_up"),
    path('logout/', user_logout, name="user_logout"),
    path('delete/', user_delete, name="user_del"),
    path('update/', user_update, name="user_upd"),
    path('find/', user_find, name="user_find"),
]
