from django.shortcuts import render
from .forms import RegisterForm


def add_user(request):

    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'authors/pages/add-user.html', {
        'form': form,
        "title": 'Register | '
    })
