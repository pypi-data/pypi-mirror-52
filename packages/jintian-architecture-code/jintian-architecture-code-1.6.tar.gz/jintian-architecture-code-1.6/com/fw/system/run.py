import importlib
import os
import multiprocessing
from com.fw.system.red_conf import system_conf

import falcon

from com.fw.base.base_log import logger
from com.fw.db.mongo_db import mongo_dao
from com.fw.db.mysql_db import mysql_dao
from com.fw.db.redis_db import redis_db
from com.fw.system.falcon_filter import falconFilter
from com.fw.system.socket_server_asgi import socket
from com.fw.system.task import task
from com.fw.utils.json_serializer import JsonSerializerutils
from com.fw.utils.time_utils import TimeUtils, DateType


class System(object):
    def __init__(self):
        self.mysql_dao = mysql_dao
        self.mongo_dao = mongo_dao
        self.work_dir = os.getcwd()
        self.task = task
        self.redis_db = redis_db
        self.socket = socket
        self.app = falcon.API(middleware=falconFilter)

        try:
            self.ip = system_conf.get_value('environment', "ip")
        except Exception as e:
            raise BaseException("no apidoc ip", e)

        if ("com" in self.work_dir):
            self.work_dir = self.work_dir[:self.work_dir.index("com") - 1]

    def create_apidoc_json(self):
        with open(os.path.join(self.work_dir, "apidoc.json"), 'w') as f:
            f.write(
                '{"name": "嗡润科技Api平台","version": "0.0.1","description": "支付-后台API","url": "http://' + self.ip + ':8000","sampleUrl": "http://' + self.ip + ':8000", "apidoc": {"title": "支付-后台API"}}')

        result = os.popen("apidoc -i " + self.work_dir + "  -o static/apidoc/")
        logger.warn(result._stream.read())

    def startSocket(self):

        self.socket.run(self.work_dir)

    def run(self, after=None):

        self.create_apidoc_json()

        # 设置这个参数才能接受post参数
        self.app.req_options.auto_parse_form_urlencoded = True

        route_files = self.__find_route(self.work_dir)

        for file_path in route_files:

            route = importlib.import_module(file_path)

            if not route.route:
                logger.error("ERROR {} : NO ROUTE  ......".format(file_path))
                continue

            route_ex = route.route

            if not route_ex.path:
                logger.error("ERROR {} : ROUTE NO PATH ......".format(file_path))
                continue

            for suffix in route_ex.suffix:
                params = {"suffix": suffix}
                try:
                    self.app.add_route(route_ex.path + "/" + suffix, route_ex, **params)
                except Exception as e:
                    raise BaseException("未找到该路由:{}".format(route_ex.path + "/" + suffix), e)

        print("       00000000       0      0        ")
        print("       0      0       0    0          ")
        print("       0      0       0  0            ")
        print("       0      0       00              ")
        print("       0      0       0  0            ")
        print("       0      0       0    0          ")
        print("       00000000       0       0       ")

        task.add_task_time(self.startSocket,run_date=TimeUtils.add_date_time(2, DateType.SECONDS))

        # httpd = simple_server.make_server("0.0.0.0", 8000, app)
        #         # logger.info("------ http server 启动成功 ----- ")
        #         # httpd.serve_forever()

        result = os.popen("gunicorn -b 0.0.0.0:8000 --workers={} --threads=2 com.fw.system.run:app".format(multiprocessing.cpu_count()))
        logger.info("------ http server 启动成功:{} ----- ".format(result._stream.read()))

    def __find_route(self, work_dir, result=[]):

        if not work_dir:
            work_dir = self.work_dir

        files = os.listdir(work_dir)

        for file in files:
            if file.startswith("_"):
                continue

            item_path = os.path.join(work_dir, file)

            if os.path.isdir(item_path):
                self.__find_route(item_path, result)
            elif os.path.isfile(item_path):
                if file.endswith('_route.py') and file != "base_route.py":
                    result.append(item_path[item_path.index("com"):-3].replace("/", "."))
        return result


system = System()

app = system.app
