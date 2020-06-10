# cceh/eisp
FROM alpine:latest
ADD . /tmp/eisp
RUN \
#
# packages
apk --no-cache add \
  py3-lxml \
  py3-setuptools \
  py3-urllib3 \
  py3-wheel \
  python3 && \
apk --no-cache --virtual build add \
  make \
  py3-pip && \
#
# eisp
make -C /tmp/eisp && \
#
# cleanup
apk del --purge build && \
find /root /tmp -mindepth 1 -delete
#
# runtime
ENTRYPOINT ["/usr/bin/eisp"]
