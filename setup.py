from pylux import __version__
from distutils.core import setup
import os 

TARGET = '/usr/share/pylux/'
HOME = os.path.expanduser('~/')
FIXTURES = os.listdir('fixture/')
EXTENSIONS = os.listdir('extension/')
SYMBOLS = os.listdir('symbol/')
TEMPLATES = os.listdir('template/')
FIXFILES = []
EXTFILES = []
SYMFILES = []
TEMFILES = []

INSFILES = [(TARGET, ['pylux.conf'])]
for fixfile in FIXTURES:
    FIXFILES.append('fixture/'+fixfile)
    print('Found fixture file '+fixfile)
for extfile in EXTENSIONS:
    EXTFILES.append('extension/'+extfile)
    print('Found extension '+extfile)
for symfile in SYMBOLS:
    SYMFILES.append('symbol/'+symfile)
    print('Found fixture symbol '+symfile)
for temfile in TEMPLATES:
    TEMFILES.append('template/'+temfile)
    print('Found template '+temfile)
INSFILES.append((TARGET+'fixture/', FIXFILES))
INSFILES.append((TARGET+'extension/', EXTFILES))
INSFILES.append((TARGET+'symbol/', SYMFILES))
INSFILES.append((TARGET+'template/', TEMFILES))
setup(name='Pylux',
      version=__version__,
      description='Suite for the management of lighting documentation',
      author='J. Page',
      author_email='jdpboc98@gmail.com',
      url='https://github.com/jackdpage/pylux',
      packages=['pylux'],
      data_files=INSFILES
      )
