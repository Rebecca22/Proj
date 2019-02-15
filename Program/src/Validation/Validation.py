__author__ = "Rebecca Merriman"
from scipy.cluster.hierarchy import cut_tree
from src.ProduceVector import ProduceVector
from sklearn import metrics
from matplotlib import pyplot as plt
import numpy as np
"""
    This class evaluates the cuts on the dendogram at different heights using metrics by finding 
    the best clustering for the matrix passed in. 
"""


def evaluate(matrix, vector, type):
    """
        Method should cut the dendogram from the matrix passed in up to the number of json files
        and then for each dendogram cut it should calculate the fowlkes_mallows_score, adjusted
        rand index score and silhouette coefficient score and store the highest score in a variable.
        Once all cuts are evaluated, it returns the best cut number and the fowlkes_mallows_score,
        the best cut number and F1 score, the best cut number and adjusted rand index score and the
        best cut number and the silhouette coefficient.
        :param matrix: the matrix to cut and then evaluate each cut
        :param vector: the numpy array of all the feature vectors
        :param type: the type of vector to validate
        :return: the best cut number and the fowlkes_mallows_score for that cut, the best cut
        number, f1 score for that cut and the best cut number adjusted rand index score for that
        cut and the best cut number and silhouette coefficient for that cut.
    """
    funcMatrix = matrix
    expectedVectors = ProduceVector.getExpectedVector()

    print("Validating the clusters obtained")

    # the actual true assignments in the dataset (ie. json files split up into families = what
    # is expected) made into a list of cluster assignments
    # where the number = the cluster number it is assigned to
    labelsTrue = []
    length = len(expectedVectors)
    for index in range(0, length):
        listFamily = expectedVectors[index]
        # for all the json files in the family, add the number of the family to the list
        for listVec in listFamily:
            labelsTrue.append(index)

    fowlkesMallowsScoreList = []
    adjRandIndexList = []
    f1ScoreList = []
    silhouetteList = []
    lengthMatrix = len(funcMatrix)
    heights = []

    # stores all heights in a list (removed set as did not retain ordering)
    for cutNum in range(1, lengthMatrix):
        cutHeight = funcMatrix[cutNum][2]  # gets third column of linkage matrix (height of merge)
        if cutHeight not in heights:
            heights.append(cutHeight)
    print "The number of different heights are = ", len(heights)

    count = 0  # to get index of set
    for heightDendogram in heights:
        count += 1

        # Given a linkage matrix z and the height to cut the dendogram at
        # (cut = cut_tree(z, height)) return the cut tree = array where z[i] indicates the
        # cluster number that it is assigned to e.g. any row with a 0 in it are in the same
        # cluster and any with a 1 is in the same cluster etc.
        # meaning any row with the same number are allocated to the same cluster
        cut = cut_tree(funcMatrix, height=heightDendogram)  # cuts the dendogram at the cut height

        # the assignments of clusterings by the cut of the dendogram
        # made into a list of cluster assignments
        # where the number = the cluster number it is assigned to
        # converts the cut list to integers and returns the list
        labelsPred = map(int, cut)

        # calculates the FMS score between the true labels and the predictive labels and stores
        # the score in a list
        fowlkesMallowsScore = metrics.fowlkes_mallows_score(labelsTrue, labelsPred)
        fowlkesMallowsScoreList.append(fowlkesMallowsScore)

        # calculates the f1 score between the true labels and the predictive labels and stores
        # the score in a list
        f1Score = metrics.f1_score(labelsTrue, labelsPred, average = 'micro')
        f1ScoreList.append(f1Score)

        # calculates the ARI score between the true labels and the predictive labels and stores
        # the score in a list
        adjRandIndex = metrics.adjusted_rand_score(labelsTrue, labelsPred)
        adjRandIndexList.append(adjRandIndex)

        # calculates the SC score between the feature array and the predictive labels and stores
        # the score in a list
        if count != 1:
            silhouette = metrics.silhouette_score(vector, labelsPred, metric='euclidean')
        else:
            silhouette = -1

        silhouetteList.append(silhouette)

    # update the pickle files with the updated lists
    nGram, syscallRep = type.split()

    # set up the paths for the files
    nGram = nGram + r"-gram\'"

    temp, temp2 = nGram.split("'")
    nGram = temp

    if syscallRep == "b":
        nGram += "Syscalls and Ioctls\Bit Vector"
    if syscallRep == "f":
        nGram += "Syscalls and Ioctls\Frequency Vector"
    if syscallRep == "bb":
        nGram += "Syscalls and Binder Semantics\Bit Vector"
    if syscallRep == "fb":
        nGram += "Syscalls and Binder Semantics\Frequency Vector"
    if syscallRep == "bc":
        nGram += "Composite Behaviours and Ioctls\Bit Vector"
    if syscallRep == "fc":
        nGram += "Composite Behaviours and Ioctls\Frequency Vector"
    if syscallRep == "bbc":
        nGram += "Composite Behaviours and Binder Semantics\Bit Vector"
    if syscallRep == "fbc":
        nGram += "Composite Behaviours and Binder Semantics\Frequency Vector"

    path = r"..\lists\'"
    temp, path2 = path.split("'")
    path = temp
    path += nGram

    import cPickle as pickle
    # use cPickle instead of pickle to speed up pickle access

    # depending on the file in the directory, update the correct one with the information

    fileName = path + "\heights.p"

    pickle.dump(heights, open(fileName, "wb"))

    fileName = path + r"\FMS.p"

    pickle.dump(fowlkesMallowsScoreList, open(fileName, "wb"))

    fileName = path + r"\F1.p"

    pickle.dump(f1ScoreList, open(fileName, "wb"))

    fileName = path + r"\ARI.p"

    pickle.dump(adjRandIndexList, open(fileName, "wb"))

    fileName = path + r"\SC.p"

    pickle.dump(silhouetteList, open(fileName, "wb"))

    # calculates the highest scores from the list and determines the height at which the the highest
    # scores from the list was obtained
    bestClusteringFMS = min(fowlkesMallowsScoreList, key=lambda x: abs(x - 1.0))
    FMS = fowlkesMallowsScoreList.index(bestClusteringFMS)
    cutNumFMS = heights[FMS]
    bestClusteringF1 = min(f1ScoreList, key=lambda x: abs(x - 1.0))
    F1 = f1ScoreList.index(bestClusteringF1)
    cutNumF1 = heights[F1]
    bestClusteringARI = min(adjRandIndexList, key=lambda x: abs(x - 1.0))
    ARI = adjRandIndexList.index(bestClusteringARI)
    cutNumARI = heights[ARI]
    bestClusteringSC = min(silhouetteList, key=lambda x: abs(x - 1.0))
    SC = silhouetteList.index(bestClusteringSC)
    cutNumSC = heights[SC]

    bestClustering = ((bestClusteringFMS, cutNumFMS), (bestClusteringF1, cutNumF1),
                      (bestClusteringARI, cutNumARI), (bestClusteringSC, cutNumSC))

    vectorRep, syscall = type.split()

    if syscall == "b":
        vectorRep += " bit"
    if syscall == "f":
        vectorRep += " freq"
    if syscall == "bb":
        vectorRep += " bit binder"
    if vectorRep == "fb":
        vectorRep += " freq binder"
    if syscall == "bc":
        vectorRep += " bit composite"
    if syscall == "fc":
        vectorRep += " frequency composite"
    if syscall == "bbc":
        vectorRep += " bit binder composite"
    if syscall == "fbc":
        vectorRep += " frequency binder composite"

    scoreGraphs(fowlkesMallowsScoreList, f1ScoreList, adjRandIndexList, silhouetteList, heights,
                vectorRep)

    return bestClustering


