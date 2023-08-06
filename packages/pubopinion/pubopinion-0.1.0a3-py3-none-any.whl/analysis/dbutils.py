from crawler.db.db import get_connection

table_article = "cadrem_pubopinion_article"
table_comment = "cadrem_pubopinion_comment"


def select(table, offset=0, limit=100):
    """
    从表中选择limit条数据直到遍历结束
    :param table:
    :param offset:
    :param limit:
    :return: A tuple of tuples of rows
    """
    sql = " SELECT * FROM `%s` " % table
    sql += " LIMIT %(offset)s, %(limit)s "
    conn = get_connection()
    cursor = conn.cursor()
    is_remaining = True
    while is_remaining:
        params = {
            "offset": offset,
            "limit": limit,
        }
        cursor.execute(sql, params)
        sets = cursor.fetchall()
        if len(sets) > 0:
            offset += limit
            yield sets
        else:
            is_remaining = False
    conn.close()


def insert(table, fields, *rows):
    try:
        sql = "INSERT INTO `%(table)s`(%(fields)s)" \
              % {"table": table, "fields": ", ".join(["`"+field+"`" for field in fields])}
        # sql += ", ".join(["("+(", ".join(row))+")" for row in rows])
        conn = get_connection()
        cursor = conn.cursor()
        result = cursor.execute(sql, rows)
        cursor.close()
        conn.commit()
    finally:
        if conn:
            conn.close()
    return result


def update_sentiment_by_id(id, sentiment):
    sql = " UPDATE `%s` SET " % table_article
    sql += " sentiment=%s WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute(sql, [sentiment, id])
    cursor.close()
    conn.commit()
    conn.close()
    return result


def update_by_id(*rows):
    """
    Update rows by id
    :param rows: A list of mapping that must has key named "id"
    :return:
    """
    if len(rows) < 1:
        return 0
    sql = " UPDATE `%s` SET " % table_article
    conn = get_connection()
    cursor = conn.cursor()
    sql += ", ".join(
        ["`"+field+"`=%("+field+")s" for row in rows for field in row.keys() if field != "id"]
    )
    sql += " WHERE id=%(id)s"
    result = cursor.executemany(sql, rows)
    cursor.close()
    conn.commit()
    conn.close()
    return result


def select_not_topic(table=table_article, batch=100):
    for rows in select(table, offset=0, limit=batch):
        selected = []
        for row in rows:
            if row[2] == "" or row[2] is None:
                selected.append(row)
        yield selected
    # yield [row for rows in select(table, offset=0, limit=batch) for row in rows if row[2] == "" or row[2] is None]


def select_not_sentiment(table=table_article, batch=100):
    for rows in select(table, offset=0, limit=batch):
        selected = []
        for row in rows:
            if row[9] == "" or row[9] is None:
                selected.append(row)
        yield selected
    # yield [row for rows in select(table, offset=0, limit=batch) for row in rows if row[9] == "" or row[9] is None]


if __name__ == '__main__':
    # result = update_sentiment_by_id("20190912V0GYF2", 0)
    # print(result)
    # rows = [
    #     {"id": "20190912V0GYF2", "sentiment": 1},
    #     {"id": "20190912V0GYF2", "sentiment": 2},
    #     {"id": "20190912V0GYF2", "sentiment": 3},
    #     {"id": "20190912V0GYF2", "sentiment": 4},
    # ]
    # result = update_by_id(rows)
    # print(result)
    for rows in select_not_topic():
        print(rows)
    for rows in select_not_sentiment():
        print(len(rows))