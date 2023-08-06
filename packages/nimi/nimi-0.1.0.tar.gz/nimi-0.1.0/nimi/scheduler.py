import sys

if sys.platform == 'darwin':
    import launchd
elif sys.platform == 'linux':
    import crontab
else:
    raise NotImplementedError('Platform {} is not supported by scheduler'.format(sys.platform))


def schedule(url, hostname, secret, rate=5):
    if sys.platform == 'darwin':
        pass
    elif sys.platform == 'linux':
        pass


def unschedule():
    if sys.platform == 'darwin':
        pass
    elif sys.platform == 'linux':
        pass