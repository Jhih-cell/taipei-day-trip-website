### 臺北一日遊

 [上線網址請點我](http://18.217.38.82:3000/)  

［會員測試資訊］(也可以自行註冊)<br />
帳號：test@mail.com <br />
密碼：test<br />

［信用卡測試資訊］<br />
卡片號碼：4242 4242 4242 4242<br />
過期時間：01/23<br />
驗證碼：123<br />

［使用技術／效果］<br />
**後端**<br />
會員功能、景點資料取得、預定行程、訂單付款 API 開發：依循 RESTfulAPI 風格<br />
伺服器：Flask<br />
網站上線：EC2 instance ( Red Hat Enterprise Linux 8 ) <br />
資料庫：MySQL<br />
第三方 API 串接：串接第三方金流服務商 TapPay API<br />
機密資訊管理：設定環境變數搭配 python-dotenv 套件載入程式中使用<br />

**前端**<br />
畫面呈現：RWD、Infinite Scroll<br />
首頁、訂單頁抓取景點資訊：AJAX<br />
訂單頁面景點輪播效果：JavaScript

［資料庫結構］（會員、訂單、景點資訊）<br />
![](https://github.com/Jhih-cell/taipei-day-trip-website/blob/main/dbstr.png)
