#!/usr/bin/env python
################################################################################
#
#    Title: modemview.py
#
#    Author: asreimer
#
#    Description: This script displays the results of a PollUHP class poll
#                 in a curses display.
#
################################################################################


import re
import os
import sys
import curses
import curses.ascii
from argparse import ArgumentParser

from polluhp import PollUHP


# helper function to remove html tags from some of the poll results
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


# class for curses display
class modemview():
    def __init__(self,stdscr,address,timeout,retrytime):
        psb = PollUHP(address, timeout=timeout, retrytime=retrytime)

        self.psb = psb
        self.stdscr = stdscr


    def run(self):
        self.stdscr.timeout(2000)
        self.update()

        while True:
            c = self.stdscr.getch()
            if c==-1:
                self.update()
            elif c==curses.ascii.ESC:
                break

        self.stdscr.erase()


    def update(self):
        self.stdscr.addstr(1,1,'*')
        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        try:
            self.psb.poll()
            status = self.psb.status
        except: 
            status = None 
        
        self.stdscr.addstr(1,1,' ')
        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        self.stdscr.erase()
        self.stdscr.border()


        self.stdscr.addstr(1,2,'UHP Networks Ku Modem Status: %s' % (self.psb.address))
        # modem status
        if status['modem']['poll_results'] == 'Success':
            modem = status['modem']
        else:
            modem = {'name':'err', 'uptime':'err', 'profile':'err',
                     'hwserial':'err', 'swversion':'err', 'cpuload':'err',
                     'buffers':'err', 'temp':'err', 'ethstatus':'err',
                     'ethlinkstate':'err', 'demod1status':'err',
                     'demod2status':'err', 'modstatus':'err'}

        # tx and rx statuses
        if status['tx']['poll_results'] == 'Success':
            tx = status['tx']
        else:
            tx = {'u2d':'err', 'd2u':'err', 'setlvl':'err','10M':'err',
                  'outlvl':'err', '24V':'ON', 'packets':'err','bytes':'err',
                  'drops':'err'}

        if status['rx']['poll_results'] == 'Success':
            rx = status['rx']
        else:
            rx = {'u2d':'err', 'd2u':'err', 'inlvl':'err', 'C/N':'err',
                  'packets':'err', 'bytes':'err', 'errors':'err'}


        col1 = 4
        col2 = 30
        col3 = 56
        self.stdscr.addstr( 3, col1-2,'MODEM')

        self.stdscr.addstr( 4, col1-1,'Uptime: %s' % (modem['uptime']))
        self.stdscr.addstr( 4, col2,'Profile: %s' % (modem['profile']))

        self.stdscr.addstr( 6, col1-1,'GENERAL')
        self.stdscr.addstr( 7, col1,'CPU Load: %s' % (modem['cpuload']))
        self.stdscr.addstr( 8, col1,'Demod-1:  %s' % (modem['demod1status']))
        self.stdscr.addstr( 9, col1,'Tx Lvl:   %s dBm' % (tx['outlvl']))
        self.stdscr.addstr( 7, col2,'CPU Buffers:  %s' % (modem['buffers']))
        self.stdscr.addstr( 8, col2,'Demod-2:      %s' % (modem['demod2status']))
        self.stdscr.addstr( 9, col2,'Rx Lvl:       %s dBm' % (rx['inlvl']))
        self.stdscr.addstr( 7, col3,'CPU Temp: %s' % (modem['temp']))
        self.stdscr.addstr( 8, col3,'Mod:      %s' % (modem['modstatus']))
        self.stdscr.addstr( 9, col3,'C/N:      %s' % (rx['C/N']))

        col1 = 4
        col2 = 40
        self.stdscr.addstr(12, col1-1,'IDENTIFICATION')
        self.stdscr.addstr(13, col1,'Name:             %s' % (modem['name']))
        self.stdscr.addstr(14, col1,'Software Version: %s' % (modem['swversion']))
        self.stdscr.addstr(15, col1,'Serial Number:    %s' % (modem['hwserial']))

        self.stdscr.addstr(18, col1-1,'NETWORK STATISTICS')
        self.stdscr.addstr(19, col1,'Eth. Status:         %s' % (modem['ethstatus']))
        self.stdscr.addstr(19, col2,'Eth. Link:         %s' % (modem['ethlinkstate']))
        self.stdscr.addstr(20, col1,'Transmitted Packets: %s' % (tx['packets']))
        self.stdscr.addstr(21, col1,'Transmitted Bytes:   %s' % (tx['bytes']))
        self.stdscr.addstr(22, col1,'Transmit Drops:      %s' % (tx['drops']))
        self.stdscr.addstr(20, col2,'Received Packets:  %s' % (rx['packets']))
        self.stdscr.addstr(21, col2,'Received Bytes:    %s' % (rx['bytes']))
        self.stdscr.addstr(22, col2,'Receive Errors:    %s' % (rx['errors']))


        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        return


# provides command line interface
def main():
    # Set up some argparse stuff
    parser = ArgumentParser(description='Poll a UHP Networks Ku Satellite Modem for status.')
    parser.add_argument("address", help="The IP address of the modem.", default='192.168.222.222')
    parser.add_argument("-t", "--timeout", help="Poll timeout. Time to wait for response to request.", type=float, default=1.,required=False)
    parser.add_argument("-r", "--retrytime", help="Retry timeout. Time to wait between retries.", type=float, default=1.,required=False)
    # Get arguments. Convert argparser Namespace class to dictionary
    args = vars(parser.parse_args())
    
    address = args['address']
    timeout = args['timeout']
    retrytime = args['retrytime']

    curses.wrapper(start_curses,address,timeout,retrytime)


# helper function for starting curses
def start_curses(stdscr,address,timeout,retrytime):
    modemview(stdscr,address,timeout,retrytime).run()


if __name__ == '__main__':
    main()
