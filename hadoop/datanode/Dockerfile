FROM apache/hadoop:3.3.5

USER root

# Create a new user and group (if not already present)
# RUN groupadd -g 1000 hadoop-gp 

RUN useradd -u 1001 -g hadoop -m -s /bin/bash hadoop-api

# Add the user to the sudoers file (optional)
RUN echo "hadoop-api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["hdfs", "datanode"]
