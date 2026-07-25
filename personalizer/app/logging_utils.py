import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("personalizer")


def log_agent_step(agent: str, state_in: dict, state_out: dict) -> None:
    logger.info(json.dumps({"agent": agent, "input_keys": list(state_in.keys()), "output": state_out}))
