FROM hackinglab/alpine-base-hl:3.2
MAINTAINER Ivan Buetler <ivan.buetler@compass-security.com>

# Add the files
ADD root /

WORKDIR /app

RUN adduser -D flask  && \
    chown -R flask:flask /app && \
    echo "**** install Python ****" && \
    apk add --no-cache python3 py3-virtualenv py3-pip py3-flask && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -rf /var/cache/apk/* && \
    cd /app && \
    pip3 install -r requirements.txt --break-system-packages


# Expose the ports for nginx
EXPOSE 80
