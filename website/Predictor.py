import sqlite3
import numpy
import sys
import website.Jaccard
import re
from website.defaultDatabaseEntries import courseList, antireqList, prereqList, otherCoursesList
class Decoder:
    #this function decodes the recommended binary array and filters out pre-reqs/anti-reqs
    def filter(self,userClasses,recommendedClasses):
        #filter duplicates
        #print(recommendedClasses)
        filteredrecommendation = [0] * len(courseList)
        for num in range(0,len(courseList)):
            if userClasses[num] ==0 and recommendedClasses[num] ==1:
                #print(num)
                #filteredrecommendation[num] == 1 
                #check prereqs
                prereqs = list(prereqList[num].values())[1:]
                prereqs2 = []

                for val in prereqs:
                    prereqs2.append(val.split(","))
                setchecks = []
                coursecheck = -2
                #print(prereqs2)
                for val in prereqs2:
                    #print(val)
                    #ignore non CPSC classes
                    for val2 in val:
                        
                        if re.search("CPSC", val2) == None:
                            val.remove(val2)
                            if coursecheck == -2:
                                coursecheck = -1
                                continue
                            #remove weird digits
                        #print(val2)
                        tempVal = val2[0:7]
                        currentprereqindex = -1
                        for course in courseList:
                            if tempVal == course["CourseCode"]:
                                currentprereqindex = courseList.index(course)
                                break
                            #print(courseList[currentprereqindex])
                            #print(currentprereqindex)
                            #if tempVal == "CPSC355":
                                #print (coursecheck)
                                #print(userClasses[currentprereqindex] == 1)
                        if userClasses[currentprereqindex] == 1:
                            #print(courseList[currentprereqindex])
                            coursecheck = 1
                        if userClasses[currentprereqindex] == 0 and coursecheck !=1:
                            coursecheck = 0
                    if coursecheck == 1:
                        setchecks.append(1)
                        coursecheck = -2
                    elif coursecheck == 0: 
                        setchecks.append(0)
                        coursecheck = -2
                    else:
                        coursecheck = -2
                #print(setchecks)
                if all(setchecks) == True:
                    filteredrecommendation[num] = 1  
            #print(filteredrecommendation)         
            #print(filteredrecommendation[num])
                #check antireqs (only if all pre-reqs have been met)
            if filteredrecommendation[num] == 1:
                antireqs = list(antireqList[num].values())[1:]
                #print(antireqs)
                antireqs2 = []
                for val in antireqs:
                    antireqs2.append(val.split(","))
                setchecks = []
                coursecheck = -2
                #print(antireqs2)
                for val in antireqs2:
                    #print(val)
                    #ignore non CPSC classes
                    for val2 in val:
                        if re.search("CPSC", val2) == None:
                            val.remove(val2)
                            if coursecheck == -2:
                                coursecheck = -1
                                continue
                            #remove weird digits
                        #print(val2)
                        tempVal = val2[0:7]
                        currentantireqindex = -1
                        for course in courseList:
                            if tempVal == course["CourseCode"]:
                                currentantireqindex = courseList.index(course)
                                break
                            #print(courseList[currentprereqindex])
                            #print(currentprereqindex)
                            #if tempVal == "CPSC355":
                                #print (coursecheck)
                                #print(userClasses[currentprereqindex] == 1)
                        if userClasses[currentantireqindex] == 1:
                            #print(courseList[currentprereqindex])
                            coursecheck = 1
                        if userClasses[currentantireqindex] == 0 and coursecheck !=1:
                            coursecheck = 0
                    if coursecheck == 1:
                        setchecks.append(1)
                        coursecheck = -2
                    elif coursecheck == 0: 
                        setchecks.append(0)
                        coursecheck = -2
                    else:
                        coursecheck = -2
                #print(setchecks)
                if any(setchecks) == True:
                    filteredrecommendation[num] = 0 
        return filteredrecommendation
    def decode(self,inputClasses):
        classesString = []
        for num in range(0,len(courseList)):
            if inputClasses[num] == 1:
                classesString.append(courseList[num]["CourseCode"] + ": " + courseList[num]["Name"])
        return classesString
    def encode(self,inputClasses):
        encodedStudent = [0] * len(courseList)
        for input in inputClasses:
            classes = -1
            for course in courseList:
                if input == course["CourseCode"]:
                    classes = courseList.index(course)
                    break
            if classes != -1:
                encodedStudent[classes] = 1     
        return encodedStudent   
dc = Decoder()


class Predictor:
    def predict(userInput):
        con = sqlite3.connect('website/CourseDB.db')
        cur = con.cursor()
        s = []
        #index of s encodes which column the class should belong to in the encodedStudents list
        for row in cur.execute("SELECT DISTINCT identifier FROM courses_taken WHERE Course LIKE 'CPSC%' ORDER BY 'identifier'"):
            s.append(row[0])
        #print((len(courseList)))
        #print(len(s))
        encodedStudents = numpy.zeros((len(s), len(courseList)))
        count = 0
        for row in cur.execute("SELECT identifier,Course FROM courses_taken WHERE Course LIKE 'CPSC%' ORDER BY identifier"):
            count = count + 1
            student = s.index(row[0])
            classes = -1
            currentClass = row[1][0:7]
            for course in courseList:
                if currentClass == course["CourseCode"]:
                    classes = courseList.index(course)
                    break
            if classes != -1:
                encodedStudents[student][classes] = 1

        #with open('encodedStudents.txt', 'w') as f:
            #numpy.set_printoptions(threshold=sys.maxsize)
            #f.write(numpy.array_str(encodedStudents))
        
        #with open('recommendations.txt', 'w') as f:
            #numpy.set_printoptions(threshold=sys.maxsize)
            #f.write(Jaccard.jc.k_means(encodedStudents.tolist()))
        clustersList = website.Jaccard.jc.k_means(encodedStudents.tolist())
        c1 = clustersList[0]
        c2 = clustersList[1]
        c3 = clustersList[2]
        decoder = Decoder()
        #print(userInput)
        encodedInput =  decoder.encode(userInput)
        #print(encodedInput)
        # replace encodedStudents[0] with input list from db
        s1 = website.Jaccard.jc.similarity(encodedInput,clustersList[0])
        s2 = website.Jaccard.jc.similarity(encodedInput,clustersList[1])
        s3 = website.Jaccard.jc.similarity(encodedInput,clustersList[2])
        closeMatch = max(s1,s2,s3)
        finalrecommendation = []
        if closeMatch == s1:
            #print(clustersList[0])
            #print(dc.filter(encodedInput,clustersList[0]))
            finalrecommendation = dc.filter(encodedInput,clustersList[0])
        elif closeMatch == s2:
            #print(clustersList[1])
            #print(dc.filter(encodedInput,clustersList[1]))
            finalrecommendation = dc.filter(encodedInput,clustersList[1])
        elif closeMatch == s3:
            print(clustersList[2])
            #print(dc.filter(encodedInput,clustersList[2]))
            finalrecommendation = dc.filter(encodedInput,clustersList[2])
        #print(finalrecommendation)
        finalrecommendation = dc.decode(finalrecommendation)
        #print(finalrecommendation)
        return finalrecommendation


        
        
        #for row in cur.execute("SELECT identifier,Course FROM courses_taken WHERE Course LIKE 'CPSC%'"):