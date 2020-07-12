
import os
import pandas

from core_utils import file_utils


def update_stock_bar_csv(file_path, kw_arg=None):
    print('--- file_path:', file_path, kw_arg)

    dir_path, file_name = os.path.split(file_path)
    if file_name.startswith('bar-') and file_name.endswith('csv'):
        prefix, adj, freq, start_date, end_date, ts_code = file_name.split('-')

        df = pandas.read_csv(file_path, index_col=0)
        df['freq'] = freq
        df['adj'] = adj
        df.to_csv(os.path.join(kw_arg['output_path'], file_name), float_format='%.4f')


if __name__ == '__main__':
    path = '/Users/lixiang/userdata/output_data/stock_bar_data/ks/tmp'
    output_path = '/Users/lixiang/userdata/output_data/stock_bar_data'
    failed_paths = []
    arg_map = {'output_path': output_path}

    file_utils.walk_sorted(update_stock_bar_csv, path, failed_paths, kwargs=arg_map)

    print('--- failed_paths:', failed_paths)
