# tutory
Final Project Summary

1. Log in page ( A form directly at the middle and maybe LOGO at the top, with some nice cool background.)
2. Dashboard page - two, one for students/one for teachers
3. Streaming page
4. Materials page ( a main page for materials, and a new route added to each material #not too sure here how we going to make it work, if teachers upload files in folders should be route to each folder then for each file it's a link right? )
5. Quizzes page
6. Homework Page
7. Report Card Page
________________________________________________________________________________________________________________________________________
Base Structure:

Homepage
- Sign up
- Login

Profile
- Edit info such as email (but not IC / full name), upload profile image

Dashboard
- (header) Image / Info (intake year, name of the school, class, student name - call from backend)
- News / Announcement (form)
- Upcoming activities / quote of the day (API - 3rd party?)
- Calendar (API - 3rd party)

Streaming
- Video streaming
- Whiteboard (drawing tablet's screen)
- Pop up quizzes:
    *Students: modal pop up
    *Staffs: form for questionnaire & answer / can see students' answers
- Chatbox (API?)
- (optional) notes / announcements

Materials 
- List of classes
    *Include materials such as lecture notes and tutorial either via:
        a) Links of google docs either via:
            i) Google DOC API 
            ii) Storing URL inside database
                    example:
                    Google doc links    Subject     Chapter/Topic     Date
                    URL                 English     Chapter 1         21/8/2020
        b) Downloadable content that is stored in database
- Online Exam either via:
    a) Google doc submission (excel / word format) and render it into online exam / form format (API requires to be researched)
    b) Staff upload (excel / word format), student download and submit it once done

Assignment
- Students: submit answers with google doc link (similar to materials(part a))
- Staffs: list of each classes > access to students' links 

Report Card
- Graph based on specific subject
- Table with subjects and grades
- Attendance record
- Teacher's remarks
- (Once teacher gave remark + all subjects are finalized) Automated email push to parents - a link of graph + tables + remarks

________________________________________________________________________________________________________________________________________
Tables in Database:
- User consisting of Student / Staff (Login / Sign up / Personal Info)
- Roles (with id & roles - hardcorded values)
- Course Material
- Announcement
- Report card
- Subject
- Exam (Result)
- Assignments
- Attendance (for both students and staffs)
