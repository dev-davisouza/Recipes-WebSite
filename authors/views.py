from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import User


def add_user(request):
    register_form_data = request.session.get(
        'register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/add-user.html', {
        'form': form,
        "title": 'Register | '
    })


def treat_post_add_user(request):
    if not request.POST:
        return render(request, 'recipes/pages/404_error.html', status=404)

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        author = form.save(commit=False)
        author.user = user
        author.save()
        messages.success(request, 'Your user was created, please log in.')

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect("authors:add_user")


def login_user(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
    })


def treat_post_login(request):
    if not request.POST:
        return redirect('authors:login')

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, "You're logged in.")
            login(request, authenticated_user)
            return redirect('recipes:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')