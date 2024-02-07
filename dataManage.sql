-- Active: 1683055826645@@group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com@3306@university
DROP TABLE IF EXISTS referenceInfo;
DROP TABLE IF EXISTS AdvisorStudent;
DROP TABLE IF EXISTS GradApplication;
DROP TABLE IF EXISTS ApplicationChecklist;
DROP TABLE IF EXISTS checkReference;
DROP TABLE IF EXISTS checkReview;
DROP TABLE IF EXISTS PriorDegree;
DROP TABLE IF EXISTS Transcript;
DROP TABLE IF EXISTS GRE;

DROP TABLE IF EXISTS Recommendation;
DROP TABLE IF EXISTS ReviewInfo;
DROP TABLE IF EXISTS DecisionInfo;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Alumni;
DROP TABLE IF EXISTS Form1;
DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS GraduationApplications;
DROP TABLE IF EXISTS Program;

DROP TABLE IF EXISTS Courses;

DROP TABLE IF EXISTS c_history;
DROP TABLE IF EXISTS c_schedule;

DROP TABLE IF EXISTS c_catalogue;


DROP TABLE IF EXISTS matChecklist;
DROP TABLE IF EXISTS Applications;
DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS GradApplication;


-- CREATE DATABASE university
--      DEFAULT CHARACTER SET  = 'utf8mb4';

-- USE university;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE users (
    UserID VARCHAR(8) not NULL PRIMARY KEY,
    email  VARCHAR(50),
    passw VARCHAR(50) not null,
    fName VARCHAR(50) not NULL,
    lName VARCHAR(50) not NULL,
    userType VARCHAR(50) not NULL,
    primaryAddress VARCHAR(50) not NULL,
    primaryPhone VARCHAR(50) not NULL,
    SSN VARCHAR(50) not NULL UNIQUE
);

CREATE TABLE c_catalogue  (
    cid INT(8) not null,
    dept varchar(10), 
    cnum INT(4) , 
    title VARCHAR(20), 
    sem VARCHAR(20), 
    cataYear VARCHAR(4), 
    cred INT(8), 
    prone VARCHAR(10) , 
    prtwo VARCHAR(10), 
    capacity INT(8) , 
    cLocation VARCHAR(50), 
    instructorID VARCHAR(8) not null,
    PRIMARY KEY(cid),
    FOREIGN KEY(instructorID) REFERENCES users(UserID) 
         ON DELETE CASCADE
);
CREATE TABLE Program
(
    programID   int(8)       NOT NULL UNIQUE,
    program_name enum('MS', 'PhD') DEFAULT ('MS'),
    program_major VARCHAR(255) NOT NULL,
    program_gpa  FLOAT       NOT NULL,
    PRIMARY KEY (programID,
                 program_name,
                program_major)
);

CREATE TABLE Applications(
    applicationID VARCHAR(8) PRIMARY KEY,
    userIdent VARCHAR(8), # link to userid

    degreeSought INT,
    NumPriorDegree INT,
    GREInclude INT,
    priorWorkExperience VARCHAR(500),
    interests VARCHAR(500),
    admissionSem VARCHAR(50),
    admissionYr VARCHAR(50),
    sendTranscript INT,

    FOREIGN KEY (userIdent) 
        REFERENCES users(UserID) 
        ON DELETE CASCADE
);

