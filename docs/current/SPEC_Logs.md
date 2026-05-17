# SPEC_Logs - 日志设计规范

## 1. 概述

本文档详细描述了 AI-EXAM-BASE-PYTHON 系统的日志记录机制和配置规范。系统采用 Python `logging` 模块作为日志框架，提供控制台输出和文件滚动存储功能，确保系统运行状态的可追溯性和问题诊断能力。

## 2. 配置文件

日志框架使用 Python 标准库 `logging`，可在 `config.py` 中配置。

## 3. 默认级别

- **生产环境**: INFO
- **开发环境**: DEBUG (可配置)

## 4. 日志存储策略

### 4.1 存储位置

- **默认路径**: `backend/logs/` 目录
- **可配置**: 通过 `LOG_PATH` 环境变量指定
- **创建**: 应用启动时自动创建 `logs` 目录

### 4.2 文件滚动策略

- **时间滚动**: 按天滚动，每天生成新的日志文件
- **大小滚动**: 当单个文件超过 10MB 时滚动
- **保留数量**: 最多保留 10 个归档文件
- **压缩格式**: 归档文件以 gzip 格式压缩

### 4.3 文件命名规则

- **当前日志**: `app.log`
- **归档日志**: `app-YYYY-MM-DD-N.log.gz`
  - `YYYY-MM-DD`: 日期
  - `N`: 序号 (1, 2, 3...)

> **注意**: 日志文件位于 `backend/logs/` 目录下。

## 5. 日志记录规范

在 Python 代码中使用标准 `logging` 模块：

```python
import logging

# 获取 logger
logger = logging.getLogger(__name__)

# 记录日志
logger.info("Some operation completed")
logger.debug("Detailed debug information")
logger.error("An error occurred", exc_info=True)
```

### 5.1 日志配置示例

在 `config.py` 或应用初始化文件中配置：

```python
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setup_logging(app):
    """配置应用日志"""

    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 日志级别
    log_level = logging.DEBUG if app.debug else logging.INFO

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 文件处理器（按时间滚动）
    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        when='midnight',
        interval=1,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)

    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
```

## 6. 日志级别使用指南

| 级别 | 使用场景 |
|------|----------|
| DEBUG | 调试信息，仅开发环境使用 |
| INFO | 常规操作信息，如启动、关闭、请求处理 |
| WARNING | 警告信息，如配置缺失、参数不完整 |
| ERROR | 错误信息，如异常捕获、数据库连接失败 |
| CRITICAL | 严重错误，如系统无法继续运行 |

## 7. 敏感信息处理

- **禁止记录**: 密码、Token、密钥、身份证号、银行卡号等敏感信息
- **脱敏处理**: 如需记录用户输入，对敏感字段进行脱敏

```python
# 错误示例
logger.info(f"User login: username={username}, password={password}")

# 正确示例
logger.info(f"User login: username={username}")
```

## 8. 日志格式

推荐日志格式：

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

输出示例：

```
2026-05-16 10:00:00 - app.services.auth - INFO - User logged in successfully
2026-05-16 10:00:01 - app.api.v1.users - ERROR - Database connection failed
```

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
