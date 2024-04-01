FROM python:3

ENV FLASK_APP "app.py"
ENV FLASK_RUN_PORT 5000

ARG UID = 1000
ARG GID = 1000

RUN mkdir /site
WORKDIR /site
ADD /app /site/
RUN pip install -r requirements.txt
EXPOSE 5000

CMD flask run --host=0.0.0.0