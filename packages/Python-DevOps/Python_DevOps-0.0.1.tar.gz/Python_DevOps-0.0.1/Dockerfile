FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

#CMD [ "python", "hi.py" ]

ENTRYPOINT ["/bin/bash", "-c", "/usr/bin/python3 -c 'from calculator import *;print(add(2,4))'"]
#RUN echo "from calculator import *; print('add two numer 2 and 4 and result is =',add(2,4))" > ./forrun.py
#CMD [ "python", "forrun.py" ]

#CMD [ "python", "helloworld.py" ]

