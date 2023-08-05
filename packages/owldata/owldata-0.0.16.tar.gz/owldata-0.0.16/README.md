![](https://owl.cmoney.com.tw/Owl/resources/images/logo.png)

---

# OwlData 數據貓頭鷹 API

數據貓頭鷹官方網站: https://owl.cmoney.com.tw/Owl/

--------

## Outline

- [OwlData 數據貓頭鷹 API](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)
  - [Outline](#outline)
  - [Dependencies](#dependencies)
  - [Install](#install)
  - [HTTP Authentication](#http-authentication)
    - [Flow Control](#flow-control)
    - [Code Example](#code-example)
  - [Quick Start](#quick-start)
  - [Data Function](#data-function)
  - [Contribute](#contribute)
  
## Dependencies

- pandas
- requests

## Install

安裝資源可以詳見 Github at https://github.com/owldb168/owldata

By PyPI

``` python
pip install owldata
```

Install source from GitHub

``` sh
git clone https://github.com/owldb168/owldata.git
cd owldata
python setup.py install
```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## HTTP Authentication

&nbsp;&nbsp;&nbsp;&nbsp;介接端須先透過取得的應用程式編號與應用程式密鑰取得一次性的有效交易驗證碼，於每次API呼叫時帶入 HTTP HEADER 提供驗證才能使用相關API。此驗證碼於特定時間後會 timeout過期，此時必須重新取得交易驗證碼得以再次操作相關API。

### Flow Control

![情境流程示意](https://owl.cmoney.com.tw/Owl/resources/images/img_api_01.png)

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

### Code Example

使用 OwlData 模組輸入 AppID 與應用程式密鑰進行登入，並呼叫欲查詢資料表

``` python
import owldata

# 輸入數據貓頭鷹會員 AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

# 引用函數取得資料
owlapp = owldata.OwlData(appid, appsecret)
```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## Quick Start

快速拿取個股歷史資料

``` python
import owldata

# 輸入數據貓頭鷹會員 AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

# 引用函數取得資料
owlapp = owldata.OwlData(appid, appsecret)

# 擷取台積電股價 from 2019/08/12 to 2019/08/13
stock_price = owlapp.ssp("2330", "20190812", "20190813")
stock_price.head()
```

## Data Function

OwlData 使用方法，使用 OwlData 不同方法擷取所需要的資料，並可以利用參數 colist 進行欄位篩選

1. 個股日收盤行情 (Single Stock Price, SSP)

    <br>依指定日期區間，撈取指定股票代號的股價資訊
    <br>

   ``` python
   OwlData.ssp(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
   ```

    <table>
    <tr>
        <td rowspan="4"><b>Parameters<b></td>
        <td> - <b> sid </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;股票代號
        </td>
    </tr>
    <tr>
        <td> - <b>  bpd </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> epd</b> : <i> string</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> colist</b> : <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>日期</td>
            <td>股票名稱</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>收盤價</td>
            <td>漲跌</td>
        </tr>
        <tr>
            <td>漲幅(%)</td>
            <td>成交量</td>
            <td>成交筆數</td>
            <td>成交金額(千)</td>
            <td>均張</td>
            <td>均價</td>
            <td>成交量(股)</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電股價 from 2019/08/12 to 2019/08/13
    >>> colist = ['日期', '股票名稱', '開盤價', '最高價', '最低價' , '收盤價', '漲跌', '漲幅(%)', '成交量']
    >>> owlapp.ssp("2330", "20190812", "20190813", colist)
    [out]

           日期   股票名稱	開盤價	最高價	最低價	收盤價	 漲跌	漲幅(%)	 成交量
    0    20190813  台積電	249.00	249.50	246.50	246.50	-4.50	-1.79	23121.00
    1    20190812  台積電	254.50	254.50	251.00	251.00	-2.50	-0.99	24732.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

2. 多股每日收盤行情 (Multi-Stock Price, MSP)

    <br>依指定日期，撈取全上市櫃台股的股價資訊
    <br>

    ``` python
    OwlData.msp(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
            </td>
        </tr>
            <tr>
                <td> - <b> colist </b>: 
                <i> list, default None</i>
                <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
                </td>
            </tr>
            <tr>
                <td><b> Returns</b></td><td>DataFrame or Series</td>
            </tr>
            <tr>
                <td colspan="2">
                <b> Note</b>
                <br>
                    &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
                </td>
            </tr>
    </table>

     - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>收盤價</td>
            <td>漲跌</td>
        </tr>
        <tr>
            <td>漲幅(%)</td>
            <td>成交量</td>
            <td>成交筆數</td>
            <td>成交金額(千)</td>
            <td>均張</td>
            <td>均價</td>
            <td>成交量(股)</td>
        </tr>
    </table>

     - 範例

    ``` python
    # 擷取台股上市上櫃  2019/08/01 所有盤後資訊
    >>> owlapp.msp("20190801")

    [out]
        股票代號 股票名稱    日期    開盤價  最高價  最低價  收盤價   漲跌   漲幅(%) 成交量    成交筆數   成交金額(千)  均張   均價   成交量(股)
    0     1101    台泥   20190801   44.50  44.55   44.00   44.05  -0.65  -1.45  33643.00  10943.00  1485589.00   3.10  44.16  33643219.00
    1     1102    亞泥   20190801   41.45  41.70   41.20   41.40  -0.40  -0.96   8384.00   4275.00   347479.00   2.00  41.44  8384463.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

3. 個股財務簡表 (Financial Statements Single, FIS)

    <br>依據 di 決定查詢資料頻率，並依股票代號，撈取指定區間的財務報表資訊
    <br>y(年)、 q(季) 是撈取財務報表資訊；m(月) 是撈取營收相關資訊

    ```python
    OwlData.fis(di:str, sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="5"><b>Parameters<b></td>
            <td> - <b> di </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
                <ul style="list-style-type:disc;">
                    <li>Y : 年度, 格式 : yyyy</li>
                    <li>Q : 季度, 格式 : yyyyqq</li>
                    <li>M : 月, 格式 : yyyymm</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td> - <b>  sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 參數 di 大小寫無異
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
        <td colspan="25">年與季財報欄位</td>
        </tr>
        <tr>
            <td>年度</td>
            <td>年季</td>
            <td>流動資產</td>
            <td>非流動資產</td>
            <td>資產總計</td>
            <td>流動負債</td>
            <td>非流動負債</td>
            <td>負債總計</td>
            <td>權益總計</td>
            <td>公告每股淨值</td>
        </tr>
        <tr>
            <td>營業收入(千)</td>
            <td>營業成本(千)</td>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
            <td>營業外收入及支出(千)</td>
            <td>稅前純益(千)</td>
            <td>所得稅(千)</td>
        </tr>
        <tr>
            <td>稅後純益歸屬(千)</td>
            <td>每股盈餘(元)</td>
            <td>營業活動現金流量(千)</td>
            <td>投資活動現金流量(千)</td>
            <td>籌資活動現金流量(千)</td>
            <td>本期現金及約當現金增減數(千)</td>
            <td>期末現金及約當現金餘額(千)</td>
            <td>自由現金流量(千)</td>
        </tr>
        <tr>
        <td colspan="25">月營收欄位</td>
        </tr>
        <tr>
            <td>年月</td>
            <td>單月合併營收(千)</td>
            <td>去年同期(千)</td>
            <td>單月合併營收年成長(%)</td>
            <td>單月合併營收月變動(%)</td>
            <td>累計合併營收(千)</td>
            <td>去年同期(千)1</td>
            <td>累計合併營收成長(%)</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電財務簡表 from 2016 to 2017
    >>> colist = ['年度', '流動資產', '非流動資產', '資產總計', '流動負債', '非流動負債', '負債總計', '權益總計', '公告每股淨值']
    >>> owlapp.fis('y', "2330", "2016", "2017", colist)

    [out]
            年度	 流動資產	非流動資產	    資產總計	  流動負債	 非流動負債 	  負債總計	   權益總計       公告每股淨值
    0	2017	857203110	1134658533	1991861643.00	358706680.00	110395320.00	469102000.00	1522759643.00	    58.70
    1	2016	817729126	1068726176	1886455302.00	318239273.00	178164903.00	496404176.00	1390051126.00	    53.58

    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

4. 多股財務簡表 (Financial Statements Multi, FIM)

    <br>依據 di 決定查詢資料頻率，並依指定區間，撈取全上市櫃台股的財務報表資訊
    <br> y(年)、 q(季) 是撈取財務報表資訊；m(月) 是撈取營收相關資訊

    ``` python
    OwlData.fim(di:str, dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="3"><b>Parameters<b></td>
            <td> - <b> di </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
                <ul style="list-style-type:disc;">
                    <li>Y : 年度, 格式 : yyyy</li>
                    <li>Q : 季度, 格式 : yyyyqq</li>
                    <li>M : 月, 格式 : yyyymm</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td> - <b>  dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 參數 di 大小寫無異
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
        <td colspan="25">年與季財報欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>年季</td>
            <td>流動資產</td>
            <td>非流動資產</td>
            <td>資產總計</td>
            <td>流動負債</td>
            <td>非流動負債</td>
            <td>負債總計</td>
        </tr>
        <tr>
            <td>權益總計</td>
            <td>公告每股淨值</td>
            <td>營業收入(千)</td>
            <td>營業成本(千)</td>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
            <td>營業外收入及支出(千)</td>
            <td>稅前純益(千)</td>
            <td>所得稅(千)</td>
        </tr>
        <tr>
            <td>稅後純益歸屬(千)</td>
            <td>每股盈餘(元)</td>
            <td>營業活動現金流量(千)</td>
            <td>投資活動現金流量(千)</td>
            <td>籌資活動現金流量(千)</td>
            <td>本期現金及約當現金增減數(千)</td>
            <td>期末現金及約當現金餘額(千)</td>
            <td>自由現金流量(千)</td>
        </tr>
        <tr>
        <td colspan="25">月營收欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年月</td>
            <td>單月合併營收(千)</td>
            <td>去年同期(千)</td>
            <td>單月合併營收年成長(%)</td>
            <td>單月合併營收月變動(%)</td>
            <td>累計合併營收(千)</td>
            <td>去年同期(千)1</td>
            <td>累計合併營收成長(%)</td>
        </tr>
    </table>

   - 範例

        ``` python
        # 台股上市上櫃財務簡表 from 2018
        >>> colist = ['股票代號', '股票名稱', '年度', '流動資產', '非流動資產', '資產總計', '流動負債', '非流動負債', '負債總計', '權益總計', '自由現金流量(千)']
        >>> owlapp.fim('Y',"2018")

        [out]
        1   股票代號   股票名稱 年度       流動資產      非流動資產      資產總計        流動負債       非流動負債     負債總計      權益總計   自由現金流量(千)
        0   1101       台泥    2018   110380695.00   233704423.00   344085118.00   64503844.00    82201818.00  146705662.00  197379456.00   11351781.00
        1   1102       亞泥    2018   80358506.00    198829492.00   279187998.00   62804294.00    57335358.00  120139652.00  159048346.00   89315.00

        ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

5. 法人籌碼個股資料 (Corporate Chip Single, CHS)

    <br>依指定日期區間，撈取指定股票的三大法人買賣狀況和該股票的融資券狀況
    <br>

   ``` python
   OwlData.chs(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
   ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>日期</td>
            <td>法人買賣超</td>
            <td>法人買賣超金額(千)</td>
            <td>外資買賣超</td>
            <td>外資買賣超金額(千)</td>
            <td>投信買賣超</td>
            <td>投信買賣超金額(千)</td>
            <td>自營買賣超</td>
            <td>自營買賣超金額(千)</td>
        </tr>
        <tr>
            <td>融資增減</td>
            <td>融資餘額</td>
            <td>融資使用率</td>
            <td>融券增減</td>
            <td>融券餘額</td>
            <td>融券使用率</td>
            <td>券資比</td>
            <td>當沖比率</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電法人籌碼資料 from 2019/08/01 to 2019/08/02
    >>> owlapp.chs("2330", "20190801", "20190802")

    [out]
        	    日期	法人買賣超	法人買賣超金額(千)   外資買賣超	    外資買賣超金額(千)	投信買賣超  投信買賣超金額(千)	自營買賣超	自營買賣超金額(千)	融資增減	    融資餘額	融資使用率   融券增減	融券餘額	 融券使用率	券資比	當沖比率
        0	20190802	-8712.00	-2191606.00	    -9356.00	    -2353623.00 	-235.00	    -59122.00	        879.00	        221139.00	        -1264.00    8948.00	0.14	    -162.00	1603.00	    0.02	17.91	0.01
        1	20190801	-9058.00	-2323101.00	    -10675.00	    -2737829.00	        196.00	    50270.00	        1421.00	        364458.00	        806.00	    10212.00	0.16	    -226.00	1765.00	    0.03	17.28	0.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

6. 法人籌碼多股資料 (Corporate Chip Multi, CHM)

    <br>查詢指定日期，全上市櫃台股的三大法人買賣狀況和融資券狀況
    <br>

   ```python
   OwlData.chm(dt:str,colist:list) -> DataFrame
   ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期 8碼，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>日期</td>
            <td>法人買賣超</td>
            <td>法人買賣超金額(千)</td>
            <td>外資買賣超</td>
            <td>外資買賣超金額(千)</td>
            <td>投信買賣超</td>
        </tr>
        <tr>
            <td>投信買賣超金額(千)</td>
            <td>自營買賣超</td>
            <td>自營買賣超金額(千)</td>
            <td>融資增減</td>
            <td>融資餘額</td>
            <td>融資使用率</td>
        <tr>
        </tr>
            <td>融券增減</td>
            <td>融券餘額</td>
            <td>融券使用率</td>
            <td>券資比</td>
            <td>當沖比率</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台股上市上櫃  from 2019/08/01 所有法人籌碼資訊
    >>> colist = ['日期', '法人買賣超', '法人買賣超金額(千)', '外資買賣超', '外資買賣超金額(千)', '投信買賣超', '投信買賣超金額(千)']
    >>> owlapp.chm("20190801", colist)

    [out]
        股票代號    股票名稱	法人買賣超  法人買賣超金額(千)	外資買賣超    外資買賣超金額(千)	投信買賣超  投信買賣超金額(千)	
    0     1101	台泥	-8374.00    -369823.00	        -8670.00	-382894.00	-63.00	          -2782.00
    1     1102	亞泥	 1697.00      70341.00           1636.00	  67813.00	  0.00	            0.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

7. 技術指標 個股 (Technical Indicators Single, TIS)

    <br>依指定日期區間，撈取指定股票的技術指標數值
    <br>

    ```python
    OwlData.tis(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
            <td>DIF</td>
            <td>MACD</td>
        </tr>
        <tr>
            <td>DIF-MACD</td>
            <td>W%R(5)</td>
            <td>W%R(10)</td>
            <td>+DI(14)</td>
            <td>-DI(14)</td>
            <td>ADX(14)</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台積電技術指標 from 2019/08/01 to 2019/08/02
    >>> colist = ['日期', 'K(9)', 'D(9)', 'RSI(5)', 'RSI(10)']
    >>> owlapp.tis("2330", "20190801", "20190802", colist)

    [out]
             日期       K(9)     D(9)     RSI(5)      RSI(10)
    0      20190802    28.62    49.84     17.88       40.98
    1      20190801    39.80    60.45     30.51       51.65
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

8. 技術指標 多股 (Technical Indicators Multi, TIM)

    <br>查詢指定日期，全上市櫃台股的技術指標數值
    <br>

    ```python
    OwlData.tim(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期 8碼，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

     - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
            <td>DIF</td>
        </tr>
        <tr>
            <td>MACD</td>
            <td>DIF-MACD</td>
            <td>W%R(5)</td>
            <td>W%R(10)</td>
            <td>+DI(14)</td>
            <td>-DI(14)</td>
            <td>ADX(14)</td>
        </tr>
    </table>
     - 範例

    ``` python
    # 擷取台股上市上櫃  from 2019/08/01 所有技術指標資訊
    >>> colist = ['股票代號', '股票名稱', '日期', 'K(9)', 'D(9)', 'RSI(5)',
            'RSI(10)']
    >>> owlapp.tim("20190801", colist)

    [out]
          股票代號 股票名稱	日期	K(9)	 D(9)	RSI(5)	RSI(10)
    0	1101	台泥  20190801	40.17	49.83	25.77	 35.40
    1	1102	亞泥  20190801	9.02	13.11	15.33	 27.81
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

9. 公司基本資料 多股 (Company Information Multi, CIM)

    <br>撈取上市櫃台股的公司基本資料
    <br>

    ``` python
    OwlData.cim(colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="1"><b>Parameters<b></td>
            <td> - <b> colist </b> : <i> list, default None </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
         <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>中文簡稱</td>
            <td>英文簡稱</td>
            <td>公司名稱</td>
            <td>英文名稱</td>
            <td>地址</td>
            <td>電話</td>
        </tr>
        <tr>
            <td>傳真機號碼</td>
            <td>實收資本額(百萬)</td>
            <td>成立日期</td>
            <td>上市日期</td>
            <td>上櫃日期</td>
            <td>興櫃日期</td>
            <td>公發日期</td>
            <td>董事長</td>
        </tr>
        <tr>
            <td>總經理</td>
            <td>發言人</td>
            <td>上市上櫃</td>
            <td>產業名稱</td>
            <td>統一編號</td>
            <td>交易所公告股本(千)</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台股上市上櫃 所有公司基本資訊
    >>> colist = ['股票代號', '股票名稱', '中文簡稱', '董事長', '總經理']
    >>> owlapp.cim(colist)

    [out]
          股票代號	股票名稱   中文簡稱    董事長	總經理
    0	1101	  台泥      台泥	      張安平	李鐘培
    1	1102	  亞泥      亞泥	      徐旭東	李坤炎
    2	1103	  嘉泥	    嘉泥       張剛綸	祁士鉅
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

10. 股利政策 個股 (Dividend Policy Single, DPS)

    <br>依據指定年度區間，撈取指定股票的配發股利狀況表
    <br>

    ``` python
    OwlData.dps(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

     - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>年度</td>
            <td>現金股利合計</td>
            <td>股票股利合計</td>
            <td>股利合計</td>
            <td>現金股利殖利率(%)</td>
        </tr>
        <tr>
            <td>盈餘配息</td>
            <td>公積配息</td>
            <td>盈餘配股</td>
            <td>公積配股</td>
        </tr>
    </table>

     - 範例

    ```python
    # 擷取台積電股利政策資料 from 2017 to 2018
    >>> colist = ['年度', '現金股利合計', '股票股利合計', '股利合計']
    >>> owlapp.dps("2330", "2017", "2018", colist)
    [out]
        年度    現金股利合計	股票股利合計    股利合計
    0   2018	8	    0.00	8.00
    1   2017	8	    0.00	8.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

11. 股利政策 多股 (Dividend Policy Multi, DPM)

    <br>依指定年度，撈取全上市櫃台股的配發股利狀況表
    <br>

    ``` python
    OwlData.dpm(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一年度 4碼，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

      - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>現金股利合計</td>
            <td>股票股利合計</td>
            <td>股利合計</td>
        </tr>
        <tr>
            <td>現金股利殖利率(%)</td>
            <td>盈餘配息</td>
            <td>公積配息</td>
            <td>盈餘配股</td>
            <td>公積配股</td>
        </tr>
    </table>
      - 範例

    ``` python
    # 擷取台股上市上櫃  from 2018 所有股利政策資訊
    >>>　colist = ['股票代號', '股票名稱', '年度', '現金股利合計', '股票股利合計', '股利合計']
    >>> owlapp.dpm("2018", colist)
    [out]
          股票代號  股票名稱	年度    現金股利合計      股票股利合計       股利合計
    0	1101	 台泥	2018	    3.31	    0.70	    4.01
    1	1102	 亞泥	2018	    2.80	    0.00	    2.80
    2	1103	 嘉泥	2018	    1.00	    0.00	    1.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

12. 除權除息 個股 (Exemption Dividend Policy Single, EDPS)

    <br>依據指定年度區間，撈取指定股票的股東會日期及停止過戶的相關日期
    <br>

    ``` python
    OwlData.edps(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>年度</td>
            <td>股東會日期</td>
            <td>停止融券起始日</td>
            <td>融券回補日</td>
            <td>停止融券終迄日</td>
        </tr>
        <tr>
            <td>停止融資起始日</td>
            <td>停止融資終迄日</td>
            <td>停止過戶起</td>
            <td>停止過戶迄</td>
            <td>最後過戶日</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台積電除權除息資料 from 2017 to 2018
    >>> colist = ['年度', '股東會日期', '停止融券起始日', '融券回補日']
    >>> owlapp.edps("2330", "2017", "2018", colist)

    [out]

            年度	股東會日期	停止融券起始日	融券回補日
    0	2018	20180605	20180328.00	20180328.00
    1	2017	20170608	20170329.00	20170329.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

13. 除權除息 多股 (Exemption Dividend Policy Multi, EDPM)

    <br>依指定日期，撈取全上市櫃台股的股東會日期及停止過戶的相關日期
    <br>

    ``` python
    OwlData.edpm(dt:str, colist:str) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一年度 4 碼，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>股東會日期</td>
            <td>停止融券起始日</td>
            <td>融券回補日</td>
        </tr>
        <tr>
            <td>停止融券終迄日</td>
            <td>停止融資起始日</td>
            <td>停止融資終迄日</td>
            <td>停止過戶起</td>
            <td>停止過戶迄</td>
            <td>最後過戶日</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台股上市上櫃  2018 所有除權除息資訊
    >>> colist = ['股票代號', '股票名稱', '年度', '股東會日期', '停止融券起始日']
    >>> owlapp.edpm("2018", colist)

    [out]
          股票代號 股票名稱	年度    股東會日期    停止融券起始日
    0	1101	台泥	2018	20180622	20180416
    1	1102	亞泥	2018	20180626	20180420
    2	1103	嘉泥	2018	20180621	20180413
    3	1104	環泥	2018	20180614	20180403
    4	1108	幸福	2018	20180615	20180409
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

14. 即時報價 (Timely Stock Price, TSP)

    <br>撈取指定股票即時股價資訊
    <br>

    ``` python
    OwlData.tsp(sid:str, colist:str) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>:
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
        <td colspan="25">欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>時間</td>
            <td>成交價</td>
            <td>漲跌</td>
            <td>漲跌幅</td>
        </tr>
        <tr>
            <td>總量</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>成交量</td>
        </tr>
    </table>
    - 範例

    ``` python
    # 擷取台積電即時報價
    >>> colist = ['股票代號', '股票名稱', '時間', '開盤價', '最高價', '最低價', '成交量']
    >>> owlapp.tsp("2330", colist)

    [out]
        股票代號    股票名稱	      時間	開盤價	最高價	最低價	成交量
    0     2330	台積電	20190814143000	252.50	254.00	249.50	 11.00
    ```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## Contribute

owldata was created by OwlData co. <owldb@cmoney.com.tw>

Contributing were welcome, please use GitHub issue and Pull Request to contribute!

歡迎協作，請使用 GitHub issue 以及 Pull Request 功能來協作。

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>