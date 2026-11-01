# 已退役：旧正式 Canvas 性能采样流程

原 benchmark 面板、native observer、M4 输入 harness、独立控制页及其专属
收据校验器依赖旧正式 Canvas DOM/前沿，已从当前项目删除。
旧 benchmark/study URL 参数不启用当前 Summary 的采样入口。

当前保留的 `studio/src/perf.ts` 是共享工程遥测，仍被 App 的现有操作使用；
它不是已经适配 Summary 异步提交的完整性能验收器。
当前 Summary 引擎诊断可用 `scripts/benchmark_summary_interactions.mjs`；
图上的 `data-frontier-ms`、`data-render-ms` 等仅描述相应阶段耗时。
这些测量不等于浏览器输入到最终呈现、INP 或 presented FPS。

历史实际测量原件（包括失败和节流现象）继续保留，例如
[旧小前沿性能收据](evidence/m4-studio-performance.json)。旧报告不计作当前性能通过。
新性能验收需要在固定环境下绑定真实输入、异步图提交、可见性和实际呈现，
另行适配；删除失效工具不会将这个门改为通过。

见 [开发入口](development.md)及 [清理范围](summary-legacy-cleanup.md)。
