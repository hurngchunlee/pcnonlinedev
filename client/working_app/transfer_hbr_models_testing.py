#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:47:34 2022

@author: piebar
"""

def transfer_hbr_models(test_data, adaptation_data):
    import os
    import pandas as pd
    #import pcntoolkit as ptk
    import numpy as np
    import pickle
    from matplotlib import pyplot as plt
    processing_dir = "/project_cephfs/3022051.01/"    # replace with a path to your working directory
    if not os.path.isdir(processing_dir):
        os.makedirs(processing_dir)
    os.chdir(processing_dir)
    processing_dir = os.getcwd()
    idps = ['rh_MeanThickness_thickness','lh_MeanThickness_thickness']

    X_adapt = (adaptation_data['age']/100).to_numpy(dtype=float)
    Y_adapt = adaptation_data[idps].to_numpy(dtype=float)
    batch_effects_adapt = adaptation_data[['sitenum','sex']].to_numpy(dtype=int)
    
    sites = test_data['site'].unique()
    test_data['sitenum'] = 0
    for i,s in enumerate(sites):
        idx = test_data['site'] == s
        test_data['sitenum'].loc[idx] = i
        
    sites = adaptation_data['site'].unique()
    adaptation_data['sitenum'] = 0
    for i,s in enumerate(sites):
        idx = adaptation_data['site'] == s
        adaptation_data['sitenum'].loc[idx] = i
        
    with open('X_adaptation.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(X_adapt), file)
    with open('Y_adaptation.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(Y_adapt), file)
    with open('adbefile.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(batch_effects_adapt), file)
    
    # Test data (new dataset)
    X_test_txfr = (test_data['age']/100).to_numpy(dtype=float)
    Y_test_txfr = test_data[idps].to_numpy(dtype=float)
    batch_effects_test_txfr = test_data[['sitenum','sex']].to_numpy(dtype=int)
    
    with open('X_test_txfr.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(X_test_txfr), file)
    with open('Y_test_txfr.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(Y_test_txfr), file)
    with open('txbefile.pkl', 'wb') as file:
        pickle.dump(pd.DataFrame(batch_effects_test_txfr), file)
        
    respfile = os.path.join(processing_dir, 'Y_adaptation.pkl')
    covfile = os.path.join(processing_dir, 'X_adaptation.pkl')
    testrespfile_path = os.path.join(processing_dir, 'Y_test_txfr.pkl')
    testcovfile_path = os.path.join(processing_dir, 'X_test_txfr.pkl')
    trbefile = os.path.join(processing_dir, 'adbefile.pkl')
    tsbefile = os.path.join(processing_dir, 'txbefile.pkl')
    
    log_dir = os.path.join(processing_dir, 'log_transfer/')
    output_path = os.path.join(processing_dir, 'Transfer/')
    model_path = os.path.join(processing_dir, 'Models/')  # path to the previously trained models
    outputsuffix = '_transfer'  # suffix added to the output files from the transfer function
    
#    yhat, s2, z_scores = ptk.normative.transfer(covfile=covfile,
#                                            respfile=respfile,
#                                            tsbefile=tsbefile,
#                                            trbefile=trbefile,
#                                            model_path = model_path,
#                                            alg='hbr',
#                                            log_path=log_dir,
#                                            binary=True,
#                                            output_path=output_path,
#                                            testcov= testcovfile_path,
#                                            testresp = testrespfile_path,
#                                            outputsuffix=outputsuffix,
#                                            savemodel=True)
import pandas as pd
import os
os.chdir(r"C:\Users\piebar\Documents\GitHub\pcnonlinedev\client\working_app")
adaptation_file = pd.read_csv('fcon1000_te.csv')
test_file = pd.read_csv('fcon1000_tr.csv')

transfer_hbr_models(test_file, adaptation_file)