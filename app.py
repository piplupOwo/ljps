from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func


DBpassword = ''  # for wamp it is default empty string
DBport = '3306'
DBusername = 'root'
DBhost = 'localhost'
DBname = 'ljms'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://b1e8ed923266c6:386c09a4@us-cdbr-east-06.cleardb.net/heroku_6da23819e2d22f8?collation=utf8mb4_general_ci"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class JobRole(db.Model):
    __tablename__ = 'jobrole'
    jobrole_id = db.Column(db.Integer, primary_key=True)
    jobrole_name = db.Column(db.String(255), nullable=False)
    jobrole_desc = db.Column(db.String(255), nullable=False)
    roleskills = db.relationship('RoleSkill', backref='jobrole', lazy=True)
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)
    learningjourneys = db.relationship(
        'LearningJourney', backref='jobrole', lazy=True)

    def __init__(
            self,
            jobrole_id,
            jobrole_name,
            jobrole_desc,
            roleskills=[],
            isDeleted=False,
            learningjourneys=[]):
        self.jobrole_id = jobrole_id
        self.jobrole_name = jobrole_name
        self.jobrole_desc = jobrole_desc
        self.roleskills = roleskills
        self.isDeleted = isDeleted
        self.learningjourneys = learningjourneys

    def json(self):
        return {
            "jobrole_id": self.jobrole_id,
            "jobrole_name": self.jobrole_name,
            "jobrole_desc": self.jobrole_desc,
            "roleskills": [
                roleskill.json() for roleskill in self.roleskills],
            "isDeleted": self.isDeleted,
            "learningjourneys": [
                learningjourney.json() for learningjourney in self.learningjourneys]}


class LearningJourney(db.Model):
    __tablename__ = 'learningjourney'
    lj_id = db.Column(db.Integer, primary_key=True)
    lj_name = db.Column(db.String(50), nullable=False)
    jobrole_id = db.Column(
        db.Integer,
        db.ForeignKey('jobrole.jobrole_id'),
        nullable=False)
    staff_id = db.Column(
        db.Integer,
        db.ForeignKey('staff.staff_id'),
        nullable=False)
    ljcourses = db.relationship(
        'LearningJourneyCourse',
        backref='learningjourney',
        lazy=True)

    def __init__(self, lj_id, lj_name, jobrole_id, staff_id, ljcourses=list()):
        self.lj_id = lj_id
        self.lj_name = lj_name
        self.jobrole_id = jobrole_id
        self.staff_id = staff_id
        self.ljcourses = ljcourses

    def json(self):
        return {
            "lj_id": self.lj_id,
            "lj_name": self.lj_name,
            "jobrole_id": self.jobrole_id,
            "staff_id": self.staff_id,
            "ljcourses": [ljcourse.json() for ljcourse in self.ljcourses],
        }


class Skill(db.Model):
    __tablename__ = 'skill'
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    skill_desc = db.Column(db.String(255))
    roleskills = db.relationship('RoleSkill', backref='skill', lazy=True)
    courseskills = db.relationship('CourseSkill', backref='skill', lazy=True)
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
            self,
            skill_id,
            skill_name,
            skill_desc,
            roleskills=[],
            courseskills=[],
            isDeleted=False):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.roleskills = roleskills
        self.courseskills = courseskills
        self.isDeleted = isDeleted

    def json(self):
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "skill_desc": self.skill_desc,
            "roleskills": [
                roleskill.json() for roleskill in self.roleskills],
            "courseskills": [
                courseskill.json() for courseskill in self.courseskills],
            "isDeleted": self.isDeleted}


class RoleSkill(db.Model):
    __tablename__ = 'roleskill'
    rsid = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(
        db.Integer,
        db.ForeignKey('skill.skill_id'),
        nullable=False)
    jobrole_id = db.Column(
        db.Integer,
        db.ForeignKey('jobrole.jobrole_id'),
        nullable=False)

    def __init__(self, rsid, skill_id, jobrole_id):
        self.rsid = rsid
        self.skill_id = skill_id
        self.jobrole_id = jobrole_id

    def json(self):
        return {
            "rsid": self.rsid,
            "skill_id": self.skill_id,
            "jobrole_id": self.jobrole_id
        }


