import sys

from cx_Freeze import setup, Executable

sys.argv.append('build')

options = {'build_exe':
           {'compressed': True,
            'includes': [],
            'excludes': [],
            'include_files': ['icon48x48.ico',
                              'Reg_Install.reg',
                              'Reg_Uninstall.reg'],
            }
           }

# base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'
executables = [Executable('igs_stp_header_parser.py',
                          icon='icon48x48.ico',
                          base='Win32GUI',  # base='Console',
                          targetName='igs_stp_header_parser.exe')]

setup(name='igs_stp_header_parser',
      version='0.1',
      description='igs_stp_header_parser',
      # author='',
      # author_email='',
      options=options,
      executables=executables
      )
