#!/usr/bin/env python3
"""
Scholarship Research Script
รันโดย cron บน Pi เพื่อค้นหาทุนใหม่
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent.parent
DATABASE_DIR = SCRIPT_DIR / "database"
SCHOLARSHIP_FILE = DATABASE_DIR / "scholarships.json"
LOG_FILE = SCRIPT_DIR / "logs" / "research.log"

# Create directories
DATABASE_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_existing():
    """โหลดข้อมูลเดิม"""
    if SCHOLARSHIP_FILE.exists():
        with open(SCHOLARSHIP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_scholarships(data):
    """บันทึกข้อมูลทุน"""
    with open(SCHOLARSHIP_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"บันทึก {len(data)} ทุนลง {SCHOLARSHIP_FILE}")


def add_new_scholarships(new_scholarships):
    """เพิ่มทุนใหม่ (ไม่ซ้ำ)"""
    existing = load_existing()
    existing_urls = {s.get('link') or s.get('url') for s in existing}
    
    added = 0
    for scholarship in new_scholarships:
        url = scholarship.get('link') or scholarship.get('url')
        if url and url not in existing_urls:
            scholarship['added_at'] = datetime.now().isoformat()
            existing.append(scholarship)
            existing_urls.add(url)
            added += 1
    
    save_scholarships(existing)
    return added


def get_search_results():
    """ค้นหาทุนจาก web search"""
    search_queries = [
        "ทุนวิจัย วิศวกรรมเครื่องกล 2026 ประเทศไทย",
        "ทุนการศึกษา การแพทย์ มหาวิทยาลัยไทย 2026",
        "scholarship mechanical engineering Thailand NRCT NIA",
        "ทุนนวัตกรรม biomedical Thailand 2026",
        "ทุนวิจัย NRCT NSTDA 2026 วิศวกรรม",
    ]
    
    all_results = []
    for query in search_queries:
        logger.info(f"Searching: {query}")
        # TODO: ใช้ web_search tool
        
    return all_results


def main():
    logger.info("=" * 50)
    logger.info("เริ่มค้นหาทุนใหม่...")
    
    # 1. ค้นหาทุนใหม่
    new_scholarships = get_search_results()
    logger.info(f"พบ {len(new_scholarships)} ทุนใหม่")
    
    # 2. เพิ่มทุนใหม่
    added = add_new_scholarships(new_scholarships)
    logger.info(f"เพิ่ม {added} ทุนใหม่")
    
    # 3. รวมจำนวนทุนทั้งหมด
    total = len(load_existing())
    logger.info(f"จำนวนทุนทั้งหมด: {total}")
    
    logger.info("เสร็จสิ้น!")
    return added


if __name__ == "__main__":
    main()
