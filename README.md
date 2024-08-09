# FixGithubHosts-windows


## 项目简介

`FixGithubHosts-windows` 是一个用于自动修复中国地区 GitHub hosts 文件的工具。在中国访问 GitHub 时，由于 DNS 解析问题，可能会遇到速度慢或无法访问的情况。本工具旨在通过更新 hosts 文件中的 GitHub 相关条目来解决这一问题。

## 功能特点

- **自动化修复**：一键运行脚本，自动下载最新的 GitHub hosts 文件并增量同步至系统hosts文件
- **错误日志记录**：所有操作和潜在的错误都会被记录到 `AutoRunLog.log` 文件中，便于调试和维护。
- **兼容性**：支持 Windows 操作系统。

## 使用方法

### 前置要求

- 确保你的计算机上安装了 Python（推荐版本 3.6 或以上）。

### 安装与运行

1. 克隆或下载此仓库至本地。
2. 在计划任务配置`AutoFix.bat`用以自动定期修复。

### 手动运行（Python）

1. 点击`AutoFix.bat`可以手动修复Hosts文件
