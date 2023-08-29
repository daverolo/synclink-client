import random
from datetime import datetime, timezone, timedelta
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from models.get_state_finality_checkpoints_response_data import \
    GetStateFinalityCheckpointsResponseData
from utils.decide_majority_checkpoint import decide_majority_checkpoint, checkpoint_has_all_attributes, quorum

from config.config import config
from core.nodes import Nodes

logger.disable("apscheduler")

class SynclinkClient():
    def __init__(self, nodes: List[str]) -> None:
        self.percent_for_quorum = config.quorum_percent
        self.node_addresses = nodes
        self.nodes = Nodes(nodes)
        self.ready_nodes = []
        self.ready_finalized_nodes = []
        self.selected_ready_finalized_node = None
        self.find_ready_node_job = None
        self.head: GetStateFinalityCheckpointsResponseData = GetStateFinalityCheckpointsResponseData()
        self.syncpoint: GetStateFinalityCheckpointsResponseData = GetStateFinalityCheckpointsResponseData()
        self.syncpoint_changed = False
        self.syncpoint_initialized = False
        self.quorum_node_warning = False

    async def start(self):
        docs_addr = config.addr if config.addr != "0.0.0.0" else "127.0.0.1" 
        docs_port = config.port
        logger.success(f"Synclink Client started, find API docs at http://{docs_addr}:{docs_port}/docs")
        self.scheduler = AsyncIOScheduler(timezone = timezone.utc)
        self.find_ready_node_job = self.scheduler.add_job(self.find_ready_node, 'interval', seconds=5, max_instances=1)
        self.find_ready_node_job.modify(next_run_time=datetime.now(timezone.utc))
        self.scheduler.start()


    async def find_ready_node(self):

        if not len(self.ready_nodes):
            logger.info('Searching for at least one ready node..')

        ready_nodes = await self.nodes.get_readies()
        if not len(ready_nodes):
            if not len(self.ready_nodes):
                logger.warning('No ready node found! Will try again in 5 sec..')
            else:
                logger.warning('No ready node found anymore, reset system!')
                self.ready_nodes = []
                self.ready_finalized_nodes = []
                self.selected_ready_finalized_node = None
                self.head: GetStateFinalityCheckpointsResponseData = GetStateFinalityCheckpointsResponseData()
                self.syncpoint: GetStateFinalityCheckpointsResponseData = GetStateFinalityCheckpointsResponseData()
                self.syncpoint_changed = False
                self.syncpoint_initialized = False
                self.quorum_node_warning = False
                self.find_ready_node_job.modify(next_run_time=datetime.now(timezone.utc) + timedelta(milliseconds=500))
            return False
        self.ready_nodes = ready_nodes

        # No need to search finality if not enough ready nodes online
        if not quorum(len(self.node_addresses), len(self.ready_nodes), self.percent_for_quorum):
            logger.warning(f"No checkpoint quorum of {self.percent_for_quorum}% possible because only {str(len(self.ready_nodes))} of {str(len(self.node_addresses))} node(s) ready! Will try again in 5 sec..")
            self.quorum_node_warning = True
            return False
        elif self.quorum_node_warning:
            logger.warning(f"Checkpoint quorum of {self.percent_for_quorum}% possible again because {str(len(self.ready_nodes))} of {str(len(self.node_addresses))} node(s) ready.")
            self.quorum_node_warning = False
        
        await self.get_head_finality()
        await self.check_final_checkpoint()
        if not self.syncpoint.finalized:
            logger.warning(f"{str(len(self.ready_nodes))} ready node(s) found, waiting for checkpoint quorum of {self.percent_for_quorum}%! Will try again in 5 sec..")
            return False
        
        if self.syncpoint_changed:
            if not self.syncpoint_initialized:
                self.syncpoint_initialized = True
                logger.success(f"SyncPoint initialized - {str(len(self.ready_nodes))} node(s) ready, checkpoint quorum of {self.percent_for_quorum}% reached.")
                logger.success(f"Node {self.selected_ready_finalized_node.url} choosen as upstream")
            else:
                logger.success(f"SyncPoint updated - {str(len(self.ready_nodes))} node(s) ready, checkpoint quorum of {self.percent_for_quorum}% reached")
                logger.success(f"Node {self.selected_ready_finalized_node.url} choosen as upstream")
            logger.success(f"ROOT: {self.syncpoint.finalized.root}")
            logger.success(f"EPOCH: {self.syncpoint.finalized.epoch}")
            self.syncpoint_changed = False


    async def get_head_finality(self):
        checkpoints = []

        # Each node checkpoint must have all attributes available to decide majoroty!
        for node in self.ready_nodes:
            checkpoint = await node.api.beacon.state_finality_checkpoints('head')
            if checkpoint_has_all_attributes(checkpoint):
                checkpoints.append(checkpoint.data)

        final_head_checkpoint = decide_majority_checkpoint(checkpoints, len(self.node_addresses), self.percent_for_quorum)

        if final_head_checkpoint:
            if (not self.head or (not self.head.finalized) or (self.head.finalized.root != final_head_checkpoint.finalized.root)):
                self.head = final_head_checkpoint.copy()

    async def check_final_checkpoint(self):
        if not self.head or not self.head.finalized:
            return

        if (self.syncpoint.finalized != None and self.head.finalized.epoch == self.syncpoint.finalized.epoch):
            return

        checkpoint = self.head

        self.ready_finalized_nodes = await self.nodes.get_finalizes(nodes=self.ready_nodes, checkpoint=checkpoint)

        self.selected_ready_finalized_node = random.choice(self.ready_finalized_nodes)

        block = await self.selected_ready_finalized_node.api.beacon.block(checkpoint.finalized.root)

        await self.selected_ready_finalized_node.get_config()
        spec = self.selected_ready_finalized_node.config.spec

        if (int(block.data.message.slot) % int(spec.SLOTS_PER_EPOCH) != 0):
            if (not len(self.ready_nodes)):
                logger.error('Validate error block is not finalized.')


        self.syncpoint = checkpoint
        self.syncpoint_changed = True
        
        #logger.success(f"ROOT: {self.syncpoint.finalized.root}")
        #logger.success(f"EPOCH: {self.syncpoint.finalized.epoch}")


client = SynclinkClient(config.nodes)
