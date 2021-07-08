FROM python:3

WORKDIR /home/som

RUN apt update
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file sudo

RUN apt install -y fonts-takao-gothic locales 

RUN locale-gen ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8