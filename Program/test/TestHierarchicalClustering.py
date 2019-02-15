__author__ = "Rebecca Merriman"
import unittest
from src.ProduceVector import ProduceVector
from src.HierarchicalClustering import HierarchicalClustering
from sklearn import preprocessing
from scipy.cluster.hierarchy import linkage
import numpy as np


class TestHierarchicalClustering(unittest.TestCase):
    """
        This class is the Unit Test class for the HierarchicalClustering class.
    """
    test = ProduceVector.getVector()
    test2 = ProduceVector.getVector()

    @classmethod
    def setUpClass(cls):
        global test, test2
        ProduceVector.produceVector("uni", "b")
        test = ProduceVector.getVector()
        ProduceVector.produceVector("uni", "f")
        test2 = ProduceVector.getVector()

    # Tests
    # Test 16 tests the calculation of euclidean distances by the calculateEuclideanDistance() and
    # getEuclideanDistance() methods in the class HierarchicalClustering.
    # Test 17 tests the calculation of euclidean distances and producing a dendogram from this by
    # the clustering(), calculateEuclideanDistance() and getEuclideanDistance() methods in the
    # class HierarchicalClustering.
    # Test 18 tests the standardisations of vectors by the calculateStandardisation() and
    # getStandardisation() methods in the class HierarchicalClustering.
    # Test 19 tests the standardisation (if freq vector), calculation of euclidean distances and
    # producing a dendogram from this by the clustering(), calculateEuclideanDistance(),
    # getEuclideanDistance(), calculateStandardisation() and getStandardisation() methods in the
    # class HierarchicalClustering.
    # Test 22 tests the hierarchical clustering (clustering()) and validation classes (evaluate()).

    def testEuclidean(self):
        """
         Test 16
            This method tests Clustering(), calculateEuclideanDistance() and getEuclideanDistance()
            functions in the HierarchicalClustering class.
            To pass the test, the method should calculate the euclidean distances of the feature
            vectors and then produce a dendogram.
            Changes: Made the Clustering() method call the calculateEuclideanDistance() function
            on a vector from the getVector method in the ProduceVector class.
           :param self: reference to the current instance of the class
        """
        vector = linkage(test, metric='euclidean')

        HierarchicalClustering.Clustering(typeVector="uni", behaviour="b")

        np.testing.assert_array_equal(HierarchicalClustering.getEuclideanDistance(), vector,
                                      "Test 16: Test Euclidean")

    def testEuclideanAndDendogram(self):
        """
         Test 17
            This method tests Clustering(), calculateEuclideanDistance() and getEuclideanDistance()
            functions in the HierarchicalClustering class.
            To pass the test, the method should calculate the euclidean distances of the feature
            vectors and then produce a dendogram.
            Changes: Made the Clustering() method call the calculateEuclideanDistance() function
            on a vector from the getVector method in the ProduceVector class. Added some code to
            produce a dendogram into the clustering function.
           :param self: reference to the current instance of the class
        """

        vector = linkage(test, metric='euclidean')

        HierarchicalClustering.Clustering(typeVector="uni", behaviour="b")

        np.testing.assert_array_equal(HierarchicalClustering.getEuclideanDistance(), vector,
                                      "Test 17: Test Euclidean and Dendogram")

    def testStandardisation(self):
        """
         Test 18
            This method tests calculateStandardisation() and getStandardisation()
            functions in the HierarchicalClustering class.
            To pass the test, the method should standardise the feature vectors.
           :param self: reference to the current instance of the class
        """

        std_scale = preprocessing.StandardScaler().fit(test2)
        vector = std_scale.transform(test2)

        HierarchicalClustering.calculateStandardisation(test2)

        np.testing.assert_array_equal(HierarchicalClustering.getStandardisation(), vector,
                                      "Test 18: Test Standardisation")

    def testHierarchicalClustering(self):
        """
         Test 19
            This method tests Clustering(), calculateEuclideanDistance(), getEuclideanDistance()
            calculateStandardisation() and getStandardisation() functions in the
            HierarchicalClustering class.
            To pass the test, the method should standardise the feature vectors only if the
            vector is a frequency vector and not a bit vector, calculate the euclidean distances
            of the feature vectors and then produce a dendogram.
           :param self: reference to the current instance of the class
        """

        vector = linkage(test, metric='euclidean')

        HierarchicalClustering.Clustering(typeVector="uni", behaviour="b")

        np.testing.assert_array_equal(HierarchicalClustering.getEuclideanDistance(), vector,
                                      "Test 19: Test Hierarchical Clustering")

        std_scale = preprocessing.StandardScaler().fit(test2)
        vector = std_scale.transform(test2)

        HierarchicalClustering.Clustering(typeVector="uni", behaviour="f")

        np.testing.assert_array_equal(HierarchicalClustering.getStandardisation(), vector,
                                      "Test 19: Test Hierarchical Clustering")

    def testHierarchicalClusteringAndValidation(self):
        """
         Test 22
            This method tests Clustering(), calculateEuclideanDistance(), getEuclideanDistance()
            calculateStandardisation() and getStandardisation() functions in the
            HierarchicalClustering class and evaluate(matrix) functions in the Validation class.
            To pass the test, the method should calculate the euclidean distances
            of the vector, produce a dendogram, cut the dendogram at the various cuts and find
            the best clustering using the fowlkes_mallows_score of the various cuts.
            Changes: Made the function Clustering() call the function evaluate() in Validation
            class. Added print statements in main to get the value returned as the best cluster.
            Added getBestCluster() and setBestCluster(score, clustNum) into Hierarchical
            Clustering and added test 23 into TestHierarchicalClustering.
            Changed it so it stored the best cluster for the cut and the score in a dictionary in
            main and then found the best one and only printed cut with the best
            fowlkes_mallows_score and the type of vector. Added the calculation of ARI and SC
            into the test class. Added F1 score to the test class.
           :param self: reference to the current instance of the class
        """
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="b")
        bestCluster = HierarchicalClustering.getBestCluster()

        import cPickle as pickle

        path = '../lists/uni-gram/Syscalls and Ioctls/Bit Vector'

        fileName = path + "\heights.p"
        heights = pickle.load(open(fileName, "rb"))

        fileName = path + "\FMS.p"
        fmsList = pickle.load(open(fileName, "rb"))

        fileName = path + "\F1.p"
        f1List = pickle.load(open(fileName, "rb"))

        fileName = path + "\ARI.p"
        ariList = pickle.load(open(fileName, "rb"))

        fileName = path + "\SC.p"
        scList = pickle.load(open(fileName, "rb"))

        bestClusteringFMS = min(fmsList, key=lambda x: abs(x - 1.0))
        FMS = fmsList.index(bestClusteringFMS)
        cutNumFMS = heights[FMS]
        bestClusteringF1 = min(f1List, key=lambda x: abs(x - 1.0))
        F1 = f1List.index(bestClusteringF1)
        cutNumF1 = heights[F1]
        bestClusteringARI = min(ariList, key=lambda x: abs(x - 1.0))
        ARI = ariList.index(bestClusteringARI)
        cutNumARI = heights[ARI]
        bestClusteringSC = min(scList, key=lambda x: abs(x - 1.0))
        SC = scList.index(bestClusteringSC)
        cutNumSC = heights[SC]

        bestClustering = (
            (bestClusteringFMS, cutNumFMS), (bestClusteringF1, cutNumF1),
            (bestClusteringARI, cutNumARI), (bestClusteringSC, cutNumSC))

        self.assertEqual(bestClustering, bestCluster,
                         "Test 22: Test Hierarchical clustering and Validation")


if __name__ == '__main__':
    unittest.main()
