# Rolithax Schema 官方插件源

在 Rolithax Schema 的插件源页面添加：

```text
https://github.com/WLudy1012/rolithax-schema-plugins
```

客户端会固定仓库 commit，读取这份 README 的目录，再下载选中插件的三个文件。每个文件都校验 SHA-256 与大小，原生引擎校验通过后才允许安装。

| 面板 | 操作与状态 | 当前格式覆盖 |
| --- | --- | --- |
| [Paper](plugins/paper/README.md) | 启动状态、在线玩家、进出记录 | Paper/Spigot 常见英文日志 |
| [LuckPerms](plugins/luckperms/README.md) | 插件信息、玩家与权限组、继承关系 | 5.4/5.5 主线默认英文格式 |
| [Chunky](plugins/chunky/README.md) | 进度、暂停继续、世界与生成范围 | 1.4/1.5 主线英文及简体中文格式 |

“格式覆盖”表示官方源码格式核对与合成样本回放，不等同于每个服务端版本都做过真服测试。插件详情记录具体依据及边界。日志中没有足够信息时保留“等待查询”，不推测服务器状态。

## 开发

使用 [Rolithax Schema SDK](https://github.com/WLudy1012/rolithax-console-sdk) 和 [独立模板](https://github.com/WLudy1012/rolithax-console-plugin-template)。配置 `ROLITHAX_SCHEMA_CLI` 后：

```sh
python ../rolithax-console-sdk/rolithax_schema_sdk.py validate plugins/chunky
python ../rolithax-console-sdk/rolithax_schema_sdk.py replay plugins/chunky plugins/chunky/fixtures/1.5.66-en.log plugins/chunky/fixtures/expected.json
python ../rolithax-console-sdk/rolithax_schema_sdk.py source-index .
python ../rolithax-console-sdk/rolithax_schema_sdk.py source-index . --check
```

本源当前全部是可直接下载打包的 YAML 插件。新增 Lua 插件时必须提供已上传的预构建 ZIP 地址、SHA-256 和字节数；ZIP 内含 business.lua 源码及元数据，不在安装时执行仓库构建脚本。

CI 的 catalogue job 每次提交都会独立检查 README 结构、manifest 一致性、文件大小与 SHA-256，只需要 Python 标准库。native job 在仓库变量 ROLITHAX_RUNTIME_REF 与 ROLITHAX_SDK_REF 都配置后才运行；请将两者设为已发布且包含 Schema 2 的 commit SHA。目前 8 组格式样本、参数注入拒绝、聊天伪装与 Chunky 指定世界命令已经使用本地原生引擎回放通过。远程未配置发布引用时会跳过原生集成，不会将跳过标记成实测通过。

```rolithax-schema-repository
{
  "schemaVersion": 1,
  "id": "rolithax.official",
  "name": "Rolithax 官方插件源",
  "description": "Paper 运行概览、LuckPerms 权限管理与 Chunky 世界预生成。",
  "plugins": [
    {
      "id": "rolithax.paper-overview",
      "version": "1.0.0",
      "name": "Paper 运行概览",
      "description": "启动状态、在线玩家与最近进出记录。",
      "engine": "yaml",
      "readme": "plugins/paper/README.md",
      "compatibility": {
        "platforms": [
          "Paper",
          "Spigot"
        ],
        "versions": [
          "1.20.x",
          "1.21.x"
        ],
        "locales": [
          "en"
        ],
        "verification": "synthetic-fixture"
      },
      "source": {
        "type": "files",
        "path": "plugins/paper",
        "files": [
          {
            "path": "plugin.json",
            "sha256": "e03b61bb22eca5c52958f156f39e902d6013b13b1a39ce75ab0948a40530644a",
            "size": 437
          },
          {
            "path": "rules.yaml",
            "sha256": "cb48f1d7bc1b2b9658c20da39d153ff0d4326f343aeb655719d9eda70d7fe805",
            "size": 916
          },
          {
            "path": "ui.xml",
            "sha256": "11373c63af938295f9abe8750ebcb4ec7c91cc1fdc645e859d6feda51d038fb1",
            "size": 655
          }
        ]
      }
    },
    {
      "id": "rolithax.luckperms",
      "version": "1.0.0",
      "name": "LuckPerms 权限管理",
      "description": "查看插件和玩家信息、查询权限组并管理继承关系。",
      "engine": "yaml",
      "readme": "plugins/luckperms/README.md",
      "compatibility": {
        "plugin": "LuckPerms",
        "versions": [
          "5.4.x",
          "5.5.x"
        ],
        "locales": [
          "en"
        ],
        "verification": "upstream-format-fixture"
      },
      "source": {
        "type": "files",
        "path": "plugins/luckperms",
        "files": [
          {
            "path": "plugin.json",
            "sha256": "da9ea7c44e5ba3c3811ce1ea7e1376b3d7572e2088d8f365a81e321339f2e97f",
            "size": 433
          },
          {
            "path": "rules.yaml",
            "sha256": "9cf33df8c95a3e534df0c3e901563bdc5d459634a2bfe56b2cdd89d5c4913fcb",
            "size": 1038
          },
          {
            "path": "ui.xml",
            "sha256": "b61b05a36a6198c10830c8e5d1ad7dec20c8eba2104e5f335c77cbf834ad86b8",
            "size": 1707
          }
        ]
      }
    },
    {
      "id": "rolithax.chunky",
      "version": "1.0.0",
      "name": "Chunky 世界预生成",
      "description": "查询中英文任务进度、暂停继续任务并配置生成范围。",
      "engine": "yaml",
      "readme": "plugins/chunky/README.md",
      "compatibility": {
        "plugin": "Chunky",
        "versions": [
          "1.4.x",
          "1.5.x"
        ],
        "locales": [
          "en",
          "zh_CN"
        ],
        "verification": "upstream-format-fixture"
      },
      "source": {
        "type": "files",
        "path": "plugins/chunky",
        "files": [
          {
            "path": "plugin.json",
            "sha256": "32118ff5031c86d91a986e04f17fec9177856e39a4cd795b78288f02e6aefff4",
            "size": 445
          },
          {
            "path": "rules.yaml",
            "sha256": "7b18e36ce83d52a55ab782f20f16a7ad5e246d8da725cd3dfe6ab679dfeffed5",
            "size": 2740
          },
          {
            "path": "ui.xml",
            "sha256": "d367599654c740f7d86bb85831d1c27f0ab9d310e9d02055e556812a93dc8c3e",
            "size": 1637
          }
        ]
      }
    }
  ]
}
```
