# youdao-translate

> 逆向有道翻译
>
> 仅限学术交流，如有侵权等联系我删除

# Docker

```shell
docker pull ghcr.io/xiaoxuan6/youdao-translate:latest
```

## Run

```shell
docker run --name=yd -d -p 8888:8888 ghcr.io/xiaoxuan6/youdao-translate:latest
```

## Shell test

```shell
curl -sX POST http://127.0.0.1:8888/api/translate -H "Content-Type: application/json; charset=utf-8" -d "{\"text\": \"你好\"}"
```