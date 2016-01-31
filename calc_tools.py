# -*- coding: utf-8 -*-
import ast
from pprint import pprint as pp
import logging
# import numpy as np
# routem, mapm, dropboxm, gmaps, tools, bokehm, tspm

logger = logging.getLogger(__name__)

def type_of_value(var):
    try:
       return type(ast.literal_eval(var))
    except Exception:
       return str


import logging.config, os, yaml

def setup_logging(
    default_path='app_logging.yaml', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_string_caller_objclass_method(obj,inspect_stack):
    return "\n%s() -> " % (inspect_stack[1][3])+obj.__class__.__name__+"#%s()" % (inspect_stack[0][3])

def print_vars_values_types(obj, with_id=False):
    out_str = ""
    sorted_var_list = [revvar[::-1] for revvar in sorted([var[::-1] for var in  dir(obj)])]
    # sorted_var_list = sorted(dir(obj))
    for var in sorted_var_list:
        if not (var.startswith("__") and var not in ['os','sys']):
            cons_width = 80
            out_str_part = ''
            try:
                var_value = obj.__dict__[var]
            except (KeyError, AttributeError):
                continue
            out_str_part += var + " "*(cons_width/4-len(var)) + str(var_value)[:cons_width/2]
            out_str_part += " "*(cons_width/2-len(str(var_value)[:cons_width/2])) + str(type(var_value))
            out_str_part = out_str_part[:cons_width-1] + "\n"
            if with_id:
                out_str_part += str(hex(id(var_value))) + "\n"
            out_str += out_str_part
    return out_str

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None) # b itterator is moved one step forward from initial position
    return itertools.izip(a, b)

