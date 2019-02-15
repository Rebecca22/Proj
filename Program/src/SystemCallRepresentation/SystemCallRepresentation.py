__author__ = "Rebecca Merriman"
from JsonFiles import ReadFromJsonFiles

"""
    This class produces a list and returns it depending on the type of syscall behaviour being 
    represented ie syscall and ioctl, syscall with binder semantics, composite behaviours and 
    ioctl or composite behaviour and binder semantics.
"""

syscalls = []  # stores all the names of the system call or ioctl calls in a list for each family
allSystemCallNames = dict()  # stores every system/ioctl call key observed for each family where
# each key = the number of the family
syscallsPerFamily = {}  # stores the names of the system calls or ioctl calls per family
idPerSample = []  # contains the id of the samples
allIds = []  # contains the ids of all the samples per family
syscallsPerFile = []  # contains syscalls of all the samples per family
allIdFamily = {}  # stores ids of files per family


def getSystemCallRepresentation(typeSyscall):
    """
        Method should return the list of all syscalls seen in the json files in each family. It
        should distinguish between the type of behaviour to represent. If the type = "b" or "f"
        it should represent the behaviours as syscalls and ioctl, if the type = "bb" or "fb" it
        should represent the behaviours as syscalls with binder semantics, if the type = "bc" or
        "fc" it should represent the behaviours as composite behaviours with ioctl and if the
        type = "bbc" or "fbc" it should represent the behaviours as composite behaviours with
        binder semantics.
        :param typeSyscall: refers to the type of behaviour of the system call ie. syscalls and
        ioctl calls, syscalls and binder semantics, composite behaviours and ioctl or composite
        behaviours and binder semantics.
        :return: list of all syscalls seen in the json files in each family
    """

    global syscalls, syscallsPerFamily, allSystemCallNames, allIds, syscallsPerFile
    syscalls = []
    ReadFromJsonFiles.readJsonFile()
    familiesDictionary = ReadFromJsonFiles.getFamiliesDictionary()
    numOfFamilies = ReadFromJsonFiles.getNumberOfFamilies()
    numOfFiles = ReadFromJsonFiles.getNumOfFilesDictionary()

    # checks all traces in every family and adds any syscalls or ioctl names (via type) to a list
    for family in range(0, numOfFamilies):
        syscallsPerFamily = {}
        allIds = []
        # loops for the number of json files in the current family
        for listIndex in range(0, (numOfFiles[family])):
            dictionary = familiesDictionary[family][listIndex]['behaviors']['dynamic']['host']
            dictionaryLen = len(dictionary)
            syscallsPerFile = []
            # loops through the traces in each file in the current family
            for index in range(0, dictionaryLen):

                if typeSyscall == "b" or typeSyscall == "f":
                    # if trace has type syscall
                    # add all syscalls to list
                    # loop through the list add the name of the syscall to the list
                    # if it isnt a syscall
                    # add the name ioctl to the list
                    if dictionary[index]['low'][0]['type'] == 'SYSCALL':
                        list1 = dictionary[index]['low']
                        for index2 in range(0, len(list1)):
                            key = dictionary[index]['low'][index2]["sysname"]
                            syscalls.append(key)
                            syscallsPerFile.append(key)
                    else:
                        key = "ioctl"
                        syscalls.append(key)
                        syscallsPerFile.append(key)

                elif typeSyscall == "bb" or typeSyscall == "fb":
                    # if trace has type syscall
                    # add all syscalls to list
                    # loop through the list add the name of the syscall to the list
                    # if it isnt a syscall
                    # if it is a BINDER or INTENT transaction, make the key the method_name
                    # add the name ioctl to the list
                    if dictionary[index]['low'][0]['type'] == 'SYSCALL':
                        list1 = dictionary[index]['low']
                        for index2 in range(0, len(list1)):
                            key = dictionary[index]['low'][index2]["sysname"]
                            syscalls.append(key)
                            syscallsPerFile.append(key)
                    else:
                        key = dictionary[index]['low'][0]['type']
                        if key == 'BINDER':
                            key = dictionary[index]['low'][0]['method_name']
                        elif key == 'INTENT':
                            key = dictionary[index]['low'][0]['intent']
                        syscalls.append(key)
                        syscallsPerFile.append(key)

                elif typeSyscall == "bc" or typeSyscall == "fc":
                    # if trace has class type FS ACCESS
                    # add the name of the class FS ACCESS, to the list
                    # if trace has class type NETWORK ACCESS
                    # add the name of the class NETWORK ACCESS, to the list
                    # if trace has type syscall
                    # add all syscalls to list
                    # loop through the list and add the name of the syscall to the list
                    # if it isnt a syscall
                    # add the name ioctl to the list
                    if dictionary[index]['class'] == 'FS ACCESS':
                        key = dictionary[index]['class']
                        syscalls.append(key)
                        syscallsPerFile.append(key)
                    elif dictionary[index]['class'] == 'NETWORK ACCESS':
                        key = dictionary[index]['class']
                        syscalls.append(key)
                        syscallsPerFile.append(key)
                    elif dictionary[index]['low'][0]['type'] == 'SYSCALL':
                        list1 = dictionary[index]['low']
                        for index2 in range(0, len(list1)):
                            key = dictionary[index]['low'][index2]["sysname"]
                            syscalls.append(key)
                            syscallsPerFile.append(key)
                    else:
                        key = "ioctl"
                        syscalls.append(key)
                        syscallsPerFile.append(key)

                else:
                    # if trace has class type FS ACCESS
                    # add the name of the class FS ACCESS, to the list
                    # if trace has class type NETWORK ACCESS
                    # add the name of the class NETWORK ACCESS, to the list
                    # if trace has type syscall
                    # add all syscalls to list
                    # loop through the list and add the name of the syscall to the list
                    # if it is a BINDER or INTENT transaction, make the key the method_name
                    # add the name ioctl to the list
                    if dictionary[index]['class'] == 'FS ACCESS':
                        key = dictionary[index]['class']
                        syscalls.append(key)
                        syscallsPerFile.append(key)
                    elif dictionary[index]['class'] == 'NETWORK ACCESS':
                        key = dictionary[index]['class']
                        syscalls.append(key)
                        syscallsPerFile.append(key)
                    elif dictionary[index]['low'][0]['type'] == 'SYSCALL':
                        list1 = dictionary[index]['low']
                        for index2 in range(0, len(list1)):
                            key = dictionary[index]['low'][index2]["sysname"]
                            syscalls.append(key)
                            syscallsPerFile.append(key)
                    else:
                        key = dictionary[index]['low'][0]['type']
                        if key == 'BINDER':
                            key = dictionary[index]['low'][0]['method_name']
                        elif key == 'INTENT':
                            key = dictionary[index]['low'][0]['intent']
                        syscalls.append(key)
                        syscallsPerFile.append(key)

            # add the id of the sample to a list
            allIds.append(familiesDictionary[family][listIndex]['md5'])
            # add all system calls observed per file a list
            syscallsPerFamily[listIndex] = syscallsPerFile
        # add all ids per json file per family to a dictionary
        allIdFamily[family] = allIds
        # add all system calls observed per file per family to a dictionary
        allSystemCallNames[family] = syscallsPerFamily
    return syscalls


def getAllSystemCallNames():
    """
        Method should return the dictionary of all the system call names
        :return: the dictionary allSystemCallNames
    """
    global allSystemCallNames
    return allSystemCallNames


def getAllSamplesIds():
    """
        Method should return the dictionary of all the id's of each file in each family
        :return: dictionary of all the id's of each file in each family
    """
    global allIdFamily
    return allIdFamily
