import pymysql

from bid_tender.config.ah_cgw import *


def ah_cgw_detail_pipline(data):
    xzconn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset=MYSQL_CHATSET,
        port=MYSQL_PORT
    )
    cursor = xzconn.cursor()

    ins_sql = 'insert into ah_cgw(xmbh,title,pur_name,content,link,sorce_web,cgpmmc,ly,ywlx,xxlx,fbsj,xmsd,has_attach) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=values(title),pur_name=values(pur_name),content=values(content),link=values(link),sorce_web=values(sorce_web),cgpmmc=values(cgpmmc),ly=values(ly),ywlx=values(ywlx),xxlx=values(xxlx),fbsj=values(fbsj),xmsd=values(xmsd),has_attach=values(has_attach)'
    par = [data['xmbh'], data['title'], data['pur_name'], data['content'], data['link'], data['sorce_web'],data['cgpmmc'], data['ly'],
           data['ywlx'], data['xxlx'], data['fbsj'], data['xmsd'], data['has_attach']]
    try:
        xzconn.ping()
        cursor.execute(ins_sql, par)
        xzconn.commit()
        ins_sql = 'insert into ah_cgw_list(url) values (%s)'
        par = [data['link']]
        xzconn.ping()
        cursor.execute(ins_sql, par)
        xzconn.commit()
    except Exception as e:
        print('ah_cggg_detail_pipline:', e)
    sql = 'insert into ah_attachment_cgw(notice_id,fj_link,fj_location,fj_name) values (%s,%s,%s,%s)'
    for n in data['fj_list']:
        par = [n['notice_id'], n['fj_link'], n['fj_location'], n['fj_name']]
        try:
            xzconn.ping()
            cursor.execute(sql, par)
            xzconn.commit()
        except Exception as e:
            print(e)
    cursor.close()
    xzconn.close()
