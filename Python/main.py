import json
import JsonParser
import CallChatGtp

def combine_json(query):
    '''''''''
    Note: we will need to make this into a method which we will be calling from the main.py
    method of the entire repo 
    '''

    endpointFile = open("C:\\Users\\davin\\PycharmProjects\\real-world-alt-text\\JsonCombiner\\MainJsons\\EndpointResult.json", "r")

    endpointsJson = json.loads(endpointFile.read())

    maskRCNNJson = endpointsJson["MaskRCNNEndpointCaller"]

    OCRJson = endpointsJson["OCREndpointCaller"]

    GRiTJson = endpointsJson["GriTEndpointCaller"]

    print(maskRCNNJson)

    # default JSON until the OCR JSON comes in later
    ocr_json = {"results": []}

    # This will allow us to make a new Json Parser object
    # Then we can get the string back from the object
    jsonParser = JsonParser.JsonParser(maskRCNNJson, ocr_json, GRiTJson)

    resultJson = jsonParser.return_final_json()

    # Call ChatGPT
    # response = ChatGPT.call(query, resultJson)

    print("This is the resulting Json: \n ", resultJson)

    f = open("C:\\Users\\davin\\PycharmProjects\\real-world-alt-text\\JsonCombiner\\textFiles\\history.txt", "a")
    f.write(query + "\n")

    callChatpGTp = CallChatGtp.CallChatGtp(query, resultJson)

    gpt4_results = callChatpGTp.__call__()
    print(gpt4_results)

    return gpt4_results


# here we will be testing out JsonCobiner
if __name__ == '__main__':
    results = combine_json("What is in the current image?")
    print(results)







