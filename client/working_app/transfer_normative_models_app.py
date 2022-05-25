# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:23:33 2022

@author: piebar
"""


# This script is still PSEUDOCODE and UNTESTED.
# It will be tested once we can access the models.
def transfer_normative_model(data_type, model_choice):
    from apply_normative_models_app import apply_normative_model
    from transfer_hbr_models import transfer_hbr_models
    import os
    
    # Map the data type and model choice to the right dirs
    if data_type == "Brain surface area":
        data_subdir = "SurfArea"
    if data_type == "Average Thickness":
        data_subdir = "ThickAvg"
    # else: return error
    
    # TO-DO: create intelligible model names for users, instead of file names.
    model_choice_subdir = model_choice
    
    models_dir = "/project_cephfs/3022051.01/models/"
    chosen_model_dir = os.path.join(models_dir, data_subdir, model_choice)