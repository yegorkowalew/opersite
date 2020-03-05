# -*- coding: utf-8 -*-
""" Работа с папкой прихода документации. Обновление фактических дат документации"""
import glob
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
in_document_folder = settings.IN_DOCUMENT_FOLDER
in_document_file = settings.IN_DOCUMENT_FILE
tech_doc_base_file = settings.TECH_DOC_BASE_FILE
tech_doc_deficit_folder = settings.TECH_DOC_DEFICIT_FOLDER

from basedocumentations.models import PickupDates, ShipmentDates, DesignDates
from baseorders.models import Order
import basedocumentations
def inDocumentReadFile(path, file_name):
    try:
        df = pd.read_excel(
            os.path.join(path, file_name),
            sheet_name="График",
            header=3,
            usecols = [
                'ID',
                'ДПКД % 1',
                'ДПКД Дата 1',
                'ДПКД Дата 2',
                'ДПКД Дата 3',
                'ДПОД % 1',
                'ДПОД Дата 1',
                'ДПОД Дата 2',
                'ДПОД Дата 3',
            ],

            parse_dates = [
                'ДПКД Дата 1',
                'ДПКД Дата 2',
                'ДПКД Дата 3',
                'ДПОД Дата 1',
                'ДПОД Дата 2',
                'ДПОД Дата 3',
            ],

            dtype={
                'ID':int,
            },
        )

    except Exception as ind:
        # logger.error("inDocumentReadFile error with file: %s - %s" % (file_name, ind))
        fail_text = 'Тип: Файлы конструкторской документации. Диспетчер: Коваленко И.С., Ошибка: %s. Файл: %s' % (ind, file_name)
        print(fail_text)
    else:
        df = df.rename(columns={
            'ID':'in_id',
            'Диспетчер':'dispatcher',
            'ДПКД % 1':'pickup_issue',
            'ДПКД Дата 1':'pickup_date_1',
            'ДПКД Дата 2':'pickup_date_2',
            'ДПКД Дата 3':'pickup_date_3',
            'ДПОД % 1':'shipping_issue',
            'ДПОД Дата 1':'shipping_date_1',
            'ДПОД Дата 2':'shipping_date_2',
            'ДПОД Дата 3':'shipping_date_3',
            }
        )
        df['dispatcher'] = os.path.split(path)[-1]
        df['pickup_date_1'] = pd.to_datetime(df['pickup_date_1'])
        df['pickup_date_2'] = pd.to_datetime(df['pickup_date_2'])
        df['pickup_date_3'] = pd.to_datetime(df['pickup_date_3'])
        df['shipping_date_1'] = pd.to_datetime(df['shipping_date_1'])
        df['shipping_date_2'] = pd.to_datetime(df['shipping_date_2'])
        df['shipping_date_3'] = pd.to_datetime(df['shipping_date_3'])

        df = df.astype({
            'pickup_date_1':'object',
            'pickup_date_2':'object',
            'pickup_date_3':'object',
            'shipping_date_1':'object',
            'shipping_date_2':'object',
            'shipping_date_3':'object',
            })
        def setup_pickup_date(row):
            return max([row['pickup_date_1'], row['pickup_date_2'], row['pickup_date_3']])
        
        def setup_shipping_date(row):
            return max([row['shipping_date_1'], row['shipping_date_2'], row['shipping_date_3']])
        df['pickup_date'] = df.apply (lambda row: setup_pickup_date(row), axis=1)
        df['shipping_date'] = df.apply (lambda row: setup_shipping_date(row), axis=1)

        def setup_pickup_issue(row):
            if row['pickup_issue'] == 0:
                return False
            else:
                return True
        df['pickup_issue_f'] = df.apply (lambda row: setup_pickup_issue(row), axis=1)

        def setup_shipping_issue(row):
            if row['shipping_issue'] == 0:
                return False
            else:
                return True
        df['shipping_issue_f'] = df.apply (lambda row: setup_shipping_issue(row), axis=1)

        df = df[['in_id', 'dispatcher', 'pickup_date', 'shipping_date', 'pickup_issue_f', 'shipping_issue_f']]
        df = df.set_index('in_id')
        return df

def inDocumentFindFile(in_folder, need_file):
    tree = os.walk(in_folder)
    folder_list = []
    for i in tree:
        for address, dirs, files in [i]:
            for fl in files:
                if fl == need_file:
                    folder_list.append(address)
    return folder_list

