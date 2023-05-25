Welcome! This is the ProductFinder - Warehouse Navigation Application program by CoGPT!

Table of Contents:
--Overview
--Requirements
--Installation

##Overview
This Beta version has all the basic features available, such as：
	1)display the overall map with shelf location;
	2)reading product location data from a file;
	3)basic setting options;
	4)asking the user to input the location of the products he/she wants to pick up; 
	5)generating a recommended route and printing it out. 
	6)worker location manual setup.
New features in Beta version:
	1) allow using 2 algo(Branch&Bound or tspDp) to get multiple orders
    	2) introduce multiprocessing to monitor and handle a stack situation
    	3) allow allocating product coordinates by ProductID
    	4) add test function to run multiple test cases at once

##Requirements
This program will use package tqdm. If this is not installed on your working envirement, you may open the command line terminal and use "pip install tqdm" command to install.

##Installation:
Go to https://github.com/BruceWang3077/EECS216 and download the source code. Our Alpha version is in ProductFinder folder.
To run the program, you may:
	1)open ProductFinder directory in Pycharm, VScode or any other IDE and run the main.py.
	2)open the command line terminal from the directory, and use the command "python main.py" to run the program



