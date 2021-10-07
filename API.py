import sys,time,sys,datetime,re,os,threading

import DataUse

def Merchandize_YMD_toCode(yymm):#特定有年月參數的商品代碼
    # yymm==202108 若為台指期 就會生成 TXFH1 
    yymm=str(yymm)
    mm_list=['','A','B','C','D','E','F','G','H','I','J','K','L']
    mm=mm_list[int(yymm[4:])]
    Tailcode=mm+str(yymm[3])
    return Tailcode
class TempData:
    # 暫時取用性資料
    def __init__(self):
        self.widget=''# 用以串接特定TK WIDGET
        self.write=0 # 1:在串流同時記錄下來
        if self.write:
            print("★ Ticks 串流中紀錄開啟並存成文本")
        self.topic=''
        self.sub_ver={}# 商品串流使用的版本
        self.bid_dict={}# 存放BIDASK資料
        self.tic_dict={}# 存放TICK 串流資料
        self.PLOTCODE={}# 根據CODE 提供QUOTE

    def _SaveBidask_2file(self,code,content):# 大量RUN DICT 而存放
        # content: [list]
        Folder=r'D:\Stock\Securities\永豐盤中資料\\Bidask\\'
        today=datetime.datetime.today().strftime("%Y%m%d")
        eachfolder=Folder+str(code)
        if not os.path.isdir(eachfolder):os.mkdir(eachfolder)
        path= eachfolder+'\\'+today+'.txt'
        with open(path,'a+') as W:
                      for each in content: 
                          W.write(str(each))
                          W.write('\n')
    def _SaveTicks_2file(self,code,content):# 大量RUN DICT 而存放
        # content: [list]
        Folder=r'D:\Stock\Securities\永豐盤中資料\\Ticks\\'
        today=datetime.datetime.today().strftime("%Y%m%d")
        eachfolder=Folder+str(code)
        if not os.path.isdir(eachfolder):os.mkdir(eachfolder)
        path= eachfolder+'\\'+today+'.txt'
        with open(path,'a+') as W:
                      for each in content: 
                          W.write(str(each))
                          W.write('\n')                 
    def savedata_bid(self,quote,code,length2save=100):
##        code=quote['Code']
        
        if code not in self.bid_dict:
                 self.bid_dict[code]=[0,[]]
        self.bid_dict[code][1].append(quote)
        self.bid_dict[code][0]=(quote)
        if len(self.bid_dict[code][1])>=length2save:
            content=self.bid_dict[code][1][:length2save].copy()
            self._SaveBidask_2file(code,content)
            self.bid_dict[code][1]=self.bid_dict[code][1][length2save:]
    def savedata_tick(self,quote,code,length2save=100):
        # length2save 多少筆資料後開始儲存
##        code=quote['Code']
        if code not in self.tic_dict:
                 self.tic_dict[code]=[0,[]]
        self.tic_dict[code][1].append(quote)
        self.tic_dict[code][0]=(quote)
        if len(self.tic_dict[code][1])>=length2save:
            content=self.tic_dict[code][1][:length2save].copy()
            self._SaveTicks_2file(code,content)
            self.tic_dict[code][1]=self.tic_dict[code][1][length2save:]
    def quote_fut_1(self,exchange, tick):
        self.quote=tick
        self.tick=tick
        self.sub_ver[code]='1:tick'
    def quote_fut_2(self,exchange,  bidask):
        self.quote=quote
        self.bidask=bidask
        self.sub_ver[code]='1:bidask'
    def quote_2(self,topic,quote):
         
         try:code=quote['Code']
         except:
             code=re.findall('\/(\d+)',str(topic))
             if code:
                 code=str(code[0])
         self.quote=quote
         self.topic=topic
         self.code=code
         self.sub_ver[code]='0:tick'
         
         if self.PLOTCODE:
             if code in self.PLOTCODE:
                 plot_,code_,showlabel=self.PLOTCODE[code]
                 showlabel['text']='價格: '+str(float(quote['Close'][0]))
            
                 vol=int(quote['Volume'][0])
                 close=float(quote['Close'][0])
                 time__=datetime.datetime.strptime(quote['Time'],'%H:%M:%S.%f')
                 Time_split=(time__).strftime("%H:%M")
                 REF=plot_.plot.Stream.LastClose
                 if Time_split not in plot_.dict_:
                     plot_.dict_[Time_split]=0,0
                     try:
                         lastclose,lastvolsum=plot_.dict_[list(plot_.dict_[Time_split])[-1]]
                     
                         plot_.plot.Stream.RunWithTick(lastclose,lastvolsum)
                     except:pass
                 _,volsum=plot_.dict_[Time_split]
                 volsum+=vol
                 plot_.dict_[Time_split]=close,volsum
                 plot_.plot.Stream.UpdatePrice(close,volsum)# 當前更新
                 plot_.label_showtime['text']='Time :   '+str(time__.strftime("%H:%M:%S"))
                 LIST=[plot_.label_showPrice,plot_.label_showavgprice,plot_.label_showvol]
                 if float(close)<float(REF):
                     for eachlabel in LIST:
                         eachlabel['fg']=plot_.plot.Stream.GreenLineColor
                 elif float(close)>float(REF):
                     for eachlabel in LIST:
                         eachlabel['fg']=plot_.plot.Stream.RedLineColor
                 else:
                     for eachlabel in LIST:
                         eachlabel['fg']=plot_.plot.Stream.WhiteLineColor
                 plot_.label_showPrice['text']=close
                 plot_.label_showavgprice['text']=round(plot_.plot.Stream.avgprice[-1],2)
                 plot_.label_showvol['text']=plot_.plot.Stream.vollist[-1]
         if self.write:self.savedata_tick(quote,code)# 儲存資料
         else:
             if code not in self.tic_dict:
                 self.tic_dict[code]=[0,[]]
             
             self.tic_dict[code][0]=(quote) 
##         print(topic)
##        {'AmountSum': [0.0], 'Close': [132.5], 'Date': '2021/08/16', 'Simtrade': 1, 'TickType': [1], 'Time': '08:59:38.174362', 'VolSum': [0], 'Volume': [4456]}
##         self.open=float(quote.get('Open'))
##         self.time=quote.get('Time')
####         self.Avgprice=float(quote.get('Avgprice')[0])
####         self.high=float(quote.get('High')[0])
####         self.low=float(quote.get('Low')[0])
##         self.close=float(quote.get('Close')[0])
####         self.amount=float(quote.get('Amount')[0])
##         self.total_amount=float(quote.get('AmountSum')[0])
##         self.ticktype=int(quote.get('TickType')[0])
##         self.date=quote.get('Date')
##         self.volume=float(quote.get('Volume')[0])        
##         self.total_volume=float(quote.get('VolSum')[0])
##         self.TradeAskVolSum=quote.get('TradeAskVolSum')
##         self.TradeBidVolSum=quote.get('TradeBidVolSum')
         
    
    def quote_3(self,topic,quote):# UPDN 查看五檔
         try:code=quote['Code']
         except:
             code=re.findall('\/(\d+)',str(topic))
             if code:
                 code=str(code[0])
         self.quote=quote
         self.topic=topic
         self.code=code
         self.sub_ver[code]='0:bidask'
         
         if self.write:self.savedata_bid(quote,code)# 儲存資料
         else:
      
             if code not in self.bid_dict:
                 self.bid_dict[code]=[0,[]]
             self.bid_dict[code][0]=(quote)
