# import numpy as np
import pandas as pd
import glob

from settings import GRAPH_FOLDER

def get_dispatcher(path_str):
    # Вырезаем Фамилия И.О из пути по шаблону
    # 'C:\\work\\newoperplan\\testfiles\\Графики\\Диспетчер-1 - Сосяк Наталія Олексіївна\\164 - Яворина\\~$№2317353 патрубок 7219.00.xlsx'
    full_name = path_str.split('Диспетчер-')[-1].split(' - ')[1].split('\\')[0]
    split_name = '%s %s.%s.' % (full_name.split(' ')[0], full_name.split(' ')[1][0], full_name.split(' ')[2][0])
    return split_name

def append_files(base_path):
    all_data = pd.DataFrame()
    ii = 0
    searh_folder = '%s\\**\\*.xlsx' % base_path # маска чтоб выбрать нужные файлы
    for file_path in glob.glob(searh_folder, recursive=True):
        if not "~$" in file_path: # если это не екселевский временный файл
            # идем по файлам найденным в папках и подпапках по шаблону
            dispatcher = get_dispatcher(file_path) # вырезал диспетчера из пути
            try:
                df = pd.read_excel(file_path, sheet_name="График")
                order = df.iloc[1]['Unnamed: 2']
                df.columns = df.iloc[4]
                df = df.iloc[5:]
                df['order'] = order
                df['dispatcher'] = dispatcher
                all_data = all_data.append(df, ignore_index=True, sort=False)
                ii += 1
            except BaseException as idn:
                print(ii, idn, file_path)

    all_data.to_excel('testfiles\\outt.xlsx')


append_files(GRAPH_FOLDER)

# all_data = pd.DataFrame()

# for f in glob.glob("*.xlsx"):
#     df = pd.read_excel(f)
#     all_data = all_data.append(df, ignore_index=True)

# # now save the data frame
# writer = pd.ExcelWriter('testfiles\\output.xlsx')
# all_data.to_excel(writer,'График')
# writer.save()