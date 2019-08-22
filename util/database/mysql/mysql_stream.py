#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Input stream and output stream interface.
    沿用绣哥的stream,去掉了mqs的stream，iostring对python3进行适配，stream在构造时直接赋handler实例
    @version:   1.0
    @author:    yangxiu@renrenche.com
    @date:      20141020
"""


class InputStream:
    """Data input stream interface
    """
    def __init__(self, config):
        """Initialize.
        Args:
            config      A dict object for configurations containing key,value 
                        pairs as config items.
        """
        pass

    def read(self, timeout=0):
        """Read one object from stream.
        Returns:
            dict        data object. format: {field_name:value}
            None        no data.
        """
        pass


class OutputStream:
    """Data output stream interface
    """
    def __init__(self, config):
        """Initialize.
        Args:
            config      A dict object for configurations containing key,value 
                        pairs as config items.
        """
        pass

    def write(self, data, immutable_fields=None):
        """Write one object into stream.
        Args:
            data                data object. format: {field_name:value}
            immutable_fields    immutable field name list
        Returns:
            int                 number of affected data
        Raises:
            OutputStreamError
        """
        pass


class MysqlInputStream(InputStream):
    pass


class MysqlOutputStream(OutputStream):
    '''Mysql output stream. Put data object into mysql'''
    def __init__(self, handler, main_table):
        '''Initialize.
        Args:
            config      dict 
                {
                    'MYSQL_HOST':'',
                    'MYSQL_PORT':0,
                    'MYSQL_USER':'',
                    'MYSQL_PASSWD':'',
                    'MYSQL_DB':'',
                    'MYSQL_CHARSET':'',
                    'MAIN_TABLE':'',
                }
        '''
        # self.db = MysqlHandler(config)
        # self.table = config['MAIN_TABLE']
        self.db = handler
        self.table = main_table

    def prepare_sql(self, data, immutable_fields):
        """Prepare sql and params.
        Args:
            data                data object. format: {field_name:value}
            immutable_fields    immutable field name list
        """
        if immutable_fields is None:
            immutable_fields = []
        import io
        sbuf = io.StringIO()
        sbuf.write('INSERT INTO %s SET ' % self.table)
        sbuf.write(','.join([
                   ' %s=%%s '%(key) for key in data.keys() if data.get(key)
        ]))
        sbuf.write('ON DUPLICATE KEY UPDATE ')
        sbuf.write(','.join([
                   ' %s=%%s ' % (key) for key in data.keys() 
                   if data.get(key) and key not in immutable_fields
        ]))        

        sql = sbuf.getvalue()
        values = [data[key] for key in data.keys() if data.get(key)]
        values.extend([data[key] for key in data.keys()
                      if data.get(key) and key not in immutable_fields])
        return sql, values

    def write(self, data, immutable_fields=None):
        """Write one object into stream.
        Args:
            data                data object. format: {field_name:value}
            immutable_fields    immutable field name list
        Returns:
            int                 number of affected data
        Raises:
            OutputStreamError
        """
        sql, values = self.prepare_sql(data, immutable_fields)
        return self.db.insert(sql, values)
