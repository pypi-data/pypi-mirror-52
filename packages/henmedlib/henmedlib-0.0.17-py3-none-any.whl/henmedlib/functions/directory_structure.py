__author__ = "Henning Schmitz"

import os
from henmedlib.i_o.dicom import read_dicom_tags

def get_list_of_files(dir_name):
    """
    Creates a list of files within subdirectory of given path.
    :param dir_name: Path to the main directory.
    :return: List containing names of files.
    """

    list_of_files = os.listdir(dir_name)

    all_files = []

    for entry in list_of_files:
            path = os.path.join(dir_name,entry)
            # if entry is a directory then get the list of files in the directory
            if os.path.isdir(path):
                all_files += get_list_of_files(path)
            else:
                all_files.append(path)

    return all_files

def order_dicom_into_folders(path):
    """
    Given a path with unsorted dicom files, this function creates folders from 0-9 and sorts the .dcm files accordingly.
    :param path: path to .dcm files
    :return: 10 subfolders with sorted dicom files
    """
    # create subfolders
    try:
        os.mkdir(path + '0/')
    except:
        pass
    try:
        os.mkdir(path + '1/')
    except:
        pass
    try:
        os.mkdir(path + '2/')
    except:
        pass
    try:
        os.mkdir(path + '3/')
    except:
        pass
    try:
        os.mkdir(path + '4/')
    except:
        pass
    try:
        os.mkdir(path + '5/')
    except:
        pass
    try:
        os.mkdir(path + '6/')
    except:
        pass
    try:
        os.mkdir(path + '7/')
    except:
        pass
    try:
        os.mkdir(path + '8/')
    except:
        pass
    try:
        os.mkdir(path + '9/')
    except:
        pass

    # order files accordingly to the subfolders
    for filename in os.listdir(path):
        if filename.endswith('.dcm'):
            # print('Open file', filename)
            dataset = read_dicom_tags(path + filename)
            # print(dataset.SeriesDescription)
            if ' 0%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '0/' + filename)
            if '10%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '1/' + filename)
            if '20%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '2/' + filename)
            if '30%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '3/' + filename)
            if '40%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '4/' + filename)
            if '50%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '5/' + filename)
            if '60%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '6/' + filename)
            if '70%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '7/' + filename)
            if '80%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '8/' + filename)
            if '90%' in dataset.SeriesDescription:
                os.rename(path + filename, path + '9/' + filename)
            else:
                pass
