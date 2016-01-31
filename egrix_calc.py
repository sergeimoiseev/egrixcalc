# -*- coding: utf-8 -*-
import re, yaml, logging, inspect
import calc_tools, dropboxm
logger = logging.getLogger(__name__)

def read_params_dict(from_dropbox=True):
    logger.debug(calc_tools.get_string_caller_objclass_method(read_params_dict,inspect.stack()))

    d = {}

    if from_dropbox:
        logger.debug("reading from dropbox")
        dr_fname = 'params.txt'
        dc = dropboxm.DropboxConnection()
        with dc.open_dropbox_file(dr_fname) as dr_f:
            srt_params = dr_f.read().decode('utf-8')
    else:
        logger.debug("reading from local txt file")
        srt_params = open("params.txt",'rb').read().decode('utf-8')

    lines_list = srt_params.split('\n')
    for i,line in enumerate(lines_list):
        logger.debug("line\n%s" % (line,))
        if '=' not in line:
            continue
        tmp_list = [p.strip() for p in re.split('=|#',line)]
        comment = tmp_list[-1] # not used!
        try:
            float_value = float(tmp_list[1])
        except Exception as e:
            float_value = False
        d[tmp_list[0]] = float_value
    return d

def get_and_store_params():
    logger.debug(calc_tools.get_string_caller_objclass_method(get_and_store_params,inspect.stack()))

    params_dict = {}
    #try to load prarms from dropbox
    try:
        params_dict = read_params_dict(from_dropbox=True)
        read_dropbox_successfully = True
    except Exception as e: 
        read_dropbox_successfully = False
    if len(params_dict)==0:
        read_dropbox_successfully = False

    if not read_dropbox_successfully:
        # if no success - load params_dict from yaml file
        with open('params.yml', 'r') as backup_file:
            params_dict = yaml.load(backup_file)

    with open('params.yml', 'w') as outfile:
        outfile.write( yaml.dump(params_dict, default_flow_style=True) )
    return params_dict

if __name__ == '__main__':
    calc_tools.setup_logging()
    d = get_and_store_params()
    # d = read_params_dict(from_dropbox=True)
    print(d)
