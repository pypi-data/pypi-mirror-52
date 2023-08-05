from typing import List, NamedTuple, Optional

from plenum.common.config_util import getConfig
from plenum.common.messages.node_messages import PrePrepare, Checkpoint
from sortedcontainers import SortedListWithKey

from plenum.common.startable import Mode
from plenum.server.propagator import Requests
from plenum.server.quorums import Quorums

BatchID = NamedTuple('BatchID', [('view_no', int), ('pp_seq_no', int), ('pp_digest', str)])


def preprepare_to_batch_id(pre_prepare: PrePrepare) -> BatchID:
    return BatchID(pre_prepare.viewNo, pre_prepare.ppSeqNo, pre_prepare.digest)


class ConsensusSharedData:
    """
    This is a 3PC-state shared between Ordering, Checkpoint and ViewChange services.
    TODO: Consider depending on audit ledger
    TODO: Consider adding persistent local storage for 3PC certificates
    TODO: Restore primary name from audit ledger instead of passing through constructor
    """

    def __init__(self, name: str, validators: List[str], inst_id: int, is_master: bool = True):
        self._name = name
        self.inst_id = inst_id
        self.view_no = 0
        self.waiting_for_new_view = False
        # TODO: Do we need primaries for all instances here?
        #  Also this basically duplicates primary_name, so one of them needs to be removed.
        self.primaries = []
        self.is_master = is_master

        self.legacy_vc_in_progress = False
        self.requests = Requests()
        self.last_ordered_3pc = (0, 0)
        # Indicates name of the primary replica of this protocol instance.
        # None in case the replica does not know who the primary of the
        # instance is
        self.primary_name = None
        # seqNoEnd of the last stabilized checkpoint
        self.stable_checkpoint = 0
        # Checkpoint messages which the current node sent.
        self.checkpoints = SortedListWithKey(key=lambda checkpoint: checkpoint.seqNoEnd)
        # List of BatchIDs of PrePrepare messages for which quorum of Prepare messages is not reached yet
        self.preprepared = []  # type:  List[BatchID]
        # List of BatchIDs of PrePrepare messages for which quorum of Prepare messages is reached
        self.prepared = []  # type:  List[BatchID]
        self._validators = None
        self.quorums = None
        # a list of validator node names ordered by rank (historical order of adding)
        self.set_validators(validators)
        self.low_watermark = 0
        self.log_size = getConfig().LOG_SIZE
        self.high_watermark = self.low_watermark + self.log_size
        self.pp_seq_no = 0
        self.node_mode = Mode.starting
        # ToDo: it should be set in view_change_service before view_change starting
        # 3 phase key for the last prepared certificate before view change
        # started, applicable only to master instance
        self.legacy_last_prepared_before_view_change = None

    @property
    def name(self) -> str:
        return self._name

    def set_validators(self, validators: List[str]):
        self._validators = validators
        self.quorums = Quorums(len(validators))

    @property
    def validators(self) -> List[str]:
        """
        List of validator nodes aliases
        """
        return self._validators

    @property
    def is_primary(self) -> Optional[bool]:
        """
        Returns is replica primary for this instance.
        If primary name is not defined yet, returns None
        """
        return None if self.primary_name is None else self.primary_name == self.name

    @property
    def is_participating(self):
        return self.node_mode == Mode.participating

    @property
    def is_synced(self):
        return Mode.is_done_syncing(self.node_mode)

    @property
    def total_nodes(self):
        return len(self.validators)

    @property
    def last_checkpoint(self) -> Checkpoint:
        if not self.checkpoints:
            return None
        else:
            return self.checkpoints[-1]
