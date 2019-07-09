from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import platform

from football.crawler.utils import log_util as log, utils


import football.crawler.cra_route as cra_route
from football.crawler.craImpl import cra_data, cra_bifen, cra_oupei, gameImpl


"""
打包运行文件，打包的之后 运行这个------
"""
app = Flask(__name__)
app.register_blueprint(cra_route.simple_page)


# game_id_list_if=set([])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    query_date = request.args.get('queryDate')
    now = datetime.now()

    # 查询多天的日期 默认12天
    all_date = gameImpl.query_game_dates()
    # 根据日期做筛选
    if not query_date or len(query_date) < 4:
        query_date = datetime.today().strftime('%Y-%m-%d')
        result = gameImpl.query_game_info_day(query_date)
    # elif query_date >= today_date:
    #     result = gameImpl.query_game_info_day(query_date)
    else:
        result = gameImpl.query_game_info_day(query_date, query_type="DAY")
    return render_template("index.html", data=result, now=now, all_date=all_date, query_date=query_date)


@app.route('/trend/<gameId>')
def trend(gameId):
    dd = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    start_time = time.time()
    # 让球 即时欧赔 echart数据
    result = cra_data.query_pay_echart(dd, gameId)
    log.info("trend > query_pay_echart 耗时：%s" % utils.float_num(time.time() - start_time))

    # 比分指数 数据
    start_time = time.time()
    bifen_result = cra_bifen.query_record(gameId)
    log.info("trend > query_record 耗时：%s" % utils.float_num(time.time() - start_time))

    # 波胆
    start_time = time.time()
    bodan_data = cra_bifen.calc_bodan(bifen_result)
    log.info("trend > calc_bodan 耗时：%s" % utils.float_num(time.time() - start_time))

    # 计算即赔的波胆标准差
    start_time = time.time()
    bifen_sta_echart_data = cra_bifen.query_bodan_std(gameId)
    log.info("trend > start_time 耗时：%s" % utils.float_num(time.time() - start_time))

    # 百家欧赔
    start_time = time.time()
    baijia_oupei = cra_oupei.query_oupei_echart(dd, gameId)
    log.info("trend > query_oupei_echart 耗时：%s" % utils.float_num(time.time() - start_time))

    #欧赔初始凯利与即时凯利
    baijia_oupei_start = cra_oupei.query_oupei_echart2(gameId)
    baijia_oupei_end=cra_oupei.query_jishioupei_echart2(gameId)
    # print("baijia_oupei_start---------------------------")
    # print(baijia_oupei_start)

    #让球-竞彩初始凯利与即时凯利
    rangqiu_oupei_start = cra_oupei.query_oupei_echart3(gameId)
    rangqiu_oupei_end=cra_oupei.query_jishioupei_echart3(gameId)


    return render_template("trend_echart.html", data=result, baijia_oupei=baijia_oupei, bifen_result=bifen_result,
                           bodan_data=bodan_data, team=request.args.get('team'), bfs_data=bifen_sta_echart_data
                           , startTime=request.args.get('startTime'),oupei_kaili=baijia_oupei_start,rangqiu_kaili=rangqiu_oupei_start,
                           biajia_oupei_end=baijia_oupei_end,rangqiu_oupei_end=rangqiu_oupei_end)


def sch_method():
    time_inteval = 5
    if platform.node() == "DESKTOP-MKICEMAN":
        time_inteval = 18
    """ 每8分钟执行一次 """
    if datetime.now().minute % time_inteval == 0:
        start_time = time.time()
        game_id_list = cra_data.process_cra()

        #从oupei_start_info获取
        game_id_list_oupei=cra_oupei.query_oupei_gameId()
        for gameId in game_id_list:
            # print("gameId:-----------------------------------",gameId)
            gameId_id=gameId["game_no"]
            if gameId_id in game_id_list_oupei:
                print(gameId_id,":初始凯利已存在，无需抓取")
            else:
                print("开始抓取初始凯利--------------------",gameId_id)
                # 抓取初始欧赔凯利
                cra_oupei.cra_chupei_oupei([gameId])
                # 抓取让球初时凯利
                cra_oupei.cra_rangqiu_oupei([gameId])
                # game_id_list_if.add(gameId["game_no"])
                print("抓取完成",gameId_id)


        # 抓取比分
        cra_bifen.cra_bifen(game_id_list)
        # 抓取即时欧赔
        cra_oupei.cra_sub_oupei(game_id_list)
        print("抓取完成了 耗时：%s" % (float('%.2f' % (time.time() - start_time))))
    else:
        return


def run_job():
    scheduler = BlockingScheduler()
    # seconds,interval周期触发任务
    scheduler.add_job(sch_method, 'interval', max_instances=2, seconds=40)
    scheduler.start()
    print(time.time())


# python run.py
if __name__ == '__main__':
    print("tornado started")
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()
