import os
import sys

from setuptools import setup, find_packages, Command


class RunTests(Command):
    description = "Run the django test suite from the test_project dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "test_project")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                        "DJANGO_SETTINGS_MODULE", "settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        execute_manager(settings_mod, argv=[
            __file__, "test"])
        os.chdir(this_dir)


setup(
    name = "django-serverconf",
    version = "0.1",
    packages = find_packages(exclude=['test_project']),
    install_requires = [
        'django>=1.3',
    ],
    include_package_data = True,
    cmdclass = {"test": RunTests},
    author="Stefan Kjartansson",
    author_email="esteban.supreme@gmail.com",
    description="Server Configuration Helpers",
    zip_safe = False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
