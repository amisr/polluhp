#!/usr/bin/env python
################################################################################
#
#    Title: PollUHP.py
#
#    Author: asreimer
#
#    Description: This class was built to poll the status pages of a ViaSat
#                 SurfBeam 2 Satellite Modem. The modem is accessed via an IP
#                 address of 192.168.100.1. This script gets both the TRIA and
#                 modem status.
#
#                 This script assumes modem software version: UT_2.2.4.11.0
#
################################################################################

import time
import requests
from bs4 import BeautifulSoup

class PollUHP():

    HEADER_URL = 'http://%s/h'
    STATUS_URL = 'http://%s/ss40.htm'
    TXMOD_URL = 'http://%s/ss32.htm'
    RXMOD_URL = 'http://%s/ss33.htm'

    def __init__(self,address,timeout=5,retrytime=1):
        # need to make a call to request the UHP-200 html pages
        self.query_header_url = self.HEADER_URL % (address)
        self.query_modem_url = self.STATUS_URL % (address)
        self.query_tx_url = self.TXMOD_URL % (address)
        self.query_rx_url = self.RXMOD_URL % (address)

        # initialize some output params
        self.header_status_raw = None
        self.modem_status_raw = None
        self.tx_status_raw = None
        self.rx_status_raw = None
        self.status = dict()
        self.status['modem'] = dict()
        self.status['tx'] = dict()
        self.status['rx'] = dict()
        self.timeout = timeout
        self.retrytime = retrytime
        self.address = address


    def __do_poll(self,url):
        # poll url
        num_tries = 0
        status = 0
        while num_tries < 3:
            try:
                r = requests.get(url, timeout=self.timeout)
                status = r.status_code
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                status = 0
            if status == 200:
                break
            num_tries += 1
            time.sleep(self.retrytime)
        if status == 200:
            return r.text
        else:
            return None


    # poll the modem for modem, tx, and rx statuses then parse the raw response
    def poll(self):
        # poll the page header
        self.header_status_raw = self.__do_poll(self.query_header_url)
        # poll the modem status
        self.modem_status_raw = self.__do_poll(self.query_modem_url)
        # parse the modem info from the header and status page
        self.parse_modem_status()

        # poll modem status
        self.tx_status_raw = self.__do_poll(self.query_tx_url)
        self.parse_tx_status()
        
        # poll modem status
        self.rx_status_raw = self.__do_poll(self.query_rx_url)
        self.parse_rx_status()


    def parse_modem_status(self):
        # replicates some of the functionality in "scripts.js" in the
        # "decodeAndUpdateModemStatus()" function.
        if (self.header_status_raw is None) and (self.modem_status_raw is None):
            self.status['modem']['poll_results'] = 'Fail'
            return
        else:
            self.status['modem']['poll_results'] = 'Success'

        # extract the name and uptime of the modem
        if not self.header_status_raw is None:
            temp = self.header_status_raw.encode('utf-8')
            bs = BeautifulSoup(temp,features="html.parser")
            # extract name and uptime in the "st1" class
            # format is title:value in <p></p>:<h3></h3>
            t = bs.find("div",{"class":"st1"})
            h3s = t.find_all('h3')

            self.status['modem']['name'] = h3s[0].contents[0]
            self.status['modem']['uptime'] = h3s[1].contents[0]
            self.status['modem']['profile'] = h3s[2].a.contents[0]


        if not self.modem_status_raw is None:
            temp = self.modem_status_raw.encode('utf-8')
            bs = BeautifulSoup(temp,features="html.parser")

            tds = bs.find_all('td')
            # extract the serial number
            self.status['modem']['hwserial'] = tds[1].contents[1].contents[0]
            # extract sw version
            swver = tds[1].td.b.contents[0]
            swver += ' ' + tds[1].td.b.td.b.contents[0]
            self.status['modem']['swversion'] = swver
            # cpu load
            self.status['modem']['cpuload'] = tds[4].b.contents[0]
            # buffers
            self.status['modem']['buffers'] = tds[5].b.contents[0]
            # temperature
            self.status['modem']['temp'] = tds[6].b.contents[0]
            # ethernet status
            self.status['modem']['ethstatus'] = tds[9].contents[0]
            self.status['modem']['ethlinkstate'] = tds[10].b.contents[0]
            # demod1 status
            self.status['modem']['demod1status'] = tds[15].contents[0]
            # demod2 status
            self.status['modem']['demod2status'] = tds[21].contents[0]
            # modulator status
            self.status['modem']['modstatus'] = tds[27].contents[0]


    def parse_tx_status(self):

        if self.tx_status_raw is None:
            self.status['tx']['poll_results'] = 'Fail'
            return
        else:
            self.status['tx']['poll_results'] = 'Success'

        temp = self.tx_status_raw.split('\n')
        
        # uplink and downlink
        self.status['tx']['u2d'] = ' '.join(temp[1].split(' ')[2:4])
        self.status['tx']['d2u'] = ' '.join(temp[2].split(' ')[2:4])
        # levels
        line = [x for x in temp[4].split(' ') if x != '']
        self.status['tx']['setlvl'] = line[7]
        self.status['tx']['10M'] = line[11]
        line = [x for x in temp[5].split(' ') if x != '']
        self.status['tx']['outlvl'] = line[7]
        self.status['tx']['24V'] = line[11]

        # packets, bytes, and drops
        self.status['tx']['packets'] = sum([int(x[14:26]) for x in temp[11:17]])
        self.status['tx']['bytes'] = sum([int(x[33:45]) for x in temp[11:17]])
        self.status['tx']['drops'] = sum([int(x[74:]) for x in temp[11:17]])


    def parse_rx_status(self):

        if self.rx_status_raw is None:
            self.status['rx']['poll_results'] = 'Fail'
            return
        else:
            self.status['rx']['poll_results'] = 'Success'

        temp = self.rx_status_raw.split('\n')

        # uplink and downlink
        self.status['rx']['u2d'] = ' '.join(temp[1].split(' ')[2:4])
        self.status['rx']['d2u'] = ' '.join(temp[2].split(' ')[2:4])

        # in level and C/N
        line = [x for x in temp[8].replace('|','').split(' ') if x != '']
        self.status['rx']['inlvl'] = line[0]
        self.status['rx']['C/N'] = line[6]

        # packets, bytes, errors
        self.status['rx']['packets'] = sum([int(x[9:26]) for x in temp[11:19]])
        self.status['rx']['bytes'] = sum([int(x[33:45]) for x in temp[11:19]])
        self.status['rx']['errors'] = sum([int(x[57:]) for x in temp[11:19]])


def main():
    import sys
    puhp = PollUHP(sys.argv[1])
    puhp.poll()
    print(puhp.status)


if __name__ == '__main__':
	main()