##        {'AskPrice': [134.5, 135.0, 135.5, 136.0, 136.5], 'AskVolume': [2415, 3923, 1708, 2890, 1049], 'BidPrice': [134.0, 133.5, 133.0, 132.5, 132.0], 'BidVolume': [485, 2550, 1427, 1141, 1521], 'Date': '2021/08/16', 'Time': '09:31:15.839790'}
##
##         self.AskPrice=quote.get('AskPrice')[0] #賣價第一檔 /'AskPrice': [134.5, 135.0, 135.5, 136.0, 136.5]    SELL      
##         self.AskVolume=quote.get('AskVolume')[0]# [5, 28, 18, 41, 38]
####         self.AskVolSum=float(quote.get('AskVolSum'))
####         self.sell_price=float(quote.get('AskPrice')[0])
##         self.BidPrice =quote.get('BidPrice')[0]#  買價第一檔/ 'BidPrice': [134.0, 133.5, 133.0, 132.5, 132.0]
##         self.BidVolume =quote.get('BidVolume')[0]
####         self.BidVolSum =float(quote.get('BidVolSum'))
####         self.buy_price=float(quote.get('BidPrice')[0])
##         self.time=quote.get('Time')
         
    def quote_v1_tick(self,exchange, tick):# Tick Sj V1版本
         self.exchange=exchange
         self.tick=tick
         
         try:code=tick['code']
         except:
             return 
             code=re.findall('\/(\d+)',str(topic))
             if code:
                 code=str(code[0])
         self.code=code
         self.sub_ver[code]='1:tick'
         if self.write:self.savedata_tick(tick,code)# 儲存資料
         else:
             if code not in self.tic_dict:
                 self.tic_dict[code]=[0,[]]
             self.tic_dict[code][0]=(tick) 
         self.quote=tick
        
    def quote_v1_bidask(self,exchange,  bidask):# Bidask Sj V1版本
         self.exchange=exchange
         self.tick= bidask
         self.bidask=bidask
         tick= bidask
         try:code=tick['code']
         except:
             return 
             code=re.findall('\/(\d+)',str(topic))
             if code:
                 code=str(code[0])
         if self.write:self.savedata_bid(tick,code)# 儲存資料
         else:
      
             if code not in self.bid_dict:
                 self.bid_dict[code]=[0,[]]
             self.bid_dict[code][0]=(tick)
         self.quote=tick
         self.code=code
         self.sub_ver[code]='1:bidask'
class Initial:
    ##OTC_all=[i.replace('OTC','') for i int api.Contracts.Stocks.OTC.keys()] 純獲得代碼
    ##TSE_all=[i.replace('OTC','') for i int api.Contracts.Stocks.TSE.keys()]
    # 取得所有合約
    def getallcontract(self,exchange,list_,stock_fut_opt=0,_lite=0):
        _lite=self._lite
        # _lite 0: 不加入CONTRACT 資訊 1:加入CONTRACT資訊
##        stock_fut_opt  {0:stocks ,1:futures,2:options}
        if stock_fut_opt==0: 
            
            for i in  self.api.Contracts.Stocks[exchange]:
                if not _lite:list_.append(i)
                else:
                    list_.append((i.code,i.name,exchange))
        elif stock_fut_opt==1:
            for i in  self.api.Contracts.Futures.keys():
                for j in self.api.Contracts.Futures[i]:
                    if not _lite:list_.append(j)
                    else:
                        list_.append((j.code,j.name,exchange))
        elif stock_fut_opt==2:
            for i in  self.api.Contracts.Options.keys():
                for j in self.api.Contracts.Options[i]:
                    
                    if not _lite:list_.append(j)
                    else:
                        list_.append((j.code,j.name,exchange))
        elif stock_fut_opt==3:
            for i in  self.api.Contracts.Indexs.keys():
                for j in self.api.Contracts.Indexs[i]:
                    if not _lite:list_.append(j)
                    else:
                        list_.append((j.code,j.name,exchange))
        return list_
    def __init__(self,api,_lite):
        self._lite=_lite
        self.api=api
        self.TSE_all,self.OTC_all,self.Fut_all,self.Opt_all,self.OES_all,self.Indexs_all=[],[],[],[],[],[]
        self.TSE_all=self.getallcontract('TSE',self.TSE_all)
        self.OTC_all=self.getallcontract('OTC',self.OTC_all)
        self.OES_all=self.getallcontract('OES',self.OES_all)
        self.Fut_all=self.getallcontract('Futures',self.Fut_all,stock_fut_opt=1)
        self.Opt_all=self.getallcontract('Options',self.Opt_all,stock_fut_opt=2)
        self.Indexs_all=self.getallcontract('Indexs',self.Indexs_all,stock_fut_opt=3)
        
        MergeList_allcode=self.Indexs_all+self.TSE_all+self.OTC_all+self.OES_all+self.Fut_all+self.Opt_all
        self.dict_stock_name={}
  
        for eachcontract in MergeList_allcode:
            mergename=''
            if not _lite:
                if 'otc' in str(eachcontract.exchange).lower():
                    mergename='[上櫃OTC] '+eachcontract.name
                elif 'tse' in str(eachcontract.exchange).lower():
                    mergename='[上市TSE] '+eachcontract.name
                mergename=eachcontract.name
                
                self.dict_stock_name[eachcontract.code]=mergename,eachcontract
            else:
                self.dict_stock_name[eachcontract[0]]=eachcontract[1],eachcontract[2]
   
class API:
    def timestamp2datetime(self,timestamp, convert_to_local=False):
   
        if len(str(timestamp))>13:
           timestamp=float(  str(timestamp)[:10]+'.'+str(timestamp)[13:])
        if isinstance(timestamp, (int, float)):
            dt = datetime.datetime.utcfromtimestamp(timestamp)
     
        return dt
    def get_ticks(self,code,yymmdd,lastcount=''):# yymmdd=yyyy-mm-dd
        
        if len(str(yymmdd))==8 and str(yymmdd).isdigit():
            yymmdd=str(yymmdd)[:4]+'-'+str(yymmdd)[4:6]+'-'+str(yymmdd)[6:]
        if '-' not in str(yymmdd):
            raise ValueError("yymmdd need '-' Ex: 2020-01-01")
        contract=''
        if  isinstance(code,self.sj.contracts.Contract) :
                contract=code
        if  code and not contract:
                contract=self.GetContractFromCode(str(code))
        if lastcount:
            ticks = self.api.ticks(
                contract=contract, 
                date=yymmdd, 
                query_type=self.sj.constant.TicksQueryType.LastCount,
                last_cnt=lastcount
            )
        else:
            ticks=self.api.ticks(contract,yymmdd)
        return ticks
    def trans_tickdata(self,ticks): # 將TICKS資料轉換
        #ticks['ts'] = timestamp list
        # bid_price 買入價
        # ask_price 賣出價
        #
        endpoint=len(ticks['ts'])
        # Timestamp
        for i in range(0,endpoint):
            time_=str(ticks['ts'][i])[:10]#  utcfromtimestamp will get utc |if utc not +8 - 28800 seconds = 8hrs
            ms=str(ticks['ts'][i])[10:14]
            mergetime_stamp=float(time_+'.'+ms)
            data_time=datetime.datetime.utcfromtimestamp(mergetime_stamp)
    def SaveTickDataToTxt(self,ticks,path):
        with open(path,'w+') as W:
          for i in ticks:
              W.write(i[0])
              W.write(':')
              W.write(str(i[1]))
              W.write('\n')
    def GetAllCodeNowFromOhlc(self,Volset=0):# 從OHLC 取得大部分STOCK CODE
    ##    Volset 設定選入的股票需求一定的成交量
        PATH=r'D:\Stock\Securities\每日資料\20210817\20210817_OHLC.txt' 
        LIST=[]
        with open(PATH,'r') as OHLC:
            for i in OHLC:
                tmp=i.split(',')
                code=str(tmp[1])
                Vol=int(tmp[-1].strip())
                if Volset:
                    if Vol<Volset:continue
                if len(code)==4:
                    
                    if code in self.init_info.dict_stock_name:
                        NAME,CONTRACT=self.init_info.dict_stock_name[code]
                    else:
                        CONTRACT=self.GetContractFromCode(code)
                    if CONTRACT:
                        if re.findall("otc|tse",str(CONTRACT.symbol),re.IGNORECASE):
                            LIST.append(code)
        return LIST
    def get_tickdatafromtxt(self,file):
        
        with open (file,'r' ) as FF:
            Dict={}
            for i in FF:
                tmp=i.split(':')
                tmp2=tmp[1].split(',')
                tmp2[0]=tmp2[0].replace('[','').strip()
                tmp2[-1]=tmp2[-1].replace(']','').strip()
                Dict[str(tmp[0])]=tmp2
            return Dict
    def SaveCodeTicks(self,code,today=0,StartDay=''):
        Folderohlc=r'D:\Stock\Securities\每日資料\\'
        Folder=r'D:\Stock\Securities\Ticks\\'
        folder_each=Folder+str(code)
        yy_mm_dd=''
        if '-' in str(StartDay):
            tmp_=(StartDay.split('-'))
            StartDay=datetime.datetime(int(tmp_[0]),int(tmp_[1]),int(tmp_[2]))
        if not StartDay:   
             StartDay=datetime.datetime(2018,12,7)# 2018/12/7 才開始有資料可以擷取    
