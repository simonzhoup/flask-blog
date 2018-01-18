from blog import create_blog
from flask_script import Manager
from blog import db
from flask_migrate import Migrate, MigrateCommand

blog = create_blog()
manager = Manager(blog)
migrate = Migrate(blog, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
