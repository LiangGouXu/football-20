from football.crawler.craImpl import cra_data
from football.crawler.craImpl import oupeiInfoImpl
from football.crawler.utils.DBUtils import DBUtils

def cra_sub_oupei(elem_no_list):

    cra_data.process_sub_page(testElemNo=elem_no_list, first_tmp_url="http://odds.500.com/fenxi/ouzhi-%s.shtml",
                              next_tmp_url="http://odds.500.com/fenxi1/ouzhi.php?id=%s&ctype=1&start=%s"
                                           "&r=1&style=0&guojia=0&chupan=1", table_name="oupei_info")


def query_oupei_echart(dd, gameId):
    result = oupeiInfoImpl.query_oupei_echart(dd, gameId)
    if result is None:
        result = []
    return result


def query_oupei_echart2(gameId):
    result = oupeiInfoImpl.query_oupei_echart2(gameId)
    if result is None:
        result = []
    return result


def query_jishioupei_echart2(gameId):
    result = oupeiInfoImpl.query_jishioupei_echart2(gameId)
    if result is None:
        result = []
    return result

def query_oupei_gameId():
    """获取game_id列表"""
    sql="""select game_id from oupei_startvalue_info"""
    game_id=DBUtils.executeOne(sql)
    gameId_list=[]
    for gameId in game_id:
        gameId_id=gameId["game_id"]
        gameId_list.append(gameId_id)
    # print(gameId_list)
    return set(gameId_list)


#######################

def query_oupei_echart3(gameId):
    result = oupeiInfoImpl.query_oupei_echart3(gameId)
    if result is None:
        result = []
    return result


def query_jishioupei_echart3(gameId):
    result = oupeiInfoImpl.query_jishioupei_echart3(gameId)
    if result is None:
        result = []
    return result


def cra_chupei_oupei(elem_no_list):
    cra_data.process_sub_page2(testElemNo=elem_no_list, first_tmp_url="http://odds.500.com/fenxi/ouzhi-%s.shtml",
                              next_tmp_url="http://odds.500.com/fenxi1/ouzhi.php?id=%s&ctype=1&start=%s"
                                           "&r=1&style=0&guojia=0&chupan=1", table_name="oupei_startvalue_info")


def cra_rangqiu_oupei(elem_no_list):        #http://odds.500.com/fenxi1/rangqiu.php?id=768573&ctype=1&start=30&r=1&style=0&guojia=0&chupan=1&lot=all
    cra_data.process_sub_page3(testElemNo=elem_no_list, first_tmp_url="http://odds.500.com/fenxi/rangqiu-%s.shtml?lot=jczq",
                              next_tmp_url="http://odds.500.com/fenxi1/rangqiu.php?id=%s&ctype=1&start=%s"
                                           "&r=1&style=0&guojia=0&chupan=1&lot=jczq", table_name="rangqiu_startvalue_info")


if __name__ == "__main__":
    print(123)
    # cra_sub_oupei([{"game_no": 773174}])
    # data=query_jishioupei_echart2('768585')
    # print(data)
    # data=cra_rangqiu_oupei([{"game_no": 788682}])
    # data=cra_chupei_oupei([{"game_no": 788682,"haha":777},{"game_no": 788682,"haha":796360}])
    # print(data)
    data=query_oupei_gameId()
    print(data)
    # print(data[5]["game_id"])