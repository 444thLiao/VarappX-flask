from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from varappx.handle_init import *

# basedir
## Login stuff.
## Care, this stupid Django automatically adds '_id' to foreign key fields,
## e.g. a foreign key named 'variants_db' here corresponds to 'variants_db_id' in the db.


# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))


class UsersModel(object):
    """Abstract, to add these fields to all db"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    created_by = db.Column(db.String(50), nullable=True)
    updated_by = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=1)

    #
    # class Meta:
    #     abstract = True
    def __init__(self,**kwargs):
        #import pdb;pdb.set_trace()
        for key,value in kwargs.items():
            if not hasattr(self,key) and key != 'password':
                import pdb;pdb.set_trace()
                raise SyntaxError
            elif key == 'password':
                setattr(self, key, value)
            else:
                setattr(self,key,value)


class Users(UsersModel, db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255), default='')
    email = db.Column(db.String(255))
    code = db.Column(db.String(25))
    activation_code = db.Column(db.String(25), nullable=True)
    is_password_reset = db.Column(db.Integer, nullable=True)

    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    DbAccess = db.relationship('DbAccess', lazy='dynamic', backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.salt = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.salt, password)

    class Meta:
        managed = True  # If True, Django will create a table on migration
        db_table = 'users'

    def __repr__(self):
        return "[User]: <username> %s; <email> %s; <roles> {%s}" % (self.username,self.email,str(self.role).split(':')[1])

class Roles(UsersModel, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    rank = db.Column(db.Integer, nullable=True)
    can_validate_user = db.Column(db.Integer, default=0)
    can_delete_user = db.Column(db.Integer, default=0)

    users = db.relationship(Users, lazy='dynamic', backref='role')

    class Meta:
        managed = True

    def __repr__(self):
        return "[Roles]: <name> %s; <rank> %s; <can_validate_user> %s; <can_delete_user> %s" % \
               (self.name,self.rank,self.can_validate_user,self.can_delete_user)

class People(UsersModel, db.Model):
    """Extra data on users"""
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    institution = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    is_laboratory = db.Column(db.Integer, nullable=True)
    laboratory = db.Column(db.String(255), nullable=True)

    users = db.relationship(Users, lazy='dynamic', backref='person')

    class Meta:
        managed = True



class Bookmarks(UsersModel, db.Model):
    """App states saved by user"""
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text)
    description = db.Column(db.String(255))
    long_description = db.Column(db.Text, default='')

    db_access_id = db.Column(db.Integer, db.ForeignKey('db_accesses.id'), nullable=True)

    class Meta:
        managed = True


class DbAccess(UsersModel, db.Model):
    """Many-to-many access of users to databases"""
    __tablename__ = 'db_accesses'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    variants_db_id = db.Column(db.Integer, db.ForeignKey('variants_db.id'), nullable=True)

    bookmark = db.relationship(Bookmarks, lazy='dynamic', backref='DbAccess')


    class Meta:
        managed = True
        unique_together = ("user", "variants_db")

    def __repr__(self):
        return "[DbAccess]: <users> {%s}; <access_db> {%s}" % \
               (str(self.users).split(':')[1],str(self.variantsdb).split(':')[1])

class VariantsDb(UsersModel, db.Model):
    """Gemini databases"""
    __tablename__ = 'variants_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    visible_name = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    location = db.Column(db.Text, nullable=True, default='')
    hash = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True, default='')
    size = db.Column(db.BigInteger, nullable=True)
    parent_db_id = db.Column(db.Integer, nullable=True)  # not a ForeignKey because it is only informative

    DbAccess = db.relationship(DbAccess, lazy='dynamic', backref='variantsdb')

    class Meta:
        managed = True
        unique_together = ("filename", "hash")

    def __repr__(self):
        return "[VariantsDb]: <name> %s; <filename> %s; <description> %s" % (self.name,self.filename,self.description)

class Preferences(UsersModel, db.Model):
    """User preferences, such as columns selection"""
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True)
    preferences = db.Column(db.Text, default='')
    description = db.Column(db.Text, default='')

    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    class Meta:
        managed = True


class Annotation(UsersModel, db.Model):
    """Versions of databases, programs, gemini etc."""
    __tablename__ = 'annotation'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=True)
    source_version = db.Column(db.String(255), nullable=True)
    annotation = db.Column(db.String(255), nullable=True)
    annotation_version = db.Column(db.String(255), nullable=True)

    variants_db = db.Column(db.Integer, db.ForeignKey('variants_db.id'), nullable=True)

    class Meta:
        managed = True


class History(UsersModel, db.Model):
    """Record user actions"""
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    session_start = db.Column(db.DateTime)
    url = db.Column(db.Text)
    query = db.Column(db.Text, default='')
    description = db.Column(db.String(255))
    long_description = db.Column(db.Text, default='')
    ip_address = db.Column(db.String(255))

    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    class Meta:
        managed = True


class Bam(UsersModel, db.Model):
    """Relate samples to filenames or keys for the bam server"""
    __tablename__ = 'bam'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=True)
    key = db.Column(db.String(255), nullable=True)
    sample = db.Column(db.String(255), nullable=True)

    variants_db = db.Column(db.Integer, db.ForeignKey('variants_db.id'), nullable=True)

    class Meta:
        managed = True


import os,json
base_dir = os.path.abspath(os.path.dirname(__file__))
def loaddata(file_name = base_dir+'/../../varappx/main/resources/init/basic_info.json'):
    #print(file_name)
    data = json.load(open(file_name))
    #import pdb;pdb.set_trace()
    for each in data:
        model = each['model']
        fields = each['fields']
        try:
            exec('_cache = %s(**fields)' % model)
        except:
            import pdb;pdb.set_trace()
        exec("db.session.add(_cache);db.session.commit()")