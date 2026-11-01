# 使用说明

## 打开模型

先按根目录 README 构建并启动服务。通过界面导入 Python 文件或源码目录，选择模型入口和必要的构造参数，也可打开内置模型。构造参数用于静态分析，不会执行构造函数。未知调用或动态结构会保留为待解析区域。

展开模块、查看层级和源码证据、移动节点、编辑样式与图例，都在画布内进行。原生组装入口与正式 Python 源码工作副本具有不同契约：视觉连线不会自动写回 Python；正式源码修改需进入对应工作副本和审查流程。

## 保存与迁移

服务端默认保存到 `.archcanvas/`，可通过 `serve --data-dir /absolute/state-root` 指定其他目录。递归几何、路由和偏好还会保存在当前浏览器的 IndexedDB/localStorage 中。需要换浏览器、换端口或迁移到其他机器时，使用“导出 → 编辑 JSON”，再通过导入入口恢复。

## 导出

SVG 不需要可选 Python 转换依赖。PDF/PNG 需要系统 Cairo 和锁定依赖：

```bash
.venv/bin/python -m pip install -r requirements.lock
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli capabilities
```

缺少 Cairo 时请通过操作系统包管理器安装相应库，例如 Debian/Ubuntu 的 `libcairo2`。字体依赖宿主系统，中文图建议安装 Noto CJK 字体。转换能力以当前解释器的 `capabilities` 返回值为准。

可以导出当前图的 SVG/PDF/PNG，也可导出编辑 JSON 用于恢复。物理尺寸和字体可读性仍需对最终文件进行审看。

## Agent 调用

完整源码目录中的 Skill 启动器会自动绑定本仓库：

```bash
python3 -I -B skills/archcanvas/scripts/archcanvas_runtime.py doctor --summary
```

使用任何 Agent 宿主前，先查看实际 `doctor` 和 `capabilities` 输出。具体调用和工作流见 Skill 的 `references` 目录。
