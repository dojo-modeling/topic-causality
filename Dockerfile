FROM python:3.10

ENV TRANSFORMERS_CACHE="/recommender/big_models_data_cache"
WORKDIR /recommender

RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /recommender/
RUN poetry install --no-root

RUN poetry run python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2-xl')"

COPY ./topic_causality /recommender/topic_causality
COPY ./README.md /recommender/README.md

RUN poetry install

CMD [ "poetry", "run", "python", "topic_causality/api.py" ]
