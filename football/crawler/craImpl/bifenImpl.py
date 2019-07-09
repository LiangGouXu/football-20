from football.crawler.utils.DBUtils import DBUtils
import time


def query_record(game_id=729379):
    # 查询主胜 客胜,主胜 拼接 客胜
    return DBUtils.execute("""
     SELECT *,substr(insert_datetime,6,11) as dd from (
         SELECT  cid, concat(com_name,'即赔') as com_name,insert_datetime ,`m1_0`,  `m2_0`,  `m2_1`, 
        `m3_0`,  `m3_1`,  `m3_2`,  `m4_0`,  `m4_1`,  `m4_2`,  `m4_3`,  `m0_0`,  `m1_1`,  `m2_2`,  `m3_3`,  `m4_4`
        ,order_num ,next.* 
        FROM bifen_index as main ,(
				SELECT  cid as nid,`m1_0` as m0_1,  `m2_0` as m0_2,  `m2_1` as m1_2,  `m3_0` as m0_3,  `m3_1` as m1_3,
				`m3_2`as m2_3,  `m4_0` as m0_4,  `m4_1` as m1_4,  `m4_2` as m2_4,  `m4_3` as m3_4 FROM bifen_index
        WHERE game_id=%(game_id)s AND win_type='客胜' and insert_datetime =
				(select max(insert_datetime) FROM bifen_index WHERE game_id=%(game_id)s)
        ) as next
                WHERE game_id=%(game_id)s AND win_type='主胜' and main.cid=next.nid and insert_datetime =
                        (select max(insert_datetime) FROM bifen_index WHERE game_id=%(game_id)s)
        union all
        SELECT  cid,concat(com_name,'初赔') as com_name,insert_datetime ,`m1_0`,  `m2_0`,  `m2_1`,  
                `m3_0`,  `m3_1`,  `m3_2`,  `m4_0`,  `m4_1`,  `m4_2`,  `m4_3`,  `m0_0`,  `m1_1`,  `m2_2`,  `m3_3`,
                `m4_4`,order_num, next.* FROM bifen_index as main ,(
                        SELECT  cid as nid,`m1_0` as m0_1,  `m2_0` as m0_2,  `m2_1` as m1_2,  `m3_0` as m0_3,
                        `m3_1` as m1_3,  `m3_2`as m2_3,  `m4_0` as m0_4,  `m4_1` as m1_4,  `m4_2` as m2_4, 
                        `m4_3` as m3_4 FROM bifen_index
                WHERE game_id=%(game_id)s AND win_type='客胜' and insert_datetime =
                        (select min(insert_datetime) FROM bifen_index WHERE game_id=%(game_id)s)
        ) as next
                WHERE game_id=%(game_id)s AND win_type='主胜' and main.cid=next.nid and insert_datetime =
                        (select min(insert_datetime) FROM bifen_index WHERE game_id=%(game_id)s)
              ) as all_data ORDER BY order_num,insert_datetime
    """, {"game_id": game_id})


def query_record2(game_id=729379):
    cids = query_had_comps(game_id)
    sql = ""
    for i in range(cids.__len__()):
        sql += """
        select * from (
SELECT  cid, concat(com_name,'初赔') as com_name,insert_datetime ,`m1_0`,  `m2_0`,  `m2_1`, 
        `m3_0`,  `m3_1`,  `m3_2`,  `m4_0`,  `m4_1`,  `m4_2`,  `m4_3`,  `m0_0`,  `m1_1`,  `m2_2`,  `m3_3`,  `m4_4`
        ,order_num ,next.* 
        FROM bifen_index as main ,(
      SELECT cid as nid,`m1_0` as m0_1,`m2_0` as m0_2,`m2_1` as m1_2,`m3_0` as m0_3, `m3_1` as m1_3,
      `m3_2`as m2_3,  `m4_0` as m0_4,  `m4_1` as m1_4,  `m4_2` as m2_4,  `m4_3` as m3_4 FROM bifen_index
        WHERE game_id={game_id} and cid ={cid} AND win_type='客胜'  order by insert_datetime limit 1
        ) as next
                WHERE game_id={game_id} and main.cid={cid} AND win_type='主胜'  order by insert_datetime limit 1) as a1
        union all
select * from (
SELECT  cid, concat(com_name,'即赔') as com_name,insert_datetime ,`m1_0`,  `m2_0`,  `m2_1`, 
        `m3_0`,  `m3_1`,  `m3_2`,  `m4_0`,  `m4_1`,  `m4_2`,  `m4_3`,  `m0_0`,  `m1_1`,  `m2_2`,  `m3_3`,  `m4_4`
        ,order_num ,next.* 
        FROM bifen_index as main ,(
            SELECT  cid as nid,`m1_0` as m0_1,  `m2_0` as m0_2,  `m2_1` as m1_2,  `m3_0` as m0_3,  `m3_1` as m1_3,
            `m3_2`as m2_3,  `m4_0` as m0_4,  `m4_1` as m1_4,  `m4_2` as m2_4,  `m4_3` as m3_4 FROM bifen_index
        WHERE game_id={game_id} and cid ={cid}  AND win_type='客胜' order by insert_datetime desc limit 1
        ) as next
                WHERE game_id={game_id} and main.cid={cid} AND win_type='主胜'  order by insert_datetime desc limit 1) as a1
        """.format(game_id=game_id, cid=cids[i]['cid'])
        if i != cids.__len__() - 1:
            sql += " UNION ALL "
    return DBUtils.execute(sql)


def query_had_comps(game_id):
    """
    查询已经抓取的公司
    :return:
    """
    return DBUtils.execute("SELECT cid,order_num FROM `bifen_index` WHERE game_id=%(game_id)s "
                           "GROUP BY cid,order_num ORDER BY order_num"
                           , {"game_id": game_id})


def insert_std_data(std_data):
    """ 保存比分的标准差 """
    return DBUtils.executeMany("INSERT INTO bifen_index_std(win_type,m1_0,m2_0,m2_1,m3_0,m3_1,m3_2"
                               ",m4_0,m4_1,m4_2,m4_3,m0_0,m1_1,m2_2,m3_3,m4_4,"
                               "game_id)VALUES(" + "%s," * 16 + "%s" + ") ", std_data)


def query_echart_data(game_id):
    """ 查询比分的echart 数据 """
    return DBUtils.execute("select * from bifen_index_std where game_id=%s and win_type = 'main'"
                              " union all "
                              "select * from bifen_index_std where game_id=%s and win_type = 'next'",
                              (game_id, game_id))


def insert_bodan_std(bodan_std):
    """
    插入波胆标准差
    :param bodan_std:
    :return: 插入条数
    """
    return DBUtils.executeOne("INSERT INTO bifen_bodan_std(game_id,win_bodan_std,dogfall_bodan_std"
                           ",lose_bodan_std) values (%s,%s,%s,%s)", bodan_std)


def query_bodan_std(game_id):
    """
    查询波胆平方差
    :param game_id:
    :return:
    """
    return DBUtils.queryNoDict("select win_bodan_std, dogfall_bodan_std, lose_bodan_std, "
                               " substr(insert_datetime,6,11) as insert_datetime "
                               "from bifen_bodan_std where game_id=%s", game_id)


if __name__ == "__main__":
    # print(query_record_id(730592))
    startTime = time.time()
    for i in range(10):
        query_record2(730592)
    print(time.time() -startTime)