def inDocumentRebuild(in_folder, need_file):
    df_list = []
    for folder in inDocumentFindFile(in_folder, need_file):
        df = inDocumentReadFile(folder, need_file)
        df_list.append(df)
    return df_list

def get_col_header(dispatcher_len):
    col_header = [
        'dispatcher',
        'pickup_date',
        'shipping_date',
        'pickup_issue',
        'shipping_issue',
    ]
    df_header = []
    for disp_num in range(1, dispatcher_len+1):
        for col_header_name in col_header:
            df_header.append('%s_%s' % (col_header_name, str(disp_num)))
    return df_header

def get_col_header_disp(name, dispatcher_len, row):
    df_list = []
    for num in range(1, dispatcher_len+1):
        col_name = '%s_%s' % (name, str(num))
        df_list.append(row[col_name])
    return df_list

def tablestodf(IN_DOCUMENT_FILE, IN_DOCUMENT_FOLDER):
    df_arr = inDocumentRebuild(IN_DOCUMENT_FOLDER, IN_DOCUMENT_FILE)
    dispatcher_len = len(df_arr)
    result = pd.concat(df_arr, axis=1, sort=False)
    result.columns = get_col_header(dispatcher_len)
    def example(row):
        doc_type_list = [
            'pickup',
            'shipping',
        ]
        for doc_type in doc_type_list:
            doc_type_is = '%s_%s' % (doc_type, 'issue')
            disp_doc_type_is = 'dispatcher_%s_%s' % (doc_type, 'issue')

            iss_df = pd.DataFrame({
                'date': get_col_header_disp(doc_type_is, dispatcher_len, row),
                'disp': get_col_header_disp('dispatcher', dispatcher_len, row)
            })
            
            iss_df = iss_df[(iss_df['date']==False)]
            if iss_df.empty != True:
                row[doc_type_is] = False
                row[disp_doc_type_is] = iss_df.loc[iss_df.index[0], 'disp']
            else:
                row[doc_type_is] = None
                row[disp_doc_type_is] = None

            doc_type_is = '%s_%s' % (doc_type, 'date')
            disp_doc_type_is = 'dispatcher_%s_%s' % (doc_type, 'date')

            cut_df = pd.DataFrame({
                'date': get_col_header_disp(doc_type_is, dispatcher_len, row),
                'disp': get_col_header_disp('dispatcher', dispatcher_len, row)
            })
            cut_df = cut_df.dropna()
            if cut_df.empty != True:
                cut_df = cut_df.loc[cut_df['date'].idxmax()]
                row[doc_type_is] = cut_df['date']
                row[disp_doc_type_is] = cut_df['disp']
            else:
                row[doc_type_is] = None
                row[disp_doc_type_is] = None
        return row

    result = result.apply(example, axis=1)
    result = result[[
            'pickup_date',
            'dispatcher_pickup_date',
            'pickup_issue',
            'dispatcher_pickup_issue',
            'shipping_date',
            'dispatcher_shipping_date',
            'shipping_issue',
            'dispatcher_shipping_issue',
        ]]
    result = result.dropna(how='all')
    # print(result)
    return result

def renew_kw_os(dftbl):
    for rowindex, row in dftbl.iterrows():
        try:
            pickup_object = PickupDates.objects.get(in_id=rowindex) 
        except BaseException as identifier:
            fail_text = 'Тип: Файлы конструкторской документации. Диспетчер: Коваленко И.С., Ошибка: %s' % (identifier)
            print(fail_text)
        else:
            if row['pickup_issue'] == False:
                pickup_object.pickup_dispatcher = row['dispatcher_pickup_issue']
                pickup_object.pickup_need = False
                pickup_object.pickup_fact_end_date = pickup_object.pickup_plan_end_date
                pickup_object.save()
            elif not pd.isnull(row['pickup_date']):
                pickup_object.pickup_dispatcher = row['dispatcher_pickup_date']
                pickup_object.pickup_fact_end_date = row['pickup_date']
                pickup_object.save()
        
        try:
            shipment_object = ShipmentDates.objects.get(in_id=rowindex) 
        except BaseException as identifier:
            fail_text = 'Тип: Файлы конструкторской документации. Диспетчер: Коваленко И.С., Ошибка: %s' % (identifier)
            print(fail_text)
        else:
            if row['shipping_issue'] == False:
                shipment_object.shipment_dispatcher = row['dispatcher_shipping_issue']
                shipment_object.shipment_need = False
                shipment_object.shipment_fact_end_date = shipment_object.shipment_plan_end_date
                shipment_object.save()
            elif not pd.isnull(row['shipping_date']):
                shipment_object.shipment_dispatcher = row['dispatcher_shipping_date']
                shipment_object.shipment_fact_end_date = row['shipping_date']
                shipment_object.save()

