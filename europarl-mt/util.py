# -*- coding: utf-8 -*-

import os

def mkdir(dir_path):
    os.system('mkdir '+dir_path)
    
    
def create_experiment(experiment_folder_name, moses_script_path):
    script = ['#!/bin/bash']+['\n']
    script += ["MOSES_SCRIPT="+moses_script_path] + ["EXPERIMENT="+os.getcwd()+'/'+experiment_folder_name]
    script += ['\n'] + ['mkdir '+experiment_folder_name]
    script += ['cd '+ experiment_folder_name]
    return script
    
def find_moses():
    return os.popen('cd; locate -b "mosesdecoder" | head -n 1').read().strip()+'/script'