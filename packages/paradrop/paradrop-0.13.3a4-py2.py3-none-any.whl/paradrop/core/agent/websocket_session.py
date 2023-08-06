"""
WebSocket session for communication with cloud controller.
"""
from __future__ import print_function
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtol

from paradrop.base.output import out
from paradrop.base import nexus


class HostWebSocketProtocol(WebSocketClientProtol):
    # Make this a class variable because a new WampSession object is created
    # whenever the WAMP connection resets, but we only call set_update_fetcher
    # on program initialization.
    update_fetcher = None

    def onConnect(self, response):
        out.info("WebSocket connected to {}".format(response.peer))

    def onOpen(self):
        out.info("WebSocket connection open.")
        self.sendMessage("subscribe:update:" + nexus.core.info.pdid)

    def onMessage(self, payload, isBinary):
        out.info("WebSocket message: {}".format(payload))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class HostWebSocketFactory(WebSocketClientFactory):
    pass


# class WampSession(BaseSession):
#
#    def __init__(self, *args, **kwargs):
#        self.uriPrefix = 'org.paradrop.'
#        super(WampSession, self).__init__(*args, **kwargs)
#
#    def onConnect(self):
#        out.info('Router session connected.')
#        if (nexus.core.info.pdid and nexus.core.getKey('apitoken')):
#            out.info('Starting WAMP-CRA authentication on realm "{}" as user "{}"...'\
#                     .format(self.config.realm, nexus.core.info.pdid))
#            self.join(self.config.realm, [u'wampcra'],
#                    six.u(nexus.core.info.pdid))
#
#    def onChallenge(self, challenge):
#        if challenge.method == u"wampcra":
#            out.verbose("WAMP-CRA challenge received: {}".format(challenge))
#
#            wampPassword = nexus.core.getKey('apitoken')
#            if u'salt' in challenge.extra:
#                # salted secret
#                key = auth.derive_key(wampPassword,
#                                      challenge.extra['salt'],
#                                      challenge.extra['iterations'],
#                                      challenge.extra['keylen'])
#            else:
#                # plain, unsalted secret
#                key = wampPassword
#
#            # compute signature for challenge, using the key
#            signature = auth.compute_wcs(key, challenge.extra['challenge'])
#
#            # return the signature to the router for verification
#            return signature
#
#        else:
#            raise Exception("Invalid authmethod {}".format(challenge.method))
#
#
#    @inlineCallbacks
#    def onJoin(self, details):
#        out.info('Router session joined')
#
#        yield self.subscribe(self.updatesPending, self.uriPrefix + 'updatesPending')
#        yield self.register(self.update, self.uriPrefix + 'update')
#        yield BaseSession.onJoin(self, details)
#
#
#    def onLeave(self, details):
#        out.info("Router session left: {}".format(details))
#        nexus.core.wamp_connected = False
#        self.disconnect()
#
#
#    def onDisconnect(self):
#        out.info("Router session disconnected.")
#
#    def update(self, pdid, data):
#        print("Sending command {} to pdinstall".format(data['command']))
#        success = pdinstall.sendCommand(data['command'], data)
#
#        # NOTE: If successful, this process will probably be going down soon.
#        if success:
#            return "Sent command to pdinstall"
#        else:
#            return "Sending command to pdinstall failed"
#
#
#    @classmethod
#    def set_update_fetcher(cls, update_fetcher):
#        WampSession.update_fetcher = update_fetcher
#
#
#    @inlineCallbacks
#    def updatesPending(self, pdid):
#        out.info('Notified of updates...')
#        if WampSession.update_fetcher is not None:
#            out.info('Pulling updates from the server...')
#            yield WampSession.update_fetcher.pull_update()
