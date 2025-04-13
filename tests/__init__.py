
def parse_query(query:str, params:dict)->str:
    for k,v in params.items():
        query = query.replace(f"%({k})s", f"'{v}'")
    
    return query
