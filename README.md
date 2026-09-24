# Note API

一个基于 **FastAPI + SQLModel + SQLite** 开发的笔记管理后端项目。

本项目用于练习 FastAPI Web API 开发、数据库 CRUD、ORM、请求参数校验、异常处理以及接口自动化测试。

---

## 项目功能

目前实现了以下功能：

- 创建笔记
- 查询单条笔记
- 查询笔记列表
- 修改笔记
- 删除笔记
- 根据分类筛选笔记
- 根据归档状态筛选笔记
- 分页查询
- 数据持久化到 SQLite
- 404 异常处理
- Pydantic / SQLModel 数据校验
- Response Model 控制返回字段
- 使用 TestClient 进行接口测试

---

## 技术栈

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Pytest
- FastAPI TestClient

---

## 项目结构

```text
Note/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers.py
│   └── test_main.py
│
├── database.db
└── README.md
