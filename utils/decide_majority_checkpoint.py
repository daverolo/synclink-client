import math
from typing import List

from models.get_state_finality_checkpoints_response_data import \
    GetStateFinalityCheckpointsResponseData

from utils.eth import hex_to_dec_string

def checkpoint_has_all_attributes(checkpoint: GetStateFinalityCheckpointsResponseData):
    if not hasattr(checkpoint, 'data'):
        return False
    data = checkpoint.data
    required_attributes = ['previous_justified', 'current_justified', 'finalized']
    for attr in required_attributes:
        if not hasattr(data, attr) or not hasattr(getattr(data, attr), 'root'):
            return False
    return True

def quorum(num_total: int, num_active: int, percent_for_quorum: int = 66):
    if num_total <= 0 or num_active <= 0 or num_total < num_active:
        return False
    if percent_for_quorum > 100:
        percent_for_quorum = 100
    if percent_for_quorum < 0:
        percent_for_quorum = 0
    required_quorum = math.ceil(num_total * percent_for_quorum / 100)
    if num_active >= required_quorum:
        return True
    return False

def generate_key(checkpoint: GetStateFinalityCheckpointsResponseData):
    key_chunk_0 = hex_to_dec_string(checkpoint.previous_justified.root)
    key_chunk_1 = hex_to_dec_string(checkpoint.current_justified.root)
    key_chunk_2 = hex_to_dec_string(checkpoint.finalized.root)

    key = f"{key_chunk_0}-{key_chunk_1}_{key_chunk_2}"

    return key


def decide_majority_checkpoint(
        checkpoints: List[GetStateFinalityCheckpointsResponseData],
        num_total_nodes: int,
        percent_for_quorum: int = 66
    ) -> GetStateFinalityCheckpointsResponseData:
    checkpoints_repeats = {}

    for checkpoint in checkpoints:
        key = generate_key(checkpoint)
        if key in checkpoints_repeats:
            checkpoints_repeats[key]["count"] += 1
        else:
            checkpoints_repeats[key] = {
                "finality": checkpoint,
                "count": 1
            }

        for _, value in checkpoints_repeats.items():
            if quorum(num_total_nodes, value['count'], percent_for_quorum):
                return (value['finality'])