CREATE TABLE referenceInfo(
    appID VARCHAR(8),
    referencer1fname VARCHAR(50),
    referencer1lname VARCHAR(50),
    referencer1email VARCHAR(50),
    referencer1title VARCHAR(50),
    referencer1affil VARCHAR(50),

    referencer2fname VARCHAR(50),
    referencer2lname VARCHAR(50),
    referencer2email VARCHAR(50),
    referencer2title VARCHAR(50),
    referencer2affil VARCHAR(50),

    referencer3fname VARCHAR(50),
    referencer3lname VARCHAR(50),
    referencer3email VARCHAR(50),
    referencer3title VARCHAR(50),
    referencer3affil VARCHAR(50),

    FOREIGN KEY(appID)
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE ApplicationChecklist(
    IDapp VARCHAR(8), # link to applicationid
    IDuser VARCHAR(8), # link to userid
    GREIncluded BOOLEAN,
    transcriptReceived BOOLEAN,
    isReviewed BOOLEAN,
    isReferenced BOOLEAN,
    finaldecisionreceived BOOLEAN,
    isCompleted BOOLEAN,
    FOREIGN KEY (IDuser) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (IDApp) REFERENCES Applications(applicationID) ON DELETE CASCADE
);

CREATE TABLE checkReference( 
    idApp VARCHAR(8),
    reference1received BOOLEAN, 
    reference2received BOOLEAN,
    reference3received BOOLEAN,
    FOREIGN KEY (idApp) REFERENCES Applications(applicationID) ON DELETE CASCADE
);

CREATE TABLE checkReview(
    idAPP VARCHAR(8),
    review1received BOOLEAN,
    review2received BOOLEAN,
    review3received BOOLEAN,
    FOREIGN KEY (idAPP) REFERENCES Applications(applicationID)
);

CREATE TABLE PriorDegree(
    AID VARCHAR(8), # link to applicationid
    DegreeType VARCHAR(8),
    GPA FLOAT,
    Major VARCHAR(50),
    priorYear INT, 
    University VARCHAR(50),
    FOREIGN KEY (AID) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE Transcript(
    idu VARCHAR(8), # link to userID
    IApplication VARCHAR(8), # link to ApplicationID
    TranscriptID VARCHAR(8),
    Transcript VARCHAR(50),
    School VARCHAR(50),
    FOREIGN KEY (idu) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (IApplication) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE GRE(
    AppID VARCHAR(8), # link to ApplicationID
    UI VARCHAR(8), # linke to UserID
    GREScore INT, 
    Verbal INT,
    Quantitative INT,
    GREAdvScore INT, 
    GREAdvSbj VARCHAR(50),
    TOEFL INT,
    TOEFLDate VARCHAR(50),
    examYear INT,
    FOREIGN KEY (UI) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (AppID) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE Recommendation(
    referencerfName VARCHAR(50),
    referencerlName VARCHAR(50),
    letter VARCHAR(3000),
    IDApplication VARCHAR(8), # link to applicationID
    -- RecommenderID VARCHAR(8), # link to userID
    
    -- FOREIGN KEY (RecommenderID) 
    --     REFERENCES users(UserID)
    --     ON DELETE CASCADE,
    FOREIGN KEY (IDApplication) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE ReviewInfo(
    IDA VARCHAR(8), # link to ApplicationID
    reviewerID VARCHAR(8), # link to UserID for reviewers
    reviewerName VARCHAR(50),
    reviewerScore INT,
    isGeneric BOOLEAN,
    isCredible BOOLEAN,
    refFrom VARCHAR(50),
    rating INT,
    deficiency VARCHAR(4),
    commenting VARCHAR(40),
    FOREIGN KEY (reviewerID) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (IDA) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE DecisionInfo(
    ApplicationI VARCHAR(8), # link to ApplicationID
    GASID VARCHAR(8), # link to UserID of final decider
    finalDecision BOOLEAN,
    finalComments VARCHAR(40),
    admissionDate VARCHAR(20),
    recommendedAdvisor VARCHAR(50),
    FOREIGN KEY (GASID) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (ApplicationI) 
        REFERENCES Applications(applicationID)
        ON DELETE CASCADE
);

CREATE TABLE Student( 
    studentID VARCHAR(8),
    program_id int(8),
    advisor_id VARCHAR(8),
    FOREIGN KEY (studentID)
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY(advisor_id) 
        REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (program_id)
        REFERENCES Program(programID)
        ON DELETE CASCADE
);

CREATE TABLE Alumni
(
    alumniID VARCHAR(8),
    graduation_date DATE,
    degreeAlumni  INT(8),
    FOREIGN KEY (alumniID) 
        REFERENCES users (UserID)
        ON DELETE CASCADE,
    FOREIGN KEY (degreeAlumni) 
        REFERENCES Program (programID)
        ON DELETE CASCADE
);



CREATE TABLE Form1 (
  UserID VARCHAR(8) NOT NULL,
  ExtremelyLongString TEXT NOT NULL,
  IsApproved BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (UserID)
);


CREATE TABLE GraduationApplications
(
    student_id       VARCHAR(8),
    graduatingDegree INT(8) NOT NULL,
    application_date DATE   NOT NULL,
    graduatingStatus           ENUM('APPROVED', 'PENDING', 'REJECTED', 'GRADUATED') DEFAULT ('PENDING'),
    thesis           VARCHAR(255) NULL,
    FOREIGN KEY (student_id) REFERENCES users (UserID),
    FOREIGN KEY (graduatingDegree) REFERENCES Program (programID)
);

CREATE TABLE Enrollments
(
    student_id VARCHAR(8),
    course_id  INT(10),
    semester   enum ('SPRING', 'SUMMER', 'FALL', 'WINTER'),
    enrollyear       YEAR NOT NULL,
    enrollstatus     enum ('FINAL', 'IN PROGRESS', 'REGISTERED'),
    grade      VARCHAR(1),
    FOREIGN KEY (student_id) REFERENCES users (UserID),
    FOREIGN KEY (course_id) REFERENCES c_catalogue (cid),
    PRIMARY KEY (student_id,
                 course_id)
);



CREATE TABLE Courses
(
    course_code  INT(8) NOT NULL,
    course_name  VARCHAR(255),
    credit_hours INT(4),
    FOREIGN KEY(course_code) REFERENCES c_catalogue(cid)
        ON DELETE CASCADE
);

CREATE TABLE c_history (
    userID VARCHAR(8) not null,
    cid INT(8) not null,
    fgrade VARCHAR(8),
    sem VARCHAR(10) not null,
    prevYear VARCHAR(4),
    instructor_ID VARCHAR(8) not null,

    FOREIGN KEY(userID) REFERENCES users(UserID)
        ON DELETE CASCADE,
    FOREIGN KEY(cid) REFERENCES c_catalogue(cid)
        ON DELETE CASCADE,
    FOREIGN KEY(instructor_ID) REFERENCES users(UserID)
        ON DELETE CASCADE
);

CREATE TABLE c_schedule (
    cid INT(8) not null,
    cDay varchar(5) not null,
    cTime varchar(50) not null,
    FOREIGN KEY(cid) REFERENCES c_catalogue(cid)
        ON DELETE CASCADE
);

CREATE TABLE AdvisorStudent (
    advisorID VARCHAR(8) NOT NULL,
    studentID VARCHAR(8) NOT NULL,
    PRIMARY KEY (advisorID, studentID),
    FOREIGN KEY (advisorID) REFERENCES users (UserID),
    FOREIGN KEY (studentID) REFERENCES users (UserID)
);
CREATE TABLE GradApplication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    application_date DATE NOT NULL,
    graduating_status VARCHAR(255) NOT NULL,
    thesis TEXT NOT NULL,
    graduating_degree ENUM('MS', 'PhD') NOT NULL
);

ALTER TABLE GradApplication DROP COLUMN ID;

ALTER TABLE GradApplication
ADD COLUMN metRequirements BOOLEAN DEFAULT TRUE;

CREATE TABLE matChecklist(
    idUser VARCHAR(8),
    acceptance BOOLEAN,
    payFee     BOOLEAN,
    FOREIGN KEY(idUser) REFERENCES users(UserID)
    ON DELETE CASCADE
);

#Data for faculty user 
INSERT INTO users VALUES('10000005', 'bn@gwu.edu', 'pass','Bhagirath', 'Narahari', 'Faculty', '1 GW Street, Washington, District of Coumbia, 21125', '(505)117-8990', '22211220');
#Data for GS user
INSERT INTO users VALUES('10000001', 'jt@gwu.edu', 'pass','James', 'Taylor', 'GS', '308 Negra Arryo Lane, Albuquergue, New Mexico', '(505)117-8993', '123456789');
#Data for CAC USER
INSERT INTO users VALUES('65432109', 'cat@gwu.edu', 'pass', 'Cat', 'Meadows', 'CAC', 'No thoughts head empty', '(123)456-7890', '123456793');
#Data for sysadmin
INSERT INTO users VALUES('00000000', 'wjh@gwu.edu', 'pass', 'Willem', 'Huizinga', 'ADMIN', '1 GW Street, Nashville, Tennessee', '(615)481-6267', '123456791');
#Data for applicant John: application complete but no reviews
INSERT INTO users VALUES('12312312', 'john@gwu.edu', 'pass', 'John', 'Lennon', 'Applicant', '450 Dubs Street, Arlington, Virginia', '(101)101-1010', '111111111' );

INSERT INTO Applications VALUES('54210258', '12312312', '1', '2', '1', 'intern at Google', 'Digital Forensics', 'Fall', '2023', '0');
INSERT INTO ApplicationChecklist VALUES('54210258','12312312', '1', '1', '0', '1', '0', '1');
INSERT INTO GRE VALUES('54210258', '123123312', '260', '130', '130', '260', 'math', '120', '2020', '2022');
INSERT INTO PriorDegree VALUES('54210258', 'MS', '3.5', 'cybersecurity', '2020', 'GW');
INSERT INTO PriorDegree VALUES('54210258', 'BS', '3.5', 'cybersecurity', '2020', 'GW');
INSERT INTO Recommendation VALUES('a', 'a', 'good student', '54210258');
INSERT INTO Recommendation VALUES('b', 'b', 'good student', '54210258');
INSERT INTO Recommendation VALUES('c', 'c', 'good student', '54210258');
INSERT INTO checkReference VALUES('54210258', '1', '1', '1');
INSERT INTO referenceInfo VALUES('54210258', 'a', 'a', 'a@gwu.edu', 'professor', 'GW', 'b', 'b', 'b@gwu.edu', 'professor', 'GW', 'c', 'c', 'c@gwu.edu', 'professor', 'GW');

#Data for applicant Ringo Star
INSERT INTO users VALUES('66666666', 'ringo2@gwu.edu', 'pass', 'Ringo2', 'Starr2', 'Applicant','89 Best Ave', '(425)445-6245', '222111111');


INSERT INTO users VALUES('10000004', 'wood@gwu.edu', 'pass', 'Heller', 'Wood', 'Faculty', '45 GW Street, Nashville, Tennessee', '(615)481-6267', '45215368');

INSERT INTO users VALUES('10000006', 'choi@gwu.edu', 'pass', 'Choi', 'Choi', 'Faculty', '45 GW Street, Nashville, Tennessee', '(615)481-6267', '45335368');

SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO c_catalogue
VALUES (1, 'CSCI', 6221, "SW Paradigms", "F", "2023", 3, null, null,50,"GEL",'10000001');
INSERT INTO c_catalogue
VALUES (2,'CSCI',6461,"Computer Architecture", "F", "2023", 3, null, null, 50, "TOMP",'10000004');
INSERT INTO c_catalogue
VALUES (3,'CSCI',6212,"Algorithms","F","2023",3,null,null,50,"GEL",'10000006');
INSERT INTO c_catalogue
VALUES (4,'CSCI',6220,"Machine Learning","F","2023",3,null,null,50,"TOMP",'10000001');
INSERT INTO c_catalogue
VALUES (5,'CSCI',6232,"Networks 1","F","2023",3,null,null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (6,'CSCI',6233,"Networks 2","F","2023",3,"CSCI 6232",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (7,'CSCI',6241,"Database 1","F","2023",3,null,null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (8,'CSCI',6242,"Database 2","F","2023",3,"CSCI 6241",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (9,'CSCI',6246,"Compilers","F","2023",3,"CSCI 6461","CSCI 6212",50,"TOMP",'10000001');
INSERT INTO c_catalogue
VALUES (10,'CSCI',6260,"Multimedia","F","2023",3,null,null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (11,'CSCI',6251,"Cloud Computing","F","2023",3,"CSCI 6461",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (12,'CSCI',6254,"SW Engineering","F","2023",3,"CSCI 6221",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (13,'CSCI',6262,"Graphics 1","F","2023",3,null,null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (14,'CSCI',6283,"Security 1","F","2023",3,"CSCI 6212",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (15,'CSCI',6284,"Cryptography","F","2023",3,"CSCI 6212",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (16,'CSCI',6286,"Network Security","F","2023",3,"CSCI 6283","CSCI 6232",50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (17,'CSCI',6325,"Algorithms 2","F","2023",3,"CSCI 6212",null,50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (18,'CSCI',6461,"Embedded Systems","F","2023",3,"CSCI 6461","CSCI 6212",50,"SEH",'10000001');
INSERT INTO c_catalogue
VALUES (19,'CSCI',6384,"Cryptography 2","F","2023",3,"CSCI 6241",null,50,"TOMP",'10000001');
INSERT INTO c_catalogue
VALUES (20,'ECE',6241,"Communication Theory","F","2023",3,null,null,50,"TOMP",'10000001');
INSERT INTO c_catalogue
VALUES (21,'ECE',6242,"Information Theory","F","2023",3,null,null,50,"GEL",'10000001');
INSERT INTO c_catalogue
VALUES (22,'MATH',6210,"Logic","F","2023",3,null,null,50,"GEL",'10000001');


INSERT INTO c_schedule VALUES ( 1, 'M', "1500-1730" );
INSERT INTO c_schedule VALUES ( 2, 'T', "1500-1730" );
INSERT INTO c_schedule VALUES ( 3, 'W', "1500-1730" );
INSERT INTO c_schedule VALUES ( 4, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 5, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 6, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 7, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 8, 'R', "1800-2030" );
INSERT INTO c_schedule VALUES ( 9, 'T', "1500-1730" );
INSERT INTO c_schedule VALUES ( 10, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 11, 'M', "1530-1800" );
INSERT INTO c_schedule VALUES ( 12, 'R', "1800-2030" );
INSERT INTO c_schedule VALUES ( 13, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 14, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 15, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 16, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 17, 'W', "1500-1730" );
INSERT INTO c_schedule VALUES ( 18, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 19, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 20, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 21, 'R', "1600-1830" );
INSERT INTO c_schedule VALUES ( 22, 'T', "1600-1830" );


