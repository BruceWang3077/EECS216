Welcome! This is the ProductFinder - Warehouse Navigation Application program by CoGPT!

Table of Contents:
--Overview
--Requirements
--Installation

## Overview
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
    5) add results export
    6) add memory usage/runtime comparison

## Requirements
This program will use package memory-profiler. If this is not installed on your working envirement, you may open the command line terminal and use "pip install memory-profiler" command to install.

## Installation:
Go to https://github.com/BruceWang3077/EECS216 and download the source code. Our Alpha version is in ProductFinder folder.
To run the program, you may:
	1)open ProductFinder directory in Pycharm, VScode or any other IDE and run the main.py.
	2)open the command line terminal from the directory, and use the command "python main.py" to run the program

## Get start
After running the program, you will see the following interface:
```bash
Welcome to the ProductFinder!
1) go get product!
2) settings
3) run tests
4) exit
```
before running tests, you should set up the settings first.
```bash
1) set rotation
2) set algorithm option
3) set MapSize
4) set worker
5) set shelves
6) set countDown
```
specifically, you should set shelves before running tests.
```bash
please choose(1~8): 5
please input file path:qvBox-warehouse-data-s23-v01.txt
```
then you can run tests or get any products you want.

