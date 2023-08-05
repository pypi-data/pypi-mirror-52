from functools import partial

import pytest

from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.common.messages.internal_messages import RequestPropagates
from plenum.common.startable import Mode
from plenum.common.event_bus import InternalBus
from plenum.common.messages.node_messages import PrePrepare, ViewChange
from plenum.common.stashing_router import StashingRouter
from plenum.common.util import get_utc_epoch
from plenum.server.consensus.consensus_shared_data import ConsensusSharedData
from plenum.common.messages.node_messages import Checkpoint
from plenum.server.consensus.view_change_service import ViewChangeService
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_managers.write_request_manager import WriteRequestManager
from plenum.test.checkpoints.helper import cp_digest
from plenum.test.consensus.helper import primary_in_view
from plenum.test.greek import genNodeNames
from plenum.test.helper import MockTimer, MockNetwork
from plenum.test.testing_utils import FakeSomething


@pytest.fixture(params=[4, 6, 7])
def validators(request):
    return genNodeNames(request.param)


@pytest.fixture(params=[0, 2])
def initial_view_no(request):
    return request.param


@pytest.fixture(params=[False, True])
def already_in_view_change(request):
    return request.param


@pytest.fixture
def primary(validators):
    return partial(primary_in_view, validators)


@pytest.fixture
def initial_checkpoints(initial_view_no):
    return [Checkpoint(instId=0, viewNo=initial_view_no, seqNoStart=0, seqNoEnd=0, digest=cp_digest(0))]


@pytest.fixture
def consensus_data(validators, primary, initial_view_no, initial_checkpoints, is_master):
    def _data(name):
        data = ConsensusSharedData(name, validators, 0, is_master)
        data.view_no = initial_view_no
        data.checkpoints.update(initial_checkpoints)
        return data

    return _data


@pytest.fixture
def view_change_service(internal_bus, external_bus, stasher):
    data = ConsensusSharedData("some_name", genNodeNames(4), 0)
    return ViewChangeService(data, MockTimer(0), internal_bus, external_bus, stasher)


@pytest.fixture
def pre_prepare():
    return PrePrepare(
        0,
        0,
        1,
        get_utc_epoch(),
        ['f99937241d4c891c08e92a3cc25966607315ca66b51827b170d492962d58a9be'],
        '[]',
        'f99937241d4c891c08e92a3cc25966607315ca66b51827b170d492962d58a9be',
        DOMAIN_LEDGER_ID,
        'CZecK1m7VYjSNCC7pGHj938DSW2tfbqoJp1bMJEtFqvG',
        '7WrAMboPTcMaQCU1raoj28vnhu2bPMMd2Lr9tEcsXeCJ',
        0,
        True
    )


@pytest.fixture(scope='function',
                params=[Mode.starting, Mode.discovering, Mode.discovered,
                        Mode.syncing, Mode.synced])
def mode_not_participating(request):
    return request.param


@pytest.fixture(scope='function',
                params=[Mode.starting, Mode.discovering, Mode.discovered,
                        Mode.syncing, Mode.synced, Mode.participating])
def mode(request):
    return request.param


@pytest.fixture
def view_change_message():
    def _view_change(view_no: int):
        vc = ViewChange(
            viewNo=view_no,
            stableCheckpoint=4,
            prepared=[],
            preprepared=[],
            checkpoints=[Checkpoint(instId=0, viewNo=view_no, seqNoStart=0, seqNoEnd=4, digest=cp_digest(4))]
        )
        return vc

    return _view_change


@pytest.fixture(params=[True, False])
def is_master(request):
    return request.param


@pytest.fixture()
def internal_bus():
    def rp_handler(ib, msg):
        ib.msgs.setdefault(type(msg), []).append(msg)

    ib = InternalBus()
    ib.msgs = {}
    ib.subscribe(RequestPropagates, rp_handler)
    return ib


@pytest.fixture()
def external_bus():
    return MockNetwork()


@pytest.fixture()
def bls_bft_replica():
    return FakeSomething(gc=lambda *args, **kwargs: True,
                         validate_pre_prepare=lambda *args, **kwargs: None,
                         update_prepare=lambda params, lid: params,
                         process_prepare=lambda *args, **kwargs: None,
                         process_pre_prepare=lambda *args, **kwargs: None,
                         validate_prepare=lambda *args, **kwargs: None,
                         validate_commit=lambda *args, **kwargs: None,
                         update_commit=lambda params, pre_prepare: params,
                         process_commit=lambda *args, **kwargs: None)


@pytest.fixture()
def db_manager():
    dbm = DatabaseManager()
    return dbm


@pytest.fixture()
def write_manager(db_manager):
    return WriteRequestManager(database_manager=db_manager)


@pytest.fixture()
def stasher(internal_bus, external_bus):
    return StashingRouter(limit=100000, buses=[internal_bus, external_bus])
