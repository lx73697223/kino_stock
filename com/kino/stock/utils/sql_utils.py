

def get_range_where_sql(start, end, column_name):
    return where_sql_joiner(range_where(start, end, column_name))


def where_sql_joiner(sql_wheres):
    if sql_wheres:
        return "WHERE %s" % " AND ".join(sql_wheres)
    return ""


def range_where(start, end, column_name):
    _where = []
    if start is not None:
        _where.append("{} >= '{}'".format(column_name, start))
    if end is not None:
        _where.append("{} <= '{}'".format(column_name, end))
    return _where
