
涉及到数据库的操作：

在数据库中：

    CREATE EXTENSION plpython3u;


联合检索：

    https://drr.ikcest.org/csw?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&DistributedSearch=1&hopCount=2


测试

    https://drr.ikcest.org/csw?service=CSW&version=3.0.0&request=GetCapabilities
    https://csw.deep-time.org/csw?service=CSW&version=3.0.0&request=GetCapabilities


查找数据:

    https://csw.deep-time.org/csw?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&outputFormat=application/json
    https://csw.deep-time.org/csw?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&outputFormat=application/json&DistributedSearch=1&hopCount=2
