# uhp200 #
A package for polling and parsing the status of a UHP Networks Ku Satellite Modem.

### Installation ###

Clone this repo and install using:

    pip install .

from the root directory of the repository.

### Usage ###

There are 2 ways to use this package,
1) from a python shell, or
2) from the command line (2 commands).

#### Python Shell ####

    from polluhp import PollUHP
    address = '192.168.222.222'
    timeout = 5
    retrytime = 1
    psb = PollUHP(address,timeout=timeout,retrytime=retrytime)
    psb.poll()
    print(psb.status)

#### Command Line ####
Installation results in a `polluhp` command line tool. Example usage:

    $ polluhp 192.168.222.222

which will poll the modem with IP address `192.168.222.222`. By default, the
program will try to poll the modem 3 times waiting with a timeout of 5
seconds and a retry time of 1 second. Check out the help to see how to
modify the `timeout` and `retrytime`:

    $ polluhp -h
    usage: polluhp [-h] [-t TIMEOUT] [-r RETRYTIME] address
    
    Poll a UHP Networks Ku Satellite Modem for status.
    
    positional arguments:
      address               The IP address of the modem.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TIMEOUT, --timeout TIMEOUT
                            Poll timeout. Time to wait for response to request.
      -r RETRYTIME, --retrytime RETRYTIME
                            Retry timeout. Time to wait between retries.


There is another tool, `modemview` that is also available. Usage is the same
as for `polluhp`, however the results are displayed in a curses display
and updated every ~5 seconds.