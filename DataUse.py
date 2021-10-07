import plotly.offline as pyoff
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import re
import os
import datetime,calendar,typing
import time
from datetime import datetime as DT

mon=['mon','monday']
tue=['tue','tuesday']
wed=['wed','wednesday']
thu=['thu','thursday']
fri=['fri','friday']
sat=['sat','saturday']
sun=['sun','sunday']
dict_week={1:mon,2:tue,3:wed,4:thu,5:fri,6:sat,7:sun}

Chose_OHLC_LIST_={'o':0,'h':1,'l':2,'c':3}

def tick_unit(price,contract):
    type_=type(contract)
    tick=0
    # type= shioaji.contracts.Stock/shioaji.contracts.Future etc...
    if 'Future' in  str(type_):
         if re.findall('mxf|txf', str(contract.code).lower()):
            tick=1
         elif re.findall('fxf', str(contract.code).lower()):
            tick=0.2
         elif re.findall('te|zef|exf|gtf', str(contract.code).lower()):
            tick=0.05
         else:
             tick=1
    elif 'option' in str(type_).lower():
        # 台指選
        if re.findall('tx', str(contract.code).lower()):
             if float(price)<10:
                 tick=0.1
             elif 50>float(price)>=10:tick=0.5
             elif 500>float(price)>=50:tick=1
             elif 1000>float(price)>=500:tick=5
             elif float(price)>=1000:tick=10
        elif re.findall('teo', str(contract.code).lower()):
             if float(price)<0.5:
                 tick=0.005
             elif 2.5>float(price)>=0.5:tick=0.025
             elif 25>float(price)>=2.5:tick=0.05
             elif 50>float(price)>=25:tick=0.25
             elif float(price)>=50:tick=0.5
        elif re.findall('tfo', str(contract.code).lower()):
             if float(price)<2:
                 tick=0.02
             elif 10>float(price)>=2:tick=0.1
             elif 100>float(price)>=10:tick=0.2
             elif 200>float(price)>=100:tick=1
             elif float(price)>=200:tick=2
    elif 'stock' in str(type_).lower():
        return StockOneTick(price)
    return tick
def StockOneTick(price):
    tick=0
    if float(price)<10:
        tick=0.01
    elif 10<= float(price)<50:
        tick=0.05
    elif 50<=float(price)<100:
        tick=0.1
    elif 100<=float(price)<500:
        tick=0.5
    elif 500<=float(price)<1000:
        tick=1
    else:
        tick=5
    return tick


def read_tick_record_rpt(__FileRPTRECORD__):
    list_=[]
    with open(__FileRPTRECORD__,'r') as F:
        Day=DT.strptime( os.path.basename(__FileRPTRECORD__)[:8],'%Y%m%d')
        
        for i in F:
            tmp=i.split(',')
            try:
                DataTime=DT.strptime(os.path.basename(__FileRPTRECORD__)[:8]+'-'+tmp[0],'%Y%m%d-%H:%M:%S.%f')
            except:
                DataTime=DT.strptime(tmp[0],'%H:%M:%S.%f')
            list_.append((DataTime,float(tmp[2]),float(tmp[5])))
        return list_  
            
def getlastprice(tx,day,N=1,get='c'):# get = o h l c
    # 獲得該DICT內的前N天的對應參數 OHLC
    getindex={'o':0,'h':1,'l':2,'c':3}
    list_=list(tx)
    index=list_.index(day)
    last_day=list_[index-N]
    return tx[last_day][getindex[str(get).lower()]]
class KDD:
    def __init__(self):
        self.KD={}
        self.rpt_=''
        self.KD5_Special={}
def CI_calculate(Bmaxf):# 信賴區間統計
    CI5_Bmax=int((len(Bmaxf)*0.05)/2) # Confidence interval
    
    CI5_Bmax_front=Bmaxf[:CI5_Bmax]
    CI5_Bmax_back=Bmaxf[-CI5_Bmax:]
    
    sum_=sum(Bmaxf)-sum(CI5_Bmax_front)-sum(CI5_Bmax_back)
    allsmaplenumber=len(Bmaxf)-len(CI5_Bmax_front)-len(CI5_Bmax_back)
    avg=sum_/allsmaplenumber
    return avg
def GetTrend(kdtime_start,dict_,N,LIST=''):# N=往前幾根K棒
    if not LIST:
        LIST=list(dict_)
    if len(LIST)<N:return 0,0
    index=LIST.index(kdtime_start)
    Trend=0
    Trend_PT=0
    LAST_C=0
    for i in range(1,N+1):
        
        
        key=LIST[index-i]
   
        OO,HH,LL,CC=dict_[key][:4]
        if  LAST_C:
            if CC>LAST_C:# 返回去 如果一路 CC 比 LAST_C 還大 代表往下 相反往上
                Trend-=1
            elif CC<LAST_C:
                Trend+=1
            Trend_PT+=(LAST_C-CC)# 若為正數代表 往上
        LAST_C=CC
    return Trend,Trend_PT
def getkd_csv_path(set_kdtime): # 得到特定KD的CSV位置
    folderkd=r'D:\Python\All_Practice\證券\TXO回測\其他工具\\'
    
    am_kd=folderkd+'All_KD_'+str(set_kdtime)+'k_am.csv'
    pm_kd=folderkd+'All_KD_'+str(set_kdtime)+'k_pm.csv'
    return am_kd,pm_kd
def getkd(list_rpt): # 得到KD 含特化5K
        
            ST_DATA=KDD()
           
            for k in list_rpt:
                time_,open_today,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,sellout= k
                HH,MM,SS=time_.strftime("%H:%M:%S").split(":")
                next_kd_=(datetime.datetime(time_.year,time_.month,time_.day,int(HH),int(MM),int(SS))).strftime("%H:%M")
                if  next_kd_ in ST_DATA.KD:
                         
                                       
                            OPEN_,High_,Low_,Close_,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vo= ST_DATA.KD[next_kd_]            
                            if High_<close:
                                    High_=close
                            if Low_>close:
                                    Low_=close
                            Volume=int(Volume)
                            Volume_sum=int(Volume_sum)
                        
                            Volume+=int(vol_)
                        
                            ST_DATA.now_ask_bid_vol[int(ticktype)]+=int(vol_)
                            
                     
                        
                    
                    
                            ST_DATA.KD[next_kd_] =  OPEN_,High_,Low_,close,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,ST_DATA.now_ask_bid_vol
                else:
                            ST_DATA.now_ask_bid_vol=[0,0,0,0] 
                            ST_DATA.now_ask_bid_vol[int(ticktype)]+=int(vol_)
                            list_kd=list(ST_DATA.KD)
                            
                     # ========= 特化AMAT 5分K=========
                            try:
                                
                                if next_kd_ in day_kd_list:
                                     kd5O,kd5H,kd5L,kd5C,kd5Vol=0,0,0,0,0
                                     
                                     if len(list_kd[len(list_kd)-5:len(list_kd)])>=5:
                                         for kd5 in range(len(list_kd)-5,len(list_kd)):
                                             O_,H_,L_,C_,_,_,Vol__=ST_DATA.KD[list_kd[kd5]][:7]
                                             kd5Vol+=int(Vol__)
                                             if kd5==len(list_kd)-5:
                                                 kd5O=float(O_)
                                             if kd5==len(list_kd)-1:kd5C=float(C_)
                                             if kd5!=len(list_kd)-1:
                                                 if not kd5H:
                                                     kd5H=float(H_)
                                                 elif float(H_)>kd5H:
                                                     kd5H=float(H_)
                                                 if not kd5L:
                                                     kd5L=float(L_)
                                                 if float(L_)<kd5L:
                                                     kd5L=float(L_)
                                         Amat_Speci=((kd5H-kd5L)/kd5O/kd5Vol)*1000000
                                         ST_DATA.KD5_Special[next_kd_]=kd5O,kd5H,kd5L,kd5C,kd5Vol,Amat_Speci
                            except Exception as Errorkd:
                                print(" Special KD5 Error:" , Errorkd)
                                pass   
                            if list_kd:
                              index_=list_kd.index(list_kd[-1])