class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)
    staffs = db.relationship('Staff', backref='Role', lazy=True)

    def __init__(self, role_id, role_name, staffs=list()):
        self.role_id = role_id
        self.role_name = role_name
        self.staffs = staffs

    def json(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    registrations = db.relationship('Registration', backref='Staff', lazy=True)

    def __init__(
            self,
            staff_id,
            staff_fname,
            staff_lname,
            dept,
            email,
            role,
            registrations=list()):
        self.staff_id = staff_id
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.email = email
        self.role = role
        self.registrations = registrations

    def json(self):
        return {
            "staff_id": self.staff_id,
            "staff_fname": self.staff_fname,
            "staff_lname": self.staff_lname,
            "dept": self.dept,
            "email": self.email,
            "role": self.role
        }


class CourseSkill(db.Model):
    __tablename__ = 'courseskill'
    csid = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(
        db.Integer,
        db.ForeignKey('skill.skill_id'),
        nullable=False)
    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course.course_id'),
        nullable=False)

    def __init__(self, csid, skill_id, course_id):
        self.csid = csid
        self.skill_id = skill_id
        self.course_id = course_id

    def json(self):
        return {
            "csid": self.csid,
            "skill_id": self.skill_id,
            "course_id": self.course_id
        }


class Course(db.Model):
    course_id = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
    registrations = db.relationship(
        'Registration', backref='course', lazy=True)
    courseskills = db.relationship('CourseSkill', backref='course', lazy=True)
    ljcourses = db.relationship(
        'LearningJourneyCourse',
        backref='course',
        lazy=True)

    def __init__(
            self,
            course_id,
            course_name,
            course_desc,
            course_status,
            course_type,
            course_category,
            registrations=list(),
            courseskills=list(),
            ljcourses=list()):
        self.course_id = course_id
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status
        self.course_type = course_type
        self.course_category = course_category
        self.registrations = registrations
        self.courseskills = courseskills
        self.ljcourses = ljcourses

    def json(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_desc": self.course_desc,
            "course_status": self.course_status,
            "course_type": self.course_type,
            "course_category": self.course_category,
            "registrations": [
                registration.json() for registration in self.registrations],
            "courseskills": [
                courseskill.json() for courseskill in self.courseskills],
            "ljcourses": [
                ljcourse.json() for ljcourse in self.ljcourses]}


class Registration(db.Model):
    reg_id = db.Column(db.Integer, primary_key=True)
    # course_id = db.Column(db.String(20))
    # staff_id = db.Column(db.Integer)
    reg_status = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey('course.course_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

    def __init__(
            self,
            reg_id,
            reg_status,
            completion_status,
            course_id,
            staff_id):
        self.reg_id = reg_id
        self.reg_status = reg_status
        self.completion_status = completion_status
        self.course_id = course_id
        self.staff_id = staff_id

    def json(self):
        return {
            "reg_id": self.reg_id,
            "reg_status": self.reg_status,
            "completion_status": self.completion_status,
            "course_id": self.course_id,
            "staff_id": self.staff_id
        }


class LearningJourneyCourse(db.Model):
    __tablename__ = 'learningjourneycourse'
    ljc_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course.course_id'),
        nullable=False)
    lj_id = db.Column(db.Integer, db.ForeignKey(
        'learningjourney.lj_id'), nullable=False)

    def __init__(self, ljc_id, course_id, lj_id):
        self.ljc_id = ljc_id
        self.course_id = course_id
        self.lj_id = lj_id

    def json(self):
        return {
            "ljc_id": self.ljc_id,
            "course_id": self.course_id,
            "lj_id": self.lj_id
        }


# db.create_all()

