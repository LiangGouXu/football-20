# -*-coding:utf-8-*-
import requests
from ..craImpl import testData
from lxml import etree
from ..utils.DBUtils import DBUtils
import time


def cra_data_url(url, encoding="gb2312"):
    """
    :param url: 页面url
    :param encoding: 编码，默认gb2312
    抓取数据
    """
    session = requests.session()

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
    response = session.get(url, headers=headers)
    content = response.content.decode(encoding, errors="ignore")
    return content


"""
读取第一列、5列 存入数据库
进入子页面
读取数据
存入数据库
读取
"""

print("开始了_store_all")
total_num_list = []


# //tbody[@id="main-tbody"]//input[@type="checkbox"]/../text()
def cra_main_page():
    # 先用测试数据
    content = testData.str
    # print(soup.select("#main-tbody input[type='checkbox']"))
    selector = etree.HTML(content)

    # 编号
    elemtsNo = selector.xpath('//tbody[@id="main-tbody"]'
                              '//input[@type="checkbox"]/@value')
    global total_num_list
    total_num_list = elemtsNo
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
    exe_result = DBUtils.executeMany("replace into football_game_info values (%s, %s, %s, %s, %s)",
                                     zip(elemtsNo, elemts1, elemtsTime, elemtsTeam1, elemtsTeam2))
    print("result:" + str(exe_result))
    for el in zip(elemtsNo, elemts1, elemtsTime, elemtsTeam1, elemtsTeam2):
        print(el)


def analysis_all_sub_page(data, head_info='table[@id="datatb"]'):
    """
    子页面的解析
    :param data: 要解析的数据
    :param head_info: 类型
    :return:
    """
    # table[@id="datatb"]  tr
    selector = etree.HTML(data)

    elemOrderNums = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]/../text()')
    elemOrderNums = [idn.replace('\n', '').strip() for idn in elemOrderNums]

    # print(elemIds)
    # 赔率公司
    elemCompanyNames = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                         '/../../following-sibling::*[1]/@title')
    # print(elemCompanyNames)
    # 胜负平成绩
    elemsGrade = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                   '/../../following-sibling::*[3]//tr[2]/td/text()')
    elemsGrade = [elemsGrade[i:i + 3] for i in range(0, len(elemsGrade), 3)]

    # print(elemsGrade)
    # 网页上面的时间
    dataReleaseTimes = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                         '/../../../@data-time')

    # 即时凯利
    timeKely = selector.xpath('//' + head_info + '//input[@type="checkbox"][@id]'
                                                 '/../../following-sibling::*[6]//tr[2]/td/text()')

    timeKely = [timeKely[i:i + 3] for i in range(0, len(timeKely), 3)]
    # all_data['timeKely'] = timeKely
    # print(bb)
    # for val in bb:
    #     print(val)
    listGrade = list(zip(*elemsGrade))
    listKelly = list(zip(*timeKely))
    all_data = zip(elemOrderNums, elemCompanyNames, *listGrade, dataReleaseTimes, *listKelly)


    return all_data


def process_sub_page(elemNoList):
    """  解析让球指数页面 """
    for elNo in elemNoList:
        str_sql = "insert into pay_info(orderNum,pay_comp_name," \
                  "get_datetime,kelly_win_num,kelly_avg_num,kelly_lost_num,game_id) " \
                  "values(%s,%s,%s,%s,%s,%s," + str(elNo) + ") "
        url = "http://odds.500.com/fenxi/rangqiu-%s.shtml?lot=jczq" % elNo
        # 子页面第一页的数据
        result = analysis_all_sub_page(cra_data_url(url, "utf-8"), None)
        # 存库
        count = DBUtils.executeMany(str_sql, list(result))
        print("首页保存数量: %s" % count)

        # 子页面其他页的数据
        start = 30
        while True:
            url = "http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&" \
                  "start=%d&r=1&style=0&guojia=0&chupan=0&lot=all" % (elNo, start)
            start += 30
            htmlData = cra_data_url(url, "utf-8")
            if htmlData and len(htmlData.strip()) > 100:
                result = analysis_all_sub_page(htmlData, 'tr')
            count = DBUtils.executeMany(str_sql, result)
            print("分页start=%s保存数量: %s" % (start, count))
            # 存库

    # 解析之后，直接存库


if __name__ == "__main__":
    process_sub_page(["733460"])
   # start = 30
   # url = "http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&" \
   #       "start=%d&r=1&style=0&guojia=0&chupan=0&lot=all" % (735562, start)
   # htmlData = cra_data_url(url)
   # print(htmlData)
   #analysis_all_sub_page(testData.page_str, 'tr')

