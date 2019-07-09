from football.crawler.utils.DBUtils import DBUtils


def query_pay_echart(dd, gameId):
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
        FROM pay_info where insert_datetime > %s and game_id=%s GROUP BY game_id,insert_datetime"""
    return DBUtils.executeOne(sql, (dd, gameId))
