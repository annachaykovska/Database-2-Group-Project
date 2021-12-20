import random
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
        return oneOneCount/(zeroOneCount + oneZeroCount + oneOneCount)
    # where arraylist is an n-dimensional list on the number of students data we are using.
    # each list is a binary list as to whether or not the student has taken a course or not
    # clusters = k for k means (# of clusters to divide into)  
    def k_means(self,arrayList):
        #Steps:
        # Set up cluster variables
        k1 = []
        k2 = []
        k3 = []
        k4 = []
        k5 = []
        # using clusters number, pick random seeds from ArrayList as starting points for clusters
        numStudents = len(arrayList)
        #print(numStudents)
        seed = (int)(random.random() * numStudents)
        seed2 = (int)(random.random() * numStudents)
        seed3 = (int)(random.random() * numStudents)
        seed4 = (int)(random.random() * numStudents)
        seed5= (int)(random.random() * numStudents)
        k1 = arrayList[seed]
        print(seed)
        if seed2 == seed:
            while seed2 == seed:
                seed2 = (int)(random.random() * numStudents)
        k2 = arrayList[seed2]
        print(seed2)
        if seed3 == seed or seed3 == seed2:
                while seed3 == seed or seed3 == seed2:
                    seed3 = (int)(random.random() * numStudents)
        k3 = arrayList[seed3]
        print(seed3)
        if seed4 == seed3 or seed4 == seed2 or seed4 == seed:
                while seed4 == seed3 or seed4 == seed2 or seed4 == seed:
                    seed4 = (int)(random.random() * numStudents)
        k4 = arrayList[seed4]
        print(seed4)
        if seed5 == seed3 or seed5 == seed4 or seed5 == seed2 or seed5 == seed:
                while seed5 == seed3 or seed5 == seed4 or seed5 == seed2 or seed5 == seed:
                    seed5 = (int)(random.random() * numStudents)
        k5 = arrayList[seed5]
        print(seed5)
        #for a in k1:
            #print(a)
        #for a in k2:
        #    print(a)
        #for a in k3:
        #    print(a)
        #for a in k4:
        #    print(a)
        #for a in k5:
        #    print(a)
        # list of floats containing similarity between cluster and every student
        k1sim = []
        k2sim = []
        k3sim = []
        k4sim = []
        k5sim = []

        #list of cluster each student currently belongs to 
        currentcluster = [0] * numStudents

        #list of cluster each student had in the previous round
        lastcluster = []
       
        #round start
        while currentcluster != lastcluster:
            print("HEY")
            lastcluster = currentcluster.copy()
            for student in arrayList:
                position = arrayList.index(student)
                # using the seeds, calculate Jaccard index between every non-seed array in ArrayList
                c1 = self.similarity(k1,student)
                c2 = self.similarity(k2,student)
                c3 = self.similarity(k3,student)
                c4 = self.similarity(k4,student)
                c5 = self.similarity(k5,student)
                # group Arrays in Array into their nearest cluster
                closeMatch = max(c1,c2,c3,c4,c5)

                if closeMatch == c1:
                    currentcluster[position] = 1
                elif closeMatch == c2:
                    currentcluster[position] = 2
                elif closeMatch == c3:
                    currentcluster[position] = 3
                elif closeMatch == c4:
                    currentcluster[position] = 4
                elif closeMatch == c5:
                    currentcluster[position] = 5
            
            #for a in currentcluster:
            #    print(a)
            # Take new average seed vector using rounding to keep arrays as 0's and 1's
            numClasses = len(arrayList[0])
            k1 = [0] * numClasses
            k2 = [0] * numClasses
            k3 = [0] * numClasses
            k4 = [0] * numClasses
            k5 = [0] * numClasses
            k1size = 0
            k2size = 0
            k3size = 0
            k4size = 0
            k5size = 0
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
                elif belongsTo == 4:
                    k4size +=1
                    for index in range(0,numClasses):
                        k4[index] += student[index] 
                elif belongsTo == 5:
                    k5size +=1
                    for index in range(0,numClasses):
                        k5[index] += student[index] 

            #Calculate next round if something belongs to the cluster
            #for b in k5:
            #    print(b)
            if k1size > 0:
                k1 = [round(num/k1size) for num in k1]
            if k2size > 0:
                k2 = [round(num/k2size) for num in k2]
            if k3size > 0:
                k3 = [round(num/k3size) for num in k3]
            if k4size > 0:
                k4 = [round(num/k4size) for num in k4] 
            if k5size > 0:
                k5 = [round(num/k5size) for num in k5]
            #print(currentcluster)
            
        return k1, k2, k3, k4, k5    

testArr3 = [[1,0,0],[1,1,1],[1,0,1],[1,1,0],[0,1,1],[0,1,0]]
jc = Jaccard()
print(jc.k_means(testArr3))
    #print(similarity(testArr,testArr2))

