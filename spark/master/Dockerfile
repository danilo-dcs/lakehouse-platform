# MASTER NODE

FROM bitnami/spark:3.5.1

USER root

RUN install_packages curl

USER 1001

RUN mkdir -p /opt/bitnami/spark/scripts

COPY ./spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf

# # Remiving hadoop jars
# RUN rm -r /opt/bitnami/spark/jars

# # Adding compatible hadoop jars to spark:3.5.0
# RUN curl --location https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz | \
# tar --extract --gzip --strip=1 --directory /opt/bitnami/spark/ spark-3.5.1-bin-hadoop3/jars/

# Removing old jar files
RUN rm -f /opt/bitnami/spark/jars/hadoop-aws-*.jar

RUN rm -f /opt/bitnami/spark/jars/hadoop-common-*.jar

RUN rm -f /opt/bitnami/spark/jars/gcs-connector-*.jar

RUN rm -f /opt/bitnami/spark/jars/aws-java-sdk-bundle-*.jar 

# Adding hadoop aws jar
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.4.0/hadoop-aws-3.4.0.jar --output /opt/bitnami/spark/jars/hadoop-aws-3.4.0.jar

# Adding hadoop common jar
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.4.0/hadoop-common-3.4.0.jar --output /opt/bitnami/spark/jars/hadoop-common-3.4.0.jar

# Google Cloud Connector Jar
RUN curl https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/3.0.1/gcs-connector-3.0.1.jar --output /opt/bitnami/spark/jars/gcs-connector-3.0.1.jar

# AWS S3 Connector Jar
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.761/aws-java-sdk-bundle-1.12.761.jar --output /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.761.jar

# Expose any necessary ports (e.g., Spark master port, worker port, etc.)
EXPOSE 7077 8080 6060

# Set the entrypoint to the Spark start script
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]

# Specify the default command to start the Spark master with REST API enabled
CMD ["/opt/bitnami/spark/bin/spark-class", "org.apache.spark.deploy.master.Master", "--host", "0.0.0.0", "--port", "7077", "--webui-port", "8080"]