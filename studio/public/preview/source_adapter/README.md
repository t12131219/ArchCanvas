# 源码导入

在仓库根目录按 README 构建并启动 ArchCanvas，然后通过工作台的导入窗口选择 Python 文件或源码目录。入口使用相对模块路径与类名，例如 `models.network:MyModel`；构造参数为静态 JSON。

默认路径由 `archcanvas_summary_semantic` 生成语义 IR，经 `archcanvas_preview` 交给当前画布；不导入、不实例化、不执行用户模型。未知结构保留为待解析区域。源码适配包验证来源摘要、证据位置与端口身份，不接受其提供的任意 SVG/HTML。

原有 legacy adapter 仍用于兼容旧格式；它与当前 Summary 路径有各自的支持范围。各项能力以当前服务的 capabilities 返回值为准。

可在同一导入窗口恢复编辑 JSON 或源码适配包。画布布局和路由保存在当前浏览器，跨机器或端口迁移时应先导出编辑 JSON。视觉连线不会自动写回 Python。
