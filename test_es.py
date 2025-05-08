from elasticsearch import Elasticsearch

try:
    # 连接配置（适配 Elasticsearch 8.x）
    es = Elasticsearch(
        hosts=["http://localhost:9200"],
        request_timeout=30,
        verify_certs=False,  # 如果使用 HTTPS 但不想验证证书
        headers={"Accept": "application/json", "Content-Type": "application/json"}  # 明确指定 headers
    )

    # 测试连接
    if not es.ping():
        raise ConnectionError("无法连接到 Elasticsearch")

    # 测试索引名称
    test_index = "test-index-python"

    # 测试文档数据
    doc = {
        "title": "Python 测试文档",
        "content": "这是通过 Python elasticsearch 库创建的测试文档",
        "timestamp": "2023-10-01"
    }

    # 索引文档（注意：8.x 使用 'document' 而不是 'body'）
    response = es.index(
        index=test_index,
        document=doc,
        id=1  # 可选：指定文档 ID
    )
    print(f"\n索引文档结果：{response['result']} (ID: {response['_id']})")

    # 刷新索引使文档可搜索
    es.indices.refresh(index=test_index)

    # 查询该索引的所有文档
    search_result = es.search(
        index=test_index,
        query={"match_all": {}}  # 8.x 使用 'query' 而不是 'body'
    )
    print("\n查询结果：")
    for hit in search_result['hits']['hits']:
        print(f"ID: {hit['_id']}, 内容: {hit['_source']}")

    # 获取所有用户索引（排除系统索引）
    indices = es.cat.indices(format="json", h="index,docs.count")
    print("\n系统中的用户索引：")
    for index in indices:
        if not index['index'].startswith('.'):
            print(f"索引名：{index['index']}, 文档数：{index['docs.count']}")

except Exception as e:
    print(f"\n操作失败：{type(e).__name__}: {str(e)}")