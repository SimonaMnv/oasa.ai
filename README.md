# oasa.ai

## General Description 

Greek chatbot that retrieves stop and bus information. In terms of technologies/frameworks, the following were used:
* Flask,
* NLP (Spacy),
* HTML/CSS, used to build the UI of oasa.ai.

## Building steps

* Phase 1: Create flask sqlite db, create and form tables, drain the static info from OASA API into db.  
* Phase 2: create a many:many relationship of the 2 tables  
* Phase 3: Value mapping. Line description needs preprocessing/mapping? 
    * static replacement is bad option - solution: when user types a stop, check if its most part matches a db stop_name  
    * check each stops suffix, map based on that?  
    * check if user input exists as is. If not, suggest similar stops?  
    * Add the JSON patterns as stop words  
* Phase 3: Chat API added  
* Phase 4: Class "stopInfo" responses -- static information -> drained from local db
* Phase 5: Class "BusRoute" response -- static information -> drained from local db
* Phase 6: Class "busTime" response -- dynamic infomration -> drained from  api
* Phase 7: Chat Logger adedd

## Directory Structure

The following directories exist in the system:
* **db**, this is where the collection from the oasa api and some string preprocessing is performed. All static information is stored in a local db,
* **chatbot**, this is where the NLP model processed the user's input and returns a response either from the local db (static info) or from the oasa api (dynamic info)

## Steps to run 
* to just chat: chat.py,
* to create and drain data from oasa api: models.py > oasa_pull > stop_name_preprocessing,
* to train the NLP model: edit data/training_dataGREEK > ..train.py. 

## Versions

| |Version|
| ------------- |:-------------:|
| Python         |3.8  |


