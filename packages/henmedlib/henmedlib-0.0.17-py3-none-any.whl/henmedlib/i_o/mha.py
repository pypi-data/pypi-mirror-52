__author__ = "Henning Schmitz"

import SimpleITK as sitk

def read_mha(path):
    """
    Given a path the function reads the image and returns header as well as the intensity values into a 3d array.
    :param path: String value that represents the path to the .mha file
    :return: image executable and 3D array filled with intensity values
    """
    reader = sitk.ImageFileReader()
    reader.SetFileName(path)
    image = reader.Execute()
    image_array = sitk.GetArrayFromImage(image)

    return image, image_array

def write_mha(image, image_array, path):
    """
    Given a 3d array and header the function saves a .mha file at the requested path.
    :param image: Executable of image
    :param image_array: 3d array filled with intensity values corresponding to a .mha file
    :param path: String value that represents the path to the created .mha file
    :return: Image file corresponding to the input
    """
    writer = sitk.ImageFileWriter()
    writer.SetFileName(path)

    newimage=sitk.GetImageFromArray(image_array)

    # Get header
    newimage.SetOrigin(image.GetOrigin())
    newimage.SetSpacing(image.GetSpacing())

    writer.Execute(newimage)