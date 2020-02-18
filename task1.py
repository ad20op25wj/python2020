import sys

def print_usage():
    print('''Usage 1: python task1.py <log file name.clf> <group by> <information>
Usage 2: python task1.py <log file name> <group by> <information> <lines>
*****************************************************************************
<group by> --ip: IP Address / --http: HTTP Status Code
<information> -1: Request Count / -2: Request Count Percentage of All Logged Requests / -3: Total Number of Bytes Transferred
<lines> (e.g. --77) Limit of the Number of Rows Printed''')

def call_handler():
    if __name__ != '__main__':
        print("call_handler() can't be used as a module.")
        exit()

    args = len(sys.argv)
    lines = -1 # -1 means that args != 5

    if args != 4 and args != 5:
        print_usage()
        exit()

    # args == 4 or args == 5
    group_by = sys.argv[2].lower()
    if group_by != '--ip' and group_by != '--http':
        print_usage()
        exit()

    information = sys.argv[3]
    if information != '-1' and information != '-2' and information != '-3':
        print_usage()
        exit()

    # args != 4
    if args == 5:
        lines = sys.argv[4]
        if not lines.startswith('--') or not lines[2:].isalnum():
            print_usage()
            exit()
        lines = int(lines[2:])

    return (group_by, information, lines)

def token_extractor(line):
    tokens = line.split(' ', 3)
    remain = str(tokens[-1])[1:]
    tokens = tokens[:-1]

    tokens.extend(remain.split(']', 1))
    remain = str(tokens[-1])[2:]
    tokens = tokens[:-1]

    tokens.extend(remain.split('"', 1))
    remain = str(tokens[-1])[1:]
    tokens = tokens[:-1]

    tokens.extend(remain.split(' ', 2))
    tokens = tokens[:-1]

    try:
        tokens[-1] = int(tokens[-1])
    except: # tokens[-1] is '-'
        tokens[-1] = 0

    return tokens

def log_analyzer(key_index):
    log_stat = dict()
    total_request_number = 0
    file_name = sys.argv[1]

    if key_index == '--ip':
        key_index = 0
    else: # key == '--http'
        key_index = -2

    try:
        logfile = open(file_name, 'r')
        for line in logfile:
            total_request_number += 1

            tokens = token_extractor(line)

            key = tokens[key_index]
            if key not in log_stat:
                log_stat.update({key: [1, tokens[-1]]})
            else: # key in log_stat
                log_stat[key][0] += 1
                log_stat[key][1] += tokens[-1]
    except FileNotFoundError:
        print("Can't find <" + file_name + '>.')
        exit()
    
    logfile.close()

    return (log_stat, total_request_number)

def report(options, stat):
    log_stat = stat[0]
    total_request_num = stat[1]

    max_len = options[2]
    if max_len == -1: # -1 means there is no limit of the number of rows printed
        max_len = len(log_stat)

    information = options[1]
    if information == '-1' or information == '-2':
        log_table = sorted(log_stat.items(), key = lambda x:x[1][0], reverse = True)

        if information == '-1':
            print('*** Ranked by Request Count ***')
            print('{0: ^11s}|{1: ^21s}|{2: ^19s}'.format('No.', 'IP Address', 'Request Count'))
            for i in range(max_len):
                print('{0: ^11d}|{1: ^21s}|{2: ^19d}'.format(i + 1, log_table[i][0], log_table[i][1][0]))
        else: # information == '-2'
            print('*** Ranked by Request Count Percentage of All Logged Requests ***')
            print('{0: ^11s}|{1: ^21s}|{2: ^23s}'.format('No.', 'IP Address', 'Request Count (%)'))
            for i in range(max_len):
                print('{0: ^11d}|{1: ^21s}|{2: ^23.2f}'.format(i + 1, log_table[i][0], log_table[i][1][0]/total_request_num*100))
    else: # information == '-3'
        log_table = sorted(log_stat.items(), key = lambda x:x[1][1], reverse = True)

        print('*** Ranked by Total Number of Bytes Transferred ***')
        print('{0: ^11s}|{1: ^21s}|{2: ^23s}'.format('No.', 'IP Address', 'Transferred Bytes'))
        for i in range(max_len):
            print('{0: ^11d}|{1: ^21s}|{2: ^23d}'.format(i + 1, log_table[i][0], log_table[i][1][1]))

# main
options = call_handler()
stat = log_analyzer(options[0])
report(options, stat)