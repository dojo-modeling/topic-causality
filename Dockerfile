FROM python:3.10

ENV TRANSFORMERS_CACHE="/recommender/big_models_data_cache"
WORKDIR /recommender

RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /recommender/
RUN poetry install --no-root

COPY ./topic_causality /recommender/topic_causality
COPY ./README.md /recommender/README.md

RUN poetry install

CMD [ "poetry", "run", "python", "topic_causality/api.py" ]
