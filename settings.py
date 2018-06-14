from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

TOKEN = '505101349:AAFz76h3FvMCGP5_mfmM4s-zGCPX65v3Ql4'

StepLength = 200
api_id = 0
api_hash = ''

DbUser = 'root'
DbPwd = ''
DbHost = '127.0.0.1'
DbPort = '3306'
DbName = ''

proxy_host = ''
proxy_port = 0

try:
    from local_settings import *
except ImportError:
    pass

engine = create_engine(
    'mysql+pymysql://' + DbUser + ':' + DbPwd + '@' + DbHost + ':' + str(DbPort) + '/' + DbName + '?charset=utf8mb4',
    encoding='utf8', )
DBSession = sessionmaker(bind=engine)