##                              Trend=Get_KD_Before(index_,list_kd,5,ST_DATA.KD) #前五K棒之趨勢 是以上一根為主

                            
                            ST_DATA.KD[next_kd_] =  close,close,close,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,str(sellout).strip(),ST_DATA.now_ask_bid_vol
            return ST_DATA.KD,ST_DATA.KD5_Special
def Read_tse_5sec(file_):# 讀取每5 秒 大盤指數
        with open(file_,'r') as f:
                year=int(os.path.basename(file_).split('.')[0][:4])
                month=int(os.path.basename(file_).split('.')[0][4:6])
                day=int(os.path.basename(file_).split('.')[0][6:])
                dict_={}



                for i in f:
                    try:    
                        if '指數統計' in str(i) or re.findall('年|月|日|時間|指數',str(i)):continue
                        temp_=i.split(',')
                        temp_2=i.split('",')
                        temp_2_copy=temp_2.copy()
                        for j in range(0,len(temp_2)):
                                try:
                                 if ':' not in str(temp_2[j]):
                                     temp_2_copy[j]=float(temp_2[j].replace(",",'').replace('"',''))

                                 else:
                                     temp_2_copy[j]=str(temp_2[j].replace("=",'').replace('"',''))
             
                                except:pass
                        
                        HH,MM=re.findall("(\d+):(\d+)",temp_[0])[0]
                        TIMEDATA=DT(year,month,day,int(HH),int(MM))
                        dict_[TIMEDATA]=temp_2_copy
                    except:continue
        return dict_
def SD(List):# 標準差
    avg=sum(List)/len(List)
    sd_sum=0
    for i in List:
        sd_sum+=(abs(i-avg)**2)
    return (sd_sum/len(List))**0.5,avg


class Dateday():
    ____change_dash=""
    ____splitext=['/','-','~',',','\\','_']
    
    def __init__(self,dateofday):
        self.origindal_day=dateofday
        dateofday=str(dateofday)
        s=self._____get()
    def __call__(self,a,b):
        return 123456,a
    def __repr__(self):
        return ( self.____change_dash) 
    def _____get(self):
        global ____change_dash
        for i in self.____splitext:  #yyyy-mm-dd
            
            if i in self.origindal_day:
               self.____change_dash=self.origindal_day.replace(i,'-')
               year,month,day=self.origindal_day.split(i)
               self.year=year
               self.month=month
               self.day=day
               return ( self.____change_dash)
        if len(self.origindal_day)==8 :     #yyyymmdd:
            self.year=self.origindal_day[:4]
            self.month=(self.origindal_day[4:6])
            self.day=(self.origindal_day[6:])
        elif len(self.origindal_day)==6 :   #yyyy m d:
            
            
            self.year=self.origindal_day[:4]
            self.month=(self.origindal_day[4:5])
            self.day=(self.origindal_day[5:])
        self.____change_dash=str(self.year)+'-'+str(self.month)+'-'+str(self.day )
            
        return ( self.____change_dash)
    def get_week_alp2num(daychoose):
    
            for i in dict_week:
                for j in dict_week[i]:
                 
                    if re.findall(j,daychoose,re.IGNORECASE):
                        daychoose=i
                        
                        return daychoose
def Nday(kdtime_start,dict_,N,LIST=''):# N=往後幾日 狀況OHLC
    if not LIST:
        LIST=list(dict_)
    if len(LIST)<N:return 0,0
    index=LIST.index(kdtime_start)
  
    return dict_[LIST[index+N]][:4]
def highest(OHLC,N,time_,dict_k,LIST=''):# 找N K棒前的最高點
    # N= 包含自己 + 前面幾根
    # OHLC= Chose one  : {'o'=0,'h'=1,'l'=2,'c'=3} # 可以放 0 或是O(大小寫皆可) = 查詢Open
    if not str(OHLC).isdigit():
        
        FIND_=Chose_OHLC_LIST_[str(OHLC).lower()]
    else:
        FIND_=OHLC
    LIST_Div={0:[],1:[],2:[],3:[]}
    index=LIST.index(time_)
    for i in range(index-N,index+1):
            
            _OHLC=dict_k[LIST[i]][:4]
            LIST_Div[FIND_].append(_OHLC[FIND_])
    return max(LIST_Div[FIND_])
def lowest(OHLC,N,time_,dict_k,LIST=''):
    # N= 包含自己 + 前面幾根
 
    # OHLC= Chose one  : {'o'=0,'h'=1,'l'=2,'c'=3} # 可以放 0 或是O(大小寫皆可) = 查詢Open
    if not str(OHLC).isdigit():
        
        FIND_=Chose_OHLC_LIST_[str(OHLC).lower()]
    else:
        FIND_=OHLC
    LIST_Div={0:[],1:[],2:[],3:[]}
    index=LIST.index(time_)
    for i in range(index-N,index+1):
            
            _OHLC=dict_k[LIST[i]][:4]
            LIST_Div[FIND_].append(_OHLC[FIND_])
    
    return min(LIST_Div[FIND_])
def get_k_info_from(t,dict_k,N,LIST=''):# 從第N個K棒開始往前比對所有資訊 N 也包含自己 共會有 N+1 結果
    if not LIST:LIST=list(dict_k)
    index=LIST.index(t)
    list_group=[]
    for i in range(index-N,index+1):
            
            _OHLC=dict_k[LIST[i]][:4]
            list_group.append(_OHLC)
    
    return list_group
def get2k_info(K1,K2):# 比對兩個K棒細部關係
    #K1 時間 都要比K2早
    o1,h1,l1,c1=K1
    o2,h2,l2,c2=K2
    detail=[]
    count=0
    # 0: O1>O2 4:H1>O2  8:L1>O2 12:C1>O2
    # 1: O1>H2 5:H1>H2  9:L1>H2 13:C1>H2
    # 2: O1>L2 6:H1>L2 10:L1>L2 14:C1>L2
    # 3: O1>C2 7:H1>C2 11:L1>C2 15:C1>C2
    # 先取六種 0 3 5 10 12 15
    for k1 in K1:
        for k2 in K2:
            res=0
            if k1>k2:
                res=1
            elif k1<k2:
                res=2
            else:
                res=3
            detail.append(res)
            count+=1
    # 例外新增 index=>16/17 收盤情形
    res=0
    if c1>o1:
        res=1
    elif c1<o1:
        res=2
    else:
        res=3
    detail.append(res)
    res=0
    if c2>o2:
        res=1
    elif c2<o2:
        res=2
    else:
        res=3
    detail.append(res)
    return detail
