def smart_append(list, item, item_type):
    """
    This appends the item, but ensures that the type matches Type.

    If the item doesn't match Type, it simply won't append it. This is mostly used when
    generating needs_lists in order to prevent the default "None" that is returned from functions
    winding up in needs_lists.

    :param list:
        The list to append to

    :param item:
        The Item to append

    :param item_type:
        The item to be used for validation

    :return:
        None. This is an in-place operation
    """
    if type(item) is item_type:
        list.append(item)


def compare_lists(left, right):
    """
    This function compares two lists to determine what they don't have in common

    :param left:
        "Left" List

    :param right:
        "Right" List

    :return:
        A Dict containing the missing items from the left and right side

        Example:
            list1 = [1,3,4]
            list2 = [1,2,3]
            compare_lists(list1, list2)
            {'missing_left': [2], 'missing_right': [4]}
    """
    missing_from_left = []
    missing_from_right = []
    for item in left:
        if item not in right:
            missing_from_right.append(item)
    for item in right:
        if item not in left:
            missing_from_left.append(item)
    return {"missing_left": missing_from_left, "missing_right": missing_from_right}