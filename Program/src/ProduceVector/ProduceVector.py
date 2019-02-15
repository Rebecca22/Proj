__author__ = "Rebecca Merriman"
from src.SystemCallRepresentation import SystemCallRepresentation
import numpy as np

"""
    This class produces a vector depending if it is a bit vector, frequency vector or 
    n-gram and returns it.
"""
vector = 0
expectedVectors = {}


def getVector():
    """
        Method should return the vector
        :return: the vector called vector
    """
    global vector
    return vector


def setVector(vec):
    """
        Method should set the vector to the value passed in.
        :param vec: set the global parameter vector to vec
    """
    global vector
    vector = vec


def produceVector(typeVector, behaviour):
    """
        Method should produce the vector according to the type (uni = uni-gram, d = di-gram
        vector and t = tri-gram vector).
        :param typeVector: refers to the type of vector ie. uni-gram (1-gram), di-gram (2-gram) or
        tri-gram (3-gram)
        :param behaviour: refers to the type of behaviour of the system call ie. syscalls and ioctl
        calls, syscalls and binder semantics, composite behaviours and ioctl or composite
        behaviours and binder semantics.
    """
    global vector, expectedVectors
    expectedVectors = {}
    systemCallDictionary = {}  # stores every system/ioctl call for each family

    systemCallsRep = SystemCallRepresentation.getSystemCallRepresentation(behaviour)

    print("Producing the feature vectors")

    # set up keys for dictionary
    systemCallDictionary = setUpKeys(systemCallsRep, typeVector, systemCallDictionary)

    allSystemCallsDictionary = dict()  # stores every system/ioctl call for each family

    allSysCalls = SystemCallRepresentation.getAllSystemCallNames()
    syscallsLength = len(allSysCalls)
    allIdFamily = SystemCallRepresentation.getAllSamplesIds()

    # loops for all the samples, sets up the key in the dictionary according to uni-gram,
    # di-gram or tri-gram and then sets the value at the key to 1 if it is a bit vector or
    # increments the value at the key to 0 if it is a frequency vector
    for sample in range(0, syscallsLength):
        expectedVectors[sample] = list()
        sampleLen = len(allSysCalls[sample])
        for listIndex in range(0, sampleLen):
            listSyscalls = allSysCalls[sample][listIndex]
            listIds = allIdFamily[sample][listIndex]

            length = len(listSyscalls)
            if typeVector == "di":
                length -= 1
            if typeVector == "tri":
                length -= 2

            # setting up the key in the dictionary
            for index in range(0, length):
                if typeVector == "uni":
                    # set the key to the system call at the corresponding index of the list to a
                    # uni-gram
                    key = "%s" % (listSyscalls[index])
                elif typeVector == "di":
                    # set nextKey to the next system call in the list
                    # concatenate the next system call in the list to the previous system call
                    # set the key to the system call at the corresponding index of the list to a
                    # di-gram
                    nextIndex = index + 1
                    nextKey = listSyscalls[nextIndex]
                    key = "%s  %s" % (listSyscalls[index], nextKey)
                else:
                    # set nextKey to the next system call in the list
                    # set nextKey2 to the next system call in the list after nextKey
                    # concatenate the next system call and the one after that in
                    # the list to the name of the previous system call
                    # set the key to the system call at the corresponding index of the list to a
                    # tri-gram
                    nextIndex = index + 1
                    followingIndex = index + 2
                    nextKey = listSyscalls[nextIndex]
                    nextKey2 = listSyscalls[followingIndex]
                    key = "%s  %s  %s" % (listSyscalls[index], nextKey, nextKey2)

                # setting up the value of the key in the dictionary
                # if it is a bit vector set the key calculated above to 1
                if (behaviour == "b") or (behaviour == "bb") or (behaviour == "bc") or (behaviour
                                                                                        == "bbc"):
                    systemCallDictionary[key] = 1
                else:
                    # otherwise it is a frequency vector increment the value by 1
                    systemCallDictionary[key] += 1

            # adds the dictionary containing the vector of system calls per file per family to
            # the dictionary containing the vector of system calls for all json files
            fileName = listIds
            allSystemCallsDictionary[fileName] = systemCallDictionary.values()
            expectedVectors[sample].append(systemCallDictionary.values())

            # sets all keys in dictionary to 0
            systemCallDictionary = systemCallDictionary.fromkeys(systemCallDictionary.keys(), 0)
    # convert to numpy array
    setVector(np.array(allSystemCallsDictionary.values()))
    setExpectedVector(expectedVectors)
    shape = int(vector.shape[1])

    print "The number of system call dimensions is:", shape


def getExpectedVector():
    """
        Method should return the expectedVectors dictionary
        :return: the dictionary called expectedVectors
    """
    global expectedVectors
    return expectedVectors


def setExpectedVector(expectedVec):
    """
        Method should set the expectedVectorDictionary to the value passed in.
        :param expectedVec: set the expectedVectorDictionary to expectedVec
    """
    global expectedVectors
    expectedVectors = expectedVec


def setUpKeys(systemCallsRep, typeVector, systemCallDictionary):
    """
        Method should set up the keys in the systemCallDictionary depending on the type of vector
        passed in.
        :param systemCallsRep the system call representation from getSystemCallRepresentation in
        the SystemCallRepresentation class
        :param typeVector: refers to the type of vector ie. uni-gram (1-gram), di-gram (2-gram) or
        tri-gram (3-gram)
        :param systemCallDictionary stores every system/ioctl call for each family
        :return the dictionary containing the keys in the systemCallDictionary depending on the
        type of vector passed in.
    """
    # creates all the keys for the uni-gram, di-gram or tri-gram
    # loops for the all the json files in all the families and adds all keys to dictionary
    systemCallsRepLength = len(systemCallsRep)
    if typeVector == "uni":
        # add the keys to the dictionary and set the value as 0
        systemCallDictionary = systemCallDictionary.fromkeys(systemCallsRep, 0)
    elif typeVector == "di":
        for index in range(0, systemCallsRepLength):
            # set nextKey to the next system call in the list
            # concatenate the name of the next system call in the list to the
            # name of the previous system call
            # add the key to the dictionary and set the value as 0
            nextKey = index + 1
            # make sure that the index does not go out of the range of the list
            if nextKey < systemCallsRepLength:
                key = "%s  %s" % (systemCallsRep[index], systemCallsRep[nextKey])
                systemCallDictionary[key] = 0
    else:
        # set nextKey to the next system call in the list
        # set nextKey2 to the next system call in the list after nextKey
        # concatenate the name of the next system call and the one after that in
        # the list to the name of the previous system call
        # add the key to the dictionary and set the value as 0
        for index in range(0, systemCallsRepLength):
            nextIndex = index + 1
            followingIndex = index + 2
            length = systemCallsRepLength
            if followingIndex < length:
                key = "%s  %s  %s" % (systemCallsRep[index], systemCallsRep[nextIndex],
                                      systemCallsRep[followingIndex])
                systemCallDictionary[key] = 0
    return systemCallDictionary
