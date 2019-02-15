__author__ = "Rebecca Merriman"
import unittest
from src.HierarchicalClustering import HierarchicalClustering

class TestValidation(unittest.TestCase):
    """
        This class is the Unit Test class for the TestValidation class.
    """
    def testEvaluate(self):
        """
         Test 21
            This method tests evaluate(matrix) function in the Validation class.
            To pass the test, the method should return best clustering using the
            fowlkes_mallows_score and the number of the cut from the matrix passed in.
            Changes: Instead of returning an integer or a cut of a matrix for a given
            number of clusters, it should return the labelsTrue list (list of true assignments of
            the dataset. This loops through the matrix returned from the cut_tree function (an
            array where z[i] indicates the cluster number that it is assigned to e.g. any row
            with a 0 in it are in the same cluster and any with a 1 is in the same cluster etc).
            Added into produceVector the expectedVector Dictionary. This dictionary will store
            the actual true vector assignments of samples to families in the dataset. Added
            getters and setters for this dictionary and so added a test for this in
            TestProduceVector. Added labelsPred list which stores the assignments of clusterings by
            the cut of the dendogram. Added code to calculate the true positives, false positives,
            true negatives and false negatives and then compute the fowlkes_mallows_score.
            Changed it to instead of hard coding the number of clusters to split the data up into (
            parameter 2 in cut function), I created a loop to calculate the
            fowlkes_mallows_score for all cuts of the dendogram and store the scores in a list
            and return the list. Finally, the function was changed to return the best clustering
            from the list of values and not the list of fowlkes_mallows_score values. Changed
            main, test 22 in TestHierarchicalClustering and Hierarchical Clustering to validate
            after producing the dendogram. Changed it to calculate the adjusted rand index score
            and then return the best clustering for both the fowlkes_mallows_score and adjusted
            rand index. Changed main, test 22 in TestHierarchicalClustering and Hierarchical
            Clustering to incorporate this change. Changed it to calculate the silhouette
            coefficient score and then return the best clustering for all 3 evaluation metrics.
            Changed main, test 22 in TestHierarchicalClustering and Hierarchical Clustering to
            incorporate this change. Added F1 score to the test class.
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

        self.assertEqual(bestClustering, bestCluster, "Test 21: Test evaluate")


if __name__ == '__main__':
    unittest.main()
