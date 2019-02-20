# scicharpy

Scientific instrument control for measurement and analysis using python and PyQt, primarily developed for transistor and biosensor characterization
Documentation will be added soon.

## Installation:

Note: Using virtual environment is highly recommended. Conda and such scientific environments with popular packages such as numpy, matplotlib etc are required. For GUI pyqt is used. For live data plotting pyqtgraph is used. Easy way to install all that is required is by running following inside a virtualenv.

`pip insatall -r req.txt`

Please note that some unnecessary packages might be installed. You may manually tweek the req.txt file to suit the package requirements.

# Customizing the GUI.

We have used non commercial version of qtDesigner please open the single .ui file located at
./UI/main.ui. This will give a general idea of the UI organisation. There are two main parts to the GUI. The left section is for documentation puropose and the right side is for running the experiments with the given parameters.
You may add/delete the tabs as per your desire. The main purpose of GUI is to simply pass the parameters from user to underlying scripts.

# General flow of the measurement process.

Once the user inputs the parameters, appropriate charactrizationType class is constructed using Characterization object called from main.py. This class passes the parameters from GUI to the next step.

TransistorCharacterizationTasks constructs the appropriate characterizationtask and passes it the required instrument. This is the place where you may try to use fake instrument to test the system.

After this two threads are construced one for data collection and other for plotting purpose.
Depending upon the user interaction the measurement can be terminated at any point. As soon as the measurement process is terminated, dataprocessing kicks in and prepares the image from the data collected.
Different datalogging strategies can be adopted, we have used some time batch data saving and on other ocassions to save data only when measurement is completed successfully. You may choose whatever suits your needs.

# Issues/ pull requests.

Though this measurement system is used extensively by our group, issues might still exist and we fix them as they are found. Since our main focus is to perform measurements without putting excessive time to make the software perfect. However in case you encounter any issue or would like our help to setup the python based measurement system please raise issue in the github issue section. Also any pull requests making the system more robust and extensible are more than welcome.

finally .. keep measuring !!
