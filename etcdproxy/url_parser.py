from urllib.parse import urlparse, parse_qsl
from typing import Dict, Union


def etcdurl_parser(url: str) -> Dict[str, Union[str, int, Dict[str, str]]]:
    """解析etcd路径

    Args:
        url (str): etcd的地址,注意请以`etcd://`开头

    Raises:
        AttributeError: schema 必须为etcd

    Returns:
        Dict[str, Union[str, int, Dict[str, str]]]: 初始化etcd客户端的参数数据
    """
    keys = ("timeout", "ca_cert", "cert_key", "cert_cert")
    intkeys = ("timeout",)
    result: Dict[str, Union[str, int, Dict[str, str]]] = {
        "host": '127.0.0.1',
        "port": 2379,
    }
    parse_result = urlparse(url)
    if parse_result.scheme.lower() != "etcd":
        raise AttributeError("schema 必须为etcd")
    if parse_result.username:
        result.update({"user": parse_result.username})
    if parse_result.password:
        result.update({"password": parse_result.password})
    if parse_result.port:
        result.update({"port": parse_result.port})
    if parse_result.hostname:
        result.update({"host": parse_result.hostname})
    if parse_result.query:
        sql_result = dict(parse_qsl(parse_result.query))
        grpc_options = {}
        for k, v in sql_result.items():
            if k in keys:
                if k in intkeys:
                    result.update({k: int(v)})
                else:
                    result.update({k: v})
            else:
                grpc_options.update({k: v})
        if grpc_options:
            result.update({"grpc_options": grpc_options})
    return result
