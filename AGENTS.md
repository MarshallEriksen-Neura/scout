# Scout (Crawler Service)

**Python Crawler / Data Ingestion Microservice**

## OVERVIEW
Python 爬虫/数据摄取微服务，负责数据抓取和知识库摄取。

## STRUCTURE
```
scout/
├── app/
│   ├── api/          # API 端点
│   ├── core/         # 核心逻辑
│   ├── services/     # 业务服务
│   └── extractors/  # 数据提取器
├── Dockerfile        # Docker 镜像定义
└── pyproject.toml    # 项目配置
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| API 端点 | `app/api/` |
| 爬虫逻辑 | `app/services/` |
| 数据提取 | `app/extractors/` |

## CONVENTIONS
- Python 3.12+, PEP 8
- FastAPI 框架
- 使用 Playwright 进行网页抓取

## ANTI-PATTERNS
- 禁止在生产环境使用同步阻塞调用

## COMMANDS
```bash
# Docker 构建
docker build -t scout:latest ./scout
```
