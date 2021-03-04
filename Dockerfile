# Create a ubuntu base image with python 3 installed.
FROM python:3

# Set the working directory
WORKDIR /usr/src/app

# copy all the files
COPY . .

# Install the dependencies
RUN apt-get -y update
RUN pip3 install -r requirements.txt

# Expose the required port
EXPOSE 80

# Run the command
CMD gunicorn -b 0.0.0.0:80 --log-level=debug app:app