1. 启动命令:  
    celery -A tasks worker --loglevel=info
   
2. rabbitQ:  
    broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
   
3. redis:  
    redis://:password@hostname:port/db_number
   
4. 检查配置  
    python -m celery_config