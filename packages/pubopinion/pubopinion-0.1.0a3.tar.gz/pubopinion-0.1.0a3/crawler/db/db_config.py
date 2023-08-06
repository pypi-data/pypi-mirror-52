
# 启用的数据库配置
ENABLED_DB = "test00"
# ENABLED_DB = "localhost"
# ENABLED_DB = "remote_dev"


# 数据库的详细配置
DB_CONFIG = [
    {
        "name": "localhost",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "public_opinion",
        "pool_size": 5,
    },
    {
        "name": "product",
        "hostname": "",
        "username": "",
        "password": "",
        "database": "",
    },
    {
        "name": "remote_dev",
        "hostname": "swc.ddns.net",
        "username": "root",
        "password": "1234",
        "database": "",
        "pool_size": 5
    },
    {
        "name": "test",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "public_opinion_test",
        "pool_size": 5
    },
    {
        "name": "crawler",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "",
        "pool_size": 5
    },
    {
        "name": "target",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "",
        "pool_size": 5
    },
    {
        "name": "test00",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "test00",
        "pool_size": 5
    }
]
