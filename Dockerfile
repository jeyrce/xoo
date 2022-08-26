FROM python:3.10.6-alpine3.16
WORKDIR /xoo
LABEL Author=Jeyrce<jeyrce@gmail.com> \
      PoweredBy=https://github.com/jeyrce/xoo
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/  \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir && \
    python /xoo/manage.py collectstatic

VOLUME /xoo/media/ /xoo/xoo/settings.py
ENV AUTH_USERNAME='xoo'
ENV AUTH_PASSWORD='一船清梦压星河'

EXPOSE 80
ENTRYPOINT [\
    "python", \
    "manage.py", \
    "runserver", \
    "--noreload", \
    "--insecure", \
    "--no-color", \
    "0.0.0.0:80" \
]
