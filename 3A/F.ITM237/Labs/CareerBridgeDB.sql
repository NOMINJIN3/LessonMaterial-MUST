-- ДААЛГАВАР 1. Өгөгдлийн сан үүсгэх
CREATE DATABASE CareerBridgeDB;
GO

USE CareerBridgeDB;
GO


-- ДААЛГАВАР 2. Байгууллагын хүснэгт үүсгэх
-- PK, IDENTITY, UNIQUE, CHECK)

CREATE TABLE CareerOfficer (
    officer_id   INT           PRIMARY KEY IDENTITY(1,1),
    employee_id  NVARCHAR(10)  NOT NULL UNIQUE,        
    full_name    NVARCHAR(100) NOT NULL,
    position     NVARCHAR(50),
    email        NVARCHAR(100) NOT NULL UNIQUE
);
GO

CREATE TABLE Company (
    company_id        INT           PRIMARY KEY IDENTITY(1,1), 
    name              NVARCHAR(100) NOT NULL UNIQUE,           
    register_no       NVARCHAR(10)  NOT NULL UNIQUE,          
    industry          NVARCHAR(50),
    established_year  INT CHECK (established_year >= 1900
                                 AND established_year <= YEAR(GETDATE())),
    is_verified       BIT DEFAULT 0,                          
    verified_by       INT NULL,                                
    FOREIGN KEY (verified_by) REFERENCES CareerOfficer(officer_id)
        ON DELETE NO ACTION
);
GO


-- ДААЛГАВАР 3. (FOREIGN KEY, Computed Column, ON DELETE / ON UPDATE)

CREATE TABLE Student (
    student_id     INT           PRIMARY KEY IDENTITY(1,1),
    first_name     NVARCHAR(50)  NOT NULL,
    last_name      NVARCHAR(50)  NOT NULL,
    student_code   NVARCHAR(10)  NOT NULL UNIQUE,             
    email          NVARCHAR(100) NOT NULL UNIQUE,
    phone          NVARCHAR(20),
    date_of_birth  DATE,
    age AS (DATEDIFF(YEAR, date_of_birth, GETDATE())),       
    gender         NVARCHAR(10)
                   CHECK (gender IN (N'Эрэгтэй', N'Эмэгтэй', N'Бусад')),
    registered_at  DATE DEFAULT GETDATE()
);
GO

Alter TABLE Student
Add CONSTRAINT CHK_Student_Age CHECK (age <= 38);
GO


CREATE TABLE CV (
    cv_id             INT           PRIMARY KEY IDENTITY(1,1),
    student_id        INT           NOT NULL UNIQUE,           
    title             NVARCHAR(100) NOT NULL,
    field             NVARCHAR(50)  NOT NULL,                  
    major             NVARCHAR(100),                           
    gpa               DECIMAL(3,2)  CHECK (gpa >= 0.00 AND gpa <= 4.00),
    graduation_year   INT           CHECK (graduation_year BETWEEN 2000 AND 2040),
    desired_job_type  NVARCHAR(20)  DEFAULT N'Дадлага'
                      CHECK (desired_job_type IN (N'Дадлага', N'Ажил')),
    location          NVARCHAR(50),
    updated_at        DATETIME      DEFAULT GETDATE(),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON DELETE CASCADE                                     
        ON UPDATE CASCADE
);
GO


