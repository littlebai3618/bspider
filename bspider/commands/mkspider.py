import os
from os.path import join, exists

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile
from bspider.utils.tools import module_name2class_name

TEMPLATES_TO_RENDER = (
    ('__init__.py.tmpl',),
    ('extractor.py.tmpl',),
    ('settings-development.yml.tmpl',),
    ('settings-production.yml.tmpl',),
)


class Command(BSpiderCommand):

    def syntax(self):
        return "<spider_name>"

    def short_desc(self):
        return "Create new spider in current platform"

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError('args error')

        project_name = args[0]
        project_dir = join(os.environ[PLATFORM_PATH_ENV], 'projects', project_name)
        if exists(project_dir):
            self.exitcode = 1
            print(f'Error: {project_name} already exists in this platform')
            return

        self._copytree(join(self.templates_dir, 'spiders'), project_dir)
        for paths in TEMPLATES_TO_RENDER:
            tplfile = join(project_dir, *paths)
            render_templatefile(tplfile, project_name=project_name, ProjectName=module_name2class_name(project_name))

        print(f"New spider '{project_name}' init success")
        print(f"    template directory:\n    '{self.templates_dir}'")
        print("You can development your spider in:")
        print(f"    cd {project_dir}")


if __name__ == '__main__':
    Command().run(['hello_project'])
