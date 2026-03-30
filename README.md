# Scholarship Dashboard

เว็บแสดงทุนวิจัย/ทุนการศึกษาในประเทศไทย

## 🏗️ สถาปัตยกรรม

```
Pi (Cron) → Subagent Search → GitHub → Railway Deploy
```

## 📁 โครงสร้าง

```
scholarship-updater/
├── app.py                 # Flask app (Railway)
├── database/
│   └── scholarships.json  # ข้อมูลทุน
├── scripts/
│   └── research.py        # Script สำหรับ cron
├── templates/
│   └── index.html         # UI
├── railway.toml           # Railway config
└── requirements.txt
```

## 🚀 วิธีติดตั้ง

### 1. Clone Repo
```bash
git clone https://github.com/Theeratikorn/scholarship-dashboard.git
cd scholarship-dashboard
```

### 2. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

### 3. รัน local
```bash
python app.py
# เปิด http://localhost:5000
```

### 4. Deploy Railway
```bash
railway login
railway init
railway up
```

## ⏰ Cron Job (บน Pi)

```bash
# แก้ไข crontab
crontab -e

# เพิ่มบรรทัดนี้ (ทุกวัน 9.00 น.)
0 9 * * * cd /home/pi4eiei/scholarship-updater && python3 scripts/research.py && git push
```

## 🔄 Flow การทำงาน

1. **Cron** รัน `research.py` ทุกวัน 9.00 น.
2. **Script** spawns subagent ไปค้นหาทุนใหม่
3. **Subagent** รวบรวมข้อมูล → `database/scholarships.json`
4. **Git push** ขึ้น GitHub
5. **Railway** auto-deploy เมื่อมี push ใหม่

## 📊 แหล่งที่ค้นหา

- NRCT (สำนักงานการวิจัยแห่งชาติ)
- NIA (สำนักงานนวัตกรรมแห่งชาติ)
- NSTDA (สถาบันนโยบายวิทยาศาสตร์)
- มหาวิทยาลัยต่างๆ

## 📝 ข้อมูลทุน

| Field | Type | Description |
|-------|------|-------------|
| title | string | ชื่อทุน |
| provider | string | ผู้ให้ทุน |
| deadline | string | วันปิดรับสมัคร |
| eligibility | string | คุณสมบัติ |
| amount | string | วงเงิน |
| link | string | URL สมัคร |
| category | string | หมวด (research/education/training) |
| field | string | สาขา (mechanical/medical/biomedical) |

## ⚠️ Disclaimer

ข้อมูลในเว็บนี้อาจไม่ถูกต้อง 100%  
โปรดตรวจสอบกับแหล่งที่มาก่อนสมัครทุกครั้ง

## 📜 License

MIT