def add_values():  # THIS IS EXAMPLE TO ADD VALUES TO DB (CURRENTLY NOT USED AS WE PRIORITISE READ OVER OTHER OPERATIONS)
    role1 = Role(role_id=1, role_name='Admin', staffs=[])

    staff1 = Staff(staff_id=1,
                   staff_fname='Apple',
                   staff_lname='Tan',
                   dept='HR',
                   email='apple.tan.hr@spm.com',
                   role=1,
                   registrations=[])

    course1 = Course(course_id='IS111',
                     course_name='Introduction to Programming',
                     course_desc='Introductory Python module',
                     course_status='Active',
                     course_type='Internal',
                     course_category='Technical',
                     registrations=[])

    registration1 = Registration(reg_id=1,
                                 course_id='IS111',
                                 staff_id=1,
                                 reg_status='Registered',
                                 completion_status='Completed')

    db.session.add(role1)
    db.session.add(staff1)
    db.session.add(course1)
    db.session.add(registration1)
    db.session.commit()


@app.route('/')
def home():
    return """
    <h1>Hello! this links are to test the backend, expect json files from them.</h1>
    <a href='/course'>get courses</a>
    <a href='/staff'>get staffs</a>
    <a href='/role'>get roles</a>
    <a href='/jobrole'>get jobroles</a>
    <a href='/skill'>get skills</a>
    <a href='/roleskill'>get roleskills</a>
    <a href='/courseskill'>get courseskills</a>
    <a href='/registration'>get registrations</a>
    <a href='/learningjourney'>get learningjourneys</a>
    <a href='/learningjourneycourse'>get learningjourneycourse</a>
    """


@app.route('/skill')
def skill():
    skills = Skill.query.all()
    if len(skills):

        skills_not_softdeleted = [skill.json()
                                  for skill in skills if not skill.isDeleted]

        if len(skills_not_softdeleted):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skills": skills_not_softdeleted
                    }
                }
            )

        return jsonify(
            {
                "code": 404,
                "message": "No skills found that are non softdeleted."
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no skills."
        }
    ), 404


@app.route('/skill/softdeleted')
def skill_softdeleted():
    skills = Skill.query.all()
    if len(skills):
        softdeleted_skills = [skill.json()
                              for skill in skills if skill.isDeleted]

        if len(softdeleted_skills):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skills": softdeleted_skills
                    }
                }
            )

        return jsonify(
            {
                "code": 404,
                "message": "No skills found that are softdeleted."
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no skills in the database."
        }
    ), 404


@app.route('/skill/<int:skill_id>')
def find_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    linked_courses = []

    if skill:
        courseskillswithname = []
        # iterate through courseskills and get the course name
        for courseskill in skill.courseskills:
            course = Course.query.filter_by(
                course_id=courseskill.course_id).first()
            linked_courses.append(course.json())

            courseskillswithname.append({
                "csid": courseskill.csid,
                "skill_id": courseskill.skill_id,
                "course_id": courseskill.course_id,
                "course_name": course.course_name
            })

        skilljson = skill.json()
        skilljson["courseskills"] = courseskillswithname
        skilljson["linked_courses"] = linked_courses

        return jsonify(
            {
                "code": 200,
                "data": skilljson,
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

# add skill


@app.route('/skill', methods=['POST'])
def add_skill():
    data = request.get_json()
    skill_id = 1
    try:
        skill_id = Skill.query.count() + 1
    except:
        pass
    skill = Skill(**data, skill_id=skill_id)
    skill_name = data['skill_name'].lower()
    if (Skill.query.filter(func.lower(Skill.skill_name) == skill_name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "skill already exists."
            }
        ), 400
    try:
        db.session.add(skill)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skill_id": data['skill_id']
                },
                "message": "An error occurred while creating the skill."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skill.json()
        }
    ), 201

# update skill


@app.route('/skill/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        data = request.get_json()
        skill_name = data['skill_name'].lower()

        original_name = skill.skill_name

        skill.skill_name = "temp"
        db.session.commit()

        if (Skill.query.filter(func.lower(Skill.skill_name) == skill_name).first()):
            skill.skill_name = original_name
            db.session.commit()
            return jsonify(
                {
                    "code": 400,
                    "message": "skill already exists."
                }
            ), 400
        try:
            skill.skill_name = data['skill_name']
            skill.skill_desc = data['skill_desc']
            db.session.commit()
        except BaseException:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "skill_id": skill_id
                    },
                    "message": "An error occurred while updating the skill."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

# soft delete skill


