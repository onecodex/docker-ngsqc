FROM quay.io/refgenomics/docker-ubuntu:14.04

MAINTAINER Nik Krumm <nkrumm@gmail.com>


# Install Java (Dependencies for FASTQC)
# from https://github.com/dockerfile/java/blob/master/openjdk-7-jre/Dockerfile

RUN \
  apt-get update && \
  apt-get install -y openjdk-7-jre && \
  rm -rf /var/lib/apt/lists/*

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64

# install wget and unzip
RUN apt-get update && apt-get install -y unzip wget

# Install FASTQC
RUN \
	wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.2.zip && \
	unzip fastqc_v0.11.2.zip && \
	chmod +x FastQC/fastqc && \
	ln -s /FastQC/fastqc /usr/local/bin/fastqc

# Install Skewer (adapter trimming)
RUN git clone https://github.com/relipmoc/skewer && \
	cd skewer && \
	git checkout e246277b0d7dfffa0b3e7fd9c0d61885e6486052 &&  \
	make && \
	make install

# Install wrapper FastQC -> JSON script
ADD fastqc_json.py /usr/local/bin/fastqc_json.py
RUN chmod +x /usr/local/bin/fastqc_json.py
RUN ln -s /usr/local/bin/fastqc_json.py /usr/local/bin/fastqc_json

# # Integration tests
# ADD test /tmp/test
# RUN bats /tmp/test
