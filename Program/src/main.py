__author__ = "Rebecca Merriman"
from src.HierarchicalClustering import HierarchicalClustering
import cPickle as pickle

"""
    Depending on what the user types into the program, this class will either run experiments for 
    each type of vector (uni-gram bit vector, uni-gram frequency vector, di-gram bit vector, 
    di-gram frequency vector, tri-gram bit vector or tri-gram frequency vector) and for each type 
    of behaviour (syscalls and ioctls, syscalls and binder semantics, composite behaviours and 
    ioctls or composite behaviours and binder semantics)and works out the best clustering according
    to FMS, F1, ARI and SC, runs one experiment for one type of vector and system call 
    representation and works out the best clustering according to FMS, F1, ARI and SC or calculated 
    the best clustering according to FMS, F1, ARI and SC from the stored lists of the scores at the 
    various heights.
"""


def main():

    bestCluster = dict()
    maxFMSScore = 0
    maxF1Score = 0
    maxARIScore = 0
    maxSCScore = 0

    import sys
    print("What would you like to execute?\n Please type 'all' if you want to run all the "
          "experiments\n please type 'best cluster' if you want to find the best cluster\n "
          "please type 'one' if you would like to run a single experiment\n and "
          "then press enter (without the quote marks)")
    answer = (sys.stdin.readline())

    if answer == "one\n":

        # is the user wants to only run one experiment, find out wich feature vector to generate
        print("What vector would you like to execute?\n Please type 'uni' for uni-grams, 'di' for "
              "di-grams and 'tri' for tri-grams\n and then press enter (without the quote marks)")
        nGram = (sys.stdin.readline())
        vec = ""
        syscall = ""

        if nGram == "uni\n":
            print(
                "What type of vector?\n Please type 'b' for a bit vector or 'f' for a "
                "frequency vector\n and then press enter (without the quote marks)")
            vec = (sys.stdin.readline())

            if vec == "b\n" or vec == "f\n":

                print(
                    "What type of system call representation?\n Please type 'n' for syscalls and "
                    "ioctls\n 'b' for syscalls and binder semantics\n 'c' for composite behaviours"
                    " and ioctls\n or bc' for composite behaviours and binder semantics\n and then "
                    "press enter(without the quote marks)")
                syscall = (sys.stdin.readline())
            else:
                print "You have entered an incorrect input"
                exit(0)

        elif nGram == "di\n":

            print(
                "What type of vector?\n Please type 'b' for a bit vector or 'f' for a "
                "frequency vector\n and then press enter (without the quote marks)")
            vec = (sys.stdin.readline())

            if vec == "b\n" or vec == "f\n":

                print(
                    "What type of system call representation?\n Please type 'n' for syscalls and "
                    "ioctls\n 'b' for syscalls and binder semantics\n 'c' for composite behaviours"
                    " and ioctls\n or bc' for composite behaviours and binder semantics\n and then "
                    "press enter(without the quote marks)")
                syscall = (sys.stdin.readline())
            else:
                print "You have entered an incorrect input"
                exit(0)

        elif nGram == "tri\n":

            print(
                "What type of vector?\n Please type 'b' for a bit vector or 'f' for a "
                "frequency vector\n and then press enter (without the quote marks)")
            vec = (sys.stdin.readline())

            if vec == "b\n" or vec == "f\n":

                print(
                    "What type of system call representation?\n Please type 'n' for syscalls and "
                    "ioctls\n 'b' for syscalls and binder semantics\n 'c' for composite behaviours"
                    " and ioctls\n or bc' for composite behaviours and binder semantics\n and then "
                    "press enter(without the quote marks)")
                syscall = (sys.stdin.readline())
            else:
                print "You have entered an incorrect input"
                exit(0)

        else:
            print "You have entered an incorrect input"
            exit(0)

        if syscall == "n\n" or syscall == "b\n" or syscall == "c\n" or syscall == "bc\n":

            nGram, temp = nGram.split("\n")
            vec, temp = vec.split("\n")
            syscall, temp = syscall.split("\n")

            if syscall == "n":
                syscall = ""

            behaviour = vec+syscall

            # run the experiment for the feature vector the user wanted
            HierarchicalClustering.Clustering(typeVector=nGram, behaviour=behaviour)

            if behaviour == "b":
                nGram += " bit"
            if behaviour == "f":
                nGram += " freq"
            if behaviour == "bb":
                nGram += " bit binder"
            if nGram == "fb":
                nGram += " freq binder"
            if behaviour == "bc":
                nGram += " bit composite"
            if behaviour == "fc":
                nGram += " frequency composite"
            if behaviour == "bbc":
                nGram += " bit binder composite"
            if behaviour == "fbc":
                nGram += " frequency binder composite"

            # determine the best SC, FMS, F1 and ARI scores
            bestCluster[nGram] = (HierarchicalClustering.getBestCluster())

            print("The best clusters according to the FMS, F1, ARI and SC scores are")

            clustersFMS = []
            clustersF1 = []
            clustersARI = []
            clustersSC = []

            cluster = bestCluster.values()[0]
            clustFMSScore = cluster[0][0]
            clustF1Score = cluster[1][0]
            clustARIScore = cluster[2][0]
            clustSCScore = cluster[3][0]
            clustersFMS.append((bestCluster.keys(), "at height", cluster[0][1]))
            clustersF1.append((bestCluster.keys(), "at height", cluster[1][1]))
            clustersARI.append((bestCluster.keys(), "at height", cluster[2][1]))
            clustersSC.append((bestCluster.keys(), "at height", cluster[3][1]))

            print clustersFMS, "with FMS score", clustFMSScore
            print clustersF1, "with F1 score", clustF1Score
            print clustersARI, "with ARI score", clustARIScore
            print clustersSC, "with SC score", clustSCScore
        else:
            print "You have entered an incorrect input"
            exit(0)

    elif answer == "all\n":

        # uni-gram
        # bit vector with syscalls and ioctls
        print("Running experiment for Uni-gram bit vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="b")
        bestCluster["uni bit"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and ioctls
        print("Running experiment for Uni-gram frequency vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="f")
        bestCluster["uni freq"] = (HierarchicalClustering.getBestCluster())
        # bit vector with syscalls and binder semantics
        print("Running experiment for Uni-gram bit vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="bb")
        bestCluster["uni bit binder"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and binder semantics
        print("Running experiment for Uni-gram frequency vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="fb")
        bestCluster["uni freq binder"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and ioctls
        print("Running experiment for Uni-gram bit vector with composite behaviours and ioclts")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="bc")
        bestCluster["uni bit composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and ioctls
        print("Running experiment for Uni-gram frequency vector with composite behaviours and"
              "ioclts")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="fc")
        bestCluster["uni freq composite"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and binder semantics
        print("Running experiment for Uni-gram bit vector with composite behaviours and binder "
              "semantics")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="bbc")
        bestCluster["uni bit binder composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and binder semantics
        print("Running experiment for Uni-gram frequency vector with composite behaviours and"
              " binder semantics")
        HierarchicalClustering.Clustering(typeVector="uni", behaviour="fbc")
        bestCluster["uni freq binder composite"] = (HierarchicalClustering.getBestCluster())

        # di-gram
        # bit vector with syscalls and ioctls
        print("Running experiment for Di-gram bit vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="b")
        bestCluster["di bit"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and ioctls
        print("Running experiment for Di-gram frequency vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="f")
        bestCluster["di freq"] = (HierarchicalClustering.getBestCluster())
        # bit vector with syscalls and binder semantics
        print("Running experiment for Di-gram bit vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="bb")
        bestCluster["di bit binder"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and binder semantics
        print("Running experiment for Di-gram frequency vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="fb")
        bestCluster["di freq binder"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and ioctls
        print("Running experiment for Di-gram bit vector with composite behaviours and ioclts")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="bc")
        bestCluster["di bit composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and ioctls
        print(
            "Running experiment for Di-gram frequency vector with composite behaviours and ioclts")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="fc")
        bestCluster["di freq composite"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and binder semantics
        print("Running experiment for Di-gram bit vector with composite behaviours and binder "
              "semantics")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="bbc")
        bestCluster["di bit binder composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and binder semantics
        print(
            "Running experiment for Di-gram frequency vector with composite behaviours and binder "
            "semantics")
        HierarchicalClustering.Clustering(typeVector="di", behaviour="fbc")
        bestCluster["di freq binder composite"] = (HierarchicalClustering.getBestCluster())

        # tri-gram
        # bit vector with syscalls and ioctls
        print("Running experiment for Tri-gram bit vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="b")
        bestCluster["tri bit"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and ioctls
        print("Running experiment for Tri-gram frequency vector with syscalls and ioclts")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="f")
        bestCluster["tri freq"] = (HierarchicalClustering.getBestCluster())
        # bit vector with syscalls and binder semantics
        print("Running experiment for Tri-gram bit vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="bb")
        bestCluster["tri bit binder"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with syscalls and binder semantics
        print("Running experiment for Tri-gram frequency vector with syscalls and binder semantics")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="fb")
        bestCluster["tri freq binder"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and ioctls
        print("Running experiment for Tri-gram bit vector with composite behaviours and ioclts")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="bc")
        bestCluster["tri bit composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and ioctls
        print("Running experiment for Tri-gram frequency vector with composite behaviours and"
              "ioclts")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="fc")
        bestCluster["tri freq composite"] = (HierarchicalClustering.getBestCluster())
        # bit vector with composite behaviours and binder semantics
        print("Running experiment for Tri-gram bit vector with composite behaviours and binder "
              "semantics")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="bbc")
        bestCluster["tri bit binder composite"] = (HierarchicalClustering.getBestCluster())
        # frequency vector with composite behaviours and binder semantics
        print("Running experiment for Tri-gram frequency vector with composite behaviours and"
              " binder semantics")
        HierarchicalClustering.Clustering(typeVector="tri", behaviour="fbc")
        bestCluster["tri freq binder composite"] = (HierarchicalClustering.getBestCluster())

        print("The best clusters according to the FMS, F1, ARI and SC scores are")
        for index in range(0, len(bestCluster)):
            cluster = bestCluster.values()[index]
            clustFMSScore = cluster[0][0]
            clustF1Score = cluster[1][0]
            clustARIScore = cluster[2][0]
            clustSCScore = cluster[3][0]
            if maxFMSScore < clustFMSScore:
                maxFMSScore = clustFMSScore
            if maxF1Score < clustF1Score:
                maxF1Score = clustF1Score
            if maxARIScore < clustARIScore:
                maxARIScore = clustARIScore
            if maxSCScore < clustSCScore:
                maxSCScore = clustSCScore

        clustersFMS = []
        clustersF1 = []
        clustersARI = []
        clustersSC = []

        for index in range(0, len(bestCluster)):
            cluster = bestCluster.values()[index]
            clustFMSScore = cluster[0][0]
            clustF1Score = cluster[1][0]
            clustARIScore = cluster[2][0]
            clustSCScore = cluster[3][0]
            if clustFMSScore == maxFMSScore:
                clustersFMS.append((bestCluster.keys()[index], "at height", cluster[0][1]))
            if clustF1Score == maxF1Score:
                clustersF1.append((bestCluster.keys()[index], "at height", cluster[1][1]))
            if clustARIScore == maxARIScore:
                clustersARI.append((bestCluster.keys()[index], "at height", cluster[2][1]))
            if clustSCScore == maxSCScore:
                clustersSC.append((bestCluster.keys()[index], "at height", cluster[3][1]))

        print clustersFMS, "with FMS score", maxFMSScore
        print clustersF1, "with F1 score", maxF1Score
        print clustersARI, "with ARI score", maxARIScore
        print clustersSC, "with SC score", maxSCScore

    elif answer == "best cluster\n":

        from glob import glob
        import os.path

        fmsList = []
        f1List = []
        ariList = []
        scList = []
        heights = []

        # naviagte through the lists directory, through the different types of feature vectors
        # and system call representations

        print("Getting all the FMS, F1, ARI and SC scores for each vector")

        pattern = os.path.join('../lists', '*')
        for file_name in glob(pattern):
            pattern2 = os.path.join(file_name, '*')
            for file_name2 in glob(pattern2):
                pattern3 = os.path.join(file_name2, '*')

                for file_name3 in glob(pattern3):

                    # for each heights pickle file, store the heights in a list

                    pattern4 = os.path.join(file_name3, 'heights.p')
                    for file_name4 in glob(pattern4):
                        heights = pickle.load(open(file_name4, "rb"))

                    # for each FMS pickle file, store the scores in a list

                    pattern4 = os.path.join(file_name3, 'FMS.p')
                    for file_name4 in glob(pattern4):
                        fmsList = pickle.load(open(file_name4, "rb"))

                    # for each F1 pickle file, store the scores in a list

                    pattern4 = os.path.join(file_name3, 'F1.p')
                    for file_name4 in glob(pattern4):
                        f1List = pickle.load(open(file_name4, "rb"))

                    # for each ARI pickle file, store the scores in a list

                    pattern4 = os.path.join(file_name3, 'ARI.p')
                    for file_name4 in glob(pattern4):
                        ariList = pickle.load(open(file_name4, "rb"))

                    # for each SC pickle file, store the scores in a list

                    pattern4 = os.path.join(file_name3, 'SC.p')
                    for file_name4 in glob(pattern4):
                        scList = pickle.load(open(file_name4, "rb"))

                    # calculate the highest FMS, F1 SC and ARI score for the vector
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

                    delimiter = r"\'"
                    symbol, data = delimiter.split("'")

                    temp = file_name3.split(symbol)
                    graphKey = temp[1] + " " + temp[2] + "\n" + temp[3]
                    key = temp[1] + " " + temp[2] + " " + temp[3]

                    bestCluster[key] = bestClustering

                    # display the validation graphs for each type of feature vector
                    from src.Validation import Validation
                    Validation.scoreGraphs(fmsList, f1List, ariList, scList, heights, graphKey)

        print("The best clusters according to the FMS, F1, ARI and SC scores are")
        for index in range(0, len(bestCluster)):
            cluster = bestCluster.values()[index]
            clustFMSScore = cluster[0][0]
            clustF1Score = cluster[1][0]
            clustARIScore = cluster[2][0]
            clustSCScore = cluster[3][0]
            if maxFMSScore < clustFMSScore:
                maxFMSScore = clustFMSScore
            if maxF1Score < clustF1Score:
                maxF1Score = clustF1Score
            if maxARIScore < clustARIScore:
                maxARIScore = clustARIScore
            if maxSCScore < clustSCScore:
                maxSCScore = clustSCScore

        clustersFMS = []
        clustersF1 = []
        clustersARI = []
        clustersSC = []

        for index in range(0, len(bestCluster)):
            cluster = bestCluster.values()[index]
            clustFMSScore = cluster[0][0]
            clustF1Score = cluster[1][0]
            clustARIScore = cluster[2][0]
            clustSCScore = cluster[3][0]
            if clustFMSScore == maxFMSScore:
                clustersFMS.append((bestCluster.keys()[index], "at height", cluster[0][1]))
            if clustF1Score == maxF1Score:
                clustersF1.append((bestCluster.keys()[index], "at height", cluster[1][1]))
            if clustARIScore == maxARIScore:
                clustersARI.append((bestCluster.keys()[index], "at height", cluster[2][1]))
            if clustSCScore == maxSCScore:
                clustersSC.append((bestCluster.keys()[index], "at height", cluster[3][1]))

        print clustersFMS, "with FMS score", maxFMSScore
        print clustersF1, "with F1 score", maxF1Score
        print clustersARI, "with ARI score", maxARIScore
        print clustersSC, "with SC score", maxSCScore

    else:
        print "You have entered an incorrect input"
        exit(0)


if __name__ == '__main__':
    main()
