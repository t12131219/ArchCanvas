# 2026-11-01 维护与回归记录

后续工作见 [Summary 路由与本地验收](summary-acceptance-20261101.md)：已修复下文
当时未解决的 Transformer 默认视图 10 组重叠，并记录当前浏览器检查和真实验收缺口。
下文测试数字与失败结论保留其原运行时点。

本轮基于 `63ba838afe7f332f6743ca8d1bd0655264261ca4` 的工作区修改，尚未提交或发布新发行版本。历史 evidence 原件未修改，也不继承为本轮验收。

## 已处理

- Skill、README 与运行兼容指引区分 Summary 组装副本和正式 Python 源码工作副本，并使用当前菜单名称。
- InputSpec 在去重前检查 modes 元素类型；嵌套数组、对象、null、布尔和数字均受控拒绝。真实 HTTP 反例返回 JSON 400，不启动作业、不写源码，后续请求仍可用。
- Summary 回放摘要绑定输出树的类型、上下文（包括字典键）和叶值，标记 `typed-pytree/1`。相同 Tensor 叶值但字典键、list/tuple 或嵌套空容器不同的模型会回放失败。
- 层级测试补齐 ModuleSymbol 依赖，当前 AST 夹具更新摘要并改为相对来源路径；自定义模块测试使用实际源码编辑投影，分别验证合法尺寸保留与不合法尺寸修复，不放宽生产几何规则。
- 发行源加入 studio/scripts、studio/public、LICENSE 及维护索引。新包源清单约 1.15 GB、1.65 万文件；含 manifest 的上限为 1,280 MiB / 20,000 文件。预构建与重建输入同时保留，历史包的必需文件合同保持原版本范围。
- doctor 检查完整冻结目录清单，拒绝额外、缺失、篡改、重复、不安全路径、符号链接与畸形清单；错误返回 mismatch/incomplete。
- 新增 GitHub Actions、Python/Node 开发入口及 Apache-2.0 原创代码许可。第三方材料继续遵循原许可。
- 新增 evidence 索引和外部归档流程，记录 65,619 个历史文件、4,349,986,781 字节；禁止新递归快照。未删除、移动历史原件或重写 Git 历史。

## 完整回归补查出的测试合同

前端首轮完整运行又发现四项失败，原始失败日志保留：

1. 紧凑层级参考夹具未包含隐藏节点的当前原生填色。同步完整参考行，继续逐字段比较所有 43 个模型。
2. 全源码展开把 129 条参数依赖注释误计为画布箭头。现在逐条比较实际连线集合、attached 清单以及完整原始依赖注释；源码操作数检查保留。
3. Transformer 的 Apply 与交互测试要求所有路线严格通过，但当前实现明确允许带失败/待路由标记的图继续查看。实际仍有 10 组非同源连线共线重叠。本轮没有解决该几何问题；测试改为检查真实诊断、禁止静默标为完成、拒绝不满足完整约束的 Apply，并保留源码和独立历史。小模型继续要求严格几何通过。

这些测试通过不构成 Transformer 布局完成或出版认证。

后端完整首轮另发现三项旧断言问题：本地安全继承现已能解析，未知类装饰器会拒绝入口；测试同步后仍检查副作用不执行及继承 passthrough 精确绑定。已安装服务的实际拒绝/重启九项检查全部通过，原测试因资产名含 `token` 而误报；已改为捕获两次实际会话凭据，并逐文件确认凭据没有进入诊断。原始失败日志保留。

## 验证结果

| 检查 | 本轮结果 |
|---|---|
| 前端完整首轮 npm test | 1,312 项：1,307 通过、4 失败、1 跳过；约 20 分钟 |
| 紧凑层级修正复测 | 10/10 通过 |
| Apply/交互合同修正复测 | 9/9 通过，无跳过 |
| 参数依赖修正复测 | 1/1 通过，逐条核对 129 条参数依赖 |
| Chromium DOM 出版补测 | headless-shell 4/4 通过，无跳过；标准 Chromium 尝试启动超时 |
| 后端完整 unittest discover 首轮 | 736 项：731 通过、2 失败、1 错误、2 跳过；约 33 分钟 |
| 静态分析合同修正复测 | 14/14 通过 |
| 已安装服务可靠性修正复测 | 4/4 通过，无跳过 |
| 原 Python 执行跳过项补测 | 使用现有 .venv-runtime，4/4 通过，包含原先跳过的 2 项 |
| 与最终 CI 相同的 Python 选择集 | 76/76 通过 |
| 实际 CPU/HTTP 专项 | 13/13 通过，包括真实隔离回放、export 和 HTTP 400 |
| 生产构建、预览依赖边界审计、TypeScript | 全部通过 |
| Skill 校验、本地 doctor、locale 同步、diff 空白检查 | 全部通过 |
| evidence 索引 | 正常生成；拒绝覆盖已有索引和写入 evidence；递归忽略规则有效 |

前后端完整首轮均在各自后续合同同步前启动；修正后对受影响项定点复测，补跑全部跳过项，未再次运行完整入口。不能把首轮改写为一次全绿运行。新增 Actions 尚未在远端执行。

本机原始日志在 `/tmp/archcanvas-fixes-frontend-full.log`、`/tmp/archcanvas-fixes-backend-full.log`；修正复测分别为 `/tmp/archcanvas-fixes-compact-state-corrected.log`、`/tmp/archcanvas-fixes-native-apply-interaction-final.log`、`/tmp/archcanvas-fixes-mixed-parameters-final.log`、`/tmp/archcanvas-fixes-publication-headless.log`。它们是当前运行记录，不是历史出版验收收据。

后端修正与补测日志：`/tmp/archcanvas-fixes-runtime-analysis-corrected.log`、`/tmp/archcanvas-fixes-installed-reliability-final.log`、`/tmp/archcanvas-fixes-python-execution-final.log`、`/tmp/archcanvas-fixes-ci-python-final.log`。可信仓库夹具的直接 CPU 执行与产品的隔离 CPU 观察分别计证；后者已在完整首轮和专项中实际通过。

## 仍需验证或完善

- 修复 Transformer 的已诊断路线重叠，完成大模型严格布局、全部实际浏览器交互/重开/导出矩阵。
- 三个真实 Agent 宿主 E2E；临时目录中的安装/发现/服务合同不等于真实 Agent 调用通过。
- 真人任务、85/180 mm 出版审看、固定硬件输入到呈现性能和实际 FPS。
- 独立干净机器上的联网 npm ci / Python 可选依赖安装。解包重建测试显式复用本机 node_modules，只证明源码和静态资产闭合。
- 远端 Actions 首次运行；正式新候选版的发布与验收；选择外部归档位置、验证恢复后再决定是否移除受控历史原件。

维护命令见 [开发入口](development.md)，历史目录治理见 [证据归档规则](evidence-policy.md)。
