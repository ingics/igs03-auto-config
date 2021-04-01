import time
import getopt
import logging
import telnetlib

logger = logging.getLogger()

class IgsCmdError(Exception):
    def __init__(self, rst, cmd):
        self.rst = rst
        self.cmd = cmd
        super().__init__("\'%s\' return %d" % (self.cmd, self.rst))

def connect(host, username, password, retry = 5):
    count = 1
    while True:
        logger.log(logging.INFO, 'Connecting, try ' + str(count) + ' ...')
        try:
            client = telnetlib.Telnet(host)
            logger.log(logging.INFO, 'Login as ' + username + ', ' + password)
            client.read_until(b'login:')
            client.write(username.encode() + b'\n')
            client.read_until(b'password:')
            client.write(password.encode() + b'\n')
            data = client.read_until(b'>', 3)
            if len(data) == 0 or data.decode('utf8') != '>':
                raise Exception('Wrong password')
            client.exec = lambda cmd, *args, **kwargs: exec(client, cmd, *args, **kwargs)
            client.get = lambda cmd: get(client, cmd)
            client.reboot = lambda *args, **kwargs: exec(client, 'REBOOT', expect_close=True)
            client.reset = lambda *args, **kwargs: exec(client, 'REBOOT DEFAULT', expect_close=True)
            logger.log(logging.INFO, 'Logged in ...')
            return client
        except OSError as e:
            count += 1
            logger.log(logging.ERROR, 'Fail to loggin, ' + str(e))
            if count > retry:
                raise e
            else:
                time.sleep(3)

def exec(client, cmd, *args, ignore_error_4=False, expect_close=False):
    if len(args) > 0:
        for arg in args:
            cmd = cmd + ' "' + str(arg) + '"'
    # logger.log(logging.INFO, cmd)
    try:
        client.write(cmd.encode() + b'\n')
        data = client.read_until(b'RESULT:').decode('utf8')[:-9].strip()
        result = int(client.read_until(b'>').decode('utf8')[:-1].strip())
        if ignore_error_4 and result == 4:
            return ''
        elif result != 0:
            raise IgsCmdError(result, cmd)
        return data
    except EOFError as e:
        if expect_close:
            client.close()
            logger.log(logging.INFO, "Connection closed")
            return ''
        else:
            raise e

def get(client, cmd):
    # logger.log(logging.INFO, cmd)
    ans = client.exec(cmd)
    return ans.split('=')[1]
