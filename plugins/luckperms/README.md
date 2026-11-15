# LuckPerms 权限管理

支持 `lp info`、`lp listgroups`、玩家信息、玩家继承组、权限组信息，以及指定玩家添加/移除继承组。玩家名使用 player 校验，权限组使用 token 校验；写操作需要宿主按实例授权并确认具体命令。

版本、平台和存储类型通过默认英文 info 输出提取；最近响应列表保留 LP 前缀消息。其他翻译仍可手动查询和查看响应，但不能保证概况字段被识别。面板不会把命令被发送当成权限已经修改成功。

核对范围（2026-11-15）：

- [LuckPerms v5.4 官方语言表](https://github.com/LuckPerms/LuckPerms/blob/99c3d68d3a618677800fd674363855ae143f4452/common/src/main/resources/luckperms_en.properties)。
- [LuckPerms v5.5 官方语言表](https://github.com/LuckPerms/LuckPerms/blob/0486bc885bce9cbfd310cff3f6d7ef8685605e97/common/src/main/resources/luckperms_en.properties)。
- [当前官方消息构造代码](https://github.com/LuckPerms/LuckPerms/blob/b878ae92ff7558621f30c245ff8494fd6cf63f24/common/src/main/java/me/lucko/luckperms/common/locale/Message.java)。
- [官方近期发布容器](https://github.com/LuckPerms/LuckPerms/pkgs/container/luckperms/versions?filters%5Bversion_type%5D=tagged) 中的 5.5.91，用作近期版本字符串样本。

fixtures 按上述格式构造，并非运行各个版本导出的真实日志。5.4.x / 5.5.x 为相同格式的兼容目标，已回放的是列出的 tag 快照与当前源码格式；未经逐个构建实测，不宣称覆盖每一个定制发行版。Bukkit 命令前缀为 lp，其他平台的 lpb/lpv 等别名未在本面板暴露。

```sh
python path/to/rolithax_schema_sdk.py replay . fixtures/5.5.91-en.log fixtures/5.5.91-expected.json
```
