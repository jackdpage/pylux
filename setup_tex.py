from pylux import __version__
from distutils.core import setup
import os 

HOME = os.path.expanduser('~/')
TEX = os.listdir('tex/')
TEXFILES = []

INSFILES = []
for texfile in TEX:
    TEXFILES.append('tex/'+texfile)
    print('Found LaTeX template '+texfile)
INSFILES.append((HOME+'texmf/tex/latex/base/', TEXFILES))
setup(name='Pylux',
      version=__version__,
      description='Suite for the management of lighting documentation',
      author='J. Page',
      author_email='jdpboc98@gmail.com',
      url='https://github.com/jackdpage/pylux',
      packages=[],
      data_files=INSFILES
      )
