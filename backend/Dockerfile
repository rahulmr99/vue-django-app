FROM lambci/lambda:build-python3.6

MAINTAINER "Noortheen" <jnoortheen@gmail.com>

WORKDIR /var/task

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc

RUN \
    yum -y update && \
    yum -y install yum-plugin-ovl && \
    yum -y install mysql-devel


COPY dev-requirements.txt dev-requirements.txt
COPY test-requirements.txt test-requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r dev-requirements.txt

#EXPOSE 8001
CMD ["bash"]
