import matplotlib.pyplot as plt

from . import parsing

def visualize_dicom(dicom):
    '''
    Draw the given dicom image.
    Parameters
    ----------
    dicom: string
        path to the dicom image
    '''
    dicom_file = parsing.parse_dicom_file(dicom)
    plt.imshow(dicom_file['pixel_data'])

def visualize_mask_overlay(dicom, mask, savepath):
    '''
    Draw the given dicom image and the given mask, then save to disk
    Parameters
    ----------
    dicom: string
        path to the dicom image
    mask: numpy array
    savepath: string
        path to be saved on disk
    '''
    visualize_dicom(dicom)
    plt.imshow(mask, alpha=0.5)
    plt.savefig(savepath)

def visualize_contour_overlay(dicom, contour, savepath):
    '''
    Draw the given dicom image and the given contour, then save to disk
    Parameters
    ----------
    dicom: string
        path to the dicom image
    contour: numpy array
    savepath: string
        path to be saved on disk
    '''
    visualize_dicom(dicom)
    x = [point[0] for point in contour]
    y = [point[1] for point in contour]
    plt.plot(x, y, alpha=1, color='g')
    plt.savefig(savepath)