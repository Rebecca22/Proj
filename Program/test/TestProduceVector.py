__author__ = "Rebecca Merriman"
import unittest
from numpy.testing import assert_array_equal
from src.ProduceVector import ProduceVector
import numpy as np
from src.SystemCallRepresentation import SystemCallRepresentation


class TestProduceVector(unittest.TestCase):
    """
        This class is the Unit Test class for the ProduceVector class.
    """

    # Tests
    # Test 9 tests getVector() and setVector(vector) in the class ProduceVector.
    # Test 11-15 test produceVector() in the class ProduceVector. Starting off with bit
    # uni-grams followed by frequency uni-grams and finishing off with frequency and bit di-grams
    # and tri_grams.
    # Test 22 tests setExpectedVector(expectedVec) and getExpectedVector() in the class
    # ProduceVector.

    def testGetAndSetVector(self):
        """
         Test 9
            This method tests setVector(vector) function in the ProduceVector class.
            To pass the test, the method should set the vector to the value specified here using
            setVector(vector) and getVector() should return it.
            Changes: Instead of the method returning a variable or a vector, it should return the
            global variable vector set by setVector(vector).
            :param self: reference to the current instance of the class
        """
        ProduceVector.setVector([1, 0, 1, 0])
        self.assertEqual(ProduceVector.getVector(), [1, 0, 1, 0], "Test 9: Test getVector "
                                                                  "and setVector ")

    def testProduceVector(self):
        """
         Test 11
            This method tests produceVector() function in the ProduceVector class.
            To pass the test, the method should produce a vector containing all the
            system calls as keys and then set the value of each key to 1 if the system call is
            present in the first family if not set the key to 0.
            :param self: reference to the current instance of the class
        """

        test = [[1, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0]]
        vec = np.array(test)
        ProduceVector.produceVector("uni", "b")
        actualVector = ProduceVector.getVector()
        vector = [actualVector[0], actualVector[1]]
        assert_array_equal(vector, vec, "Test 11: Test ProduceVector ")

    def testProduceVectorFreqAndBit(self):
        """
         Test 13
            This method tests produceVector() function in the ProduceVector class.
            To pass the test, the method should produce a dictionary containing all the
            system calls as keys and if the behaviour passed in is a bit vector
            then set the value of each key to 1 if the system call is present in the all the
            families if not set the key to 0 or if the type passed in is a frequency vector,
            set the value of each key to 1 if the key isnt in the dictionary otherwise increment
            the value of the key by 1.
            Changes: added frequency vector into class so that the value of each key will be set to
            1 if the key isnt in the dictionary otherwise it will be incremented by 1.
            :param self: reference to the current instance of the class
        """
        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("b")
        for i in range(0, len(syscalls)):
            key = "%s" % (syscalls[i])
            dictionary[key] = 0
        dictionaries = {}

        allSystemCallNames = SystemCallRepresentation.getAllSystemCallNames()
        allIdFamily = SystemCallRepresentation.getAllSamplesIds()

        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls)):
                    key = "%s" % (listSyscalls[i])
                    dictionary[key] = 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                for keys in dictionary.keys():
                    dictionary[keys] = 0

        test = dictionaries.values()
        vec = np.array(test)
        ProduceVector.produceVector("uni", "b")
        assert_array_equal(ProduceVector.getVector(), vec, "Test 13: Test "
                                                           "ProduceVector for Bit "
                                                           "vector ")
        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("f")
        for i in range(0, len(syscalls)):
            key = "%s" % (syscalls[i])
            dictionary[key] = 0

        dictionaries = {}

        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls)):
                    key = "%s" % (listSyscalls[i])
                    dictionary[key] += 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                for keys in dictionary.keys():
                    dictionary[keys] = 0

        test = dictionaries.values()
        vec = np.array(test)
        ProduceVector.produceVector("uni", "f")
        assert_array_equal(ProduceVector.getVector(), vec, "Test 13: Test "
                                                           "ProduceVector for freq "
                                                           "vector ")

    def testProduceVectorDiGrams(self):
        """
         Test 14
            This method tests produceVector() function in the ProduceVector class.
            To pass the test, the method should produce a dictionary containing all the
            system calls as keys. If the type passed in is a uni-gram, then it should
            produce the keys and a vector for the uni-gram and if it is a di-gram, then it should
            produce the keys and a vector for the di-gram. If the behaviour passed in is a bit
            vector then set the value of each key to 1 if the system call is present in the all the
            families if not set the key to 0 or if the type passed in is a frequency vector,
            set the value of each key to 1 if the key isnt in the dictionary otherwise increment
            the value of the key by 1.
            Changes: added if statement for the produce vector to determine between a uni-gram
            and a di-gram.
            :param self: reference to the current instance of the class
        """
        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("b")
        for i in range(0, len(syscalls)-1):
            key = "%s  %s" % (syscalls[i], syscalls[i+1])
            dictionary[key] = 0
        dictionaries = {}

        allSystemCallNames = SystemCallRepresentation.getAllSystemCallNames()
        allIdFamily = SystemCallRepresentation.getAllSamplesIds()

        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls)-1):
                    key = "%s  %s" % (listSyscalls[i], listSyscalls[i+1])
                    dictionary[key] = 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                dictionary = dictionary.fromkeys(dictionary.keys(), 0)

        test = dictionaries.values()
        vec = np.array(test)
        ProduceVector.produceVector("di", "b")

        assert_array_equal(ProduceVector.getVector(), vec, "Test 14: Test "
                                                           "ProduceVector for Bit "
                                                           "di-gram vector ")

        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("f")
        for i in range(0, len(syscalls)-1):
            key = "%s  %s" % (syscalls[i], syscalls[i+1])
            dictionary[key] = 0

        dictionaries = {}
        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls) - 1):
                    j = i + 1
                    key = "%s  %s" % (listSyscalls[i], listSyscalls[j])
                    dictionary[key] += 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                dictionary = dictionary.fromkeys(dictionary.keys(), 0)

        test = dictionaries.values()
        vec = np.array(test)
        ProduceVector.produceVector("di", "f")
        assert_array_equal(ProduceVector.getVector(), vec, "Test 14: Test "
                                                           "ProduceVector for freq "
                                                           "di-gram vector ")

    def testProduceVectorTriGrams(self):
        """
         Test 15
            This method tests produceVector() function in the ProduceVector class.
            To pass the test, the method should produce a dictionary containing all the
            system calls as keys. If the type passed in is a uni-gram, then it should
            produce the keys and a vector for the uni-gram, if it is a di-gram, then it should
            produce the keys and a vector for the di-gram and if it is a tri-gram, then it should
            produce the keys and a vector for the tri-gram. If the behaviour passed in is a bit
            vector then set the value of each key to 1 if the system call is present in the all the
            families if not set the key to 0 or if the type passed in is a frequency vector,
            set the value of each key to 1 if the key isnt in the dictionary otherwise increment
            the value of the key by 1.
            Changes: added if statement for the produce vector to determine between a uni-gram,
            a di-gram and a tri-gram.
            :param self: reference to the current instance of the class
        """
        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("b")
        for i in range(0, len(syscalls)-2):
            key = "%s  %s  %s" % (syscalls[i], syscalls[i+1],  syscalls[i+2])
            dictionary[key] = 0
        dictionaries = {}

        allSystemCallNames = SystemCallRepresentation.getAllSystemCallNames()
        allIdFamily = SystemCallRepresentation.getAllSamplesIds()

        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls)-2):
                    key = "%s  %s  %s" % (listSyscalls[i], listSyscalls[i+1], listSyscalls[i+2])
                    dictionary[key] = 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                dictionary = dictionary.fromkeys(dictionary.keys(), 0)

        test = dictionaries.values()
        vec = np.array(test)

        ProduceVector.produceVector("tri", "b")
        assert_array_equal(ProduceVector.getVector(), vec, "Test 15: Test "
                                                           "ProduceVector for Bit "
                                                           "tri-gram vector ")
        dictionary = {}
        syscalls = SystemCallRepresentation.getSystemCallRepresentation("f")
        for i in range(0, len(syscalls)-2):
            key = "%s  %s  %s" % (syscalls[i], syscalls[i+1], syscalls[i+2])
            dictionary[key] = 0

        dictionaries = {}
        for sample in range(0, len(allSystemCallNames)):
            for k in range(0, len(allSystemCallNames[sample])):
                listSyscalls = allSystemCallNames[sample][k]
                listIds = allIdFamily[sample][k]
                for i in range(0, len(listSyscalls) - 2):
                    j = i + 1
                    m = i + 2
                    key = "%s  %s  %s" % (listSyscalls[i], listSyscalls[j], listSyscalls[m])
                    dictionary[key] += 1
                fileName = listIds
                dictionaries[fileName] = dictionary.values()
                dictionary = dictionary.fromkeys(dictionary.keys(), 0)

        test = dictionaries.values()
        vec = np.array(test)
        ProduceVector.produceVector("tri", "f")
        assert_array_equal(ProduceVector.getVector(), vec, "Test 15: Test "
                                                           "ProduceVector for freq "
                                                           "tri-gram vector ")

    def testGetSetExpectedVector(self):
        """
         Test 22
            This method tests setExpectedVector(expectedVec) and getExpectedVector() functions in
            the ProduceVector class.
            To pass the test, the method should set the value to the value specified here using
            setExpectedVector(expectedVec) and getExpectedVector() should return it.
            Changes: Added code in produceVector(typeVector, behaviour) method to set the value
            of expectedVector.
            :param self: reference to the current instance of the class
        """
        ProduceVector.setExpectedVector([1, 0, 1, 0])
        self.assertEqual(ProduceVector.getExpectedVector(), [1, 0, 1, 0], "Test 22: Test "
                                                                          "getExpectedVector "
                                                                          "and setExpectedVector")


if __name__ == '__main__':
    unittest.main()
