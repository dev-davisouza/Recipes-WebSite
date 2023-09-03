from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


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
        form.save()
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])

    return redirect("authors:add_user")
