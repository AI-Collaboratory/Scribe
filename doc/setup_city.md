Setting Up the Platform for a City's Documents
=========
Myeong
------------

The process to set up the Scribe platform for a city is not straightforward, and requires improvements in the pipeline. This document provides step-by-step process for setting up a city in the Mapping Inequality project. 

## 0. Prerequisites
For launching documents in the Scribe platform, you need to be able to deal with:
- Github
- Linux (Ubuntu) in the command line
- Python scripts
- Ruby on Rails
- HTML 
- AWS EC2

Also, you need to have access to the EC2 server if you want to launch the Scribe on the production server. If you want to test it out by yourself on your local PC, you additionally need to be able to deal with:
- Vagrant
- Ansible
- VirtualBox

The following instructions are for launching a new collection for a city on the EC2 server. Instructions for local testing will be provided later as a separate document.

## 1. Select a City
For now, only one type of document formats is supported in the repository (as of September 2017). There are totally four or five different formats of documents in the collection, and for each form, you need to configure possible fields and workflow files. For the details for configure a particular form and fields, see the [Scribe Wiki](https://github.com/zooniverse/scribeAPI/wiki) written by original developers from NYPL.

## 2. Create a Project Folder 
Inside the "project" folder, you need to create a project folder for the target city. For example, if you are setting documents for Pittsburgh, you can make a folder named "pittsburgh". This folder name is important for loading the project in the last step. The easist way to do this is to copy another project's folder and rename it. 

## 3. Prepare Document Files and Thumbnail Images in the JPG format
You need to download scanned documents from the UMD Box and convert them to JPG files (if needed). Also, you need to create another folder called "thumb" inside the folder, and copy the image files after resizing them to thumbnails.

## 4. Turn On the EC2 Server
Log in to the AWS console, and turn the EC2 machine on (I assume that there's already an instance that has everything set up). After using them, you need to turn it off to prevent unnecessary charges. Once it's up, copy the server URL (whenever you turn it on, the URL changes).

## 5. Generate Group Configuration Files using "scripts/scribe_csv_generator.py"
Before running the script, modify the "path" variable to the current EC2 URL. Also, if you have a specific folder that you have all the BlueText images, you need to change the paths. Then, run:
```
python scribe_csv_generator.py
```
This will generate CSV files after reading all the image files in the target folder. Particularly, the outcomes include `group_[city_name].csv` files and one `group.csv` file. 

## 6. Copy the CSV files to the Project Folder
Since you're targetting only one city, copy `group_[city_name].csv` to the `subjects` folder inside the project folder. For example, if you're targetting Pittsburgh, you copy `group_Pittsburgh.csv` to `/html/project/pittsburgh/subjects/`. Of course, you need to delete other csv files, if any.

`group.csv` file contains all the city data that were in the image folder. You need to delete all the cities other than the target city. In the Pittsburgh case, you just leave the following lines and delete all others.
```
key,name,description,cover_image_url,external_url,retire_count
Pittsburgh,Pittsburgh Redlining Documents,Pittsburgh Redlining Documents from Pittsburgh_Box94,http://[EC2_URL]:3000/dcic_docs/Pittsburgh_Box94/Pittsburgh_AD_001.jpg,http://ec2-52-90-254-241.compute-1.amazonaws.com:3000,2
```
Then, copy this file to the same folder: `/html/project/pittsburgh/subjects/`

## 7. Copy Document Images to the Server
