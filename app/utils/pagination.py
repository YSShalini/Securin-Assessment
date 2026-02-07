def paginate(query, page: int, page_size: int):
    if page < 1:
        page = 1

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)
