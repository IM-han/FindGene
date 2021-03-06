import json,re,xlrd
from datetime import datetime,date
from xlrd import xldate_as_tuple
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.serializers.json import DjangoJSONEncoder
from utils.mixin_utils import LoginRequiredMixin
from .models import NIPTImportData
from django.contrib.auth import get_user_model
from .forms import NIPTCreateForm, NIPTStandardImportForm, NIPTLimsImportForm, NIPTUpdateForm
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
        area_list = []
        result_list = []
        fetus_num_list = []
        tube_baby_list = []
        DS_result_list = []
        for DS_result in NIPTImportData.DS_result_choices:
            DS_result_dict = dict(item=DS_result[0], value=DS_result[1])
            DS_result_list.append(DS_result_dict)
        for tube_baby in NIPTImportData.tube_choices:
            tube_baby_dict = dict(item=tube_baby[0], value=tube_baby[1])
            tube_baby_list.append(tube_baby_dict)
        for fetus_num in NIPTImportData.fetus_number_choices:
            fetus_num_dict = dict(item=fetus_num[0], value=fetus_num[1])
            fetus_num_list.append(fetus_num_dict)
        for area_type in NIPTImportData.area_choices:
            area_dict = dict(item=area_type[0], value=area_type[1])
            area_list.append(area_dict)
        for result_type in NIPTImportData.result_choices:
            result_dict = dict(item=result_type[0], value=result_type[1])
            result_list.append(result_dict)
        ret = {
            'area_list': area_list,
            'result_list': result_list,
            'fetus_num_list': fetus_num_list,
            'tube_baby_list': tube_baby_list,
            'DS_result_list': DS_result_list,
        }
        return render(request, 'NIPT/data_import/data_import.html', ret)

class NIPTDataTableView(LoginRequiredMixin, View):
    """
    NIPT数据获取视图
    """
    def parse_date(self, s):
        Y,M,D = s.split('-')
        return date(int(Y),int(M),int(D))

    def get(self, request):
        fields = ['id', 'sample_number', 'name', 'date_blood', 'age', 'gestation_weeks', 'last_menstrual', 'fetus_number', 'tube_baby', 'telephone', 'hospital', 'doctor', 'province', 'remark', 'report_area', 'T13', 'T18', 'T21', 'result', 'date_report', 'state_report', 'person_import', 'date_import']
        filters = dict()
        if 'sample_number' in request.GET and request.GET['sample_number']:
            filters['sample_number__icontains'] = request.GET['sample_number']
        if 'date_blood_range' in request.GET and request.GET['date_blood_range']:
            date_blood = request.GET['date_blood_range']
            start_time, end_time = date_blood.split('--')
            start_time = self.parse_date(start_time)
            end_time = self.parse_date(end_time)
            filters['date_blood__range'] = (start_time, end_time)
        if 'name' in request.GET and request.GET['name']:
            filters['name'] = request.GET['name']
        if 'hospital' in request.GET and request.GET['hospital']:
            filters['hospital'] = request.GET['hospital']
        if 'province' in request.GET and request.GET['province']:
            filters['province'] = request.GET['province']
        if 'report_area' in request.GET and request.GET['report_area']:
            filters['report_area'] = request.GET['report_area']
        if 'date_report_range' in request.GET and request.GET['date_report_range']:
            date_report = request.GET['date_report_range']
            start_time,end_time = date_report.split('--')
            start_time=self.parse_date(start_time)
            end_time=self.parse_date(end_time)
            filters['date_report__range'] = (start_time, end_time)
        ret = dict(data=list(NIPTImportData.objects.filter(**filters).values(*fields).order_by('-date_import')))
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')

