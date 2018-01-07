DROP DATABASE IF EXISTS examdb;

DROP ROLE IF EXISTS examdb; 

-- 创建一个登陆角色（用户），用户名examdbo, 缺省密码pass
CREATE ROLE examdbo LOGIN
  ENCRYPTED PASSWORD 'md568cefad35fed037c318b1e44cc3480cf' -- password: pass
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;

CREATE DATABASE examdb WITH OWNER = examdbo ENCODING = 'UTF8';
   


   

DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    student_no       VARCHAR(15),     --学号   
    student_name     TEXT,        --姓名
    PRIMARY KEY(student_no)
);

-- === 课程表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    course_no       VARCHAR(15), --课程号
    course_name     TEXT,        --课程名称    
    PRIMARY KEY(course_no)
);

DROP TABLE IF EXISTS teacher;
CREATE TABLE IF NOT EXISTS teacher  (
    teacher_no       VARCHAR(15), --课程号
    teacher_name     TEXT,        
    PRIMARY KEY(teacher_no)
);



DROP TABLE IF EXISTS link1;
CREATE TABLE IF NOT EXISTS link1  (
    link1_student_no VARCHAR(15),     -- 学生序号
    link1_teacher_no VARCHAR(15),     -- 教师编号
    link1_course_no  VARCHAR(15), -- 课程编号
    course_time     TEXT,
    course_place    TEXT,    
    PRIMARY KEY(link1_student_no, link1_teacher_no,link1_course_no),
    FOREIGN KEY(link1_teacher_no) REFERENCES teacher(teacher_no),
    FOREIGN KEY(link1_student_no) REFERENCES student(student_no),
    FOREIGN KEY(link1_course_no) REFERENCES course(course_no)
);



DELETE FROM teacher;
DELETE FROM student;
DELETE FROM course;
DELETE FROM link1;

INSERT INTO student (student_no, student_name)  VALUES
    ('1501', '张三'),
    ('1502', '李四'), 
    ('1503', '王五');

INSERT INTO course (course_no, course_name)  VALUES 
    ('101',  'Web'), 
    ('102',  'Python'),
    ('103',  'Java');

INSERT INTO teacher (teacher_no, teacher_name)  VALUES 
    ('1001',  '赵玲'), 
    ('1002',  '丁一'),
    ('1003',  '钱二');

INSERT INTO link1 (link1_student_no,link1_teacher_no,link1_course_no,course_time,course_place)  VALUES 
    ('1501', '1001',  '101','周一10：00','A321'), 
    ('1502', '1002',  '102','周二14：00','B222'),
    ('1503', '1003',  '103','周三16：00','C111');
