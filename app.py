"""
Scholarship Dashboard - Flask App for Railway
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Database path - Railway จะ mount volume ที่นี่
DATABASE_FILE = Path(__file__).parent / "database" / "scholarships.json"


def load_scholarships():
    """โหลดข้อมูลทุน"""
    if DATABASE_FILE.exists():
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


@app.route("/")
def index():
    """หน้าแรก"""
    scholarships = load_scholarships()
    count = len(scholarships)
    return render_template("index.html", scholarships=scholarships, count=count)


@app.route("/api/scholarships")
def api_scholarships():
    """API สำหรับดึงข้อมูลทุนทั้งหมด"""
    scholarships = load_scholarships()
    return jsonify({
        "success": True,
        "count": len(scholarships),
        "data": scholarships
    })


@app.route("/api/scholarships/filter")
def api_filter():
    """กรองทุนตามประเภท"""
    scholarships = load_scholarships()
    
    category = request.args.get('category')
    field = request.args.get('field')
    
    if category:
        scholarships = [s for s in scholarships if s.get('category') == category]
    if field:
        scholarships = [s for s in scholarships if field.lower() in s.get('field', '').lower()]
    
    return jsonify({
        "success": True,
        "count": len(scholarships),
        "data": scholarships
    })


@app.route("/api/stats")
def api_stats():
    """สถิติ"""
    scholarships = load_scholarships()
    
    # นับตามหมวด
    categories = {}
    for s in scholarships:
        cat = s.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    # นับตามสาขา
    fields = {}
    for s in scholarships:
        field = s.get('field', 'unknown')
        fields[field] = fields.get(field, 0) + 1
    
    return jsonify({
        "total": len(scholarships),
        "by_category": categories,
        "by_field": fields
    })


@app.route("/health")
def health():
    """Health check"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
