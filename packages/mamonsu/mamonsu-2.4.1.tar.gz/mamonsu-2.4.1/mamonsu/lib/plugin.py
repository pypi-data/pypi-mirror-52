# -*- coding: utf-8 -*-

import time
import logging
import traceback
import sys
import json

from threading import Thread

from mamonsu.lib.const import Template


class PluginDisableException(Exception):
    pass


class Plugin(object):
    # can be 'mamonsu' or 'agent'
    # type depends on run command
    Type = 'mamonsu'

    # --plugin-type for zabbix-agent can be: all,postgres,sys
    AgentPluginType = 'all'

    # PG version
    VersionPG = {'type': 'PG_V', 'number': '10.0'}

    # Macros for run as agent type or as mamonsu
    Macros = {"mamonsu": "", "agent": "{$PG_CONNINFO},{$PG_PATH}"}

    # plugin interval run
    Interval = 60

    # plugin config
    DEFAULT_CONFIG = {}  # type: Dict[str, str]

    _thread = None  # type: Thread
    _sender = False
    _enabled = True

    # for all childs
    is_child = True

    # const
    PATH = "/etc/zabbix/zabbix_agent.d/scripts"
    DELTA = Template.DELTA
    GRAPH_TYPE = Template.GRAPH_TYPE
    VALUE_TYPE = Template.VALUE_TYPE
    UNITS = Template.UNITS

    DELTA_SPEED = Template.DELTA.speed_per_second
    DELTA_CHANGE = Template.DELTA.simple_change

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(
            self.__class__.__name__.upper())
        self.sender = None
        self.last_error_text = ''

        # from config => _plugin_config
        self._plugin_config = {}
        name = self.__class__.__name__.lower()
        if self.config.has_plugin_config(name):
            for x in self.config.plugin_options(name):
                self._plugin_config[x] = self.config.fetch(name, x)

    @classmethod
    def only_child_subclasses(self):
        plugins = []
        for klass in self.__subclasses__():
            if klass.is_child:
                plugins.append(klass)
            plugins.extend(klass.only_child_subclasses())
        return plugins

    @classmethod
    def set_default_config(cls, config, interval):
        name = cls.__name__.lower()
        # if section already loaded via config file
        # if not config.has_section(name) and len(cls.DEFAULT_CONFIG) > 0:
        if not config.has_section(name):
            config.add_section(name)
        for x in cls.DEFAULT_CONFIG:
            if config.has_option(name, x):
                continue
            value = cls.DEFAULT_CONFIG[x]
            if not isinstance(value, str):
                sys.stderr.write(
                    'Config value {0} in section {1} must'
                    ' be string! Fix plugin please.\n'.format(x, name))
            config.set(name, x, '{0}'.format(cls.DEFAULT_CONFIG[x]))
        if not config.has_option(name, 'interval') and interval is not None:
            config.set(name, 'interval', '{0}'.format(interval))

    # get value from config
    def plugin_config(self, name, as_json=False):
        if name not in self._plugin_config:
            return None
        if as_json:
            return json.loads(self._plugin_config[name])
        else:
            return self._plugin_config[name]

    def start(self):
        self._thread = Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
        self.log.info('started ...')

    def is_alive(self):
        if self._thread is not None:
            return self._thread.is_alive()
        return False

    def run(self, sender):
        return None

    def is_sender(self):
        return self._sender

    def is_enabled(self):
        if self.plugin_config('enabled') == 'False':
            return False
        return self._enabled

    def disable(self):
        self._enabled = False

    def set_sender(self, sender):
        self.sender = sender

    def items(self, template):
        return None

    def graphs(self, template):
        return None

    def triggers(self, template):
        return None

    def discovery_rules(self, template):
        return None

    def keys_and_queries(self, template_zabbix):
        return None

    def _log_exception(self, e, trace):
        self.last_error_text = 'catch error: {0}'.format(e)
        self.log.error(self.last_error_text)
        self.log.info('hint: enable debug level to full exception trace')
        self.log.debug(trace)

    def _loop(self):
        while (True):
            last_start = time.time()
            try:
                self.run(self.sender)
            except PluginDisableException as e:
                text = 'disable plugin: {0}.'.format(e)
                self.log.info(text)
                return
            except Exception as e:
                trace = traceback.format_exc()
                self._log_exception(e, trace)
                return
            # time interval btw sending metrics
            sleep_time = int(self.plugin_config('interval')) - int(time.time() - last_start)
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                self.log.error(
                    'Timeout: {0}s'.format(int(time.time() - last_start)))
                return

    # convert zabbix key to right type: zabbix-trapper or zabbix-agent
    def right_type(self, key, var="", var_discovery=""):
        if self.Type == "mamonsu":
            if len(var_discovery) == 0:
                new_key = key.format('[{0}]'.format(var))
            else:
                new_key = key.format('[{0}{1}]'.format(var, var_discovery[:-1]))
        else:
            if self.AgentPluginType == 'sys':
                if var_discovery != "":
                    if var == "":
                        new_key = key.format('{0}[{1}]'.format(var, var_discovery))
                    else:
                        new_key = key.format('.{0}[{1}]'.format(var, var_discovery))
                else:
                    if var != "":
                        new_key = key.format('.{0}'.format(var))
                    else:
                        new_key = key.format('')
            else:
                if var == "":
                    new_key = key.format('{0}[{1}]'.format(var, var_discovery + self.Macros[self.Type]))
                else:
                    new_key = key.format('.{0}[{1}]'.format(var, var_discovery + self.Macros[self.Type]))
        return new_key
