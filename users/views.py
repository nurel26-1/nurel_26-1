from django.shortcuts import render, redirect
from users.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView


# def register_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': RegisterForm
#         }
#         return render(request, 'users/register.html', context=context)
#     if request.method == 'POST':
#         form = RegisterForm(data=request.POST)
#         if form.is_valid():
#             if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
#                 User.objects.create_user(
#                     username=form.cleaned_data.get('username'),
#                     password=form.cleaned_data.get('password1')
#                 )
#                 return redirect('/users/login/')
#             else:
#                 form.add_error('password1', 'чет ошибка, чекни че не так')
#         return render(request, 'users/register.html', context={'form': form})

class RegisterCBV(ListView, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, **kwargs):
        context = {
            'form': RegisterForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        data = request.POST
        form = RegisterForm(data=data)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/users/login/')

            else:
                form.add_error('password1', 'Пароли не совпадают!')

        return render(request, self.template_name, context={
            'form': form
        })


# def login_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': LoginForm
#         }
#         return render(request, 'users/login.html', context=context)
#
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = authenticate(request,
#                                 username=form.cleaned_data.get('username'),
#                                 password=form.cleaned_data.get('password'))
#             if user:
#                 login(request, user)
#                 return redirect('/products/')
#             else:
#                 form.add_error('username', 'не зарегался, соболезную')
#         return render(request, 'users/login.html', context={'form': form})

class LoginCBV(ListView, CreateView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request, **kwargs):
        context = {
            'form': LoginForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        data = request.POST
        form = LoginForm(data=data)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('username', 'Пользователь не найден!')

        return render(request, self.template_name, context=self.get_context_data(
         form=form
        ))


# def logout_view(request):
#     logout(request)
#     return redirect('/products/')

class LogoutCBV(ListView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/products/')