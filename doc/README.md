In order to start with Scribe...
=======
Myeong Lee (iSchool, UMD)
-------

## Tools/Technology that Are Needed to Work on this Platform.
- Github
- Ubuntu Trusty (14.04)
- Vagrant (for local environment setup)
- Ansible (for local environment setup)
- Ruby on Rails
- React.js (if you want to make changes in the interfaces)
- MongoDB
- AWS EC2 (for the real server)


## General Approach/Workflow (Details for each step are in separate files)
1. Create a project on your local PC (inside the Scribe's project folder `html/project/`). 
2. Create files that are required for the target city using Python scripts (These files are generated from Python scripts that are avaialble at [https://github.com/UMD-DCIC/Scribe/tree/master/scripts/csv_generator](https://github.com/UMD-DCIC/Scribe/tree/master/scripts/csv_generator))
3. Upload them to the server using Git.
4. Load the project in the Ruby of Rails framework.
5. Start the server.
6. Mark one page of the city manually and save the marking data as a csv file.
7. Use the Bot user to replicate the csv file's data onto other documents. 
8. Then, the city is set up. For the details for setting up the server: see [Setup City](setup_city.md). 
9. Once the transcription and verification are done, you need to export the data as a JSON file. SSH to the server and export the MongoDB by typing:
```
rake project:build_and_export_final_data
```
Once the JSON file is exported, download it to your local PC using the `scp` command. 

If this `rake` command doesn't work or you face errors, see [this document](https://github.com/UMD-DCIC/Scribe/blob/master/doc/export_data.md).


## Original Scribe Manual (Developer's)
[https://github.com/zooniverse/scribeAPI/wiki](https://github.com/zooniverse/scribeAPI/wiki)


## Installing MongoDB on Ubuntu 16.04
https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04


## Python Scripts that process the output of the MongoDB
These scripts are available at `scripts` folder of this Github repo:
[https://github.com/UMD-DCIC/Scribe/tree/master/scripts](https://github.com/UMD-DCIC/Scribe/tree/master/scripts)