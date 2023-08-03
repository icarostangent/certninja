FROM openresty/openresty:1.21.4.2-0-buster-fat

RUN mkdir -p /var/lib/GeoIP/

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpcre++-dev \
        zlib1g-dev \
        libgeoip-dev \
        libssl-dev \
        libmaxminddb-dev \
        wget \
        git \
        libmaxminddb0

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN cd /opt \
    && git clone --depth 1 --single-branch https://github.com/leev/ngx_http_geoip2_module.git \
    && wget -o - http://openresty.org/download/openresty-1.21.4.2.tar.gz \
    && tar zxvf openresty-1.21.4.2.tar.gz \
    && rm openresty-1.21.4.2.tar.gz \
    && mv /opt/openresty-1.21.4.2 /opt/openresty \
    && cd /opt/openresty \
    && ./configure --with-compat --add-dynamic-module=/opt/ngx_http_geoip2_module \
    && make \
    && make install 
