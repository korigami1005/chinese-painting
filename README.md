# Identifying Chinese Painting Genres with Deep Learning
先用segement.py將指定資料夾內的圖片分割程式當的大小，將這些分割後的圖片以檔名開頭進行標籤，例如第一分類就標01xxxx，第二分類就標02xxxx，全部標籤好後，利用label.py產生對應的csv檔，即準備好訓練資料。
modelD.py跟transfer.py為訓練之模型。
訓練好模型後，使用GUI.py可產生一個簡易介面將欲判斷的圖片載入切割再進行辨識，運作過程如附圖。
1.簡易介面
![image](https://github.com/korigami1005/chinese-painting/blob/master/01.png)
2.載入圖片
![image](https://github.com/korigami1005/chinese-painting/blob/master/02.png)
3.分割圖片
![image](https://github.com/korigami1005/chinese-painting/blob/master/03.png)
4.選擇模型進行分析
![image](https://github.com/korigami1005/chinese-painting/blob/master/04.png)
5.顯示結果
![image](https://github.com/korigami1005/chinese-painting/blob/master/05.png)
6.開啟顏色對應表
![image](https://github.com/korigami1005/chinese-painting/blob/master/06.png)
