題目1：
在原先的user的table中新增account, password以及role(str)兩三個欄位
登入的API會以account跟password來判斷能不能給token
新增使用者的API中 role 只能接受AM / SUBAM / NORMAL 這三種值，否則不給新增

題目2：
透過解析token的方式來辨別改次登入的使用者權限為何，AM可以執行所有API ; SUBAM只能GET, CREATE, PATCH ; 一般使用者只能GET 以及PATCH自己