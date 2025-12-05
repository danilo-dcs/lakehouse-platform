FROM apache/hadoop:3.3.5

USER root

RUN useradd -u 1001 -g hadoop -m -s /bin/bash hadoop-api

RUN echo "hadoop-api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["yarn", "resourcemanager"]
