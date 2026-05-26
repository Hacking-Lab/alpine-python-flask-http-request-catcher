FROM hackinglab/alpine-python-flask-hl:latest
LABEL maintainer="Ivan Buetler <ivan.buetler@hacking-lab.com>"

# Add the files
ADD root /

WORKDIR /opt/app
RUN chown flask:flask /opt/app

# Expose the ports for Flask app
EXPOSE 8080
