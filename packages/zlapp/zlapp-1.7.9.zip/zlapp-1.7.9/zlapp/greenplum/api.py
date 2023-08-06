
import time
from zlapp.greenplum.api_dag import  tbdag  
def update_tb(name,loc='aliyun'):
    if name in ['qy_zz','qy_base','qy_zcry']:
        print("%s--静态表，不更新"%name)
        return 
    exec("from zlapp.greenplum import %s"%name)

    f=eval('%s.update_%s'%(name,name))

    if loc=='kunming':
        conp=['developer','developer','192.168.169.111','biaost','public']
        conp_src=['developer','zhulong!123','192.168.169.91:5433','base_db','public']
        conp_dst=['postgres','since2015','192.168.169.108','biaost','public']

    else:
        conp=['developer','zhulong!123','192.168.4.206','biaost','public']
        conp_src=['developer','zhulong!123','192.168.4.183:5433','base_db','public']
        conp_dst=['postgres','since2015','192.168.4.207','biaost','public']
    if name in ['gg_html','gg_html_algo']:
        f(conp_src,conp_dst)
    else:

        f(conp)

def plan_tb(name,loc='aliyun'):
    if name=='all':
        plan_tb('gg_meta')
        plan_tb('gg_html')
        return 
    tbs=tbdag.tplist(name)
    print("准备更新tbs--",tbs)
    for tb in tbs:
        print(tb)
        update_tb(tb,loc)



# def update_all(loc):
#     bg=time.time()

#     names=['gg_meta','gg_html','gg','gg_zhongbiao','qy_zhongbiao','xmjl_zhongbiao','app_gg_zhongbiao','app_qy_zz'
#     ,'app_qy_zcry','t_gg_ent_bridge','app_qy_query','bd_dt','bd','t_bd_xflv']

#     for name in names:
#         print(name)
#         update_tb(name,loc)



# def update_all(static=None):
#     bg=time.time()
#     update_gg_meta()
#     update_gg()
#     gg_html.update_gg_html()
#     if static is not None:
#         update_qy_base()
#         update_qy_zcry()
#         update_qy_zz()
#         update_t_person()

#     ###应用表部分
#     update_gg_zhongbiao()
#     update_qy_zhongbiao()
#     xmjl_zhongbiao.update_xmjl_zhongbiao()
#     update_app_gg_zhongbiao()
#     update_app_qy_zz()
#     update_app_qy_zcry()
#     update_t_gg_ent_bridge()
#     update_app_qy_query()
#     bd_dt.update_bd_dt()
#     t_bd_xflv.update_t_bd_xflv()
#     ed=time.time()

#     cost=int(ed-bg)

#     print("耗时 %d 秒"%cost)

#update_all()










