#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""the actual control peer"""

import asyncio

from titanfe import log as logging
from titanfe.connection import Connection

from .webapi import WebApi
from .flow import parse_flows

log = logging.getLogger(__name__)


class ControlPeer:
    """The control peer application will start runners as required for the flows/bricks
       as described in the given config file. Once the runners have registered themselves,
       they will get according assignments.

    Arguments:
        config_file (Path): path to the flow config yaml
        kafka_bootstrap_servers (str):
            'host[:port]' string (or list of 'host[:port]' strings)
            to contact the Kafka bootstrap servers on
    """

    def __init__(self, config_file, kafka_bootstrap_servers):
        self.loop = asyncio.get_event_loop()
        self.kafka_bootstrap_servers = kafka_bootstrap_servers

        self.flows = parse_flows(self, config_file)
        self.flows_by_uid = {flow.uid: flow for flow in self.flows}
        self.runners = {}

        self.server = None
        self.server_address = None
        self.webapi = None

    async def run(self):
        """run the application"""
        log.debug("running control peer")
        await self.setup_runner_communication()
        self.setup_webapi()
        self.start_flows()

        try:
            await self.server.serve_forever()
        except asyncio.CancelledError:
            pass

    async def shutdown(self):
        """shut down the controlpeer"""
        log.info('Initiating shutdown')
        await self.stop_flows()
        await self.webapi.stop()
        self.server.close()
        await self.server.wait_closed()
        log.info('Shutdown sequence complete - should exit soon')

    async def setup_runner_communication(self):
        """create a server to communicate with brick runners"""
        log.debug("create server")
        self.server = await asyncio.start_server(self.establish_communication, "127.0.0.1", 8888)
        self.server_address = self.server.sockets[0].getsockname()

    def setup_webapi(self):
        self.webapi = WebApi(self)
        self.webapi.run()

    def start_flow(self, uid):
        flow = self.flows_by_uid[uid]
        flow.start()
        return flow

    def start_flows(self):
        for flow in self.flows:
            flow.start()

    async def stop_flows(self):
        for flow in self.flows:
            await flow.stop()

    async def stop_flow(self, uid):
        flow = self.flows_by_uid[uid]
        await flow.stop()
        return flow

    async def establish_communication(self, reader, writer):
        """establish communication with brick runners: handle registration"""
        runner_connection = Connection(reader, writer, log)

        runner_registration = await runner_connection.receive()
        _, runner_uid = runner_registration
        runner = self.runners.get(runner_uid)
        if not runner:
            log.error("No runner found for id: %s", runner_uid)
            log.debug("Available brick runner: %r", self.runners)
            return

        # move communication to the runner
        asyncio.create_task(runner.process_messages(runner_connection))