@app.route('/skill/<int:skill_id>/softdelete')
def soft_delete_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        if not skill.isDeleted:
            skill.isDeleted = True
        else:
            skill.isDeleted = False

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

# add role


@app.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()
    role = Role(**data)
    role_name = data['role_name'].lower()
    if (Role.query.filter(func.lower(Role.role_name) == role_name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "role already exists."
            }
        ), 400
    try:
        db.session.add(role)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "role_id": data['role_id']
                },
                "message": "An error occurred while creating the role."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": role.json()
        }
    ), 201


@app.route('/roleskill')
def roleskill():
    roleskills = RoleSkill.query.all()
    if len(roleskills):
        return jsonify({"code": 200, "data": {"roleskills": [
            roleskill.json() for roleskill in roleskills]}})
    return jsonify(
        {
            "code": 404,
            "message": "There are no roleskills."
        }
    ), 404


@app.route('/roleskill/<int:roleskill_id>')
def find_roleskill(roleskill_id):
    roleskill = RoleSkill.query.filter_by(roleskill_id=roleskill_id).first()
    if roleskill:
        return jsonify(
            {
                "code": 200,
                "data": roleskill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Roleskill not found."
        }
    ), 404


@app.route('/staff')
def staff():
    staffs = Staff.query.all()

    if len(staffs):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staffs": [staff.json() for staff in staffs]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no staffs."
        }
    ), 404


@app.route('/staff/<int:staff_id>')
def find_staff(staff_id):
    staff = Staff.query.filter_by(staff_id=staff_id).first()
    if staff:
        return jsonify(
            {
                "code": 200,
                "data": staff.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff not found."
        }
    ), 404


@app.route('/role')
def role():
    roles = Role.query.all()

    if len(roles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in roles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no roles."
        }
    ), 404


@app.route('/role/<int:role_id>')
def find_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        return jsonify(
            {
                "code": 200,
                "data": role.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Role not found."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>', methods=['PUT'])
def update_jobrole(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
    if jobrole:
        data = request.get_json()
        jobrole_name = data['jobrole_name'].lower()

        original_name = jobrole.jobrole_name

        jobrole.jobrole_name = "temp"
        db.session.commit()

        if (JobRole.query.filter(func.lower(
                JobRole.jobrole_name) == jobrole_name).first()):
            jobrole.jobrole_name = original_name
            db.session.commit()
            return jsonify(
                {
                    "code": 400,
                    "message": "job role already exists."
                }
            ), 400
        try:
            jobrole.jobrole_name = data['jobrole_name']
            jobrole.jobrole_desc = data['jobrole_desc']
            db.session.commit()
        except BaseException:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "jobrole_id": jobrole_id
                    },
                    "message": "An error occurred while updating the jobrole."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "role not found."
        }
    ), 404

# soft delete role


@app.route('/role/<int:role_id>/softdelete')
def soft_delete_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        if not role.isDeleted:
            role.isDeleted = True
        else:
            role.isDeleted = False

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": role.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "role not found."
        }
    ), 404


@app.route('/jobrole')
def getjobrole():
    # get all non soft deleted job roles
    jobroles = JobRole.query.filter_by(isDeleted=False).all()

    if len(jobroles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobroles": [jobrole.json() for jobrole in jobroles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no jobroles."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>')
def getjobrolebyid(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()

    if jobrole:
        jobrolejson = jobrole.json()

        linked_skills = []

        # iterate through roleskills in jobrole
        for roleskill in jobrole.roleskills:
            # get skill name from skill id
            skill = Skill.query.filter_by(skill_id=roleskill.skill_id).first()
            # append skill.json to linked_skills
            linked_skills.append(skill.json())

        jobrolejson['linked_skills'] = linked_skills

        return jsonify(
            {
                "code": 200,
                "data": jobrolejson
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "JobRole not found."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>/softdelete')
def soft_delete_jobrole(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
    if jobrole:
        if not jobrole.isDeleted:
            jobrole.isDeleted = True
        else:
            jobrole.isDeleted = False

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "JobRole not found."
        }
    ), 404


@app.route('/jobrole/softdeleted')
def getsoftdeletedjobroles():
    jobroles = JobRole.query.filter_by(isDeleted=True).all()

    if len(jobroles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobroles": [jobrole.json() for jobrole in jobroles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no soft deleted jobroles."
        }
    ), 404

# add job role


@app.route('/jobrole', methods=['POST'])
def add_jobrole():
    data = request.get_json()
    jobrole_id = 1
    try:
        jobrole_id = JobRole.query.count() + 1
    except:
        pass

    jobrole = JobRole(**data, jobrole_id=jobrole_id)
    # check if jobrole already exists
    if JobRole.query.filter_by(jobrole_name=jobrole.jobrole_name).first():
        return jsonify(
            {
                "code": 400,
                "message": "A jobrole with name '{}' already exists.".format(jobrole.jobrole_name)
            }
        ), 400
    try:
        db.session.add(jobrole)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the jobrole."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": jobrole.json()
        }
    ), 201


