__author__ = "Rebecca Merriman"
import unittest
import json
from glob import glob
import os.path
from src.JsonFiles import ReadFromJsonFiles


class TestReadFromJsonFiles(unittest.TestCase):
    """
        This class is the Unit Test class for the ReadFromJsonFiles class.
    """

    @classmethod
    def setUpClass(cls):
        ReadFromJsonFiles.readJsonFile()  # store the contents of each file in one family
        #  into a list and then stores the list in a dictionary

    # Tests
    # Test 1 tests the getter getJsonFiles function in the class ReadFromJsonFiles
    # Tests 2, 3, 4 and 5 test the readJsonFile and getJsonFile functions in the class
    # ReadFromJsonFiles
    # Tests 6, 7 and 8 test the getters getFamiliesDictionary(), getNumOfFilesDictionary() and
    # getNumberOfFamilies() in the class ReadFromJsonFiles

    def testGetJsonFiles(self):
        """
         Test 1
         This method tests getJsonFiles() function in the ReadFromJsonFiles class.
         To pass the test, the method getJsonFiles() should return the list data from the
         class ReadFromJsonFiles.
         Changes: I changed the return statement to instead of returning a string or a string set
         in the class or a list the method should return the global list variable called data in
         the class.
         :param self: reference to the current instance of the class
        """
        self.assertEqual(ReadFromJsonFiles.getJsonFiles(), ReadFromJsonFiles.data, "Test 1: Test"
                                                                                   "getJson Files")

    def testReadJsonFile(self):
        """
            Test 2, 3, 4 and 5
             This method tests readJsonFile() function in the ReadFromJsonFiles class.
             To pass the test, the method readJsonFile() should get the contents of all the json
             files from all the samples in the samples directory and add it to the list and then
             add that list to a dictionary when all the files in the family have been dealt with.
             Changes: I changed the code in readJsonFile so that instead of storing "hi" in the
             global list data or the file name of the first file in the list or all the file names
             of the first family or the names of all the sample directories in the list or the
             names of all json files in all the directories, or the contents of the first file
             name in the first directory in the list or the contents of all the json files of
             every family, it will store the contents for each family (sub directory in samples
             folder) will be stored in a list and then once all the files in one family have been
             dealt with, then the list is stored in the dictionary with the key being the directory
             number in the samples directory and the value is the list.
            :param self: reference to the current instance of the class
        """

        value = ReadFromJsonFiles.familiesDictionary  # store the contents all file names for
        # each family in the dictionary where the key = family number and value = list of the
        # contents of the file

        numberOfFamilies = ReadFromJsonFiles.numberOfFamilies
        # expectedNumberOfFamilies = 2
        expectedNumberOfFamilies = 49

        self.assertEqual(numberOfFamilies, expectedNumberOfFamilies, "Test 3: Test readJsonFile")

        expectedValue = {}
        numberOfFamilies = 0
        numOfFilesDictionary = {}
        pattern = os.path.join('../samples', '*')
        for file_name in glob(pattern):
            data = []
            count = 0
            pattern2 = os.path.join(file_name, '*.json')
            for name in glob(pattern2):
                with open(name) as f:
                    data.append(json.load(f))
                    count += 1
                    f.close()
            numOfFilesDictionary[numberOfFamilies] = count
            expectedValue[numberOfFamilies] = data
            numberOfFamilies += 1

        self.assertEqual(value, expectedValue, "Test 4: Test readJsonFile")
        self.assertEqual(len(value), len(expectedValue), "Test 5: Test readJsonFile")

    def testGetters(self):
        """
            Test 6, 7 and 8
            This method tests getFamiliesDictionary(), getNumOfFilesDictionary() and
            getNumberOfFamilies().
            To pass the test, the all the getters should return their expected values.
            :param self: reference to the current instance of the class
        """

        numberOfFamilies = 0
        numOfFilesDictionary = {}
        familiesDictionary = {}
        pattern = os.path.join('../samples', '*')
        for file_name in glob(pattern):
            data = []
            count = 0
            pattern2 = os.path.join(file_name, '*.json')
            for name in glob(pattern2):
                with open(name) as f:
                    data.append(json.load(f))
                    count += 1
                    f.close()
            numOfFilesDictionary[numberOfFamilies] = count
            familiesDictionary[numberOfFamilies] = data
            numberOfFamilies += 1

        self.assertEqual(ReadFromJsonFiles.getFamiliesDictionary(), familiesDictionary,
                         "Test 6: Test getFamiliesDictionary()")
        self.assertEqual(ReadFromJsonFiles.getNumOfFilesDictionary(), numOfFilesDictionary,
                         "Test 7: Test getNumOfFilesDictionary")
        self.assertEqual(ReadFromJsonFiles.getNumberOfFamilies(), numberOfFamilies,
                         "Test 8: Test getNumberOfFamilies")


if __name__ == '__main__':
    unittest.main()
