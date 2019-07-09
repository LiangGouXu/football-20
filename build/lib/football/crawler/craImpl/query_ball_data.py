from football.crawler.utils.DBUtils import DBUtils


def queryMatchCount():
    """
    查询所有日期
    :return:
    """
    return DBUtils.execute(
        "SELECT left(start_datetime,10) dd FROM football_game_info "
        "GROUP BY left(start_datetime,10) ORDER BY dd desc")
