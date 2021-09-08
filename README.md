# Docker + Seleniumで猫画像を取ってくる

Docker と Selenium を使ってスクレイピングするサンプル。

## 1. 準備

必要なライブラリをインストール

### PDMを使っている場合

``` shell
$ pdm install
```

### Pipを使う場合

``` shell
$ pip install -r requirements.txt
```

## 2. docker-compose.yml の準備

自分の使っているMacのCPUに応じて docker-compose.yml を準備する。

### Intel Macの場合

``` shell
$ cp docker-compose.yml.intel docker-compose.yml
```

### M1 Macの場合

``` shell
$ cp docker-compose.yml.apple_silicon docker-compose.yml
```

## 3. DockerでSeleniumを起動

``` shell
$ docker compose up -d
```

## 4. プログラムを実行

### 4.1 検索のみ（保存しない）

PDMを利用していない場合は最初の「pdm run」は不要です。（以下も同じ）

``` shell
$ pdm run python img_collector.py 猟奇的
```

### 4.2 画像を保存

- `-t <保存場所>` のオプションをつける。
- `-n <数>` で取ってくる画像の枚数を指定できる。
- `-s <数>` でスキップする画像の枚数を指定できる。

``` shell
$ pdm run python img_collector.py -t imgs/ryokiteki -n 3 猟奇的 暴力的
```

## 5. 実行が終わったら Selenium を終了

``` shell
$ docker compose down
```

いじょ。
