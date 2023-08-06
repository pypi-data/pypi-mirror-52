__author__ = "Henning Schmitz"

import pydicom

def read_dicom_tags(path):
    """
    Given a path containing dicom files the corresponding dataset (python type class) is returned.
    :param path: String values that represents the path to the .dcm file
    :return: class corresponding to .dcm file
    """
    dataset = pydicom.dcmread(path)

    return dataset

def write_dicom(dataset, path):
    """
    Given a class and path as input a .dcm file is created
    :param path: class containing dicom image attributes
    :return: .dcm file
    """
    dataset.save_as(path)
