# MultiverseNote 快速入门指南

欢迎使用 MultiverseNote！本指南将引导您完成项目的设置和运行步骤，并提供有关自定义配置的详细说明。通过引入 `uv` 工具，整个设置流程已被简化，使工作流更加高效。

---

## 前置要求

在开始之前，请确保您的系统已安装以下内容：

- **Python 3.8+**：用于运行后端和管理脚本。

---

## 安装步骤

### 第一步：安装 `uv`

项目通过 `uv` 工具管理，负责配置和依赖项的处理。运行以下命令安装 `uv`：

```bash
pip install uv
```

### 第二步：同步项目文件

安装 `uv` 后，使用它设置项目。进入项目目录，运行以下命令：

```bash
uv sync
```

此命令将下载并配置所有必要的依赖项和文件。

### 第三步：激活虚拟环境并启动项目

同步完成后，激活由 `uv sync` 创建的虚拟环境。根据您的系统类型，运行以下命令：

- **Linux/macOS**：
  ```bash
  source .venv/bin/activate
  ```
- **Windows**：
  ```bash
  .venv\Scripts\activate
  ```

更多信息，请参考 [Python venv 文档](https://docs.python.org/3/library/venv.html)。

激活虚拟环境后，运行以下命令启动项目：

```bash
python main.py
```

此操作将启动后端并初始化应用程序。

---

## 配置说明

MultiverseNote 支持通过配置文件和模块化组件进行自定义。按照以下步骤更新配置并扩展功能：

### 1. 更新配置文件

配置文件存储在 `storage/config` 目录中。更新或自定义配置的步骤如下：

1. 进入 `storage/config` 目录。
2. 打开需要编辑的配置文件（默认是 `main_config.yaml`）。
3. 根据需求修改配置内容。

#### 配置文件示例（含注释）

```yaml
control:  
  bot:  
    api_key:  # 填入聊天机器人服务的 API 密钥。
    name: OpenAI  # 聊天机器人的名称（例如 OpenAI）。
  tools:  
    - searchOnlineTool  # 聊天机器人可用工具的名称列表。

dao:  
  db:  
    activate: false  # 如果使用数据库，设置为 true；否则为 false。
    db_name: storage/db/db.sqlite  # 数据库文件的路径。
    db_type: sqlite  # 数据库类型（如 sqlite、postgres 等）。
    db_url: null  # 数据库 URL（如果适用）。
    password: null  # 数据库密码（如果适用）。
    user: null  # 数据库用户名（如果适用）。
  file:  
    activate: false  # 如果使用基于文件的存储，设置为 true。
    file_path: storage/file  # 文件存储位置的路径。

runtime:  
  agent_path: storage/agent  # 存储代理配置的目录。
  current_session_id:  # 留空以生成运行时会话 ID。
  history_path: storage/history  # 用于存储对话历史的路径。

view:  
  flask:  
    activate: true  # 启用 Flask 服务器。
    debug: true  # 启用调试模式（用于开发）。
    host: localhost  # Flask 服务器的主机地址。
    port: 5000  # Flask 服务器的端口。
  taipy:  
    activate: false  # 启用 Taipy 前端（设置为 true 时启用）。
```

---

### 2. 添加自定义代理

要添加自定义代理，请按照以下步骤操作：

1. **将代理文件放入 `storage/agent` 目录**：
   - 将代理的配置文件添加到 `storage/agent` 目录中，该文件定义代理的行为和响应。

2. **遵循现有代理文件的结构和命名规则**：
   - 确保一致性，使用与目录中现有代理相同的命名规则和文件结构。这有助于系统正确识别和加载代理。

3. **重启应用程序以加载新代理**：
   - 添加代理后，重启应用程序以确保新代理可用。

#### 代理文件示例（含注释）

```yaml
name: base  # 代理的名称。
args:  
  - query  # 代理所需的参数（例如用户输入 'query'）。
prompt: >  
  ## 参与者简介  
  **姓名**: KK  
  **角色**: 一个乐于助人的助手。  

  ## 用户对话  
  用户忙于工作时，尽量简洁地回答。KK 与用户互动。用户首先说：“{query}”
```

---

### 3. 添加自定义工具

要将新工具集成到应用程序中，需要创建工具文件并遵循特定的开发规范。每个工具必须包括以下内容：

1. **进入 `app/tools` 目录**：所有工具文件都存储在此目录中。
2. **添加工具文件**：在该目录中创建新的 Python 文件，用于定义工具。
3. **定义工具函数**：每个工具以函数形式实现。例如：

   ```python
   def fetch_web_page(url):
       """获取并返回网页内容。"""
       try:
           response = requests.get(url)
           response.raise_for_status()
           return response.text
       except requests.RequestException as e:
           return "无法访问：" + str(e)
   ```

4. **指定输入参数**：清晰定义函数的输入参数，以便 OpenAI 的函数调用系统可以识别。
5. **在映射字典中注册函数**：将函数名与实现进行映射。例如：

   ```python
   FUNCTION_MAPPING = {
       "fetch_web_page": fetch_web_page,  # 将函数名称与其实现映射。
   }
   ```

6. **在 `TOOLS_DEFINE` 中定义工具**：遵循 OpenAI 函数调用格式定义工具，包括名称、描述和输入参数。例如：

   ```python
   TOOLS_DEFINE = [
       {
           "type": "function",
           "function": {
               "name": "fetch_web_page",
               "description": "获取并返回网页内容。",
               "parameters": {
                   "type": "object",
                   "properties": {
                       "url": {
                           "type": "string",
                           "description": "要获取的网页 URL。"
                       }
                   },
                   "required": ["url"]
               }
           }
       }
   ]
   ```

---

## 下一步

完成配置和自定义后，您可以：

- **探索功能**：测试您添加的工具和代理。
- **参与贡献**：查看 GitHub 仓库中的开放问题和任务。
- **协作讨论**：加入社区讨论，分享想法并获得反馈。

---

## 故障排查

如果遇到问题，请检查以下内容：

1. 确保已正确安装 Python 3.8+。
2. 确保成功运行了 `uv sync` 且无错误。
3. 仔细检查配置文件、代理文件和工具文件的结构及命名规则。
4. 查看终端日志中的详细错误信息。
5. 在 GitHub 仓库中提交问题或联系项目维护人员以获得支持。

---

## 结语

感谢您为 MultiverseNote 做出贡献！您的支持将帮助我们扩展和改进此项目。如需进一步帮助，请联系我们或参考文档。

祝您开发愉快！🚀