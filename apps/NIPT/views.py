import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin
from .models import NIPTImportData
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class NIPTView(LoginRequiredMixin, View):
    """
    NIPT index 视图
    """
    def get(self, request):
        return render(request, 'NIPT/NIPT_index.html')

class NIPTDataImportView(LoginRequiredMixin, View):
    """
    NIPT数据导入视图
    """
    def get(self, request):
        return render(request, 'NIPT/data_import/data_import.html')

class NIPTDataImportTableView(LoginRequiredMixin, View):
    """
    NIPT数据导入表格
    """
    def get(self, request):
        fields = ['id', 'sample_number', 'name', 'date_blood', 'age', 'gestational_weeks', 'last_menstrual', 'fetus_number', 'tube_baby', 'telephone', 'hospital', 'doctor', 'province', 'remark', 'report_area', 'T13', 'T18', 'T21', 'result', 'date_report', 'state_report', 'person_import', 'date_import']
        filters = dict()
        filters['proposer_id'] = request.user.id
        ret = dict(data=list(NIPTImportData.objects.filter(**filters).values(*fields).order_by('-date_import')))
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')

class NIPTCreateView(LoginRequiredMixin, View):
    """
    NIPT新建样本视图
    """
    def get(self, request):
        area_list = []
        result_list = []
        for area_type in NIPTImportData.area_choices:
            area_dict = dict(item=area_type[0], value=area_type[1])
            area_list.append(area_dict)
        for result_type in NIPTImportData.result_choices:
            result_dict = dict(item=result_type[0], value=result_type[1])
            result_list.append(result_dict)
        ret = {
            'area_list': area_list,
            'result_list': result_list,
        }
        return render(request, 'NIPT/data_import/NIPT_create.html', ret)