from django.contrib import messages
from django.shortcuts import render
from web.forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm, UserForm, EditUserForm, PasswordRemindForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from web.emails import Emails


def log_in(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.add_message(request, messages.INFO, 'Rejestracja musi zostać zaakceptowana przez administratora')
            else:
                messages.add_message(request, messages.INFO, 'Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            email = Emails()
            email.register_me(user.email)
            return redirect('login')
        else:
            messages.add_message(request, messages.INFO, 'Nieprawidłowe dane uwierzytelniające.')

    else:
        user_form = UserForm()

    return render(request, 'account/register.html', {'user_form': user_form})


def log_out(request):
    logout(request)
    return redirect('index')


def password_reminder(request):
    if request.method == 'POST':
        form = PasswordRemindForm(request.POST)
        if form.is_valid():
            email = Emails()
            email.remind_password(receiver=form.cleaned_data['email'])
            messages.add_message(request, messages.INFO, 'Na twoją skrzynkę mailową wysłano hasło.')
            return redirect('login')

    else:
        form = PasswordRemindForm()

    return render(request, 'account/password_reminder.html', {'form': form})