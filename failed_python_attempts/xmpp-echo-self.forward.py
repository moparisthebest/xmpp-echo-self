#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

import logging
from argparse import ArgumentParser

from xml.parsers.expat import ExpatError

from slixmpp.stanza import Message
from slixmpp.componentxmpp import ComponentXMPP
from slixmpp.xmlstream import ET


class EchoComponent(ComponentXMPP):

    """
    A simple Slixmpp component that echoes messages.
    """

    def __init__(self, jid, secret, server, port):
        ComponentXMPP.__init__(self, jid, secret, server, port)

        # You don't need a session_start handler, but that is
        # where you would broadcast initial presence.

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler('forwarded_stanza', self.forward)

    def forward(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Since a component may send messages from any number of JIDs,
        it is best to always include a from JID.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        # The reply method will use the messages 'to' JID as the
        # outgoing reply's 'from' JID.
        if msg.xml.find('{https://code.moparisthebest.com/moparisthebest/echo-self}echo') is not None:
            #to = msg['to']
            #msg['to'] = msg['from']
            #msg['from'] = to

            print(msg)
            # this might be cleaner, except sleekxmpp isn't sending body-less messages here at all, just silently swallowing them...
            to = msg['to']
            ffrom = msg['from']
            msg = self._build_stanza(msg['forwarded'].get_stanza(), self.default_ns)
            #kwargs = {"stream": self.stream, "xml":msg}
            #msg.stream = self.stream
            #msg.stream['default_ns'] = 'cc'
            #msg = Message(msg)
            #nmsg = None
            #for stanza in self:
            #    if isinstance(stanza, (Message)):
            #        nmsg = stanza
            #        break
            #msg = nmsg
            #msg = msg.xml.find('{urn:xmpp:forward:0}forwarded').find('{jabber:client}message')
            #msg = ET.fromstring(msg)
            #msg.attrib['default_ns'] = 'jabber:client'
            #msg = Message(xml=msg)
            #msg = Message()
            #msg.xml = msg
            #msg.attrib['to'] = ffrom
            #msg.attrib['from'] = to
            msg['to'] = ffrom
            msg['from'] = to
            msg['xmlns'] = self.default_ns
            msg
            print(msg)
            #msg.send()
            #self.send_xml(msg)
            self.send_raw("%s" % msg)


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=EchoComponent.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid", required=True,
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-s", "--server", dest="server", required=True,
                        help="server to connect to")
    parser.add_argument("-P", "--port", dest="port", required=True,
                        help="port to connect to")

    args = parser.parse_args()

    if args.jid is None or args.server is None or args.port is None:
        parser.print_help()
        exit(1)
    if args.password is None:
        args.password = ''

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    # Setup the EchoComponent and register plugins. Note that while plugins
    # may have interdependencies, the order in which you register them does
    # not matter.
    xmpp = EchoComponent(args.jid, args.password, args.server, args.port)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0297') # Stanza Forwarding

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()
