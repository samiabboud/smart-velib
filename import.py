import scipy.io as sio
import os
import os.path as op
import pandas as pd

db_path = '/media/ssd/open_data/'

hour_df = None
stop_max = 10
iter_n = 0
for filename in os.listdir(db_path):
    iter_n += 1
    if iter_n > stop_max:
        break
    mat_fname = op.join(db_path, filename)
    print('Loading file %s' % mat_fname)
    curr_record = sio.loadmat(mat_fname,
                              chars_as_strings=True, struct_as_record=True,
                              squeeze_me=True)
    minute = curr_record['hourly'][0]
    header = minute.dtype
    header = [key for key in header.fields.keys()]

    index = [record[0] for record in minute]

    for i, minute in enumerate(curr_record['hourly']):
        minute_df = pd.DataFrame(minute, index=index, columns=header, copy=True)
        ab_df = minute_df['available_bikes']
        ab_df.name = 'm%02d%d' % (iter_n, i)
        if hour_df is None:
            hour_df = pd.DataFrame(ab_df)
        else:
            hour_df = hour_df.join(ab_df)
