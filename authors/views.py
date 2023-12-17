from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm


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
    if request.user.is_authenticated:
        messages.info(request, "Você já está conectado, caso queira sair de "
                      "sua conta clique no botão de logout")
        return redirect("recipes:home")
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
            return redirect('authors:dashboard')
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
    recipes = Recipe.objects.filter(author=request.user.profile,
                                    is_published=False,)
    messages.info(request, "As an author, you can edit or exclude your recipes that not was published :D")  # noqa
    return render(request, 'authors/pages/dashboard.html',
                  context={'recipes': recipes, 'is_dashboard_page': True})


@login_required(login_url='authors:login', redirect_field_name='next')
def author_recipe_create(request):
    recipe_form_data = request.session.get(
        'recipe_form_data')
    form_action = True

    form = AuthorRecipeForm(recipe_form_data, request.FILES)
    return render(request, 'authors/pages/author_recipe.html',
                  context={'form': form, 'recipe_title': 'Crie suas receitas!',
                           'create_recipe_form_action': form_action})


@login_required(login_url='authors:login', redirect_field_name='next')
def treat_author_recipe_create(request):
    if not request.POST:
        messages.error(request, "Você só pode enviar os dados uma vez!")
        return render(request, 'recipes/pages/404_error.html', status=404)

    POST = request.POST
    request.session['recipe_form_data'] = POST
    form = AuthorRecipeForm(POST, request.FILES)
    if form.is_valid():
        f = form.save(commit=False)
        f.author = request.user.profile
        f.save()
        messages.success(request, 'Receita criada com sucesso!.')
        del (request.session['recipe_form_data'])
        return redirect('authors:dashboard')

    messages.error(request, 'Formulário não válido!')
    return redirect('authors:create_recipe')


@login_required(login_url='authors:login', redirect_field_name='next')
def author_recipe_edit(request, id):
    try:
        recipe = Recipe.objects.get(author=request.user.profile, pk=id,) # noqa
    except Recipe.DoesNotExist:
        messages.error(request, "Receita solicitada não existe!")
        return redirect('authors:create_recipe')

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Receita editada com sucesso!")
        return redirect('authors:dashboard')
    return render(request, 'authors/pages/author_recipe.html',
                  context={'form': form, 'recipe_title': recipe.title})


@login_required(login_url='authors:login', redirect_field_name='next')
def author_recipe_exclude(request, id):
    try:
        recipe = Recipe.objects.get(pk=id) # noqa
    except Recipe.DoesNotExist:
        messages.error(request, "Receita solicitada não existe!")
        return redirect('authors:create_recipe')

    if recipe:
        recipe.delete()
        messages.success(request, 'Receita excluída com sucesso!')
        return redirect('authors:dashboard')
