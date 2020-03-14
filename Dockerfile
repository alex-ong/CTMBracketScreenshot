FROM python:3

WORKDIR /usr/src/app

#copy source code
COPY . .

#install poppler-utils
RUN apt-get update && apt-get install -y \
	poppler-utils 

#install pip requirements
RUN pip install --no-cache-dir -r requirements.txt

#open port 8080
EXPOSE 8080

#run the app
CMD ["python", "./main.py"]