"""
Работа с дифицитами
"""
def get_dispatcher_from_path(path_str):
    # Не факт что эта фигня будет всю жизнь работать правильно
    return path_str.split('\\')[-2] 

def techdocbase(in_folder):
    all_data = pd.DataFrame()
    search_dir = '%s\\**\\*.xlsx' % (in_folder)
    for file_path in glob.glob(search_dir): # Все .xlsx файлы в папке
        dispatcher = get_dispatcher_from_path(file_path) # выдираем имя диспетчера из папки
        try:
            df = pd.read_excel(file_path, sheet_name="Лист1")
            order = df.iloc[0]['Unnamed: 1']
            if pd.isnull(order):
                raise ValueError('Не указан номер заказа')
            header_row = list(df.loc[np.where(df['Unnamed: 0'] == 'Наименование')].index)[0]
            if not header_row > 0:
                raise ValueError('Не нашел шапку таблицы')
            df.columns = df.iloc[header_row]
            df = df.iloc[header_row+1:]
            df = df.dropna(how='all')
            df['Диспетчер'] = dispatcher
            df['Заказ №'] = order
            df['Путь к файлу'] = file_path
            all_data = all_data.append(df, ignore_index=True, sort=False)
            df = df.dropna(subset=['Наименование'])
        except ValueError as identifier:
            fail_text = 'Тип: Файлы конструкторской документации. Диспетчер: %s, Ошибка: %s, Файл: %s' % (dispatcher, identifier, file_path)
            print(fail_text)
    
    bool_series = pd.isnull(all_data["Наименование"])
    fail_df = all_data[bool_series]
    for _, row in fail_df.iterrows():
        fail_text = 'Тип: Файлы конструкторской документации. Диспетчер: %s, Ошибка: не указано "Наименование", в файле: %s' % (row['Диспетчер'], row['Путь к файлу'])
        print(fail_text)
    bool_series = pd.notnull(all_data["Наименование"])
    all_data = all_data[bool_series]
    # print(all_data.filter(items=['Наименование']))
    # df.filter(items=['one', 'three'])

    # Группировка по максимальной дате
    all_data['Дата выдачи'] =  pd.to_datetime(all_data['Дата выдачи'])
    all_data['Диспетчер'] = all_data['Диспетчер'] + '||'
    all_data = all_data.groupby(['Заказ №']).agg({'Дата выдачи':'max', 'Диспетчер': 'sum'})
    all_data['Диспетчер'] = all_data['Диспетчер'].apply(lambda x: x.split('||')[0])
    # На выходе имеем таблицу с номером заказа, датой и диспетчером
    # all_data.to_excel('group.xlsx')
    all_data = all_data.reset_index(level='Заказ №', col_level=1, col_fill='Заказ №')
    df['Заказ №'] = df['Заказ №'].astype(str)
    # print(all_data)
    return all_data

def renew_kd(dftbl):
    dftbl.to_excel('out2.xlsx')
    for rowindex, row in dftbl.iterrows():
        try:
            order_object = Order.objects.get(order_no=row['Заказ №'])
            design_object = DesignDates.objects.get(in_id=order_object.in_id)
            if not pd.isnull(row['Дата выдачи']):
                design_object.design_fact_end_date = row['Дата выдачи']
                design_object.design_dispatcher = row['Диспетчер']
                design_object.design_need = True
                design_object.save()
            else:
                design_object.design_dispatcher = row['Диспетчер']
                design_object.design_need = True
                design_object.save()
            # print(design_object.order_no, design_object.in_id)
        except BaseException as identifier:
            print(identifier, row['Заказ №'])

def renew_basedocumentations_fact_worker():
    kw_os_df = tablestodf(in_document_file, in_document_folder)
    # kw_os_df.to_excel('out1.xlsx')
    renew_kw_os(kw_os_df)

    kd_df = techdocbase(tech_doc_deficit_folder)
    renew_kd(kd_df)

if __name__ == "__main__":
    # tablestodf(in_document_file, in_document_folder).to_excel('out1.xlsx')
    renew_basedocumentations_fact_worker()