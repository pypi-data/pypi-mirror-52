__author__ = "Henning Schmitz"

import numpy as np

def calculate_hounsfield_unit(mu, mu_water, mu_air):
    """
    Given linear attenuation coefficients the function calculates the corresponding Hounsfield units.
    :param mu: Attenuation coefficient to determine corresponding Hounsfield unit.
    :param mu_water: Constant linear attenuation coefficient for water
    :param mu_air: Constant linear attenuation coefficient for air
    :return: Hounsfield unit corresponding to mu
    """

    HU = 1000 * ((mu - mu_water) / (mu_water - mu_air))

    return HU

def create_array_with_hounsfield_units(image_data, mu_water, mu_air):
    """
    Given 3d array with linear attenuation coefficients the function calculates the corresponding Hounsfield units.
    :param image_data: 3d array corresponding to image
    :param mu: Attenuation coefficient to determine corresponding Hounsfield unit.
    :param mu_water: Constant linear attenuation coefficient for water
    :param mu_air: Constant linear attenuation coefficient for air
    :return: 3d array calculated in Hounsfield unit
    """
    # print dimensions of array
    dim_x = np.size(image_data, 0)
    dim_y = np.size(image_data, 1)
    dim_slice = np.size(image_data, 2)

    # loop through array
    count = 0
    iterations = dim_x * dim_y * dim_slice
    # loop through x direction
    for i in range(0, dim_x):
        # loop through y direction
        for j in range(0, dim_y):
            # loop through slices
            for k in range(0, dim_slice):
                image_data[i][j][k] = calculate_hounsfield_unit(image_data[i][j][k], mu_water, mu_air)
                count += 1
                if count % (0.1 * iterations) == 0:
                    print(round(count / iterations, 1) * 100, "% progress")

    return image_data