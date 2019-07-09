from football.crawler.utils.DBUtils import DBUtils


def query_oupei_echart(dd, gameId):
    """
    查询指定日期到现在的数据库
    :param dd: 日期
    :param gameId: 比赛编号
    :return: 结果
    """
    sql = """select game_id,
                GROUP_CONCAT( eu_win_num SEPARATOR ',' ) AS eu_win_num,
                GROUP_CONCAT( eu_avg_num SEPARATOR ',' ) AS eu_avg_num,
                GROUP_CONCAT( eu_lost_num SEPARATOR ',' ) AS eu_lost_num,
                GROUP_CONCAT( kelly_win_num SEPARATOR ',' ) AS kelly_win_num,
                GROUP_CONCAT( kelly_avg_num SEPARATOR ',' ) AS kelly_avg_num,
                GROUP_CONCAT( kelly_lost_num SEPARATOR ',' ) AS kelly_lost_num,
                insert_datetime
        FROM oupei_info where insert_datetime > %s and game_id=%s GROUP BY game_id,insert_datetime"""
    return DBUtils.executeOne(sql, (dd, gameId))


def query_oupei_echart2(gameId):
    """
    查询对应比赛的初始凯利值
    :param gameId: 比赛编号
    :return:
    """
    sql="""select kelly_win_num,kelly_avg_num,kelly_lost_num from oupei_startvalue_info 
    where game_id=%s and insert_datetime=(select max(insert_datetime) from oupei_startvalue_info where game_id=%s)"""
    #select * from oupei_startvalue_info where game_id='807259' and insert_datetime=(select max(insert_datetime) from oupei_startvalue_info where game_id='807259');
    try:
        return DBUtils.executeOne(sql, (gameId,gameId))
    except Exception as e:
        return None


def query_jishioupei_echart2(gameId):
    """
    :param gameId:
    :return: 返回即时欧赔凯里
    """
    sql="""select kelly_win_num,kelly_avg_num,kelly_lost_num from oupei_info 
    where game_id=%s and insert_datetime=(select max(insert_datetime) from oupei_info where game_id=%s)"""
    return DBUtils.executeOne(sql, (gameId, gameId))


def query_oupei_echart3(gameId):
    """
    查询对应比赛的初始凯利值
    :param gameId: 比赛编号
    :return:
    """
    sql = """select kelly_win_num,kelly_avg_num,kelly_lost_num from rangqiu_startvalue_info 
        where game_id=%s and insert_datetime=(select max(insert_datetime) from rangqiu_startvalue_info where game_id=%s)"""
    return DBUtils.executeOne(sql,(gameId,gameId))


def query_jishioupei_echart3(gameId):
    """
    :param gameId:
    :return: 返回即时让球欧赔凯里
    """
    sql = """select kelly_win_num,kelly_avg_num,kelly_lost_num from pay_info 
        where game_id=%s and insert_datetime=(select max(insert_datetime) from pay_info where game_id=%s)"""
    return DBUtils.executeOne(sql,(gameId,gameId))



if __name__ == '__main__':
    print()
    print(query_oupei_echart2(gameId='807259'))
    #select kelly_win_num,kelly_avg_num,kelly_lost_num,jishi_kelly_win_num,jishi_kelly_avg_num,jishi_kelly_lost_num from oupei_startvalue_info  where game_id='807259' and insert_datetime=(select max(insert_datetime) from oupei_startvalue_info where game_id='807259');