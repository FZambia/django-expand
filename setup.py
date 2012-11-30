import sys
import platform
from distutils import log
from distutils.core import setup


requires = ["django>=1.4.1"]


# PyPy and setuptools don't get along too well, yet.
if sys.subversion[0].lower().startswith('pypy'):
    from distutils.core import setup
    extra = dict(requires=requires)
else:
    from setuptools import setup
    extra = dict(install_requires=requires)


setup(
    name="django-ease",
    version="0.1.0",
    author="Alexandr Emelin",
    author_email="frvzmb@gmail.com",
    url="https://github.com/FZambia/cyclone-sse",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Easily create rest skeleton based on django model, including templates, views, urls etc",
    keywords="python django rest",
    packages=["expand", "expand.management", "expand.management.commands"],
    package_data={"expand": ["templates/*", "pyfiles/*"]},
    **extra
)
