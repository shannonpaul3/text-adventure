#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import csv

#### ====================================================================================================================== ####
#############                                          CSV_LOADER                                                  #############
#### ====================================================================================================================== ####

def csv_loader(filename, readall=False):
    ''' Helper function that reads in a CSV file. Optional flag for including header row.
    Input: filename (string), bool_flag (optional)
    Output: List of Rows (comma separated)
    '''
    return_list = []
    with open(filename) as csvfile:
        for row in csv.reader(csvfile):
            return_list.append(row)
    if readall:
        return return_list
    else:
        return return_list[1:]