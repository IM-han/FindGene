# -*- coding: utf-8 -*-

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import ListFlowable
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('simhei-bold', 'simhei-bold.ttf'))
pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttf'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle

from reportlab.lib.pagesizes import A4
import time



def generate_rpt():
    story = []
    stylesheet = getSampleStyleSheet()
    titleStyle = stylesheet['Heading2']
    normalStyle = stylesheet['Normal']
    body = PS(name='body',
              leading=16.5,
              fontName='simhei',
              fontSize=11,)  # leading 设置行间距11+11/2为1.5倍行间距
    body_new = PS(name='body',
              leading=16.5,
              fontName='simhei',
              fontSize=11,)
    # 标题
    rpt_title = '<para autoLeading="off" fontSize=18 align=center><font face="simhei">山东凡迪医学检验实验室</font></para>'
    rpt_subtitle = '<para autoLeading="off" fontSize=18 align=center><font face="simhei">孕妇外周血胎儿游离DNA产前检测报告</font><br/><br/></para>'
    story.append(Paragraph(rpt_title, titleStyle))
    story.append(Paragraph(rpt_subtitle, titleStyle))
    # 样本信息
    component_data = [['送检单位/部门：好孕帮济南孕之门诊部', '', '', '', '样本编号：', '300001703870'],
                      ['姓名：白洁', '', '', '', '采样时间：', '2019-01-04'],
                      ['年龄：22', '', '孕    周：', '18w', '末次月经：', '2018-10-14'],
                      ['单胎/双胎/多胎：单胎', '', '试管婴儿：', '否', '样本类型：', '全血'],
                      ['样本状态：合格', '', '联系电话：', '15562576812', '送检医生：', '托尔斯泰']]
    # 创建表格对象，并设定各列宽度
    component_table = Table(component_data, colWidths=[110, 70, 70, 80, 70, 99])
    # 添加表格样式
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'simhei'),  # 字体
        ('FONTSIZE', (0, 0), (-1, -1), 11),  # 字体大小
        #    ('GRID',(0,0),(-1,-1),0.5,colors.black),#边框颜色及线宽
        ('SPAN', (1, 0), (3, 0)),  # 合并第一行前2-4列
        ('SPAN', (1, 1), (3, 1)),  # 合并第二行前2-4列
        ('SPAN', (0, 0), (1, 0)),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # 在第一行上加横线
        ('LINEBELOW', (0, 4), (-1, 5), 1, colors.black),
    ]))
    story.append(component_table)
    # 表格下面的内容
    text1 = '<para fontSize=11><br/><font face="simhei-bold">检测项目：</font>胎儿染色体非整倍体（T21、T18、T13）检测</para>'
    text2 = '<para fontSize=11><font face="simhei-bold">检测方法与性能：</font>孕妇外周血胎儿游离DNA高通量基因测序分析<br/><br/></para>'
    text3 = '<para fontSize=11><font face="simhei-bold">结果：</font></para>'
    story.append(Paragraph(text1, body))
    story.append(Paragraph(text2, body))
    story.append(Paragraph(text3, body))
    # 检测结果表

    result_desc = Paragraph('''结果描述：提示胎儿21三体、18三体、13三体的风险均为低风险，建议遗传咨询、定期产前检查。''', body)
    other_tips = Paragraph('''其他提示：无''', body)
    #checker = Paragraph("检测者：审核者：报告日期：", body_new)
    checker = Image('SD_checker.png')
    checker.drawHeight = 40
    checker.drawWidth = 60
    detector = Image('SD_detector.png', width=60, height=40)
    suggestion_and_explaination = Paragraph('''建议与解释：''', body)
    content = ListFlowable([Paragraph('''本报告的检测结果只对本次送检的样本负责。''', body),
                            Paragraph('''本报告仅针对21三体综合征、18三体综合征和13三体综合征3种常见胎儿染色体异常。''', body),
                            Paragraph('''该技术不适用的检测孕妇人群为：孕周<12<super>+0</super>周；夫妇有一方有明确染色体异常；1年内接受过异体输血、移植手术、异体细胞治疗等；胎儿超声检查提示有结构异常须进行产前诊断；有基因遗传病家族史或提示胎儿罹患基因病高风险；孕妇合并恶性肿瘤；医师认为有明显影响结果准确性的其他情形。''', body),
                            Paragraph("鉴于当前医学技术发展水平和孕妇个体差异等因素，即使在检测人员已经履行了工作职责和操作规程的前提下，仍有可能出现假阳性和假阴性结果。", body),
                            Paragraph("本检测结果不作为产前诊断结果。如检测结果为高风险，建议受检者接受遗传咨询及相应性产前诊断；如检测结果为未见异常，说明胎儿罹患本检测目标疾病的风险很低，但不排除其他异常的可能性，应当进行胎儿系统超声等其他检查。", body),
                            Paragraph("医疗机构不承担因孕妇提供信息资料不实而导致检测结果不准确的责任。<br/><br/>", body)], bulletType='1')



    result_data = [['检测项目', '检测结果（Z值）', '正常参考值（Z值）', '高风险/低风险'],
                   ['21号染色体', '0.530', '-3～+3', '三体低风险'],
                   ['18号染色体', '-0.150', '-3～+3', '三体低风险'],
                   ['13号染色体', '-0.260', '-3～+3', '三体低风险'],
                   [[result_desc, other_tips]],
                   [[suggestion_and_explaination, content]],
                   ]
    result_table = Table(result_data, colWidths=[125, 125, 125, 124])

    result_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'simhei'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, 3), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 3), 'MIDDLE'),
        ('ALIGN', (0, -1), (0, -1), 'CENTER'),
        ('SPAN', (0, 4), (-1, 4)),
        ('SPAN', (0, 5), (-1, 5)),
        ('SPAN', (0, -1), (-1, -1)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4682B4")),
    ]))
    story.append(result_table)
    # 添加检测者一栏
    new_data = [['检测者：', detector, '审核者：', checker, '报告日期：', '2019年01月09日']]
    new_table = Table(new_data, colWidths=[75, 91, 75, 90, 75, 93])
    new_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'simhei'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBEFORE', (0, 0), (0, 0), 0.5, colors.black),  # 添加左边线
        ('LINEAFTER', (-1, 0), (-1, 0), 0.5, colors.black),  # 添加右边线
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),  # 添加下边线

    ]))
    story.append(new_table)
    #服务电话
    #telephone = Paragraph("<para fontSize=9><br/><font face='simsun'>服务电话：4006-830-321</font></para>", body)
    #story.append(telephone)
    #rpt = SimpleDocTemplate('shangdong.pdf', pageSize=A4)
    #rpt.build(story)
    return story

class Header_and_FooterCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        foot = "服务电话：4006-830-321"
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.25)
        #self.line(66, 78, A4[0] - 66, 78)
        #self.line(66, 78, 530, 78) #页脚横线
        #print(A4[0],A4)
        self.setFont('simsun', 9)
        #self.drawString(A4[0]-x, 65, page)
        self.drawString(48, 65, foot)
        header = "检测基因 关爱未来 让世界不再缺陷"
        logo = 'LOGO.png'
        self.line(48, 780, 548, 780)
        self.drawString(393, 785, header)
        self.drawImage(logo, 48, 782, width=100, height=40)#在页眉添加logo
        SD_seal = 'SD_seal.png'
        self.drawImage(SD_seal, 399, 130, width=100, height=70, mask='auto')#印章
        self.restoreState()



if __name__ == "__main__":
    story = generate_rpt()
    rpt = SimpleDocTemplate('shangdongnew.pdf', pageSize=A4, rightMargin=48, leftMargin=48)
    rpt.multiBuild(story, canvasmaker=Header_and_FooterCanvas)
