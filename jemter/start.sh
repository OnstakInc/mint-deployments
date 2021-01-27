#!/bin/bash

rm -rf /opt/apache-jmeter-5.4/load.jmx
cp /opt/apache-jmeter-5.4/teastore_load.jmx /opt/apache-jmeter-5.4/load.jmx

sed -i "s/{{THREADS}}/${THREADS}/" /opt/apache-jmeter-5.4/load.jmx
sed -i "s/{{RAMP_TIME}}/${RAMP_TIME}/" /opt/apache-jmeter-5.4/load.jmx

sed -i "s/{{HOST}}/${HOST}/" /opt/apache-jmeter-5.4/load.jmx
sed -i "s/{{PORT}}/${PORT}/" /opt/apache-jmeter-5.4/load.jmx
sed -i "s/{{PROTOCOL}}/${PROTOCOL}/" /opt/apache-jmeter-5.4/load.jmx

/opt/apache-jmeter-5.4/bin/jmeter -n -t /opt/apache-jmeter-5.4/load.jmx -l /opt/apache-jmeter-5.4/test_output.csv -JThreadNumber=10 -JRampUpPeriod=10 -Jiterations=10