# base image
FROM node:latest

# make the 'app' folder the current working directory
RUN mkdir /app
WORKDIR /app

# expose port 8080 to the host
EXPOSE 8080

# Start the `start` script.
CMD ["/app/docker/dev/start.sh"]
