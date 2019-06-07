


# This file contains general useful functions

def mapInput(input, init_min, init_max, final_min, final_max):

    output = ((input - init_min) / (init_max - init_min)) * (final_max - final_min) + final_min
    return output


def limit(input_, top_limit, bottom_limit):

    if input_ > top_limit:
        return top_limit
    elif input_ < bottom_limit:
        return bottom_limit
    else:
        return input_

def interpolate(independent_list, dependent_list, independent_value):

    for x in independent_list:
        if independent_value <= x:
            pass
            return 0

def limitByRate(input_, output, target_rate, dt):

    rate = (input_ - output) / dt

    rate = limit(rate, target_rate, -target_rate)

    output += rate * dt

    return output

