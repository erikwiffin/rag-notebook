FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser worker
USER worker

RUN mkdir /caches/llama_index

COPY --chown=worker:worker . .

CMD [ "celery", "-A", "make_celery", "worker", "--loglevel", "INFO" ]