CREATE TABLE Experience (
    exp_id        INT           PRIMARY KEY IDENTITY(1,1),
    cv_id         INT           NOT NULL,
    company_name  NVARCHAR(100) NOT NULL,                      
    position      NVARCHAR(100) NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES CV(cv_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
GO


CREATE TABLE Skill (
    skill_id    INT          PRIMARY KEY IDENTITY(1,1),
    name        NVARCHAR(50) NOT NULL UNIQUE,
    skill_type  NVARCHAR(10) NOT NULL
                CHECK (skill_type IN ('hard', 'soft'))
);
GO


CREATE TABLE CVSkill (
    cv_id     INT          NOT NULL,
    skill_id  INT          NOT NULL,
    level     NVARCHAR(15) NOT NULL DEFAULT 'beginner'
              CHECK (level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    PRIMARY KEY (cv_id, skill_id),                         
    FOREIGN KEY (cv_id)    REFERENCES CV(cv_id)       ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id) ON DELETE CASCADE
);
GO


CREATE TABLE JobPosting (
    posting_id     INT           PRIMARY KEY IDENTITY(1,1),
    company_id     INT           NOT NULL,
    title          NVARCHAR(100) NOT NULL,
    job_type       NVARCHAR(20)  NOT NULL
                   CHECK (job_type IN (N'Дадлага', N'Ажил')),
    start_date     DATE          NOT NULL,
    end_date       DATE          NOT NULL,
    duration_days AS (DATEDIFF(DAY, start_date, end_date)),    
    CHECK (end_date >= start_date),
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
        ON DELETE CASCADE                                      
        ON UPDATE CASCADE
);
GO


CREATE TABLE JobPostingSkill (
    posting_id  INT NOT NULL,
    skill_id    INT NOT NULL,
    PRIMARY KEY (posting_id, skill_id),
    FOREIGN KEY (posting_id) REFERENCES JobPosting(posting_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id)   REFERENCES Skill(skill_id)        ON DELETE CASCADE
);
GO


CREATE TABLE Application (
    application_id  INT          PRIMARY KEY IDENTITY(1,1),
    student_id      INT          NOT NULL,
    posting_id      INT          NOT NULL,
    applied_at      DATETIME     DEFAULT GETDATE(),
    status          NVARCHAR(20) NOT NULL DEFAULT N'Хүлээгдэж буй'
                    CHECK (status IN (N'Хүлээгдэж буй', N'Тэнцсэн', N'Тэнцээгүй')),
    UNIQUE (student_id, posting_id),                           
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (posting_id) REFERENCES JobPosting(posting_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
GO


CREATE TABLE Agreement (
    agreement_id    INT          PRIMARY KEY IDENTITY(1,1),
    application_id  INT          NOT NULL UNIQUE,              
    officer_id      INT          NOT NULL,
    start_date      DATE         NOT NULL,
    end_date        DATE         NOT NULL,
    status          NVARCHAR(20) DEFAULT N'Идэвхтэй'
                    CHECK (status IN (N'Идэвхтэй', N'Дууссан', N'Цуцлагдсан')),
    CHECK (end_date > start_date),
    FOREIGN KEY (application_id) REFERENCES Application(application_id)
        ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES CareerOfficer(officer_id)
        ON DELETE NO ACTION                                    
);
GO


-- ДААЛГАВАР 4. Өгөгдөл оруулах (0.5)


INSERT INTO CareerOfficer (employee_id, full_name, position, email) VALUES
    ('CO001', N'Д.Оюунчимэг', N'Карьерын зөвлөх',   'oyunchimeg.d@careerbridge.mn'),
    ('CO002', N'Б.Ганзориг',  N'Дадлагын зохицуулагч', 'ganzorig.b@careerbridge.mn');


INSERT INTO Company (name, register_no, industry, established_year, is_verified, verified_by) VALUES
    (N'Мэдээ Тех ХХК',       '6012345', N'Програм хангамж', 2012, 1, 1),
    (N'Хангай Дата ХХК',     '6023456', N'Өгөгдөл',         2016, 1, 1),
    (N'Тэнгэр Финтек ХХК',   '6034567', N'Санхүү',          2018, 1, 2),
    (N'Говь Лоджистик ХХК',  '6045678', N'Тээвэр',          2009, 0, NULL),
    (N'Алтай Медиа ХХК',     '6056789', N'Медиа',           2020, 1, 2);


INSERT INTO Student (first_name, last_name, student_code, email, phone, date_of_birth, gender) VALUES
    (N'Номин',     N'Цэрэн',   'B241940115', 'nomin.ts@student.edu.mn',    '99001122', '2006-02-14', N'Эмэгтэй'),
    (N'Тэмүүлэн',  N'Бат',     'B231940150', 'temuulen.b@gmail.com',       '99112233', '2005-07-22', N'Эрэгтэй'),
    (N'Ану',       N'Ганбаат', 'B221940088', 'anu.g@student.edu.mn',       '99223344', '2004-11-05', N'Эмэгтэй'),
    (N'Билгүүн',   N'Дорж',    'B221940091', 'bilguun.d@gmail.com',        '99334455', '2004-01-30', N'Эрэгтэй'),
    (N'Солонго',   N'Мөнх',    'B241940140', 'solongo.m@student.edu.mn',   '99445566', '2006-05-18', N'Эмэгтэй'),
    (N'Батзориг',  N'Сүх',     'B231940162', 'batzorig.s@student.edu.mn',  '99556677', '2005-09-12', N'Эрэгтэй'),
    (N'Мишээл',    N'Энх',     'B221940102', 'misheel.e@gmail.com',        '99667788', '2004-12-25', N'Эмэгтэй'),
    (N'Бат-Эрдэнэ',N'Төмөр',   'B231940171', 'baterdene.t@student.edu.mn', '99778899', '2005-04-08', N'Эрэгтэй');


INSERT INTO CV (student_id, title, field, major, gpa, graduation_year, desired_job_type, location) VALUES
    (1, N'Junior өгөгдлийн шинжээч', 'IT',      N'Мэдээллийн систем',  3.72, 2028, N'Дадлага', N'Улаанбаатар'),
    (2, N'Backend хөгжүүлэгч',       'IT',      N'Програм хангамж',    3.45, 2027, N'Дадлага', N'Улаанбаатар'),
    (3, N'Санхүүгийн шинжээч',       N'Бизнес', N'Санхүү',             3.88, 2026, N'Ажил',    N'Улаанбаатар'),
    (4, N'DevOps инженер',           'IT',      N'Компьютерийн ухаан', 3.10, 2026, N'Ажил',    N'Дархан'),
    (5, N'UI/UX дизайнер',           'IT',      N'Програм хангамж',    3.56, 2028, N'Дадлага', N'Улаанбаатар'),
    (6, N'Логистикийн туслах',       N'Бизнес', N'Менежмент',          2.95, 2027, N'Дадлага', N'Эрдэнэт'),
    (7, N'Контент менежер',          N'Медиа',  N'Сэтгүүл зүй',        3.67, 2026, N'Ажил',    N'Улаанбаатар'),
    (8, N'Мобайл хөгжүүлэгч',        'IT',      N'Програм хангамж',    3.81, 2027, N'Дадлага', N'Улаанбаатар');


INSERT INTO Experience (cv_id, company_name, position) VALUES
    (2, N'Код Академи',         N'Сургалтын туслах'),
    (3, N'Номын сан ТББ',       N'Сайн дурын санхүүч'),
    (4, N'Сүлжээ Сервис ХХК',   N'Техникийн туслах'),
    (7, N'Оюутны радио',        N'Хөтлөгч');


INSERT INTO Skill (name, skill_type) VALUES
    ('SQL', 'hard'), ('Python', 'hard'), ('Java', 'hard'), ('Docker', 'hard'),
    ('Figma', 'hard'), ('Excel', 'hard'),
    (N'Багаар ажиллах', 'soft'), (N'Харилцаа', 'soft');


INSERT INTO CVSkill (cv_id, skill_id, level) VALUES
    (1, 1, 'advanced'), (1, 2, 'intermediate'), (1, 7, 'expert'),
    (2, 1, 'intermediate'), (2, 3, 'advanced'),
    (3, 6, 'expert'), (3, 8, 'advanced'),
    (4, 4, 'advanced'), (4, 2, 'intermediate'), (4, 1, 'beginner'),
    (5, 5, 'expert'), (5, 7, 'advanced'),
    (6, 6, 'intermediate'),
    (7, 8, 'expert'),
    (8, 3, 'advanced'), (8, 1, 'expert');


INSERT INTO JobPosting (company_id, title, job_type, start_date, end_date) VALUES
    (1, N'Backend дадлагажигч',      N'Дадлага', '2027-06-01', '2027-08-31'),
    (1, N'Junior Java хөгжүүлэгч',   N'Ажил',    '2027-01-15', '2027-12-31'),
    (2, N'Өгөгдлийн шинжээч дадлага', N'Дадлага', '2027-06-15', '2027-08-15'),
    (3, N'Санхүүгийн шинжээч',       N'Ажил',    '2027-02-01', '2027-12-31'),
    (4, N'Агуулахын туслах',         N'Дадлага', '2027-07-01', '2027-08-31'),
    (5, N'UI/UX дизайн дадлага',     N'Дадлага', '2027-06-01', '2027-07-31');


INSERT INTO JobPostingSkill (posting_id, skill_id) VALUES
    (1, 1), (1, 3), (2, 3), (3, 1), (3, 2), (4, 6), (5, 6), (6, 5);


INSERT INTO Application (student_id, posting_id, status) VALUES
    (1, 3, N'Тэнцсэн'),
    (2, 1, N'Хүлээгдэж буй'),
    (8, 2, N'Тэнцсэн'),
    (3, 4, N'Хүлээгдэж буй'),
    (6, 5, N'Тэнцээгүй'),
    (5, 6, N'Хүлээгдэж буй'),
    (4, 1, N'Тэнцээгүй'),
    (2, 2, N'Хүлээгдэж буй'),
    (8, 1, N'Хүлээгдэж буй'),
    (1, 1, N'Хүлээгдэж буй');


INSERT INTO Agreement (application_id, officer_id, start_date, end_date) VALUES
    (1, 1, '2027-06-15', '2027-08-15'),
    (3, 2, '2027-01-15', '2027-12-31');
GO



-- ДААЛГАВАР 5. SELECT асуулгууд


SELECT * FROM Student;                                         

SELECT first_name, last_name, student_code, email FROM Student;


SELECT s.first_name, s.last_name, c.gpa                        
FROM Student s JOIN CV c ON c.student_id = s.student_id
WHERE c.gpa > 3.5;

SELECT * FROM JobPosting                                       
WHERE job_type = N'Дадлага';


SELECT s.first_name, s.last_name, s.gender, c.field, c.major, c.gpa
FROM Student s JOIN CV c ON c.student_id = s.student_id
WHERE c.field = 'IT' AND s.gender = N'Эрэгтэй';


SELECT s.first_name, s.last_name, cs.level
FROM Student s
JOIN CV c       ON c.student_id = s.student_id
JOIN CVSkill cs ON cs.cv_id = c.cv_id
JOIN Skill sk   ON sk.skill_id = cs.skill_id
WHERE sk.name = 'SQL' AND cs.level IN ('advanced', 'expert');


SELECT s.first_name, s.last_name, c.gpa                        
FROM Student s JOIN CV c ON c.student_id = s.student_id
ORDER BY c.gpa DESC;

SELECT last_name, first_name FROM Student                      
ORDER BY last_name ASC, first_name ASC;


SELECT first_name, last_name FROM Student                    
WHERE first_name LIKE N'Б%';

SELECT first_name, last_name, email FROM Student               
WHERE email LIKE '%@gmail.com';

SELECT title, job_type FROM JobPosting                         
WHERE title LIKE N'%дадлага%';

-- 5.5 Агрегат функцууд
SELECT COUNT(*) AS TotalStudents FROM Student;

SELECT AVG(gpa) AS AverageGPA, MAX(gpa) AS HighestGPA, MIN(gpa) AS LowestGPA FROM CV;

SELECT status, COUNT(*) AS ApplicationCount        
FROM Application
GROUP BY status;

SELECT jp.title, COUNT(a.application_id) AS ApplicantCount    
FROM JobPosting jp
LEFT JOIN Application a ON a.posting_id = jp.posting_id
GROUP BY jp.title
ORDER BY ApplicantCount DESC;

SELECT c.field, COUNT(*) AS StudentCount, AVG(c.gpa) AS AvgGPA 
FROM CV c
GROUP BY c.field
HAVING COUNT(*) >= 2;
GO


-- ДААЛГАВАР 6. UPDATE болон DELETE (0.4)


UPDATE Application                                             
SET status = N'Тэнцсэн'
WHERE application_id = 2;

UPDATE CV                                                      
SET gpa = 3.60, updated_at = GETDATE()
WHERE student_id = (SELECT student_id FROM Student WHERE student_code = 'B231940150');

UPDATE Company                                               
SET is_verified = 1, verified_by = 2
WHERE is_verified = 0;



DELETE FROM Application                                        
WHERE status = N'Тэнцээгүй';

DELETE FROM Student                                         
WHERE student_code = 'B231940162';                            

SELECT * FROM CV WHERE student_id = 6;                     

GO


--  ДААЛГАВАР 7. Индекс үүсгэх (0.3)
CREATE INDEX IDX_CV_Field            ON CV(field);                          
CREATE INDEX IDX_Application_Status  ON Application(status);                
CREATE INDEX IDX_Student_Name        ON Student(last_name, first_name);     
CREATE INDEX IDX_JobPosting_TypeDate ON JobPosting(job_type, end_date);     

GO