def Bday(kdtime_start,dict_,N,LIST=''):# N=往前幾日 狀況OHLC # 用List速度會比dict快
    if not LIST:
        LIST=list(dict_)
    if len(LIST)<N:return 0,0
    index=LIST.index(kdtime_start)
    if index-N==-1:return (0,0,0,0),None
    return dict_[LIST[index-N]][:4],LIST[index-N]
def getma(maall,N=5,dict_ma=''):
    if len(maall)<N:return 0
    if dict_ma:
        dict_ma[N]=sum(maall[-N:])/N
        return sum(maall[-N:])/N,dict_ma
    else:
        return sum(maall[-N:])/N
def BTrend(kdtime_start,dict_,N,LIST='',only=''):# N=往後幾根K棒
    if not LIST:
        LIST=list(dict_)
    if len(LIST)<N:return 0,0
    index=LIST.index(kdtime_start)
    
    tO,tH,tL,tC=dict_[kdtime_start][:4]
    HH=0
    LL=0
    
    for i in range(index+1,index+N+1):


        key=LIST[i]
        if only:
            if i!=index+N:continue
        O,H,L,C=dict_[(key)][:4]
        if not HH:
                HH=H
        elif H>HH:
            HH=H
        if not LL:
            LL=L
        elif L<LL:
            LL=L
 
    return HH-tC,LL-tC,HH/tC,LL/tC
def get_weektimes(year,month,times,daychoose:typing.Union[int,str]):
        # daychoose:typing.Union[int,str]
        if isinstance(daychoose,str):
            daychoose=Dateday.get_week_alp2num(daychoose)
       
        arr_week=calendar.monthcalendar(year,month)
       
        if daychoose==None:
            return 'Not Found' 
        counday=0
        for each in arr_week:
          
            if each[daychoose-1]:
                counday+=1
                
                
                if counday==times:
                    day_data=datetime.datetime(int(year),int(month),int(each[daychoose-1]))
                    day=Dateday(str(year)+'/'+str(month)+"/"+str(each[daychoose-1]))
                    return day,day_data

                        
def make_kd(list_am,LIMIT_VALUE_MIN_2=1.1,kd_settime=60,TIMEDIFFSET=90,TIMEDIFF_BACKPROFIT=50
               ,outtimes_stoploss=20,MAXOUT=100,Stoploss=-20,RD_Value=10,mkd_settime=10,uplimit_out=0.8
               ,dnlimit_out=0.3,dnlimit_in=0.3,uplimit_in=0.8,anotherset_times_of_out=1234,anotherset=9999
               ,LIMIT_VALUE_MIN=0.8 ,loss_continue_set_back=3,setprofit=40,setprofit_smallthan=0,loss_continue_set_=3
               ,midtime=10,mini_loss=20,mini_set_time='',allAMP_list='',read_txo_='',AMPM='am'):

        TradeData=INFO()
        
        midtime=':'+str(midtime)
        next_kd_=''
        next_kd_data=''
        
       
        AMAT_TIMES=1000000
        Last_kd=''
        Trend=0
        Last_mkd=''
        Amp=0
        
        UPS,DOS,PT=0,0,0
       
        # USE RPT FORMAT
        if list_am and not read_txo_:
            time___=list_am[1][0]
            
            OCD_string,Out_of_contracct_day=get_weektimes(time___.year,time___.month,3,3)#得到合約到期日
    

        
        for k in list_am:

            if read_txo_:
                time_,open_today,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,sellout= k.split(',')
                time_str=time_[:8]
             
                today_str=''
            else:
                time_,open_today,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,sellout= k
                time_str=time_.strftime("%H:%M:%S")
                Day_str=time_.strftime('%Y/%m/%d')
                today_str=time_.strftime("%Y%m%d")
            sellout=int(str(sellout).strip())
        
            
            
            ST_H=int(time_str.split('.')[0][:2])
            ST_M=int(time_str.split('.')[0][3:5])
            ST_S=int(time_str.split('.')[0][6:8])
            if 'pm' in str((AMPM)).lower():
                TimeNow=time_
                if not PM_DAY:
                    PM_DAY=time_
            else:
                TimeNow=DT(2020,1,1,ST_H,ST_M,ST_S)
            
            TimeNow_2=DT(2020,1,1,ST_H,ST_M)
            

            now_amp=float(today_high)-float(today_low)
           
            # 1K
            if not next_kd_data:
                if kd_settime<=60:
                    if 'pm' in str((AMPM)).lower():
                        
                        next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,time_.minute)
                    else:
                        next_kd_data=DT(2020,1,1,int(ST_H),int(ST_M))
                    
                else:
                    if 'pm' in str((AMPM)).lower():
                        
                        next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,0)+datetime.timedelta(seconds=kd_settime)
                    else:next_kd_data=TimeNow_2+datetime.timedelta(seconds=kd_settime)
                next_kd_=next_kd_data.strftime("%H:%M")
            elif  TimeNow>=next_kd_data:
                if kd_settime<=60:
                    next_kd_data=DT(2020,1,1,int(ST_H),int(ST_M))
                    
                else:
                    
                    next_kd_data=next_kd_data+datetime.timedelta(seconds=kd_settime)
                    

                next_kd_=next_kd_data.strftime("%H:%M")

            if not Last_mkd:
                Last_mkd=(DT(2020,1,1,int(ST_H),int(ST_M),int(ST_S))).strftime("%H:%M:%S")
            
            
            if not Last_kd:
                Last_kd=next_kd_
            if next_kd_ in TradeData.KD:
                                                    OPEN_,High_,Low_,Close_,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vo= TradeData.KD[next_kd_]            
                                                    TradeData.KD[next_kd_] =  OPEN_,High_,Low_,close,Today_High,Today_Low,Volume,Volume_sum,TickType,buyin,sellout,now_ask_bid_vo
            else:
                                                
                                                now_ask_bid_vol=[0,0,0,0] 
                                                now_ask_bid_vol[int(ticktype)]+=int(vol_)
                                                
                                                
                                                
                                                
                                                if len(TradeData.KD)>=1:
                                                 if TradeData.KD[list(TradeData.KD)[-1]]:
                                                                             
                                                                            
                                                                            Open,now_high,now_low,Close,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vol___=TradeData.KD[list(TradeData.KD)[-1]]
                                                                                                                                                       
                                                                            
                                                                                
                                                                           
                                                TradeData.Price_KD[next_kd_]={}
                                                
                                                TradeData.KD[next_kd_] =  close,close,close,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,str(sellout).strip(),now_ask_bid_vol
        return TradeData.KD
           
