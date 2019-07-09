from football.crawler.craImpl import cra_data
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import bs4
import time
from urllib.parse import urlparse, parse_qs
from football.crawler.utils.DBUtils import DBUtils
from football.crawler.constants.timeout_constant import ConstantVal
import re
from football.crawler.craImpl import bifenImpl
from football.crawler.utils import utils
import numpy as np

from urllib.parse import quote

"""
抓取比分
1.第一步抓取页面数据
2。解析 比例
3.解析主胜
4.解析客胜
5.存库


6.查询第一条和最后一条
7.显示在页面
8.计算结果
"""

"""
第二阶段：
抓取比分页面中的所有数据
根据公司，查询出数据
要展示的数据：比分、赔率
"""


def parse_bifen(game_id=729379):
    time.sleep(ConstantVal.TIMER_INTERVAL)
    startTime = time.time()
    bifen_url = "http://odds.500.com/fenxi/bifen-%s.shtml" % game_id
    bifen_html = cra_data.cra_data_url(bifen_url)
    # 只解析class 为pub_table的table 即可
    only_table = SoupStrainer("table", class_="pub_table")
    soup = BeautifulSoup(bifen_html, "lxml", parse_only=only_table)
    if not soup:
        print("%s 内容无效" % game_id)
        return
    # 获取比分,find搜索到一个就会停止搜索，搜索全部要使用 find_all
    scores_th = soup.find('tr').contents[5:]
    scores = [text.get_text() for text in scores_th if type(text) is bs4.element.Tag]

    # 0:0的位置
    dogfall_index = scores.index("0:0")
    # 所有赔率
    #  威廉希尔:293、Bwin:5、Bet365:3、Eurobet:15   1Bet:671、金宝博:348、澳门:11、18Bet：863
    # 用于排序 老的 ["威廉希尔", "Bet365", "Bwin", "澳门"] + ["Eurobet", "1Bet", "金宝博"]
    specify_cids = [293, 5, 3, 15]+[863, 348, 11]
    main_comp = ["威廉希尔", "Bwin", "Bet365", "Eurobet"] + ["18Bet", "金宝博", "澳门"]

    # 用于在网页上查找所有 有class属性的tr
    all_trs = soup.find_all("tr", {"class": re.compile(".*")})

    find_table_bifen_result = []
    main_win_data = []
    next_win_data = []
    col_pay_data = []
    for tr in all_trs:
        # 获取编号
        cid = parse_qs(urlparse(tr.a.get('href')).query)['cid']
        # 获取横着的整行数据
        temp_list = list(tr.stripped_strings)

        # 平局赔付
        avg_pay_list = temp_list[(dogfall_index + 2) * 2:]
        com_name = temp_list[1]
        order_num = [(main_comp.index(com_name) + 1) * 10 if com_name in main_comp else 100]
        # 主胜的赔率
        main_win_pay = [ps for ps in temp_list[2:(dogfall_index + 2) * 2][::2]]
        # 客胜的赔率
        next_win_pay = [ps for ps in temp_list[2:(dogfall_index + 2) * 2][1::2]]
        # 主胜
        temp_list_main = [game_id] + cid + temp_list[:2] + order_num + main_win_pay + avg_pay_list
        # 客胜
        temp_list_next = [game_id] + cid + temp_list[:2] + order_num + next_win_pay + avg_pay_list

        # 将客胜、平局、主胜的赔率存入数组
        col_pay_data.append(main_win_pay[1:] + avg_pay_list + next_win_pay[1:])

        main_win_data.append(temp_list_main)
        next_win_data.append(temp_list_next)
        #
        if com_name in com_name and cid and int(cid[0]) in specify_cids:
            find_table_bifen_result.append(temp_list_main)
            find_table_bifen_result.append(temp_list_next)

    # 比分存入数据库
    if find_table_bifen_result.__len__() > 0:
        result_count = DBUtils.executeMany(
            "insert into bifen_index(game_id,`cid`,`html_index`,`com_name`,order_num,win_type,`m1_0`,`m2_0`,`m2_1`"
            ",`m3_0`,`m3_1`,"
            "`m3_2`,`m4_0`,`m4_1`,`m4_2`,`m4_3`,`m0_0`,`m1_1`,`m2_2`,`m3_3`,`m4_4`) values (%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", find_table_bifen_result)
        print("%s bifen存库条数：%s 耗时：%s" % (game_id, result_count, utils.float_num(time.time() - startTime)))
    # 计算波胆的标准差，然后存入到标准差表
    if col_pay_data and len(col_pay_data) > 0:
        # 计算波胆平方差
        calc_bodan_std_result = bodan_std(col_pay_data)
        result = bifenImpl.insert_bodan_std([game_id] + calc_bodan_std_result)
        print("%s 保存波胆标准差数据条数：%s" % (game_id, result))


