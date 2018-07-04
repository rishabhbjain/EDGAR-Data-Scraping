# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /edgardatascrapping
WORKDIR /edgardatascrapping
# Copy the current directory contents into the container at /edgardatascrapping
ADD . /edgardatascrapping

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install lxml





























