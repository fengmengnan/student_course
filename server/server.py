# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import dbconn
dbconn.register_dsn("host=localhost dbname=examdb user=examdbo password=pass")


class BaseReqHandler(tornado.web.RequestHandler):

    def db_cursor(self, autocommit=True):
        return dbconn.SimpleDataCursor(autocommit=autocommit)
    
#课程表获取处理器，获取课程表的全部信息，返回到list.html界面
class MainHandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql = '''
           SELECT student_no, student_name, teacher_no, teacher_name,course_no,
             course_name,course_time,course_place
            FROM student,teacher,course,link1
            WHERE student_no=link1_student_no AND teacher_no=link1_teacher_no AND course_no=link1_course_no
            ORDER BY student_no, teacher_no;
            '''
            cur.execute(sql)
            items = cur.fetchall()
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render("list.html", title="课程表", items=items)

#课程添加处理器，从文本框获取学生编号、教师编号、课程编号，课程的上课时间、上课地点
#并把文本框中的信息添加到link1表中，通过数据库的表连接查询到课程表
class CourseAddHandler(BaseReqHandler):
    def post(self):
        student_no = self.get_argument("student_no")
        teacher_no = self.get_argument("teacher_no")
        course_no = self.get_argument("course_no")
        course_time=self.get_argument("course_time")
        course_place=self.get_argument("course_place")
        
        with self.db_cursor() as cur:
            sql = '''INSERT INTO link1 
            (link1_student_no, link1_teacher_no, link1_course_no,course_time,course_place)  VALUES( %s, %s, %s,%s,%s);'''
            cur.execute(sql, (student_no, teacher_no, course_no,course_time,course_place))
            cur.commit()
        
        self.set_header("Content-Type", "text/html; charset=UTF-8") 
        self.redirect("/")
#课程删除处理器，通过link1表中的student_no、course_no、teacher_no来定位要删除的课程
#删除课程后重定向到list.html界面
class CourseDelHandler(BaseReqHandler):
    def get(self, link1_student_no, link1_course_no,link1_teacher_no):
        
        with self.db_cursor() as cur:
            sql = '''
            DELETE FROM link1 
                WHERE link1_student_no= %s AND link1_course_no= %s AND link1_teacher_no=%s'''
            cur.execute(sql, (link1_student_no, link1_course_no,link1_teacher_no))
            cur.commit()

        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.redirect("/")
#课程编辑界面，先从数据库中查询是否有本条数据，再对该条数据进行修改
class CourseEditHandler(BaseReqHandler):
    def get(self, link1_student_no, link1_course_no,link1_teacher_no):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        with self.db_cursor() as cur:
            sql = '''
            SELECT course_time , course_place FROM link1
                WHERE link1_student_no = %s AND link1_course_no = %s AND link1_teacher_no=%s ;
            '''
            cur.execute(sql, (link1_student_no, link1_course_no,link1_teacher_no))
            row = cur.fetchone()
            if row:
                self.render("edit.html", link1_student_no=link1_student_no, 
                    link1_course_no=link1_course_no,link1_teacher_no=link1_teacher_no, course_time=row[0],course_place=row[1])
            else:
                self.write('Not FOUND!')
 #post方法是从网页的文本框中获取信息   
    def post(self, link1_student_no, link1_course_no,link1_teacher_no):
        
        course_time = self.get_argument("course_time")
        course_place = self.get_argument("course_place")
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        with self.db_cursor() as cur:
            sql = '''
            UPDATE link1 SET course_time=%s , course_place=%s
                WHERE link1_student_no= %s AND link1_course_no= %s AND link1_teacher_no=%s '''
            cur.execute(sql, (course_time, course_place, link1_student_no,link1_course_no,link1_teacher_no))
            cur.commit()
        self.redirect("/")
  
#各个url对应的处理器
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/course.add", CourseAddHandler),
    (r"/course.del/([0-9]+)/([0-9]+)/([0-9]+)", CourseDelHandler),
    (r"/course.edit/([0-9]+)/([0-9]+)/([0-9]+)", CourseEditHandler),
], debug=True)

#端口号8888
if __name__ == "__main__":
    application.listen(8888)
    server = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(lambda: None, 500, server).start()
    server.start()
