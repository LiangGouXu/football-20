# -*-coding:utf-8-*-
import requests
from lxml import etree
import time
import numpy as np

import random
from football.crawler.constants.timeout_constant import ConstantVal
from football.crawler.utils.DBUtils import DBUtils
from football.crawler.utils import utils
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ReadTimeout, ConnectTimeout
from football.crawler.craImpl import payInfoImpl


def cra_data_url(url, encoding="gb2312"):
    """
    :param url: 页面url
    :param encoding: 编码，默认gb2312
    抓取数据
    """
    session = requests.session()
    proxies = None

    # proxies = [
    #     {
    #         "http:": "http://222.168.41.246:8090"
    #     }
    # ]
    # url = "http://odds.500.com/yazhi_jczq.shtml"
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': 'bdshare_firstime=' + str(
                   int(time.time() * 1000)) + '; __utmz=63332592.1545544702.1.1.utmcsr=(direct)|utmccn=('
                                              'direct)|utmcmd=(none); ck_RegFromUrl=http%3A//odds.500.com/yazhi_jczq.shtml; '
                                              'WT_FPC=id=undefined:lv=1545553412636:ss=1545553412636; sdc_session=1545553412642; '
                                              'Hm_lvt_4f816d475bb0b9ed640ae412d6b42cab=1545544701,1545553413; '
                                              'Hm_lpvt_4f816d475bb0b9ed640ae412d6b42cab=1545553413; '
                                              '__utma=63332592.624522735.1545544702.1545544702.1545553415.2; __utmc=63332592; '
                                              'CLICKSTRN_ID=116.22.1.111-1545544699.545040::1883A6B4C23FEF9A197FDF30312303F6',
               'Host': 'odds.500.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/70.0.3538.67 Safari/537.36'}
    timeout = 10
    try:
        if proxies is not None:
            response = session.get(url, headers=headers, proxies=random.choice(proxies))
        else:
            response = session.get(url, headers=headers, timeout=timeout)
    except (ReadTimeoutError, ReadTimeout, ConnectTimeout) as b:
        print(b.args)
        return "读取超时了，如果网络状况不好，请修改上的超时时间 当前超时时间：%s 秒" % timeout
    content = response.content.decode(encoding, errors="ignore")
    return content


"""
读取第一列、5列 存入数据库
进入子页面
读取数据
存入数据库
读取
"""

print("开始了cra")


def cal_std(data):
    """
    计算平方差
    :param data: 要计算的数据
    :return:
    """
    return np.std(data)/np.mean(data)

def cal_std2(data):
    """
    计算方差:变异系数
    :param data: 要计算的数据
    :return:
    """
    return np.std(data)/np.mean(data)


# //tbody[@id="main-tbody"]//input[@type="checkbox"]/../text()
def cra_main_page():
    print("主页抓取：")
    # 先用测试数据
    # content = testData.str
    content = cra_data_url("http://odds.500.com/yazhi_jczq.shtml")
    # print(soup.select("#main-tbody input[type='checkbox']"))
    selector = etree.HTML(content)

    # 编号
    elemtsNo = selector.xpath('//tbody[@id="main-tbody"]'
                              '//input[@type="checkbox"]/@value')
    # 第一列 场次
    elemts1 = selector.xpath('//tbody[@id="main-tbody"]'
                             '//input[@type="checkbox"]/../text()')
    # 比赛时间
    elemtsTime = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                '/../../../@date-dtime')
    # 隐藏的第4列 比赛队名1
    elemtsTeam1 = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                 '/../../following-sibling::*[4]/a/text()')
    # 隐藏的第六列 比赛队名2
    elemtsTeam2 = selector.xpath('//tbody[@id="main-tbody"]//input[@type="checkbox"]'
                                 '/../../following-sibling::*[6]/a/text()')
    # elNo, el1, elTime, name1, name2
    # 可以开始存库了
    if elemtsNo and len(elemtsNo) > 0:
        exe_result = DBUtils.executeMany("replace into football_game_info values (%s, %s, %s, %s, %s)",
                                         zip(elemtsNo, elemts1, elemtsTime, elemtsTeam1, elemtsTeam2))
        print("主页保存条数：%s" % exe_result)
    else:
        print("主页抓取失败：%s" % content)


