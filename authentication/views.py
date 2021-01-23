from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserLoginForm, CustomUserRegisterForm, CustomUserUpdateForm, CustomUserSearchForm
from .models import CustomUser
from order.models import Order


def users_listing_view(request):
    users = CustomUser.get_all()[::-1]
    paginator = Paginator(users, 20)
    page = request.GET.get('page', 1)
    try:
        context_users = paginator.page(page)
    except PageNotAnInteger:
        context_users = paginator.page(1)
    except EmptyPage:
        context_users = paginator.page(paginator.num_pages)
    return render(request, "users_listing.html", {"users":context_users, "page_title": "Users", 'page':page})

def user_detail_view(request, pk):
    template_name = "user_detail.html"
    context = {}
    user = CustomUser.get_by_id(pk)
    context["context_user"] = user
    context["orders"] = Order.get_orders_by_user_id(pk)
    context["page_title"] = "{0} {1} profile".format(user.first_name, user.last_name)
    return render(request, template_name, context)

def sign_in(request):
    template_name = 'sign_in.html'
    context = {}
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=request.POST.get("email"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                return redirect("home")      
    else:
        form  = CustomUserLoginForm()
    context["form"] = form
    return render(request, template_name, context)

def user_logout(request):
    logout(request)
    return redirect("user_sign_in")

def sign_up(request):
    template_name = 'sign_up.html'
    context = {}
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = CustomUserRegisterForm()
    context["form"] = form
    return render(request, template_name, context)

def user_delete(request):
    CustomUser.delete_by_id(request.user.id)
    logout(request)
    return redirect ("user_sign_in")

def user_update(request):
    context = {}
    user = CustomUser.get_by_id(request.user.id)
    template_name = "user_update.html"
    
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST)
        if form.is_valid():
            user.update(
                first_name=form.data["first_name"],
                middle_name=form.data["middle_name"],
                last_name=form.data["last_name"],
                password=form.data["password"],
                role=form.data["role"],
                is_active=form.data["is_active"]
            )
            return redirect("user_details", pk=user.id)
    else:
        form = CustomUserUpdateForm()

    context["context_user"] = user
    context["form"] = form
    context["page_title"] = "Update infomation"

    return render(request, template_name, context)

def user_find(request):
    context = {}
    template_name = "user_find.html"

    if request.method == "POST":
        form = CustomUserSearchForm(request.POST)
        if form.is_valid():
            f_name = form.data["first_name"]
            m_name = form.data["middle_name"]
            l_name = form.data["last_name"]
            email = form.data["email"]
            context_users = CustomUser.objects.all()
            if f_name:
                context_users = context_users.filter(first_name__contains=f_name)
                context["f_name"] = f_name
            if m_name:
                context_users = context_users.filter(middle_name__contains=m_name)
                context["m_name"] = m_name
            if l_name:
                context_users = context_users.filter(last_name__contains=l_name)
                context["l_name"] = l_name
            if email:
                context_users = context_users.filter(email__contains=email)
                context["email"] = email
            if context_users:
                context["context_users"] = context_users
            else:
                context["context_users"] = 0

    else:
        form = CustomUserSearchForm()

    context["form"] = form
    context["page_title"] = "Find user"

    return render(request, template_name, context)