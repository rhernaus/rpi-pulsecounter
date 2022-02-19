FROM python

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python -u ./pulsecounter.py