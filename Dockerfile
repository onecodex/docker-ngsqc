FROM quay.io/aptible/ubuntu:16.04

MAINTAINER Christopher Smith <christopher@onecodex.com>


# Install Java (Dependencies for FASTQC)
# from https://github.com/dockerfile/java/blob/master/openjdk-8-jre/Dockerfile

RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jre python-dev && \
  rm -rf /var/lib/apt/lists/*

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# install wget and unzip
RUN apt-get update && apt-get install -y unzip wget

# Install FASTQC
RUN \
	wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip && \
	unzip fastqc_v0.11.5.zip && \
	chmod +x FastQC/fastqc && \
	ln -s /FastQC/fastqc /usr/local/bin/fastqc

# Install wrapper FastQC -> JSON script
ADD run_fastqc.py /usr/local/bin/run_fastqc.py
RUN chmod +x /usr/local/bin/run_fastqc.py
RUN ln -s /usr/local/bin/run_fastqc.py /usr/local/bin/run_fastqc
