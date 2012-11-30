from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from optparse import make_option
import sys
import os


class Command(BaseCommand):
    help = 'Helps to create rest django environment from model'

    option_list = BaseCommand.option_list + (
        make_option('--app',
            dest='app',
            default=None,
            help='app to work with'),
        make_option('--model',
            dest='model',
            default=None,
            help='model to work with'),
        make_option('--append',
            action='store_true',
            dest='append',
            default=False,
            help='Append data to existing files for new model'),
    )

    def handle(self, *args, **options):
        self.append = options['append']
        appname = options['app']
        modelname = options['model']

        if not appname or not modelname:
            print 'Please, provide both app and model options.'
            sys.exit(1)

        self.model = get_model(appname, modelname)
        if not self.model:
            msg = "Model not found.\nMake sure you provided correct app and model name.\nAlso check that app is in INSTALLED_APPS."
            print msg
            sys.exit(1)

        self.modelname = self.model.__name__
        self.appname = self.model._meta.app_label
        self.folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.create_templates()
        self.create_views()
        self.create_urls()
        self.create_forms()
        self.create_admin()

    def create_templates(self):
        # create template directory in app's folder
        dst_templates = os.path.abspath(os.path.join(self.appname, 'templates'))
        if not os.path.exists(dst_templates):
            os.mkdir(dst_templates, 0755)
        dst = os.path.join(dst_templates, self.appname)
        if not os.path.exists(dst):
            os.mkdir(dst, 0755)

        # move templates to app's folder
        template_dir = os.path.join(self.folder, 'templates')
        template_names = os.listdir(template_dir)
        for template_name in template_names:
            template = os.path.join(template_dir, template_name)
            with open(template, 'r') as f:
                content = f.read()
            content = content.replace('$APP', self.appname.lower())
            content = content.replace('$MODEL', self.modelname.lower())
            dst_name = template_name.replace('model', self.modelname.lower())
            dst_path = os.path.join(dst, dst_name)
            if os.path.exists(dst_path):
                print '%s template already exists. Continue without any modifications.' % dst_name
                continue
            with open(dst_path, 'w', 0644) as f:
                f.write(content)

    def create_file(self, name):
        """
        creates file with content specific for model
        """
        if self.append:
            # append to file
            mode = 'a'
        else:
            # write to file
            mode = 'w'

        src = os.path.join(self.folder, 'pyfiles', name)

        name = name + ".py"
        dst = os.path.abspath(os.path.join(self.appname, name))
        if os.path.exists(dst) and not self.append:
            print '%s already exists. Continue without any modifications.' % name
            return
        
        # get file content
        with open(src, 'r') as f:
            content = f.read()

        # make replacements
        content = content.replace('$LOWERAPP', self.appname.lower())
        content = content.replace('$LOWERMODEL', self.modelname.lower())
        content = content.replace('$APP', self.appname)
        content = content.replace('$MODEL', self.modelname)
        if self.append:
            # remove all import and encoding cause we suppose file already has them
            lines = [x for x in content.split('\n') if x.find('import') == -1 and x.find('utf-8') == -1]
            content = "\n" + "\n".join(lines)
            # urls.py specific
            content = content.replace('urlpatterns = ', 'urlpatterns += ')
        with open(dst, mode, 0644) as f:
            f.write(content)

    def create_views(self):
        self.create_file('views')

    def create_urls(self):
        self.create_file('urls')

    def create_forms(self):
        self.create_file('forms')

    def create_admin(self):
        self.create_file('admin')