def analysis_all_sub_page(data, head_info='table[@id="datatb"]', col_index=3):
    """
    子页面的解析
    :rtype: object
    :param data: 要解析的数据
    :param head_info: 要抓取的表格的信息
    :param col_index: 数据所在列的索引
    :return:
    """
    # table[@id="datatb"]  tr
    selector = etree.HTML(data)
    all_data = {}

    # 胜
    # 即时凯利
    timeKellyWin = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 3) + ']//tr[2]/td[1]/text()')
    # 平
    timeKellyAvg = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 3) + ']//tr[2]/td[2]/text()')
    # 负
    timeKellylose = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                      '/../../following-sibling::*['
                                   + str(col_index + 3) + ']//tr[2]/td[3]/text()')
    all_data["Kelly"] = [list(map(float, timeKellyWin)),
                         list(map(float, timeKellyAvg)),
                         list(map(float, timeKellylose))]
    result_data = tuple(all_data["Kelly"])

    return result_data


def process_sub_page(testElemNo=None,
                     first_tmp_url="http://odds.500.com/fenxi/rangqiu-%s.shtml?lot=jczq",
                     next_tmp_url="http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&"
                                  "start=%d&r=1&style=0&guojia=0&chupan=0&lot=jczq",
                     table_name="pay_info"
                     ):
    startTotalTime = time.time()
    if testElemNo is not None:
        elemNoList = testElemNo
    else:
        elemNoList = DBUtils.execute("select game_no,start_datetime from football_game_info "
                                     "where start_datetime>now() order by start_datetime ")
    all_sub_data = []
    str_sql = "insert into " + table_name + "(kelly_win_num, kelly_avg_num, " \
                                            "kelly_lost_num, game_id) values(%s,%s,%s,%s) "
    # 设置解析列索引
    params = {}
    if table_name != "pay_info":
        params = {"col_index": 2}
    if not isinstance(elemNoList, list):
        print("不是数组:", end="")
        print(elemNoList)
        return []
    """  解析让球指数页面 """
    for elObj in elemNoList:
        startTime = time.time()
        time.sleep(ConstantVal.TIMER_INTERVAL)
        elNo = elObj["game_no"]

        url = first_tmp_url % elNo
        # 子页面第一页的数据,存在多页的情况
        all_grade_data = analysis_all_sub_page(cra_data_url(url, "utf-8"), **params)

        # 子页面其他页的数据
        start = 30
        while True:
            url = next_tmp_url % (elNo, start)
            htmlData = cra_data_url(url, "utf-8")
            if htmlData and len(htmlData.strip()) > 100:
                result = analysis_all_sub_page(htmlData, 'tr', **params)
                all_grade_data = concat_array(all_grade_data, result)
                start += 30
            else:
                break

        # 计算平方差
        if len(all_grade_data) > 0:
            avg_data = [str(float('%.3f' % cal_std(bb))) for bb in all_grade_data]
            avg_data.append(elNo)
            all_sub_data.append(avg_data)
            # count = DBUtils.executeOne(str_sql, avg_data)
        print(str(elNo) + " " + table_name + " 子页总共抓取条数：%s  耗时：%s" % (start, utils.float_num(time.time() - startTime)))
    count = DBUtils.executeMany(str_sql, all_sub_data)
    print("子页面保存数量：%s 耗时：%s" % (count, utils.float_num(time.time() - startTotalTime)))
    return elemNoList



#######################
##########################################
def analysis_all_sub_page3(data, head_info='table[@id="datatb"]', col_index=3):
    """
    子页面的解析
    :rtype: object
    :param data: 要解析的数据
    :param head_info: 要抓取的表格的信息
    :param col_index: 数据所在列的索引
    :return:
    """
    # table[@id="datatb"]  tr
    selector = etree.HTML(data)
    all_data = {}

    # 胜
    # 初始凯利
    timeKellyWin = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 4) + ']//tr[1]/td[1]/text()')

    # 平
    timeKellyAvg = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 4) + ']//tr[1]/td[2]/text()')
    # 负
    timeKellylose = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                      '/../../following-sibling::*['
                                   + str(col_index + 4) + ']//tr[1]/td[3]/text()')

    # 胜
    # 即时凯利
    # timeKellyWin_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                  '/../../following-sibling::*['
    #                               + str(col_index + 4) + ']//tr[2]/td[1]/text()')
    # # 平
    # timeKellyAvg_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                  '/../../following-sibling::*['
    #                               + str(col_index + 4) + ']//tr[2]/td[2]/text()')
    # # 负
    # timeKellylose_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                   '/../../following-sibling::*['
    #                                + str(col_index + 4) + ']//tr[2]/td[3]/text()')



    all_data["Kelly"] = [list(map(float, timeKellyWin)),
                         list(map(float, timeKellyAvg)),
                         list(map(float, timeKellylose))
                         ]
    result_data = tuple(all_data["Kelly"])
    return result_data


