import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='pylux',
    version='1.0',
    author='Jack Page',
    author_email='jdpboc98@gmail.com',
    description='Program for creating stage and entertainment lighting documentation',
    long_description=long_description,
    url='https://github.com/jackdpage/pylux',
    package_data={'pylux': ['config.ini']},
    entry_points={
        'console_scripts': [
            'pylux = pylux.__main__:main'
        ]
    },
    install_requires=['urwid', 'jinja2', 'numpy', 'pygdtf'],
    packages=['pylux', 'pylux.interface', 'pylux.lib', 'pylux.interpreter']
)
