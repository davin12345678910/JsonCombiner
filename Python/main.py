import json
import JsonCombiner.Python.JsonParser
import JsonCombiner.Python.CallChatGtp
import openai

def combine_json(oneformer, llava, ocr):
    '''''''''
    Note: we will need to make this into a method which we will be calling from the main.py
    method of the entire repo 
    '''

    # print("went into combineJson!")

    # default JSON until the OCR JSON comes in later
    ocr_json = {"results": ocr}

    # This will allow us to make a new Json Parser object
    # Then we can get the string back from the object
    jsonParser = JsonCombiner.Python.JsonParser.JsonParser(oneformer, ocr_json, llava)

    resultJson = jsonParser.return_final_json()

    # print("THIS IS THE RESULT JSON: ", resultJson)
    return resultJson


# here we will be testing out JsonCobiner
'''''''''
if __name__ == '__main__':
    results = combine_json("What is in the current image?")
    print(results)
'''







