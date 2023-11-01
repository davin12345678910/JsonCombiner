import json
import JsonParser
import CallChatGtp


'''''''''
Note: we will need to make this into a method which we will be calling from the main.py
method of the entire repo 
'''

endpointFile = open("C:\\Users\\davin123\\PycharmProjects\\makeability_real-world-alt-text\\JsonCombiner\\MainJsons\\EndpointResult.json", "r")

endpointsJson = json.loads(endpointFile.read())

maskRCNNJson = endpointsJson["MaskRCNNEndpointCaller"]

OCRJson = endpointsJson["OCREndpointCaller"]

GRiTJson = endpointsJson["GriTEndpointCaller"]

# This will allow us to make a new Json Parser object
# Then we can get the string back from the object
jsonParser = JsonParser.JsonParser(maskRCNNJson, OCRJson, GRiTJson)

resultJson = jsonParser.return_final_json()

# Call ChatGPT
# response = ChatGPT.call(query, resultJson)

print("This is the resulting Json: \n ", resultJson)

query = input("What questions do you have about the current image?: ")

f = open("C:\\Users\\davin123\\PycharmProjects\\makeability_real-world-alt-text\\JsonCombiner\\textFiles\\history.txt", "a")
f.write(query + "\n")

callChatpGTp = CallChatGtp.CallChatGtp(query, resultJson)

print(callChatpGTp.__call__())







