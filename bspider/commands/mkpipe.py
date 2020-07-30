import os
from os.path import join, exists

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile
from bspider.utils.tools import class_name2module_name

TEMPLATES_TO_RENDER = (
    ('pipeline.py.tmpl',),
)


class Command(BSpiderCommand):

    def syntax(self):
        return "<pipeline name like DemoPipeline>"

    def short_desc(self):
        return "Create new pipeline in current platform"

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError('args error')

        pipeline_name = args[0]
        file_name = f'{class_name2module_name(pipeline_name)}.py'
        project_dir = join(os.environ[PLATFORM_PATH_ENV], 'pipeline')
        if exists(join(project_dir, file_name)):
            self.exitcode = 1
            print(f'Error: pipeline: {pipeline_name} already exists in this platform')
            return

        self._copytree(join(self.templates_dir, 'pipeline'), project_dir)
        for paths in TEMPLATES_TO_RENDER:
            tplfile = join(project_dir, *paths)
            new_file = join(project_dir, file_name)
            render_templatefile(tplfile, new_file=new_file, pipeline_name=pipeline_name)

        print(f"New pipeline '{pipeline_name}' init success")
        print(f"    template directory:\n    '{self.templates_dir}'")


if __name__ == '__main__':
    Command().run(['Hello_project'])
