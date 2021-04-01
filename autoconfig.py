import sys
import logging
from igscli import connect
from zeroconf import ServiceBrowser, Zeroconf

logging.basicConfig(
    stream = sys.stdout,
    level = logging.DEBUG,
    format = '[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger('__main__')

class MyListener:

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if 'IGS03E' in info.name:
            ip = info.parsed_addresses()[0]
            logger.info('Found %s at %s' % (name, ip))
            client = connect(ip, 'admin', 'admin')
            # configurate HTTP CN_CHECK (example)
            value = client.get('HTTP CN_CHECK')
            logging.info('Get HTTP CN_CHECK = %s' % value)
            if value != '1':
                logging.info('Set HTTP CN_CHECK = 1')
                client.exec('HTTP CN_CHECK', 1)
            # add more configurate
            # done
            client.close()

    def update_service(self, zeroconf, type, name):
        pass

    def remove_service(self, zeroconf, type, name):
        pass

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_ble-gw._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
