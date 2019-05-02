


# This file contains general useful functions

def mapInput(input, init_min, init_max, final_min, final_max):

    output = ((input - init_min) / (init_max - init_min)) * (final_max - final_min) + final_min
    return output


def limit(input, top_limit, bottom_limit):

    if input > top_limit:
        return top_limit
    elif input < bottom_limit:
        return bottom_limit
    else:
        return input

def interpolate(independent_list, dependent_list, independent_value):

    for x in independent_list:
        if independent_value <= x:
            return 0

