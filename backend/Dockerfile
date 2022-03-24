FROM python:3.9.0-slim-buster

ARG HOME
WORKDIR $HOME

RUN apt-get update && \
    apt-get install -y gcc gettext-base libopencv-dev git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock* ./

#RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip && pip install poetry 
RUN pip install -U pip && pip install poetry 
RUN poetry config virtualenvs.create false
#RUN --mount=type=cache,target=/root/.cache/pypoetry poetry install
RUN poetry install

COPY ./ .

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME}

ENTRYPOINT ["./entrypoint.sh"]
