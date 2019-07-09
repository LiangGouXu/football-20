#### 安装
在football_web目录执行如命令
python setup.py install
尝试
python setup.py install -i https://pypi.tuna.tsinghua.edu.cn/simple/
> python3.x 以上，当系统中同时存在2和3的时候，一般直接使用python3即可

##### tar.gz包安装
pip或者pip3 install football-version.tar.gz -U

#### 启动项目
在football_web目录里面执行如下命令
python run.py

#### 启动定时器
python run_timer.py

#### 启用代理功能
football/crawler/craImpl/cra_data.py
在上面文件的第24行加上代理ip，然后去掉21和27行的三个引号即可

#### 修改各个网页抓取间隔时间，单位是 秒
football/crawler/constants/timeout_constant.py
TIMER_INTERVAL