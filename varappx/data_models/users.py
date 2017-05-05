

from varappx.common import manage_dbs

def user_factory(u):
    """Create a more useful User instance from a Django Users instance *u*.
    In particular, its 'databases' attribute stores all active database names
    he has access to, with a runtime check of the connection and physical presence.
    """
    from varappx.handle_config import settings
    if not u:
        return

    role = role_factory(u.role)
    person = person_factory(u.person)
    accesses_qs = DbAccess.query.filter_by(users=u, is_active=1)
    user_dbs = [acc.variantsdb for acc in accesses_qs if acc.variantsdb.is_active]
    databases = []
    for _db in user_dbs:
        if not _db.name in settings.SQLALCHEMY_BINDS.keys():
            # logger.warning("Database '{}' "
            #                 "found in users db but not in settings.DATABASES. "
            #                 "It was probably introduced manually. Syncing.".format(db.name))
            manage_dbs.add_db_to_settings(_db.name, _db.filename)
        #import pdb;pdb.set_trace()
        if not os.path.exists(settings.SQLITE_DB_PATH+'/'+_db.filename):
            #logger.warning("Database '{}' not found on disk!".format(_db.name))
            _vdb = VariantsDb.query.filter_by(name=_db.name).order_by('filename','updated_at').all()[-1]

            manage_dbs.deactivate_if_not_found_on_disk(_vdb)
            continue
        if _db.name not in [a_db.name for a_db in databases]:
            databases.append(_db)
    databases = [database_factory(_db) for _db in databases]
    return User(u.username, u.email, u.code, u.salt, u.is_active, person, role, databases)

def database_factory(d):
    """Create a Database from a users_db.VariantsDb."""
    users = list(set([acc.users.username for acc in DbAccess.query.filter_by(variantsdb=d)]))
    return Database(d.name, d.location, d.filename, d.hash, d.description, d.is_active, d.size, users)

def role_factory(r):
    """Create a Role from a users_db.Roles."""
    return Role(r.name, r.rank, r.can_validate_user, r.can_delete_user)

def person_factory(p):
    """Create a Person from a users_db.People."""
    return Person(p.firstname, p.lastname, p.institution, p.street, p.city, p.phone, p.is_laboratory, p.laboratory)


############


def users_list_from_users_db(query_set=None, db='default'):
    """Return a list of `User`s from database content."""
    if query_set is None:
        query_set = Users.query.join('DbAccess', 'variantsdb').all()
    return [user_factory(u) for u in query_set]

def databases_list_from_users_db(query_set=None, db='default'):
    """Return a list of Database objects, one per active entry in VariantsDb."""
    manage_dbs.activate_deactivate_at_gemini_path()
    manage_dbs.diff_disk_VariantsDb()
    if query_set is None:
        query_set = VariantsDb.query.filter_by(is_active=1).all()
    return [database_factory(d) for d in query_set]

def roles_list_from_users_db(query_set=None, db='default'):
    """Create a list of Roles, one per entry in users_db.Roles"""
    if query_set is None:
        query_set = Roles.query.join('users','DbAccess','variantsdb').all()
    return [role_factory(d) for d in query_set]

def persons_list_from_db(query_set=None, db='default'):
    """Return a list of Persons, one per entry in users_db.People"""
    if query_set is None:
        query_set = People.query.join('users','DbAccess','variantsdb').all()
    return [person_factory(d) for d in query_set]

from varappx.models.users import *


class User:
    def __init__(self, username, email='', code='', salt='', is_active=0, person=None, role=None, dbs=None):
        self.username = username
        self.email = email
        self.salt = salt
        self.code = code
        self.is_active = is_active
        self.person = person
        self.role = role
        self.databases = dbs  # list of db names

    def expose(self):
        return {
            'username': self.username,
            'email': self.email,
            'code': self.code,
            'isActive': self.is_active,
            'role': self.role.expose(),
            'databases': [d.expose() for d in (self.databases or [])],
            'firstname': self.person.firstname,
            'lastname': self.person.lastname,
        }
    def __str__(self):
        return "<User {}>".format(self.username)


class Database:
    def __init__(self, name, location='', filename='', hashsum='', description='',
                 is_active=None, size=None, users=None):
        self.name = name
        self.location = location
        self.filename = filename
        self.hash = hashsum
        self.description = description
        self.is_active = is_active
        self.size = size
        self.users = users  # list of user names

    def expose(self):
        return {
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'users': self.users,
        }
    def __str__(self):
        return "<Database {}>".format(self.name)


class Role:
    def __init__(self, name, rank=99, can_validate_user=0, can_delete_user=0):
        self.name = name
        self.rank = rank
        self.can_validate_user = can_validate_user
        self.can_delete_user = can_delete_user

    def expose(self):
        return {
            'name': self.name,
            'rank': self.rank,
            'can_validate_user': self.can_validate_user,
            'can_delete_user': self.can_delete_user
        }
    def __str__(self):
        return "<Role {}>".format(self.name)


class Person:
    def __init__(self, firstname='', lastname='', institution='', street='', city='', phone='',
                 is_laboratory=0, laboratory=''):
        self.firstname = firstname
        self.lastname = lastname

    def expose(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
        }
    def __str__(self):
        return "<Person {} {}>".format(self.firstname, self.lastname)
