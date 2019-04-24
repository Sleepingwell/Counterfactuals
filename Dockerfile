FROM python:3.7
COPY /package/requirements.txt /tmp
WORKDIR /pat/notebooks
RUN chmod 777 /pat && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y xorg openbox && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
ENV PYTHONPATH /pat/package
EXPOSE 8888
ENTRYPOINT ["jupyter"]
CMD ["notebook", "--ip", "0.0.0.0", "--port", "8888", "--allow-root"]
