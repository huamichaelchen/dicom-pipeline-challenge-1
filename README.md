# Goals

Prepare DICOM MRI images and contour files to prepare them for training a convolutional neural network. 

The inputs to the network will be dicom images and the targets will be the contours encoded as boolean masks (foreground pixels = True; background pixels = False)

## Getting Started:

#### Option 1: (only for DEV env)
1. `./run-jupyter-lab.sh` to launch jupyter-lab
2. `docker logs theContainerJustLaunched` to find the jupyterlab URL
3. run the first cell in `exploratory.ipynb` to install the necessary library
4. open up a terminal and navigate to `work` directory. 
5. `python main.py`

#### Option 2:
0. `conda create -n temp python=3.7` (optional)
1. `pip install -r requirements.txt`
2. `python main.py`


### Part 1: Parse the DICOM images and Contour Files
Using the functions given above, build a pipeline that will parse the DICOM images and i-contour contour files, ***making sure to pair the correct DICOM image(s) with the correct contour file.*** After parsing each i-contour file, make sure to ***translate the parsed contour to a boolean mask.***


#### Answer the following questions: 

1. How did you verify that you are parsing the contours correctly?
First, I need to find and make sure I have matching dicom & contours. Function `get_dicom_contour_file_paths()` is used for that. I didn't implement this, but one thing I could think of is that I could create correct and false stub data to see how my module behave. Another thing, I could do is loading the extracted data in `.npy` format and compare it with the original `dicom['pixel_data']` and see if they are the same.
 


2. What changes did you make to the code, if any, in order to integrate it into our production code base? 
Didn't make any changes to `parsing.py`. Just used it as helper methods in the module added. The logic behind making these scripts as modules is because this should be easily imported into the existing production code base or being deployed separately and running as a small ETL service. 


### Part 2: Model training pipeline

Using the saved information from the DICOM images and contour files, add an additional step to the pipeline that will **load batches of data for input into a 2D deep learning model**. This pipeline should meet the following criteria:

* Cycles over the entire dataset, loading a single batch (e.g. 8 observations) of inputs (DICOM image data) and targets (boolean masks) at each training step.
* A single batch of data consists of one numpy array for images and one numpy array for targets.
* Within each epoch (e.g. iteration over all studies once), samples from a batch should be loaded randomly from the entire dataset. 

#### Answer the following questions:

1. Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
No, I didn't change anything from the pipelines built in part 1. I was experimenting with PyTorch [Dataset and DataLoader](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html). 


2. How do you/did you verify that the pipeline was working correctly?

Sorry, unfortunately I couldn't finish this part, but it seems that PyTorch Custom Datasets and DataLoaders seems to be a good option.


3. Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

Unfortunately, I coudln't finish it at a production ready level in my opinion. That's been said, I've done quite some research of how other people having been trying to tackle medical imaging datasets, specifically dicom. 

I will just highlight one of them here, [sparktk dicom](https://github.com/trustedanalytics/spark-tk). In a nutshell, this libaray allows one to utilize pyspark to do ETL as well as ML works on various data source, including dicom. 

A few other thoughts I'm having:
1. Utilizing workflow tools, such as, Airflow or Kubeflow to easily automate this process.
2. Utilizing [Google Cloud HealthCare API](https://cloud.google.com/blog/topics/healthcare-life-sciences/getting-to-know-the-google-cloud-healthcare-api-part-3) https://cloud.google.com/healthcare/
3. Also, [SimpleITK](https://github.com/SimpleITK/SimpleITK) is good library too

------------------------------

### Rubric
* Well-organized, easily-understandable, documented (and self-documenting) code
* Appropriate comments where the code may be difficult to understand
* Object oriented programming where appropriate
* Unit tests if appropriate
* Use of standard library functions and open source code as much as possible. If some functionality is already available in open source code, you should use it and not waste your time duplicating effort. But if you are
using open source code, make sure you understand it and can defend the design decisions.

------------------------------
# Context

*Definitions*

*i-contour*:
    inner contour that separates the left ventricular blood pool from the heart muscle (myocardium)

*o-contour*:
    outer contour that defines the outer border of the left ventricular heart muscle

