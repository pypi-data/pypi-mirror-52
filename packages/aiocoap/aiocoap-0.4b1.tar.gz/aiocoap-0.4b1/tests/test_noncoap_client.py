# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""Confront an aiocoap server with a client that speaks so bad protocol it is
easier to mock with sending byte sequences than with aiocoap"""

import socket
import asyncio
import signal
import contextlib

import aiocoap

from .test_server import WithTestServer, precise_warnings, no_warnings, asynctest

class TimeoutError(RuntimeError):
    """Raised when a non-async operation times out"""

    @classmethod
    def _signalhandler(cls, *args):
        raise cls()

    @classmethod
    @contextlib.contextmanager
    def after(cls, time):
        old = signal.signal(signal.SIGALRM, cls._signalhandler)
        signal.alarm(time)
        yield
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)

class TestNoncoapClient(WithTestServer):
    def setUp(self):
        super(TestNoncoapClient, self).setUp()

        self.mocksock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.mocksock.connect((self.serveraddress, aiocoap.COAP_PORT))

    def tearDown(self):
        self.mocksock.close()

        super(TestNoncoapClient, self).tearDown()

    @precise_warnings(["Ignoring unparsable message from ..."])
    @asynctest
    async def test_veryshort(self):
        self.mocksock.send(b'\x40')
        await asyncio.sleep(0.1)

    @precise_warnings(["Ignoring unparsable message from ..."])
    @asynctest
    async def test_short_mid(self):
        self.mocksock.send(b'\x40\x01\x97')
        await asyncio.sleep(0.1)

    @precise_warnings(["Ignoring unparsable message from ..."])
    @asynctest
    async def test_version2(self):
        self.mocksock.send(b'\x80\x01\x99\x98')
        await asyncio.sleep(0.1)

    @no_warnings
    @asynctest
    async def test_duplicate(self):
        self.mocksock.send(b'\x40\x01\x99\x99') # that's a GET /
        await asyncio.sleep(0.1)
        self.mocksock.send(b'\x40\x01\x99\x99') # that's a GET /
        await asyncio.sleep(0.1)
        r1 = r2 = None
        try:
            with TimeoutError.after(1):
                r1 = self.mocksock.recv(1024)
                r2 = self.mocksock.recv(1024)
        except TimeoutError:
            pass
        self.assertEqual(r1, r2, "Duplicate GETs gave different responses")
        self.assertTrue(r1 is not None, "No responses received to duplicate GET")

    @no_warnings
    @asynctest
    async def test_ping(self):
        self.mocksock.send(b'\x40\x00\x99\x9a') # CoAP ping -- should this test be doable in aiocoap?
        await asyncio.sleep(0.1)
        with TimeoutError.after(1):
            response = self.mocksock.recv(1024)
        assert response == b'\x70\x00\x99\x9a'

    @no_warnings
    @asynctest
    async def test_noresponse(self):
        self.mocksock.send(b'\x50\x01\x99\x9b\xd1\xf5\x02') # CoAP NON GET / with no-response on 2.xx
        await asyncio.sleep(0.1)
        try:
            with TimeoutError.after(1):
                response = self.mocksock.recv(1024)
            self.assertTrue(False, "Response was sent when No-Response should have suppressed it")
        except TimeoutError:
            pass
