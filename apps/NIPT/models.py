from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class NIPTImportData(models.Model):
    tube_choices = (('0','否'),('1','是'))
    area_choices = (('0','成都'),('1','福州总医院'),('2','湘雅医院'),('3','贵州医科大学附属医院'),('4','吉林省妇幼'),('5','西南医院'),('6','长治妇幼'),('7','山东检验所'),('8','山东凡迪'),('9','广东省妇幼'),('10','扬州市妇幼保健院'),('11','宜春妇幼保健医院'),('12','河北省医科大学第二医院'),('13','武汉市中心医院'))
    result_choices = (('0','未见异常'),('1','chr13三体高风险'),('2','chr13三体低风险'),('3','chr18三体高风险'),('4','chr18三体低风险'),('5','chr21三体低风险'),('6','chr21三体低风险'))
    fetus_number_choices = (('0','单胎'),('1','双胎'),('2','三胎'),('3','多胎'))
    DS_result_choices = (('0','未做'),('1','高危'),('2','低危'))
    sample_number = models.CharField(max_length=50, verbose_name='样本编号', unique=True)
    name = models.CharField(max_length=10, verbose_name='孕妇姓名')
    date_blood = models.DateTimeField(default='', verbose_name='采血时间')
    age = models.CharField(max_length=10, verbose_name='孕妇年龄')
    gestation_weeks = models.CharField(max_length=20, verbose_name='孕周')
    last_menstrual = models.DateTimeField(default='', verbose_name='末次月经')
    fetus_number = models.CharField(max_length=10, choices=fetus_number_choices, default=0,verbose_name='胎儿数量')
    tube_baby = models.CharField(max_length=10, choices=tube_choices, default='0', verbose_name='试管婴儿')
    telephone = models.CharField(max_length=50, verbose_name='联系电话')
    hospital = models.CharField(max_length=50, verbose_name='送检医院')
    doctor = models.CharField(max_length=20, verbose_name='送检医生')
    province = models.CharField(max_length=20, verbose_name='省区')
    remark = models.CharField(max_length=200, verbose_name='备注')
    report_area = models.CharField(max_length=50, choices=area_choices, default='0', verbose_name='报告区域')
    T13 = models.CharField(max_length=10, verbose_name='13号染色体值')
    T18 = models.CharField(max_length=10, verbose_name='18号染色体值')
    T21 = models.CharField(max_length=10, verbose_name='21号染色体值')
    result = models.CharField(max_length=30, verbose_name='检测结果')
    date_report = models.DateTimeField(default='', verbose_name='报告时间')
    state_report = models.DateTimeField(default='', verbose_name='报告状态')
    person_import = models.CharField(max_length=10, verbose_name='导入人员')
    date_import = models.DateTimeField(default='', verbose_name='导入时间')
    DS21_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='21号唐筛结果',null=True)
    DS21_value = models.CharField(max_length=10, verbose_name='21号唐筛值', null=True)
    DS18_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='18号唐筛结果',null=True)
    DS18_value = models.CharField(max_length=10, verbose_name='18号唐筛值', null=True)
    DSother_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='其他唐筛结果',null=True)
    DSother_value = models.CharField(max_length=10, verbose_name='其他唐筛值', null=True)
    preghistory = models.CharField(max_length=50, null=True, verbose_name='妊娠史')

    class Meta:
        verbose_name = 'NIPT导入数据表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sample_number