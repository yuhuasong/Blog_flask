import os

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

config_name = os.environ.get('FLASK_CONFIG') or 'default'

app = create_app(config_name)

manager = Manager(app)

manager.add_command('db',MigrateCommand)


if __name__ =='__main__':
    manager.run()












