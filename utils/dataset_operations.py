import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from random import randint
from pickle import dump,load
from os import listdir
from time import time
from scipy.stats import pearsonr

def evaluate_execution_time(file_name,function):
    if function  == "list":
        initial_time = time()
        get_dataset_itens(file_name)
        final_time =  time()
    else:
        initial_time = time()
        load_dataset_to_dataframe(file_name)
        final_time =  time() 
    return final_time - initial_time

def load_dataset_to_dataframe(file_name):
    header_length = get_header_length(file_name)
    dataset = pd.read_csv(file_name,low_memory=False)
    return dataset

def get_header(file_name):
    with open(file_name,"r") as dataset:
        header = dataset.readline().split(',')
    return header

def get_header_length(file_name):
    return len(get_header(file_name))


def get_dataset_itens(file_name):
    dataset_identifiers = []
    dataset_features = []
    dataset_labels = []
    with open(file_name,"r") as dataset:
        header = dataset.readline()
        for line in dataset:
            line_list = line.split(',')
            dataset_identifiers.append(line_list[:8])
            dataset_features.append(line_list[8:-1])
            dataset_labels.append(line_list[-1])
    return [dataset_identifiers,dataset_features,dataset_labels]


def load_all_dataset_csvs_to_dataframe(path):
    names = []
    files = listdir(path)
    for name in files:
        names.append(path+name) 
    dataset_identifiers, dataset_features, dataset_labels = load_dataset_to_dataframe(names[0])
    for file_name in names[1:]:
        new_dataset_identifiers, new_dataset_features, new_dataset_labels = load_dataset_to_dataframe(file_name)
        dataset_identifiers = pd.concat([dataset_identifiers,new_dataset_identifiers])
        dataset_features = pd.concat([dataset_features,new_dataset_features])
        dataset_labels = pd.concat([dataset_labels,new_dataset_labels])
    return dataset_identifiers,dataset_features,dataset_labels
     

def load_all_dataset_csvs_to_list(path):
    names = []
    files = listdir(path)
    dataset = [[],[],[]]
    for name in files:
        names.append(path+name)
    for file_name in names:
        data = get_dataset_itens(file_name)
        dataset = [dataset[0]+data[0],dataset[1]+data[1],dataset[2]+data[2]] 

def verify_nan_features(dfDataset):
    print('Number of missing features: ', dfDataset.isna().sum().sum(),'\n\n')
    for column_name in dfDataset.keys():
        if dfDataset[column_name].isna().sum():
            print('Number of missing features in column %s:' % str(column_name), dfDataset[column_name].isna().sum())

def binarize_label_dataframe(labels):
    return labels.apply(lambda label: 1 if (label.item() == "BENIGN") else -1, axis=1)
    
def multiclass_label_dataframe(labels):
    labels_dictionary = get_dataframe_labels_dictionary(labels)
    return labels.apply(lambda label: labels_dictionary[label.item()], axis=1)

def get_dataframe_labels_dictionary(dataframe):
    unique_labels =  list(dataframe[" Label"].unique())
    labels_dictionary = {}
    for label,name in enumerate(unique_labels):
        labels_dictionary[name] = label
    return labels_dictionary


def get_binary_labels_list(labels):
    binary_labels = []
    for item in labels:
        if item == "BENIGN\n":
            binary_labels.append(-1)
        else:
            binary_labels.append(1)
    return binary_labels

def get_labels_dictionary(labels):
    unique_labels = list(set(labels))
    labels_dictionary = {}
    for label,name in enumerate(unique_labels):
        labels_dictionary[name] = label 
    return labels_dictionary

def get_multiclass_labels(labels):
    multiclass_labels = []
    labels_dictionary = get_labels_dictionary(labels)
    for item in labels:
        multiclass_labels.append(labels_dictionary[item])
    return multiclass_labels


def write_obj(dataset,file_name):
    with open(file_name,"wb") as dataset_file:
        dump(dataset,dataset_file)

def read_obj(file_name):
    with open(file_name,'rb') as dataset_file:
        dataset = load(dataset_file)
    return dataset

def append_text(file_name,text):
    with open(file_name,'a') as writer:
        writer.writelines(text)

def print_column_names(file_name):
    with open(file_name,"r") as dataset:
        names = dataset.readline()
    names_list = names.split(',')
    for item in names_list:
        print(item)

def get_classes_statistic(file_name,column_name="class"):
    dataset = load_dataset_to_dataframe(file_name)
    
    print(dataset[column_name].value_counts())


# Receives the label and returns all samples with this label
def get_subset_by_labels(features, labels, label):
    y_subset = labels[labels['class_'+str(label)] == 1]
    X_subset = features[features.index.isin(y_subset.index)]
    return X_subset, y_subset

def divide_samples_by_class(DATASET_PATH):
    # Load data
    X = read_obj(DATASET_PATH+"/pre_processed/features")
    y = read_obj(DATASET_PATH+"/pre_processed/labels")
    
    for index in range(20):
        X_subset, y_subset = get_subset_by_labels(X, y, index)
        write_obj(y_subset,DATASET_PATH+"/divided_by_class/labels_class_"+str(index))
        write_obj(X_subset,DATASET_PATH+"/divided_by_class/features_class_"+str(index))

def prob_to_class(prob_df):
    class_y = []
    prob_df[np.isnan(prob_df)] = 0
    for index in range(len(prob_df)):
        class_y.append(list(prob_df[index]).index(max(prob_df[index])))
    return class_y

def remove_high_correlation_features(corr_matrix,features):
    high_correlation_columns = {}
    for column_name in corr_matrix.keys():
        for index in range(len(corr_matrix[column_name])):
            if (corr_matrix[column_name][index] >= 0.8) and (corr_matrix.index[index] != column_name):
                if corr_matrix.index[index] in high_correlation_columns.keys():
                    high_correlation_columns[corr_matrix.index[index]].append(str(column_name))
                else:
                    high_correlation_columns[corr_matrix.index[index]] = [str(column_name)]
    
    # separe the features 
    features_to_not_delete = []
    features_to_delete = []

    # sort features according to the number of correlated features
    for key in sorted(high_correlation_columns, key=lambda key: len(high_correlation_columns[key]), reverse=True):
        if key not in features_to_delete:
            features_to_not_delete.append(key)
            for item in high_correlation_columns[key]:
                if item not in features_to_delete:
                    features_to_delete.append(item)
    
    # delete the features
    for name in features_to_delete:
        corr_matrix.drop(name, axis='columns', inplace=True)
        corr_matrix.drop(name, axis='index', inplace=True)
        features.drop(name, axis='columns', inplace=True)



def remove_nan_features_corr(data,corr_matrix,num_features=30):
    columns_to_delete = []
    for column_name in corr_matrix.keys():
        if corr_matrix[column_name].isna().sum() == num_features:
            columns_to_delete.append(str(column_name))

    for name in columns_to_delete:
        corr_matrix.drop(name, axis='columns', inplace=True)
        corr_matrix.drop(name, axis='index', inplace=True)
        data.drop(name, axis='columns', inplace=True)
  
    return columns_to_delete