##        StartDay=datetime.datetime(2018,12,7)# 2018/12/7 才開始有資料可以擷取
        if not os.path.isdir(folder_each):
                os.mkdir(folder_each)
        if today:#只下載今日的TICK資料
        
                StartDay=datetime.datetime.today()
        if 1:
            
                
                yymmdd=StartDay.strftime('%Y%m%d')
                yy_mm_dd=StartDay.strftime('%Y-%m-%d')
                
                eachohlc=Folderohlc+str(yymmdd)+'\\'+yymmdd+'_OHLC.txt'
                savetickpath=folder_each+'\\'+str(yymmdd)+'.txt'
                ticks = self.api.ticks(self.api.Contracts.Stocks[str(code)], yy_mm_dd)
                if not ticks['ts']:
                    StartDay+=datetime.timedelta(days=1)
               
                SaveTickDataToTxt(ticks,savetickpath)
              
    def StoreCodeTicks(self,today=0,RunFromBack=0):# 將TICKS資料全部存下來# Historical Market Data
        # today: 1:只下載今天的
        #  RunFromBack:# 會從最後一個資料夾內的檔案日期開始,前面已經Run過就不跑了
        Folder=r'D:\Stock\Securities\Ticks\\'
        Folderohlc=r'D:\Stock\Securities\每日資料\\'
        LIST=GetAllCodeNowFromOhlc(Volset=0)# 成交量500以上才會列入考量
        for each in LIST:
            folder_each=Folder+str(each)
            
            StartDay=datetime.datetime(2018,12,7)# 2018/12/7 才開始有資料可以擷取
            if not os.path.isdir(folder_each):
                os.mkdir(folder_each)
            
            if today:#只下載今日的TICK資料
                StartDay=datetime.datetime.today()
                yymmdd=StartDay.strftime('%Y%m%d')
                yy_mm_dd=StartDay.strftime('%Y-%m-%d')
                eachohlc=Folderohlc+str(yymmdd)+'\\'+yymmdd+'_OHLC.txt'
                savetickpath=folder_each+'\\'+str(yymmdd)+'.txt'
                ticks = self.api.ticks(self.api.Contracts.Stocks[str(each)], yy_mm_dd)
                if not ticks['ts']:
                    StartDay+=datetime.timedelta(days=1)
                    continue
                SaveTickDataToTxt(ticks,savetickpath)
                continue
            if  RunFromBack:# 會從最後一個資料夾內的檔案日期開始,前面已經Run過就不跑了
              if os.listdir(folder_each):
                NowProcessDay=datetime.datetime.strptime(os.listdir(folder_each)[-1].replace('.txt',''),'%Y%m%d')# 會從最後一個資料夾內的檔案日期開始,前面已經Run過就不跑了
                if (NowProcessDay+datetime.timedelta(days=1)).date()>=datetime.datetime.today().date():continue
            while 1:
                
                if StartDay.date()>=datetime.datetime.today().date():
                    break
                ticks=''
                yymmdd=StartDay.strftime('%Y%m%d')
                yy_mm_dd=StartDay.strftime('%Y-%m-%d')
                eachohlc=Folderohlc+str(yymmdd)+'\\'+yymmdd+'_OHLC.txt'
                savetickpath=folder_each+'\\'+str(yymmdd)+'.txt'
                if StartDay.isoweekday()==6 or StartDay.isoweekday()==7 or not os.path.isfile(eachohlc) or os.path.isfile(savetickpath):
                    StartDay+=datetime.timedelta(days=1)
                    continue
                
                ticks = self.api.ticks(self.api.Contracts.Stocks[str(each)], yy_mm_dd)
                if not ticks['ts']:
                    StartDay+=datetime.timedelta(days=1)
                    continue
                SaveTickDataToTxt(ticks,savetickpath)
                StartDay+=datetime.timedelta(days=1)
                if StartDay.date()>=datetime.datetime.today().date():
                    break
                
    def __init__(self,_lite=0):
        import shioaji as sj
        from shioaji.data import Kbars
        self.rq_times=0
        self._lite=_lite
        self.sj=sj
        self.login_times=0
        self.api= sj.Shioaji()
        self.streaming_data={}# 以商品化分再以時間為單位的儲存之串流資料
        self.dict_stock_name={}
        self.kbar_dict={}# Today Bar 
    def Logout_api(self):
        self.api.logout()
    @property
    def isalive(self):# 查看API是否有持續在連線
        return self.UpdateFu()
    def Logout(self):
        self.api.logout()
    def ReStart(self):
        try:
            self.api.logout()
            self.api.logout()
            accounts = self.api.login(self.Pid_, self.Password,fetch_contract=False)
##            self.api.activate_ca(
##                ca_path=self.ca_path,
##                ca_passwd=self.ca_passwd,
##                person_id=self.person_id,
##            )
            self.UpdateAll()
##            login_state=self.Login_api(self.Pid_,self.Password,ca_path=self.ca_path,ca_passwd=self.ca_passwd,person_id=self.person_id)
            return 1
        except:
            return 0
    def Login_api(self,Pid_,Password,_lite=0,ca_path='',ca_passwd='',person_id='',fetch_contract=True):
        # _lite : 1:將需要耗費到的記憶體降到最低
        
        self.login_times+=1
        try:

            if not ca_path:
                ca_path=sys.path[0]# Default Ca Path
            start=time.time()

        ##            Pid_='Your PID'
        ##            Password='Your PASSWORD'
        ##            Usually ca_passwd=person_id
            if not ca_passwd:
                ca_passwd=Pid_
            if not person_id:
                person_id=Pid_
            accounts = self.api.login(Pid_, Password,fetch_contract=fetch_contract)
            self.api.activate_ca(
                ca_path=ca_path,
                ca_passwd=ca_passwd,
                person_id=person_id,
            )


           
            print('登入花費時間:',round(time.time()-start,2),' Secs')
            self.UpdateAll()   #優先載入持倉資訊
            if self.login_times==1:
                
                self.list_trade
                self.POS_data=self.Get_Position(account=0)
                self.Pid_=Pid_
                self.Password=Password
                self.ca_path=ca_path
                self.ca_passwd=ca_passwd
                self.person_id=person_id
                self.init_info=Initial(self.api,self._lite)
                self.dict_stock_name=self.init_info.dict_stock_name
                self.TickData=TempData()
            return 1
        except:
            return 0
    
    def UpdateFu(self):# 更新期貨帳戶
            try:
                self.api.update_status(self.api.futopt_account)
            except:
                return 0
            return 1
