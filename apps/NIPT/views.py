from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class NIPTView(LoginRequiredMixin, View):
    """
    NIPT index 视图
    """
    def get(self, request):
        return render(request, 'NIPT/NIPT_index.html')