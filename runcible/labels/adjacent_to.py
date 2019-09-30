from runcible.core.label import LabelBase


class AdjacentTo(LabelBase):
    type_label = "adjacent_to"
    description = "The 'adjacent_to' label is used to inform schedulers (such as the filter scheduler) about device " \
                  "topology, allowing them to scheduler runs in the last disruptive way possible."
    attributes = {
        "device": {
            "type": str,
            "description": "Contains an identifier for the adjacent device. May be an IP address, name, MAC adress "
                           "or other."
        },
        "port": {
            "type": str,
            "description": "The port on which the device is adjacent."
        }
    }