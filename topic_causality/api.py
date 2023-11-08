from __future__ import annotations

import uvicorn
from pydantic import BaseModel

from fastapi import (
    FastAPI
)
from fastapi.logger import logger
from typing import List, Optional
import torch

from topic_causality.model import recommender_engine

app = FastAPI()


class RequestBody(BaseModel):
    topic: str
    location: Optional[str]


class CausesResponseSchema(BaseModel):
    causes: List[str]


class EffectsResponseSchema(BaseModel):
    effects: List[str]


class AllResponseSchema(BaseModel):
    causes: List[str]
    effects: List[str]

@app.get("/healthcheck")
def get_healthcheck():
    return {
        "status": "OK",
        "gpu": torch.cuda.is_available()
    }


@app.post("/causal-recommender/causes", response_model=CausesResponseSchema)
def get_causality_recommendation_causes(payload: RequestBody):
    topic = payload.topic

    if (payload.location):
        topic = f"{topic} in {payload.location}"

    logger.info("Calculating causes for topic")

    causes = recommender_engine.get_causes(topic)
    return {"causes": causes}


@app.post("/causal-recommender/effects", response_model=EffectsResponseSchema)
def get_causality_recommendation_effects(payload: RequestBody):
    topic = payload.topic

    if (payload.location):
        topic = f"{topic} in {payload.location}"

    logger.info("Calculating effects for topic")

    effects = recommender_engine.get_effects(topic)
    return {"effects": effects}


@app.post("/causal-recommender", response_model=AllResponseSchema)
def get_causality_recommendation_both(payload: RequestBody):
    topic = payload.topic

    if (payload.location):
        topic = f"{topic} in {payload.location}"

    logger.info("Calculating effects for topic")

    return {
        "causes": recommender_engine.get_causes(payload.topic),
        "effects": recommender_engine.get_effects(topic)
    }


# uvicorn.run(
#     f"{__name__}:app",
#     host="0.0.0.0",
#     port=8084,
#     reload=True,
#     log_config="logging.yaml"
# )
