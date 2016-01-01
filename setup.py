from pylux import __version__
from distutils.core import setup
import os 

HOME = os.path.expanduser('~/')
FIXTURES = os.listdir('fixture/')
TEX = os.listdir('tex/')
EXTENSIONS = os.listdir('extension/')
TEXFILES = []
FIXFILES = []
EXTFILES = []

INSFILES = [(HOME+'.pylux/', ['pylux.conf'])]
for texfile in TEX:
    TEXFILES.append('tex/'+texfile)
for fixfile in FIXTURES:
    FIXFILES.append('fixture/'+fixfile)
for extfile in EXTENSIONS:
    EXTFILES.append('extension/'+extfile)
INSFILES.append((HOME+'.pylux/fixture/', FIXFILES))
INSFILES.append((HOME+'texmf/tex/latex/base/', TEXFILES))
INSFILES.append((HOME+'.pylux/extension/', EXTFILES))
print(INSFILES)
setup(name='Pylux',
      version=__version__,
      description='Suite for the management of lighting documentation',
      author='J. Page',
      author_email='jdpboc98@gmail.com',
      url='https://github.com/jackdpage/pylux',
      packages=['pylux'],
      data_files=INSFILES
      )