def get_trend(kdtime_start,dict_,N):# N=往前幾根K棒
    LIST=list(dict_)
    if len(LIST)<5:return 0,0
    index=LIST.index(kdtime_start)
    Trend=0
    Trend_PT=0
    LAST_C=0
    for i in range(0,N+1):
        
        
        key=LIST[index-i]
        OO,HH,LL,CC=dict_[key][:4]
        if  LAST_C:
            if CC>LAST_C:# 返回去 如果一路 CC 比 LAST_C 還大 代表往下 相反往上
                Trend-=1
            elif CC<LAST_C:
                Trend+=1
            Trend_PT+=(LAST_C-CC)# 若為正數代表 往上
        LAST_C=CC
    return Trend,Trend_PT
def get_breaktrend(kdtime_start,dict_,N,bs,giveprice=''):# N=往前幾根K棒
    LIST=list(dict_)
    if len(LIST)<5:return 0,0
    if kdtime_start not in LIST:return 0,0
    index=LIST.index(kdtime_start)
    MAXDIFF=0
    NowHL=0
    for i in range(0,N+1):
        
        
        key=LIST[index-i]
        OO,HH,LL,CC=dict_[key][:4]
        if i==0 :# 若為做多就是要搜尋突破向上
            if bs==1   :
                if giveprice:
                   NowHL=float( giveprice)
                else:
                   NowHL=HH
                
            elif  bs==2:
                if giveprice:
                   NowHL=float( giveprice)
                else:
                    NowHL=LL
        else:
            if bs==2 and i!=0:
              if not MAXDIFF:
                  MAXDIFF=HH-NowHL
              elif MAXDIFF<HH-NowHL:
                  MAXDIFF=HH-NowHL
              if NowHL>=LL:
                    return 0,0
            elif bs==1:
                if not MAXDIFF:
                    MAXDIFF=NowHL-LL
                elif MAXDIFF<NowHL-LL:
                    MAXDIFF=NowHL-LL
                if NowHL<=HH:
                    return 0,0
    return 1,MAXDIFF
def get_shadow(O,H,L,C):
    
    if float(C)>=float(O):
        up_shadow=float(H)-float(C)
        do_shadow=float(O)-float(L)
    else:
        up_shadow=float(H)-float(O)
        do_shadow=float(C)-float(L)
    return abs(up_shadow),abs(do_shadow),float(C)-float(O)
def get_level(O,H,L,C,price=''):# 取得該價格在該K棒的位置水平
        amp=float(H)-float(L)
        if not price:# 若沒有給特定價位 則預設收盤價
            price=float(C)
        if amp == 0 :
            return -1
        where=(float(price)-float(L))/amp
        return where
def getamat(O,H,L,C,vol):
        AMAT_Times=10000000
        if float(vol)<10000:
            AMAT_Times=1000000
        AMAT=((H-L)/O/float(vol))*AMAT_Times
        return AMAT
def make_tse_k(dict_,k_set,Data='',AMPM='am',CoverDraw=0):
    # k_set 繪製日線
    next_kd_data=''
    next_kd=''
    if not Data:
        Data=INFO_2()
      
    Data.KD_TSE ={}
    kd_settime=k_set*60
    if k_set==-1:
        kd_settime=9999999
    Today_High=0
    Today_Low=0
    for time_ in dict_:
         close=dict_[time_]
         if not Today_High:
                Today_High=close
         elif   Today_High<close:
                Today_High=close
         if not Today_Low:
                Today_Low=close
         elif   Today_Low>close:
                Today_Low=close
             
         if not next_kd_data:
                if kd_settime<=60:
                    if 'pm' in str((AMPM)).lower():
                        
                        next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,time_.minute)
                    else:
                        next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,time_.minute)
                    
                else:
                    if 'pm' in str((AMPM)).lower():
                        
                        next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,0)+datetime.timedelta(seconds=kd_settime)
                    else:next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,time_.minute)+datetime.timedelta(seconds=kd_settime)
                next_kd_=next_kd_data.strftime("%H:%M")
         elif  time_>=next_kd_data:
                if kd_settime<=60:
                    next_kd_data=DT(time_.year,time_.month,time_.day,time_.hour,time_.minute)
                    
                else:
                    
                    next_kd_data=next_kd_data+datetime.timedelta(seconds=kd_settime)

                next_kd_=next_kd_data.strftime("%H:%M")
         if next_kd_ in Data.KD_TSE:
                                                    OPEN_,High_,Low_,Close_,Today_High_,Today_Low_,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vo= Data.KD_TSE[next_kd_]            
                                                         
                                                    Volume=int(Volume)
                                                    Volume_sum=int(Volume_sum)
                                                    
                                                    
                                                    if float(close)>=float(High_):
                                                        High_=float(close)
                                                      
                                                        
                                                    if float(close)<=float(Low_):
                                                        Low_=float(close)
                                                      
                                                        
                                                    Data.KD_TSE[next_kd_] =  OPEN_,High_,Low_,close,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vo
         else:
              if Data.KD_TSE:
                Open,now_high,now_low,Close,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vol___=Data.KD_TSE[list(Data.KD_TSE)[-1]]
                                                                              
                if CoverDraw:TradeData.DF['Time'].append(list(TradeData.KD)[-1])
                
                else:
                        Data.DF_TSE['Time'].append(time_.strftime("%Y/%m/%d")+' ' +list(Data.KD_TSE)[-1])
                        Data.DF_TSE['Open'].append(Open)
                        Data.DF_TSE['High'].append(now_high)
                        Data.DF_TSE['Low'].append(now_low)
                        Data.DF_TSE['Close'].append(Close)
                        Data.DF_TSE['Volume'].append(Volume)
              Data.KD_TSE[next_kd_] =  close,close,close,close,close,close,0,0,0,0,0,0
    if k_set==-1:
                        Open,now_high,now_low,Close,Today_High,Today_Low,Volume,Volume_sum,TickType,AskVolSum,BidVolSum,now_ask_bid_vol___=Data.KD_TSE[list(Data.KD_TSE)[-1]]
                
                        Data.DF_TSE['Time'].append(time_.strftime("%Y/%m/%d"))
                        Data.DF_TSE['Open'].append(Open)
                        Data.DF_TSE['High'].append(now_high)
                        Data.DF_TSE['Low'].append(now_low)
                        Data.DF_TSE['Close'].append(Close)
                        Data.DF_TSE['Volume'].append(Volume)

    return Data
##    k_set=幾分K
def get5sec_csv(day):# day=20210101 or datetime.datetime(2021,1,1)
    if isinstance(day,datetime.datetime):
        day=day.strftime("%Y%m%d")
    elif isinstance(day,str):
        if len(day)!=8:
           
            return
    elif isinstance(day,int):
        day=str(day)
        if len(day)!=8:return
    return Sec5_folder+str(day)+'.csv'
