DATA_FIELDS = ('description', 'f', 'n')


def get_total(data):
    if 'n' in data:
        return data['n']
    else:
        return sum(get_total(child) for child in data.values()
                   if child not in DATA_FIELDS)
