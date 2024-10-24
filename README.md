## ページを自動遷移しながらスクレイピングするCLIツール

### 開発目的
複数ページにわたり、特定のタグを抽出してCSVに落とし込むためのツール。
今回はfantiaというSNSの中でユーザー・Twitter（X）・いいね数などをスクレイピングするために開発。

### 実行環境

python3

Chromeドライバを使用。
https://developer.chrome.com/docs/chromedriver/downloads?hl=ja からダウンロード → 今回は ~/usr/share/ に配置

・selenium
・requests
・csv

### 実行手順
プログラムないでCSVファイル名、スクレイピング対象URLを変更しながら実行。

### 備考
CSRやSSRでページが生成されている場合、ChromeドライバでURLにアクセスしてからすぐ解析し始めると目的のCSSを見つけられずエラーになる場合があるので、下記コードで対応。

```
# 要素が存在するまで待機
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
```

また、100件を超えるデータを挿入する場合になぜかタイムアウトになるケースがあったので、1回に取得・書き込みするデータの最大数を100に設定し、最大データ量に応じて書き換えながら実行。

### 改善点
スクレイピング自体にもかなり時間がかかっているほか、ドライバ操作やCSV書き込みなどでさらに多くの時間がかかりパフォーマンスが良くないので要改善。

また、本スクリプトはコードを書き換えながら実行するものなので、スクレイピング対象やCSSセレクタを任意で指定できるようにし極力コードを変更しなくても実行できるようにしたい。

PyInstallerなどを利用して実行ファイルに落とし込むとChromeDriverのインストールとpythonスクリプトの時効手順を省略できる。