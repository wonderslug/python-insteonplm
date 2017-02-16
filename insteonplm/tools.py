"""Provides a raw console to test module and demonstrate usage."""
import argparse
import asyncio
import logging
import binascii

import insteonplm

__all__ = ('console', 'monitor')


from .plm import Address, PLMProtocol, Message

@asyncio.coroutine
def console(loop, log):
    """Connect to receiver and show events as they occur.

    Pulls the following arguments from the command line (not method arguments):

    :param device:
        Unix device where the PLM is attached
    :param verbose:
        Show debug logging.
    """
    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument('--device', default='/dev/ttyUSB0', help='Device')
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level)

    def log_callback(message):
        """Receives event callback from PLM Protocol class."""
        log.info('Callback invoked: %s', message)

    device = args.device

    log.info('Connecting to Insteon PLM at %s', device)

    conn = yield from insteonplm.Connection.create(
        device=device, loop=loop)

    def async_insteonplm_light_callback(device):
        log.warn('New Device: %s', device)

    criteria = dict()
    conn.protocol.add_device_callback(async_insteonplm_light_callback, criteria)

    #yield from asyncio.sleep(5, loop=loop)
    # Successfully turns off the light in my computer room (yay)
    # conn.protocol._send_raw(binascii.unhexlify('02624095e6001300'))
    #
    #conn.protocol._send_raw(binascii.unhexlify('02624095e6000300'))
    #conn.protocol.product_data_request('15c3ab')
    #yield from asyncio.sleep(10, loop=loop)

    yield from asyncio.sleep(10, loop=loop)

    if 1==0:
        #conn.protocol.send_insteon_extended('4095e6', '2e', '00', '0000000000000000000000000000')
        # INFO:insteonplm.protocol:INSTEON extended 40.95.E6->39.55.37: cmd1:2e
        # cmd2:00 flags:15 data:b'0101000020201cff1f0001000000'
        # d2: 01
        #
        conn.protocol.extended_status_request('4095e6')
        yield from asyncio.sleep(5, loop=loop)

        conn.protocol.update_setlevel('4095e6',127)
        conn.protocol.update_ramprate('4095e6',27)
        yield from asyncio.sleep(5, loop=loop)

        conn.protocol.extended_status_request('4095e6')
        yield from asyncio.sleep(5, loop=loop)


    if 1==0:
        conn.protocol.turn_on('4095e6', ramprate=2)
        yield from asyncio.sleep(5, loop=loop)

    if 1==0:
        conn.protocol.text_string_request('4095e6')

    if 1==0:
        conn.protocol.product_data_request('395fa4')

    if 1==0:
        conn.protocol.product_data_request('4095e6')
        conn.protocol.product_data_request('395fa4')
        conn.protocol.text_string_request('4095e6')
        yield from asyncio.sleep(5, loop=loop)

    #conn.protocol._send_raw(binascii.unhexlify('02624095e6150300000000000000ffff000000000000'))
    #yield from asyncio.sleep(5, loop=loop)

    if 1==1:
        print('-- ')
        conn.protocol.relay_request('395fa4')
        conn.protocol.relay_request('395ecb')
        print('-- ')
        conn.protocol.turn_off('395fa4')
        conn.protocol.turn_off('395ecb')
        print('-- ')
        conn.protocol.turn_on('395fa4', 1)
        yield from asyncio.sleep(5, loop=loop)
        print('-- ')
        conn.protocol.turn_on('395ecb', 1)
        yield from asyncio.sleep(5, loop=loop)

    if 1==0:
        yield from asyncio.sleep(5, loop=loop)
        conn.protocol.dump_all_link_database()
        yield from asyncio.sleep(5, loop=loop)


def monitor():

    """Wrapper to call console with a loop."""
    log = logging.getLogger(__name__)
    loop = asyncio.get_event_loop()
    asyncio.async(console(loop, log))
    loop.run_forever()
