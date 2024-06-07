colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def fail(msg):
    print(colors['FAIL'] + '[FAIL] ' + msg + colors['ENDC'])

def warn(msg):
    print(colors['WARNING'] + '[WARN] ' + msg + colors['ENDC'])

def ok(msg):
    print(colors['OKCYAN'] + '[OK] ' + msg + colors['ENDC'])

def info(msg):
    print('[LOG] ' + msg)