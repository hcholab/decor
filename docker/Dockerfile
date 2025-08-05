FROM ubuntu:latest
LABEL Name=decor \
      Version=0.0.1 \
      Description="Docker image for Decor with Sequre plugin"

RUN \
    apt-get update && \
    apt-get install -y \
    curl openssl vim time git \
    patch python3 python3-pip

ENV CODON_PYTHON=/usr/lib/x86_64-linux-gnu/libpython3.12.so
ENV SEQURE_GMP_PATH=/sequre/external/GMP/lib/libgmp.so

# Install Sequre
RUN mkdir /.codon && curl -L https://github.com/exaloop/codon/releases/download/v0.17.0/codon-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C /.codon --strip-components=1 \
    && curl -L https://github.com/0xTCG/sequre/releases/download/v0.0.20-alpha/sequre-$(uname -s | awk '{print tolower($0)}')-$(uname -m).tar.gz | tar zxvf - -C /.codon/lib/codon/plugins

# Apply Decor patch
RUN git clone --depth 1 -b decor-patch https://github.com/0xTCG/sequre.git /sequre \
    && cp -r /sequre/stdlib /.codon/lib/codon/plugins/sequre/

# Set up sequre alias for all users
RUN echo 'alias sequre="/.codon/bin/codon run --disable-opt=\"core-pythonic-list-addition-opt\" -plugin sequre"' >> /etc/bash.bashrc

# Copy Decor
COPY . /decor
WORKDIR /decor

# Install py deps
RUN apt install -y python3-numpy python3-sklearn
