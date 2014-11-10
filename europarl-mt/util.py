# -*- coding: utf-8 -*-

import os

def mkdir(dir_path):
    os.system('mkdir '+dir_path)
    
    
def create_experiment(experiment_folder_name, moses_script_path):
    mkdir(experiment_folder_name)
    os.chdir(experiment_folder_name)
    script = ['#!/bin/bash']+['\n']
    script += ["MOSES_SCRIPT="+moses_script_path] + ["EXPERIMENT="+os.getcwd()] 
    return script
    