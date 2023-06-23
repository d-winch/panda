FROM python:3.8

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN pip install --upgrade pip

COPY ./requirements.txt /panda/

RUN pip install --no-cache-dir --upgrade -r /panda/requirements.txt

COPY ./panda /panda

CMD ["uvicorn", "panda.main:app", "--host", "0.0.0.0", "--port", "80"]