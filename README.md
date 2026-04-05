# 🎬 مولد الفيديو بالذكاء الاصطناعي

<div align="center">

![Video Generator](https://img.shields.io/badge/AI-Video%20Generator-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**أرسل صورة + برومبت ← احصل على فيديو 🚀**

</div>

---

## ✨ المميزات

- 🖼️ **صورة + نص → فيديو** (Image to Video)
- 📝 **نص → فيديو** (Text to Video)
- ⚡ **يعمل على CPU و GPU**
- 🆓 **مجاني 100% - مفتوح المصدر**
- 🎛️ **إعدادات قابلة للتخصيص**
- 📥 **تحميل الفيديو مباشرة**

---

## 📦 المتطلبات

- Python 3.10+
- 8GB RAM (16GB مُفضل)
- GPU اختياري (يسرّع التوليد بشكل كبير)
- مساحة ~7GB للنموذج

---

## 🚀 التثبيت والتشغيل

### 1. استنساخ المستودع
```bash
git clone https://github.com/moddto20133/nethunter--rr.git
cd nethunter--rr
```

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. تشغيل التطبيق
```bash
streamlit run app.py
```

---

## 🎯 كيفية الاستخدام

### توليد فيديو من نص:
1. اختر تبويب **"نص فقط (T2V)"**
2. أدخل البرومبت بالإنجليزية
3. اضبط الإعدادات
4. اضغط **"ولّد فيديو"**

### توليد فيديو من صورة:
1. اختر تبويب **"صورة + نص (I2V)"**
2. ارفع الصورة
3. أدخل البرومبت
4. اضغط **"ولّد فيديو من الصورة"**

---

## 💡 نصائح للحصول على أفضل نتائج

- ✅ اكتب البرومبت بالإنجليزية
- ✅ كن تفصيلياً في وصف الحركة
- ✅ استخدم 16-24 إطار للحصول على فيديو أطول
- ✅ زيادة خطوات التوليد تحسن الجودة (لكن تبطئ)

### أمثلة على برومبت جيد:
```
A cat walking gracefully on a wooden floor, cinematic lighting, high quality
A beautiful sunset over the ocean with gentle waves, golden hour lighting
A person smiling and waving their hand, natural background
```

---

## 🤖 النموذج المستخدم

**ModelScope text-to-video-ms-1.7B**
- الحجم: ~7GB
- المعاملات: 1.7B
- يعمل على: CPU + GPU
- المصدر: [HuggingFace](https://huggingface.co/ali-vilab/text-to-video-ms-1.7b)

---

## 📊 متطلبات الأجهزة

| الوضع | RAM | VRAM | الوقت لكل فيديو |
|-------|-----|------|----------------|
| CPU فقط | 16GB | - | 5-15 دقيقة |
| GPU (6GB) | 8GB | 6GB | 1-3 دقيقة |
| GPU (12GB+) | 8GB | 12GB+ | 30-60 ثانية |

---

## 📝 الترخيص

MIT License - مجاني للاستخدام الشخصي والتجاري