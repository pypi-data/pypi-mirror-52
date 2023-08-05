# -*- coding: utf-8 -*-

from mamonsu.plugins.pgsql.plugin import PgsqlPlugin as Plugin
from .pool import Pooler


class Instance(Plugin):
    query_agent = "select sum({0}) as {0} from pg_catalog.pg_stat_database;"
    key = 'pgsql.'
    AgentPluginType = 'pg'
    Items = [
        # key, zbx_key, description,
        #    ('graph name', color, side), units, delta

        ('xact_commit', 'transactions[total]', 'transactions: total',
            ('PostgreSQL instance: rate', '0000CC', 1),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('blks_hit', 'blocks[hit]', 'blocks: hit',
            ('PostgreSQL instance: rate', '00CC00', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('blks_read', 'blocks[read]', 'blocks: read',
            ('PostgreSQL instance: rate', 'CC0000', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),

        ('conflicts', 'events[conflicts]', 'event: conflicts',
            ('PostgreSQL instance: events', '0000CC', 0),
            Plugin.UNITS.none, Plugin.DELTA.simple_change),
        ('deadlocks', 'events[deadlocks]', 'event: deadlocks',
            ('PostgreSQL instance: events', '000000', 0),
            Plugin.UNITS.none, Plugin.DELTA.simple_change),
        ('xact_rollback', 'events[xact_rollback]', 'event: rollbacks',
            ('PostgreSQL instance: events', 'CC0000', 0),
            Plugin.UNITS.none, Plugin.DELTA.simple_change),

        ('temp_bytes', 'temp[bytes]', 'temp: bytes written',
            ('PostgreSQL instance: temp files', 'CC0000', 0),
            Plugin.UNITS.bytes, Plugin.DELTA.simple_change),
        ('temp_files', 'temp[files]', 'temp: files created',
            ('PostgreSQL instance: temp files', '0000CC', 1),
            Plugin.UNITS.none, Plugin.DELTA.simple_change),

        # stacked
        ('tup_deleted', 'tuples[deleted]', 'tuples: deleted',
            ('PostgreSQL instance: tuples', '000000', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('tup_fetched', 'tuples[fetched]', 'tuples: fetched',
            ('PostgreSQL instance: tuples', '0000CC', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('tup_inserted', 'tuples[inserted]', 'tuples: inserted',
            ('PostgreSQL instance: tuples', '00CC00', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('tup_returned', 'tuples[returned]', 'tuples: returned',
            ('PostgreSQL instance: tuples', 'CC00CC', 1),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
        ('tup_updated', 'tuples[updated]', 'tuples: updated',
            ('PostgreSQL instance: tuples', 'CC0000', 0),
            Plugin.UNITS.none, Plugin.DELTA.speed_per_second),
    ]

    def run(self, zbx):
        params = ['sum({0}) as {0}'.format(x[0]) for x in self.Items]
        result = Pooler.query('select {0} from \
            pg_catalog.pg_stat_database'.format(
            ', '.join(params)))
        for idx, val in enumerate(result[0]):
            key, val = 'pgsql.{0}'.format(
                self.Items[idx][1]), int(val)
            zbx.send(key, val, self.Items[idx][5], only_positive_speed=True)
        del params, result

    def items(self, template):
        result = ''
        for num, item in enumerate(self.Items):
            if self.Type == "mamonsu":
                delta = Plugin.DELTA.as_is
            else:
                delta = item[5]
            # split each item to get values for keys of both agent type and mamonsu type
            keys = item[1].split('[')
            result += template.item({
                    'key': self.right_type(self.key + keys[0] + '{0}', keys[1][:-1]),
                    'name': 'PostgreSQL {0}'.format(item[2]),
                    'value_type': self.VALUE_TYPE.numeric_float,
                    'units': item[4],
                    'delay': self.plugin_config('interval'),
                    'delta': delta
            })
        return result

    def graphs(self, template):
        graphs_name = [
            'PostgreSQL instance: rate',
            'PostgreSQL instance: events',
            'PostgreSQL instance: temp files',
            'PostgreSQL instance: tuples']
        result = ''
        for name in graphs_name:
            items = []
            for num, item in enumerate(self.Items):
                if item[3][0] == name:
                    # split each item to get values for keys of both agent type and mamonsu type
                    keys = item[1].split('[')
                    items.append({
                        'key': self.right_type(self.key + keys[0] + '{0}', keys[1][:-1]),
                        'color': item[3][1],
                        'yaxisside': item[3][2]
                    })
            graph = {'name': name, 'items': items}
            result += template.graph(graph)

        return result

    def keys_and_queries(self, template_zabbix):
        result = []
        for item in self.Items:
            # split each item to get values for keys of both agent type and mamonsu type
            keys = item[1].split('[')
            result.append('{0}[*],$2 $1 -c "{1}"'.format('{0}{1}.{2}'.format(self.key, keys[0], keys[1][:-1]),
                                                         self.query_agent.format(format(item[0]))))
        return template_zabbix.key_and_query(result)
