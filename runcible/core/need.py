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
    Only used by ad-hoc commands, returns the value of the attribute
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

    def __init__(self, module, attribute, operation, value=None, parent_module=None):
        """
        Needs are generated when the desired state is compared to the current state. Ideally, if a provider performs
        all of the needs required by a module, the dstate and cstate will be equivalent on the next run. Needs are
        somewhat arbitrary, and the attribute and sub_resource will usually be a string. value will be either a list,
        string, integer, or nothing.

        :param module:
            The module from which the need originates.

        :param attribute:
            The attribute the need modifies, creates, or deletes.

        :param operation:
            The operation to perform on the attribute.

        :param value:
            If the operation requires a value, the value of the operation.

        :param sub_module:
            When operating from a sub_module such as a ModuleArray, the sub_module attribute identifies which
            sub_module the need is associated with.
        """
        self.attribute = attribute
        if not isinstance(operation, NeedOperation):
            raise TypeError("Operation parameter for Need object must be an instance of NeedOperation")
        self.operation = operation
        self.value = value
        self.module = module
        self.parent_module = parent_module

    def get_formatted_string(self):
        """
        :return:
            A string suitable to display to the user, detailed enough for them to grasp the intent of the need.
        """
        # If sub attribute or value aren't set, insert an emptystring in their place
        # sub_resource = ''
        # value = ''
        # if self.module:
        #     sub_resource = f"{self.module}."
        # if self.value or self.value is False:
        #     value = f": {self.value.__str__()}"
        # return f"{self.attribute}.{sub_resource}{self.operation.name}{value}"
        module = ''
        sub_module = ''
        parent_module = ''
        value = ''
        if self.module:
            module = f"{self.module}."
        if self.parent_module:
            parent_module = f"{self.parent_module}."
        if self.value or self.value is False:
            value = f": {self.value.__str__()}"
        return f"{parent_module}{module}{self.attribute}.{self.operation.name}{value}"

    def __eq__(self, other):
        comparison_list = []
        comparison_list.append(self.attribute == other.attribute)
        comparison_list.append(self.operation == other.operation)
        comparison_list.append(self.value == other.value)
        comparison_list.append(self.module == other.module)
        comparison_list.append(self.parent_module == other.parent_module)
        return all(comparison_list)

    def __repr__(self):
        return f"<Needs: {self.get_formatted_string()}>"
