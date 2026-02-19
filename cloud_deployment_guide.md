# ☁️ TON空投Bot - 云端部署指南

## 🎯 为什么需要云端部署？

### 当前问题（本地运行）：
```
❌ 关机即停止
❌ 断网无法用
❌ 重启需手动
❌ 无法24/7运行
❌ 依赖本地网络
```

### 云端部署优势：
```
✅ 24/7不间断运行
✅ 不受本地关机影响
✅ 专业网络环境
✅ 自动备份和恢复
✅ 可扩展性强
✅ 成本可控（$5-10/月）
```

## 🚀 推荐部署方案

### 方案1：腾讯云/阿里云轻量服务器（最推荐）
```
价格: ¥30-50/月 ($5-8/月)
配置: 1核1G/2G内存，40G SSD
优势: 国内访问快，管理简单
适合: 中小规模用户（支持1000+用户）
```

### 方案2：VPS（DigitalOcean/Vultr）
```
价格: $5-10/月
配置: 1核1G/2G内存，25G SSD
优势: 国际网络好，教程丰富
适合: 国际用户较多的情况
```

### 方案3：云函数（Serverless）
```
价格: 按使用量计费（可能免费）
配置: 无需管理服务器
优势: 无需运维，自动扩缩容
适合: 初期测试，成本敏感
缺点: 冷启动延迟，配置复杂
```

### 方案4：Raspberry Pi（树莓派）
```
价格: ¥300-500一次性
配置: 4核4G内存，自备电源
优势: 完全控制，学习价值高
适合: 技术爱好者，长期运行
缺点: 需要网络和电力保障
```

## 📋 部署前准备

### 1. 代码整理
```
确保以下文件完整：
• bot_framework.py
• run_bot.py
• config.py
• requirements.txt
• 所有文档文件
```

### 2. 配置检查
```
config.py 中的Token正确
requirements.txt 依赖完整
日志路径配置正确
数据库连接（如有）配置
```

### 3. 数据备份
```
本地运行日志备份
用户测试数据备份
配置文件备份
```

## 🔧 腾讯云部署步骤（推荐）

### 步骤1：购买服务器
```
1. 访问腾讯云官网
2. 选择"轻量应用服务器"
3. 选择配置：1核2G内存，40G SSD
4. 选择系统：Ubuntu 20.04/22.04
5. 购买（约¥35/月）
```

### 步骤2：连接服务器
```bash
# 使用SSH连接
ssh root@你的服务器IP

# 或使用腾讯云控制台VNC
```

### 步骤3：环境配置
```bash
# 更新系统
apt update && apt upgrade -y

# 安装Python
apt install python3 python3-pip -y

# 安装Git
apt install git -y

# 创建项目目录
mkdir -p /opt/ton-bot
cd /opt/ton-bot
```

### 步骤4：上传代码
```bash
# 方法1：使用Git（推荐）
git clone 你的仓库地址 .

# 方法2：使用SCP上传
# 在本地执行：
scp -r TON_Airdrop_Bot/* root@服务器IP:/opt/ton-bot/
```

### 步骤5：安装依赖
```bash
cd /opt/ton-bot
pip3 install -r requirements.txt
```

### 步骤6：配置运行
```bash
# 测试运行
python3 run_bot.py

# 如果正常，配置守护进程
```

### 步骤7：使用systemd守护进程
```bash
# 创建服务文件
cat > /etc/systemd/system/ton-bot.service << EOF
[Unit]
Description=TON Airdrop Dashboard Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ton-bot
ExecStart=/usr/bin/python3 /opt/ton-bot/run_bot.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ton-bot

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
systemctl daemon-reload
systemctl enable ton-bot
systemctl start ton-bot

# 查看状态
systemctl status ton-bot
```

## 📊 成本分析

### 腾讯云轻量服务器
```
月费: ¥35-50
年费: ¥420-600（常有优惠）
流量: 1TB/月（足够）
备份: 免费快照
```

### 其他成本
```
域名: ¥50/年（可选）
SSL证书: 免费（Let's Encrypt）
监控: 免费基础监控
```

### 与本地运行对比
```
本地运行:
• 电费: ¥30-50/月（电脑24小时）
• 硬件损耗: 无法计算
• 网络要求: 公网IP或内网穿透
• 维护成本: 个人时间

云端运行:
• 服务器费: ¥35/月
• 无需担心断电断网
• 专业运维环境
• 可随时扩展
```