def read_5sec(file,day=''):# Read Csv from my create > EX :filepath= r'All_KD_1k_am.csv'
    if day:
        file=get5sec_csv(day)
    dict_={}# 讀取自行產生的k線
    day=os.path.basename(file).split('.')[0].strip()
    with open(file,'r') as ck:
        for i in ck:
            if re.findall('時間|日期|盤|價|月|日|秒|分|說|明' ,str(i)) :continue
            
            arr=i.split('","')
            time_str=arr[0].replace('=','').replace('"','').strip()
            if not time_str:continue
            
            DATATIME=datetime.datetime.strptime(day+time_str,'%Y%m%d%H:%M:%S')
            dict_[DATATIME]=float(arr[1].replace(',',''))
        return dict_
def read_kdcsv(file):# Read Csv from my create > EX :filepath= r'All_KD_1k_am.csv'
    dict_1k={}# 讀取自行產生的k線
    with open(file,'r') as ck:
        for i in ck:
            if re.findall('時間|日期|盤|價|月|日|秒|分|說|明' ,str(i)) :continue
            arr=(i.split(','))
            day_time=arr[0]
            if len(arr)>10:
                O,H,L,C,up,uper,ma5,ma10,ma20,ma60,ma120,Vol=arr[1:13]
            else:
                O,H,L,C,Vol,AT1,AT2=arr[1:8]
           
            day_1=re.findall('(\d+)\/(\d+)\/(\d+)',day_time.split(' ')[0])
            if day_1:
                year,month,dayy=day_1[0]
                year=int(year)
                month=int(month)
                dayy=int(dayy)
            
            time_hh,time_mm=day_time.split(' ')[1].split(':')
           
            time_hh=int(time_hh)
            time_mm=int(time_mm)
            TIMEDATA=datetime.datetime(year,month,dayy,time_hh,time_mm)
##            try:
            if len(arr)>10:
                dict_1k[TIMEDATA]=float(O),float(H),float(L),float(C),float(Vol)
            else:
                dict_1k[TIMEDATA]=float(O),float(H),float(L),float(C),float(Vol),float(AT1),float(AT2.strip())
            
        return dict_1k

def readcsv2(csvfile):# 讀取日線常用
    dict_csv={}
    change_type=0 # 0: 日線K  1:偵測到錯誤改為 縮小時間K   2: 元大資料的分K
    AT1=0 # 自行新增之欄位參數
    AT2=0 # 自行新增之欄位參數
    ma5,ma10,ma20,ma30,ma60=0,0,0,0,0
    PT,PTPER,Vol=0,0,1
    with open(csvfile,'r') as T:
        for j in T:
            if re.findall('時間|日期|盤|價' ,str(j)) :continue
            if not j.replace(',','')	:
                
                continue
            
            if '/' in str(j) or '-' in str(j):
               day_,O,H,L,C,PT,PTPER,ma5,ma10,ma20,ma30,ma60,Vol=(j.split(','))[:13]
               
               try:
                       if '/' in str(j):yy,mm,dd=day_.split('/')
                       elif  '-' in str(j):yy,mm,dd=day_.split('-')
                       TIMEDATA=datetime.datetime(int(yy),int(mm),int(dd))
               except:
                       continue
                      
                
                 
  
            if not ma5:
                    ma5=0
            if not ma10:
                    ma10=0
            if not ma20:
                    ma20=0
            if not ma30:
                    ma30=0
            if not ma60:
                    ma60=0
            dict_csv[TIMEDATA]=float(O),float(H),float(L),float(C),float(PT),float(PTPER),float(ma5),float(ma10),float(ma20),float(ma30),float(ma60),float(Vol),float(AT1),float(AT2)
            
    return dict(sorted(dict_csv.items(),key=lambda i:i[0] ,reverse=0) )

def readcsv(csvfile):# 讀取日線常用
    dict_csv={}
    change_type=0 # 0: 日線K  1:偵測到錯誤改為 縮小時間K   2: 元大資料的分K
    AT1=0 # 自行新增之欄位參數
    AT2=0 # 自行新增之欄位參數
    ma5,ma10,ma20,ma30,ma60=0,0,0,0,0
    PT,PTPER,Vol=0,0,1
    with open(csvfile,'r') as T:
        for j in T:
            if '日期'in str(j):continue
            if not j.replace(',','')	:continue
            ma5,ma10,ma20=0,0,0
            try:
               day_,O,H,L,C,PT,PTPER,ma5,ma10,ma20,ma30,ma60,Vol=(j.split(','))[:13]
               yy,mm,dd=day_.split('/')
               TIMEDATA=datetime.datetime(int(yy),int(mm),int(dd))
            except:
                if len(j.split(','))>10:
                    change_type=2
                else:
                    change_type=1
            if change_type:
                if change_type==1:
                    arr=(j.split(','))
                    day_time=arr[0]# day+time
                    O,H,L,C,Vol,AT1,AT2=arr[1:8]
                   
                
                elif change_type==2:
                    day_time,O,H,L,C,PT,PTPER,ma5,ma10,ma20,ma30,ma60,Vol=(j.split(','))[:13]
                    

                    
                day_1=re.findall('(\d+)\/(\d+)\/(\d+)',day_time.split(' ')[0])
                if day_1:
                    year,month,dayy=day_1[0]
                    year=int(year)
                    month=int(month)
                    dayy=int(dayy)
                try:
                        time_hh,time_mm=day_time.split(' ')[1].split(':')
               
                        time_hh=int(time_hh)
                        time_mm=int(time_mm)
                        TIMEDATA=datetime.datetime(year,month,dayy,time_hh,time_mm)
                except:continue
                
                 
  
            if not ma5:
                    ma5=0
            if not ma10:
                    ma10=0
            if not ma20:
                    ma20=0
            try:
                     dict_csv[TIMEDATA]=float(O),float(H),float(L),float(C),float(PT),float(PTPER),float(ma5),float(ma10),float(ma20),float(ma30),float(ma60),float(Vol),float(AT1),float(AT2)
            except:continue
    return dict(sorted(dict_csv.items(),key=lambda i:i[0] ,reverse=0) )
def get_kd_path(set_kdtime):
    folderkd=r'D:\Python\All_Practice\證券\TXO回測\其他工具\\'
    
    am_kd=folderkd+'All_KD_'+str(set_kdtime)+'k_am.csv'
    pm_kd=folderkd+'All_KD_'+str(set_kdtime)+'k_pm.csv'
    return am_kd,pm_kd
def ReadOHLC(file):
        dict_={}
        with open(file,'r') as OHLC:
                for i in OHLC:
                        temp=i.split(',')
                        dict_[temp[1]]=temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9],temp[10]
        return dict_
def Read_RPT_ZIP(zipfile):
    find_day=re.findall('Daily_(\d+)\_(\d+)_(\d+).zip',zipfile)[0]
    yy,mm,dd=find_day
    NowTIME=datetime.datetime(int(yy),int(mm),int(dd))
    SPLITTIME=datetime.datetime(2011,1,1)
    if NowTIME>SPLITTIME:# 2011之前為自行產生 只有TX資料 檔案偏小
      if os.path.getsize(zipfile)<1000:
        return 0
    my_zip = ZipFile(zipfile, 'r')
