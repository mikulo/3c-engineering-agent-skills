# Agent Skills

面向不同 Agent 复用的工程提示词技能集合。每个技能独立放在以技能名和版本号命名的根目录中，内容遵循 Agent Skills 的 `SKILL.md` 结构。

## 技能

| 技能 | 版本 | 适用场景 |
|---|---:|---|
| [bom-check-v1-0-0](bom-check-v1-0-0/SKILL.md) | 1.0.0 | 3C BOM 表只读审核，以及 Excel 与 STP/STEP 装配核对 |
| [translator-v1-0-0](translator-v1-0-0/SKILL.md) | 1.0.0 | 多语言翻译，支持 `eng`、`kr`、`jp`、`eu`、`fr` 前缀 |
| [structural-design-v1-0-0](structural-design-v1-0-0/SKILL.md) | 1.0.0 | 3C 产品结构设计与工程评审 |
| [part-naming-v1-0-0](part-naming-v1-0-0/SKILL.md) | 1.0.0 | 结构零件英文命名 |
| [creo-parametric-official-help-v0-1-0](creo-parametric-official-help-v0-1-0/SKILL.md) | 0.1.0 | Creo Parametric 官方资料核验与设置排障 |

## 版本约定

每个版本使用独立目录，目录名格式为 `<skill-name>-v<major>.<minor>.<patch>`。有不兼容的行为或输出规则变更时递增 major；兼容性扩展递增 minor；修正或澄清递增 patch。保留旧版本目录，便于调用方固定版本。每个版本的 `SKILL.md` 元数据包含对应 `name` 和 `metadata.version`。

技能目录名及 frontmatter `name` 使用小写 ASCII 和连字符，便于不同 Agent 工具链识别；说明与技能正文采用简体中文。

## 使用
**重要：必须独立安装、独立调用。** 本仓库只是多个技能的集合索引，不是一个可整体安装或调用的汇总技能。无论使用哪种 Agent，都必须把需要的每个技能目录分别作为独立技能安装，并按技能名分别调用；严禁把多个技能合并、打包或安装成一个汇总技能。

将需要的版本目录作为 Agent Skills 加载路径中的独立技能目录。技能入口为该目录下的 `SKILL.md`。

## 许可

当前未指定开源许可。除非另行添加许可文件，公开可见不代表授予复制、修改或再分发权限。
