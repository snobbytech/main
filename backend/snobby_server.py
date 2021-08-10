from app import flask_app

@flask_app.shell_context_processor
def make_shell_context():
    return {}
