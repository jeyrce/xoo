FROM python:3.10.6-slim
WORKDIR /xoo
LABEL Author=Jeyrce<jeyrce@gmail.com> \
      PoweredBy=https://github.com/jeyrce/xoo
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/  \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir

VOLUME /var/lib/xoo/media/ /xoo/db.sqlite3 /xoo/xoo/settings.py
ENV XOO_AES_KEY='青青子衿悠悠我心'

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
