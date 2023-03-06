FROM python:3.10

WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /app
RUN rm settings.ini

CMD streamlit run --server.port 8501 --server.enableCORS false overview.py
