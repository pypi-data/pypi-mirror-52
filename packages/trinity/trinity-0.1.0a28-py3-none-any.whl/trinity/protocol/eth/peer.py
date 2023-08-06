import asyncio
from typing import (
    Any,
    cast,
    Dict,
    Sequence,
    Tuple,
)

from lahja import EndpointAPI

from eth_typing import BlockNumber

from eth.constants import GENESIS_BLOCK_NUMBER
from eth.rlp.headers import BlockHeader
from lahja import (
    BroadcastConfig,
)

from p2p.abc import CommandAPI, ConnectionAPI, HandshakerAPI, HandshakeReceiptAPI, SessionAPI
from p2p.exceptions import PeerConnectionLost
from p2p.handshake import DevP2PReceipt
from p2p.protocol import (
    Payload,
)

from trinity._utils.decorators import (
    async_suppress_exceptions,
)
from trinity.protocol.common.peer import (
    BaseChainPeer,
    BaseChainPeerFactory,
    BaseChainPeerPool,
)
from trinity.protocol.common.peer_pool_event_bus import (
    BaseProxyPeer,
    BaseProxyPeerPool,
    PeerPoolEventServer,
)
from trinity.protocol.common.typing import (
    BlockBodyBundles,
    NodeDataBundles,
    ReceiptsBundles,
)

from .commands import (
    GetBlockHeaders,
    GetBlockBodies,
    GetReceipts,
    GetNodeData,
    NewBlock,
    NewBlockHashes,
    Transactions,
)
from .constants import MAX_HEADERS_FETCH
from .events import (
    GetBlockHeadersEvent,
    GetBlockHeadersRequest,
    GetBlockBodiesEvent,
    GetBlockBodiesRequest,
    GetReceiptsEvent,
    GetNodeDataEvent,
    GetNodeDataRequest,
    GetReceiptsRequest,
    NewBlockEvent,
    NewBlockHashesEvent,
    SendBlockBodiesEvent,
    SendBlockHeadersEvent,
    SendNodeDataEvent,
    SendReceiptsEvent,
    TransactionsEvent,
)
from .proto import ETHProtocol, ProxyETHProtocol, ETHHandshakeParams
from .handlers import ETHExchangeHandler, ProxyETHExchangeHandler
from .handshaker import ETHHandshaker, ETHHandshakeReceipt


class ETHPeer(BaseChainPeer):
    max_headers_fetch = MAX_HEADERS_FETCH

    supported_sub_protocols = (ETHProtocol,)
    sub_proto: ETHProtocol = None

    _requests: ETHExchangeHandler = None

    def process_handshake_receipts(self,
                                   devp2p_receipt: DevP2PReceipt,
                                   protocol_receipts: Sequence[HandshakeReceiptAPI]) -> None:
        super().process_handshake_receipts(devp2p_receipt, protocol_receipts)
        for receipt in protocol_receipts:
            if isinstance(receipt, ETHHandshakeReceipt):
                self.head_td = receipt.handshake_params.total_difficulty
                self.head_hash = receipt.handshake_params.head_hash
                self.genesis_hash = receipt.handshake_params.genesis_hash
                self.network_id = receipt.handshake_params.network_id
                break
        else:
            raise Exception(
                "Did not find an `ETHHandshakeReceipt` in {protocol_receipts}"
            )

    def get_extra_stats(self) -> Tuple[str, ...]:
        stats_pairs = self.requests.get_stats().items()
        return tuple(
            f"{cmd_name}: {stats}" for cmd_name, stats in stats_pairs
        )

    @property
    def requests(self) -> ETHExchangeHandler:
        if self._requests is None:
            self._requests = ETHExchangeHandler(self.connection)
        return self._requests

    def setup_protocol_handlers(self) -> None:
        self.connection.add_command_handler(NewBlock, self._handle_new_block)

    async def _handle_new_block(self, connection: ConnectionAPI, msg: Payload) -> None:
        msg = cast(Dict[str, Any], msg)
        header, _, _ = msg['block']
        actual_head = header.parent_hash
        actual_td = msg['total_difficulty'] - header.difficulty

        if actual_td > self.head_td:
            self.head_hash = actual_head
            self.head_td = actual_td


class ETHProxyPeer(BaseProxyPeer):
    """
    A ``ETHPeer`` that can be used from any process instead of the actual peer pool peer.
    Any action performed on the ``BCCProxyPeer`` is delegated to the actual peer in the pool.
    This does not yet mimic all APIs of the real peer.
    """

    def __init__(self,
                 session: SessionAPI,
                 event_bus: EndpointAPI,
                 sub_proto: ProxyETHProtocol,
                 requests: ProxyETHExchangeHandler):

        super().__init__(session, event_bus)

        self.sub_proto = sub_proto
        self.requests = requests

    @classmethod
    def from_session(cls,
                     session: SessionAPI,
                     event_bus: EndpointAPI,
                     broadcast_config: BroadcastConfig) -> 'ETHProxyPeer':
        return cls(
            session,
            event_bus,
            ProxyETHProtocol(session, event_bus, broadcast_config),
            ProxyETHExchangeHandler(session, event_bus, broadcast_config)
        )


class ETHPeerFactory(BaseChainPeerFactory):
    peer_class = ETHPeer

    async def get_handshakers(self) -> Tuple[HandshakerAPI, ...]:
        headerdb = self.context.headerdb
        wait = self.cancel_token.cancellable_wait

        head = await wait(headerdb.coro_get_canonical_head())
        total_difficulty = await wait(headerdb.coro_get_score(head.hash))
        genesis_hash = await wait(
            headerdb.coro_get_canonical_block_hash(BlockNumber(GENESIS_BLOCK_NUMBER))
        )

        handshake_params = ETHHandshakeParams(
            head_hash=head.hash,
            total_difficulty=total_difficulty,
            genesis_hash=genesis_hash,
            network_id=self.context.network_id,
            version=ETHProtocol.version,
        )
        return (
            ETHHandshaker(handshake_params),
        )


