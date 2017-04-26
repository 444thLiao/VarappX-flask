from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from varappx.models.users import loaddata,db
import sys


migrate = Migrate(db.app,db)
manager = Manager(db.app)
manager.add_command('db',MigrateCommand)


if __name__ == "__main__":
    if 'loaddata' in sys.argv:
        loaddata()
    else:
        manager.run()