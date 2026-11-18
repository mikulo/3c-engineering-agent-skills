# Creo 12 `config.pro` 官方资料

## 随附来源

- PDF：`references/creo-12.4.5.0-config-options.pdf`
- 可搜索索引：`references/creo-12.4.5.0-config-options.txt`
- 标题：`Creo 12.4.5.0 Parametric 配置选项`
- 页数：130
- 出版标识：Copyright 2026 PTC Inc.
- SHA-256：`0F623BC1813A3AC5A856D7FC91FCA6952CACF7533F2D96BEA98E4EDFBD3269E1`

索引由 PDF 逐页提取，每页以 `===== PDF PAGE N =====` 标记。索引用于定位，PDF 是原始依据。页码是 PDF 的 1 基页码。

## 检索

在技能目录中运行：

```powershell
python scripts/config_lookup.py "template_solidpart"
python scripts/config_lookup.py "模板 零件" --mode all
python scripts/config_lookup.py "template" --mode phrase --context 10
```

- 已知选项名：用完整英文名检索，命中后读取同一条记录的说明、值和默认值。
- 自然语言问题：先用少量关键词定位候选项，再以候选项完整英文名复查。
- `--mode all` 要求所有查询词出现在同一行或默认 3 行的相邻范围内（可用 `--span` 调整）；`--mode any` 匹配任一词；`--mode phrase` 匹配完整短语。
- 输出只是 PDF 原文上下文。不要根据相邻行猜测字段归属；遇到跨页、断行或列错位时，打开 PDF 对应页核对版面。
- 没有命中时脚本以非零状态退出。这表示“索引中未找到”，不自动证明选项不存在。

## 更新来源

若用户替换了 PDF，可用以下命令重建索引：

```powershell
python scripts/config_lookup.py --rebuild --pdf path\to\config.pdf
```

重建后更新本页的标题、页数、版本和哈希信息，并重新验证代表性选项。不要在未核验版本标识时沿用文件名中的版本。

## 交叉版本规则

- Creo 12 问题：以此 12.4.5.0 PDF 为 `config.pro` 主依据。
- Creo 3 问题：先查版本表中的 PTC 官方 Creo 3.0 配置选项 PDF；本 PDF 只作为 12.4.5.0 对照。
- Creo 4–6 问题：用最近的 Creo 7 官方帮助核验可查到的版本行为，并把本 PDF 作为 12.4.5.0 对照；必须明确这两者都不是目标版本的完整配置清单。
- Creo 7–11、13 问题：必须再查目标版本官方帮助；本 PDF 只说明 12.4.5.0 的状态。
- 目标版本帮助与 PDF 冲突时，目标版本帮助决定该目标版本的结论，并明确列出冲突。
- PDF 只包含 `config.pro` 配置选项，不应用来证明绘图 `.dtl` 详细信息选项。
