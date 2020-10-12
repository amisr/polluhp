#!/usr/bin/env python
################################################################################
#
#    Title: test.py
#
#    Author: asreimer
#
#    Description: This tests the PollUHP class
#
################################################################################

import time
import requests
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from PollUHP import PollUHP


# we need to mock the requests.get call in PollUHP
def mocked_requests_get(*args,**kwargs):
    HEADER_URL = 'http://192.168.222.222/h'
    STATUS_URL = 'http://192.168.222.222/ss40.htm'
    TXMOD_URL = 'http://192.168.222.222/ss32.htm'
    RXMOD_URL = 'http://192.168.222.222/ss33.htm'

    MOCK_HEADER_RESPONSE = """<!DOCTYPE html><html><head><meta http-equiv=X-UA-Compatible content="IE=edge" /><meta charset='utf-8' /><link rel=stylesheet type=text/css href=ly.css ><title>UHP-GBEU0121</title></head><body><DIV class=st0 style='width:900px'><DIV class=st2><H3 class=yellow><A href=ss33 target=mn>DEM1</A></H3><H3><A href=ss27 target=mn>DEM2</A></H3><BR><H3 class=green><A href=ss32 target=mn>MOD</A></H3><H3 class=green><A href=ss37 target=mn>NET</A></H3></DIV><DIV class=st2></DIV><DIV class=st1><P>Name</P><H3>GBEU0121</H3><P>Uptime</P><H3>+8   d 04:24:11</H3><P>Profile</P><H3><A href=cb3?da=3 target=mn>3-Star station (FWD-Pro2)</A> <P>&nbsp;&nbsp;<A href=hy1>&#8634</A></P></H3><P>State</P><H3>Operation</H3></DIV><DIV class=st3><P style=background-color:#fcb940;>&nbsp;&nbsp;<A href=hx1>Save config</A></P><H3 class=yellow>REBT</H3><H3 class=yellow><A href=ss35 target=mn>SYST</A></H3><H3>                                                            <A href=ss34 target=mn>LAN</A></H3><H3 class=yellow>CRC</H3><H3>OFFS</H3><H3>TLC</H3><H3>NWRN</H3><H3>LWRN</H3><H3>NFLT</H3><H3>LFLT</H3><P><A href=hz1>Clear</A></P></DIV></DIV></BODY></HTML>"""
    MOCK_STATUS_RESPONSE = """<!DOCTYPE html><html><head><meta http-equiv=X-UA-Compatible content="IE=edge" /><meta charset='utf-8' /><link rel=stylesheet type=text/css href=ls.css ><title>UHP-GBEU0121</title><script type="text/javascript">pg_refresh=setTimeout( function () {window.location.replace('/ss40?dJ=1')},10000)</script></head><body><table width=750><tr><td><a href=ss40>Refresh</a><td>SN: <B>40075545<td><A href=cc41>SW:</A> <B>UHP-105 Software<TD>Ver: <B>3.5.2 (27.04.2020)</TABLE><TABLE width=750><TR><TD>CPU load: <B>12 %<TD>Buffers: <B>2 %<TD>Temp: <B>53 C<TD>Profile: <B>UP during +15:02:58       (7 runs)</TABLE><TABLE width=750><tr><tr><th>Interface<th>State<th>Info<th>TX rate (bps)<th>RX rate (bps)<th>RX errors<tr><td><a href=ss34.htm>Ethernet</a><td class=green>Up<TD>Link: <B>Eth1:100/FD Eth2:No link<td><B>4283<td><B>14759<td><B>0<tr><td><a href=ss33.htm>Demodulator-1</a><td class=green>Up<TD>C/N: <B>10.7 dB<td><B>-<td><B>377963<td><B>14807<tr><td><a href=ss27.htm>Demodulator-2</a><td class=gray>Disabled<TD>Lvl: <B>- 8.0 dBm<td><B>-<td><B>0<td><B>0<tr><td><a href=ss32.htm>Modulator</a><td class=green>Up<TD><A href=cm3?da=3>Tx Lvl:</A> <B>- 24.0 dBm<td><B>14425<td><B>-<td><B>-</TABLE><BR><TABLE width=750><TR><TH colspan=10>Station<TR><TD>Number<TD><B>100<TD>FP lost<TD><B>42<TD>DTTS cor<TD><B>7764 us<TD>Frq cor<TD><B>50196 Hz<TD>Lvl cor<TD><B>0.0 dBm<TR><TD>Cur BW<TD><B>6 (101 k)<TD>Sum Rq<TD><B>1 (16 k)<TD>RT rq<TD><B>0 (0 k)<TD><A href=cc16>Codecs</A><TD><B>0<TD>Timeout<TD><B>0</TABLE><BR><TABLE width=750><TR><TH><A href=cc8 target=mn>DHCP</A><TD colspan="2">IP&nbsp;start: <B>173.244.85.198<TD colspan="2">IP&nbsp;end: <B>173.244.85.198<TD colspan="2">Issued&nbsp;addresses:&nbsp;<B>1</TABLE></BODY></HTML>"""
    MOCK_TXMOD_RESPONSE = """<!DOCTYPE html><html><head><meta http-equiv=X-UA-Compatible content="IE=edge" /><meta charset='utf-8' /><link rel=stylesheet type=text/css href=ls.css ><title>UHP-GBEU0121</title><script type="text/javascript">pg_refresh=setTimeout( function () {window.location.replace('/ss32?dJ=1')},10000)</script></head><body><PRE>Modulator interface is UP
Last U->D: 09.Oct.20 19:45:11   U->D transitions: 9
Last D->U: 09.Oct.20 19:45:14   Counters cleared: never          
----------------------------- Modulator settings -----------------------------
Freq: 1569263 FreqAdj: 0     SR: 1500   SetLvl: -24.0 Max: -30.0      10M: ON 
LO: 12800000  FixCorr: 0     BR: 2500   OutLvl: -24.0 TX: ON          24V: ON 
------------------------------------------------------------------------------
Mode: TDMA  MOD: QPSK FEC: 5/6  Rolloff: 5%  Pilots: OFF
------------------------------------------------------------------------------
Rate/bps: 15652           Shaper_drops: 71638
P1   Packets: 0           Bytes: 0           Q_len/400  : 0        Drops: 0
P2   Packets: 0           Bytes: 0           Q_len/100  : 0        Drops: 0
P3   Packets: 0           Bytes: 0           Q_len/100  : 0        Drops: 0
P4   Packets: 4083767     Bytes: 1076825504  Q_len/400  : 2        Drops: 0
P5   Packets: 0           Bytes: 0           Q_len/100  : 0        Drops: 0
P6   Packets: 0           Bytes: 0           Q_len/50   : 0        Drops: 0
P7   Packets: 112744      Bytes: 34853112    Q_len/50   : 0        Drops: 0
CTRL Packets: 15          Bytes: 963         Q_len/20   : 0        Drops: 0

</BODY></HTML>"""
    MOCK_RXMOD_RESPONSE = """<!DOCTYPE html><html><head><meta http-equiv=X-UA-Compatible content="IE=edge" /><meta charset='utf-8' /><link rel=stylesheet type=text/css href=ls.css ><title>UHP-GBEU0121</title><script type="text/javascript">pg_refresh=setTimeout( function () {window.location.replace('/ss33?dJ=1')},10000)</script></head><body><PRE>Demodulator-1 interface is UP
Last U->D: 09.Oct.20 19:44:06   U->D transitions: 8
Last D->U: 09.Oct.20 19:44:07   Counters cleared: never          
-------------------------------- Outdoor Unit --------------------------------
| LNB-pwr: 18V    T10M: OFF      Offset: 0    KHz      SearchBW: 300  KHz    |
| LO: 10750000    Frq: 1279085   SR: 14500      Input:  RX-1      SpI:  OFF  |
----------------------------- Demodulator state ------------------------------
| InLvl | SpI |      MODCOD      | SRoff  | C/N  | RX-offset |   FixOffset   |
| -15.7 | OFF | SF QPSK 2/3      | 0      | 10.5 | -2    KHz |   0     KHz   |
------------------------------- Data received --------------------------------
Rate/bps: 2084448        
Packets: 22942803         Bytes: 4291027684  CRC_errors: 11530
Packets: 17290570         Bytes: 4193664768  CRC_errors: 41
Packets: 10172320         Bytes: 3350737334  CRC_errors: 88
Packets: 80544850         Bytes: 335984958   CRC_errors: 713
Packets: 85547723         Bytes: 3061244383  CRC_errors: 2336
Packets: 9738779          Bytes: 2718740489  CRC_errors: 279
Packets: 0                Bytes: 0           CRC_errors: 0
Packets: 0                Bytes: 0           CRC_errors: 0
</BODY></HTML>"""

    class MockResponse():
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    if args[0] == HEADER_URL:
        return MockResponse(MOCK_HEADER_RESPONSE, 200)
    if args[0] == STATUS_URL:
        return MockResponse(MOCK_STATUS_RESPONSE, 200)
    if args[0] == TXMOD_URL:
        return MockResponse(MOCK_TXMOD_RESPONSE, 200)
    if args[0] == RXMOD_URL:
        return MockResponse(MOCK_RXMOD_RESPONSE, 200)

    return MockResponse(None, 404)


