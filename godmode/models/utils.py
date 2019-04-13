def model_hash(model, table_name=None):
    database = model.db.hash if model.db else model.__class__.__name__

    if not table_name:
        if hasattr(model.table, "__tablename__"):
            table_name = model.table.__tablename__
        elif hasattr(model.table, "__table__"):
            table_name = model.table.__table__.name
        else:
            table_name = model.__class__.__name__

    return "{database}_{table_name}".format(
        database=database,
        table_name=table_name
    )
