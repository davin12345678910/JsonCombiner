import json
import JsonCombiner.Python.JsonParser


def combine_json(oneformer, llava, ocr, gpt4):

    '''''''''
    Note: we will need to make this into a method which we will be calling from the JsonCombiner.py
    method of the entire repo 
    '''
    # default JSON until the OCR JSON comes in later
    ocr_json = {"results": ocr}

    # This will allow us to make a new Json Parser object
    # Then we can get the string back from the object
    jsonParser = JsonCombiner.Python.JsonParser.JsonParser(oneformer, ocr_json, llava, gpt4)

    resultJson = jsonParser.return_final_json()

    return resultJson








