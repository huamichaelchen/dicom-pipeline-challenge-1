import csv
import errno
import glob
import itertools
import logging
import numpy as np
import os

from pydicom.errors import InvalidDicomError
from . import parsing, utils

logging.basicConfig(
    filename="dicom_parser.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

class DicomContourParser():


    def __init__(self, output_data_dir, dicom_dir, contour_dir, links_file,
                contours_type='i-contours,o-contours'):
        '''
        Create a DicomContour Extractor
        Parameters
        ----------
        dicom_dir: string
            Input raw dicom directory
        contour_dir: string
            Input raw contourfiles directory
        links_file: string
            A CSV file that contains dicom and contour mapping
        contour_type: string
            Types of contour(s), in this case we only have inner-contour and outer-contour
        '''

        self.output_data_dir = output_data_dir
        self.dicom_dir = dicom_dir
        self.contour_dir = contour_dir
        self.links_file = links_file
        self.contours_type = contours_type

        self.parse_outfile_headers = ['image']
        self.parse_outfile_headers.extend(self.contours_type.split(','))

    def get_dicom_contour_file_paths(self):
        '''
        A generator that finds the matching dicom and contour(s)
        '''
        with open(self.links_file, 'r') as links_file:
            reader = csv.DictReader(links_file, fieldnames=['patient_id', 'original_id'])
            next(reader)
            for current in reader:
                dicom_dir = os.path.join(self.dicom_dir, current['patient_id'])
                dicom_filenames = os.listdir(dicom_dir)
                dicom_file_set = set([ int(name.split('.')[0]) for name in dicom_filenames])
                
                contour_dirs = []
                contour_file_sets = []
                for contour_type in self.contours_type.split(','):
                    contour_dir = os.path.join(self.contour_dir, current['original_id'], contour_type)
                    contour_dirs.append(contour_dir)
                    contour_filenames = os.listdir(contour_dir)
                    contour_file_set = set([int(name.split('-')[2]) for name in contour_filenames ])
                    contour_file_sets.append(contour_file_set)
                
                valid_dicom_indices = set.intersection(dicom_file_set, *contour_file_sets)
                if len(valid_dicom_indices) == 0: continue

                for valid_dicom_index in valid_dicom_indices:
                    valid_dicom_path = glob.glob(os.path.join(dicom_dir, '{}.dcm'.format(valid_dicom_index)))[0]
                    valid_contour_paths = []
                    contour_file_regex = '*{:04d}*'.format(valid_dicom_index)
                    for contour_dir in contour_dirs:
                        valid_contour_path = glob.glob(os.path.join(contour_dir, contour_file_regex))[0]
                        valid_contour_paths.append(valid_contour_path)

                    yield valid_dicom_path, valid_contour_path

    def extract(self):
        '''
        Extract dicoms and contours files.
        '''
        dicom_output_dir = self.output_data_dir+"dicom"
        contour_output_dir = self.output_data_dir+"contours"

        utils.mkdir_p(dicom_output_dir)
        utils.mkdir_p(contour_output_dir)
        
        logging.info('===> Starting extracting dicom and contours files.')
        outfile = open('{}output.csv'.format(self.output_data_dir), 'w')
        header_line = ' '.join(self.parse_outfile_headers)
        outfile.write('{}\n'.format(header_line))

        dcm_contours_paths = list(self.get_dicom_contour_file_paths())
        for i, (dcm_path, contour_paths) in enumerate(dcm_contours_paths):
            try:
                dicom = parsing.parse_dicom_file(dcm_path)
                contours, masks = [], []
                contour = parsing.parse_contour_file(contour_paths)
                mask = parsing.poly_to_mask(contour, dicom['pixel_data'].shape[0], dicom['pixel_data'].shape[1])
                contours.append(contour)
                masks.append(mask)
            except InvalidDicomError:
                logging.error('Error loading dicom file: {}'.format(dcm_path), exc_info=True)
            except Exception:
                logging.error('===> Unspecified errors....', exc_info=True)
            else:
                sample_line = []

                img_path = os.path.join(self.output_data_dir+"dicom", '{}.npy'.format(i))
                sample_line.append(img_path)
                np.save(img_path, dicom)

                for contour_type, mask in zip(self.contours_type.split(','), masks):
                    mask_path = os.path.join(self.output_data_dir+"contours", '{}.{}.npy'.format(i, contour_type))
                    sample_line.append(mask_path)
                    np.save(mask_path, mask)

                sample_line = ' '.join(sample_line)
                outfile.write('{}\n'.format(sample_line))

        outfile.close()
        logging.info('===> Finshed.')