##            self.rq_times+=1
##            print(self.rq_times,'RQTIMES')
    def UpdateSt(self):# Update all account
        self.api.update_status(self.api.stock_account)
##        self.rq_times+=1
##        print(self.rq_times,'RQTIMES')
    def UpdateAll(self):# Update all account
##        self.rq_times+=1
##        print(self.rq_times,'RQTIMES')
        self.api.update_status(self.api.stock_account)
        self.api.update_status(self.api.futopt_account)
    @property
    def list_trade(self):# Get list of trade contract today
        return self.api.list_trades()
    # today profitloss
    def Today_profitloss(self):
        today=datetime.datetime.now().strftime("%Y-%m-%d")
        list_=self.api.list_profit_loss(self.api.stock_account,today,today)
        sum_pnl=0
        mymsg='今日已實現損益: \n'
        for i in list_:
            Contract=self.GetContractFromCode(i.code)
            pfloss=i.pnl
            pr_ratio=round(i.pr_ratio*100,2)# 報酬率
           
            mymsg_='{:<5}'.format(str(Contract.name))+'('+str(i.code)+') | 損益:'+'{:<8}'.format(str(pfloss))+'| 報酬率: {:<5}'.format(str(pr_ratio))+' %\n'
            mymsg+=mymsg_
            
                 
            sum_pnl+=pfloss
        
        print("總計: ",sum_pnl)
        mymsg_="\n總計: "+str(sum_pnl)+'\n--- --- --- --- --- --- ---\n'
        mymsg+=mymsg_

        return mymsg
   # 得到日K棒
    def get_day_kbars(self,contract,date):

        _BARS=self.api.kbars(contract, start=date, end=date)
        BARS={k:[] for k in _BARS.keys()}

        for idx in range(0,len(_BARS['ts'])):
            _time=datetime.datetime.utcfromtimestamp((int(str(_BARS['ts'][idx])[:10])))

            if  8<=_time.hour<14:
                    for each in _BARS.keys():
                            BARS[each].append(_BARS[each][idx])
        day_kbars={}
        day_kbars['Open']=BARS['Open'][0]
        day_kbars['High']=max(BARS['High'])
        day_kbars['Low']=min(BARS['Low'])
        day_kbars['Close']=BARS['Close'][-1]
        day_kbars['Volume']=sum(BARS['Volume'])
        return  day_kbars
     #today trade list
    def Today_trade_list(self,*args,action='',list_=[],code_pos={}):
        if 'buy' in str(args).lower():
            action='buy'
        elif 'sell' in str(args).lower():
            action='sell'
        self.UpdateAll()
        list_trade=self.api.list_trades()
        msg='\n今日買入:\n'
        BorS= ['現股買入 |','現股賣出 |']
        for each in list_trade:
            Nodeals=0
            if 'fill' in str(each.status.status).lower():# fill 分 ed/ing: 完全與非完全
                bs=0
                if list_:
                    if each.contract.code not in list_:continue# 要在清單內的CODE 才可以被列入
                if action:
                    if action not in str(each.order.action).lower():continue
                if 'sell' in str(each.order.action).lower():
                    bs=1
                    
                Contract=self.GetContractFromCode(each.contract.code)
                quantity=each.status.deal_quantity
                try:
                        dealprice=each.status.deals[0].price
                except:
                        
                        print('沒有 deals:\n',each,'\n\n')
                        dealprice=each.order.price
                        Nodeals=1
                        if code_pos:
                            dealprice=float(code_pos[each.contract.code][-2])
                            Nodeals=int(code_pos[each.contract.code][-1])
##                        continue
                if len(Contract.code)!=4:continue
                if Nodeals:
                    stamp_=each.status.order_datetime.strftime("%H:%M:%S")
                else:
                    stamp_=datetime.datetime.fromtimestamp(int(each.status.deals[0].ts)).strftime("%H:%M:%S")
                msg_=BorS[bs]+'{:<5}'.format(str(Contract.name))+'('+str(Contract.code)+') | 價格:'+'{:<8}'.format(str(dealprice))+'| 數量: {:<4}'.format(str(quantity))+'| 時間 : '+stamp_+' \n'
                msg+=msg_
                print(msg_)
        
        return msg
    def get_tse_tradeday(self,lastday=5):# 得前 lastday 天有交易的日期
        today=datetime.datetime.today().date()
        trade_day=[]
        while 1:
            today=today-datetime.timedelta(days=1)
            tks_=self.get_ticks('001',today.strftime("%Y-%m-%d"),lastcount=1)
            if tks_['ts']:
                trade_day.append(today)
            if len(trade_day)>=lastday:
                break
        return trade_day
    def readOhlc(self,N=5,class_='',startday='',directuse_ohlc=0,direct_use_index=0):# 往前找N天並返還每一天的DICT
        # directuse_ohlc=0  # 1 : 直接使用OHLC的資料作為MA驗證
        # direct_use_index=0# 1 : 直接使用INDEX資料作為驗證
        # startday : Default = today.date()
        # class_ = CLASS From Other Py Call
        dict_={}
        folder=r'D:\Stock\Securities\每日資料\\'
        today=datetime.datetime.now()#.strftime("%Y%m%d")
        # 若今天不是正常日
        temp=today
        temp0=today
        verify_list=[temp0]
        if startday:
            temp=startday.date()
        allcode=[]
        Find_=0
        useindex=0 # 由於INDEX時間更晚於OHLC的時間 判定為OHLC 失去資料 從INDEX著手
        while 1:# 先對 加權指數進行驗證 那些日子有實際交易
            temp0=temp0-datetime.timedelta(days=1)
            tks_=self.get_ticks('001',temp0.strftime("%Y-%m-%d"),lastcount=1)
            if tks_['ts']:
                verify_list.append(temp0)
            if len(verify_list)==N+2:# 多+一天驗證CLOSE BEFORE
                break
            # temp0= 最後一次交易的日子 應該要和N=1 的日子相同 
        if class_:
            class_.find_ohlc_times+=1# 超過N次就可以不用再RUN
        while 1:
            temp=temp-datetime.timedelta(days=1)
            ohlc_path=folder+temp.strftime("%Y%m%d")+'\\'+temp.strftime("%Y%m%d")+'_OHLC.txt'
            
            if os.path.isfile(ohlc_path):
                Find_+=1
                if Find_ not in  dict_:
                   dict_[Find_]={}
 
                if verify_list[Find_].date()!=temp.date():
                    print("★ OHLC 文件 有可能有遺漏或是 API 訊源出錯>> Find_:",Find_,verify_list[Find_].date(),temp.date())
                    if Find_!=0:
                        if temp>verify_list[Find_] :#
                            print("   OHLC 時間晚於 API INDEX")
                            
                        else:
                            print("   OHLC 時間早於 API INDEX")  
                            useindex=1
                            
                if useindex:
                    for ind_ in range(1,6):
                       
                       if  verify_list[ind_].date()==temp.date():
                           if ind_ not in dict_:
                               dict_[ind_]={}
                           with open(ohlc_path,'r') as OH:
                                for i in OH:
                                    temp_list_stock=i.split(',')
                                    dict_[ind_][str(temp_list_stock[1]).strip()]=float(temp_list_stock[2]),float(temp_list_stock[3]),float(temp_list_stock[4]),float(temp_list_stock[5]),int(temp_list_stock[-1]),float(temp_list_stock[6])
                                    if str(temp_list_stock[1]).strip() not in  allcode:
                                        allcode.append(str(temp_list_stock[1]).strip())
                           break
                else:
                    with open(ohlc_path,'r') as OH:
                        for i in OH:
                            temp_list_stock=i.split(',')
                            dict_[Find_][str(temp_list_stock[1]).strip()]=float(temp_list_stock[2]),float(temp_list_stock[3]),float(temp_list_stock[4]),float(temp_list_stock[5]),int(temp_list_stock[-1]),float(temp_list_stock[6])
                            
            if Find_==N:break
        requests_time=0
        Limit_Q_rate=400/5 # 300times/5 Secs
        
        if useindex:
            all_starttime=time.time()
            for lossday in range(1,N+1):
                if not dict_[lossday]:
                    DATATIME=verify_list[lossday].strftime("%Y-%m-%d")
                    start_time=time.time()
                    print("NOT Exist:",lossday,' -> ',DATATIME)
                    for eachcode in allcode:
                        
