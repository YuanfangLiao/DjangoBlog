echo "开始重启服务"
echo "尝试关闭nginx"
if `killall -9 nginx`
then
	`service nginx start`
	echo "nginx重启成功"
fi

echo "开始重启uwsgi"
if `killall -9 uwsgi`
then 
	`/root/.virtualenvs/py37_Dj21/bin/uwsgi -d --ini uwsgi.ini`
fi
