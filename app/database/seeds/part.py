"""
Database seed logic for parts.
"""
from app.repositories.part import PartRepository
from datetime import datetime

class PartSeeder:
    """Handle part seed operations."""

    SAMPLE_PARTS = [
        {
            "part_number": "91310A235",
            "part_name": "六角頭螺絲",
            "material": "10.9級鋼",
            "status": 1,
            "revision": "1.2.1",
            "updated_at": datetime.strptime("2026/04/05", "%Y/%m/%d"),
            "owner": "William Tai",
            "tolerance": "± 0.15 mm",
            "cad_file_url": "DXF/91310A235.DXF",
            "model_file_url": "GLB/91310A235.glb",
            "description": "用於固定機構外殼的六角頭螺絲，提供高強度的連接性能。",
            "standard": "ISO 4017",
            "specification": "尺寸：M10 x 30 mm，強度等級：10.9，表面處理：鍍鋅",
            "project_code": "PRJ-001",
            "drawing_number": "DRW-91310A235",
        },
        {
            "part_number": "91772A502",
            "part_name": "不銹鋼盤頭十字螺絲",
            "material": "不銹鋼",
            "status": 0,
            "revision": "1.3.2",
            "updated_at": datetime.strptime("2026/04/04", "%Y/%m/%d"),
            "owner": "William Tai",
            "tolerance": "± 0.15 mm",
            "cad_file_url": "DXF/91772A502.DXF",
            "model_file_url": "GLB/91772A502.glb",
            "description": "用於固定機構內部組件的不銹鋼盤頭十字螺絲，具有優異的耐腐蝕性能和強度。",
            "standard": "DIN 933",
            "specification": "尺寸：M8 x 20 mm，強度等級：A2-70，表面處理：無",
            "project_code": "PRJ-001",
            "drawing_number": "DRW-91772A502",
        },
        {
            "part_number": "90031A198",
            "part_name": "鋼製十字槽平頭螺絲",
            "material": "鋼",
            "status": 1,
            "revision": "1.0.0",
            "updated_at": datetime.strptime("2026/04/03", "%Y/%m/%d"),
            "owner": "William Tai",
            "tolerance": "± 0.15 mm",
            "cad_file_url": "DXF/90031A198.DXF",
            "model_file_url": "GLB/90031A198.glb",
            "description": "用於固定木質部件的鋼製十字槽平頭螺絲，提供穩定的連接性能和耐用性。",
            "standard": "ISO 7040",
            "specification": "尺寸：M6 x 25 mm，強度等級：4.8，表面處理：黑色氧化",
            "project_code": "PRJ-002",
            "drawing_number": "DRW-90031A198",
        },
        {
            "part_number": "91271A584",
            "part_name": "鋼製十二角螺絲",
            "material": "鋼",
            "status": 0,
            "revision": "1.1.0",
            "updated_at": datetime.strptime("2026/04/02", "%Y/%m/%d"),
            "owner": "William Tai",
            "tolerance": "± 0.15 mm",
            "cad_file_url": "DXF/91271A584.DXF",
            "model_file_url": "GLB/91271A584.glb",
            "description": "用於固定機構內部組件的鋼製十二角螺絲，具有優異的耐腐蝕性能和強度。",
            "standard": "DIN 912",
            "specification": "尺寸：M5 x 15 mm，強度等級：8.8，表面處理：鍍鋅",
            "project_code": "PRJ-002",
            "drawing_number": "DRW-91271A584",
        },
        {
            "part_number": "91746A116",
            "part_name": "不銹鋼滾花頭蝶形螺絲",
            "material": "不銹鋼",
            "status": 1,
            "revision": "1.0.0",
            "updated_at": datetime.strptime("2026/04/01", "%Y/%m/%d"),
            "owner": "William Tai",
            "tolerance": "± 0.15 mm",
            "cad_file_url": "DXF/91746A116.DXF",
            "model_file_url": "GLB/91746A116.glb",
            "description": "用於固定機構內部組件的不銹鋼滾花頭蝶形螺絲，具有優異的耐腐蝕性能和強度。",
            "standard": "ISO 7040",
            "specification": "尺寸：M4 x 12 mm，強度等級：A2-70，表面處理：無",
            "project_code": "PRJ-003",
            "drawing_number": "DRW-91746A116",
        },
    ]

    @staticmethod
    def seed_all():
        """
        Seed all sample part data. 若資料已存在則略過。
        """
        # 先確保 category 存在
        category_name = "螺絲"
        category = PartRepository.get_category_by_name(category_name)
        if not category:
            category = PartRepository.create_category(category_name)

        added_count = 0
        skipped_count = 0
        for part_data in PartSeeder.SAMPLE_PARTS:
            # 以 part_number 判斷是否已存在
            exists = PartRepository.list()
            if any(p.part_number == part_data["part_number"] for p in exists):
                skipped_count += 1
                continue
            part_data["category_id"] = category.id
            PartRepository.create(**part_data)
            added_count += 1
        return {"added": added_count, "skipped": skipped_count}

    @staticmethod
    def clear_all():
        """
        清除所有 parts 資料。
        """
        count = len(PartRepository.list())
        for part in PartRepository.list():
            PartRepository.delete(part.id)
        return count
