package com.moparisthebest.echoself;

import org.dom4j.Element;
import org.jivesoftware.whack.ExternalComponentManager;
import org.xmpp.component.Component;
import org.xmpp.component.ComponentManager;
import org.xmpp.component.ComponentManagerFactory;
import org.xmpp.component.ComponentException;
import org.xmpp.packet.Packet;
import org.xmpp.packet.JID;
import org.xmpp.packet.Message;

import java.util.Iterator;

/**
 * This component receives forwarded messages from a client, and sends the forwarded messages right back.
 *
 * This is to enable a concept someone once called 'client-side components'
 *
 * Currently you have to send a <echo xmlns="https://code.moparisthebest.com/moparisthebest/xmpp-echo-self"/> element inside
 * <message> or this will ignore you, that's still up for debate as to whether it'll end up being required.
 *
 * @author Travis Burtrum
 */
public class EchoSelf implements Component {

    public String getName() {
        return "Echo Self";
    }

    public String getDescription() {
        return "Echo Self implementation";
    }

    public void processPacket(final Packet packet) {
        //System.out.println("Received package:"+packet.toXML());
        // Only process Message packets
        if (packet instanceof Message) {
            final Message message = (Message) packet;

            // we technically don't *need* this, we could just echo-self any forwarded message we receive...
            if(message.getChildElement("echo", "https://code.moparisthebest.com/moparisthebest/xmpp-echo-self") == null)
                return;

            final Element forwarded = message.getChildElement("forwarded", "urn:xmpp:forward:0");
            if(forwarded == null)
                return;

            Element forwardedMessage = getChildElement(forwarded,"message", "jabber:client");
            if(forwardedMessage == null)
                forwardedMessage = getChildElement(forwarded,"message", null);
            if(forwardedMessage == null)
                return;

            // move delay down into new message if we have it
            final Element delay = getChildElement(forwarded, "delay", "urn:xmpp:delay");
            if(delay != null)
                forwardedMessage.add(delay.createCopy());

            // Build the answer
            final Packet reply = new Message(forwardedMessage);
            reply.setTo(message.getFrom());
            reply.setFrom(message.getTo());

            //System.out.println("Sending package:"+reply.toXML());

            // Send the response to the sender of the request
            try {
                ComponentManagerFactory.getComponentManager().sendPacket(this, reply);
            } catch (ComponentException e) {
                e.printStackTrace();
            }
        }
    }

    @SuppressWarnings("unchecked")
    public Element getChildElement(final Element el, final String name, final String namespace) {
        for (final Iterator<Element> i = el.elementIterator(name); i.hasNext(); ) {
            final Element element = i.next();
            if (namespace == null || element.getNamespaceURI().equals(namespace)) {
                return element;
            }
        }
        return null;
    }

    public void initialize(JID jid, ComponentManager componentManager) {
    }

    public void start() {
    }

    public void shutdown() {
    }

    public static void main(final String[] args) {
        if(args == null || args.length < 4){
            System.err.println("Usage: java -jar echo-self.jar echo.example.org componentPassword 127.0.0.1 5347");
            return;
        }
        final String subdomain = args[0];
        final String password = args[1];
        final String host = args[2];
        final int port = Integer.parseInt(args[3]);

        // Create a manager for the external components that will connect to the server "localhost"
        // at the port 5225
        final ExternalComponentManager manager = new ExternalComponentManager(host, port, false);
        // Set the secret key for this component. The server must be using the same secret key
        // otherwise the component won't be able to authenticate with the server. Check that the
        // server has the property "component.external.secretKey" defined and that it is using the
        // same value that we are setting here.
        manager.setSecretKey(subdomain, password);
        // Set the manager to tag components as being allowed to connect multiple times to the same
        // JID.
        manager.setMultipleAllowed(subdomain, true);
        try {
            // Register that this component will be serving the given subdomain of the server
            manager.addComponent(subdomain, new EchoSelf());
            // Quick trick to ensure that this application will be running for ever. To stop the
            // application you will need to kill the process
            while (true) {
                try {
                    Thread.sleep(Long.MAX_VALUE);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } catch (ComponentException e) {
            e.printStackTrace();
        }
    }
}
