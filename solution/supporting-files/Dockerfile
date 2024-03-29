FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "application.py"
# ENV FLASK_ENV "development"
# ENV FLASK_DEBUG True
ENV FLASK_RUN_PORT 5000

RUN mkdir /code
WORKDIR /code
ADD /app /code/
RUN pip install -r requirements.txt
EXPOSE 5000

CMD flask run --host=0.0.0.0