@app.route('/course')
def course():
    courses = Course.query.all()

    if len(courses):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in courses]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no courses."
        }
    ), 404


@app.route('/course/<string:course_id>')
def find_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify(
            {
                "code": 200,
                "data": course.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Course not found."
        }
    ), 404


@app.route('/courseskill')
def courseskill():
    courseskills = CourseSkill.query.all()

    if len(courseskills):
        return jsonify({"code": 200, "data": {"courseskills": [
            courseskill.json() for courseskill in courseskills]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no courseskills."
        }
    ), 404

# put request to courseskill with only skill_id


@app.route('/skill/<int:skill_id>/courseskills', methods=['PUT'])
def update_courseskill_forskill(skill_id):

    try:
        data = request.get_json()
        print(data)
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        courseskill = CourseSkill.query.filter_by(skill_id=skill_id).all()

        # delete all courseskills for skill
        for cs in courseskill:
            db.session.delete(cs)

        unique_course_id = []
        # add new courseskills for skill
        for courseskillobject in data['courseskills']:
            course_id = courseskillobject['course_id']
            if course_id not in unique_course_id:
                unique_course_id.append(course_id)
            else:
                continue

            csid = 1
            try:
                csid = CourseSkill.query.filter(CourseSkill.csid is not None).order_by(
                    CourseSkill.csid).all()[-1].csid + 1
            except:
                pass

            courseskill = CourseSkill(
                skill_id=skill_id, course_id=course_id, csid=csid)
            db.session.add(courseskill)

        db.session.commit()

        # return updated courseskills
        return jsonify(
            {
                "code": 200,
                "data": [courseskill.json() for courseskill in skill.courseskills]
            }
        )
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the courseskill."
            }
        ), 500


@app.route('/jobrole/<int:jobrole_id>/roleskills', methods=['PUT'])
def update_roleskill_forrole(jobrole_id):
    try:
        data = request.get_json()
        print(data)
        jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
        roleskill = RoleSkill.query.filter_by(jobrole_id=jobrole_id).all()

        # delete all roleskills for skill
        for rs in roleskill:
            db.session.delete(rs)

        unique_jobrole_id = []
        # add new roleskills for skill
        for roleskillobject in data['roleskills']:
            skill_id = roleskillobject['skill_id']
            if skill_id not in unique_jobrole_id:
                unique_jobrole_id.append(skill_id)
            else:
                continue

            rsid = 1
            try:
                rsid = RoleSkill.query.filter(RoleSkill.rsid is not None).order_by(
                    RoleSkill.rsid).all()[-1].rsid + 1
            except:
                pass

            roleskill = RoleSkill(
                skill_id=skill_id,
                jobrole_id=jobrole_id,
                rsid=rsid)
            db.session.add(roleskill)
        db.session.commit()

        # return updated roleskills
        return jsonify(
            {
                "code": 200,
                "data": [roleskill.json() for roleskill in jobrole.roleskills]
            }
        )
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the roleskill."
            }
        ), 500


# put request to courseskill
# @app.route('/courseskill/<string:course_id>/<int:skill_id>', methods=['PUT'])
# def update_courseskill(course_id, skill_id):
#     # get courseskill by course_id and skill_id
#     courseskill = CourseSkill.query.filter_by(course_id=course_id, skill_id=skill_id).first()

