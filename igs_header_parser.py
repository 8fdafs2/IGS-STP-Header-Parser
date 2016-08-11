import re


class igs_header_parser():

    def igs_header_parser(self, igs_filename='', is_debug=False):

        lines_S = []
        lines_G = []

        infos_name = [
            # index 00
            'Prologue',  # required, no default
            # index 01
            'Parameter Delimiter Character',
            # required, default = ,
            # index 02
            'Record delimiter character',  # required, default = ;
            # index 03
            'Product Identification from Sender',
            # required, no default
            # index 04
            'File Name',  # required, no default
            # index 05
            'Native System ID',  # required, no default
            # index 06
            'Preprocessor Version',  # required, no default
            # index 07
            # required, no default
            'Number of Binary Bits for Integer Representation',
            # index 08
            'Single-Precision Magnitude',  # required, no default
            # index 09
            'Single-Precision Significance',  # required, no default
            # index 10
            'Double-Precision Magnitude',  # required, no default
            # index 11
            'Double-Precision Significance',  # required, no default
            # index 12
            'Product Identification for the Receiver',
            # required, default = consistent with 'Product Identification from Sender'
            # index 13
            'Model Space Scale',  # required, default = 1.0
            # index 14
            'Units Flag',  # required, default = 1
            # 1   Inches (default)
            # 2   Millimeters
            # 3   (See Parameter 15 for name of units)
            # 4   Feet
            # 5   Miles
            # 6   Meters
            # 7   Kilometers
            # 8   Mils (i.e., 0.001 inch)
            # 9   Microns
            # 10  Centimeters
            # 11  Microinches
            # index 15
            'Units Name',
            # required, default = consistent with 'Units Flag'
            # IN / INCH
            # MM
            # FT
            # MI
            # M
            # KM
            # MIL
            # UM
            # CM
            # UIN
            # index 16
            'Maximum Number of Line Weight Gradations',
            # required, default = 1
            # index 17
            'Width of Maximum Line Weight in Units',
            # required, no default
            # index 18
            'Date and Time of Exchange File Generation',
            # required, no default
            # 15HYYYYMMDD.HHNNSS or 13HYYMMDD.HHNNSS
            # where:
            # YYYY or YY is 4 or 2 digit year  HH is hour (00-23)
            # MM is month (01-12)  NN is minute (00-59)
            # DD is day (01-31)  SS is second (00-59)
            # index 19
            'Minimum User-Intended Resolution',
            # required, no default
            # index 20
            'Approximate Maximum Coordinate Value',
            # required, default = 0.0
            # index 21
            'Name of Author',  # required, default = NULL
            # index 22
            'Author\'s Organization',  # required, default = NULL
            # index 23
            'Version Flag',  # required, default = 3
            # 1   1.0                         [NBS80]
            # 2   ANSI Y14.26M -1981          [ANSI81]
            # 3   2.0                         [NBS83] (default)
            # 4   3.0                         [NBS86]
            # 5   ASME/ANSI  Y14.26M  -1987   [ASME87]
            # 6   4.0                         [NBS88]
            # 7   ASME  Y14.26M  -1989        [ASME89]
            # 8   5.0                         [NIST90]
            # 9   5.1                         [USPRO91]
            # 10  USPRO/IPO100  IGES5.2       [USPRO93]
            # 11  5.3
            # index 24
            'Drafting Standard Flag',  # required, default = 0
            # 0    None    No standard specified (default)
            # 1    ISO     International organization for Standardization
            # 2    AFNOR   French Association for Standardization
            # 3    ANSI    American National Standards Institute
            # 4    BSI     British Standards Institute
            # 5    CSA     Canadian Standards Association
            # 6    DIN     German Institute for Standardization
            # 7    JIS     Japanese Institute for Standardization
            # index 25
            'Date and Time Model was Created or Modified',
            # required,  default = NULL
            # index 26
            'Application Protocol/Subset Identifier',
            # required, default = NULL
        ]

        units_name = [
            'IN',
            'MM',
            'FT',
            'MI',
            'M',
            'KM',
            'MIL',
            'UM',
            'CM',
            'UIN',
        ]

        ptrn_0 = re.compile(r'(\d*)[H,]')

        with open(igs_filename, 'r') as f:
            while(True):
                line = f.readline()
                if line[-9] == 'S':
                    lines_S.append(line)
                elif line[-9] == 'G':
                    lines_G.append(line)
                else:
                    break

        # Start Section - a human readable prologue to the file.
        # It contains one or more lines
        # using ASCII characters in columns 1-72.
        if lines_S:
            line_S = ''.join([line_S[:-9] for line_S in lines_S]).rstrip()
        else:
            line_S = ''

        # Global Section - sending system and file information.
        # It  contains  the  number  of  lines  needed  to  hold  the  parameter  fields,  separated  by
        # parameter delimiters, and terminated by one record delimiter, in columns
        # 1-72.
        line_G = ''.join([line_G[:-9] for line_G in lines_G]).rstrip()

        matched = ptrn_0.match(line_G, 0)
        index_start = matched.end()

        try:
            int(matched.group(1))
        except ValueError:
            parameter_delimiter = ','
        else:
            parameter_delimiter = line_G[index_start: index_start + 1]

        line_G = line_G[index_start + 2:].lstrip()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        matched = ptrn_0.match(line_G, 0)
        index_start = matched.end()

        try:
            int(matched.group(1))
        except ValueError:
            record_delimiter = ';'
        else:
            record_delimiter = line_G[index_start: index_start + 1]

        line_G = line_G[index_start + 2:].lstrip()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        ptrn_0 = re.compile(r'(\d*)H')
        ptrn_1 = re.compile(r'(.*?)' + parameter_delimiter)
        ptrn_2 = re.compile(r'(.*?)' + record_delimiter)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        infos_value = [
            line_S,
            parameter_delimiter,
            record_delimiter,
        ]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        while True:

            matched = ptrn_0.match(line_G, 0)
            if matched:
                index_start = matched.end()
                try:
                    index_end = index_start + int(matched.group(1))
                except ValueError:
                    index_end = index_start - 1
                    parameter_value = ''
                else:
                    parameter_value = line_G[index_start: index_end]
            else:
                matched = ptrn_1.match(line_G, 0)
                if matched:
                    index_start = matched.start()
                    index_end = matched.end() - 1
                    parameter_value = line_G[index_start: index_end]
                else:
                    matched = ptrn_2.match(line_G, 0)
                    if matched:
                        index_start = matched.start()
                        index_end = matched.end() - 1
                        parameter_value = line_G[index_start: index_end]
                    else:
                        if is_debug:
                            print('>>> Block End Mark Not Found <<<')
                    break

            infos_value.append(parameter_value)
            line_G = line_G[index_end + 1:].lstrip()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        len_infos_value = len(infos_value)
        len_infos_name = len(infos_name)

        if len_infos_value < len_infos_name:
            infos_value += [''] * (len_infos_name - len_infos_value)

        infos_dict = {
            index: list(parameter) for (
                index, parameter) in zip(
                range(len_infos_name), zip(
                    infos_name, infos_value))}

        if is_debug:
            for key in infos_dict:
                print('{:02}\t{}'.format(key, infos_dict[key]))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if not infos_dict[12][1]:
            infos_dict[12][1] = infos_dict[3][1]

        if not infos_dict[13][1]:
            infos_dict[13][1] = '1.0'

        if not infos_dict[14][1]:
            infos_dict[14][1] = '1'
            if not infos_dict[15][1]:
                infos_dict[15][1] = 'IN'
        elif infos_dict[14][1] == '3':
            if not infos_dict[15][1]:
                infos_dict[15][1] = 'IN'
        else:
            infos_dict[15][1] = units_name[int(infos_dict[14][1]) - 1]

        if not infos_dict[16][1]:
            infos_dict[16][1] = '1'

        if not infos_dict[20][1]:
            infos_dict[20][1] = '0.0'

        if not infos_dict[23][1]:
            infos_dict[23][1] = '3'

        if not infos_dict[24][1]:
            infos_dict[24][1] = '0'

        if is_debug:
            for key in infos_dict:
                print('{:02}\t{}'.format(key, infos_dict[key]))

        return infos_dict
