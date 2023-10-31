# JsonCombiner

## Purpose of JsonCombiner 
JsonCombiner is a repo which allows us to do a few important tasks:
- combine all of the given json information from various models
- reformat the given json information into the best possible format that gpt-4 can understand
- filter any information that does not meet a threshold 

## Installation steps 
To install JsonCombiner, here are the steps:

1. `git clone https://github.com/davin12345678910/JsonCombiner.git`
2. `pip install copy`
3. `pip install json`
4. `pip install shapely`
5. `pip install os`
6. `pip install openai`
7. `pip install unittest`

## Important note: 
if you commit changes from JsonParser to makeability_real-world-alt-text, you will
need to generate a new API-Key in order to ask a query to gpt-4:
Visit: https://platform.openai.com/account/api-keys to generate a new API key

## Directory structure
### JsonParserTestsJson
- this contains the Jsons for tests to make sure all the code is working 
  - Note: this is currently in progress due to repo changes

### MainJsons
- this contains the main json which we use in main.py

### Python
contains a few important files
- main.py: this is the class to call when you want to get results 
- CallChatGPT.py: code that allows an individual to call the gpt-4 api
- Hierachy.py: this is the code that represents each of the hierachies in the end result
- JsonParser.py: this allows us to combine all of the information into a readable format for gpt-4
- test_JsonParser.py: you can test out the program to make sure everything is working properly

### textFiles
- history.txt: contains past chat history for the current discussion with gpt-4


## Questions?
Feel free to contact me at: davin123@uw.edu or davin123@cs.washington.edu
