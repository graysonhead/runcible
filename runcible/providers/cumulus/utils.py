def pre_parse_commands(pre_parse_commands):
    """
    :param pre_parse_commands:
    :return:
    """
    commands = []

    for line in pre_parse_commands:
        # This handles lines like: net add interface swp3,5 bridge vids 2-5
        if line.startswith('net add interface') and ',' in line.split(' ')[3] \
                or line.startswith('net add interface') and '-' in line.split(' ')[3]:
            components = line.split(' ')
            int_iter = multi_port_parse(components[3])
            # int_iter = line.split(' ')[3].strip('swp').split(',')
            # int_iter = extrapolate_list(int_iter, int_out=False)
            for interface in int_iter:
                newline = []
                for comp in components[0:3]:
                    newline.append(comp)
                newline.append(interface)
                for comp in components[4:]:
                    newline.append(comp)
                commands.append(' '.join(newline))
        # Same thing but for bonds
        # TODO: This and the above could probably be a function
        elif line.startswith('net add bond') and ',' in line.split(' ')[3] \
                or line.startswith('net add bond') and '-' in line.split(' ')[3]:
            components = line.split(' ')
            int_iter = multi_port_parse(components[3])
            for interface in int_iter:
                newline = []
                for comp in components[0:3]:
                    newline.append(comp)
                newline.append(interface)
                for comp in components[4:]:
                    newline.append(comp)
                commands.append(' '.join(newline))
        else:
            commands.append(line)
    return commands


def multi_port_parse(prt):
    # Populate this list with the complete list of interface names
    int_names = []
    # We may have an abbreviation like this 'po1-3,pol2-4'
    if ',' in prt:
        ports_list = prt.split(',')
    else:
        ports_list = [prt]
    # Split it into ['pol1-3', 'pol2-4']
    for ports in ports_list:
        prt_name = None
        # Take 'po1-3' and turn it into [ 'po1', 'po2', 'po3' ]
        prt_name = ports.strip('1234567890-')
        compact_list = ports.strip(prt_name)
        prt_list = extrapolate_list([compact_list])
        # This is for some really ugly edge-cases like 'po1-3,6,pol4' where a number can appear without an ID
        # It seems safe to assume that the last ID can be used in all cases
        for pn in prt_list:
            if prt_name is None or prt_name == '':
                if last_name is not None:
                    # prt_list[prt_list.index(pn)] = last_name + pn
                    int_names.append(last_name + pn)
                else:
                    raise ValueError(
                        "The name of the port could not be determined, this is probably due to a malformed"
                        " name string")
            else:
                int_names.append(prt_name + pn)
        if bool(prt_name) is True:
            last_name = prt_name
    return int_names


def extrapolate_list(numlist, int_out=False):
    newlist = []
    # We need to ensure False values pass through here in order to deset lists
    if numlist is False:
        return False
    elif type(numlist) is not list:
        raise TypeError
    for num in numlist:
        if type(num) is str:
            if '-' in num:
                nums = num.split('-')
                for n in range(int(nums[0]), int(nums[1]) + 1, 1):
                    newlist.append(str(n))
            else:
                newlist.append(str(num))
        else:
            newlist.append(str(num))
    if int_out:
        intlist = []
        for num in newlist:
            intlist.append(int(num))
        return intlist
    else:
        return newlist
