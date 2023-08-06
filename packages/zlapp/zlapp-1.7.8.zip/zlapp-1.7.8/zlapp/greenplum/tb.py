
def update_tb(name,loc='aliyun'):
    exec("from zlapp.greenplum import %s"%name)

    f=eval('%s.update_%s'%(name,name))

    


