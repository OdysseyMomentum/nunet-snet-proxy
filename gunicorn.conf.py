import os
proxy_port=os.getenv("API_PORT")

bind = "0.0.0.0:"+str(proxy_port)
workers = 3
timeout=600