##                        self.get_ticks(str(eachcode),DATATIME,lastcount=1)
                        try:
                           Lastday_ticks=self.get_ticks(str(eachcode), verify_list[lossday+1].strftime("%Y-%m-%d"),lastcount=1)
                           last_close=Lastday_ticks['close'][0]
                        except:continue
                        Contract=self.GetContractFromCode(str(eachcode))
                        try:BARS=self.api.kbars(Contract, start=DATATIME, end=DATATIME)
                        except:continue
                        if BARS['Open']:
                            
                            Open=BARS['Open'][0]
                            High=max(BARS['High'])
                            Low=min(BARS['Low'])
                            Close=BARS['Close'][-1]
                            Volume=sum(BARS['Volume'])
                            ChangeRate=(Close-last_close)*100/last_close
                            
                            dict_[lossday][str(eachcode)]=Open,High,Low,Close,Volume,ChangeRate
                        requests_time+=2
                        if (requests_time/float(time.time()-start_time))>=Limit_Q_rate:
                            time.sleep(5)
                    threading.Thread(target=self._ReBuildOhlc,args=(dict_[lossday],verify_list[lossday],folder,)).start()
                        
           
            print("USE INDEX SPENDTIME:",time.time()-all_starttime)
        return dict_
    def _ReBuildOhlc(self,dict_,date,folder):
        _folder=folder+date.strftime("%Y%m%d")
        if not os.path.isdir(_folder):os.mkdir(_folder)
        ohlc_path=folder+date.strftime("%Y%m%d")+'\\'+date.strftime("%Y%m%d")+'_OHLC.txt'
        TIME=date.strftime("%Y%m%d")
        with open(ohlc_path,'a+') as OH:
            for code in dict_:
                O,H,L,C,Vol,ChangeRATE=dict_[code]
                try:
                   Changepoint=round(float(C)/(1+(float(ChangeRATE)/100)),2)
                except:
                   Changepoint=-100
                OH.write(str(TIME))
                OH.write(',')
                OH.write(str(code))
                OH.write(',')
                OH.write(str(O))
                OH.write(',')
                OH.write(str(H))
                OH.write(',')
                OH.write(str(L))
                OH.write(',')
                OH.write(str(C))
                OH.write(',')
                OH.write(str(ChangeRATE))
                OH.write(',')
                OH.write(',')
                OH.write(',')
                OH.write(str(Changepoint))
                OH.write(',')
                OH.write(str(Vol))
                OH.write('\n')

    
    def kbars_today(self,Code):
      
        Contract=self.GetContractFromCode(Code)
        if not Contract:return
        Today=str(datetime.datetime.today().date())
        
        if Contract.code not in self.kbar_dict:
            self.kbar_dict[Contract.code ]={}
        tmp=self.api.kbars(Contract, start=Today, end=Today)
        my_tmp={}
        for i in range(0,len(tmp['ts'])):
            time_=(datetime.datetime.utcfromtimestamp(int(str(tmp['ts'][i])[:10]))-datetime.timedelta(minutes=1)).strftime("%H:%M")
           
            self.kbar_dict[Contract.code][time_]=tmp['Open'][i],tmp['High'][i],tmp['Low'][i],tmp['Close'][i],tmp['Volume'][i]

    def quick_scanner(self,only=0):
        c_list=[]  
##        s=time.time()
        TSE,OTC=[],[]
        TSE=[ i.code for i in self.api.Contracts.Stocks['TSE']  if len(str(i.code))==4]
        OTC=[ i.code for i in self.api.Contracts.Stocks['OTC']  if len(str(i.code))==4]
##        TSE=[i.code for i in self.init_info.TSE_all if len(str(i.code))==4]
##        OTC=[i.code for i in self.init_info.OTC_all if len(str(i.code))==4]
        if only==1:
            list_=TSE
        elif only==2:
            list_=OTC
        else:
            list_=TSE+OTC
        for i in list_: #list=os.listdir('日線')# Stock Contract
                
                ax=self.api.Contracts.Stocks[i]
                if (ax) is None:continue
                if str(datetime.datetime.now().strftime("%Y/%m/%d"))!=str(ax.update_date):continue
                if len(str(ax))<10:continue
                c_list.append(ax)
##        for j in Dict_index_TW:
##            symbol,name=Dict_index_TW[j]
##            INDEXCONTRACT=self.api.Contracts.Indexs[symbol[:3]][symbol[3:]]
##            if INDEXCONTRACT: # api.Contracts.Indexs['TSE']['005']
##               c_list.append(INDEXCONTRACT)
        self.quick_sc=self.api.snapshots(c_list)
        return self.quick_sc
    def Scanner_2(self,market=''): # filter_{0:TSE ,1:OTC ,2:OSE, 3:FUT,4:OPT# 通常比較久
        c_list=[]  
        s=time.time()
        MergeList_allcode=self.TSE_all+self.OTC_all+self.OES_all+self.Fut_all+self.Opt_all
        list_=MergeList_allcode
        try:
         if str(market).isdigit():
             list_=MergeList_allcode[market]
        except:return
##        for i in list_: #list=os.listdir('日線')# Stock Contract
##                
##         
##                if str(datetime.datetime.now().strftime("%Y/%m/%d"))!=str(i.update_date):continue
##                if len(str(i))<10:continue
##                c_list.append(i)
       
        
        self.all_snap=api.snapshots(list_)
   #
    def Settlement(self):# 查詢交割訊息
        return self.api.list_settlements()[0]
##    self.api.list_settlements()[0].t1_money= T1日 的交割金額 / 今天之後的第一個交易日交割金額
##    self.api.list_settlements()[0].t_day  = T1日 的交割日期

   #查詢股票帳務損益
    def PL_stock(self,today=0,date_start='',date_end=''): # date_start('2020-05-05')/ date_end('2020-05-30')
        if today:
            date_start=str(datetime.datetime.today().date())
            date_end=date_start
        
        return self.api.list_profit_loss(self.api.stock_account,date_start,date_end)
    def Get_Position(self,account=1,query_type='0'):# Default Stock Ware
        '''
          account ={0:all ,1:stock ,2:future}
        '''
        #  query_type: {0, 1}  Only for futopt account
