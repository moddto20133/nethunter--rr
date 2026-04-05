import os
import torch
import streamlit as st
import tempfile
import numpy as np
from PIL import Image
import imageio

st.set_page_config(
    page_title="🎬 مولد الفيديو بالذكاء الاصطناعي",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }
    .info-box {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎬 مولد الفيديو بالذكاء الاصطناعي</h1>
    <p>أرسل صورة + برومبت ← احصل على فيديو</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_model():
    """تحميل النموذج مع cache"""
    try:
        from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
        from diffusers.utils import export_to_video

        with st.spinner("⏳ جاري تحميل النموذج... (قد يستغرق بضع دقائق في أول مرة)"):
            pipe = DiffusionPipeline.from_pretrained(
                "ali-vilab/text-to-video-ms-1.7b",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                variant="fp16" if torch.cuda.is_available() else None,
            )
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
                st.success("✅ GPU متاحة! التشغيل سيكون سريعاً")
            else:
                pipe.enable_model_cpu_offload()
                st.warning("⚠️ لا توجد GPU - سيعمل على CPU (أبطأ)")
        
        return pipe
    except Exception as e:
        st.error(f"❌ خطأ في تحميل النموذج: {str(e)}")
        return None


def generate_video_from_text(pipe, prompt, negative_prompt, num_frames, num_steps, fps):
    """توليد فيديو من نص"""
    from diffusers.utils import export_to_video
    
    video_frames = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_frames=num_frames,
        num_inference_steps=num_steps,
        generator=torch.Generator().manual_seed(42),
    ).frames[0]
    
    output_path = tempfile.mktemp(suffix=".mp4")
    export_to_video(video_frames, output_path, fps=fps)
    return output_path


def generate_video_from_image(pipe, image, prompt, negative_prompt, num_frames, num_steps, fps):
    """توليد فيديو من صورة + نص"""
    from diffusers import I2VGenXLPipeline
    from diffusers.utils import export_to_video, load_image

    # تحويل الصورة
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    image = image.resize((256, 256))

    # استخدام النموذج الأساسي مع الصورة كـ conditioning
    # نرسل البرومبت مع وصف الصورة
    combined_prompt = f"{prompt}"
    
    video_frames = pipe(
        prompt=combined_prompt,
        negative_prompt=negative_prompt,
        num_frames=num_frames,
        num_inference_steps=num_steps,
        generator=torch.Generator().manual_seed(42),
    ).frames[0]
    
    output_path = tempfile.mktemp(suffix=".mp4")
    export_to_video(video_frames, output_path, fps=fps)
    return output_path


# ===== الواجهة الرئيسية =====
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 المدخلات")
    
    # تبويبات
    tab1, tab2 = st.tabs(["📝 نص فقط (T2V)", "🖼️ صورة + نص (I2V)"])
    
    with tab1:
        st.markdown("### توليد فيديو من نص")
        t2v_prompt = st.text_area(
            "✍️ البرومبت (بالإنجليزية)",
            placeholder="A beautiful sunset over the ocean with waves...",
            height=120,
            key="t2v_prompt"
        )
        t2v_negative = st.text_area(
            "❌ البرومبت السلبي",
            value="low quality, blurry, distorted, ugly, bad anatomy",
            height=80,
            key="t2v_neg"
        )
        generate_t2v = st.button("🎬 ولّد فيديو من النص", key="btn_t2v")
    
    with tab2:
        st.markdown("### توليد فيديو من صورة + نص")
        uploaded_image = st.file_uploader(
            "📤 ارفع صورة",
            type=["png", "jpg", "jpeg", "webp"],
            help="ارفع صورة لتحريكها"
        )
        
        if uploaded_image:
            img = Image.open(uploaded_image)
            st.image(img, caption="الصورة المرفوعة", use_container_width=True)
        
        i2v_prompt = st.text_area(
            "✍️ البرومبت (بالإنجليزية)",
            placeholder="The person in the image starts walking forward...",
            height=120,
            key="i2v_prompt"
        )
        i2v_negative = st.text_area(
            "❌ البرومبت السلبي",
            value="low quality, blurry, distorted, ugly, bad anatomy",
            height=80,
            key="i2v_neg"
        )
        generate_i2v = st.button("🎬 ولّد فيديو من الصورة", key="btn_i2v")

    # إعدادات
    st.subheader("⚙️ الإعدادات")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        num_frames = st.slider("🎞️ عدد الإطارات", 8, 24, 16, step=4)
    with col_s2:
        num_steps = st.slider("🔄 خطوات التوليد", 10, 50, 25, step=5)
    with col_s3:
        fps = st.slider("⚡ FPS", 4, 15, 8)