class NIPTDataStandardImportView(LoginRequiredMixin, View):
    """
    NIPT标准导入视图
    """

    def get(self, request):
        return render(request, 'NIPT/data_import/standard_upload.html')
    def post(self, request):
        '''
        上传Excel表，并进行解析
        '''

        res = dict(status='fail')
        myform = NIPTStandardImportForm(request.POST, request.FILES)
        print(myform)
        print(myform.is_valid())
        if myform.is_valid():
            f = request.FILES['standard_content']

            #解析Excel
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows #行数

            ncols = table.ncols #列数
            date_import = datetime.now()#获取当前日期
            #print(date_import)
            #从第二行开始遍历

            for i in range(1,nrows):
                rowValues = table.row_values(i) #一行数据
                NIPT = NIPTImportData()  # 实例化NIPT表
                NIPT.sample_number = int(rowValues[0])
                NIPT.name = rowValues[2]
                if isinstance(rowValues[1], str):
                    blood = [int(x) for x in rowValues[1].split('/')]
                    NIPT.date_blood = date(blood[0],blood[1],blood[2])
                elif isinstance(rowValues[1], float):
                    NIPT.date_blood = date(*xldate_as_tuple(rowValues[1], 0)[:3])
                #NIPT.date_blood = date(*xldate_as_tuple(rowValues[1],0)[:3])
                NIPT.age = int(rowValues[3])
                NIPT.gestation_weeks = rowValues[4]
                if isinstance(rowValues[11], str):
                    blood = [int(x) for x in rowValues[11].split('/')]
                    NIPT.last_menstrual = date(blood[0],blood[1],blood[2])
                elif isinstance(rowValues[11], float):
                    NIPT.last_menstrual = date(*xldate_as_tuple(rowValues[11], 0)[:3])
                #NIPT.last_menstrual = date(*xldate_as_tuple(rowValues[11],0)[:3])
                NIPT.fetus_number = rowValues[12]
                NIPT.tube_baby = rowValues[13]
                NIPT.telephone = int(rowValues[14])
                NIPT.hospital = rowValues[15]
                NIPT.doctor = rowValues[16]
                NIPT.province = rowValues[17]
                NIPT.remark = rowValues[18]
                NIPT.report_area = rowValues[19]
                NIPT.T13 = rowValues[21]
                NIPT.T18 = rowValues[22]
                NIPT.T21 = rowValues[23]
                NIPT.result = rowValues[20]
                NIPT.state_report = '1'
                if isinstance(rowValues[24], str):
                    blood = [int(x) for x in rowValues[24].split('/')]
                    NIPT.date_report = date(blood[0],blood[1],blood[2])
                elif isinstance(rowValues[24], float):
                    NIPT.date_report = date(*xldate_as_tuple(rowValues[24], 0)[:3])
                #NIPT.date_report = date(*xldate_as_tuple(rowValues[24],0)[:3])
                NIPT.date_import = date_import
                NIPT.person_import = request.user.username
                NIPT.DS21_result = rowValues[5]
                NIPT.DS21_value = rowValues[6]
                NIPT.DS18_result = rowValues[7]
                NIPT.DS18_value = rowValues[8]
                NIPT.DSother_result = rowValues[9]
                NIPT.preghistory = rowValues[10]
                NIPT.save()
            res['status'] = 'success'
            #return HttpResponseRedirect('NIPT/DataImport/DataTable')

        else:
            myform = NIPTStandardImportForm()
            #return render()
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')

