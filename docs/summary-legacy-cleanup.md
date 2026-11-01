# Summary 旧功能清理（2026-11-01）

当前 Summary 是原生图、交互与层级视图的权威。旧正式 Canvas 的固定前沿编号、
全局黑白预设矩阵、研究席位及 DOM 性能采样不能直接用于这个界面。
本次删除专属实现与测试，避免 Agent 或维护者继续使用失效入口。

## 删除范围

共删除 38 个文件，421,916 字节。可核对的路径、分组、原字节数与 SHA256 见
[退役清单](summary-legacy-retirement.json)，原实现可从清单中的 Git 基线提交恢复。
不新增源码快照。

- 未挂载的 `PerfBenchmarkPanel`、`StudyPanel`、`perfBenchmark`、`nativePerformance`
  及其专属测试。
- 依赖旧正式 Canvas DOM、固定九组前沿和黑白预设的浏览器矩阵、黄金图校验与准备脚本。
- 旧研究任务席位、分配、收集、readiness 与汇总脚本及其专属测试。
- 旧 M4 输入 harness、控制页、DOM observer、性能/输入/连续观测/调度校验器及其专属测试。

同步删除这两个旧面板独占的 34 项翻译，更新当前资源摘要；将 Skill 视觉流程改为
实际 Summary 模块范围、源码深度、架构概览、模块详图与默认展开恢复。
旧协议入口页保留退役说明和历史证据链接，不再提供旧启动命令。

## 保留范围

当前模块展开面板和 Summary 原生图没有删除；85/180 mm 是导出宽度。
现有已保存/导入文档的 monochrome 样式及共享渲染、导出兼容能力继续保留，
这不表示当前存在全局黑白预设选择器。

正式 Python 源码工作副本、审核事务、CanvasDocument、共享 renderer、路由依赖
及 `perf.ts` 工程遥测仍有实际调用。当前原生引擎 benchmark、共享 core CPU
benchmark 和 `HierarchyTree` 组件对比 probe 按各自有限范围保留；这些诊断
不能替代当前 Summary 的真实输入到呈现或 presented FPS 验收。

`docs/evidence/**`、`docs/validation/**` 及冻结历史收据不改写。
当前浏览器矩阵应绑定真实模块范围、当前图版本与导出工件，不再沿用旧固定前沿表。
真人、出版与完整性能验收仍需新协议和实际执行；三宿主真实 Agent E2E、
DeepSeek E2E 待办和远端 CI 状态不因本次清理改变。本次仅做本地检查。

## 本地验证

- TypeScript/Vite 生产构建通过。
- 针对性回归共 20 项：19 通过，1 项因沙箱浏览器启动限制跳过；
  另用本机 headless-shell 补跑出版测试，4/4 通过、无跳过。
- 预览架构审计通过：旧路径、旧声明和旧 `.publication-scene` DOM 查询均为空；
  新反例同时覆盖未挂载旧面板和更名后的旧 DOM observer。
- Python unittest 收集 690 项，导入失败 0；仅证明收集完整，不等于执行完整后端套件。
- 翻译与架构边界补验 8/8 通过；Skill 格式校验、资源摘要、删除清单基线哈希、
  新增文档链接和 `git diff --check` 均通过。

本次没有重跑完整前后端套件或完整浏览器矩阵，也没有修改/保存用户当前画布。
