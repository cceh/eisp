# cceh/eisp
FROM alpine:edge
ADD . /tmp/eisp
RUN \
# packages
apk --no-cache add \
  py3-setuptools \
  pkgconfig \
  g++ \
  python3-dev \
  poppler-dev \
  py3-urllib3 \
  python3 && \
apk --no-cache --virtual build add \
  make \
  py3-pip && \
# eisp
make -C /tmp/eisp && \
# cleanup
apk del --purge build && \
find /root /tmp -mindepth 1 -delete
# runtime
ENTRYPOINT ["/usr/bin/eisp"]