# Read Mehod:
#  1. Without Extractall
    with my_zip.open(my_zip.namelist()[0]) as my_file:
      
            return [i.decode('cp950') for i in my_file.readlines()]
##  2. To Extractall
##    my_zip.extractall() 
##    new_rptfile=zipfile.replace(".zip",'.rpt')
##    
##    with open(new_rptfile,'r')as me:
##            readtxt=me.readlines()
##            return readtxt
def read_ticks_txt(file):
    return  read_stock_rpt_sj(file)
     
def read_stock_rpt_sj(file):# 從永豐金存下來的格式轉成可讀list
    dict_={}
    list_all=[]
    ##time_,open_today,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,sellout= k
    with open(file,'r') as stock_rpt_sj:
            for i in stock_rpt_sj:
                tmp=(i.split(':'))
   
                dict_[tmp[0].strip()]=eval(tmp[1])
     
            
            
    todayopen=0
    today_high=0
    today_low=0
    vol_sum=0
    ticktype=0
    for j in range(0,len(dict_['ts'])):
        if j==0:
            todayopen=dict_['close'][0]
        time_stamp=dict_['ts'][j]
        close=float(dict_['close'][j])
        if not today_high:today_high=close
        elif today_high<close:today_high=close
        if not today_low:today_low=close
        elif today_low>close:today_low=close
        time_=datetime.datetime.utcfromtimestamp(float(str(time_stamp)[:10]+'.'+str(time_stamp)[10:13]))
        vol_=float(dict_['volume'][j])
        vol_sum+=vol_
        if close==float(dict_['bid_price'][j]):
            ticktype=1
        elif close==float(dict_['ask_price'][j]):
            ticktype=2
        buyin=float(dict_['bid_volume'][j])
        sellout=float(dict_['ask_volume'][j])
        
        list_all.append((time_,todayopen,close,today_high,today_low,vol_,vol_sum,ticktype,buyin,sellout))
    return list_all    
            
## 通常會從夜盤開始
def Write_TXT(file_txt,list_):
    with open(file_txt,'w+') as W:
     for X in list_:
                    now_time,Open_,Price,High_,Low_,Volume,All_Volume,_,_,_=X
        
                    W.write(now_time.strftime("%H:%M:%S"))
                    W.write(',')
                    W.write(str(Open_))
                    W.write(',')
                    W.write(str(Price))
                    W.write(',')
                    W.write(str(High_))
                    W.write(',')
                    W.write(str(Low_))
                    W.write(',')
                    W.write(str(Volume))
                    W.write(',')
                    W.write(str(All_Volume))
                    W.write(',')
                    W.write(str(1))
                    W.write(',')
                    W.write(str(1))
                    W.write(',')
                    W.write(str(1))
                    W.write('\n')

def read_tx_rpt(file):
    if file.endswith('.zip'):
        
        B=Read_RPT_ZIP(file)
    else:    
        B=open(file,'r') 
    if 1:
            start_count_time=time.time()
            list_am=[]
            list_pm=[]
            now_time=''
            
            Open_='' #今日開盤
            High_=''# 當前最高
            Low_='' # 當前最低
            Type=0  # 讀檔分兩種
            All_Volume=0
            first_day=''
            next_day=''
            AMSTART=0
            last_time_record=''
            AMStartTime=''
            NotGetPmdata=0
            for i in B:
                
                if ',' not in str(i) or not str(i).replace(' ','').replace('\t',''):
                    continue
                
                
                if '成交' in str(i) or '交易'in str(i) or '商品' in str(i) or '成交' in str(i) or '價' in str(i) or 'tx' not in str(i).lower() or 'mtx' in str(i).lower():continue
                if len(i.split(','))<9:
                    Day,Code,Contract,Time_,Price,Volume,_,_=(i.split(','))
                else:
                    Day,Code,Contract,Time_,Price,Volume,_,_,_=(i.split(','))
                
                 
                if '-' in str(Price) or float(Price)<100:
##                     Day,Code,Contract,Time_,DIFFPRICE,Volume,Price,_,_=(i.split(','))
                     continue
                  
                
                
                if 'tx' in str(Code).lower() and 'mtx' not in str(Code).lower():
                    
                    hh=int(Time_[:2])
                    mm=int(Time_[2:4])
                    ss=int(Time_[4:6])
                    year=int(Day[:4])
                    month=int(Day[4:6])
                    day__=int(Day[6:8])
                    Volume=int(Volume)/2 # B+S
                    All_Volume+=Volume
                    if not first_day:
                        first_day=datetime.datetime(year,month,day__)
                        next_day=datetime.datetime(year,month,day__)+datetime.timedelta(days=1)
                        if hh<15 or ( hh==8 and mm==45):# 代表沒有夜盤資料
                            
                            NotGetPmdata=1
                            

                        
                    if first_day<datetime.datetime(2017,5,15):# 2017/05/15 之後才有夜盤
                        am_start=datetime.datetime(first_day.year,first_day.month,first_day.day,8,45,0)
                        am_end=datetime.datetime(first_day.year,first_day.month,first_day.day,13,45,0)
                    else:
                        
                        am_start=datetime.datetime(next_day.year,next_day.month,next_day.day,8,45,0)
                        am_end=datetime.datetime(next_day.year,next_day.month,next_day.day,13,45,0)
                        if NotGetPmdata:
                            am_start=datetime.datetime(first_day.year,first_day.month,first_day.day,8,45,0)
                            am_end=datetime.datetime(first_day.year,first_day.month,first_day.day,13,45,0)
                    if '2017_05_15.zip' in str(file):
                        am_start=datetime.datetime(first_day.year,first_day.month,first_day.day,8,45,0)
                        am_end=datetime.datetime(first_day.year,first_day.month,first_day.day,13,45,0)
                    pm_start=datetime.datetime(first_day.year,first_day.month,first_day.day,15,00,0)
                    pm_end=datetime.datetime(first_day.year,first_day.month,next_day.day,5,00,0)
                    
                    now_time=datetime.datetime(year,month,day__,hh,mm,ss)
                    if am_start:
                        if len(list_am)>5000:
                            if AMStartTime==now_time:
                                return list_am,list_pm
                    
                    if not Open_:
                        Open_=float(Price)
                    if not High_:
                        High_=float(Price)
                    else:
                        if float(Price)>float(High_):High_=float(Price)
                    if not Low_:
                        Low_=float(Price)
                    else:
                        if float(Price)<float(Low_):Low_=float(Price)
                    if AMSTART:
                        if not AMStartTime:
                            AMStartTime=now_time
                        if (now_time-am_start).seconds>19000:
                            break
                    if not  AMSTART:
                        if (now_time-pm_start).seconds<50401:
                             
                               
                               list_pm.append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))
        ##               
                               pass
                    
                    if now_time>=am_start: # AM
                        if not AMSTART:
                            Open_=''# 今日開盤
                            High_=''# 當前最高
                            Low_='' # 當前最低
                            All_Volume=0
                            All_Volume+=int(Volume)
                        AMSTART=1
                        if not Open_:
                            Open_=float(Price)
                        if not High_:
                            High_=float(Price)
                        else:
                            if float(Price)>float(High_):High_=float(Price)
                        if not Low_:
                            Low_=float(Price)
                        else:
                            if float(Price)<float(Low_):Low_=float(Price)
                     
                        last_time_record=now_time
                        list_am.append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))
                    if am_start:
                      
                                
                        if now_time==am_end:
                            return list_am,list_pm
        
       
