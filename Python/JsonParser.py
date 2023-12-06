import copy
import json

from shapely import Polygon

import JsonCombiner.Python.Hierachy

class JsonParser:



    """
    Important Class definitions:
    Hierachies: these consist of a tree-like data structure that consist
    of the parent/child relationships between objects. In the final json
    there can be multiple of these hierachies.
    EXP Hierachies:
    1. bus->person->shirt
    2. stroller -> baby -> pasifier
    """


    """
    Definition: this method will initalize a JsonParser object which is an object that takes in  
    three Jsons, one for objects, one for text, and a final json for descriptions. With this object
    you can call get_final_json on this JsonParser object to produce the final json of that represents 
    the data that was in the three json passed in.
    
    Parameters:
    1. mask_rcnn: this is the maskRCNN Json that you will use to get the objects and build the hierachies 
    that consist of the parent/child relationships between objects
    2. ocr: this is the OCR json, that you will use to get the text which you will be giving to objects 
    in the hierachies in which you will be building 
    3. GRiT: this is the GRiT json, that you will use to get the descriptions which you will be giving to
    objects in the hierachies that you will be building 
    
    Returns: nothing 
    """
    def __init__(self, oneformer, ocr, GRiT, gpt4):

        """
        Here you will be saving the jsons passed in for later use,
        in this case you will be saving oneformer, OCR, and GRiT and GPT4, into
        oneformer_json, ocr_json, GRiT_json, gpt4 respectively
        """
        self.oneformer_json = oneformer
        self.ocr_json = ocr
        self.GRiT_json = GRiT
        self.gpt4_json = gpt4

        # these are required for the construction of the json
        self.hierachy_dict = {}
        self.center = {}
        self.not_visited_descriptions = []

        """
        other fields
        """
        self.OVERLAP_THRESHOLD = 0.60
        self.object_level = {}
        self.child_map = {}



    """
    Definition: This is where we will be running the main parts of the algorithm that will allow 
    us to get the final json which we will be returning to the client
    
    Parameters: None
    
    Returns: Returns the final json string that represents and contains all of the hierachies found from the 
    three passed in jsons in a nicely formed json
    """
    def return_final_json(self):

        """
        check to see if any passed in jsons are None, if so return an exception
        """
        if self.GRiT_json == None or self.ocr_json == None or self.oneformer_json == None:
            raise Exception("Cannot pass in a None json object")

        """
        #1. This part will sort the maskRCNN objects by their size (in terms of area)
        """
        oneformer_objects = self.oneformer_json["results"]
        oneformer_objects_sorted = sorted(oneformer_objects,
                key=lambda x: Polygon(x["bbox"]).area)

        # here we will be storing all of the object names
        object_names = []
        for object in oneformer_objects_sorted:
            object_names.append(object["name"])

        """
        #2. This part will iterate through objects from smallest to largest to determine parent/child 
        relationships between the objects in the maskRCNN object and will also make sure that 
        no object has a child of any of its child objects 
        """
        layer_one_hierachy = self.get_first_layer(oneformer_objects_sorted)


        """
        #3. Add in layer two. You will iterate through the OCR which contains the text in the image
        and GRiT which contains the descriptions in the image, and give the text and
        descriptions to the smallest valid child objects in each hierachy 
        """
        complete_hierachies = self.add_in_second_layer(layer_one_hierachy, self.ocr_json, self.GRiT_json, self.gpt4_json)


        """
        #4. Here we will make the final Json as a string, which will contain all of 
        the hierachies that we built from the three 
        Jsons that were given, mas_rcnn, ocr, and GRiT
        """
        final_json = self.build_final_json(complete_hierachies)

        # Here we will return the final results
        return final_json



    """
    Step #2
    Definition: This is where we will be building the first layer of the program. For the first layer
    we will be building hierachies which will contain the parent/child relationships between the objects
    passed in from the json, but does not have the text and descriptions for each object. 
    Example: hierachy with three objects bus, person, and shirt would be bus->person->shirt
    
    Parameters: 
    1. mask_rcnn_objects: this is the Json that will have all of the objects that we will 
    be using in order to build the hierachies (check definition of hierachies at the top for a more in-depth def)
    
    Return: a list of hierachy objects that contain the parent-child relationships between the objects
    that came from the mask_rcnn Json without text or descriptions (text or descriptions will be added in second layer)
    """
    def get_first_layer(self, oneformer_objects):

        """
        Make sure that the json given is not None, or else we will return an exception
        """
        if oneformer_objects == None:
            raise Exception("Cannot give None mask_rcnn Json")

        """
        Using the passed in mask_rcnn object, we will build the hierachies using the objects in the given json.
        We will build the hierachies, by looping through the objects in the mask_rcnn json, and for each object,
        we will see if any previous hierachies can be a child of the current hierachy using the root object of the
        other hierachy, which is the largest object, and based on how much of this object is contained within the
        current hierachies object, if it meets the OVERLAP_THRESHOLD, we will make the other hieachy a child of the current hierachy.
        EXP: if a previous hierachy was person->shirt, and the current hierachy which you just made is bus
        and the person object is in the bus object by 75% percent which is more than the OVERLAP_THRESHOLD of 67%,
        we will make the hierachy containing the person object a child of the current hierachy with the bus.
        """
        hiearchies = []

        for current_object in oneformer_objects:

            # Create a Shapely Polygon object
            polygon = Polygon(current_object["bbox"])

            # Calculate the centroid
            centroid = polygon.centroid

            # Access the x and y coordinates of the centroid
            x, y = centroid.x, centroid.y
            self.center[str(current_object["bbox"])] = [x, y]

            # here we will need to do the thing where if there are multiple objects we will need to append the
            # count for it to the back
            current_hierachy = JsonCombiner.Python.Hierachy.Hierachy(current_object["bbox"], current_object["name"])

            self.hierachy_dict[current_object["name"]] = current_hierachy

            # see if any of the previous objects overlap with the hierachies that we already found
            for other_hierachy in hiearchies:

                # Here we will get data about the intersection
                current_polygon = Polygon(current_object["bbox"])

                # this is the other polygon that we will be comparing this polygon to
                other_polygon = Polygon(other_hierachy.polygon)

                # here we will check the overlap area and if it is more we will have it as
                # a child of the current hierachy
                intersection_area = current_polygon.intersection(other_polygon).area
                percentage_overlap = intersection_area / other_polygon.area
                if percentage_overlap >= self.OVERLAP_THRESHOLD:

                    """
                    Here you will set other hierachies is_child to true 
                    since it is a child of the current object 
                    """
                    other_hierachy.is_child = True

                    # here we will give the current hierachy a list where it can
                    # add its first child
                    if current_hierachy.children == None:
                        current_hierachy.children = []

                    """
                    Here you will also need to make sure if a potential child 
                    hierachy's root object is not already a child of any of the 
                    child objects in the current hierachy. 
                    For example if you have bus->person->shirt, you 
                    cannot have shirt added to the hierachy since shirt is already 
                    a child of person
                    """
                    """
                    We want to prevent the case where you have 
                    bus->person->shirt and bus->shirt 
                    """
                    if self.can_add_as_child(current_hierachy, other_hierachy):
                        current_hierachy.children.append(other_hierachy)

            # here we will be appending the new hierachy into the hierachy list
            hiearchies.append(current_hierachy)

            """
            Everytime we add a new hierachy, we will sort the hierachies by their size and reverse, so that 
            We always compare with the largest hierachies before going to the smaller ones. 
            For example if we had people->shirt and shirt, we would want to go to the largest
            hierachy first, the bottom code allows us to do that. If you did not sort from largest
            to smallest bus for example would take shirt which will give us bus->shirt, but what we
            really want it bus->people->shirt
            """
            """
            overall we sort by largest hierachy so that we can add the largest hierachy possible to the 
            current hierachy first, and if any sub hierachies come in, we will already have it in the hierachy
            and will not add it in 
            if we did not sort we would add a smaller one in, and then would have to remove it and add the larger
            one in, which would be a larger hassle 
            """
            sorted(hiearchies,
                   key=lambda x: JsonCombiner.Python.Hierachy.Hierachy.hierachy_size(x))
            hiearchies.reverse()

        return hiearchies


    """
    Definition: This will check to see if you can have another hierachy as a child to the 
    current hierachy that you are on. This is done through looking at the root object of the other hierachy 
    and seeing if any of current hierachies child objects has the root object of the other hierachy 
    as a child
    EXP: you want to add in shirt as a child to your current hierachy of bus->person->shirt, 
    given that person already has shirt as a child object, you cannot add in shirt as a child to the 
    current hierachy
    
    Paramaters:
    1. current_hierachy: this is the current_hierachy you are on, and trying to 
    see if you can add the other_hierachy as a child 
    2. other_hierachy: this is the other_hierachy you are looking at, and you are trying to 
    see if you can add this hierachy to the current_hierachy as a child
    
    Returns: a boolean that tells you if you can add the other_hierachy 
    to the current_hierachy that you are on as a child 
    """
    def can_add_as_child(self, current_hierachy, other_hierachy):

        """
        Make sure that none of the hierachies passed in are None, if one is, you will throw an exception
        """
        if current_hierachy == None or other_hierachy == None:
            raise Exception("Cannot pass in a none hierachy")

        """
        Here we will call get_objects_of_hierachy which will put all of the objects
        in the current hierachy in a given list current_hierachy_objects, then we will check to see if the
        other_hierachy can be added as a child by seeing if it's root object is not
        a child to any of the current_hierachy's child objects. You can do this by
        seeing if the other hierachies root object is contained within a list of all of the objects in the current hierachy
        """

        """
        Get all of the current hieachies objects
        """
        current_hieachy_objects = []
        self.get_objects_of_hierachy(current_hierachy, current_hieachy_objects)

        """
        Here we check to see if the other hierachy's root is already a child in the current hierachy 
        """
        return not current_hieachy_objects.__contains__(other_hierachy.object_label + " " + str(other_hierachy.polygon))



    """
    Definition: This will get all of the objects of the current hierachy and put them into the 
    passed in list
    
    Parameters: 
    1. current_hierachy: this is the hierachy that you will get all of the objects from 
    2. current_children: this will store all of the objects from the current hierachy 
    
    Returns: nothing 
    """
    def get_objects_of_hierachy(self, current_hierachy, current_children):

        """
        Make sure the hierachy and the list we are storing the children
        in are not None, if so, throw an exception
        """
        if current_hierachy == None or current_children == None:
            raise Exception("Passed in a None hierachy or list")

        """
        Here we will be iterating through the hierachy and getting
        all of the objects in the current hierachy and storing them
        into currentChildren
        """
        if current_hierachy == None:
            return

        # here we will add in the current hierachy that is in the current hierachy
        current_children.append(current_hierachy.object_label + " " + str(current_hierachy.polygon))

        # if there no longer are children we will stop looking through the hiearchy
        if current_hierachy.children != None:

            # look through the rest of the children and their children
            for child in current_hierachy.children:
                self.get_objects_of_hierachy(child, current_children)



    """
    Description: This will add in the second layer of the hierachy, in other words 
    it will give the objects in the hierachies text and descriptions if valid to do so
    
    Parameters:
    1. hierachies: these are the hierachies that you will be adding text and 
    descriptions into their objects
    2. ocr: this is the Json that contains all of the text which you could possibily be adding
    onto the objects in the hierachies 
    3. GRiT: this is the json that contains all of the possible descriptions which you could be
    adding onto the objects in the hierachies
    
    returns: nothing 
    """
    def add_in_second_layer(self, hierachies, ocr, grit, gpt4):

        """
        Make sure that the hierachy and that the jsons we
        are passed in are not none, if not throw an exception
        """
        if hierachies == None or ocr == None or grit == None or gpt4 == None:
            raise Exception("Passed in a None hierachy or json(s)")

        # we need this so that we only get the largest of the largest hierachies that do not have
        # any parent above it
        # OVERALL IDEA: this removes all of the nodes that are not a root of their hierachy
        valid_hearchies = []
        for hierachy in hierachies:
            if not hierachy.is_child:
                valid_hearchies.append(hierachy)

        """
        Here you will get the text and the descriptions from GRiT and gpt4
        which you will possible add to the hierachies if valid to do so
        """
        text_candidates = ocr["results"]
        description_candidates = grit["results"]
        description_candidates2 = gpt4["response"]

        # TEXT
        """
        Here we will be adding all of the text into the hierachies if valid to do so 
        then we will add the descriptions to the hierachies given if valid to do so
        and then return the hierachy that results from the possible addition of text and descriptions  
        """
        for current_hierachy in valid_hearchies:
            visited_text = []
            self.add_in_text(current_hierachy, text_candidates, visited_text)

        #GPT4
        # here we will be adding in the descriptions for gpt4
        for current_gpt4 in description_candidates2:

            # this is to check if the json has the name in the json, if not, it is possible
            # that gpt4 could not find a description for the given object
            if current_gpt4["name"] in self.hierachy_dict:

                # now we will need to set the corresponding hierachies description
                self.hierachy_dict[current_gpt4["name"]].descriptions2 = current_gpt4["caption"]

        #GRiT
        # this we will need to use for GRiT
        visited_descriptions = []
       # add in GRiT descriptions over here
        for current_hierachy in valid_hearchies:
            self.add_in_descriptions(current_hierachy, description_candidates, visited_descriptions)

        # LEFT OVER DESCR
        # here we will be adding in all of the descriptions that are not attached to a hierachy
        for description in description_candidates:
            if description not in visited_descriptions:
                self.not_visited_descriptions.append(description)

        # FILTER THE HIERARCHY
        # here we will only be including hierachies that are not a child of another hierachy
        filtered_hierachies = []
        # look through all of the hierachies
        for hierachy in valid_hearchies:
            # make sure it's not a child
            if not hierachy.is_child:
                filtered_hierachies.append(hierachy)

        # here we will only be sending out valid hiearchies
        return copy.deepcopy(filtered_hierachies)


    """
    Definition: Here we will be adding all of the text to the hierachy that is given, and we will 
    add the text to the smallest child obect in the hierachy where it is valid to do so
    
    Parameters:
    1. current_hieachy: this is the current_hierachy we are on and going to possiibly add text onto
    2. text_candidates: this is the text which you will check to see if you can add to the 
    objects in your hierachy
    3. visited_text: this is the text that you have already added to the hierachy. 
    This helps ensure that only the smallest valid object gets the text
    
    Return: nothing
    """
    def add_in_text(self, current_hierachy, text_candidates, visited_text):

        """
        Make sure that the text we are passed in is not None and that the
        list we will store the visited text is not None, and throw exception if so
        """
        if text_candidates == None or visited_text == None:
            raise Exception("Passed in a None text_candidates or visited_text")

        """
        base case
        """
        if current_hierachy == None:
            return

        """
        This will allow us to do the bottom up approach, since we are calling the recursive 
        calls first. Meaning that the smallest valid object will get the text
        """
        if current_hierachy.children != None:
            for child_hierachy in current_hierachy.children:
                self.add_in_text(child_hierachy, text_candidates, visited_text)

        """
        Here we will checking to see if we can add a text to the current object
        in the hierachy that we are on. At the end we will set the text we found for 
        to the current object 
        """
        valid_text = current_hierachy.text
        for text_canidate in text_candidates:

            text_canidate_polygon = [[round(float(text_canidate[0][0][0]), 1), round(float(text_canidate[0][0][1]), 1)],
                                     [round(float(text_canidate[0][1][0]), 1), round(float(text_canidate[0][1][1]), 1)],
                                     [round(float(text_canidate[0][2][0]), 1), round(float(text_canidate[0][2][1]), 1)],
                                     [round(float(text_canidate[0][3][0]), 1), round(float(text_canidate[0][3][1]), 1)]]

            current_polygon = Polygon(current_hierachy.polygon)
            other_polygon = Polygon(text_canidate_polygon)
            intersection_area = current_polygon.intersection(other_polygon).area

            overlap_percentage = intersection_area / other_polygon.area
            if overlap_percentage >= self.OVERLAP_THRESHOLD and overlap_percentage <= 1:
                if not visited_text.__contains__(text_canidate):
                    valid_text[text_canidate[1]] = text_canidate_polygon
                    visited_text.append(text_canidate)


    """
    Definition: this will add in all of the valid descriptions to objects in the hierachies if valid to do so 
    
    Parameters:
    1. current_hieachy: this is the current_hierachy we are on and going to add descriptions onto if valid to do so
    2. description_candidates: this is the descriptions which you will check to see if you can add to the 
    objects in your hierachy
    3. visited_descriptions: this is the descriptions that you have already added to the hierachy. 
    This helps ensure that only the smallest valid object gets the description
    
    Return: nothing
    """
    def add_in_descriptions(self, current_hierachy, description_canidates, visited_descriptions):

        """
        Make sure that the hierachy and the list we are storing the
        visited descriptions is not None, else return an exception
        """
        if description_canidates == None or visited_descriptions == None:
            raise Exception("Passed in a None description_candidates or visited_descriptions")

        """
        This contains the base case
        It also does the bottom up approach, to ensure that we start giving valid descriptions
        to the smallest object first
        """
        if current_hierachy == None:
            return
        if current_hierachy.children != None:
            for child_hierachy in current_hierachy.children:
                self.add_in_descriptions(child_hierachy, description_canidates, visited_descriptions)

        """
        Here we will be checking to see if we can add any descriptions
        to the object in the hieachy we are currently on 
        """
        current_descriptions = current_hierachy.descriptions
        for description_canidate in description_canidates:

            description_canidate_polygon = []
            x = round(float(description_canidate["bbox"][0]), 2)
            y = round(float(description_canidate["bbox"][1]), 2)
            w = round(float(description_canidate["bbox"][2]), 2) - round(float(description_canidate["bbox"][0]), 2)
            h = round(float(description_canidate["bbox"][3]), 2) - round(float(description_canidate["bbox"][1]), 2)
            description_canidate_polygon.append([x, y])
            description_canidate_polygon.append([x, (y + h)])
            description_canidate_polygon.append([(x + w), (y + h)])
            description_canidate_polygon.append([(x + w), y])

            # Here we will be getting the intersection data
            current_polygon = Polygon(current_hierachy.polygon)
            other_polygon = Polygon(description_canidate_polygon)
            intersection_area = current_polygon.intersection(other_polygon).area
            overlap_percentage = intersection_area / other_polygon.area
            if overlap_percentage >= self.OVERLAP_THRESHOLD and overlap_percentage <= 1:
                if not visited_descriptions.__contains__(description_canidate):
                    current_descriptions[description_canidate["label"]] = description_canidate_polygon
                    visited_descriptions.append(description_canidate)

    """
    Definition: this will swap two positions in a list given
    
    Parameters:
    1. List: this is teh list that you will be swapping elements in 
    2. pos1: this is the first position that you are considering for swapping
    3. pos2: This is the second position that you are considering for swapping
    
    Return: nothing  
    """
    def swap_positions(self, list, pos1, pos2):

        """
        Here we will make sure that the list we are swapping in is not None
        and that the positions given are not less than 0, else we will return an exception
        """
        if list == None or pos1 == None or pos1 < 0 or pos2 < 0:
            raise Exception("Passed in a None list or invalid indexes for pos1 or pos2")

        """
        Here we will pop the elements at the positions and there re-insert them
        in the right places so that they are swapped
        """
        first_ele = list.pop(pos1)
        second_ele = list.pop(pos2 - 1)
        list.insert(pos1, second_ele)
        list.insert(pos2, first_ele)

        return list



    """
    Definition: This will build the json that we will be giving back the user 
    which represents the data given by the three jsons that were passed in 

    Parameters:
    1. hirachies: this consist of the hierachies that you will be including in your final json

    Returns: string that represents the json representation of the three jsons that you gave
    """
    def build_final_json(self, hierachies):

        """
        Here we will check to make sure that the hierachy given is not None
        """
        if hierachies == None:
            raise Exception("Passed in a None hierachy")


        # here I will be removing hierachies that should not be higher than
        # they should be in terms of the hierachy
        hierachies = self.remove_if_is_child(hierachies)

        """
        We need to get the count of hierachies that have is_child == false, to know
        the number of valid hierachies there are, this comes in handy for the formatting 
        of the json 
        """
        number_of_valid_hierachies = 0
        for current_hierachy in hierachies:
            if current_hierachy.is_child == False:
                number_of_valid_hierachies = number_of_valid_hierachies + 1

        """
        Here you will be building the string representation of the final json
        - you will be going through each hierachy in the hierachies list
        - then you will check to see if this is a valid hierachy to include, by checking is_child
        - then you will be building the string for the current hierachy using build_hieachy_string
        - then you will add the string representation to the final json string that we will be returning
          back to the client
        """
        hierachy_json_list = []
        for current_hierachy in hierachies:
            if current_hierachy.is_child == False and current_hierachy.include:
                current_hieracy_json = {}
                current_json = self.build_hierachy_json(current_hierachy, current_hieracy_json)
                hierachy_json_list.append(current_json)

        # Here we will gonna return the finalJson
        final_json = {}

        """
        There are some hierachies that need to be removed and update hierachy will 
        remove all of the unwanted portions of the hierachy 
        """
        final_list = []
        # we need to check over each hierachy in the hierachy_json_list and make updates as needed
        for hierachy in hierachy_json_list:
            result = self.update_hierachy(hierachy, 0)
            final_list.append(result)

        # these are the final items that we will be using
        final_json["items"] = final_list

        # here we will add on the descriptions that were not attached to any specific objects
        final_json["dense_captions"] = self.not_visited_descriptions

        return json.dumps(final_json)

    """
    This will remove any cases where there is a child that shows up as a hierachy object as it should only 
    be a child of a hierachy object 
    
    Parameters:
    hierachies: these are the hierachies where we will be travesing over and will setting a boolean called 
    include if we want to include a hierachy or not
    
    Returns:
    a hierachy with the needed include variable updates, 
    this will be needed when we are building the developing the final json,


    Exp: we do not want backpack2, person -> backpack2. 
         We only want person -> backpack2
    """
    def remove_if_is_child(self, hiearchies):

        # here we will go through each of the hierachies
        visited = []
        for hierachy in hiearchies:
            if not self.object_level.__contains__(hierachy.object_label):
                visited.append(hierachy)
                # for objects at the top, they should have a level of 0
                self.traverse_hierachy(hierachy, 1)

        # then we will traverse while seeing if the
        # an object has a higher level, and if it does we will remove it
        for hierachy in hiearchies:
            if visited.__contains__(hierachy):
                self.remove_hierachy(self.object_level, hierachy, 0)

        return copy.deepcopy(hiearchies)

    """
    Description: for this method we will say include == False if we do not want to include a hierachy
    
    Parameters:
    object_level: here we will be checking if the hierachies are at the right level or not
    level: this is the current level in the hierachy we are at   
    """
    def remove_hierachy(self, object_level, hierachy, level):

        """
        If there is a hierachy that is in the wrong level, we will mark it as something to not include
        """
        if object_level.__contains__(hierachy.object_label) and object_level[hierachy.object_label] > level:
            hierachy.include = False

        if hierachy.children == None:
            return

        # go through the rest of the children
        for child in hierachy.children:
            self.remove_hierachy(object_level, child, level + 1)

    """
    Parameter: Here we will be getting the object level of the current objects by traversing through the tree
    and we will get the lowest level for each object name, where each object name is unique 
    
    Parameters:
    hierachy: this is the current hierachy we are travesing over
    level: this is the current level in the hierachy we are on 
    """
    def traverse_hierachy(self, hierachy, level):

        # if the hierachy is none we will stop
        if hierachy.children == None:
            return

        # traverse through all of the current children of the current hierahcy
        for child in hierachy.children:

            # this is where we will be updating the level for the current object name in the hierachy
            if self.object_level.__contains__(child.object_label):
                self.object_level[child.object_label] = max(level, self.object_level[child.object_label])
            else:
                self.object_level[child.object_label] = level

            # here we will traverse over the child children if any
            self.traverse_hierachy(child, level + 1)


    """
    Definition: Here you will be building up the string for the current hierachy that is passed in

    Parameters:
    1. currentHierachy: this is the currentHierachy that you will be building a string for 
    2. indentLevel: this is the current indentation level that you will be having in the current 
    level of the hierachy

    Returns: A string representation of the current hierachy that has been passed in 
    """

    def build_hierachy_json(self, current_hierachy, current_hierachy_json):

        """
        Here we will check to make sure that the current Hierachy passed in is not None
        and that the indentLevel is not less than 0, or esle given an exception
        """
        if current_hierachy == None:
            raise Exception("Passed in a None hierachy or invalid intentLevel")

        """
        Base Case: This in the case when you are at the end of the hierachy
        """
        if current_hierachy == None:
            return ""

        """
        This is where you will be building the string for 
        the current object in the hierachy that you are on, 
        where you will give the label and the bounding box 
        of the current objct
        """
        current_hierachy_json["center"] = self.center[str(current_hierachy.polygon)]
        current_hierachy_json["object"] = current_hierachy.object_label

        """
        This is where we will be building the string that will represent the 
        string of the curent children of the current object we are on in the hierachy 
        """
        current_hierachy_json["children"] = []
        if current_hierachy.children != None:
            for child in current_hierachy.children:
                # here we will append the json of the child object through recursion
                current_hierachy_json["children"].append(self.build_hierachy_json(child, {}))

        """
        We will be using this to build the portion for the GRiT descriptions 
        """
        current_hierachy_json["descriptions"] = []
        if current_hierachy.descriptions != None:
            index = 0
            for description in current_hierachy.descriptions:
                description_json = {}
                description_json["description" + str(index + 1)] = description
                current_hierachy_json["descriptions"].append(description_json)
                index = index + 1

        """
        This is where we will be building the string that will represent the gpt4 
        descriptions for the current object that we are on - which we will call descriptions2
        """
        # Do not include the bounding box for anything
        current_hierachy_json["descriptions2"] = []
        if current_hierachy.descriptions2 != None:
            description_json = {"description" : current_hierachy.descriptions2}
            current_hierachy_json["descriptions2"].append(description_json)

        """
        Here we will be building the string that will represent the 
        text for the current hierachy object that we are on 
        """
        current_hierachy_json["text"] = []
        if current_hierachy.text != None:
            index = 1
            for text in current_hierachy.text:
                text_json = {}
                text_json["text" + str(index + 1)] = text
                text_json["boundingBox"] = current_hierachy.text[text]
                current_hierachy_json["text"].append(text_json)
                index = index + 1

        """
        Here we will return the nicely and correctly formatted string back to build_final_json 
        for the current hierachy we are working with
        """
        if not current_hierachy.include:

            # update the map to have the object that it should be
            self.child_map[current_hierachy.object_label] = current_hierachy_json

            # later if we see just a string we can update it to be the object
            return current_hierachy.object_label

        return current_hierachy_json

    # NOTE: this is an important method that is requried
    """
    Defintion: Here we will be checking if there are any parts of the hierachy that is a string 
    if it is, it means that we found an object that showed up at multiple levels
    
    Parameters 
    hierachy: current hierachy we are updating 
    level: current level in the hierachy we are at 
    
    Returns:
    an updated hierachy 
    """
    def update_hierachy(self, hierachy, level):

        # if there are no more children we won't need to update anything
        if hierachy["children"] == None:
            return

        # here we will be looking over all of the children to see if any are strings
        list = []
        for child in hierachy["children"]:
            if type(child) is not str:
                list.append(child)
            elif type(child) is str and level + 1 == self.object_level[child]:
                list.append(self.child_map[child])
        hierachy["children"] = list

        # recurse through the rest of the hierachy
        for child in hierachy["children"]:
            self.update_hierachy(child, level + 1)

        return hierachy





