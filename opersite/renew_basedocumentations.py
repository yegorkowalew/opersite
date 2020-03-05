# -*- coding: utf-8 -*-
""" Работа с файлом Служебные записки. Обновление дат документации"""
import django
import logging
from django.conf import settings
import pandas as pd
import numpy as np
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opersite.settings")
django.setup()

logger = logging.getLogger(__name__)
file_path = settings.ORDER_FILE

from basedocumentations.models import ShipmentDates, PickupDates, ServiceNoteDates, DesignDates

obj_list = (ServiceNoteDates, ShipmentDates, PickupDates, DesignDates)

def serviceNoteReadFile(sn_file):
    try:
        df = pd.read_excel(
            sn_file, 
            sheet_name="СЗ",
            usecols=[
            'ID',
            '№ Заказа',
            'Дата СЗ',
            'Дата СЗ Факт',
            'Комплектовочные План Дней от СЗ',
            'Комплектовочные План Вручную',
            'Отгрузочные План Дней от СЗ',
            'Отгрузочные План Вручную',
            'Конструкторская документация План Дней от СЗ',
            'Конструкторская документация План Вручную',
            'Материалы План',
            ],
            parse_dates = [
                # 'Отгрузка "от"',
                # 'Отгрузка "до"',
                'Дата СЗ',
                'Дата СЗ Факт',
                'Комплектовочные План Дней от СЗ',
                'Комплектовочные План Вручную',
                'Отгрузочные План Дней от СЗ',
                'Отгрузочные План Вручную',
                'Конструкторская документация План Дней от СЗ',
                'Конструкторская документация План Вручную',
                'Материалы План',
            ],
            dtype={
                'ID':int,
                'Продукция':str,
                'Контрагент':str,
                '№ Заказа':str,
            },
            # index_col=0
        )

    except Exception as ind:
        # logger.error("serviceNoteReadFile error with file: %s - %s" % (sn_file, ind))
        print("serviceNoteReadFile error with file: %s - %s" % (sn_file, ind))
    else:
        df = df.rename(columns={
            'ID':'in_id',
            '№ Заказа':'order_no',
            'Дата СЗ':'sn_date',
            'Дата СЗ Факт':'sn_date_fact',
            'Комплектовочные План Дней от СЗ':'pickup_plan_days',
            'Комплектовочные План Вручную':'pickup_plan_date',
            'Отгрузочные План Дней от СЗ':'shipping_plan_days',
            'Отгрузочные План Вручную':'shipping_plan_date',
            'Конструкторская документация План Дней от СЗ':'design_plan_days',
            'Конструкторская документация План Вручную':'design_plan_date',
            'Материалы План':'material_plan_date',
            }
        )
        df['sn_date'] = pd.to_datetime(df['sn_date'], errors='coerce')

        def setup_pickup_plan_date(row):
            if not pd.isnull(row['pickup_plan_date']):
                return row['pickup_plan_date']

            if not pd.isnull(row['pickup_plan_days']):
                if not pd.isnull(row['sn_date']):
                    return row['sn_date'] + pd.DateOffset(row['pickup_plan_days'])

            if not pd.isnull(row['sn_date']):
                return row['sn_date']

        def setup_shipping_plan_date(row):
            if not pd.isnull(row['shipping_plan_date']):
                return row['shipping_plan_date']

            if not pd.isnull(row['shipping_plan_days']):
                if not pd.isnull(row['sn_date']):
                    return row['sn_date'] + pd.DateOffset(row['shipping_plan_days'])

            if not pd.isnull(row['sn_date']):
                return row['sn_date']

        def setup_design_plan_date(row):
            if not pd.isnull(row['design_plan_date']):
                return row['design_plan_date']

            if not pd.isnull(row['design_plan_days']):
                if not pd.isnull(row['sn_date']):
                    return row['sn_date'] + pd.DateOffset(row['design_plan_days'])

            if not pd.isnull(row['pickup_plan_date_f']):
                # Если даты по плану нет и если нету дней по плану - берем дату по плану выдачи комплектовочных
                return row['pickup_plan_date_f']

            if not pd.isnull(row['sn_date']):
                return row['sn_date']

        df['pickup_plan_date_f'] = df.apply (lambda row: setup_pickup_plan_date(row), axis=1)
        df['shipping_plan_date_f'] = df.apply (lambda row: setup_shipping_plan_date(row), axis=1)
        df['design_plan_date_f'] = df.apply (lambda row: setup_design_plan_date(row), axis=1)

        # таблица служебных записок
        # in_id
        # order_no
        # sn_plan_start_date
        # sn_plan_end_date
        # sn_fact_end_date
        df_sn = df[['in_id', 'order_no', 'sn_date', 'sn_date', 'sn_date_fact']].copy()
        df_sn.columns = ['in_id','order_no','sn_plan_start_date','sn_plan_end_date','sn_fact_end_date']
        
        df_sn['sn_plan_start_date'] = df_sn['sn_plan_start_date'].dt.date
        df_sn['sn_plan_end_date'] = df_sn['sn_plan_end_date'].dt.date
        df_sn['sn_fact_end_date'] = df_sn['sn_fact_end_date'].dt.date

        df_sn = df_sn.where(df_sn.notnull(), None)
        df_sn = df_sn.replace({pd.NaT: None})
        df_sn = df_sn.replace({np.NaN: None})

        # df_sn[['sn_plan_start_date', 'sn_plan_end_date', 'sn_fact_end_date']] = [df_sn['sn_plan_start_date'].dt.date, df_sn['sn_plan_end_date'].dt.date, df_sn['sn_fact_end_date'].dt.date]

        df_sn_records = df_sn.to_dict('records')

        # таблица комплектовочных ведомостей
        # in_id
        # order_no
        # shipment_plan_start_date
        # shipment_plan_end_date
        # shipment_fact_end_date
        df_shipment = df[['in_id', 'order_no', 'sn_date', 'shipping_plan_date_f']].copy()
        df_shipment.columns = ['in_id','order_no','shipment_plan_start_date','shipment_plan_end_date']

        df_shipment['shipment_plan_start_date'] = df_shipment['shipment_plan_start_date'].dt.date
        df_shipment['shipment_plan_end_date'] = df_shipment['shipment_plan_end_date'].dt.date

        df_shipment = df_shipment.where(df_shipment.notnull(), None)
        df_shipment = df_shipment.replace({pd.NaT: None})
        df_shipment = df_shipment.replace({np.NaN: None})

        df_shipment_records = df_shipment.to_dict('records')

        # таблица отгрузочных спецификаций
        # in_id
        # order_no
        # pickup_plan_start_date
        # pickup_plan_end_date
        # pickup_fact_end_date
        df_pickup = df[['in_id', 'order_no', 'sn_date', 'pickup_plan_date_f']].copy()
        df_pickup.columns = ['in_id','order_no','pickup_plan_start_date','pickup_plan_end_date']

        df_pickup['pickup_plan_start_date'] = df_pickup['pickup_plan_start_date'].dt.date
        df_pickup['pickup_plan_end_date'] = df_pickup['pickup_plan_end_date'].dt.date

        df_pickup = df_pickup.where(df_pickup.notnull(), None)
        df_pickup = df_pickup.replace({pd.NaT: None})
        df_pickup = df_pickup.replace({np.NaN: None})

        df_pickup_records = df_pickup.to_dict('records')

        # таблица Конструкторской документации
        # in_id
        # order_no
        # design_plan_start_date
        # design_plan_end_date
        # design_fact_end_date
        df_design = df[['in_id', 'order_no', 'sn_date', 'design_plan_date_f']].copy()
        df_design.columns = ['in_id','order_no','design_plan_start_date','design_plan_end_date']

        df_design['design_plan_start_date'] = df_design['design_plan_start_date'].dt.date
        df_design['design_plan_end_date'] = df_design['design_plan_end_date'].dt.date
        # df_design  ['design_plan_end_date'] = df_design['design_plan_end_date'].dt.date
        
        # dfmi.loc[:, ('one', 'second')] = value

        df_design = df_design.where(df_design.notnull(), None)
        df_design = df_design.replace({pd.NaT: None})
        df_design = df_design.replace({np.NaN: None})

        df_design_records = df_design.to_dict('records')

        return (df_sn_records, df_shipment_records, df_pickup_records, df_design_records)

