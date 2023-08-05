version: '2'
services:
    mock_server_web:
        image: kalaiya/howfo:V1.0
        container_name: mock_server_web
        ports:
          - "8000:8000"
        volumes:
            # app
          - ../:/root/www/web/
          - /app/data/:/root/data/
        command: ["bash", "-c", "cd /root/www/web && nohup gunicorn -c ./deploy/gunicorn.conf server:app"]
        network_mode: "bridge"