# grandm.ai
Greek chatbot

* Phase 1: Create flask sqlite db, create and form tables, drain the static info from OASA API into db. # DONE
* Phase 2: create a many:many relationship of the 2 tables # IN PROGRESS
* Phase 3: Value mapping. Line description needs preprocessing/mapping? 
    * static replacement is bad option - solution: when user types a stop, check if its most part matches a db stop_name
    * check each stops suffix, map based on that?
* Phase 3: Chat API added # DONE
