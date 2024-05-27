import os

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv("FLASK_CONFIG", None))
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "db": db,
        "User": User,
        "Role": Role,
    }


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    print("upgrading")
    upgrade()
    print("finished upgrade")
    Role.insert_roles()