def analysis_all_sub_page2(data, head_info='table[@id="datatb"]', col_index=3):
    """
    子页面的解析
    :rtype: object
    :param data: 要解析的数据
    :param head_info: 要抓取的表格的信息
    :param col_index: 数据所在列的索引
    :return:
    """
    # table[@id="datatb"]  tr
    selector = etree.HTML(data)
    all_data = {}

    # 胜
    # 初始凯利
    timeKellyWin = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 3) + ']//tr[1]/td[1]/text()')

    # 平
    timeKellyAvg = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                     '/../../following-sibling::*['
                                  + str(col_index + 3) + ']//tr[1]/td[2]/text()')
    # 负
    timeKellylose = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                      '/../../following-sibling::*['
                                   + str(col_index + 3) + ']//tr[1]/td[3]/text()')

    # 胜
    # 即时凯利
    # timeKellyWin_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                  '/../../following-sibling::*['
    #                               + str(col_index + 3) + ']//tr[2]/td[1]/text()')
    # # 平
    # timeKellyAvg_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                  '/../../following-sibling::*['
    #                               + str(col_index + 3) + ']//tr[2]/td[2]/text()')
    # # 负
    # timeKellylose_jishi = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
    #                                                   '/../../following-sibling::*['
    #                                + str(col_index + 3) + ']//tr[2]/td[3]/text()')



    all_data["Kelly"] = [list(map(float, timeKellyWin)),
                         list(map(float, timeKellyAvg)),
                         list(map(float, timeKellylose))
                         ]
    result_data = tuple(all_data["Kelly"])
    return result_data


def process_sub_page2(testElemNo=None,
                     first_tmp_url="http://odds.500.com/fenxi/rangqiu-%s.shtml?lot=jczq",
                     next_tmp_url="http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&"
                                  "start=%d&r=1&style=0&guojia=0&chupan=0&lot=jczq",
                     table_name="oupei_startvalue_info"
                     ):
    startTotalTime = time.time()
    if testElemNo is not None:
        elemNoList = testElemNo
    else:
        elemNoList = DBUtils.execute("select game_no,start_datetime from football_game_info "
                                     "where start_datetime>now() order by start_datetime ")
    all_sub_data = []
    str_sql = "insert into " + table_name + "(kelly_win_num, kelly_avg_num, " \
                                            "kelly_lost_num,game_id) values(%s,%s,%s,%s) "

    # 设置解析列索引
    params = {}
    if table_name != "pay_info":
        params = {"col_index": 2}
    if not isinstance(elemNoList, list):
        print("不是数组:", end="")
        print(elemNoList)
        return []
    """  解析让球指数页面 """
    for elObj in elemNoList:
        startTime = time.time()
        time.sleep(ConstantVal.TIMER_INTERVAL)
        elNo = elObj["game_no"]

        url = first_tmp_url % elNo
        # 子页面第一页的数据,存在多页的情况
        all_grade_data = analysis_all_sub_page2(cra_data_url(url, "utf-8"), **params)

        # 子页面其他页的数据
        start = 30
        while True:
            url = next_tmp_url % (elNo, start)
            htmlData = cra_data_url(url, "utf-8")
            if htmlData and len(htmlData.strip()) > 100:
                result = analysis_all_sub_page2(htmlData, 'tr', **params)
                all_grade_data = concat_array(all_grade_data, result)
                start += 30
            else:
                break

        # 计算平方差
        if len(all_grade_data) > 0:
            avg_data = [str(float('%.3f' % cal_std2(bb))) for bb in all_grade_data]
            # print("Test1--------------------", avg_data)
            avg_data.append(elNo)
            # print("Test2--------------------", avg_data)
            all_sub_data.append(avg_data)
            # count = DBUtils.executeOne(str_sql, avg_data)
        print(str(elNo) + " " + table_name + " 子页总共抓取条数：%s  耗时：%s" % (start, utils.float_num(time.time() - startTime)))
    count = DBUtils.executeMany(str_sql, all_sub_data)
    print(all_sub_data)
    print("子页面保存数量：%s 耗时：%s" % (count, utils.float_num(time.time() - startTotalTime)))
    return elemNoList


