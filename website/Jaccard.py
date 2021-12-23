import random
import numpy
class Jaccard:
    #Where arr1 and arr2 are binary arrays of equal length
    def similarity(self,arr1, arr2):
        #input checking
        if len(arr1) != len(arr2):
            print("Error, Arrays are of different lengths")
            return 
        if(arr1[0] != 0 and arr1[0] != 1 or arr2[0] != 0 and arr2[0] != 1):
            print("Error, non-binary arrays detected")
            return

        #Calculations
        zeroOneCount = 0
        oneZeroCount = 0
        zeroZeroCount = 0
        oneOneCount = 0
        i = 0
        while(i < len(arr1)):
            if(arr1[i] == 0 and arr2[i] == 0):
                zeroZeroCount = zeroZeroCount +1
            elif (arr1[i] == 0 and arr2[i] == 1):
                zeroOneCount = zeroOneCount +1
            elif (arr1[i] == 1 and arr2[i] == 1):
                oneOneCount = oneOneCount +1
            elif (arr1[i] == 1 and arr2[i] == 0):
                oneZeroCount = oneZeroCount +1
            i = i+1
        try:
             return oneOneCount/(zeroOneCount + oneZeroCount + oneOneCount)
        except ZeroDivisionError:
            print("One or more lists has no values to compare to")

        
    # where arraylist is an n-dimensional list on the number of students data we are using.
    # each list is a binary list as to whether or not the student has taken a course or not
    # clusters = k for k means (# of clusters to divide into)  
    def k_means(self,arrayList):
        #Steps:
        # Set up cluster variables
        k1 = []
        k2 = []
        k3 = []
        # using clusters number, pick random seeds from ArrayList as starting points for clusters
        numStudents = len(arrayList)
        #print(numStudents)
        seed = (int)(random.random() * numStudents)
        seed2 = (int)(random.random() * numStudents)
        seed3 = (int)(random.random() * numStudents)
        k1 = arrayList[seed]
        #print(seed)
        if self.similarity(arrayList[seed2],k1) != 0:
            while self.similarity(arrayList[seed2],k1) != 0:
                seed2 = (int)(random.random() * numStudents)
        k2 = arrayList[seed2]
        #print(seed2)
        if self.similarity(arrayList[seed3],k2) != 0 or self.similarity(arrayList[seed3],k1) != 0:
            while self.similarity(arrayList[seed3],k2) != 0 or self.similarity(arrayList[seed3],k1) != 0:
                seed3 = (int)(random.random() * numStudents)
        k3 = arrayList[seed3]
        #for a in k1:
        #    print(a)
        #for a in k2:
        #    print(a)
        #for a in k3:
        #    print(a)
        #for a in k4:
        #    print(a)
        #for a in k5:
        #    print(a)
        # list of floats containing similarity between cluster and every student


        #list of cluster each student currently belongs to 
        currentcluster = [0] * numStudents

        #list of cluster each student had in the previous round
        lastcluster = []
       
        #round start
        while currentcluster != lastcluster:
            lastcluster = currentcluster.copy()
            for student in arrayList:
                position = arrayList.index(student)
                # using the seeds, calculate Jaccard index between every non-seed array in ArrayList
                c1 = self.similarity(k1,student)
                c2 = self.similarity(k2,student)
                c3 = self.similarity(k3,student)
                if c1 is None or c2 is None or c3 is None:
                    print("one or more students has not taken any classes. Cannot make comparison")
                    return
                # group Arrays in Array into their nearest cluster
                closeMatch = max(c1,c2,c3)

                if closeMatch == c1:
                    currentcluster[position] = 1
                elif closeMatch == c2:
                    currentcluster[position] = 2
                elif closeMatch == c3:
                    currentcluster[position] = 3
            
            #for a in currentcluster:
            #    print(a)
            # Take new average seed vector using rounding to keep arrays as 0's and 1's
            numClasses = len(arrayList[0])
            k1 = [0] * numClasses
            k2 = [0] * numClasses
            k3 = [0] * numClasses
            k1size = 0
            k2size = 0
            k3size = 0
            for student in arrayList:
                number = arrayList.index(student)
                belongsTo = currentcluster[number]
                if belongsTo == 1:
                    k1size +=1
                    for index in range(0,numClasses):
                        k1[index] += student[index] 
                elif belongsTo == 2:
                    k2size +=1
                    for index in range(0,numClasses):
                        k2[index] += student[index] 
                elif belongsTo == 3:
                    k3size +=1
                    for index in range(0,numClasses):
                        k3[index] += student[index] 
            #Calculate next round if something belongs to the cluster
            #for b in k5:
            #    print(b)
            if k1size > 0:
                k1 = [round(num/k1size) for num in k1]
            if k2size > 0:
                k2 = [round(num/k2size) for num in k2]
            if k3size > 0:
                k3 = [round(num/k3size) for num in k3]
            #print(currentcluster)
            
        #return numpy.array([k1, k2, k3]) 
        return [k1, k2, k3]  

jc = Jaccard()
    #print(similarity(testArr,testArr2))

