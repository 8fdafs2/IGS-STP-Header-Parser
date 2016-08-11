class stp_header_parser():

    def stp_header_parser(self, stp_filename='', is_debug=False):

        def line_extract(filehandle=None, str_startswith='', str_endswith=''):

            while True:

                line = filehandle.readline().strip()
                if line.startswith(str_startswith):

                    line_extracted = ''
                    while True:
                        line_extracted += line
                        if line.endswith(str_endswith):
                            break
                        else:
                            line = filehandle.readline().strip()

                    return line_extracted

        infos_name = [
            'ISO Standard',
            'Description',
            'Implementation Level',
            'Name',
            'Time_Stamp',
            'Author',
            'Organization',
            'Preprocessor Version',
            'Originating System',
            'Authorization',
            'Schema',
        ]

        infos_value = []

        len_infos_name = len(infos_name)

        with open(stp_filename, 'r') as f:

            line = line_extract(f, 'ISO-', ';')

            if line:
                ISO_Standard = line[:-1]
                infos_value.append(ISO_Standard)

            line = line_extract(f, 'HEADER', ';')

            if line:
                if is_debug:
                    print('>>> Header Start Mark Found <<<')

                line = line_extract(f, 'FILE_DESCRIPTION', ';')
                File_Description = eval(line[16:-1])
                infos_value += File_Description

                line = line_extract(f, 'FILE_NAME', ';')
                File_Name = eval(line[9:-1])
                infos_value += File_Name

                line = line_extract(f, 'FILE_SCHEMA', ';')
                File_Schema = eval(line[11:-1])
                infos_value.append(File_Schema)

                if line_extract(f, 'ENDSEC', ';'):
                    if is_debug:
                        print('>>> Header End Mark Found <<<')

        infos_dict = {
            index: list(parameter) for (
                index, parameter) in zip(
                range(len_infos_name), zip(
                    infos_name, infos_value))}

        if is_debug:
            for key in infos_dict:
                print('{:02}\t{}'.format(key, infos_dict[key]))

        return infos_dict
