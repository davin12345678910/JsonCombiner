import os
import openai

class CallChatGtp:

    def __init__(self, query, json):
        self.json = json
        self.query = query


    def __call__(self):
        prefix = "Give me the most accurate information possible with the given and previous questions: "
        betweenItemAndHistory = "Here are the previous questions asked:"
        currentQuestionPrompt = "Here is the current question, don't answer previous questions but take in mind the previous things that were mentioned, don't repeat any coordinates, do not mention coordinates or bounding boxes, do not give me information that is not in the json or history, if you do not have information about something from the json or hierachy state that you do not have information about it, and answer the current question as if you were talking to a five year old: "

        f = open("C:\\Users\\davin123\\PycharmProjects\\makeability_real-world-alt-text\\JsonCombiner\\textFiles\\history.txt", "r")
        history = f.read()

        prompt = prefix + self.json + betweenItemAndHistory + history + currentQuestionPrompt + self.query

        openai.api_key = "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"
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=709,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        return response.choices[0].text