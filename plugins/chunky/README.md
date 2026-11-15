# Chunky 世界预生成

面板提供任务进度、暂停、继续、世界选择、半径、采用世界边界、检查范围和开始任务。命令均使用 Chunky 的公开命令入口；启动和配置变更由宿主显示具体命令并确认。

Chunky progress 返回全部任务；当前概览显示最后收到进度的世界，多个世界同时预生成时不做虚假的汇总。暂停与继续显式携带用户输入的世界名，不会隐式操作全部世界。面板未暴露 trim、cancel、confirm，避免把共享的服务端确认状态当成单个面板按钮的确认。

核对范围（2026-11-15）：

- [Chunky 1.4 tag 英文日志格式](https://github.com/pop4959/Chunky/blob/cb3aee6217d0d3cad43e871595739302c2a59326/common/src/main/resources/lang/en.json)。
- [Chunky 1.5 tag 英文日志格式](https://github.com/pop4959/Chunky/blob/4bec4848adc8417fca2a5579a904b17ce6ede841/common/src/main/resources/lang/en.json)。
- [当前英文语言表](https://github.com/pop4959/Chunky/blob/c4274bd539d1d79a15fe1e73afb2eface64d625f/common/src/main/resources/lang/en.json) 与 [简体中文语言表](https://github.com/pop4959/Chunky/blob/c4274bd539d1d79a15fe1e73afb2eface64d625f/common/src/main/resources/lang/zh_CN.json)。
- [作者发布的更新记录](https://www.spigotmc.org/resources/chunky.81534/updates) 当前最新为 1.5.66；1.5 需要 Java 25，1.4 适用于 Java 21。

fixtures 是根据固定 commit 的语言表构造的日志，覆盖 1.4、1.5 的稳定任务消息及当前中英文消息。主线中间版本只要保持相同格式即可兼容；这不是逐个版本或各平台实服认证。若更换自定义翻译或消息前缀，应提交脱敏样本补充规则。

```sh
python path/to/rolithax_schema_sdk.py replay . fixtures/1.5.66-en.log fixtures/expected.json
python path/to/rolithax_schema_sdk.py replay . fixtures/zh-CN.log fixtures/expected.json
```
