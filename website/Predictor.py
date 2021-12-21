import sqlite3
import numpy
import sys
import Jaccard
from defaultDatabaseEntries import courseList, antireqList, prereqList, otherCoursesList
class Predictor:
        con = sqlite3.connect('CourseDB.db')
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

        with open('encodedStudents.txt', 'w') as f:
            numpy.set_printoptions(threshold=sys.maxsize)
            f.write(numpy.array_str(encodedStudents))
        
        with open('recommendations.txt', 'w') as f:
            numpy.set_printoptions(threshold=sys.maxsize)
            f.write(numpy.array_str(Jaccard.jc.k_means(encodedStudents.tolist())))
        
        #for row in cur.execute("SELECT identifier,Course FROM courses_taken WHERE Course LIKE 'CPSC%'"):