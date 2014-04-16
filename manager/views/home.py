from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login, logout as django_logout

@login_required
def home(request):
    context = {
    }
    return render(request, 'home.html', context)


def login(request, template='registration/login.html'):
    return django_login(request,
                       template_name=template,
                       )

def logout(request):
    django_logout(request)
    return redirect('home')












## COPIED FROM MUCKRACK


@login_required
def change_password(request):
    return django_auth_views.password_change(
        request,
        template_name='account/change_password.html',
        post_change_redirect=reverse('edit_profile'),
        password_change_form=ChangePasswordForm
    )


def reset_password(request):
    result = django_auth_views.password_reset(
        request,
        template_name='account/password_reset/password_reset_form.html',
        email_template_name='account/password_reset/password_reset_email.html',
        post_reset_redirect=reverse(reset_password_done)
    )
    return result


def reset_password_done(request):
    result = django_auth_views.password_reset_done(
        request,
        template_name='account/password_reset/password_reset_done.html'
    )
    return result


def reset_password_confirm(request, uidb64=None, token=None):
    result = django_auth_views.password_reset_confirm(
        request,
        uidb64=uidb64,
        token=token,
        template_name='account/password_reset/password_reset_confirm.html',
        post_reset_redirect=reverse(reset_password_complete)
    )
    return result


def reset_password_complete(request):
    result = django_auth_views.password_reset_complete(
        request,
        template_name='account/password_reset/password_reset_complete.html'
    )
    return result