import sys

from win32con import MB_OK, MB_ICONASTERISK
import win32ui


from igs_header_parser import igs_header_parser
from stp_header_parser import stp_header_parser


class igs_stp_header_parser(igs_header_parser, stp_header_parser):

    def __init__(self):
        pass


def main_entry():

    #     sys.argv.append('igs')
    #     sys.argv.append('4.igs')
    #     sys.argv.append('stp')
    #     sys.argv.append('as1-oc-214.stp')

    if sys.argv.__len__() >= 3:

        filename = sys.argv[2]

        if filename:

            ishp = igs_stp_header_parser()

            if sys.argv[1] == 'igs':
                headerinfos_dict = ishp.igs_header_parser(filename)

            elif sys.argv[1] == 'stp':
                headerinfos_dict = ishp.stp_header_parser(filename)

            if headerinfos_dict:
                message = '\n'.join(
                    '{:02} - {}'.format(
                        key,
                        ' : '.join(headerinfos_dict[key])) for key in headerinfos_dict)
                version = 'IGS/STP Header Parser Version 1.0 by Ray Wang'
                header = 'ID - KEY : VALUE'
                sep = '--------------------------------------------------------------------'
                win32ui.MessageBox(
                    filename + '\n\n' + header +
                    '\n' + sep + '\n' + message,
                    version,
                    MB_OK + MB_ICONASTERISK)
#                 import ctypes
#                 MessageBox = ctypes.windll.user32.MessageBoxW
#                 MessageBox(None, 'Hello', 'Window title', 0)

if __name__ == '__main__':
    main_entry()
