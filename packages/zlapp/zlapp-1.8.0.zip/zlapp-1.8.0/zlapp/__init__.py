from zlapp.cdc.api import pre_meta
from zlapp.cdc import api 

forbiden_list=["yunnan_baoshan_ggzy","yunnan_chuxiong_ggzy","yunnan_dali_ggzy","yunnan_dehong_ggzy","yunnan_honghe_ggzy","yunnan_kunming_ggzy","yunnan_lijiang_ggzy"
,"yunnan_lincang_ggzy","yunnan_puer_ggzy","yunnan_tengchong_ggzy","yunnan_wenshan_ggzy"
,"yunnan_xishuangbanna_ggzy","yunnan_yunnansheng_1_ggzy","yunnan_yunnansheng_ggzy","yunnan_yuxi_ggzy","yunnan_zhaotong_ggzy"
,"guangdong_shenzhen_gcjs"
,"sichuan_suining_ggzy",'sichuan_yibin_ggzy','sichuan_yaan_ggzy']



app_settings={

"kunming":{
    "conp_gp":['developer','zhulong!123','192.168.169.91:5433','base_db','public'],
    "conp_app1":['postgres','since2015','192.168.169.108','biaost','public'],
    "conp_app5":['developer','developer','192.168.169.111','biaost','public']
            }
,

"aliyun":{
    "conp_gp":['developer','zhulong!123','192.168.4.206','biaost','public'],
    "conp_app1":['postgres','since2015','192.168.4.207','biaost','public'],
    "conp_app5":['developer','zhulong!123','192.168.4.206','biaost','public']
}


}
