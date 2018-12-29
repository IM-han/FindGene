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
    state_report_choices = (('1','数据导入'),('2','数据确认'),('3','报告生成'),('4','报告导出'))
    sample_number = models.CharField(max_length=50, verbose_name='样本编号', unique=True)
    name = models.CharField(max_length=10, verbose_name='孕妇姓名',blank=True, null=True)
    date_blood = models.DateField(verbose_name='采血时间',blank=True, null=True)
    age = models.CharField(max_length=10, verbose_name='孕妇年龄',blank=True, null=True)
    gestation_weeks = models.CharField(max_length=20, verbose_name='孕周',blank=True, null=True)
    last_menstrual = models.DateField(verbose_name='末次月经',blank=True, null=True)
    fetus_number = models.CharField(max_length=20, choices=fetus_number_choices, default="2", verbose_name='胎儿数量',blank=True, null=True)
    tube_baby = models.CharField(max_length=10, choices=tube_choices, default='0', verbose_name='试管婴儿',blank=True, null=True)
    telephone = models.CharField(max_length=50, verbose_name='联系电话',blank=True, null=True)
    hospital = models.CharField(max_length=50, verbose_name='送检医院',blank=True, null=True)
    doctor = models.CharField(max_length=20, verbose_name='送检医生',blank=True, null=True)
    province = models.CharField(max_length=20, verbose_name='省区',blank=True, null=True)
    remark = models.CharField(max_length=200, verbose_name='备注',blank=True, null=True)
    report_area = models.CharField(max_length=50, choices=area_choices, default='0',blank=True, null=True)
    T13 = models.CharField(max_length=10, verbose_name='13号染色体值',blank=True, null=True)
    T18 = models.CharField(max_length=10, verbose_name='18号染色体值',blank=True, null=True)
    T21 = models.CharField(max_length=10, verbose_name='21号染色体值',blank=True, null=True)
    result = models.CharField(max_length=30, verbose_name='检测结果', choices=result_choices, default='0',blank=True, null=True)
    date_report = models.DateField(verbose_name='报告时间',blank=True, null=True)
    state_report = models.CharField(max_length=20, verbose_name='报告状态', default='1',blank=True, null=True)
    person_import = models.CharField(max_length=10, verbose_name='导入人员',blank=True, null=True)
    date_import = models.DateTimeField(verbose_name='导入时间',blank=True, null=True)
    DS21_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='21号唐筛结果',blank=True, null=True)
    DS21_value = models.CharField(max_length=10, verbose_name='21号唐筛值', blank=True, null=True)
    DS18_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='18号唐筛结果',blank=True, null=True)
    DS18_value = models.CharField(max_length=10, verbose_name='18号唐筛值', blank=True, null=True)
    DSother_result = models.CharField(max_length=10, choices=DS_result_choices, default='0', verbose_name='其他唐筛结果',blank=True, null=True)
    #DSother_value = models.CharField(max_length=10, verbose_name='其他唐筛值', blank=True)
    preghistory = models.CharField(max_length=50, verbose_name='妊娠史', blank=True, null=True)
    upload_excel = models.FileField(upload_to='NIPT/%Y/%m', blank=True, null=True, verbose_name='数据上传表')

    class Meta:
        verbose_name = 'NIPT导入数据表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sample_number