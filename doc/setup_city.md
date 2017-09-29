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
Since you're targetting only one city, copy `group_[city_name].csv` to the `subjects` folder inside the project folder. For example, if you're targetting Pittsburgh, you copy `group_Pittsburgh.csv` to `/html/project/pittsburgh/subjects/`. Of course, you need to delete other csv files, if any. In the `group_[city_name].csv` file, delete the line with order 0, since it usually points to the cover page of documents (if not, don't delete it. You need to check it).

`group.csv` file contains all the city data that were in the image folder. You need to delete all the cities other than the target city. In the Pittsburgh case, you just leave the following lines and delete all others.
```
key,name,description,cover_image_url,external_url,retire_count
Pittsburgh,Pittsburgh Redlining Documents,Pittsburgh Redlining Documents from Pittsburgh_Box94,http://[EC2_URL]:3000/dcic_docs/Pittsburgh_Box94/Pittsburgh_AD_001.jpg,http://ec2-52-90-254-241.compute-1.amazonaws.com:3000,2
```
Then, copy this file to the same folder: `/html/project/pittsburgh/subjects/`

## 7. Copy Document Images to the Server
Since there's no images on the server, you need to copy them over by typing the following commands:
```
scp -i [pem file path] -rp [document_folder_path] ubuntu@[EC2_URL]:/home/ubuntu/
```

For the Pittsburgh case, it looks like this:
```
scp -i [pem file path] -rp Pittsburgh_Box94 ubuntu@[EC2_URL]:/home/ubuntu/
```

Then, the entire folder that has all the images for the city is uploaded to the server.

## 8. Copy the Document Folder to the Document Root's Folder
You just copied the documents to your home directory. Actually, they need to be inside the 'html' folder for your production server. Copy them to `/var/www/html/public/dcic_docs/`. This 'public' folder is for creating static HTML pages. We're using this folder for storing images. 
```
sudo cp -R Pittsburgh_Box94 /var/www/html/public/dcic_docs/
```

## 9. Upload Project Files using Github
You have project configuration files changed on your local repo. Push them to the Git repo, and pull them on the server in the home directory.

## 10. Copy the New Project Folder to the Production Folder
Since you downloaded new files in your home directory, copy the new project folder (e.g., pittsburgh) to the Document Root's folder. For example:

```
sudo cp -R html/project/pittsburgh/ /var/www/html/project/
```

## 11. Need to Restart MongoDB
Since Scribe remembers a previous URL, you need to restart the MongoDB service.

```
sudo rm /var/lib/mongodb/mongod.lock
sudo service mongodb restart
```

## 12. Let's Test Weather the Interface Works

#### Go to the Document Root
``` 
cd /var/www/html/
```

#### Register environmental variables
```
source .env
```

#### Load the project
```
rake project:load[folder_name_of_the_project]
```

#### Run the Ruby on Rails server
```
rails s
```

#### Go to the website whether it works 
```http://[EC2_URL]:3000```

Remember -- it is running on port 3000.
For now, "transcribe" and "verify" doesn't work since you don't have mark information. You need to check by going to 
```http://[EC2_URL]:3000/#/mark```

If a target city's document shows up, it is successful so far. If successful, come back to the command line, and turn off the server by hitting `ctrl + c`.


## 13. Facebook Key Setup
Since Scribe uses Facebook for authentication, you need to register your Facebook app's key for the admin interfaces. As of September 2017, Myeong's FB key is registered for admin. It is possible to change the user privilege later in the MongoDB's user table. 

Go to your FB for Developers page, and go to your App page. In the "settings->basic" menu, you need to change the website that you're using for the app. Since you don't have a domain name for Scribe, you can type in the EC2 instance's IP address.

Also, in the "settings->advanced" menu, you need to add the EC2 IP address to the "Server IP Whitelist" field, and save it.

Lastly, go to "Facebook Login->Settings", and add OAuth redirect URLs by typing:
```
http://[EC2_IP]:3000/users/auth/facebook/callback
```
And save it.

## 14. Create Marks
We're automatically generating Masks so peopel don't have to mark every field for each document. In order to do this, you need two command line windows. Open another terminal and SSH to the server. 

In one terminal, run the app by typing `rails s`. Then, open the browser and go to the Mark page: ```http://[EC2_URL]:3000/#/mark```.
In this page, mark each field carefully. Select a marking title from the right bar, and draw a square that covers the corresponding area as big as possible. If you make a mistake while drawing squares, you need to drop the project (so to delete the DB) and start over, because everything goes to the DB. 

After finishing the marking of one page, click "Done". Click "No" for "Is there anything left to mark?", then click "Next Page". In the next page, don't mark anything. Just close the browser. 

In the other terminal (while the original terminal is running the server), go to the Document Root, `/var/www/html`, and enter to the Rails command line.
```
rails c
```

Check how many marks are there.
```
Project.current.workflows.find_by(name: 'mark').classifications.count
```

It should be same to the number of marking fields. If you made mistakes, there will be more than that. In that case, you need to drop the project and start over. If you need to drop the project, go back to the original terminal, stop the server (`ctrl + c`), and type:
```
rake project:drop[folder_name_of_the_project]
```

Then, load the project again by typing `rake project:load[folder_name_of_the_project]`, and start over the marking.

## 15. Save the Marking Data
If markings are all successful, in the Rails terminal, type the following in the correct order:
```
sudo touch project/[target_project_folder]/marks.csv

sudo chmod 777 project/[target_project_folder]/marks.csv

marks = Project.current.workflows.find_by(name: 'mark').classifications.select { |c| ! c.annotation['x'].nil? }

marks = marks.map	 { |c| [c.annotation['x'], c.annotation['y'], c.annotation['width'], c.annotation['height'], c.annotation['subToolIndex'], c.annotation['_key'], c.task_key] }

File.open('project/[target_project_folder]/marks.csv', 'w') { |file| file.write( marks.map { |c| c.join(',') }.join("\n") ) }
```
Then, exit from the Rails terminal by hitting `exit`.
If you check the project folder, you can see `marks.csv` has all Marks data in there.

## 16. Create a Bot
There is a Bot user that can generate multiple marks. Create a bot user by typing:
```
rake bot:create[MarkBot]
```

Once you do that, it shows a "HTTP_BOT_AUTH" key. Copy it and update `SCRIBE_BOT_TOKEN` in the `.env` file. Then, apply it again by typing:
```
source .env
```

## 17. Drop the Project and Load it Again
The first page shouldn't be marked twice by the bot (it was marked already once for generating the marks), so stop the server, drop the project, and load it again to clean up the DB. 
Then, run the server.
```
rake project:drop[folder_name_of_the_project]

rake project:load[folder_name_of_the_project]

rails s
```

## 18. Modify the "bot-example.rb" file inside the Project folder, and Run It
If you go to the project folder, there is `bot-example.rb`.
Use an editor such as `vi` to edit the server URL and the CSV file name in the code. The server URL is on line 118, and the CSV file name is on line 133. Save it, and run it.
```
ruby bot-example.rb
```

Then, it will start creating marks for every document. It takes some time (depending on the number of documents), so grab some coffee.

## 19. Test the Transcribe Interface
Go to the Transcribe page on your browser: 
- http://[EC2_URL]:3000/#/transcribe

If it starts letting you transcribe, it is successful. 
Turn off the server in the terminal.

## 20. Run the Server Permenantly
By using `screen` command, you can run it continuously after closing the terminal app. Also, you need to run the server in the production mode so to minimize the number of debugging outputs.
```
screen rails server -e production
```
Once it's running, close the terminal app. The website is still running. 

## 21. Check the Admin Page
You can check the status of the transcribing/verifying at:
- http://[EC2_URL]:3000/admin

Of course, your username need to be an admin account. Once you log into the admin page, you can see the progress, and users' contributions. 

If you are not an admin, go to the terminal and get into the Rails terminal.
```
rails c

# Once a user logged in, the name and email that were used on Facebook are available in the MongoDB.
User.find_by(email: "[user_email_to_be_admin]")

# If this user is available, change the role to "admin"
User.find_by(email: "[user_email_to_be_admin]").update(role: "admin")
```

Then, the target user can see the admin page after logging into the website.

## 22. Turning Off the Scribe Platform
If something goes wrong or transcription/verification work is done, you need to turn it off after exporting the data. First, you need to find the PID for the Ruby on Rails instance. In the command line of the EC2 server,
```
lsof -wni tcp:3000
```
This shows PIDs that run on the port 3000. Kill the process.
```
kill -9 [PID]
```






