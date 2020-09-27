import numpy
# Capacity list will be a list of capacities, e.g. [72, 46, 23]
# and value list will be a list of particular values, e.g. [36, 12, 17]
# and converts it to an integer using the base system
def intMapper(capacity_list, value_list):
    value = 0
    list_convert = [1]
    list_convert.extend(c + 1 for c in capacity_list)
    list_products = list_convert.copy()
    for i in range(1, len(list_products)):
        list_products[i] = list_products[i]*list_products[i-1]
    for i in range(len(capacity_list)):
        value += value_list[i]*list_products[i]
    return value
