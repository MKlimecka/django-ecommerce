import pymysql
from .celery import celery 

pymysql.install_as_MySQLdb()

__all__ = ('celery')