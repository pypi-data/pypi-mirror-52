from ..requester.nirvana import nirvana_requester
from ..requester.edtech import edtech_requester


class Backbone(object):
    course_manager = None  # CourseManager Model
    rest_table = None  # RestTable Model
    courses = {}  # num -> Course Model
    subjects = {}  # num -> Subject Model
    classrooms = {}  # num -> Classroom Model
    sections = {}  # num -> Section Model
    teachers = {}  # number -> Teacher Model
    students = {}  # number -> Student Model
    nirvana_requester = nirvana_requester
    edtech_requester = edtech_requester
    course_map = {}  # num -> uid
    subject_map = {}  # num -> uid
    classroom_map = {}  # num -> uid
    teacher_map = {}  # number -> uid
    student_map = {}  # number -> uid
    class_map = {}  # name -> uid

    def wrap_course_map(self):
        """
        拉取班牌后台课程(教学班)列表，映射出课程uid
        :return:
        """
        self.course_map = nirvana_requester.wrap_map("get_course_list", ("num", "uid"))

    def wrap_subject_map(self):
        """
        拉取班牌后台科目列表，映射出科目uid
        :return:
        """
        self.subject_map = nirvana_requester.wrap_map("get_subject_list", ("num", "uid"))

    def wrap_classroom_map(self):
        """
        拉取班牌后台教室列表，映射出教室uid
        :return:
        """
        self.classroom_map = nirvana_requester.wrap_map("get_classroom_list", ("num", "uid"))

    def wrap_class_map(self):
        """
        拉取班牌后台行政班列表，映射出行政班uid
        :return:
        """
        self.class_map = nirvana_requester.wrap_map("get_class_list", ("name", "uid"))

    def wrap_teacher_map(self):
        """
        拉取班牌后台教师列表，映射出教师uid
        :return:
        """
        self.teacher_map = nirvana_requester.wrap_map("get_teacher_list", ("number", "uid"))

    def wrap_student_map(self):
        """
        拉取班牌后台学生列表，映射出学生uid
        :return:
        """
        self.student_map = nirvana_requester.wrap_map("get_student_list", ("number", "uid"))

    def delete_table_manager(self, manager_id):
        """
        删除整张课程表
        :param manager_id: 课程表id
        :return:
        """
        print(">>> Delete course table")
        self.nirvana_requester.delete_table_manager(manager_id)

    def get_old_course_manager(self, key='number', value=None):
        """
        获取旧的相同课程表id
        :param key:  判定相同课程表的唯一标识字段
        :param value: 唯一标识字段值
        :return:
        """
        print(">>> Get table by {}".format(key))
        if value is None:
            value = getattr(self.course_manager, key)
        param = {key: value}
        res = self.nirvana_requester.get_table_manager(param)
        data = res.get('results', None)
        manager_id = data[0]['uid'] if data else None
        return manager_id

    def create_course_manager(self, is_active=True):
        """
        创建课程表
        :param is_active: 创建完是否立即激活
        :return:
        """
        print(">>> Create Course Table Manager")
        # delete old manager
        old_manager_id = self.get_old_course_manager()
        if old_manager_id:
            self.delete_table_manager(old_manager_id)

        # create new manager
        manager_data = self.course_manager.nirvana_data
        manager = self.nirvana_requester.create_table_manager(manager_data)
        self.course_manager.uid = manager["uid"]
        manager_mode = {"course_manager_id": self.course_manager.uid, "is_walking": self.course_manager.is_walking}
        self.nirvana_requester.set_manager_mode(manager_mode)

        # active new manager
        if is_active:
            self.nirvana_requester.active_table_manager(self.course_manager.uid)

    def create_courses(self):
        """
        创建课程(教学班)，需要通过course_manager
        该创建不包含课程表的课位
        :return:
        """
        print(">>> Batch Create Course")
        batch_data = {"manager": self.course_manager.uid, "item": []}
        for course in self.course_manager.courses:
            course.is_walking = self.course_manager.is_walking
            batch_data["item"].append(course.nirvana_data)
        self.nirvana_requester.batch_create_course(batch_data)

    def create_table(self):
        """
        创建课程表上的课位
        :return:
        """
        print(">>>Create Course Table")
        index = 0
        for course in self.course_manager.courses:
            index += 1
            for position in course.schedule:
                table_data = {"course": {"uid": course.uid or self.course_map[course.number]},
                              "manager": {"uid": self.course_manager.uid},
                              "num": position[0], "week": position[1]}
                nirvana_requester.set_course_position(table_data)
                print("##### already create {}/{} position ####".format(index, len(self.course_manager.courses)))

    def create_subjects(self, subjects):
        """
        同步科目信息
        :return:
        """
        print(">>>Create Subject")
        for subject in subjects:
            subject_id = self.subject_map.get(subject.number, None)
            if subject_id:
                res_data = self.nirvana_requester.update_subject(subject_id, subject.nirvana_data)
            else:
                res_data = self.nirvana_requester.create_subject(subject.nirvana_data)
            subject.uid = res_data['uid']

    def create_classrooms(self, classrooms):
        """
        同步教室信息
        :return:
        """
        print(">>>Create Classroom")
        for classroom in classrooms:
            classroom_id = self.classroom_map.get(classroom.number, None)
            if classroom_id:
                res_data = self.nirvana_requester.update_classroom(classroom_id, classroom.nirvana_data)
            else:
                res_data = self.nirvana_requester.create_classroom(classroom.nirvana_data)
            classroom.uid = res_data['uid']

    def relate_course_field(self):
        """
        将模型Course中的字段通过映射，转换为uid。(班牌后台接口结构)
        :return:
        """
        for course in self.course_manager.courses:
            course.subject_id = self.subject_map[course.subject_number]
            course.classroom_id = self.classroom_map.get(course.classroom_number, None)
            course.teacher_id = self.teacher_map.get(course.teacher_number, None)
            course.class_id = self.class_map.get(course.class_name, None)
            for student_number in course.student_list:
                student_id = self.student_map[student_number]
                course.student_ids.append(student_id)

    def get_old_rest_table(self, key='number', value=None):
        """
        获取旧的相同作息表id
        :param key:  判定相同作息表的唯一标识字段
        :param value: 唯一标识字段值
        :return:
        """
        print(">>> Get table by {}".format(key))
        if value is None:
            value = getattr(self.rest_table, key)
        param = {key: value}
        res = self.nirvana_requester.get_rest_table(param)
        data = res.get('results', None)
        rest_table_id = data[0]['uid'] if data else None
        return rest_table_id

    def create_rest_table(self, is_active=False):
        """
        创建作息表
        :param is_active: 创建好作息表后是否立即激活，不建议立即激活
        :return:
        """
        # delete old rest table
        old_rest_table_id = self.get_old_rest_table()
        if old_rest_table_id:
            self.delete_rest_table(old_rest_table_id)

        upload_data = self.rest_table.nirvana_data
        res_data = self.nirvana_requester.create_rest_table(upload_data)
        self.rest_table.uid = res_data['uid']

        if is_active:
            self.nirvana_requester.active_rest_table(res_data['uid'])

    def delete_rest_table(self, rest_table_id):
        """
        删除作息表
        :param rest_table_id:
        :return:
        """
        print(">>> Delete rest table")
        self.nirvana_requester.delete_rest_table(rest_table_id)

    def upload_rest_table(self, rest_table=None, is_active=False):
        """
        用于client调用，创建作息表
        :param rest_table: instance of RestTable for create
        :param is_active: 创建好作息表后是否立即激活，不建议立即激活
        :return:
        """
        self.rest_table = rest_table or self.rest_table
        self.create_rest_table(is_active)

    def upload_course_table(self, course_manager=None, is_active=False):
        """
        用于client调用，创建课程表
        :param course_manager: instance of CourseTableManager for create
        :param is_active: 创建好课程表后是否立即激活，不建议立即激活
        :return:
        """
        self.course_manager = course_manager or self.course_manager
        self.wrap_subject_map()
        self.wrap_classroom_map()
        self.wrap_teacher_map()
        self.wrap_class_map()
        self.wrap_student_map()
        self.relate_course_field()
        self.create_course_manager(is_active)
        self.create_courses()
        self.wrap_course_map()
        self.create_table()

    def upload_subjects(self, subjects):
        """
        用于client调用，创建科目
        :param subjects: [Subject, Subject]
        :return:
        """
        self.wrap_subject_map()
        self.create_subjects(subjects)

    def upload_classrooms(self, classrooms):
        """
        用于client调用，创建教室
        :param classrooms: [Classroom, Classroom]
        :return:
        """
        self.wrap_classroom_map()
        self.create_classrooms(classrooms)