##            query return with detail or summary
##            - 0: detail
##            - 1: summary
        
        if account==2:
            position=self.api.get_account_openposition(account=self.api.futopt_account)
            self._futopt_position=position.data()
            return self._futopt_position
        elif account==1: # Default=Stock 
            
            position=self.api.list_positions(account=self.api.stock_account) #
            self._stock_position=position
            return self._stock_position
        else:
            position=self.api.get_account_openposition(account=self.api.futopt_account)
            self._futopt_position=position.data()
            position=self.api.list_positions(account=self.api.stock_account) #
            self._stock_position=position
            return self._stock_position+self._futopt_position
    @property
    def stock_position(self):
        return self.Get_Position(account=1)
    @property
    def futopt_position(self):
        return self.Get_Position(account=2)
    def GetAveragePriceFromOrderno(self,Orderno,stock_account=0,futopt_account=0):
        # 從既有的Orderno/Code獲取相關 當時下單之資訊 找出對應合約之均價 返還dict
        # Return AveragePrice/ DictPos / Contract
        if stock_account:
            Posdata=self.stock_position
        elif futopt_account:
            Posdata=self.futopt_position
        if not Posdata:
            return 0 # 無任何庫存
        for each in Posdata:
            if str(Orderno)==str(each['OrderNum']):
                return each['ContractAverPrice'],each,self.GetContractFromCode(each['Code'])
        return 0 # 找不到Ordeno 對應之合約
    def GetContractFromOrderno(self,Orderno):# 從既有的Orderno/Code獲取相關 當時下單之資訊 找出對應合約
        # 若找不到 Orderno 就使用當初紀錄的Code> Use GetContractFromCode(Code)
        Posdata=self.Get_Position(account=0)
        self.POS_data=Posdata
       
        for each in Posdata:
            
            if str(Orderno)== str(each['OrderNum']):
                return self.GetContractFromCode(each['Code'])
        return 0 #找不到Ordeno 對應之合約
    def Contract_name(self,Contract):# 將不同商品的名字組合/  股票維持不變 / 期貨要加入月份
        if Contract:
                    name=Contract.name
                    if isinstance(Contract,self.api.sj.Contracts.Future):# 期貨
                        name=Contract.name+Contract.delivery_month
                    elif isinstance(Contract,self.api.sj.Contracts.Option):
                        extra_name=''
                        find_w=re.findall('[0-9]',Contract.code[:3])
                        if find_w:#代表周選
                            extra_name='W'+find_w[0]
                        symbol=Contract.symbol[-7:]
                        if Contract.symbol[-7:-6]=='0':
                            symbol= Contract.symbol[-6:]
                        name=Contract.name[:3]+extra_name+' '+Contract.delivery_month[-2:]+' '+symbol
                    return name
    def GetContractFromCode(self,Code,Market=''):
        """query Account ContractFromCode
        Args:
            Market=[stocks,futures(txf),option]
        """
        Code=str(Code)
        if '7799' in str(Code):
            Code=self.Get_Nearmonth("TXF")
           
        
        try:
         if re.findall('txf|mxf',str(Code).lower()) and Code.upper() not in self.dict_stock_name :
            if 'txf' in str(Code).lower():
                code_front='txf'
            else:
                code_front='mxf'
            code_tmp=str(Code).lower().replace(code_front,'')
            tailcode=Merchandize_YMD_toCode(code_tmp)
            if 'txf' in str(Code).lower():
                Code='TXF'+tailcode
            else:
                Code='MXF'+tailcode
        except:pass
        if Code.upper() in self.dict_stock_name:
            if not self._lite:
                Name,Contract=self.dict_stock_name[Code.upper()]
                return Contract
            elif self._lite:
                Name,exchange=self.dict_stock_name[Code.upper()]
                if re.findall("OTC|OES|TSE",exchange,re.IGNORECASE):
                    exchange='Stocks'
                    return self.api.Contract[exchange][Code.upper()]
                 
                
        if len(str(Code))<=4:#通常為STOCKS
            
            if str(Code).isdigit():
                Market='stocks'
        
        if 'stock' in str(Market).lower():
            return self.api.Contracts.Stocks[Code]
        elif 'txf' in str(Market).lower() or 'future' in str(Market).lower() or 'txf' in str(Code).lower() :
            Contract=self.api.Contracts.Futures[Code.upper()]
            if 'StreamMultiContract' in str(type(Contract)):return
            return Contract
        elif 'option' in str(Market).lower() or 'txo' in str(Market).lower() or re.findall('tx[0-9]{1}|txo',Code.lower()):
            Contract=self.api.Contracts.Options[Code.upper()]
            if 'StreamMultiContract' in str(type(Contract)):return
            return Contract
        else:
            Contract=self.api.Contracts.Futures[Code.upper()]
            if 'StreamMultiContract' in str(type(Contract)):return
            return Contract
        # Market
        # options
        # futures
        # stocks
   # Sum of all position pnl of stock
    def Sum_pnl(self):
        pos=self.Get_Position()
        sum_pnl=0
        for i in pos:
            sum_pnl+=i.pnl
        return sum_pnl
    # get now price(close) of code list
    def getprice(self,list_): # list_= numeric code 
        tmp=[]
        for i in list_:
            Contract=self.GetContractFromCode(i)
            tmp.append(Contract)
        tmp2=api.snapshots(tmp)
        for j in tmp2:
            stamp_=datetime.datetime.utcfromtimestamp(float(str(j.ts)[:10]+'.'+str(j.ts)[10:13]))
            print(stamp_.strftime("%Y/%m/%d %H:%M:%S"),' | ',j.code,' | close :',j.close)
        
    def snap(self,contract,code=''): # Snap merchandise
        if not isinstance(contract,self.sj.contracts.Contract) :# sj.contracts.Contract = All type of Contract
            code=contract
        if code:
            contract=self.GetContractFromCode(str(code))
        try:
                if isinstance(contract,list):
                     return contract,self.api.snapshots(contract)[0]
                else:
                     return contract,self.api.snapshots([contract])[0]
        except: return 0,0
    def _FUT_MarginCheck(self):# 期貨戶保證金查詢
            account_margin = self.api.get_account_margin()
            ProfitAccCount=account_margin.data()[0]['ProfitAccCount']  # 返還台幣幣值
            self._margin=ProfitAccCount
            return ProfitAccCount
    @property
    def futopt_margin(self):  # for futopt account
        return self._FUT_MarginCheck()
    @property
    def stock_balance(self):
        return self.api.account_balance()[0].acc_balance
    def CancelPO(self,ORDER):# Cancel Submitted PlaceOrder which not Filled
##            self.UpdateAll()
            self.api.cancel_order(ORDER)
            time.sleep(0.6)
            self.UpdateAll()
            return ORDER
    def PlaceOrder(self,Contract,price=1,quantity=1,BS='Buy',price_type='LMT'
                   ,order_type='ROD',octype='Auto',account='',
                   first_sell='',order_cond ='',
                   order_lot ="Common"):
        ##    訂單生成且交易
        ##    order_type={ROD, IOC, FOK} ROD:當日有效 IOC:部分成交其餘取消 FOK:全部成交否取消
        ##    price_type={LMT, MKT, MKP} MKP:範圍市價 MKT:市價 LMT:限價
        ##    PendingSubmit: 傳送中 # 取消也會是這樣/self.api.update_status(self.api.futopt_account)才會更新
        ##    PreSubmitted: 預約單
        ##    Submitted:    傳送成功
        ##    Failed:       失敗
        ##    Cancelled:    已刪除
        ##    Filled:       完全成交
        ##    Filling:      部分成交

        # order_lot # 盤後要選 Fixing
