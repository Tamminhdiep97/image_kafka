
FROM python:3.6

WORKDIR /usr/app
RUN apt-get update
RUN apt install libgl1-mesa-glx -y
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

CMD ["python", "app.py"]