async_fire_and_forget = async_suppress_exceptions(PeerConnectionLost, asyncio.TimeoutError)  # type: ignore  # noqa: E501


class ETHPeerPoolEventServer(PeerPoolEventServer[ETHPeer]):
    """
    ETH protocol specific ``PeerPoolEventServer``. See ``PeerPoolEventServer`` for more info.
    """

    subscription_msg_types = frozenset({
        GetBlockHeaders,
        GetBlockBodies,
        GetReceipts,
        GetNodeData,
        Transactions,
        NewBlockHashes,
        NewBlock,
    })

    async def _run(self) -> None:

        self.run_daemon_event(SendBlockHeadersEvent, self.handle_block_headers_event)
        self.run_daemon_event(SendBlockBodiesEvent, self.handle_block_bodies_event)
        self.run_daemon_event(SendNodeDataEvent, self.handle_node_data_event)
        self.run_daemon_event(SendReceiptsEvent, self.handle_receipts_event)

        self.run_daemon_request(GetBlockHeadersRequest, self.handle_get_block_headers_request)
        self.run_daemon_request(GetReceiptsRequest, self.handle_get_receipts_request)
        self.run_daemon_request(GetBlockBodiesRequest, self.handle_get_block_bodies_request)
        self.run_daemon_request(GetNodeDataRequest, self.handle_get_node_data_request)

        await super()._run()

    @async_fire_and_forget
    async def handle_block_headers_event(self, event: SendBlockHeadersEvent) -> None:
        await self.try_with_session(
            event.session,
            lambda peer: peer.sub_proto.send_block_headers(event.headers)
        )

    @async_fire_and_forget
    async def handle_block_bodies_event(self, event: SendBlockBodiesEvent) -> None:
        await self.try_with_session(
            event.session,
            lambda peer: peer.sub_proto.send_block_bodies(event.blocks)
        )

    @async_fire_and_forget
    async def handle_node_data_event(self, event: SendNodeDataEvent) -> None:
        await self.try_with_session(
            event.session,
            lambda peer: peer.sub_proto.send_node_data(event.nodes)
        )

    @async_fire_and_forget
    async def handle_receipts_event(self, event: SendReceiptsEvent) -> None:
        await self.try_with_session(
            event.session,
            lambda peer: peer.sub_proto.send_receipts(event.receipts)
        )

    async def handle_get_block_headers_request(
            self,
            event: GetBlockHeadersRequest) -> Tuple[BlockHeader, ...]:
        peer = self.get_peer(event.session)
        return await peer.requests.get_block_headers(
            event.block_number_or_hash,
            event.max_headers,
            skip=event.skip,
            reverse=event.reverse,
            timeout=event.timeout
        )

    async def handle_get_receipts_request(self,
                                          event: GetReceiptsRequest) -> ReceiptsBundles:

        return await self.with_node_and_timeout(
            event.session,
            event.timeout,
            lambda peer: peer.requests.get_receipts(event.headers)
        )

    async def handle_get_block_bodies_request(self,
                                              event: GetBlockBodiesRequest) -> BlockBodyBundles:
        return await self.with_node_and_timeout(
            event.session,
            event.timeout,
            lambda peer: peer.requests.get_block_bodies(event.headers)
        )

    async def handle_get_node_data_request(self,
                                           event: GetNodeDataRequest) -> NodeDataBundles:
        return await self.with_node_and_timeout(
            event.session,
            event.timeout,
            lambda peer: peer.requests.get_node_data(event.node_hashes)
        )

    async def handle_native_peer_message(self,
                                         session: SessionAPI,
                                         cmd: CommandAPI,
                                         msg: Payload) -> None:

        if isinstance(cmd, GetBlockHeaders):
            await self.event_bus.broadcast(GetBlockHeadersEvent(session, cmd, msg))
        elif isinstance(cmd, GetBlockBodies):
            await self.event_bus.broadcast(GetBlockBodiesEvent(session, cmd, msg))
        elif isinstance(cmd, GetReceipts):
            await self.event_bus.broadcast(GetReceiptsEvent(session, cmd, msg))
        elif isinstance(cmd, GetNodeData):
            await self.event_bus.broadcast(GetNodeDataEvent(session, cmd, msg))
        elif isinstance(cmd, NewBlock):
            await self.event_bus.broadcast(NewBlockEvent(session, cmd, msg))
        elif isinstance(cmd, NewBlockHashes):
            await self.event_bus.broadcast(NewBlockHashesEvent(session, cmd, msg))
        elif isinstance(cmd, Transactions):
            await self.event_bus.broadcast(TransactionsEvent(session, cmd, msg))
        else:
            raise Exception(f"Command {cmd} is not broadcasted")


class ETHPeerPool(BaseChainPeerPool):
    peer_factory_class = ETHPeerFactory


class ETHProxyPeerPool(BaseProxyPeerPool[ETHProxyPeer]):

    def convert_session_to_proxy_peer(self,
                                      session: SessionAPI,
                                      event_bus: EndpointAPI,
                                      broadcast_config: BroadcastConfig) -> ETHProxyPeer:
        return ETHProxyPeer.from_session(
            session,
            self.event_bus,
            self.broadcast_config
        )
