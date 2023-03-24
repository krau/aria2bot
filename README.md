# aria2bot

Aria2 Telegram Bot 用 bot 控制 Aria2 下载器

## 特性

⚡ 全程异步实现+类型标注

📝 交互式添加下载任务,支持多链接

📊 查询下载器状态

✨ 内联键盘刷新

😋 中文编程(伪)

## 使用

```bash
git clone https://github.com/krau/aria2bot
cd aria2bot
```

用你喜欢的工具创建并激活虚拟环境,然后

```bash
pip install -r requirements.txt
```

修改 `config.yaml` 各项配置,然后

```bash
python bot.py
```

## demo

![菜单](https://i.imgur.com/apNHIiG.png)

![查询下载器状态](https://i.imgur.com/M7gQTxN.png)

![查询任务队列](https://i.imgur.com/BV31Nzf.png)

![刷新](https://i.imgur.com/HFEOI3C.png)

## TODO

- [ ] 多下载器支持
- [x] 添加下载任务
  - [x] 交互式添加下载任务,支持多链接
- [ ] 查询各项状态
  - [x] 下载器状态
  - [x] 任务队列
  - [ ] 对每个任务进行查看与操作(内联键盘)
- [ ] 任务完成通知
- [ ] 自定义设置
  - [ ] 通过命令更改部分 Aria2 设置
  - [ ] 交互式更改 RPC 地址等设置
- [ ] docker compose 部署

## 参与开发

欢迎提交 PR, 请使用 autopep8 格式化代码

~~风格上希望保持伪中文编程~~

### 配置

本项目使用了 [Dynaconf](https://github.com/dynaconf/dynaconf) 作为配置管理,开发时,请在项目根目录下创建 `config.dev.yaml` 文件,它会覆盖 `config.yaml` 中的配置.

## 鸣谢

- [aioaria2](https://github.com/synodriver/aioaria2)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

etc.

## License

MIT