def calc_bodan(param):
    # sql 查询顺序
    score_arr = ["1-0", "2-0", "2-1", "3-0", "3-1", "3-2", "4-0", "4-1", "4-2", "4-3", "0-0", "1-1", "2-2", "3-3",
                 "4-4", "0-1", "0-2", "1-2", "0-3", "1-3", "2-3", "0-4", "1-4", "2-4", "3-4"]
    print("start calc bodan")

    # 获取比分的索引
    def cal_f(x):
        return [score_arr.index(sc) for sc in score_arr if x in sc]

    total_result = []
    for pp in param:
        per_score = []
        # 获取所有的比分赔率数据
        comp_data = [float(pp[key]) for key in list(pp.keys()) if key.startswith("m")]
        # AH13 计算返回率
        total_cal = 1 / sum([1 / cd for cd in comp_data])
        first_pay = []
        second_pay = []
        # 0 到 4 球就是5个，计算波胆
        for i in range(4 + 1):
            first_pay.append(sum([1 / comp_data[index] for index in cal_f(str(i) + '-')]) * total_cal)
            second_pay.append(sum([1 / comp_data[index] for index in cal_f('-' + str(i))]) * total_cal)
        # 主 计算3+ 的波胆
        first_pay.insert(3, 1 - first_pay[0] - first_pay[1] - first_pay[2])
        # 客 3+
        second_pay.insert(3, 1 - second_pay[0] - second_pay[1] - second_pay[2])

        per_score.append(pp['com_name'])
        # 放进数据 total_result
        first_pay = list(map(percent_util, first_pay))
        second_pay = list(map(percent_util, second_pay))
        # 取出最大的两个波胆，用于标色
        first_sorted = first_pay[:]
        first_sorted.sort(reverse=True)
        # 取出最大的两个波胆，用于标色
        second_sorted = second_pay[:]
        second_sorted.sort(reverse=True)
        # + [total_cal]
        per_score.append(first_pay)
        per_score.append(second_pay + [percent_util(total_cal)])
        per_score.append(first_sorted[:2])
        per_score.append(second_sorted[:2])

        total_result.append(per_score)
    return total_result


def bodan_std(next_bifen_result):
    """
    计算每个公司赔率的波胆 不同比分的平均数
    :param next_bifen_result: 即赔比分
    :return: 返回波胆平方差
    """
    # 当数组是无效的时候，直接返回
    if not next_bifen_result:
        return []
    bodan_arr = []
    for pp in next_bifen_result:
        # 获取所有的比分赔率数据
        comp_data = [float(val) for val in pp]
        # 计算返还率
        total_cal = 1 / sum([1 / cd for cd in comp_data])
        # 胜 平 负 比分求和 ，返还率除以和，存入数组
        bodan_arr.append([sum([1/p for p in comp_data[0:10]]) * total_cal, sum([1/p for p in comp_data[10:15]]) * total_cal,
                          sum([1/p for p in comp_data[15:25]]) * total_cal])
    # 将数据放进同一个数组
    zip_bodan = list(zip(*bodan_arr))
    # 计算平方差
    std_bodan = ['%.3f' % np.std(sd) for sd in zip_bodan]
    return std_bodan


def cra_bifen(game_id_arr):
    """
    通过比赛id，抓取比分
    :param game_id_arr: 比分数组
    :return: 暂无
    """
    if game_id_arr:
        for game_id in game_id_arr:
            parse_bifen(game_id["game_no"])


def percent_util(x, count=2):
    """
    :param x: 传进来的参数
    :param count: 保留的小数位数
    :return: 结果
    """
    ss = "%." + str(count) + "f"
    return float(ss % (x * 100))


def query_record(game_id=729379):
    result = bifenImpl.query_record2(game_id)
    if result is None:
        result = []
    p_result = process_game(result)
    result = [r for r in result if r['cid'] not in p_result]
    return result


def process_game(dict_arr, key="cid"):
    """
    筛选只出现了一次的记录
    :return:
    """
    from collections import Counter
    cids = [game[key] for game in dict_arr]
    dict_cid = Counter(cids).items()
    return [cid[0] for cid in dict_cid if cid[1] == 1]


def query_echart_data(game_id):
    """ 查询比分的echart 数据 """
    result = bifenImpl.query_echart_data(game_id)
    return result if result else []


def query_bodan_std(game_id):
    """
    查询波胆标准差
    :param game_id:
    :return:
    """
    result = bifenImpl.query_bodan_std(game_id)
    if result:
        return quote(str([list(bd) for bd in zip(*result)]))
    else:
        return []


if __name__ == "__main__":
    # elemNoList = DBUtils.execute("select DISTINCT game_no,start_datetime from football_game_info "
    #                              "where start_datetime>now() order by start_datetime ")
    # cra_bifen(elemNoList)
    # print(calc_bodan(bifenImpl.query_record(729379)))
    parse_bifen(784997)
    # rr = query_bodan_std(784485)
    # print(str(rr))
