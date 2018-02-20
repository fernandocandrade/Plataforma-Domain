def convert(par):
    """ convert par from string to the correct type. """
    if par.isnumeric():
        return int(par)

    if par.replace(".", "").isnumeric():
        return float(par)

    return par
