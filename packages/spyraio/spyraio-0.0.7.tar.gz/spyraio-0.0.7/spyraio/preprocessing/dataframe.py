# -*- coding: utf-8 -*-
"""Preprocessing functions.
"""
import os
import pandas as pd


def load_dataset(path, files):
    """Load dataframe.
    
    # Arguments
        `path`: a string containing the file directory.
        `files`: a list containing one or more file names.
    # Returns
        Return a concatenated dataframe from files.
    """
    
    dfs = [pd.read_csv(os.path.join(path, file)) for file in files]
    df = pd.concat(dfs, sort=False)
    
    return df


def filter_dataframe(df, filters):
    """Filter data frame.
    
    # Arguments
        `df`: a pandas dataframe.
        `filters`: a list containing the filters to apply to data frame.
    # Returns
        Return a filtered data frame.
    """
    
    df = df.query(filters)
    
    return df
    

def set_threshold(df=None, filters=[], samples=1):
    """Apply threshold to dataframe and merge.
    
    # Arguments
        `df`: a pandas dataframe.
        `filters`: a list containing the filters of threshold to apply to data 
        frame.
        `samples`: a percentage to the smallest filtered data frame.
    # Returns
        Return a single data frame with threshold.
    """
    
    dfs = []
    sizes = []
    for filter_ in filters:
        df = df.query(filter_)
        sizes.append(df.shape[0])
        dfs.append(df)
    
    samples *= 100
    samples = int((min(sizes)*samples)/100)
    
    dfs = [df.sample(samples) for df in dfs]
    
    df = pd.concat(dfs, sort=False).sample(samples*len(filters))
    
    return df
    
    
if __name__ == "__main__":
    df = load_dataset('./data/private', ['august.csv'])
    print(df)
    