# استخدام Python 3.9 كصورة أساسية
FROM python:3.9-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# إنشاء مجلد للملفات المُولدة
RUN mkdir -p generated_files

# تعيين المتغيرات البيئية
ENV FLASK_APP=server.py
ENV FLASK_ENV=production
ENV PORT=8080

# فتح المنفذ
EXPOSE 8080

# تشغيل الخادم
CMD ["python", "server.py"]
