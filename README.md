# AIvalux 自动签到

基于 GitHub Actions 的 AIvalux 每日自动签到脚本，完全免费，无需服务器。

## 功能特点

✅ 每天自动签到，领取每日福利  
✅ 完全免费，运行在 GitHub 服务器  
✅ 安全可靠，密码加密存储  
✅ 支持手动触发  
✅ 详细的运行日志  

## 快速开始

### 1. Fork 本项目

点击右上角的 `Fork` 按钮，将项目复制到你的 GitHub 账号下。

### 2. 配置账号密码

在你 Fork 的项目中：

1. 点击 `Settings`（设置）
2. 左侧菜单选择 `Secrets and variables` → `Actions`
3. 点击 `New repository secret` 添加以下两个密钥：

   **第一个密钥：**
   - Name: `AIVALUX_EMAIL`
   - Secret: 你的 AIvalux 账号邮箱（例如：`1444291137@qq.com`）

   **第二个密钥：**
   - Name: `AIVALUX_PASSWORD`
   - Secret: 你的 AIvalux 账号密码（例如：`your_password`）

### 3. 启用 GitHub Actions

1. 点击项目顶部的 `Actions` 标签
2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`
3. 在左侧找到 `AIvalux 自动签到` 工作流
4. 点击 `Enable workflow`（启用工作流）

### 4. 测试运行

为了确保配置正确，建议立即测试一次：

1. 在 `Actions` 页面，点击左侧的 `AIvalux 自动签到`
2. 点击右侧的 `Run workflow` 下拉菜单
3. 点击绿色的 `Run workflow` 按钮
4. 等待几秒钟，刷新页面查看运行结果

✅ **如果显示绿色的勾 ✓，说明配置成功！**  
❌ **如果显示红色的 ×，点击进去查看日志，检查账号密码是否正确**

## 运行时间

- **自动运行**：每天北京时间早上 8:00（UTC 0:00）
- **手动运行**：在 Actions 页面随时手动触发

## 修改运行时间

如果想改变签到时间，编辑 `.github/workflows/checkin.yml` 文件：

```yaml
schedule:
  - cron: '0 0 * * *'  # 北京时间8:00
```

常用时间对照（北京时间 = UTC时间 + 8小时）：

- `'0 0 * * *'` → 北京时间 08:00
- `'0 1 * * *'` → 北京时间 09:00
- `'0 2 * * *'` → 北京时间 10:00
- `'30 23 * * *'` → 北京时间 07:30

## 本地测试

如果想在本地测试脚本：

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/自到签到.git
cd 自到签到

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量并运行
export AIVALUX_EMAIL="你的邮箱"
export AIVALUX_PASSWORD="你的密码"
python checkin.py
```

## 查看运行日志

1. 进入项目的 `Actions` 页面
2. 点击任意一次运行记录
3. 点击 `checkin` 查看详细日志
4. 展开 `执行签到` 步骤，查看完整输出

## 常见问题

### ❓ GitHub Actions 是什么？
GitHub 提供的免费自动化服务，可以定时运行脚本，每月有 2000 分钟的免费额度，签到脚本每天只需几秒钟。

### ❓ 密码安全吗？
非常安全。密码存储在 GitHub Secrets 中，经过加密，只有你的工作流能访问，他人无法查看。

### ❓ 为什么签到失败？
1. 检查账号密码是否正确
2. 检查是否已经签到过（今天已签到会显示"今日已签到"）
3. 查看 Actions 日志中的详细错误信息

### ❓ 能签到多个账号吗？
可以。修改 `checkin.yml`，添加多个步骤，使用不同的 Secret 名称。

### ❓ 如何停止自动签到？
在 Actions 页面，点击工作流名称，右上角三个点 → `Disable workflow`

## 技术栈

- **Python 3.10**：脚本语言
- **requests**：HTTP 请求库
- **GitHub Actions**：自动化执行

## 项目结构

```
自到签到/
├── .github/
│   └── workflows/
│       └── checkin.yml      # GitHub Actions 工作流配置
├── checkin.py               # 签到脚本
├── requirements.txt         # Python 依赖
└── README.md               # 说明文档
```

## 更新日志

### 2026-10-02
- ✨ 初始版本发布
- ✅ 支持自动登录
- ✅ 支持每日签到
- ✅ 支持 GitHub Actions 自动运行

## 免责声明

本项目仅供学习交流使用，使用本项目所产生的一切后果由使用者自行承担。

## 许可证

MIT License

---

⭐ 如果这个项目对你有帮助，欢迎 Star！
