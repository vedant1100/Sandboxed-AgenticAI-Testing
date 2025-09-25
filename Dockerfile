# FROM python:3.11-slim
# RUN pip install bandit
# WORKDIR /code

FROM python:3.11
RUN pip install bandit
WORKDIR /app
ENTRYPOINT ["bandit"]
CMD ["-h"]
