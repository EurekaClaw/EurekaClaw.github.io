# 浏览器UI界面

## 打开UI界面

### 命令

```bash
# Production — build frontend, open browser, serve on :8080
make open

# Production — build frontend, serve on :8080 (no browser)
make start

# Development — hot-reload Vite on :5173 + Python backend on :7860
make dev

# Or via the CLI directly (serves the last build)
eurekaclaw ui --open-browser
```

自定义端口

```bash
eurekaclaw ui --host 0.0.0.0 --port 8080 --open-browser
```

### 原理

| 模式 | 前端 | 后端 | URL |
|---|---|---|---|
| **Production** (`make start`) | 预构建于 `eurekaclaw/ui/static/` | Python server + API| `http://localhost:8080` |
| **Dev** (`make dev`) | 配备HMR的Vite dev服务器 | Python API 在 `:7860` 端口; Vite 代理： `/api/*` | `http://localhost:5173` |

### 前端构建（当需要更改React代码时）

```bash
make build       # tsc + vite build → eurekaclaw/ui/static/
make typecheck   # type-check only, no output
```

---

## 界面

### 工作区

选择会话时的主视图。包含：

-**代理跟踪**（左）-每个流程一张卡篇（调查·构思·推理·验证·写作）。单击任意卡以打开具有特定于阶段的详细信息的智能体。
-**选项卡**（右）：

| 标签页 | 内容 |
|---|---|
| **Live** | 实时阶段卡片，日志流，运行时思考动画 |
| **Proof** | 定理块，带置信度标签的引理链，反例警告 |
| **Paper** | PDF下载，生成PDF，LaTeX 代码查看（带复制按钮） |
| **Logs** | 完整日志原始输出|

### 技能

浏览、安装和删除技能。左面板显示种子技能；右面板为ClawHub的外部安装面板。每个技能卡显示使用计数和成功率。

### 设置

在UI界面修改 `.env` 环境变量，包括 `MAX_TOKENS_*` 滑块. 修改的结果直接写入 `.env` 文件，并在下一次运行时起作用。详细信息参考 [Token限制](../reference/token-limits.md) 。

### Onboarding

交互式设置向导（首次启动时显示）。指导模型选择、API密钥设置、可选工具和技能安装。可通过右下角的导向按钮随时重新打开。

---

## Session Controls

### Pause / Resume

会话运行时，会出现**暂停验证**按钮。EurekaClaw在下一个引理边界处优雅地停止，并将检查点写入 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`.

暂停时，您可以选择在恢复之前键入反馈：

```
📐 Guide the proof before resuming

Lemma chips: [concentration_bound] [main_result] ...
Textarea: "Use Bernstein instead of Hoeffding for lemma 2"
```

反馈直接注入到下一个理论尝试中。

### 会话列表状态指示器

| 状态 | 标签 |
|---|---|
| Running | 蓝色 `RUNNING` 标签 |
| Pausing | 琥珀色 `PAUSING…` 标签 (闪烁) |
| Paused | 琥珀色 `PAUSED` 标签 |
| Resuming | 绿色 `RESUMING…` 标签 (闪烁) |
| Completed | 绿色 `FINISHED` 标签 |
| Failed | 红色 `FAILED` 标签 |

失败的会话显示**重新启动**按钮，将原始查询带到新运行。

---

## 门控机制

当设置 `--gate auto` 或者 `--gate human` ，UI界面在决策点显示全屏门控机制。

| 门控 | 出现时间 | 您能做什么 |
|---|---|---|
| **Survey** | 如果没有论文能找到 | 添加额外的内容或者搜索项 |
| **Direction** | 构思后出现多个研究方向 | 选择方向或让系统选择 |
| **Theory Review** | 理论推导完成后 | 批准理论研究，或者标记关注点、选择要重新思考的特定引理 |
