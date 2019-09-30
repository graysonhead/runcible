from runcible.core.errors import RuncibleValidationError


class LabelBase(object):
    """
    Labels get added to devices, they have a key and value
    """
    type_label = ""
    description = ""
    attributes = {}
    # Example: 
    # attributes = {"device": {"type": str, "description": "Help text here"}

    def __init__(self, input_dict: dict):
        for key, value in input_dict.items():
            if key in self.attributes:
                setattr(self, key, value)

    def validate_input(self, input_dict: dict):
        for key, value in input_dict.items():
            if key not in self.attributes:
                raise RuncibleValidationError(msg=f"{self.type_label} label doesn't have an attribute {key}:\n"
                f"Possible attributes are {self.attributes.keys()}")
            else:
                if type(value) != self.attributes[key]["type"]:
                    raise RuncibleValidationError(msg=f"Value {value} of attribute {key} in label {self.type_label}"
                    f" must be a {self.attributes[key]['type']}")

    def render_as_dict(self):
        rendered_dict = {self.type_label: {}}
        for key in self.attributes.keys():
            rendered_dict[self.type_label].update({key: getattr(self, key)})
        return rendered_dict