def process_sub_page3(testElemNo=None,
                     first_tmp_url="http://odds.500.com/fenxi/rangqiu-%s.shtml?lot=jczq",
                     next_tmp_url="http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&"
                                  "start=%d&r=1&style=0&guojia=0&chupan=0&lot=jczq",
                     table_name="rangqiu_startvalue_info"
                     ):
    startTotalTime = time.time()
    if testElemNo is not None:
        elemNoList = testElemNo
    else:
        elemNoList = DBUtils.execute("select game_no,start_datetime from football_game_info "
                                     "where start_datetime>now() order by start_datetime ")
    all_sub_data = []
    str_sql = "insert into " + table_name + "(kelly_win_num, kelly_avg_num, " \
                                            "kelly_lost_num,game_id) values(%s,%s,%s,%s) "

    # 设置解析列索引
    params = {}
    if table_name != "pay_info":
        params = {"col_index": 2}
    if not isinstance(elemNoList, list):
        print("不是数组:", end="")
        print(elemNoList)
        return []
    """  解析让球指数页面 """
    for elObj in elemNoList:
        startTime = time.time()
        time.sleep(ConstantVal.TIMER_INTERVAL)
        elNo = elObj["game_no"]

        url = first_tmp_url % elNo
        # 子页面第一页的数据,存在多页的情况
        all_grade_data = analysis_all_sub_page3(cra_data_url(url, "utf-8"), **params)

        # 子页面其他页的数据
        start = 30
        while True:
            url = next_tmp_url % (elNo, start)
            htmlData = cra_data_url(url, "utf-8")
            if htmlData and len(htmlData.strip()) > 100:
                result = analysis_all_sub_page3(htmlData, 'tr', **params)
                all_grade_data = concat_array(all_grade_data, result)
                start += 30
            else:
                break

        # 计算平方差
        if len(all_grade_data) > 0:
            avg_data = [str(float('%.3f' % cal_std2(bb))) for bb in all_grade_data]
            avg_data.append(elNo)
            all_sub_data.append(avg_data)
            # count = DBUtils.executeOne(str_sql, avg_data)
        print(str(elNo) + " " + table_name + " 子页总共抓取条数：%s  耗时：%s" % (start, utils.float_num(time.time() - startTime)))
    count = DBUtils.executeMany(str_sql, all_sub_data)
    print(all_sub_data)
    print("子页面保存数量：%s 耗时：%s" % (count, utils.float_num(time.time() - startTotalTime)))
    return elemNoList

#########################################



def query_pay_echart(dd, gameId):
    """ 查询让球赔率 """
    return payInfoImpl.query_pay_echart(dd, gameId)


def concat_array(total_arr, target_arr):
    """
    将两个对象进行拼接
    :param total_arr: 总数组
    :param target_arr: 目标数组
    :return: 返回拼接了目标数组的总数组
    """
    total_arr = [dt1 + dt2 for dt1, dt2 in zip(total_arr, target_arr)]
    return total_arr


def process_cra():
    cra_main_page()
    # 调用子页面的解析
    try:
        return process_sub_page()
    except Exception as e:
        print()


def main():
    startTotalTime = time.time()
    cra_main_page()
    print("总共时间：%s" % (time.time() - startTotalTime))


if __name__ == "__main__":
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # scheduler = BlockingScheduler()
    #
    # scheduler.add_job(main, 'interval', seconds=40)
    # scheduler.start()

    print(cra_data_url("http://odds.500.com/yazhi_jczq.shtml"))

    # process_sub_page_thread()
    # process_sub_page({"game_no":735071}) # 15  104
    # cra_main_page()
