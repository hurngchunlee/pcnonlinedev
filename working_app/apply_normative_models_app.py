# -*- coding: utf-8 -*-

''' Script to run normative model in a Docker container.

Adapted the eLife Braincharts Jupyter notebook into a python script to be run in a container on the Donders cluster. 
The Dockerfile sets up the required dependencies and necessary data files and directory structure.

Written by Saige Rutherford on 18-02-2022.
Adjusted for testing on a website by Pieter Barkema.
'''

def apply_normative_model(algorithm, data_type, app_test_data, app_adaptation_data, root_dir="/home/"):
    import os, sys
    import numpy as np
    import pandas as pd
    from pcntoolkit.normative import predict
    from pcntoolkit.util.utils import create_design_matrix
   # print(sys.path)
    #print(os.getcwd())
    site_names = 'site_ids_82sites.txt'
    model_name = 'lifespan_57K_82sites'

    # where the analysis takes place
    out_dir = os.path.join(root_dir, 'models', data_type, model_name)

    # load a set of site ids from this model. This must match the training data
    with open(os.path.join(root_dir,'docs', site_names)) as f:
        site_ids_tr = f.read().splitlines()
    #shouldnt be path to docs, but a csv uploaded from website
    #test_data = os.path.join(root_dir, 'docs/OpenNeuroTransfer_te.csv')
    df_te = app_test_data#pd.read_csv(test_data)

    # extract a list of unique site ids from the test set
    site_ids_te =  sorted(set(df_te['site'].to_list()))

    #adaptation_data = os.path.join(root_dir, 'docs/OpenNeuroTransfer_tr.csv')
    df_ad = app_adaptation_data

    # load the list of idps for left and right hemispheres, plus subcortical regions
    with open(os.path.join(root_dir,'docs','phenotypes_lh.txt')) as f:
        idp_ids_lh = f.read().splitlines()
    with open(os.path.join(root_dir,'docs','phenotypes_rh.txt')) as f:
        idp_ids_rh = f.read().splitlines()
    with open(os.path.join(root_dir,'docs','phenotypes_sc.txt')) as f:
        idp_ids_sc = f.read().splitlines()

    # we choose here to process all idps
    idp_ids = idp_ids_lh + idp_ids_rh + idp_ids_sc

    # which data columns do we wish to use as covariates? 
    cols_cov = ['age','sex']

    # limits for cubic B-spline basis 
    xmin = -5 
    xmax = 110

    for idp_num, idp in enumerate(idp_ids): 
        print('Running IDP', idp_num, idp, ':')
        idp_dir = os.path.join(out_dir, idp)
        os.chdir(idp_dir)
        
        # extract and save the response variables for the test set
        y_te = df_te[idp].to_numpy()
        
        # print("sys path: ",sys.path)
        # print("os path: ", os.getcwd())
        
        resp_file_te = os.path.join(idp_dir, 'resp_te.txt') 
        # print("resp_file_te path: ", resp_file_te)
        np.savetxt(resp_file_te, y_te)
        # configure and save the design matrix
        cov_file_te = os.path.join(idp_dir, 'cov_bspline_te.txt')
        X_te = create_design_matrix(df_te[cols_cov], 
                                    site_ids = df_te['site'],
                                    all_sites = site_ids_tr,
                                    basis = 'bspline', 
                                    xmin = xmin, 
                                    xmax = xmax)
        np.savetxt(cov_file_te, X_te)
        
        # check whether all sites in the test set are represented in the training set
        if all(elem in site_ids_tr for elem in site_ids_te):        
            # just make predictions
            yhat_te, s2_te, Z = predict(cov_file_te, 
                                        alg='blr', 
                                        respfile=resp_file_te, 
                                        model_path=os.path.join(idp_dir,'Models'))
        else:        
            # save the covariates for the adaptation data
            X_ad = create_design_matrix(df_ad[cols_cov], 
                                        site_ids = df_ad['site'],
                                        all_sites = site_ids_tr,
                                        basis = 'bspline', 
                                        xmin = xmin, 
                                        xmax = xmax)
            cov_file_ad = os.path.join(idp_dir, 'cov_bspline_ad.txt')          
            np.savetxt(cov_file_ad, X_ad)
            
            # save the responses for the adaptation data
            resp_file_ad = os.path.join(idp_dir, 'resp_ad.txt') 
            y_ad = df_ad[idp].to_numpy()
            np.savetxt(resp_file_ad, y_ad)
        
            # save the site ids for the adaptation data
            sitenum_file_ad = os.path.join(idp_dir, 'sitenum_ad.txt') 
            site_num_ad = df_ad['sitenum'].to_numpy(dtype=int)
            np.savetxt(sitenum_file_ad, site_num_ad)
            
            # save the site ids for the test data 
            sitenum_file_te = os.path.join(idp_dir, 'sitenum_te.txt')
            site_num_te = df_te['sitenum'].to_numpy(dtype=int)
            np.savetxt(sitenum_file_te, site_num_te)
            
            yhat_te, s2_te, Z = predict(cov_file_te, 
                                        alg = 'blr', 
                                        respfile = resp_file_te, 
                                        model_path = os.path.join(idp_dir,'Models'),
                                        adaptrespfile = resp_file_ad,
                                        adaptcovfile = cov_file_ad,
                                        adaptvargroupfile = sitenum_file_ad,
                                        testvargroupfile = sitenum_file_te)
            
    return Z


