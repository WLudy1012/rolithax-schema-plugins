# Paper 运行概览

从启动、停止、玩家进出和 list 命令响应展示运行概况，唯一命令为 `list`。Schema 2、YAML 引擎。

本面板使用 Paper/Spigot 常见英文 Minecraft 日志格式。fixtures 是人工构造的 1.21.1 示例，不代表所有版本已经真服测试。定制日志前缀、翻译后的 list 输出或代理服可能需要新规则。进出列表是最近事件，在线名单只取最近一次 list 响应；不会根据缺失的日志推测当前在线数。

```sh
python path/to/rolithax_schema_sdk.py validate .
python path/to/rolithax_schema_sdk.py replay . fixtures/logs.txt fixtures/expected.json
```
