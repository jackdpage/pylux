from pylux import __version__
from distutils.core import setup
import os 

TARGET = '/usr/share/pylux/'
FIXTURES = os.listdir('fixture/')
TEX = os.listdir('tex/')
EXTENSIONS = os.listdir('extension/')
SYMBOLS = os.listdir('symbol/')
TEXFILES = []
FIXFILES = []
EXTFILES = []
SYMFILES = []

INSFILES = [(TARGET, ['pylux.conf'])]
for texfile in TEX:
    TEXFILES.append('tex/'+texfile)
    print('Found LaTeX template '+texfile)
for fixfile in FIXTURES:
    FIXFILES.append('fixture/'+fixfile)
    print('Found fixture file '+fixfile)
for extfile in EXTENSIONS:
    EXTFILES.append('extension/'+extfile)
    print('Found extension '+extfile)
for symfile in SYMBOLS:
    SYMFILES.append('symbol/'+symfile)
    print('Found fixture symbol '+symfile)
INSFILES.append((TARGET+'fixture/', FIXFILES))
#INSFILES.append((HOME+'texmf/tex/latex/base/', TEXFILES))
INSFILES.append((TARGET+'extension/', EXTFILES))
INSFILES.append((TARGET+'symbol/', SYMFILES))
setup(name='Pylux',
      version=__version__,
      description='Suite for the management of lighting documentation',
      author='J. Page',
      author_email='jdpboc98@gmail.com',
      url='https://github.com/jackdpage/pylux',
      packages=['pylux'],
      data_files=INSFILES
      )
