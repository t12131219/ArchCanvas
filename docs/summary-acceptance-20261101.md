# Summary 路由修复与本地验收：2026-11-01

基于 `b993841ef33347fdb7916b9fd27dec95bb9e5892` 的未提交工作区。
本记录接续 [首轮维护](maintenance-20261101.md)，不修改其原始失败结果。
本轮只做本地测试；按用户决定，DeepSeek 真实模型调用保留待办。

## Transformer 的 10 组重叠

初次打开的全局美化搜索耗尽共享路由预算，后续 33 条边保留待路由路径，
其中出现此前报告的 10 组非同源共线重叠。初次 `generic-build` 现在先寻找
合法路线，关闭该次可选美化搜索；显式优化命令仍使用原来的美化策略。
没有放宽源码、端口或几何校验，也没有隐藏失败连线。

默认配置 `0216717d966327f4`：3,371 个原始节点、3,663 条原始依赖；
默认可见 82 节点/80 边。独立引擎和实际浏览器均通过严格约束，待路由 0、
失败 0，原 10 组重叠不再出现。该结果限定在实际检查的布局，不能推广为任意
深度、手动编辑或所有优化设置的全域保证。

Apply 和交互回归恢复对 Transformer 的严格几何要求，同时检查原始源码、
绑定、节点位置及独立历史。另用零预算、未经路由的真实构建图覆盖中断分支，
验证失败诊断保留、移除诊断后拒绝接受，以及失败 Apply 不替换已有合法图。

## 本轮测试

| 检查 | 实际结果 |
|---|---|
| 完整前端入口 | 1,313 项：1,311 通过、1 失败、1 跳过；1,185.46 秒 |
| 最终 Apply 定点复测 | 8/8 通过、无跳过 |
| 最终 Apply＋交互联合复测 | 10/10 通过、无跳过 |
| 跳过的真实 DOM 导出补测 | 现有 Chromium headless-shell，4/4 通过、无跳过 |
| 生产构建（含 TypeScript） | 通过 |
| preview 权限边界审计 | 通过；109 模块、101 可达 |

完整入口在中断夹具最终修正前启动，失败是该夹具误用已合法路由的图，导致
“应存在非法边”的断言失败；最终改用 `G.build` 的未路由图后 8/8 复测通过。
跳过项是沙箱阻止标准 Chromium 启动，已在宿主用现有 headless-shell 补跑。
没有再次执行 20 分钟完整入口，不能把这次运行改写成一次全绿结果。
本轮没有修改后端，未重复前轮完整 Python 回归。

日志和有限实现摘要在 [本轮工件目录](validation/summary-routing-20261101/)。
`implementation-binding.json` 仅绑定修改文件及顶层构建资产，不是完整发行清单。

## 实际浏览器范围

使用 Codex In-app Browser、独立 loopback 服务 `127.0.0.1:8801`。
通过模型库实际打开 42 组模型的全部 43 个配置，每份默认视图的源码和几何
DOM 约束均为 true；观察转录见 [43 配置清单](validation/summary-routing-20261101/browser-smoke.json)。
未逐配置封存截图/DOM，因此它是默认打开检查，不能充当封印的完整视觉矩阵。

MLP 的 Summary 副本实际改名、撤销、重做、保存、刷新后恢复；恢复图为源码
原子前沿 19 节点/15 边，约束通过。它与最初的语义前沿 11/9 分别计数。
编辑 JSON 下载按钮报告成功，但下载文件路径/字节未验证，不计 JSON 重导入通过。
Transformer 默认 82/80 也实际保存并刷新重开，约束通过。

另通过模块展开对话框，将 Encoder 范围依次设为深度 0/1/2/3，实际分别为
52/52、59/58、80/77、87/87（节点/边）；各次源码与布局约束通过。
深度 3 的撤销恢复 80/77，重做恢复 87/87，约束均通过。
该 87/87 视图实际保存并刷新重开，约束仍通过。
浏览器深度 3 的 `data-frontier-ms=1171`，worker 总计 976 ms、render 4.90 ms；
这些是命令/DOM 阶段耗时，不是输入到最终呈现耗时。

MLP 180 mm SVG/PDF、85 mm SVG，以及 Transformer 180/85 mm SVG 已从真实
导出对话框生成；[五份实际导出](validation/summary-routing-20261101/exports.json)
核对文件 SHA-256 与导出收据一致，SVG 物理宽度一致。
它们的 `sourceBindingVerified=false`：预览身份由浏览器声明，不能声称已完成
后端 Python 源码绑定证明。PDF 字形覆盖报告通过，也不等于目标阅读器或印样审看。

