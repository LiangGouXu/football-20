import pymysql
import platform
# 连接mysql字符串
db = None
if platform.node() == "DESKTOP-MKICEMAN":
    db = pymysql.connect("localhost", "root", "liang", "football", port=3308, cursorclass=pymysql.cursors.DictCursor)
elif platform.node() == "DESKTOP-Liang":
    db = pymysql.connect("localhost", "root", "liang1111", "rangqiu", port=3306, cursorclass=pymysql.cursors.DictCursor)
elif platform.node() == 'DESKTOP-administator':
    db = pymysql.connect("localhost", "root", "jiang", "football", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
else:
    db = pymysql.connect("127.0.0.1", "root", "mysql", "football", port=3306, cursorclass=pymysql.cursors.DictCursor)


class DBUtils:

    @staticmethod
    def execute(sql, args=None, exe_type=None):
        db.cursorclass=pymysql.cursors.DictCursor
        if sql:
            sql = sql.lstrip()
            # 增删改 需要回滚
            if sql[:7].rstrip().lower() in ["insert", "update", "delete", "replace"]:
                try:
                    with db.cursor() as cursor:
                        # 执行sql
                        if exe_type and exe_type == "MANY":
                            exe_result = cursor.executemany(sql, args)
                        else:
                            exe_result = cursor.execute(sql, args)
                        db.commit()
                        cursor.close()
                        return exe_result
                except Exception as e:
                    # 发生异常 回滚
                    db.rollback()
                    # print(e)
            else:
                try:
                    # 查询，不用做回滚
                    with db.cursor() as cursor:
                        # 执行sql
                        cursor.execute(sql, args)
                        result_query = cursor.fetchall()
                        db.commit()
                        cursor.close()
                        return result_query
                except Exception as e:
                    # print(e)
                    print()

    @staticmethod
    def executeMany(sql, args):
        return DBUtils.execute(sql, args, "MANY")

    @staticmethod
    def executeOne(sql, args=None):
        return DBUtils.execute(sql, args, None)

    @staticmethod
    def queryNoDict(sql, args=None,):
        if sql:
            sql = sql.lstrip()
            try:
                db.cursorclass = pymysql.cursors.Cursor
                with db.cursor() as cursor:
                    # 执行sql
                    cursor.execute(sql, args)
                    result_query = cursor.fetchall()
                    db.commit()
                    cursor.close()
                    return result_query
            except Exception as e:
                # 发生异常 回滚
                db.rollback()
                print(e)


if __name__ == "__main__":
    result = DBUtils.queryNoDict("select * from test")
    print(list(result))