##            Write_TXT('rpt.txt',list_am)# 必須寫下
           
            return list_am,list_pm
           # Write_TXT('rpt_pm.txt',list_pm)

def read_opt_rpt(file):
                if file.endswith('.zip'):
        
                    B=Read_RPT_ZIP(file)
                    
                else:    
                    B=open(file,'r')
                if not B:
##                    print("Plz Give OPT Filepath")
                    return 0,0
                first_day=''
                next_day=''
                AMSTART=0
                week_day=""
                last_time_record=''
                AMStartTime=''
                OPT_dict_am={}
                OPT_dict_am['put']={}
                OPT_dict_am['call']={}
                OPT_dict_pm={}
                OPT_dict_pm['put']={}
                OPT_dict_pm['call']={}
                Open_='' #今日開盤
                High_=''# 當前最高
                Low_='' # 當前最低
                LAST_merchandise=''# 商品的改變 以及紀錄
                All_Volume=0
                for i in B:
                                
                                if ',' not in str(i) or not str(i).replace(' ','').replace('\t',''):
                                    continue
                                
                                
                                if '成交' in str(i) or '交易'in str(i) or '商品' in str(i) or '成交' in str(i) or '價' in str(i) or 'tx' not in str(i).lower() or 'mtx' in str(i).lower():continue
                                if len(i.replace(' ','').replace('\r','').replace('\n','').split(','))<9:
                                    
                ##                    Day,Code,Contract,Time_,Price,Volume,_,_=(i.split(','))
                                    Day,MarketType,Code,Contrace,PC,Time_,Price,Volume=(i.replace(' ','').replace('\r','').replace('\n','').split(','))
                ##                  ['20110117', 'TXO', '6400', '201106', 'P', '08555300', '12', '6']
                                else:
                
                                    Day,MarketType,Code,Contrace,PC,Time_,Price,Volume=(i.replace(' ','').replace('\r','').replace('\n','').split(','))[:8]
           
                                if '-' in str(Price) :
                ##                     Day,Code,Contract,Time_,DIFFPRICE,Volume,Price,_,_=(i.split(','))
                                     continue
                                  
                                
                                Price=float(Price)
                                if 'tx' in str(MarketType).lower() and 'mtx' not in str(MarketType).lower():
                                    hh=int(Time_[:2])
                                    mm=int(Time_[2:4])
                                    ss=int(Time_[4:6])
                                    year=int(Day[:4])
                                    month=int(Day[4:6])
                                    day__=int(Day[6:8])
                                    Volume=int(Volume) # B+S
                                    All_Volume+=Volume
                                    
                                    now_time=datetime.datetime(year,month,day__,hh,mm,ss)
                                    now_time_2=datetime.datetime(2020,1,1,hh,mm,ss)
                                    now_time_2_amstart=datetime.datetime(2020,1,1,8,45)
                                    now_time_2_amend=datetime.datetime(2020,1,1,13,46)
                                    if not week_day:
                                        week_day=   now_time.isoweekday()
                                    
                                    merchandise=MarketType+"_"+str(Contrace)+'_'+str(Code)+str(PC)
                                    if not first_day:
                                        first_day=datetime.datetime(year,month,day__)

                                        next_day=datetime.datetime(year,month,day__)+datetime.timedelta(days=1)
                                    if first_day<datetime.datetime(2017,5,15):# 2017/05/15 之後才有夜盤
                                        am_start=datetime.datetime(first_day.year,first_day.month,first_day.day,8,45,0)
                                        am_end=datetime.datetime(first_day.year,first_day.month,first_day.day,13,45,0)
                                    else:
                                        am_start=datetime.datetime(next_day.year,next_day.month,next_day.day,8,45,0)
                                        am_end=datetime.datetime(next_day.year,next_day.month,next_day.day,13,45,0)
                                    if '2017_05_15.zip' in str(file):
                                        am_start=datetime.datetime(first_day.year,first_day.month,first_day.day,8,45,0)
                                        am_end=datetime.datetime(first_day.year,first_day.month,first_day.day,13,45,0)
                                    pm_start=datetime.datetime(first_day.year,first_day.month,first_day.day,15,00,0)
                                    pm_end=datetime.datetime(first_day.year,first_day.month,next_day.day,5,00,0)
                                    
                                    now_time=datetime.datetime(year,month,day__,hh,mm,ss)
                                    if am_start:
                                        if len(OPT_dict_am)>5000:
                                            if AMStartTime==now_time:
                                                return OPT_dict_am,OPT_dict_pm
                                    if now_time_2_amend>now_time_2>=now_time_2_amstart:
                                        AMSTART=1
                                    else:
                                        AMSTART=0
##
##                                    if am_start> now_time>=pm_start : # AM
####                                        All_Volume=0
####                                        Open_='' #今日開盤
####                                        High_=''# 當前最高
####                                        Low_='' # 當前最低
####                                        LAST_merchandise=merchandise
##                                        AMSTART=0     
##                                    if now_time>=am_start : # AM
####                                        All_Volume=0
####                                        Open_='' #今日開盤
####                                        High_=''# 當前最高
####                                        Low_='' # 當前最低
####                                        LAST_merchandise=merchandise
##                                        AMSTART=1
##                                    if week_day==1:
##                                        AMSTART=1
####                                    print(pm_start,111)
####                                    print(am_start)
####                                    a=['pm','am']
####                                    print(now_time,  a[AMSTART])
####                                    print("==============")
                                    if not LAST_merchandise:
                                        LAST_merchandise=merchandise
                                    if merchandise!=LAST_merchandise:#商品更換
                                        All_Volume=0
                                        Open_='' #今日開盤
                                        High_=''# 當前最高
                                        Low_='' # 當前最低
                                        LAST_merchandise=merchandise
                                        
                                    if not Open_:
                                            Open_=float(Price)
                                    if not High_:
                                            High_=float(Price)
                                    else:
                                            if float(Price)>float(High_):High_=float(Price)
                                    if not Low_:
                                            Low_=float(Price)
                                    else:
                                            if float(Price)<float(Low_):Low_=float(Price)
                                    if not  AMSTART:
                                        if PC=='P':
                                            if merchandise not in OPT_dict_pm['put']:
                                                OPT_dict_pm['put'][merchandise]=[]
                                            OPT_dict_pm['put'][merchandise].append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))    
                                        
                                       

                                        elif PC=='C':
                                            if merchandise not in OPT_dict_pm['call']:
                                                OPT_dict_pm['call'][merchandise]=[]
                                            OPT_dict_pm['call'][merchandise].append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))
                                    elif  AMSTART:
                                        if PC=='P':
                                            if merchandise not in OPT_dict_am['put']:
                                                OPT_dict_am['put'][merchandise]=[]
                                            OPT_dict_am['put'][merchandise].append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))    
                                        
                                       

                                        elif PC=='C':
                                            if merchandise not in OPT_dict_am['call']:
                                                OPT_dict_am['call'][merchandise]=[]
                                            OPT_dict_am['call'][merchandise].append((now_time,Open_,Price,High_,Low_,Volume,All_Volume,1,1,1))
                return OPT_dict_am,OPT_dict_pm

