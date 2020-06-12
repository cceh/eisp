# cceh/eisp
FROM python:3.8-slim-buster
ADD . /tmp/eisp
RUN apt-get update && apt-get install -y \
    make
# eisp
RUN make -C /tmp/eisp
RUN find /root /tmp -mindepth 1 -delete
# runtime
ENTRYPOINT ["/usr/local/bin/eisp"]