class NIPTDataLimsImportView(LoginRequiredMixin, View):
    """
    Lims导入视图
    """
    def get(self, request):
        return render(request, 'NIPT/data_import/lims_upload.html')

    def post(self, request):
        '''
        上传Excel表，并进行解析
        '''

        res = dict(status='fail')
        myform = NIPTLimsImportForm(request.POST, request.FILES)

        if myform.is_valid():
            f = request.FILES['lims_content']

            #解析Excel
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows #行数

            ncols = table.ncols #列数
            date_import = datetime.now()#获取当前日期
            #print(date_import)
            #从第二行开始遍历

            for i in range(1,nrows):
                rowValues = table.row_values(i) #一行数据
                NIPT = NIPTImportData()  # 实例化NIPT表
                if isinstance(rowValues[0], float):
                    NIPT.sample_number = int(rowValues[0])
                elif isinstance(rowValues[0], str):
                    NIPT.sample_number = rowValues[0]
                NIPT.name = rowValues[2]
                if isinstance(rowValues[1], str):
                    blood = [int(x) for x in rowValues[1].split('/')]
                    NIPT.date_blood = date(blood[0],blood[1],blood[2])
                elif isinstance(rowValues[1], float):
                    NIPT.date_blood = date(*xldate_as_tuple(rowValues[1], 0)[:3])
                #print(NIPT.date_blood)
                NIPT.age = int(rowValues[3])
                NIPT.gestation_weeks = rowValues[4]
                if isinstance(rowValues[13], str):
                    last_menstrual = [int(x) for x in rowValues[13].split('/')]
                    NIPT.last_menstrual = date(last_menstrual[0], last_menstrual[1], last_menstrual[2])
                elif isinstance(rowValues[13], float):
                    NIPT.last_menstrual = date(*xldate_as_tuple(rowValues[13], 0)[:3])
                NIPT.fetus_number = rowValues[14]
                print(rowValues[14],rowValues[15:19])
                NIPT.tube_baby = rowValues[15]
                NIPT.telephone = int(rowValues[16])
                NIPT.hospital = rowValues[17]
                NIPT.doctor = rowValues[18]
                NIPT.province = rowValues[19]
                NIPT.remark = rowValues[21]
                NIPT.report_area = rowValues[20]
                NIPT.T13 = rowValues[23]
                NIPT.T18 = rowValues[24]
                NIPT.T21 = rowValues[25]
                NIPT.result = rowValues[22]
                NIPT.state_report = '1'
                if isinstance(rowValues[26], str):
                    date_report = [int(x) for x in rowValues[26].split('/')]
                    NIPT.date_report = date(date_report[0], date_report[1], date_report[2])
                elif isinstance(rowValues[26], float):
                    NIPT.date_report = date(*xldate_as_tuple(rowValues[26],0)[:3])
                NIPT.date_import = date_import
                NIPT.person_import = request.user.username
                NIPT.DS21_result = rowValues[5]
                NIPT.DS21_value = rowValues[6]
                NIPT.DS18_result = rowValues[7]
                NIPT.DS18_value = rowValues[8]
                NIPT.DSother_result = rowValues[9]
                NIPT.preghistory = '孕'+str(int(rowValues[10]))+"生"+str(int(rowValues[11]))+"流"+str(int(rowValues[12]))
                NIPT.save()
            res['status'] = 'success'
            #return HttpResponseRedirect('NIPT/DataImport/DataTable')

        else:
            myform = NIPTStandardImportForm()
            #return render()
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class NIPTCreateView(LoginRequiredMixin, View):
    """
    NIPT新建样本视图
    """
    def get(self, request):
        area_list = []
        result_list = []
        fetus_num_list = []
        tube_baby_list = []
        DS_result_list = []
        for DS_result in NIPTImportData.DS_result_choices:
            DS_result_dict = dict(item=DS_result[0], value=DS_result[1])
            DS_result_list.append(DS_result_dict)
        for tube_baby in NIPTImportData.tube_choices:
            tube_baby_dict = dict(item=tube_baby[0], value=tube_baby[1])
            tube_baby_list.append(tube_baby_dict)
        for fetus_num in NIPTImportData.fetus_number_choices:
            fetus_num_dict = dict(item=fetus_num[0], value=fetus_num[1])
            fetus_num_list.append(fetus_num_dict)
        for area_type in NIPTImportData.area_choices:
            area_dict = dict(item=area_type[0], value=area_type[1])
            area_list.append(area_dict)
        for result_type in NIPTImportData.result_choices:
            result_dict = dict(item=result_type[0], value=result_type[1])
            result_list.append(result_dict)
        ret = {
            'area_list': area_list,
            'result_list': result_list,
            'fetus_num_list': fetus_num_list,
            'tube_baby_list': tube_baby_list,
            'DS_result_list': DS_result_list,
        }
        if 'id' in request.GET and request.GET['id']:
            NIPTData = get_object_or_404(NIPTImportData, pk=request.GET['id'])
            ret['NIPTData'] = NIPTData
            #print(NIPTData,request.GET,request.GET['id'])
            #print(ret)
        return render(request, 'NIPT/data_import/NIPT_create.html', ret)

    def post(self, request):

        res = dict()
        print(request.POST,)
        if 'id' in request.POST and request.POST['id']:
            NIPTData = get_object_or_404(NIPTImportData, pk=request.POST['id'])
            #print(request.POST,request.POST['id'],NIPTData,NIPTImportData())
            NewDataForm = NIPTUpdateForm(request.POST, instance=NIPTData)
            print(NIPTData,NewDataForm)
        else:
            NIPTData = NIPTImportData()
            #print(request.POST, NIPTData, )
            NewDataForm = NIPTCreateForm(request.POST, instance=NIPTData)
        #print(NewDataForm.is_valid(),request.user.username)

            #print(NewDataForm)

        if NewDataForm.is_valid():
            NewDataForm.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(NewDataForm.errors)

            NewDataForm_errors = re.findall(pattern, errors)

            res = {
                'status': 'fail',
                'NewDataForm_errors': NewDataForm_errors[0]
            }

        return HttpResponse(json.dumps(res), content_type='application/json')

