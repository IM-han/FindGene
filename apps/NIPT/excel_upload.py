#用于上传excel文件

import xlrd
from FindGene.settings import MEDIA_ROOT

class ExcelImport:
    def __init__(self, file_name):
        #文件路径修改
        self.file_name = (MEDIA_ROOT + str(file_name)).decode("utf-8")
        self.workbook = xlrd.open_workbook(self.file_name)
        self.table = self.workbook.sheets()[0]#取第一张表
        #获取总行数
        self.nrows = self.table.nrows

        self.sams = []

    def get_sam(self):
        #除去表头
        for x in range(1, self.nrows):
            row = self.table.row_values(x)
            self.sams.append(
                {
                    "sample_number": row[0],
                    "name": row[2],
                    "date_blood": row[1],
                    "age": row[3],
                    "gestation_weeks": row[4],
                    "last_menstrual": row[11],
                    "fetus_number": row[12],
                    "telephone": row[14],
                    "hospital": row[15],
                    "doctor": row[16],
                    "province": row[17],
                    "remark": row[19],
                    "report_area": row[18],
                    "T13": row[21],
                    "T18": row[22],
                    "T21": row[23],
                    "result": row[20],
                    "state_report": '0',
                    "date_report": row[24],
                    "DS21_result": row[5],
                    "DS21_value": row[6],
                    "DS18_result": row[7],
                    "DS18_value": row[8],
                    "DSother_result": row[9]
            }
            )