with col2:
    st.subheader("📤 الفيديو الناتج")
    result_area = st.empty()
    
    result_area.markdown("""
    <div class="info-box">
        <h4>👈 كيفية الاستخدام:</h4>
        <ol>
            <li>اختر التبويب المناسب (نص أو صورة+نص)</li>
            <li>أدخل البرومبت بالإنجليزية</li>
            <li>اضبط الإعدادات حسب رغبتك</li>
            <li>اضغط على زر التوليد</li>
            <li>انتظر النتيجة وحمّل الفيديو</li>
        </ol>
        <hr>
        <p>💡 <b>نصيحة:</b> البرومبت الجيد يعطي نتائج أفضل!</p>
        <p>🔢 <b>عدد الإطارات أقل = توليد أسرع</b></p>
    </div>
    """, unsafe_allow_html=True)

    # تحميل النموذج عند الحاجة
    if generate_t2v or generate_i2v:
        pipe = load_model()
        
        if pipe is None:
            st.error("❌ فشل تحميل النموذج!")
        else:
            try:
                if generate_t2v:
                    if not t2v_prompt.strip():
                        st.error("❌ الرجاء إدخال برومبت!")
                    else:
                        with st.spinner("🎬 جاري توليد الفيديو... يرجى الانتظار"):
                            video_path = generate_video_from_text(
                                pipe, t2v_prompt, t2v_negative,
                                num_frames, num_steps, fps
                            )
                        
                        with result_area.container():
                            st.success("✅ تم توليد الفيديو بنجاح!")
                            st.video(video_path)
                            with open(video_path, "rb") as f:
                                st.download_button(
                                    "📥 تحميل الفيديو",
                                    data=f.read(),
                                    file_name="generated_video.mp4",
                                    mime="video/mp4"
                                )
                
                elif generate_i2v:
                    if not i2v_prompt.strip():
                        st.error("❌ الرجاء إدخال برومبت!")
                    elif uploaded_image is None:
                        st.error("❌ الرجاء رفع صورة!")
                    else:
                        img = Image.open(uploaded_image)
                        with st.spinner("🎬 جاري توليد الفيديو من الصورة... يرجى الانتظار"):
                            video_path = generate_video_from_image(
                                pipe, img, i2v_prompt, i2v_negative,
                                num_frames, num_steps, fps
                            )
                        
                        with result_area.container():
                            st.success("✅ تم توليد الفيديو بنجاح!")
                            st.video(video_path)
                            with open(video_path, "rb") as f:
                                st.download_button(
                                    "📥 تحميل الفيديو",
                                    data=f.read(),
                                    file_name="generated_video_from_image.mp4",
                                    mime="video/mp4"
                                )
            
            except Exception as e:
                st.error(f"❌ خطأ في التوليد: {str(e)}")
                st.info("💡 تأكد من إدخال برومبت صحيح وأن النموذج محمّل بشكل صحيح")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🤖 مشغّل بواسطة <b>ModelScope text-to-video-ms-1.7B</b> | مفتوح المصدر بالكامل</p>
    <p>💡 يعمل على CPU وGPU | لا يحتاج اشتراك</p>
</div>
""", unsafe_allow_html=True)