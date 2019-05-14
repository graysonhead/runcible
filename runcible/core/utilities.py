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