def get_lastitem(dict_of_info,nowtime):# 獲取前一根K棒 或是日線 等資料
    temp_list=list(dict_of_info)
    aftertime=''
    beforetime=''
    if nowtime in dict_of_info:
        index0=temp_list.index(nowtime)
        beforetime=temp_list[index0-1]
        if beforetime in dict_of_info and beforetime<nowtime :
                  
               return beforetime
        else:
               return 0
        if index0-1==-1:
            beforetime=''
        if index0+1<len(temp_list):
            aftertime=temp_list[index0+1]
        if index0+1==-1:
            aftertime=''
        if not aftertime and not beforetime:
            print("★ 列表內資料不足")
            return 0
        elif aftertime and beforetime:
            time_diff2=(nowtime-beforetime).total_seconds()
            time_diff=(aftertime-nowtime).total_seconds()
            if aftertime<nowtime:
                time_interval =(nowtime-beforetime).total_seconds()
                aftertime=''
            elif nowtime<beforetime:
                time_interval =(aftertime-nowtime).total_seconds()
                beforetime=''
            else:
                
                if time_diff2==time_diff:
                    time_interval=time_diff
                elif time_diff2<time_diff:
                    time_interval=time_diff2
                elif time_diff2>time_diff:
                    time_interval=time_diff
                else:
                    print("★ 列表內時間間隔不定,請將列表資料內部時間設定一致")
                    return 0
        elif aftertime:
            time_interval=(aftertime-nowtime).total_seconds()
        elif beforetime:
            time_interval=(nowtime-beforetime).total_seconds()
        back=1
        before_time_=nowtime-datetime.timedelta(seconds=time_interval*back)
        if before_time_ in dict_of_info and before_time_<nowtime and 0:
                  return before_time_
        else:
            while 1 : # 避免沒有連續性的列表導致 找到不符合需求的前一天 或是前N秒
              try:  
                   before_time_=nowtime-datetime.timedelta(seconds=time_interval*back)
                   if before_time_ in dict_of_info:
                       if before_time_>nowtime:
                           print("★ 時間遞減錯誤")
                           return 0
                       
                       return before_time_
                   else:
                       back+=1
                   if (time_interval*back/86400)>20:# 計算大於20天
                       print(before_time_,nowtime)
                       return 0
                   elif time_interval<=100 and back>21600: # 21600 若為1分鐘 實際過了15天
                       return 0
                   elif time_interval>=85000 and  back>15:# 實際過了15天
                       return 0
              except:
                print(nowtime)
                dsa+=1
              
               
def get_before_price(dict_,t,N): # N= 幾根K棒前
    list_=list(dict_)
    index=list_.index(t)
    
    oo,hh,ll,cc=[],[],[],[]
    for i in range(index-1,index-N-1,-1):
        key=list_[i]
        o,h,l,c=dict_[key][:4]
        oo.append(o)
        hh.append(h)
        ll.append(l)
        cc.append(c)
    return oo,hh,ll,cc
        

def get_PNVI(dict_of_info,pvi_ma=0,nvi_ma=0,time_start='',time_end=''): # Get PVI AND NVI
    # pvi_ma=0,nvi_ma=0 設定要擷取的移動平均長度
    dict_PNVI={}
    count=0
    nvi=100
    pvi=100
    for time_ in dict_of_info:
        if time_start:
            if time_<time_start:continue
        if time_end :
            if time_>time_end:continue
##        if count>5000:return dict_PNVI
##        count+=1
        dict_PNVI[time_]={}
   #  dict_csv[TIMEDATA]=float(O),float(H),float(L),float(C),float(PT),float(PTPER),float(ma5),float(ma10),float(ma20),float(Vol),float(AT1),float(AT2)
        o,h,l,c,pt,ptper,_,_,_,vol=dict_of_info[time_][:10]
        
        time_before=get_lastitem(dict_of_info,time_)
        
        if time_before:
            vol_before=dict_of_info[time_before][9]
            close_before=dict_of_info[time_before][3]
            if vol>vol_before:
                
                pvi=pvi*(1+((c-close_before)/(close_before)))
            if vol<vol_before:
                nvi=nvi*(1+((c-close_before)/(close_before)))
           
            dict_PNVI[time_]['pvi']=pvi
            dict_PNVI[time_]['nvi']=nvi
            if pvi_ma:
                if len(dict_PNVI)>=pvi_ma:
                   key_ma=list(dict_PNVI)[(list(dict_PNVI).index(time_)-pvi_ma+1)]
                   
                  
                   pvi_ma_get= sum([ dict_PNVI[d]['pvi'] for d in dict_PNVI if key_ma <=d<=time_  ])/pvi_ma
                   dict_PNVI[time_]['pvi_ma'+str(pvi_ma)]=pvi_ma_get
                 
            if nvi_ma:
                if len(dict_PNVI)>=nvi_ma:
                   key_ma=list(dict_PNVI)[(list(dict_PNVI).index(time_)-nvi_ma+1)]
                   
                  
                   nvi_ma_get= sum([ dict_PNVI[d]['nvi'] for d in dict_PNVI if key_ma <=d<=time_  ])/nvi_ma
                   dict_PNVI[time_]['nvi_ma'+str(nvi_ma)]=nvi_ma_get
##                   print(time_,nvi_ma_get,nvi)
                  
                   
        else:
             dict_PNVI[time_]['pvi']=pvi
             dict_PNVI[time_]['nvi']=nvi
    return dict_PNVI
def Divide_group(x,div_detail=0,last_dot=1):# div=10 每10 分組
    # last_dot= 小數點後幾位 預設1
    # div_detail 要將1 分割成多少點數 0.1= 1 split 10
        ch=0
        if x<0:
            ch=1
            x=-x
        last_num=0
        if '.' in str(x) and div_detail<1:

                int_=int(str(x)[:str(x).find('.')])

                float_=float(str(x)[str(x).find('.'):])

                mid_=int_
                last_num=mid_
                if float(x)>mid_:
                    while 1:
                        mid_+=div_detail

                        if float(x)<mid_:

                            return round(last_num,last_dot)
##                              return mid_
                        last_num=mid_
                else:
                              return mid_
        elif div_detail>1:
                
                
                mid_=div_detail
                last_num=mid_
             
                if float(x)>mid_:
                    while 1:
                        mid_+=div_detail

                        if float(x)<mid_:
                            if ch:
                                last_num=-last_num

                            return round(last_num,last_dot)
##                              return mid_
                        last_num=mid_
                else:
                              if x==0:return 0
                              return mid_
        return round(x)

