import argparse
import pydicom

from dicom_extractor import parsing, dicom_contour_extractor

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-data-dir', type=str, default='./output/', help='Output directory')
    parser.add_argument('--dicom_dir', type=str, default='./final_data/dicoms', help='')
    parser.add_argument('--contour_dir', type=str, default='./final_data/contourfiles', help='')
    parser.add_argument('--links_file', type=str, default='./final_data/link.csv', help='')
    parser.parse_args()

    return parser.parse_args()

def main(args):
    dicom_contour_parser = dicom_contour_extractor.DicomContourParser(
        output_data_dir = args.output_data_dir,
        dicom_dir = args.dicom_dir,
        contour_dir = args.contour_dir,
        links_file = args.links_file
    )
    dicom_contour_parser.extract()

if __name__ == "__main__":
    args = parse_args()
    main(args)