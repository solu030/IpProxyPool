import pymysql,random
import config
def get_cur():
    db = pymysql.connect(host="localhost", port=3306, user=config.DB_USER, passwd=config.DB_PASSWORD, db="ip_pool")
    cur = db.cursor()
    return db,cur
def insert_ip(ip):
    db,cur = get_cur()
    def_score =config.DEFAULT_SCORE
    #没用orm，models里面的默认值不会生效,ip format后不带单引号sql会报错
    sql = "insert into app01_ipmodel(ip,score) values ('{ip}',{def_score})".format(ip=ip,def_score=def_score)
    try:
        cur.execute(sql)
        db.commit()
        print(ip + "添加成功!")
    except Exception as e:
        db.rollback()
        print(e)
        print(ip + "添加失败!")
    finally:
        db.close()
def add_score(ip):
    db,cur = get_cur()
    add_score = config.ADD_SCORE
    sql = " UPDATE app01_ipmodel SET score=score + {add_score} WHERE ip=%s".format(add_score=add_score)
    try:
        cur.execute(sql,ip)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
def dec_score(ip):
    db,cur = get_cur()
    dec_score = config.DECREASE_SCORE
    sql = " update app01_ipmodel set score=score - {dec_score} where ip=%s".format(dec_score=dec_score)
    try:
        cur.execute(sql,ip)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
def delete_ip(ip):
    db,cur = get_cur()
    sql = " DELETE FROM app01_ipmodel WHERE ip=%s"
    try:
        cur.execute(sql,ip)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
def delete_all():
    db,cur = get_cur()
    # sql = " DELETE FROM app01_ipmodel" #id不会重制
    sql = "TRUNCATE TABLE app01_ipmodel"
    try:
        cur.execute(sql)
        db.commit()
        print("ip表已清空!")
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
def ip_count():
    db,cur = get_cur()
    sql = "SELECT COUNT(*) FROM app01_ipmodel"
    try:
        cur.execute(sql)
        result = cur.fetchone()     #返回元组
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
        return result[0]
def get_score(ip):
    db,cur = get_cur()
    sql = "SELECT score FROM app01_ipmodel WHERE ip=%s"
    try:
        cur.execute(sql,ip)
        result = cur.fetchone()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
        try:
            r = result[0]
            return r
        except Exception as e:
            return False
def set_max(ip):
    db,cur = get_cur()
    score = config.MAX_SCORE
    sql = "update app01_ipmodel set score={score} where ip=%s".format(score=score)
    try:
        cur.execute(sql,ip)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()
def get_max_id():
    db,cur = get_cur()
    sql = "SELECT MAX(id) FROM app01_ipmodel"
    try:
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]
    except Exception as e:
        return False
def get_random():
    db,cur = get_cur()
    sql = "select ip from app01_ipmodel where id=%s"
    max_id = get_max_id()
    try:
        id = random.randint(1, max_id)
        cur.execute(sql,id)
        result = cur.fetchone()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
        try:
            r = result[0]
            return r
        except Exception as e:
            return False

if __name__ == '__main__':
    # insert_ip('192.168.127.15')
    # add_score('114.231.45.21:8888')
    # dec_score('114.231.45.21:8888')
    # delete_ip("192.168.127.12:5000")
    delete_all()
    # result = ip_count()[0]
    # result = get_score("192.168.127.10")
    # print(type(result))
    # result = get_random()
    # print(type(result))
