from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import LoginForm
from utils.mixin_utils import LoginRequiredMixin

class IndexView(LoginRequiredMixin, View):
    """
    index页面视图
    """
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    """
    用户登录视图
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'system/users/login.html')
        else:
            return HttpResponseRedirect('/')#返回index页面

    def post(self, request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    msg = '用户未激活'
                    ret = {'msg': msg, "login_form": login_form}
                    return render(request, 'system/users/login.html')
            else:
                msg = '用户名和密码不能为空'
                ret = {'msg': msg, 'login_form': login_form}
                return render(request, 'system/users/login.html')
        else:
            msg = '用户名或密码错误'
            ret = {'msg': msg, 'login_form': login_form}
            return render(request, 'system/users/login.html')

class LogoutView(View):
    """
    用户登出视图
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))