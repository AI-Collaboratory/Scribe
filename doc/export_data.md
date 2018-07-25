Exporting Data from the Scribe Platform (after transcriptions are done)
=========
Myeong Lee (iSchool, UMD)
------------

Once all the transcriptions and verifications are done, you are ready to export the data out of the MongoDB. If the system is stable, you can export the data with a couple of command lines. 

# Exporting the data using the `rake` function.

Run the following command in the SSH command line. 

```
rake project:build_and_export_final_data
```

This normally takes a while. Once it's done, you can find a `JSON` file in `tmp` or a folder where you ran the command. You can download that file to your local. 


# Dumping the Entire DB Tables

It is possible that the native `build_and_export` function doesn't work properly. In this case, you can dump the MongoDB database directly. These are all done in the SSH command line.

1. Enter the MongoDB Command Line

```
mongo --shell
```

2. Check out the DB available in the server

```
show databases;
```
This command shows all the database names in the system. Normally, the DB name for the Scribe is `scribe_api_development`.

3. Select the DB that you want to export
Since the data is normally stored in `scribe_api_development`, you can type in:

```
use scribe_api_development;
```

If the name of the DB is not `scribe_api_development`, you need to type in a correct DB name. Then, the DB is selected.

4. List out the collections

```
show collections;
```
Once you run this command, you can see all the collections ("collection" is same to "table" in MySQL). 

Normally, the relevant collections that you want to dump are:

- classifications
- final_subject_sets
- subject_sets
- subjects

5. Exit from the MongoDB commandline
```
exit
```

6. Dump the DB's collections one by one
```
mongoexport --db scribe_api_development --collection final_subject_sets --out final_subject_sets.json
```
You need to export all the four collections (meaning you need to run this command four times by changing collection and output names).

The general form of the command is:
```
mongoexport --db [DB_name] --collection [Collection_name] --out [output_file_name.json]
```

Then, you can put the JSON files in to `/db_dump/[city_name]` and push them to the Github repo. 

That's it!
