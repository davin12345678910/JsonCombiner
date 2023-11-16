class Hierachy:

    """
    Definition: This is the hierachy object, which will represent the
    child/parent relationship between the various objects with the passed
    in mask RCNN object

    Parameters:
    1. polygon: this is the polygon that
    will represent the current object in the hierachy
    2. objectLabel: this is the label for the current object, such as bus

    Returns: Nothing
    """
    def __init__(self, polygon, object_label):
        """
        Fields
        1. polygon: this is the polygon that we will be saving
        2. children: this is the children objects of the current object of the hierachy
        3. object_label: this is the label for the current object, such as bus
        4. text: this is the text that the current object has
        5. descriptions: these are the descriptions that the current object has
        6. is_child: tells us if the current object is a child of another object
        """
        self.polygon = polygon
        self.children = None
        self.object_label = object_label
        self.text = {}
        self.descriptions = {}
        self.descriptions2 = None
        self.is_child = False
        self.include = True

    """
    Definition: this will set the text of the current hierachy  

    Parameters:
    1. text: this is the text that the current object will get

    Returns: nothing
    """
    def set_text(self, text):
        self.text = text

    """
    Definition: This will set the descriptions of the current hierachy

    Parameters:
    1. descriptions: This is the descriptions that the current object will get 

    Returns: nothing 
    """
    def set_descriptions(self, descriptions):
        self.descriptions = descriptions

    """
    Definition: This gives the size of the current hierachy 

    Parameters: nothing

    Returns: the size of the hierachy
    """
    @staticmethod
    def hierachy_size(hierachy):
        if hierachy == None:
            return 0

        if hierachy.children == None:
            return 1

        maxSize = 0
        for node in hierachy.children:
            nodeSize = hierachy.hierachy_size(node)
            maxSize = max((1 + nodeSize), maxSize)

        return maxSize
