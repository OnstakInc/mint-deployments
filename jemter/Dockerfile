FROM openjdk:8

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install wget zip vim curl wget -y

RUN wget https://downloads.apache.org/jmeter/binaries/apache-jmeter-5.4.zip -O /tmp/apache-jmeter-5.4.zip
RUN unzip /tmp/apache-jmeter-5.4.zip -d /opt

COPY start.sh /opt/apache-jmeter-5.4/bin
COPY teastore_load.jmx /opt/apache-jmeter-5.4/teastore_load.jmx

WORKDIR /opt/apache-jmeter-5.4

ENTRYPOINT ["/bin/bash", "/opt/apache-jmeter-5.4/bin/start.sh"]