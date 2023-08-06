
def update_tb(name,loc='aliyun'):
    exec("from zlapp.greenplum import %s"%name)

    f=eval('%s.update_%s'%(name,name))

    if loc=='kunming':
        conp=['developer','developer','192.168.169.111','biaost','public']

    else:
        conp=['developer','zhulong!123','192.168.4.206','biaost','public']

    f(conp)


for name in ['']:
    update_tb(name,loc='kunming')


