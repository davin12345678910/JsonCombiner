import json
import JsonParser
import CallChatGtp

"""
# these are the jsons that we are going to be passing in
maskRCNN_file = open("/Users/frukyid/PycharmProjects/JsonCombiner/JsonParserTestsJsons/test10/MaskRCNN_test10.json", "r")
maskRCNNJson = json.loads(maskRCNN_file.read())

OCR_file = open("/Users/frukyid/PycharmProjects/JsonCombiner/JsonParserTestsJsons/test10/GoogleOCR_test10.json", "r")
OCRJson = json.loads(OCR_file.read())

GRiT_file = open("/Users/frukyid/PycharmProjects/JsonCombiner/JsonParserTestsJsons/test10/GRiT_test10.json", "r")
GRiTJson = json.loads(GRiT_file.read())
"""

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







