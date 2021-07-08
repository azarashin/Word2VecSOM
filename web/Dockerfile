FROM node:latest

RUN npm install -g npm
RUN more  package.json
COPY start.sh /home/web/start.sh
RUN chmod 755 /home/web/start.sh

ENTRYPOINT [ "/home/web/start.sh" ]
