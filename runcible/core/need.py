from enum import Enum


class NeedOperation(Enum):
    """
    Determine what operation should be performed to satisfy the need
    """
    SET = 1
    """
    Boolean: set sets the boolean to either True or False
    List: set replaces the entire list with a new list
    String: replaces the string with the new string
    Integer: replaces the integer with the new integer
    """

    DELETE = 2
    """
    List: must be specified with a value, and only deletes the value specified
    String: removes the string
    Integer: removes the integer
    """

    CLEAR = 3
    """
    List: deletes the whole list
    """

    GET = 4
    """
    Only used by ad-hoc commands, returns the value of the resource
    """

    ADD = 5
    """
    List: adds a new value (or values) to the listfrom runcible.core.need import NeedOperation as Op
    """

    CREATE = 6
    """
    Module: Creates a sub-module within a module array
    """

    REMOVE = 7
    """
    Module: Deletes a sub-module within a module array
    """


class Need(object):

    def __init__(self, resource, operation, value=None, sub_resource=None):
        """
        Needs are generated when the desired state is compared to the current state. Ideally, if a provider performs
        all of the needs required by a module, the dstate and cstate will be equivalent on the next run. Needs are
        somewhat arbitrary, and the resource and sub_resource will usually be a string. value will be either a list,
        string, integer, or nothing.

        :param resource:
            The attribute of the module that needs modification

        :param operation:
            How the attribute needs to be modified (see the enumeration class above)

        :param value:
            In the case of Add, Set, and Delete, the value to be added set or deleted

        :param sub_resource:
            Generally, multiple layers of attributes are discouraged (plugin writers should nest modules inside of
            other modules if depth is truly required), but in the rare cases this is necessary it allows the module
            to differentiate between multiple sub_resources
        """
        self.resource = resource
        if not isinstance(operation, NeedOperation):
            raise TypeError("Operation parameter for Need object must be an instance of NeedOperation")
        self.operation = operation
        self.value = value
        self.sub_resource = sub_resource

    def get_formatted_string(self):
        """
        :return:
            A string suitable to display to the user, detailed enough for them to grasp the intent of the need.
        """
        # If sub resource or value aren't set, insert an emptystring in their place
        sub_resource = ''
        value = ''
        if self.sub_resource:
            sub_resource = f"{self.sub_resource}."
        if self.value or self.value is False:
            value = f": {self.value.__str__()}"
        return f"{self.resource}.{sub_resource}{self.operation.name}{value}"

    def __eq__(self, other):
        comparison_list = []
        comparison_list.append(self.resource == other.resource)
        comparison_list.append(self.operation == other.operation)
        comparison_list.append(self.value == other.value)
        comparison_list.append(self.sub_resource == other.sub_resource)
        return all(comparison_list)

    def __repr__(self):
        sub_resource = ''
        value = ''
        if self.sub_resource:
            sub_resource = f"{self.sub_resource}."
        if self.value or self.value is False:
            value = f": '{self.value.__str__()}' "
        return f"<Needs: {self.resource}.{sub_resource}{self.operation.name}{value}>"
