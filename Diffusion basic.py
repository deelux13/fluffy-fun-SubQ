"""Important and currently basic update module.

Created on Mon Sep  7 12:37:08 2020

@author: Glen
"""

import numpy as np
import matplotlib.pyplot as plt


def laplaciantransform_fordiffusionrate(mat):
    """
    Find the difference in concentration.

    Compares cells to each surrounding cell
    Does the entire matrix at the same time using np.roll()
    to subract it. This is a "traditional" Laplacian transform.


    Parameters
    ----------
    mat : array
        Holds concentration information for the laplacian transform to delta(C)
    dimensions : int
        How many dimensions we are monitoring the diffusion on, should
        match mat.

    Returns
    -------
    lapmatcentral : array
        Just tells the average delta(C) for each cell.

    Notes
    -----
    This can take up to 3 dimensions
    """
    # number of neightbors
    dimensions = mat.ndim
    neighnum = dimensions*2

    # central point weight for difference formula
    lapcentral = neighnum*-1

    # central laplacian matrix
    lapmatcentral = lapcentral * mat

    neighborAddress = [(1, 0), (-1, 0), (1, 1), (-1, 1), (1, 2), (-1, 2)]

    for neigh, axis in neighborAddress[0:neighnum]:
        lapmatcentral += np.roll(mat, neigh, axis)

    print("diffmat ", lapmatcentral)
    return lapmatcentral


def update(A, DA, dimensions, delta_t):
    """
    Do the time-update, currently just diffusion.

    Parameters
    ----------
    A : TYPE
        DESCRIPTION.
    DA : TYPE
        DESCRIPTION.
    dimensions : TYPE
        DESCRIPTION.
    delta_t : number
        Simply is the scale factor/.

    Returns
    -------
    A : TYPE
        DESCRIPTION.

    """
    # compute the diffusion part of the update
    diff_A = DA * laplaciantransform_fordiffusionrate(A, dimensions)

    # adjust based on the change in concentration
    A += diff_A * delta_t

    # TODO this will need calculations later I think.
    # BUT we will need to have more than just one component to update.

    return A


def pad_edges_withduplicate(mat):
    """
    Adding to the edges so there isn't any periodicity.

    Parameters
    ----------
    mat : Array
        Input to be padded.

    Returns
    -------
    paddedmat : Array
        Padded array with theouter row being a copy of the previous outer row.

    """
    dimensions = mat.ndim
    toadd = (2, 2, 2)
    startsize = mat.shape
    small_zero_mat = np.zeros(startsize)
    paddedsize = startsize + toadd[0:dimensions]
    # TODO need to finish this
    # also need to add comments
    # aldo should fix up the earlier one.

    # this is only the 2D case :(
    # i can make those inputs myself and take off the end if it isn't 3D
    paddedmat = np.zeros(paddedsize)
    paddedmat[0:startsize[0],0:startsize[1]] = mat
    # would it be better to roll?
    paddedmat[1:startsize[0] + 1,1:startsize[1] + 1] = mat


#
#
"""----Just keeping it organized---"""
DA = .3

rect = np.zeros((66))
rect[12:25] = .5
rect[14:20] = 1
plt.plot(rect, 'o')
print(" 1 ", rect)
i = 0
while i < 9000:
    rect = update(rect, DA, 1, .01)
    # plt.plot(rect, 'o')
    i += 1

print("2 ", rect)
rect = update(rect, DA, 1, .01)
print("3 ", rect)
plt.plot(rect, 'o')
