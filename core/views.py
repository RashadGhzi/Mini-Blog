from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, BlogForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import cache_page
from .models import BlogModel
from django.contrib.auth.models import Group, User
from django.core.cache import cache


# Create your views here.


def home(request):
    blogs = BlogModel.objects.all()
    loggedCount = cache.get(request.user.username,
                            default=0, version=request.user.id)
    ip = request.session.get('ip', False)
    return render(request, 'core/home.html', {'blogs': blogs, 'loggedCount': loggedCount, 'ip':ip})


@cache_page(60*60)
def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')

# dashboard view function


def dashboard(request):

    if request.user.is_superuser is False:
        return redirect('home')

    if request.method == 'POST':
        blogForm = BlogForm(request.POST, label_suffix="")
        if blogForm.is_valid():
            blogForm.save()
            return redirect('home')
    else:
        blogForm = BlogForm(label_suffix="")
    blogs = BlogModel.objects.all()

    # counting which user has logged each time
    userLoginCount = {}
    users = User.objects.all()
    for user in users:
        userLoginCount[user.username] = cache.get(
            user.username, default=0, version=user.id)
    print(userLoginCount)

    return render(request, 'core/dashboard.html', {'blogForm': blogForm, 'blogs': blogs, "userLoginCount": userLoginCount})


def sign_up(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST, label_suffix="")
        if signupForm.is_valid():
            user = signupForm.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
            return redirect('login')
    else:
        signupForm = SignupForm(label_suffix="")
    return render(request, 'core/signup.html', {'signupForm': signupForm})


def log_in(request):
    if request.method == 'POST':
        loginForm = LoginForm(request, data=request.POST, label_suffix="")
        if loginForm.is_valid():
            login(request, loginForm.user_cache)
            return redirect('home')
    else:
        loginForm = LoginForm(label_suffix="")
    return render(request, 'core/login.html', {'loginForm': loginForm})


def log_out(request):
    logout(request)
    return redirect('login')


def blog_update(request, id):
    blog = BlogModel.objects.get(pk=id)
    if request.method == 'POST':
        blogFormUpdate = BlogForm(
            instance=blog, data=request.POST, label_suffix="")
        if blogFormUpdate.is_valid():
            blogFormUpdate.save()
            return redirect('home')
    else:
        blogFormUpdate = BlogForm(instance=blog, label_suffix="")
    return render(request, 'core/blog_update.html', {'blogFormUpdate': blogFormUpdate})


def blog_delete(request, id):
    if request.user.is_superuser:
        blog = BlogModel.objects.get(pk=id)
        blog.delete()
        return redirect('dashboard')
    else:
        return redirect('/')
