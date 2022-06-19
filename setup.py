from setuptools import setup

setup(
    name='bot_helper_py',
    url='https://github.com/overthejuncture/bot_helper_py.git',
    author='OTJ',
    author_email='overthejuncure@gmail.com',
    # Needed to actually package something
    packages=['bot'],
    # Needed for dependencies
    install_requires=[],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
