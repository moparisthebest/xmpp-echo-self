xmpp-echo-self
----------

This component receives forwarded messages from a client, and sends the forwarded messages right back.

This is to enable a concept someone once called 'client-side components'

Currently you have to send a `<echo xmlns="https://code.moparisthebest.com/moparisthebest/xmpp-echo-self"/>` element inside
`<message/>` or this will ignore you, that's still up for debate as to whether it'll end up being required.

It ignores all other messages, this means to be super useful across multiple clients, your server must do carbons/mam, but
this makes the component stateless and dead-simple.  I think the trade-off is worth it.

Here are some messages with and without delay you can paste into an XML console to try:

    <message xmlns="jabber:client" to="+15555555555@echo.example.org" type="normal" id="9316996e-88da-4d6b-9bb6-6ff19c096a2c" from="you@you.org/you">
      <echo xmlns="https://code.moparisthebest.com/moparisthebest/xmpp-echo-self"/>
        <forwarded xmlns="urn:xmpp:forward:0">
            <message xmlns="jabber:client" from="+15555555555@echo.example.org" type="chat" id="9316996e-88da-4d6b-9bb6-6ff19c096a2b" to="you@you.org/you">
                <body>aoeu</body>
            </message>
        </forwarded>
    </message>

    <message xmlns="jabber:client" to="+15555555555@echo.example.org" type="normal" id="9316996e-88da-4d6b-9bb6-6ff19c096a2c" from="you@you.org/you">
      <echo xmlns="https://code.moparisthebest.com/moparisthebest/xmpp-echo-self"/>
        <forwarded xmlns="urn:xmpp:forward:0">
            <delay xmlns="urn:xmpp:delay" stamp="2017-10-31T23:08:25Z"/>
            <message xmlns="jabber:client" from="+15555555555@echo.example.org" type="chat" id="9316996e-88da-4d6b-9bb6-6ff19c096a2b" to="you@you.org/you">
                <body>aoeu</body>
            </message>
        </forwarded>
    </message>

Usage
-----
Compile it:

    mvn package

Run it:

    java -jar target/echo-self.jar echo.example.org componentPassword 127.0.0.1 5347
