from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.views.generic import View
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from doggyfood import models as df

class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "authentication/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('doggyfood:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('doggyfood:list')

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("authentication:login")


def register_user(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render(request, 'authentication/login.html', args)


def password_change(request):
    args = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("doggyfood:list")
        form.add_error(None, "Invalid user name or password")
    args.update(csrf(request))
    args['form'] = form = PasswordChangeForm(user=request.user)
    return render(request, "authentication/login.html", args)

