import base64

from app.graph_state import GraphState
from app.llm_client import ask_vision

VISION_PROMPT = """Look at this image from a learner. It might be a code error,
a screenshot of their progress/dashboard, or handwritten notes.
In one or two sentences, describe what topic or struggle this image suggests,
useful for recommending their next learning topic. Be concise."""


async def analyze_image(image_bytes: bytes) -> str:
    return await ask_vision(image_bytes, VISION_PROMPT)


async def vision_node(state: GraphState) -> dict:
    image_bytes = state.get("image_bytes")
    if not image_bytes:
        return {"image_signal": None}

    signal = await analyze_image(image_bytes)
    return {"image_signal": signal}
