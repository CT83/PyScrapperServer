import os
from shutil import copy


def clean_prev(bk_name):
    try:
        os.remove(bk_name + '.pdf')
        os.remove(bk_name + '.txt')
    except OSError as e:
        pass


def write_convert_and_rename(bk_text, bk_name=""):
    clean_prev(bk_name)
    f = open(bk_name + '.txt', 'w')
    f.write(bk_text.encode('ascii', 'ignore'))
    f.close()
    os.system(
        'python txt2pdf.py -n --title "' + bk_name.replace('_', ' ') + '" -o ' + bk_name + '.pdf ' + bk_name + '.txt')
    copy(bk_name + '.pdf', 'path')
    clean_prev(bk_name)