# -*- coding: utf-8 -*-
""" Работа с файлом Готовые заказы """
import django
import logging
from django.conf import settings
import pandas as pd
import numpy as np
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opersite.settings")
django.setup()

from baseorders.models import Order

logger = logging.getLogger(__name__)
file_path = settings.READY_ORDER_FILE


def readyReadFile(ready_file):
    try:
        df = pd.read_excel(
            ready_file, 
            sheet_name="Готовые заказы",
            dtype={
                'ID':int,
                'Готово':str,
                'Статус в Плане производства':str,
            },
            header=1,
            usecols = [
                'ID', 
                'Готово', 
                'Статус в Плане производства',
                'Дата',
                'Отсутствие тех документации',
                'Дефицит материалов',
                'Дефицит мощностей',
                'Нет технологической возможности (аутсорс)',
                ],
            index_col=0
        )
    except Exception as ind:
        # logger.error("serviceNoteReadFile error with file: %s - %s" % (sn_file, ind))
        print("serviceNoteReadFile error with file: %s - %s" % (ready_file, ind))
    else:
        df = df.rename(columns={
            'ID':'in_id',
            'Готово':'ready',
            'Статус в Плане производства':'status',
            'Дата':'ready_date',
            'Отсутствие тех документации':'failure_1',
            'Дефицит материалов':'failure_2',
            'Дефицит мощностей':'failure_3',
            'Нет технологической возможности (аутсорс)':'failure_4',
            }
        )
        level_map = {'-': False}
        df['produced'] = df['status'].map(level_map)
        level_map = {'+': True}
        df['ready_status'] = df['ready'].map(level_map)
        df = df.drop(['status', 'ready'], axis=1)
        df['ready_status'] = df['ready_status'].fillna(False)
        df['produced'] = df['produced'].fillna(True)

        df['ready_date'] = pd.to_datetime(df['ready_date'], errors='coerce')
        df = df[[
            # 'in_id',
            'produced',
            'ready_status',
            'ready_date',
            'failure_1',
            'failure_2',
            'failure_3',
            'failure_4',
        ]]
        df['ready_date'] = df['ready_date'].dt.date

        df = df.where(df.notnull(), None)
        df = df.replace({pd.NaT: None})
        df = df.replace({np.NaN: None})

        return df

def insertToDB(dftbl):
    for rowindex, row in dftbl.iterrows():
        try:
            order_object = Order.objects.get(in_id=rowindex)
            order_object.produced = row['produced']
            order_object.ready_status = row['ready_status']
            order_object.ready_date = row['ready_date']
            order_object.failure_1 = row['failure_1']
            order_object.failure_2 = row['failure_2']
            order_object.failure_3 = row['failure_3']
            order_object.failure_4 = row['failure_4']
            order_object.save()
        except BaseException as identifier:
            print(identifier, rowindex)

def renew_baseorders_ready_worker():
    readyDf = readyReadFile(file_path)
    readyDf.to_excel("testfiles\\Ready.xlsx")
    insertToDB(readyDf)    

if __name__ == "__main__":
    # from settings import READY_FILE
    renew_baseorders_ready_worker()

    # readyDf = readyReadFile(file_path)
    # readyDf.to_excel("testfiles\\Ready.xlsx")
    # insertToDB(readyDf)