import os


def _escape_command_unix(command):
    return repr(command)[1:-1]


def run(command):
    execute = 'termite -e "{}"'.format(_escape_command_unix(command))
    os.system(execute)


def run_test():
    run('ancypwn attach -c \'/usr/bin/gdb /bin/echo\'')


if __name__ == '__main__':
    run_test()
