# -*- coding: utf-8 -*-
"""Preprocessing functions.
"""
import os
import pandas as pd


def load_dataset(path, files):
    """Load dataframe.
    
    # Arguments
        `path`: a string containing the file directory
        `files`: a list containing one or more file names
    # Returns
        Return a concatenated dataframe from files
    """
    
    dfs = pd.read_csv(os.path.join(path, file) for file in files)
    df = pd.concat(dfs, sort=False)
    
    return df
    