import sys

def print_usage():
    print('''Usage 1: python task1.py <log file name.clf> <group by> <information>
Usage 2: python task1.py <log file name.clf> <group by> <information> <lines>
*****************************************************************************
<group by> --ip: IP Address / --http: HTTP Status Code
<information> -1: Request Count / -2: Request Count Percentage of All Logged Requests / -3: Total Number of Bytes Transferred
<lines> (e.g. --77) Limit of the Number of Rows Printed''')

def call_handler():
    if __name__ != '__main__':
        print("call_handler() can't be used as a module")
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
        print(lines)

    return (group_by, information, lines)

options = call_handler()
print(options)

'''
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as logfile:
        for line in logfile:
            print(line)
'''