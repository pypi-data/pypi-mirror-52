from .handlers import setup_handlers
# Jupyter Extension points


def _jupyter_server_extension_paths():
    return [{
        'module': 'jupytergitcommit',
    }]


def _jupyter_nbextension_paths():
    return [{
        "section": "notebook",
        "dest": "jupytergitcommit",
        "src": "static",
        "require": "jupytergitcommit/main"
    }]


def load_jupyter_server_extension(nbapp):
    setup_handlers(nbapp.web_app)
