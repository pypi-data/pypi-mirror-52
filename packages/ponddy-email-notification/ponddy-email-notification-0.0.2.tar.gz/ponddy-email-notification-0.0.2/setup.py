import os

from setuptools import find_packages, setup


EXCLUDE_FROM_PACKAGES = [
    'core',
]


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='ponddy-email-notification',
    version=os.environ['CIRCLE_TAG'],
    url='https://github.com/ponddy-edu/ponddy-email-notification',
    author='Arthur Chang',
    author_email='arthurc0102@gmail.com',
    description='Ponddy email notification package',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=False,
    install_requires=[
        'django',
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='ponddy',
)
