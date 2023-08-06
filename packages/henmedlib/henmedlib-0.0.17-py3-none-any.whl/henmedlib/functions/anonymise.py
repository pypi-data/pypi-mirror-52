__author__ = "Henning Schmitz"

def anonymise_dicom (dataset):
    """
    Given a class containing the attributes of the dicom file, the following attributes are deleted to ensure anonymity:
    'PatientAge', 'PatientBirthDate', 'PatientName' and 'PatientSex'

    :param dataset: class containing all of the dicom attributes
    :return: class with reduced number of attributes (anonymised)
    """
    try:
        del dataset.PatientAge
        del dataset.PatientBirthDate
        del dataset.PatientName
        del dataset.PatientSex
    except:
        print('Data is anonymised')