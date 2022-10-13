FROM debian:latest

ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt upgrade -y && apt install python3 python3-pip -y

RUN mkdir /app
COPY ./ /app/
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/app/iquote.py"]