##    {Common, Fixing, Odd, IntradayOdd} (整股、定盤、盤後零股、盤中零股)
        order=''
        FUTURE=0
    
            
        if 'TAIFEX' in str(Contract.exchange).upper():# 期貨交易所
            account=self.api.futopt_account
            FUTURE=1
            try:
                          order = self.api.Order(action=BS,
                                  price=price,
                                  quantity=quantity,
                                  price_type=price_type,
                                  order_type=order_type,
                                  octype=self.sj.constant.FuturesOCType[octype],
                                  account=account)
            except:
                    return 0
            if order:
                    trade = self.api.place_order(Contract, order)
                    return trade
        else:
            account=self.api.stock_account
            
            try:
                if first_sell:
                    
                          order = self.api.Order(
                                  action=BS,
                                  price=price,
                                  quantity=quantity,
                                  price_type=price_type,
                                  order_type=order_type,
                                  order_lot=order_lot,
                                  first_sell=self.sj.constant.StockFirstSell.Yes,
                                  account=account)
                else:
                    
                          order = self.api.Order(
                                  action=BS,
                                  price=price,
                                  quantity=quantity,
                                  price_type=price_type,
                                  order_type=order_type,
                                  order_lot=order_lot, 
                                  account=account)
            except:
                    return 0
            if order:
                    trade = self.api.place_order(Contract, order)
                    return trade
##price (float or int): the price of order
##quantity (int): the quantity of order
##action (str): order action to buy or sell
##    {Buy, Sell}
##price_type (str): pricing type of order
##    {LMT, MKT, MKP}
##order_type (str): the type of order
##    {ROD, IOC, FOK}
##order_cond (str): order condition stock only
##    {Cash, MarginTrading, ShortSelling} (現股、融資、融券)
##order_lot (str): the type of order
##    {Common, Fixing, Odd, IntradayOdd} (整股、定盤、盤後零股、盤中零股)
##first_sell {str}: the type of first sell
##    {true, false}
##account (:obj:Account): which account to place this order
##ca (binary): the ca of this order
    def Streaming_Newest_Futures(self): # TXF=> TXF202011 [TXF+Year+Month] 取用方式2
            #取得最新台指及時串流資料      >>>>  Streaming_Futures( Get_Nearmonth_TXF())
       code= self.Get_Nearmonth_TXF()
      
       self.api.quote.subscribe(self.api.Contracts.Futures.TXF[code], quote_type='tick')
    def Get_Nearmonth(self,NXF):# 獲得 各種期貨的近期合約
        list_ym=[]
        NXF=NXF.upper()
        today=datetime.datetime.now()
        for i in self.api.Contracts.Futures[NXF]:
                if i['delivery_month'] not in list_ym:
                 list_ym.append(i['delivery_month'])
        nearmonth=sorted(list_ym)[0]
        
        yy=int(nearmonth[:4])
        mm=int(nearmonth[4:6])
        
        OCD_string,Out_of_contracct_day=DataUse.get_weektimes(yy,mm,3,3)#第一個三= 第幾個禮拜幾 第二個三為星期 > 每個月的第三個禮拜三|為結算日  # 往後還有假日問題
       
        if Out_of_contracct_day<today:
            nearmonth=sorted(list_ym)[1]
            
        return NXF+nearmonth   
    def Get_Nearmonth_TXF(self):
        list_ym=[]
        today=datetime.datetime.now()
        for i in self.api.Contracts.Futures.TXF:
                if i['delivery_month'] not in list_ym:
                 list_ym.append(i['delivery_month'])
        nearmonth=sorted(list_ym)[0]
        print(nearmonth)
        yy=int(nearmonth[:4])
        mm=int(nearmonth[4:6])
        
        OCD_string,Out_of_contracct_day=DataUse.get_weektimes(yy,mm,3,3)#第一個三= 第幾個禮拜幾 第二個三為星期 > 每個月的第三個禮拜三|為結算日  # 往後還有假日問題
       
        if Out_of_contracct_day<today:
            nearmonth=sorted(list_ym)[1]
            
        return "TXF"+nearmonth
    def Streaming_TXF_Futures(self,code): # TXF=> TXF202011 [TXF+Year+Month] 取用方式2
        #取得台指及時串流資料      >>>>  Streaming_TXF_Futures( Get_Nearmonth_TXF())
        
           self.api.quote.subscribe(self.api.Contracts.Futures.TXF[code], quote_type='tick')
           self.api.quote.set_quote_callback(self.quote_)   
    def quote_(topic,quote):
          
             day_string=datetime.datetime.today().strftime('%Y%m%d')
             yy=datetime.datetime.today().year
             mm=datetime.datetime.today().month
             dd=datetime.datetime.today().day
             
             Open=quote.get('Open')
             Time_=quote.get('Time')
             price=quote.get('Close')
             Amount=quote.get('Amount')
             AmountSum=quote.get('AmountSum')
             Date=quote.get('Date')
             Volume=quote.get('Volume')
             VolSum=quote.get('VolSum')
             High=quote.get('High')
             Low=quote.get('Low')
             TradeAskVolSum=quote.get('TradeAskVolSum')
             TradeBidVolSum=quote.get('TradeBidVolSum')
             TickType=quote.get('TickType')#  {1: deal of buy, 2: deal of sell, 0: can't judge}
             
             dict_now_txo[Time_]=Open,price[0],High[0],Low[0],Volume[0],VolSum[0],TickType[0],TradeAskVolSum,TradeBidVolSum
             STREAM.Stream_dict(dict_now_txo)
             year_=datetime.datetime.now().year
             month_=datetime.datetime.now().month
             day_=datetime.datetime.now().day
             hh=datetime.datetime.now().hour
             mm=datetime.datetime.now().minute
    def Streaming_stock(self,code,*args,quote_type='tick',intraday_odd =0):
         if 'bidask' in str(args).lower():
             quote_type='bidask'
         elif 'tick' in str(args).lower():
             quote_type='tick' 
         contract=self.GetContractFromCode(str(code))
         if intraday_odd:# 零股
             self.api.quote.subscribe(contract, quote_type=quote_type,intraday_odd = True)
             self.api.quote.set_quote_callback(quote_stock)
         else:
             self.api.quote.subscribe(contract, quote_type=quote_type)
             self.api.quote.set_quote_callback(quote_stock)
    def Streaming_stock_v0(self,code,*args,quote_type='tick',intraday_odd =0,widget=''):# 透過新的容器來儲存TICK資料
        # quote_type =['tick','bidsak']
        # widget = For Class widget use
         if 'bidask' in str(args).lower():
             quote_type='bidask'
         elif 'tick' in str(args).lower():
             quote_type='tick'
         contract=self.GetContractFromCode(str(code))
         if widget:
             self.TickData.widget=widget
##         content=TempData(self,code,widget=widget)
         if intraday_odd:# 零股
             self.api.quote.subscribe(contract, quote_type=quote_type,intraday_odd = True)
            
         else:
             self.api.quote.subscribe(contract, quote_type=quote_type)
         if re.findall('tick',str(quote_type),re.IGNORECASE):
             self.api.quote.set_quote_callback(self.TickData.quote_2)
         else:
             self.api.quote.set_quote_callback(self.TickData.quote_3)
         return 1
