# grandm.ai
Greek chatbot

* Phase 1: Create flask sqlite db, create and form tables, drain the static info from OASA API into db. # DONE
* Phase 2: create a many:many relationship of the 2 tables
* Phase 3: Value mapping. Line description needs preprocessing/mapping? # IN PROGRESS
    * static replacement is bad option - solution: when user types a stop, check if its most part matches a db stop_name
