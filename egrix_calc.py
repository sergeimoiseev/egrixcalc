# -*- coding: utf-8 -*-
import re, yaml, logging, inspect
import calc_tools, dropboxm
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    calc_tools.setup_logging()
    d = calc_tools.get_and_store_params()
    # d = read_params_dict(from_dropbox=True)
    print(d)
