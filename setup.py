from setuptools import setup, find_packages

setup(
    name = "django-serverconf",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        'django>=1.3',
    ],
    include_package_data = True,
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
