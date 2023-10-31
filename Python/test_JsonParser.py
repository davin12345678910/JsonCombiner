import unittest
import json
import os

import JsonCombiner.Python.JsonParser

"""
Here are the global variables
"""
parent_dir = "/JsonCombiner/JsonParserTestsJsons/"



class TestJsonParser(unittest.TestCase):

    # note we will not have to deal with cases where items are the same size, as this is
    # very very highly unlikely

    """
    This test to see if the most basic hierachy can be made
    in this case a hierachy with one object.
    """
    def test_basic_hierachy(self):

        """
        Here we will get the jsons that we will be using for our test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test1/MaskRCNN_test1.json"), "r")
        maskRCNNJson1 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test1/GoogleOCR_test1.json"), "r")
        OCRJson1 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test1/GRiT_test1.json"), "r")
        GRiTJson1 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test1 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson1, OCRJson1, GRiTJson1)
        actual_output = jsonParser_test1.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test1/expectedOutput_test1.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check if the outputed json is correct or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This is to check to see if the correct behavior occurs if there are two parents.
    With two parents, and both parents containing the same child, both parents should 
    have the child as a child
    """
    def test_two_parents(self):
        """
        These are the jsons that we will be using for our test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test2/MaskRCNN_test2.json"), "r")
        maskRCNNJson2 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test2/GoogleOCR_test2.json"), "r")
        OCRJson2 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test2/GRiT_test2.json"), "r")
        GRiTJson2 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test2 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson2, OCRJson2, GRiTJson2)
        actual_output = jsonParser_test2.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test2/expectedOutput_test2.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the outputs are the same are not 
        """
        self.assertEqual(expected_output, actual_output)

    """
    If you have a bus, person, and car, then the hieracy
    should only have bus -> person -> car
    """
    def test_three_level_hierachy(self):

        """
        These are the jsons that we will be using
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test3/MaskRCNN_test3.json"), "r")
        maskRCNNJson1 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test3/GoogleOCR_test3.json"), "r")
        OCRJson1 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test3/GRiT_test3.json"), "r")
        GRiTJson1 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test3 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson1, OCRJson1, GRiTJson1)
        actual_output = jsonParser_test3.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test3/expectedOutput_test3.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will be checking if the output is correct or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This checks to see if we can properly add text in to the hierachy.
    And also check to see if the smallest object that can get a piece of text gets
    the text and not something higher up in the hierachy
    """
    def test_text_added(self):
        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test4/MaskRCNN_test4.json"), "r")
        maskRCNNJson4 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test4/GoogleOCR_test4.json"), "r")
        OCRJson4 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test4/GRiT_test4.json"), "r")
        GRiTJson4 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test4 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson4, OCRJson4, GRiTJson4)
        actual_output = jsonParser_test4.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test4/expectedOutput_test4.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This checks to see if we can properly add descriptions in to the hierachy.
    And also check to see if the smallest object that can get a piece of description gets
    the description and not something higher up in the hierachy
    """
    def test_descriptions_added(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test5/MaskRCNN_test5.json"), "r")
        maskRCNNJson5 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test5/GoogleOCR_test5.json"), "r")
        OCRJson5 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test5/GRiT_test5.json"), "r")
        GRiTJson5 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test5 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson5, OCRJson5, GRiTJson5)
        actual_output = jsonParser_test5.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test5/expectedOutput_test5.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)

    """
    Here we will test to see if a hierachy can properly be made if there are objects with the 
    same name. Overall, this mainly test to see if having the same name for objects does not impact 
    the overall behavior of hierachy making 
    """
    def test_multiple_objects_with_same_name(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test6/MaskRCNN_test6.json"), "r")
        maskRCNNJson6 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test6/GoogleOCR_test6.json"), "r")
        OCRJson6 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test6/GRiT_test6.json"), "r")
        GRiTJson6 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test6 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson6, OCRJson6, GRiTJson6)
        actual_output = jsonParser_test6.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test6/expectedOutput_test6.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)



    """
    Make sure that two non overlapping hierachies are seperate
    """
    def test_two_hierachies(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test7/MaskRCNN_test7.json"), "r")
        maskRCNNJson7 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test7/GoogleOCR_test7.json"), "r")
        OCRJson7 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test7/GRiT_test7.json"), "r")
        GRiTJson7 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test7 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson7, OCRJson7, GRiTJson7)
        actual_output = jsonParser_test7.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test7/expectedOutput_test7.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This is the case when two things do not meet 
    the overlap threshold, and should not be combined into one hierachy
    """
    def test_not_met_threshold(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test8/MaskRCNN_test8.json"), "r")
        maskRCNNJson8 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test8/GoogleOCR_test8.json"), "r")
        OCRJson8 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test8/GRiT_test8.json"), "r")
        GRiTJson8 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test8 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson8, OCRJson8, GRiTJson8)
        actual_output = jsonParser_test8.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test8/expectedOutput_test8.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This is the test case when the objects do meet the 
    threshold and form to JsonCombiner one hierachy 
    """
    def test_met_threshold(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test9/MaskRCNN_test9.json"), "r")
        maskRCNNJson9 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test9/GoogleOCR_test9.json"), "r")
        OCRJson9 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test9/GRiT_test9.json"), "r")
        GRiTJson9 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test9 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson9, OCRJson9, GRiTJson9)
        actual_output = jsonParser_test9.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test9/expectedOutput_test9.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)


    """
    This test to see if the formatting of the hierachy string is proper and correct
    """
    def test_hierachy_string(self):

        """
        These are the jsons that we will be using for this test
        """
        maskRCNN_file = open(os.path.join(parent_dir, "test10/MaskRCNN_test10.json"), "r")
        maskRCNNJson10 = json.loads(maskRCNN_file.read())

        OCR_file = open(os.path.join(parent_dir, "test10/GoogleOCR_test10.json"), "r")
        OCRJson10 = json.loads(OCR_file.read())

        GRiT_file = open(os.path.join(parent_dir, "test10/GRiT_test10.json"), "r")
        GRiTJson10 = json.loads(GRiT_file.read())

        """
        Here we will be getting the actual results of the JsonParser
        """
        jsonParser_test10 = JsonCombiner.Python.JsonParser.JsonParser(maskRCNNJson10, OCRJson10, GRiTJson10)
        actual_output = jsonParser_test10.return_final_json()

        """
        Here are the expected results
        """
        json_file = open(os.path.join(parent_dir, "test10/expectedOutput_test10.json"), 'r')
        expected_output = json_file.read()

        """
        Here we will check to see if the output is the same or not
        """
        self.assertEqual(expected_output, actual_output)







    # think of more possible tests, a good way to find more tests, is to look at the code

