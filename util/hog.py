import numpy as np
from scipy import misc
from scipy import sqrt, pi, arctan2, cos, sin
from scipy.ndimage import uniform_filter

def hog(image, orientations=9, pixels_per_cell=(9,9), cells_per_block=(2,2), normalise=True):
    if not isinstance(image, np.ndarray):
        image = misc.imread(image)
    image = np.atleast_2d(image)
    if image.ndim >= 3:
        image = np.mean(image, 2)
    if normalise: # gamma
        image = sqrt(image)
    if image.dtype.kind == 'u':
        image = image.astype('float')

    gx = np.zeros(image.shape)
    gy = np.zeros(image.shape)
    gx[:, 1:-1] = np.diff(image, n=2, axis=1)
    gy[1:-1, :] = np.diff(image, n=2, axis=0)

    magnitude = sqrt(gx**2 + gy**2)
    orientation = arctan2(gy, (gx + 1e-15)) * (180 / pi) % 180 

    sy, sx = image.shape
    cx, cy = pixels_per_cell
    bx, by = cells_per_block

    n_cellsx = int(np.floor(sx // cy))
    n_cellsy = int(np.floor(sy // cy))

    orientation_histogram = np.zeros((n_cellsy, n_cellsx, orientations))
    subsample = np.index_exp[cy/2:cy*n_cellsy:cy, cx/2:cx*n_cellsx:cx]
    for i in range(orientations):
        temp_ori = np.where(orientation < 180 / orientations * (i+1), orientation, -1)
        temp_ori = np.where(orientation >= 180 / orientations * i, temp_ori, -1)
        cond2 = temp_ori > -1
        temp_mag = np.where(cond2, magnitude, 0)

        temp_filt = uniform_filter(temp_mag, size=(cy, cx))
        orientation_histogram[:,:,i] = temp_filt[subsample]
    
    n_blocksx = (n_cellsx - bx) + 1
    n_blocksy = (n_cellsy - by) + 1
    normalised_blocks = np.zeros((n_blocksy, n_blocksx, by*bx*orientations))

    for x in range(n_blocksx):
        for y in range(n_blocksy):
            block = orientation_histogram[y:y+by, x:x+bx, :]
            eps = 1e-5
            block = block / sqrt(block.sum() ** 2 + eps)
            normalised_blocks[y, x, :] = block.ravel()
    return normalised_blocks


