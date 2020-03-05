# -*- coding: utf-8 -*-
""" Работа с файлом Служебные записки """
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
file_path = settings.ORDER_FILE

def order_read_file(sn_file):
    try:
        df = pd.read_excel(
            sn_file,
            usecols = [
                'ID',
                'Отгрузка "от"',
                'Отгрузка "до"',
                # 'П/н',
                # 'Согласно КП №',
                # 'Тип продукции',
                'Продукция',
                'Контрагент',
                '№ Заказа',
                'Кол-во',
                '№ СЗ',
                '№ СЗ с изменениями',
                'Дата СЗ',
                # 'Дата СЗ Факт',
                'Комплектовочные План Дней от СЗ',
                'Комплектовочные План Вручную',
                'Отгрузочные План Дней от СЗ',
                'Отгрузочные План Вручную',
                'Конструкторская документация План Дней от СЗ',
                'Конструкторская документация План Вручную',
                'Материалы План',
                # 'Материалы План Дата',
                # 'Черный металл План Дней',
                # 'Черный металл План Дата',
                # 'Оцинкованный металл План Дней',
                # 'Оцинкованный металл План Дата',
                # 'Чугун План Дней',
                # 'Чугун План Дата',
                # 'Описание' 
                ],
            sheet_name="СЗ",
            parse_dates=[
                'Отгрузка "от"',
                'Отгрузка "до"',
                'Дата СЗ',
                # 'Дата СЗ Факт',
                'Комплектовочные План Вручную',
                'Отгрузочные План Вручную',
                'Конструкторская документация План Вручную',
                'Материалы План',
                # 'Черный металл План',
            ],
            dtype={
                'ID': int,
                'Продукция': str,
                'Контрагент': str,
                '№ Заказа': str,
                '№ СЗ': str,
                '№ СЗ с изменениями': str,
                # 'П/н': str,
                # 'Тип продукции': str,
            }
        )

    except Exception as ind:
        logger.error("serviceNoteReadFile error with file: %s - %s" %
                     (sn_file, ind))
    else:
        df = df.rename(columns={
            'ID': 'in_id',
            'Отгрузка "от"': 'shipment_from',
            'Отгрузка "до"': 'shipment_before',
            # 'П/н': 'personal_no',
            # 'Согласно КП №': 'according_to',
            # 'Тип продукции': 'pruduct_type',
            'Продукция': 'product_name',
            'Контрагент': 'couterparty',
            '№ Заказа': 'order_no',
            'Кол-во': 'amount',
            '№ СЗ': 'sn_no',
            '№ СЗ с изменениями': 'sn_no_amended',
            'Дата СЗ': 'sn_plan_date',
            # 'Дата СЗ Факт': 'sn_date_fact',
            'Комплектовочные План Дней от СЗ': 'pickup_plan_days',
            'Комплектовочные План Вручную': 'pickup_plan_date',
            'Отгрузочные План Дней от СЗ': 'shipping_plan_days',
            'Отгрузочные План Вручную': 'shipping_plan_date',
            'Конструкторская документация План Дней от СЗ': 'design_plan_days',
            'Конструкторская документация План Вручную': 'design_plan_date',
            # 'Материалы План Дней': 'material_plan_days',
            'Материалы План': 'material_plan_date',
            # 'Черный металл План Дней': 'black_metal_plan_days',
            # 'Черный металл План Дата': 'black_metal_plan_date',
            # 'Оцинкованный металл План Дней': 'galvanized_metal_plan_days',
            # 'Оцинкованный металл План Дата': 'galvanized_metal_plan_date',
            # 'Чугун План Дней': 'cast_iron_plan_days',
            # 'Чугун План Дата': 'cast_iron_plan_date',
            # 'Описание': 'product_text',
        }
        )
        # df = df.astype(object)
        # df = df.where(df.notnull(), None)
        # df['shipment_from'] = df['shipment_from'].to_datetime()
        df['sn_plan_date'] = pd.to_datetime(df['sn_plan_date'])
        df['amount'] = df['amount'].str.replace(',', '.').astype(float)
        # df['amount'] = df['amount'].astype(float)

        df['shipment_from'] = df['shipment_from'].dt.date
        df['shipment_before'] = df['shipment_before'].dt.date
        df['sn_plan_date'] = df['sn_plan_date'].dt.date
        df['pickup_plan_date'] = df['pickup_plan_date'].dt.date
        df['shipping_plan_date'] = df['shipping_plan_date'].dt.date
        df['design_plan_date'] = df['design_plan_date'].dt.date
        df['material_plan_date'] = df['material_plan_date'].dt.date
        df = df.where(df.notnull(), None)
        df = df.replace({pd.NaT: None})
        df = df.replace({np.NaN: None})
        # print(df['shipment_from'].dtype)
        df_records = df.to_dict('records')
        return df_records

def insertToDB(df_records, m_obj):
    """
    Вставляем данные в БД
    """
    model_instances = [m_obj(**record) for record in df_records]
    try:
        m_obj.objects.bulk_create(model_instances)
    except BaseException as identifier:
        logger.error("insertToDB error with class: %s, %s" % (m_obj.__class__.__name__, identifier))

def renew_baseorders_worker():
    Order.objects.all().delete()
    order_records = order_read_file(file_path)
    insertToDB(order_records, Order)

if __name__ == "__main__":
    renew_baseorders_worker()
    # работает