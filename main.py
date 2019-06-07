import os
import csv
from config import Config


def get_data_paths():
    data_paths = {
        'dev': [],
        'test': [],
        'train': [],
    }
    with open('./file_list.csv', mode='r') as csv_file:
        rows = csv_file.readlines()
        for row in rows[1:]:
            items = row.replace('\n', '').split(',')
            data_type = items[0]
            name = items[1]
            data_paths[data_type].append(os.path.join(Config.ace2005_path, name + '.apf.xml'))
    return data_paths


if __name__ == '__main__':
    data_paths = get_data_paths()
    print(data_paths)
    pass