# run the PollUHP unit test
class TestPollUHP(unittest.TestCase):

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_modem_status(self, mock_get):
        expected = {'modem': {'poll_results': 'Success', 'name': 'GBEU0121', 'uptime': '+8   d 04:24:11', 'profile': '3-Star station (FWD-Pro2)', 'hwserial': '40075545', 'swversion': 'UHP-105 Software 3.5.2 (27.04.2020)', 'cpuload': '12 %', 'buffers': '2 %', 'temp': '53 C', 'ethstatus': 'Up', 'ethlinkstate': 'Eth1:100/FD Eth2:No link', 'demod1status': 'Up', 'demod2status': 'Disabled', 'modstatus': 'Up'}, 'tx': {'poll_results': 'Success', 'u2d': '09.Oct.20 19:45:11', 'd2u': '09.Oct.20 19:45:14', 'setlvl': '-24.0', '10M': 'ON', 'outlvl': '-24.0', '24V': 'ON', 'packets': 226237045, 'bytes': 17951399616, 'drops': 0, 'errors': 14987}, 'rx': {'poll_results': 'Success', 'u2d': '09.Oct.20 19:44:06', 'd2u': '09.Oct.20 19:44:07', 'inlvl': '-15.7', 'C/N': '10.5', 'packets': 226237045, 'bytes': 17951399616, 'errors': 14987}}

        puhp = PollUHP('192.168.222.222')
        puhp.poll()
        print(puhp.status)
        # self.assertEqual(puhp.status,expected)


if __name__ == '__main__':
    unittest.main()