##    def Streaming_stock_v3(self,code,quote_type='bidask'):# 透過新的容器來儲存TICK資料(5檔)
##       
##         
##         contract=self.GetContractFromCode(str(code))
##         content=TempData(self,code)
##         self.api.quote.subscribe(contract, quote_type=quote_type)
##         self.api.quote.set_quote_callback(content.quote_3)
##         return content
    def Streaming_v1(self,code,*args,quote_type='tick',intraday_odd =0,widget=''):# 透過新版本SJ 儲存TICK/Bidask 資料(5檔)
         # 需要更新Sj版本才可以使用# for future and stock
         if 'bidask' in str(args).lower():
             quote_type='bidask'
         elif 'tick' in str(args).lower():
             quote_type='tick'
         contract=self.GetContractFromCode(str(code))
         if re.findall('tick',str(quote_type),re.IGNORECASE):
             if isinstance(contract,self.sj.contracts.Stock):
                 self.api.quote.set_on_tick_stk_v1_callback(self.TickData.quote_v1_tick)# for stock
             else:
                 self.api.quote.set_on_tick_fop_v1_callback(self.TickData.quote_v1_tick)# for index
         
         else:
             if isinstance(contract,self.sj.contracts.Stock):
                 self.api.quote.set_on_bidask_stk_v1_callback(self.TickData.quote_v1_bidask)
             else:
                 self.api.quote.set_on_tick_fop_v1_callback(self.TickData.quote_v1_tick)# for index
##         content=TempData(api,code)
         if intraday_odd:# 零股
             self.api.quote.subscribe(contract, quote_type=quote_type,intraday_odd = True, version = self.sj.constant.QuoteVersion.v1)
            
         else:
             self.api.quote.subscribe(contract, quote_type=quote_type, version = self.sj.constant.QuoteVersion.v1)
         
         return 1
    def Streaming_stock_v1(self,code,*args,quote_type='tick',intraday_odd =0,widget=''):# 透過新版本SJ 儲存TICK/Bidask 資料(5檔)
         # 需要更新Sj版本才可以使用
         if 'bidask' in str(args).lower():
             quote_type='bidask'
         elif 'tick' in str(args).lower():
             quote_type='tick'
         contract=self.GetContractFromCode(str(code))
##         content=TempData(self,code,widget=widget)
         if intraday_odd:# 零股
             self.api.quote.subscribe(contract, quote_type=quote_type,intraday_odd = True, version = self.sj.constant.QuoteVersion.v1)
            
         else:
             self.api.quote.subscribe(contract, quote_type=quote_type, version = self.sj.constant.QuoteVersion.v1)
         if re.findall('tick',str(quote_type),re.IGNORECASE):
             
             self.api.quote.set_on_tick_stk_v1_callback(self.TickData.quote_v1_tick)
         else:
             self.api.quote.set_on_bidask_stk_v1_callback(self.TickData.quote_v1_bidask)
         return 1
    def Streaming_Futures_v1(self,code,*args,quote_type='tick'): # TXF=> TXF202011 [TXF+Year+Month] 取用方式2
        #取得台指及時串流資料      >>>>  Streaming_Futures( Get_Nearmonth_TXF())
##         content=TempData(api,code)
         if 'bidask' in str(args).lower():
             quote_type='bidask'
         elif 'tick' in str(args).lower():
             quote_type='tick'
         self.api.quote.subscribe(api.Contracts.Futures.TXF[code], quote_type=quote_type,version = self.sj.constant.QuoteVersion.v1)

         if re.findall('tick',str(quote_type),re.IGNORECASE):
             self.api.quote.set_on_tick_stk_v1_callback(TickData.quote_fut_1)
         else:
             self.api.quote.set_on_bidask_stk_v1_callback(TickData.quote_fut_2)
         return contents
    def Unsubscribe(self,code,ver=0):
                 contract=self.GetContractFromCode(str(code))
                 if ver:
                        self.api.quote.unsubscribe(contract, quote_type='tick', version =  self.sj.constant.QuoteVersion.v1)
                        self.api.quote.unsubscribe(contract, quote_type='bidask', version = self.sj.constant.QuoteVersion.v1)
                 else:
                     self.api.quote.unsubscribe(contract,quote_type='tick')
                     self.api.quote.unsubscribe(contract,quote_type='bidask')
    def Stop_Streaming_stock(self,code,ver=0):
                 contract=self.GetContractFromCode(str(code))
                 if ver:
                        self.api.quote.unsubscribe(contract, quote_type='tick', version =  self.sj.constant.QuoteVersion.v1)
                        self.api.quote.unsubscribe(contract, quote_type='bidask', version = self.sj.constant.QuoteVersion.v1)
                 else:
                     self.api.quote.unsubscribe(contract,quote_type='tick')
                     self.api.quote.unsubscribe(contract,quote_type='bidask')
    def quote_stock(self,topic,quote):
         
            
        
           #QUOTE= {'Amount': [16120.0], 'AmountSum': [1317378969.0], 'AvgPrice': [16029.823309], 'Close': [16120.0], 'Code': 'TXFD1', 'Date': '2021/03/22', 'DiffPrice': [110.0], 'DiffRate': [0.687071], 'DiffType': [2], 'High': [16142.0], 'Low': [15911.0], 'Open': 16018.0, 'TargetKindPrice': 16144.78, 'TickType': [2], 'Time': '10:31:05.788000', 'TradeAskVolSum': 51356, 'TradeBidVolSum': 49661, 'VolSum': [82183], 'Volume': [1]}
             # {'AmountSum': [614968050.0], 'Close': [35.2], 'Date': '2021/03/25', 'TickType': [1], 'Time': '13:23:01.328723', 'VolSum': [16507], 'Volume': [4]}

             
             Code=quote.get('Code')
             Time_=quote.get('Time')
             price=quote.get('Close')
             Amount=quote.get('Amount')
             AmountSum=quote.get('AmountSum')
             Avgprice=quote.get('AvgPrice')
             Date=quote.get('Date')
             Volume=quote.get('Volume')
##             if Code not in streaming_data:
##                 self.streaming_data[Code]=[]
##             self.streaming_data[Code].append((Time_,price,Volume,Amount,AmountSum,Avgprice,Date))   
    def snap2(self,contract):# 透過串流資料生成Snap
        if len(str(contract))==4:
            contract=self.snap(contract)
        tmp_=''

##        tmp_=TempData(contract.code)
        
        self.api.quote.subscribe(contract)
        self.api.quote.set_quote_callback(self.TickData.quote_2)
        
        while 1:
          time.sleep(1)
          if tmp_.close:
            self.api.quote.unsubscribe(contract)
            return 1
    def snap3(self,contract):# 透過串流資料生成Snap
            if len(str(contract))==4:
                contract=snap(contract)
            tmp_=''
            
##            tmp_=TempData(contract.code)
            
            self.api.quote.subscribe(contract, quote_type=self.sj.constant.QuoteType.BidAsk)
            self.api.quote.set_quote_callback(self.TickData.quote_3)
            time_wait=time.time()
            while 1:
              
              if tmp_.quote:
                self.api.quote.unsubscribe(contract, quote_type=self.sj.constant.QuoteType.BidAsk)
                return tmp_        

def DetectConnect(API):
    while 1:
      try:  
        
                timenow=datetime.datetime.now()
                
                if not API.isalive:
                                 print(timenow.strftime("%y-%m-%d %H:%M:%S"),"API 斷線, 嘗試重新連線...")
                                 try:
                                   
                                    API.Logout_api()# 完全斷線
                                    time.sleep(3)
                                 except:pass
                                 
                                 while 1:#直到登入才能進行退出
                                      Loginstate=API.ReStart()
                                      if Loginstate:break
                                      else:
                                          print(timenow.strftime("%y-%m-%d %H:%M:%S")," API 重連出錯, 嘗試再度連線...")
                                          time.sleep(5)
                                 time.sleep(120)
                time.sleep(30)# 每20秒偵測連線狀態       
      except Exception as ERROR:
          print(ERROR)