class NIPTUpdateView(LoginRequiredMixin, View):
    """
    NIPT修改样本视图
    """

    def get(self, request):
        area_list = []
        result_list = []
        fetus_num_list = []
        tube_baby_list = []
        DS_result_list = []
        for DS_result in NIPTImportData.DS_result_choices:
            DS_result_dict = dict(item=DS_result[0], value=DS_result[1])
            DS_result_list.append(DS_result_dict)
        for tube_baby in NIPTImportData.tube_choices:
            tube_baby_dict = dict(item=tube_baby[0], value=tube_baby[1])
            tube_baby_list.append(tube_baby_dict)
        for fetus_num in NIPTImportData.fetus_number_choices:
            fetus_num_dict = dict(item=fetus_num[0], value=fetus_num[1])
            fetus_num_list.append(fetus_num_dict)
        for area_type in NIPTImportData.area_choices:
            area_dict = dict(item=area_type[0], value=area_type[1])
            area_list.append(area_dict)
        for result_type in NIPTImportData.result_choices:
            result_dict = dict(item=result_type[0], value=result_type[1])
            result_list.append(result_dict)
        ret = {
            'area_list': area_list,
            'result_list': result_list,
            'fetus_num_list': fetus_num_list,
            'tube_baby_list': tube_baby_list,
            'DS_result_list': DS_result_list,
        }
        if 'id' in request.GET and request.GET['id']:
            NIPTData = get_object_or_404(NIPTImportData, pk=request.GET['id'])
            ret['NIPTData'] = NIPTData
            # print(NIPTData,request.GET,request.GET['id'])
            # print(ret)
        return render(request, 'NIPT/data_import/NIPT_update.html', ret)

    def post(self, request):

        res = dict()
        #print(request.POST['sample_number'])
        NIPTData = get_object_or_404(NIPTImportData, sample_number=request.POST['sample_number'])
        NewDataForm = NIPTUpdateForm(request.POST, instance=NIPTData)

        if NewDataForm.is_valid():
            NewDataForm.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(NewDataForm.errors)
            NewDataForm_errors = re.findall(pattern, errors)

            res = {
                'status': 'fail',
                'NewDataForm_errors': NewDataForm_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')

class NIPTExportTemplateView(LoginRequiredMixin, View):
    """
    模板导出视图
    """
    def get(self, request):
        return render(request, 'NIPT/data_import/export_template.html')

class NIPTDeleteView(LoginRequiredMixin, View):
    """
    删除样本视图
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            #print(id_list)
            NIPTImportData.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')

class NIPTReportView(LoginRequiredMixin, View):
    '''
    NIPT报告审核视图
    '''
    def get(self, request):
        return render(request, 'NIPT/report_check/report_check.html')