def scoreGraphs(fowlkesMallowsScoreList, f1ScoreList, adjRandIndexList, silhouetteList, heights,
                type):
    """
        Method creates 4 line graphs showing the FMS, F1, ARI and SC scores at each height.
        Used https://matplotlib.org/gallery/subplots_axes_and_figures/shared_axis_demo.html
        #sphx-glr-gallery-subplots-axes-and-figures-shared-axis-demo-py

    :param fowlkesMallowsScoreList: a list of the FMS scores at each height
    :param f1ScoreList: a list of the f1 scores at each height
    :param adjRandIndexList: a list of the ARI scores at each height
    :param silhouetteList: a list of the SC scores at each height
    :param heights: a list of all the dengogram heights
    :param type: the type of system call and vector representation
    """

    N = len(fowlkesMallowsScoreList)
    ind = np.arange(N)
    width = 0

    t = np.arange(N)
    s1 = fowlkesMallowsScoreList
    s2 = f1ScoreList
    s3 = adjRandIndexList
    s4 = silhouetteList
    heights = list(heights)

    # sets up the x axis labels by converting the heights into a tuple
    labelsTuple = tuple(heights)

    # sets up the FMS graph by adding the y axis labels, x axis markers, plotting the points and
    # x axis labels
    ax1 = plt.subplot(411)
    ax1.set_ylabel('FMS Scores')
    ax1.set_xticks(ind + width / 2)
    ax1.set_title(type + ' FMS, F1, ARI and SC scores for each Height')  # title of graphs
    plt.plot(t, s1, '-o', ms=8, lw=2, alpha=0.7, mfc='orange')
    plt.setp(ax1.set_xticklabels(labelsTuple), fontsize=6)

    # sets up the f1 graph by adding the y axis labels, x axis markers, plotting the points and
    # x axis labels
    ax2 = plt.subplot(412)
    ax2.set_ylabel('F1 Scores')
    ax2.set_xticks(ind + width / 2)
    plt.plot(t, s2, '-o', ms=8, lw=2, alpha=0.7, mfc='orange')
    plt.setp(ax2.set_xticklabels(labelsTuple), fontsize=6)

    # sets up the ARI graph by adding the y axis labels, x axis markers, plotting the points and
    # x axis labels
    ax3 = plt.subplot(413)
    ax3.set_ylabel('ARI Scores')
    ax3.set_xticks(ind + width / 2)
    plt.plot(t, s3, '-o', ms=8, lw=2, alpha=0.7, mfc='orange')
    plt.setp(ax3.set_xticklabels(labelsTuple), fontsize=6)

    # sets up the SC graph by adding the y axis labels, x axis markers, plotting the points and
    # x axis labels
    ax4 = plt.subplot(414)
    ax4.set_ylabel('SC Scores')
    ax4.set_xticks(ind + width / 2)
    plt.plot(t, s4, '-o', ms=8, lw=2, alpha=0.7, mfc='orange')
    plt.setp(ax4.set_xticklabels(labelsTuple), fontsize=6)
    plt.show()
