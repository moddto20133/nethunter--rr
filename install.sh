#!/bin/bash

echo "🚀 تثبيت مولد الفيديو بالذكاء الاصطناعي..."
echo "================================================"

# تحقق من Python
python3 --version || { echo "❌ Python غير مثبت!"; exit 1; }

# تثبيت torch حسب نوع الجهاز
if command -v nvidia-smi &> /dev/null; then
    echo "✅ GPU متوفرة - تثبيت PyTorch مع CUDA..."
    pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
else
    echo "⚠️ لا توجد GPU - تثبيت PyTorch للـ CPU..."
    pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# تثبيت باقي المكتبات
echo "📦 تثبيت المكتبات..."
pip install -r requirements.txt

echo ""
echo "✅ اكتمل التثبيت!"
echo "🎬 لتشغيل التطبيق:"
echo "   streamlit run app.py"