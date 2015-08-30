# My Farm Report

부족 전쟁에서 동전줍기(이하 동줍)을 도와주는 스크립트이다.
지금은 없어져버린 twfarmreport.com과 비슷한 기능을 제공한다.


## 개발 환경

* OS: Ubuntu 14.10
* Python: 2.7.8
* Django: 1.6.10
* uWSGI: 2.0.11.1
* nginx: 1.6.2

## 요구사항

* 부족전쟁이 https 포트를 사용하므로 보안상 이슈로 서버 또한 https를 요구한다.

## nginx + uWSGI + django 설정하기

[참고 링크](http://knot.tistory.com/97)

1. uWSGI 설치

    `sudo pip install uwsgi`

2. nginx 설치하기

    `sudo apt-get install nginx`

3. 개인 인증서 만들기

   `sudo openssl req -newkey rsa:1024 -nodes -keyform PEM -keyout server.key -new -x509 -days 365 -outform PEM -out server.crt -utf8`

 KR, Seoul, 나머지는 무시한다. 

 server.crt, server.key가 만들어졌으면 완성된 것이다.
 이 두 파일을 `/etc/nginx/ssl/`에 옮겨준다.

4. nginx 설정하기

    * nginx.conf
       * worker_processes는 CPU 개수만큼 설정한다.
       * worker_connections는 예상 접속자수*2 이상이면서 worker_processes로 나누어 떨어지도록 설정한다.
       * worker_rlimit_nofile을 worker_connections와 동일하거나 크게 설정한다.
       * worker_processes 밑에 설정하면 된다.
       * keepalive_timeout을 30정도로 설정한다.


    * sites-enabled/default

 ```
upstream django {
	server unix:///tmp/myfarmreport.sock;
}

server {
    listen 443 default_server ssl;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    server_name localhost;
    location / {
		uwsgi_pass  django;
		include     /etc/nginx/uwsgi_params;
    }
    client_max_body_size 50M;
}
```


5. uWSGI + Django 실행

 아래 명령으로 실행한다.

 `uwsgi --socket /tmp/myfarmreport.sock --wsgi-file (your project path)/mwfarmreport/wsgi.py --chmod-socket=664`
