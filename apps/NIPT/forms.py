from django import forms
from django.contrib.auth import get_user_model

from .models import NIPTImportData

class NIPTCreateForm(forms.ModelForm):
    class Meta:
        model = NIPTImportData
        fields = '__all__'
        error_messages = {
            "sample_number": {"required": "请输入样本编号"},
            "report_area": {"required": "请输入报告地区"},
            "result": {"required": "请输入检测结果"},
            "T13": {"required": "请输入T13值"},
            "T18": {"required": "请输入T18值"},
            "T21": {"required": "请输入T21值"},
            "date_report": {"required": "请输入报告时间"},
            "name": {"required": "请输入孕妇姓名"},
            "telephone": {"required": "请输入联系方式"},
            "date_blood": {"required": "请输入采血时间"},
            "age": {"required": "请输入孕妇年龄"},
        }

    def clean(self):
        cleaned_data = super(NIPTCreateForm, self).clean()
        sample_number = cleaned_data.get("sample_number")
        if NIPTImportData.objects.filter(sample_number=sample_number).count():
            raise forms.ValidationError("样本编号已存在")

class NIPTStandardImportForm(forms.ModelForm):
    class Meta:
        model = NIPTImportData
        fields = ['upload_excel']

class NIPTLimsImportForm(forms.ModelForm):
    class Meta:
        model = NIPTImportData
        fields = ['upload_excel']