### 完整矩阵尚未通过的具体原因

- [历史 36+3 协议](browser-visual-matrix-protocol.md)针对正式 `.publication-scene`
  和旧九个前沿；当前默认界面使用 Summary iframe，前沿标识和几何不同。
- 当前实际界面没有找到旧协议的全局黑白预设。不能用旧 core 生成的 36 张图
  冒充当前浏览器采集；本轮生成的 formal gold 只作为旧管线候选。
- 只有 IAB 浏览器可控；没有完成独立 Chrome、Firefox、WebKit 的交互、重开及导出矩阵。
- 尚未逐配置采集交互/截图/编辑 JSON 重导入和双宽度导出；字体、浏览器版本与
  固定硬件环境未锁定。一次 Runtime.evaluate 超时已通过重新观察恢复，未计为测得延迟。

后续应先建立 Summary 版前沿/预设/物理尺寸协议和采集器，再收集全矩阵；
不要覆盖旧 spec、收据或哈希来获得通过。

## 性能与出版门

[引擎基准](validation/summary-routing-20261101/engine-performance.json)包含真实模型：
Transformer 默认构建 5,914.34 ms，Encoder 深度 0–3 为 1,786.67 / 1,237.99 /
1,469.23 / 1,316.82 ms，均严格通过且 pending/failed 为 0。
移动 34.24 ms，独立校验 17.06 ms；MLP 默认 133.39 ms。
单次运行、同机有其他负载，不是固定硬件 A/B、p95 或呈现 FPS。

原 `PerfBenchmarkPanel.tsx` 和 `nativePerformance.ts` 在当前 App 不可达，且旧
observer 读取 `.publication-scene`；仅加 `?benchmark=1` 不能采集当前 Summary。
需要适配 iframe 的真实输入、异步提交、可见性和帧呈现测量，再按原门限做
固定环境重复采样；不能把引擎、DOM 或 rAF 频率替代实际 presented FPS。

真实预检：Transformer 整图 180 mm 最小字 3.82 pt、85 mm 为 1.80 pt；
MLP 编辑后的原子前沿 180 mm 为 6.47 pt。均低于 7 pt 起点建议。
Transformer 建议页宽 330 mm、页高约 765.9 mm，也未获得目标版面批准。
因此本轮不认证 85/180 mm 出版通过。

## 真实宿主和真人状态

| 门 | 状态/下一步 |
|---|---|
| Codex 独立安装 Skill Agent E2E | CLI 已存在，但 `codex login status` 未登录；本次桌面 Agent 的本地操作单列，不替代独立宿主测试 |
| Claude Code E2E | 未发现可用执行器/认证，待具备宿主后运行 |
| 官方 DeepSeek Harness E2E | 已核对官方 Harness 可启动帮助；没有调用模型。按用户“仅本地测试”决定保留待办 |
| 真人任务/出版 | 参与者 0、分配 0、收集 0；不由 AI 填写真人结果 |

三席冻结准备包位于 `/tmp/archcanvas-acceptance-20261101/human-trial`，8811–8813
在检查时可用；`human-readiness-host.json` 只证明文件绑定和端口准备。
包仍使用旧正式 Canvas 基线，**需要先适配当前 Summary 任务和收集合同，不能直接
发给真人并声称流程已验收**。不得让自动化使用真人席位或修改空白 reviewer 模板。

适配后的人工操作须按 [研究协议](m4-research-protocol.md)记录真实环境、真实参与者、
五项任务及全部失败/放弃分母，再由独立审看者检查 85/180 mm 真实尺寸工件。
任务时间 ≤180 秒、成功率 ≥80% 的门保持开放。发布/新候选版没有在本轮执行。

## 远端 CI

基线 push 已触发 [Actions #52](https://github.com/t12131219/ArchCanvas-Model-Architecture-Studio/actions/runs/41279569549)，
不是“尚未运行”。该 run 绑定 `b993841`，不包含本轮未提交路由修改。
最终为 **Failure，33 分 47 秒**。公开错误注释定位到 step 8（Full frontend
regression）exit 1；具体失败测试的日志需要 GitHub 登录，尚未取得，不能推断
它与本机失败是同一原因。后续 Python 和 inventory 没有形成可用工件。

本地工作流已补齐前后端测试的 tee 日志，保留 Bash pipefail，并将 inventory
改为 `always()` 运行；上传诊断包含测试日志和索引，避免前序失败后仅上传不存在
的索引。没有隐藏测试失败、放宽断言或触发新的远端执行；这些工作流修改仅完成
本地结构/管道语义核验，仍待下一次获授权的远端运行。
