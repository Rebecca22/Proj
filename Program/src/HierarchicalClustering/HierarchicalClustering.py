__author__ = "Rebecca Merriman"
from sklearn import preprocessing
from scipy.cluster.hierarchy import linkage, dendrogram
from src.ProduceVector import ProduceVector
from src.Validation import Validation
from matplotlib import pyplot as plt

"""
    This class standardises the feature vectors if it receives a frequency vector, calculates the 
    euclidean distances of each of the feature vectors and then validates the clusters produced 
    by the dendograms.
    used https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
"""

euclideanDistance = 0
standardisation = 0
bestCluster = 0


def getEuclideanDistance():
    """
        Method should return a euclidean distance matrix of the vector
        :return the Euclidean Distance linkage matrix of the vector
    """
    global euclideanDistance
    return euclideanDistance


def calculateEuclideanDistance(vector):
    """
        Method should calculate the euclidean distance of the vector
        :param vector: refers to the vector that will be transformed into a linkage matrix
        of euclidean distances
    """
    global euclideanDistance
    # create linkage matrix with the distance metric as euclidean distance
    # calculate the distances of the clusters by starting as singletons
    # and in each iteration will merge the two clusters which have the smallest distance
    # returns array of length n - 1
    # Z[i] will tell us which clusters were merged in the i-th iteration
    # each row has format [cluster1, cluster1, dist, sample_count].
    euclideanDistance = linkage(vector, metric='euclidean')


def getStandardisation():
    """
        Method should return a standardisation matrix of the vector
        :return the standardisation matrix of the vector
    """
    global standardisation
    return standardisation


def calculateStandardisation(vector):
    """
        Method should standardise the feature vector
        :param vector: refers to the vector that will be standardised
        # from http://sebastianraschka.com/Articles/2014_about_feature_scaling.html
    """
    global standardisation
    # from http://sebastianraschka.com/Articles/2014_about_feature_scaling.htm
    std_scale = preprocessing.StandardScaler().fit(vector)
    standardisation = std_scale.transform(vector)


def Clustering(typeVector, behaviour):
    """
        Method should standardise the vector if the vector is a frequency vector, calculate the
        euclidean distance of the vectors and produce a dendogram.
        :param typeVector: refers to the type of vector ie. uni-gram (1-gram), di-gram (2-gram) or
        tri-gram (3-gram)
        :param behaviour: refers to the type of behaviour of the system call ie. syscalls anf ioctl
        calls, syscalls and binder semantics, composite behaviours and ioctls or composite
        behaviours and binder semantics
    """
    ProduceVector.produceVector(typeVector, behaviour)
    vector = ProduceVector.getVector()
    if (behaviour == "f") or (behaviour == "fb") or (behaviour == "fc") or (behaviour == "fbc"):
        calculateStandardisation(vector)
        vector = getStandardisation()
    calculateEuclideanDistance(vector)

    print("Producing a dendrogram")

    # produce a dendogram
    # a tree showing the order and distances of merges during the hierarchical clustering
    # x axis = indices of samples in the vector
    # y axis = euclidean distances
    # Height = the distance at which this cluster merged into another cluster.
    # Huge jumps/gaps indicate that clusters were merged that are not similar
    # ie they don't belong to the same cluster.
    plt.figure(figsize=(10, 5))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Malware Family Number')
    plt.ylabel('Euclidean Distance')
    dendrogram(getEuclideanDistance())
    plt.show()

    typeOfVector = typeVector + " " + behaviour
    setBestCluster(Validation.evaluate(getEuclideanDistance(), vector, typeOfVector))


def getBestCluster():
    """
        Method should return the bestCluster of the matrix passed in to the evaluate method in
        the validation class
        :return the bestCluster
    """
    global bestCluster
    return bestCluster


def setBestCluster(cluster):
    """
        Method should set the bestCluster variable to the values passed in
        :param cluster: the score and number of clusters of the best clustering
    """
    global bestCluster
    bestCluster = cluster