# [ServiceNoteDates, ShipmentDates, PickupDates, DesignDates]

def insertToDB(df_records, m_obj):
    """
    Вставляем данные в БД
    """
    model_instances = [m_obj(**record) for record in df_records]
    try:
        m_obj.objects.bulk_create(model_instances)
    except BaseException as identifier:
        fail_text = 'Тип: Файлы дат по плану. Пользователь: %s, Ошибка: %s' % ('Коваленко И.С.', identifier)
        logger.error(fail_text)

def renew_base(file_path, obj_list):
    df_records = serviceNoteReadFile(file_path)
    for df_records, m_obj in zip(df_records, obj_list):
        m_obj.objects.all().delete()
        insertToDB(df_records, m_obj)

def renew_basedocumentations_worker():
    ShipmentDates.objects.all().delete()
    PickupDates.objects.all().delete()
    ServiceNoteDates.objects.all().delete()
    DesignDates.objects.all().delete()
    renew_base(file_path, obj_list)

if __name__ == "__main__":
    renew_basedocumentations_worker()

    # ShipmentDates.objects.all().delete()
    # PickupDates.objects.all().delete()
    # ServiceNoteDates.objects.all().delete()
    # DesignDates.objects.all().delete()
    # renew_base(file_path, obj_list)

    # ProductType.objects.all().delete()
    # Couterparty.objects.all().delete()
    # OfficeNote.objects.all().delete()
    # Order.objects.all().delete()
    # paste_to_db(file_path)
    # dd = serviceNoteReadFile(file_path)
    # insertToDB(dd, ShipmentDates)
    # dd.to_excel('testfile.xlsx')
    # insertToDB(dd, Order)