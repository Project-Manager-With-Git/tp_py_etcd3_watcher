
from typing import  Dict, Union, Tuple
from pyproxypattern import Proxy
import etcd3
from .url_parser import etcdurl_parser


class EtcdSender(Proxy):
    @classmethod
    def create(clz, aio: bool = False, **configs: Dict[str, Union[str, int, Dict[str, str]]]) -> "EtcdSender":
        """初始化创建一个etcd的代理."""
        if aio:
            c = AioClient(**configs)
        else:
            c = Client(**configs)
            c = etcd = etcd3.client(host='etcd-host-01', port=2379)
        p = clz(c)
        return p

    @classmethod
    def create_from_url(clz, url: str, *, aio: bool = False, cert: Tuple = (), verify: bool = False) -> "EtcdSender":
        """初始化创建一个监听对象.
        参数参考<https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html>
        """
        configs = etcdurl_parser(url)
        if aio:
            c = AioClient(cert=cert, verify=verify, **configs)
        else:
            c = Client(cert=cert, verify=verify, **configs)
        p = clz(c)
        return p

    def _instance_check(self, instance: Any) -> bool:
        return isinstance(instance, (Client, AioClient))