#     if courseskill:
#         data = request.get_json()
#         courseskill.skill_id = data['skill_id']
#         courseskill.course_id = data['course_id']

#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": courseskill.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "CourseSkill not found."
#         }
#     ), 404

# post request to courseskill
@app.route('/courseskill', methods=['POST'])
def add_courseskill():

    data = request.get_json()
    csid = 1

    try:
        csid = CourseSkill.query.filter(CourseSkill.csid is not None).order_by(
            CourseSkill.csid).all()[-1].csid + 1
    except:
        pass

    courseskill = CourseSkill(**data, csid=csid)

    # check if courseskill with same skill and course already exists
    if CourseSkill.query.filter_by(
            skill_id=courseskill.skill_id,
            course_id=courseskill.course_id).first():
        return jsonify({"code": 400, "message": "A courseskill with skill_id '{}' and course_id '{}' already exists.".format(
            courseskill.skill_id, courseskill.course_id)}), 400

    try:
        db.session.add(courseskill)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                # should not happen because checks in place to prevent
                # duplicate csid
                "message": "An error occurred creating the courseskill."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": courseskill.json()
        }
    ), 201


# delete request to courseskill
@app.route('/courseskill/<string:course_id>/<int:skill_id>',
           methods=['DELETE'])
def delete_courseskill(course_id, skill_id):
    courseskill = CourseSkill.query.filter_by(
        course_id=course_id, skill_id=skill_id).first()

    if courseskill:
        db.session.delete(courseskill)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": courseskill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "CourseSkill not found."
        }
    ), 404

# get learning journey


