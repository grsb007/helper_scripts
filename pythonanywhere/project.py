from pathlib import Path
from pythonanywhere.api import Webapp
from pythonanywhere.exceptions import SanityException
from pythonanywhere.virtualenvs import Virtualenv


class Project:
    def __init__(self, domain, python_version, noverify=False):
        self.domain = domain
        self.python_version = python_version
        self.project_path = Path(f'~/{domain}').expanduser()
        self.virtualenv = Virtualenv(self.domain, self.python_version)
        self.wsgi_file_path = Path(f'/var/www/{domain.replace(".", "_")}_wsgi.py')
        self.webapp = Webapp(domain, noverify=noverify)


    def sanity_checks(self, nuke):
        self.webapp.sanity_checks(nuke=nuke)
        if nuke:
            return
        if self.virtualenv.path.exists():
            raise SanityException(f'You already have a virtualenv for {self.domain}.\n\nUse the --nuke option if you want to replace it.')
        if self.project_path.exists():
            raise SanityException(f'You already have a project folder at {self.project_path}.\n\nUse the --nuke option if you want to replace it.')


    def create_webapp(self, nuke):
        self.webapp.create(self.python_version, self.virtualenv.path, self.project_path, nuke=nuke)


    def add_static_file_mappings(self):
        self.webapp.add_default_static_files_mappings(self.project_path)

