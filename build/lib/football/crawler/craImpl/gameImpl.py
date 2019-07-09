from football.crawler.utils.DBUtils import DBUtils
from datetime import datetime, timedelta


def query_game_info_day(query_date, query_type="DAY_NEXT"):
    # 查询某一天之后的数据
    if query_type == 'DAY_NEXT':
        result = DBUtils.executeOne("SELECT * FROM football_game_info where start_datetime > %s "
                                    "order by start_datetime", query_date)
    else:
        # 查询某一天的数据
        result = DBUtils.executeOne("SELECT * FROM football_game_info where start_datetime like %s "
                                    "order by start_datetime", query_date + '%')
    if result is None:
        result = []
    return result


def query_game_dates(before_days=12):
    """ 查询12天之后的日期 """
    dd = (datetime.today() + timedelta(days=-before_days)).strftime('%Y-%m-%d')
    all_date = DBUtils.executeOne("SELECT substr(start_datetime,1,10) as start_datetime FROM football_game_info where"
                                  " start_datetime>%s group by substr(start_datetime,1,10) "
                                  "order by substr(start_datetime,1,10) desc", dd)
    if all_date is None:
        all_date = []
    return all_date