@app.route('/learningjourney')
def learningjourney():
    learningjourneys = LearningJourney.query.all()

    if len(learningjourneys):
        return jsonify({"code": 200, "data": {"learningjourneys": [
            learningjourney.json() for learningjourney in learningjourneys]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneys."
        }
    ), 404

# get learning journey by id
@app.route('/learningjourney/<int:learningjourney_id>')
def get_learningjourney(learningjourney_id):
    learningjourney = LearningJourney.query.filter_by(
        lj_id = learningjourney_id).first()

    learningjourneyjson = learningjourney.json()
    linked_jobrole = JobRole.query.filter_by(jobrole_id=learningjourneyjson['jobrole_id']).first()
    linked_courses = []
    for lj_course in learningjourneyjson['ljcourses']:
        linked_courses.append(Course.query.filter_by(course_id=lj_course['course_id']).first())
    learningjourneyjson["linked_jobrole"] = linked_jobrole.json()
    learningjourneyjson["linked_courses"] = [course.json() for course in linked_courses]

    if learningjourney:
        return jsonify(
            {
                "code": 200,
                "data": learningjourneyjson
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "LearningJourney not found."
        }
    ), 404

@app.route('/staff/learningjourney/<int:staff_id>')
def learningjourneyuser(staff_id):

    # learningjourneys = LearningJourney.query.all()

    # print(LearningJourney['staff_id'])

    listoflj = LearningJourney.query.filter_by(staff_id=staff_id)
    staff = Staff.query.filter_by(staff_id=staff_id).first()
    if listoflj:
        learningjourneysjson = []

        # iterate through learningjourneys
        for learningjourneyobject in listoflj:
            learningjourneysjson.append(learningjourneyobject.json())

            linked_jobrole = JobRole.query.filter_by(
                jobrole_id=learningjourneyobject.jobrole_id).first()
            linked_courses = []

            learningjourney = LearningJourney.query.filter_by(
                lj_id=learningjourneyobject.lj_id).first()
            # iterate through ljcourses

            ljcourses = LearningJourneyCourse.query.filter_by(
                lj_id=learningjourney.lj_id)
            for ljcourseobject in ljcourses:
                course = Course.query.filter_by(
                    course_id=ljcourseobject.course_id).first()
                linked_courses.append(course.json())

            linked_skills = []
            for roleskillobject in linked_jobrole.roleskills:
                skill = Skill.query.filter_by(
                    skill_id=roleskillobject.skill_id).first()
                linked_skills.append(skill.json())

            learningjourneysjson[-1]['linked_jobrole'] = linked_jobrole.json()
            learningjourneysjson[-1]['linked_jobrole']['linked_skills'] = linked_skills
            learningjourneysjson[-1]['linked_courses'] = linked_courses

        return jsonify(
            {
                "code": 200,
                "data": {
                    "learningjourneys": learningjourneysjson
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneys."
        }
    ), 404
    # print(listoflj)

    # print("hi")

    # if len(learningjourneys):
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": {
    #                 "learningjourneys": [learningjourney.json() for learningjourney in learningjourneys]
    #             }
    #         }
    #     )

    # return jsonify(
    #     {
    #         "code": 404,
    #         "message": "There are no learningjourneys."
    #     }
    # ), 404

# get learning journey by name
@app.route('/learningjourney/staff/<int:staff_id>/name/<string:lj_name>')
def get_learningjourney_name(staff_id, lj_name):
    learningjourney = LearningJourney.query.filter(
        LearningJourney.staff_id == staff_id, LearningJourney.lj_name == lj_name).first()

    if learningjourney:
        return jsonify(
            {
                "code": 200,
                "data": learningjourney.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "LearningJourney not found."
        }
    ), 404

# add learning journey
@app.route('/learningjourney', methods=['POST'])
def add_learningjourney():
    data = request.get_json()

    courses = data["courses"]
    staff_id = data["staff_id"]
    jobrole_id = data["jobrole_id"]
    lj_name = data["lj_name"]
    lj_id = 1

    try:
        lj_id = LearningJourney.query.filter(
            LearningJourney.lj_id is not None).order_by(
            LearningJourney.lj_id).all()[
                -1].lj_id + 1
    except:
        pass

    try:
        lj_id = data["lj_id"]
    except:
        pass

    learningjourney = LearningJourney(
        lj_name=lj_name,
        staff_id=staff_id,
        jobrole_id=jobrole_id,
        lj_id=lj_id)

    if (LearningJourney.query.filter(
        LearningJourney.staff_id == staff_id, LearningJourney.lj_name == lj_name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "A Learning Journey with the same name already exists."
            }
        ), 400

    try:
        db.session.add(learningjourney)
        db.session.commit()

        lj_id = learningjourney.lj_id
        for course_id in courses:

            ljc_id = 1
            try:
                ljc_id = LearningJourneyCourse.query.filter(LearningJourneyCourse.ljc_id is not None).order_by(
                    LearningJourneyCourse.ljc_id).all()[-1].ljc_id + 1
            except:
                pass

            lj_course = LearningJourneyCourse(
                lj_id=lj_id, course_id=course_id, ljc_id=ljc_id)
            db.session.add(lj_course)
            db.session.commit()

    except BaseException:
        return jsonify(
            {
                "code": 523,
                "message": "An error occurred creating the learningjourney."
            }
        ), 523

    return jsonify(
        {
            "code": 201,
            "data": learningjourney.json()
        }
    ), 201

# delete learning journey


@app.route('/learningjourney/<int:lj_id>', methods=['DELETE'])
def delete_learningjourney(lj_id):
    learningjourney = LearningJourney.query.filter_by(lj_id=lj_id).first()
    if learningjourney:
        try:
            # iterate through learningjourney.ljcourses
            for ljcourseobject in learningjourney.ljcourses:
                db.session.delete(ljcourseobject)

            db.session.delete(learningjourney)
            db.session.commit()

        except BaseException:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred deleting the learningjourney."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": learningjourney.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "Learning Journey not found."
        }
    ), 404

# get learning journey courses table


@app.route('/learningjourneycourse')
def learningjourneycourse():
    learningjourneycourse = LearningJourneyCourse.query.all()

    if len(learningjourneycourse):
        return jsonify({"code": 200, "data": {"learningjourneycourse": [
            learningjourneycourse.json() for learningjourneycourse in learningjourneycourse]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneycourses."
        }
    ), 404

# get registrations


@app.route('/registration')
def registration():
    registrations = Registration.query.all()

    if len(registrations):
        return jsonify({"code": 200, "data": {"registrations": [
            registration.json() for registration in registrations]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
