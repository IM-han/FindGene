from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

class SystemView(LoginRequiredMixin, View):
    """
    系统模块入口
    """
    def get(self, request):
        return render(request, 'system/system_index.html')
