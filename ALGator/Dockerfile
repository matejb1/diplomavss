FROM sapmachine:17.0.10-jre-headless-ubuntu-jammy
WORKDIR /app
COPY ALGator.jar entrypoint.sh ./
ADD lib /app/lib
CMD ["sh", "entrypoint.sh"]