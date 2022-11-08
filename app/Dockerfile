FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PANDAS_VERSION 1.4.1
ENV PYTEST_VERSION 7.2.0 


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
                    curl \
                    cron \
                    gcc \
                    git \
                    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY . /app


RUN pip install pandas==${PANDAS_VERSION} \
                pytest==${PYTEST_VERSION}

ENTRYPOINT ["python /app/jobs.py" ]