## 🛡️ 安全配置

### 基础安全
```bash
# 修改SSH端口
sed -i 's/#Port 22/Port 你的端口/' /etc/ssh/sshd_config

# 禁用root登录
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 配置防火墙
ufw allow 你的SSH端口
ufw enable

# 定期更新
apt update && apt upgrade -y
```

### Bot安全
```
1. Token保密: 不要提交到公开仓库
2. 日志管理: 定期清理，避免敏感信息
3. 访问控制: 限制管理接口访问
4. 备份策略: 定期备份配置和数据
```

## 📈 监控和维护

### 基础监控
```bash
# 查看Bot状态
systemctl status ton-bot

# 查看日志
journalctl -u ton-bot -f

# 查看资源使用
top
htop
df -h
```

### 日志管理
```bash
# 日志轮转配置
cat > /etc/logrotate.d/ton-bot << EOF
/opt/ton-bot/ton_bot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF
```

### 备份策略
```bash
# 每日备份脚本
cat > /opt/ton-bot/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/ton-bot-backup-$DATE.tar.gz \
    /opt/ton-bot/config.py \
    /opt/ton-bot/*.py \
    /opt/ton-bot/*.md \
    /var/log/ton-bot.log

# 保留最近7天备份
find $BACKUP_DIR -name "ton-bot-backup-*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/ton-bot/backup.sh
```

## 🚀 快速部署脚本

### 一键部署脚本
```bash
#!/bin/bash
# ton-bot-deploy.sh

echo "TON空投Bot一键部署脚本"
echo "=========================="

# 安装依赖
apt update
apt install -y python3 python3-pip git

# 下载代码
cd /opt
git clone https://你的仓库地址 ton-bot
cd ton-bot

# 安装Python依赖
pip3 install -r requirements.txt

# 配置服务
cat > /etc/systemd/system/ton-bot.service << EOF
[Unit]
Description=TON Airdrop Dashboard Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ton-bot
ExecStart=/usr/bin/python3 /opt/ton-bot/run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl enable ton-bot
systemctl start ton-bot

echo "部署完成！"
echo "查看状态: systemctl status ton-bot"
echo "查看日志: journalctl -u ton-bot -f"
```

## 🔄 迁移指南

### 从本地迁移到云端
```
1. 备份本地所有文件
2. 购买云服务器
3. 上传代码到服务器
4. 安装依赖和配置
5. 测试运行
6. 切换DNS或通知用户
7. 关闭本地Bot
```

### 注意事项
```
• 确保Token在云端config.py中正确
• 测试所有功能是否正常
• 监控初期运行状态
• 准备回滚方案
```

## 🆘 故障排除

### 常见问题
```
1. Bot无法启动: 检查Python版本和依赖
2. 无法连接Telegram: 检查网络和Token
3. 内存不足: 优化代码或升级配置
4. 日志文件过大: 配置日志轮转
5. 服务自动停止: 检查systemd配置
```

### 紧急恢复
```bash
# 重启服务
systemctl restart ton-bot

# 查看错误日志
journalctl -u ton-bot --since "10 minutes ago"

# 临时运行测试
cd /opt/ton-bot
python3 run_bot.py
```

## 📞 支持资源

### 文档链接
```
• 腾讯云文档: https://cloud.tencent.com/document
• Ubuntu文档: https://ubuntu.com/server/docs
• Python文档: https://docs.python.org
• pyTelegramBotAPI文档: https://github.com/eternnoir/pyTelegramBotAPI
```

### 社区支持
```
• Telegram Bot开发群组
• 腾讯云用户社区
• GitHub Issues
• Stack Overflow
```

---

## 🎯 部署建议

### 初期建议（测试阶段）
```
使用本地运行 + 腾讯云轻量服务器
• 本地: 开发和测试
• 云端: 24/7生产运行
• 成本: ¥35/月
• 稳定性: 高
```

### 中期建议（用户增长）
```
升级到更高配置
• 2核4G内存
• 负载均衡准备
• 数据库分离
• 监控告警系统
```

### 长期建议（规模化）
```
• 容器化部署（Docker）
• 自动化运维（CI/CD）
• 多区域部署
• 专业监控系统
```

---

**部署状态**: 准备就绪  
**推荐方案**: 腾讯云轻量服务器  
**预计成本**: ¥35/月  
**部署时间**: 1-2小时  
**维护需求**: 低（基础监控即可）  

**立即行动**: 购买服务器开始部署！