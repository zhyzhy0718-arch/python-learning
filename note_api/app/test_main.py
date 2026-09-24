from fastapi.testclient import TestClient
from .main import app


def test_create_note():
    with TestClient(app) as client:
        response = client.post(
            "/notes/"
            ,json={
                "title": "作业",
                "content": "数学作业",
                "category":"学习",
                "is_archived":True
            })
        assert response.status_code == 201
        assert response.json()["title"] == "作业"
        assert response.json()["content"] == "数学作业"
        assert response.json()["category"] == "学习"
        assert response.json()["is_archived"] == True


def test_get_note():
    with TestClient(app) as client:
        create_response = client.post(
            "/notes/"
            , json={
                "title": "体育课",
                "content": "引体向上",
                "category": "运动",
                "is_archived": False
            })
        assert create_response.status_code == 201

        note_id = create_response.json()["id"]
        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
        assert response.json()["id"] == note_id

def test_read_note():
    with TestClient(app) as client:

        # 先创建第一条 Note
        response1 = client.post(
            "/notes/",
            json={
                "title": "数学作业",
                "content": "完成高数习题",
                "category": "学习",
                "is_archived": False
            }
        )

        assert response1.status_code == 201

        # 再创建第二条 Note
        response2 = client.post(
            "/notes/",
            json={
                "title": "英语作业",
                "content": "背单词",
                "category": "学习",
                "is_archived": False
            }
        )

        assert response2.status_code == 201

        # 查询所有 Note
        response = client.get("/notes/")

        assert response.status_code == 200

        data = response.json()

        # 返回结果应该是列表
        assert isinstance(data, list)

        # 至少有刚刚创建的两条
        assert len(data) >= 2

    def test_update_note():
        with TestClient(app) as client:
            # 1. 先创建一条 Note
            create_response = client.post(
                "/notes/",
                json={
                    "title": "原来的标题",
                    "content": "原来的内容",
                    "category": "学习",
                    "is_archived": False
                }
            )

            assert create_response.status_code == 201

            created_note = create_response.json()
            note_id = created_note["id"]

            # 2. 更新这条 Note
            update_response = client.patch(
                f"/notes/{note_id}",
                json={
                    "title": "修改后的标题",
                    "is_archived": True
                }
            )

            assert update_response.status_code == 200

            updated_note = update_response.json()

            # 3. 检查修改后的结果
            assert updated_note["id"] == note_id
            assert updated_note["title"] == "修改后的标题"
            assert updated_note["is_archived"] is True

            # PATCH 没传 content，所以应该保持原值
            assert updated_note["content"] == "原来的内容"

def test_delete_note():
    with TestClient(app) as client:

        # 1. 先创建一条 Note
        create_response = client.post(
            "/notes/",
            json={
                "title": "待删除笔记",
                "content": "这条数据马上会被删除",
                "category": "测试",
                "is_archived": False
            }
        )

        assert create_response.status_code == 201

        created_note = create_response.json()
        note_id = created_note["id"]

        # 2. 删除
        delete_response = client.delete(
            f"/notes/{note_id}"
        )

        assert delete_response.status_code == 200

        # 如果你的 DELETE 返回 {"ok": True}
        assert delete_response.json() == {
            "ok": True
        }

        # 3. 再查询一次，确认真的删除了
        get_response = client.get(
            f"/notes/{note_id}"
        )

        assert get_response.status_code == 404