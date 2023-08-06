#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# Some functions to red config files
###############################################################################
import logging
import os.path
import codecs
import yaml

import pymdtools.common


###############################################################################
# Compute an absolute path from the config parameter
#
# @param paths list of paths to compute
# @return the absolute path
###############################################################################
def path(*paths):
    result = ""
    for path_element in paths:
        if len(result) > 0:
            result = os.path.join(path_element, result)
        else:
            result = path_element
        if os.path.isabs(result):
            return pymdtools.common.set_correct_path(result)

    return pymdtools.common.set_correct_path(result)


###############################################################################
# Expand paths in the config file
#
# @param data the config part
# @param root the root of the config part
# @return the dict of the config
###############################################################################
def expand_paths(data, root):
    if 'root' not in data:
        data['root'] = './'

    # Set the root path absolute
    data['root'] = path(data['root'], root)

    for key in data:
        if isinstance(data[key], dict):
            data[key] = expand_paths(data[key], data['root'])
        elif isinstance(data[key], list):
            new_list = []
            for element in data[key]:
                new_list.append(path(element, data['root'], root))
            data[key] = new_list
        else:
            data[key] = path(data[key], data['root'], root)

    return data

###############################################################################
# Read conf yaml
#
# @param filename the config filename
# @return the dict of the config
###############################################################################
def read_yaml(filename):
    logging.debug('Read the yaml config file %s', (filename))
    filename = pymdtools.common.check_is_file_and_correct_path(filename)
    with codecs.open(filename, "r", "utf-8") as ymlfile:
        result = yaml.load(ymlfile, Loader=yaml.FullLoader)

    logging.debug('Read finished for the yaml config file %s', (filename))

    if 'paths' not in result:
        return result

    logging.debug('Add some info in the config result for all paths')

    result['paths'] = expand_paths(result['paths'],
                                   os.path.split(filename)[0])

    if 'conf_folder' not in result['paths']:
        result['paths']['conf_folder'] = os.path.split(filename)[0]
    if 'conf_filename' not in result['paths']:
        result['paths']['conf_filename'] = filename

    return result

###############################################################################
# Write a yaml config conf yaml
#
# @param data the data to write
# @param filename the config filename
# @return empty
###############################################################################
def write_yaml(filename, data):
    filename = pymdtools.common.set_correct_path(filename)
    logging.debug('Write the yaml config file %s', (filename))
    stream = open(filename, 'w', encoding=('utf-8'))
    yaml.dump(data, stream,
              default_flow_style=False, encoding=('utf-8'),
              allow_unicode=True)
    stream.close()

    logging.debug('Write finished for the yaml config file %s', (filename))
