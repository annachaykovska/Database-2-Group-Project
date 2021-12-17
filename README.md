# CPSC-571-Group-Project

### Python Packages to Install (pip install)
- Flask
- email_validator
- flask_wtf
- flask_bcrypt
- flask_login

### Run (Windows)
- Go to repository with the run.py file
- Run:
    - ```set FLASK_APP=run.py```
    - ```flask run```
    
### Run (MAC)
- Go to repository with the run.py file
- Run:
    - ```export FLASK_APP=run.py```
    - ```flask run```
    
### See webpage
- http://127.0.0.1:5000/

### Programming Assignment Prompt
Problem 8. Develop system which will help a school in smoothly running its educational program. They need to keep track
of courses and their prerequisites, teachers/instructors, students and administrators. Courses may be offered in specific 
semesters by specific instructors. Students may register in courses without passing an allowed number of courses/credits but
they must complete prerequisites first. Instructors can post announcements, homeworks, exams, practice/lab material, lecture
notes, videos, etc. Students should submit their solutions for the homeworks/exams by the specified deadline. Instructors
can mark a submission and provide feedback. Students should be able to evaluate instructors for each course separately using a
questionnaire with scale from 1 to 10 and should be able to add written text. The evaluation by each student should be weighted 
based on his/her performance in the course. For example, lower weight should be assigned to an poor evaluation by a student whose
performance is poor in case some poor performing students have good evaluation. Based on the evaluation, it is important to rank
instructors based on course level (year in the program) or based on the specific course if more than one section are offered in 
one semester.(4 students)

### Assignment Breakdown
Courses:
- Offered in specific semesters by specific instructors

Students:
- Can register in courses given:
    - Enough correct prereqs
    - Won't pass the allowed number of courses (5 courses x 2 semesters x 4 years = 40)
- Submit homework by a deadline

Instructors:
- Can post (can probably do this as an all encompassing upload/download link for everything but announcements):
    - Announcements
    - Homework
    - Exams
    - Practice/Lab material
    - Lecture notes
    - Videos
    - Etc
    - https://www.youtube.com/watch?v=803Ei2Sq-Zs&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=7&ab_channel=CoreySchafer
- Can see and mark students submissions
    - Also add feedback
    
Instructor Evaluation:
- Students can grade each instructor separately on a scale of 1 to 10
- Weight reviews based on students course grades for that course
- Use this evaluation to rank profs
    - Sort by course levels or by lecture sections


### Code Resources:
- https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
- https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&ab_channel=CoreySchafer
