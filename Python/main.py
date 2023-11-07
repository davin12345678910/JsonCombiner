import json
import JsonCombiner.Python.JsonParser
import JsonCombiner.Python.CallChatGtp
import openai

def combine_json(oneformer, llava, query, ocr):
    '''''''''
    Note: we will need to make this into a method which we will be calling from the main.py
    method of the entire repo 
    '''

    print("went into combineJson!")

    # default JSON until the OCR JSON comes in later
    ocr_json = {"results": ocr}

    # This will allow us to make a new Json Parser object
    # Then we can get the string back from the object
    jsonParser = JsonCombiner.Python.JsonParser.JsonParser(oneformer, ocr_json, llava)

    resultJson = jsonParser.return_final_json()

    print("This is resultJson: ", resultJson)

    # Call ChatGPT
    # response = ChatGPT.call(query, resultJson)

    # let's write the result json into the final json

    # print("This is the resulting Json: \n ", resultJson)

    f = open("C:\\Users\\davin\\PycharmProjects\\real-world-alt-text\\JsonCombiner\\textFiles\\history.txt", "a")
    f.write(query + "\n")

    # callChatpGTp = JsonCombiner.Python.CallChatGtp.CallChatGtp(query, resultJson)

    # gpt4_results = callChatpGTp.__call__()

    prefix = "Given the following json answer the current question with previous questions (if any) in mind: "
    betweenItemAndHistory = " Here are the previous questions asked:"
    currentQuestionPrompt = "Here is the current question, don't answer previous questions but take in mind the previous things that were mentioned, don't repeat any coordinates, do not mention coordinates or bounding boxes, do not give me information that is not in the json or history, if you do not have information about something from the json or hierachy state that you do not have information about it, and answer the current question as if you were talking to a five year old: "

    f = open("C:\\Users\\davin\\PycharmProjects\\real-world-alt-text\\JsonCombiner\\textFiles\\history.txt", "r")
    history = f.read()

    prompt = prefix + resultJson + betweenItemAndHistory + history + currentQuestionPrompt + query

    openai.api_key = "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"

    # here we will be building the string that we will put into content

    # print(prompt)

    gpt4_results = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # print(gpt4_results)

    # print(gpt4_results.choices[0]["message"]["content"])

    return gpt4_results.choices[0]["message"]["content"]


# here we will be testing out JsonCobiner
'''''''''
if __name__ == '__main__':
    results = combine_json("What is in the current image?")
    print(results)
'''







