# ArchCanvas Studio

从 Python / PyTorch 模型源码生成可编辑的模型架构画布。

ArchCanvas 支持源码结构与依赖浏览、递归展开、模块组装、源码构件复用、画布编辑，以及 SVG / PDF / PNG 导出。静态分析读取源码文本，不导入、不实例化、不执行用户模型；无法解析的结构保留明确诊断。

## 快速开始

需要 **Python 3.11+** 和 **Node.js 24+**。从仓库根目录执行：

```bash
python3 -m venv .venv
cd studio
npm ci
npm run build
cd ..
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli serve --host 127.0.0.1 --port 8765
```

打开 [http://127.0.0.1:8765](http://127.0.0.1:8765)。在界面中导入 Python 文件、源码目录或已保存的编辑 JSON，也可以从内置模型库打开示例。

这是源码发行目录：前端依赖和构建产物不随仓库提交，首次运行需要执行上述安装与构建。静态分析与默认 SVG 导出不需要安装 PyTorch。

## 命令行

```bash
# 检查当前运行时、前端构建和模块目录
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli doctor --summary

# 不执行模型，静态分析示例源码
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli analyze \
  --root fixtures/mlp --entry model:MLP --output /tmp/mlp-architecture.json

# 查看实际可用能力
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli capabilities
```

## 可选功能

- **PDF / PNG 导出**：在 `.venv` 中安装 `requirements.lock`，并提供系统 Cairo；详见 [使用说明](docs/usage.md)。
- **CPU 运行观察**：需要独立 `.venv-runtime`、锁定的 PyTorch CPU 依赖和 Linux 内核隔离支持；必须显式启动。见 [运行环境](docs/runtime.md)。
- **Agent Skill**：入口为 [skills/archcanvas/SKILL.md](skills/archcanvas/SKILL.md)，源码目录中的启动器会绑定本仓库。只复制 Skill 说明文件无法提供完整画布。

普通拖动、连线和样式编辑只修改画布。正式 Python 源码修改使用独立工作副本和受支持的准备、审查、批准、提交流程；静态依赖和单次运行观察不等于任意输入下的执行证明。

## 项目结构

| 路径 | 用途 |
| --- | --- |
| `src/` | Python API、源码分析、语义桥接、搭建、事务、隔离运行和导出 |
| `studio/src/` | React / TypeScript 工作台 |
| `studio/public/preview/` | Summary 画布引擎、当前模型与源码构件资源 |
| `skills/` | AI 编程助手使用说明和运行时启动器 |
| `schemas/` | 架构、画布、草稿与源码适配数据契约 |
| `fixtures/` | 小型示例及测试输入 |
| `tests/`、`studio/tests/` | 保留的功能回归测试 |
| `scripts/` | 画布会话、导出、构件库重建和资源完整性检查 |
| `docs/` | 使用、开发、架构及可选运行环境说明 |
| `licenses/` | 模型材料的第三方许可 |

## 数据与开发

服务默认将文档、源码副本、草稿、事务和导出写入 `.archcanvas/`；可用 `serve --data-dir /absolute/state-root` 指定其他完整状态目录。一个状态目录只应由一个服务使用。

画布引擎还使用浏览器 IndexedDB / localStorage 保存递归布局和路由。跨浏览器或端口迁移时，请导出编辑 JSON；只备份服务端状态目录不能覆盖全部浏览器状态。

构建、测试和 CI 说明见 [开发指南](docs/development.md)，各层职责见 [架构说明](docs/architecture.md)。本目录保留使用与开发所需内容，历史验收材料、发布快照、本机环境和缓存不随仓库分发。

## 许可

项目原创代码采用 [Apache-2.0](LICENSE)。第三方依赖、模型示例及其衍生材料保留各自许可，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 [模型许可](licenses/models/README.md)。
