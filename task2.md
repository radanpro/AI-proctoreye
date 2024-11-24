### **المهمة الثانية: تعرف الأشخاص من الفيديوهات أو كاميرات المراقبة**

#### **الهدف:**

إضافة خاصية جديدة للنظام تتيح التعرف على الأشخاص من خلال الفيديوهات أو الكاميرات، مع ضمان عدم تعديل الكود السابق والاكتفاء بدمج الخاصية الجديدة كإضافة مستقلة.

---

### **الأعضاء والمسؤوليات**

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; text-align: left;">
  <thead style="background-color: #5A5252FF;">
    <tr>
      <th style="padding: 10px; border: 1px solid #ddd;">الأعضاء</th>
      <th style="padding: 10px; border: 1px solid #ddd;">المهمة</th>
      <th style="padding: 10px; border: 1px solid #ddd;">الملف/الموقع</th>
      <th style="padding: 10px; border: 1px solid #ddd;">الوصف</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">مالك وعبدالعزيز</td>
      <td style="padding: 10px; border: 1px solid #ddd;">تطوير واجهة لتحليل الفيديو أو البث المباشر</td>
      <td style="padding: 10px; border: 1px solid #ddd;">`frontend/`</td>
      <td style="padding: 10px; border: 1px solid #ddd;">- إنشاء صفحة React جديدة لرفع الفيديوهات أو تشغيل الكاميرا.<br>- تصميم زر لمعالجة البيانات وإرسالها للواجهة الخلفية.<br>- عرض تأثيرات بصرية أثناء معالجة الفيديو. <br> - تصميم صفحة لعرض النتائج (هوية الشخص أو "غير معروف").<br>- إضافة زر لإعادة المحاولة لرفع فيديو جديد أو تشغيل الكاميرا.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">عبدالرحمن</td>
      <td style="padding: 10px; border: 1px solid #ddd;">إنشاء API لتحليل الفيديو</td>
      <td style="padding: 10px; border: 1px solid #ddd;">`ProctorEye/api/routes/video_analysis.py`</td>
      <td style="padding: 10px; border: 1px solid #ddd;">- إنشاء API يتلقى الفيديوهات والصور.<br>- التكامل مع الكلاسات الجديدة لتحليل الفيديو وتحسين الصور وإجراء المطابقة.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">هادي</td>
      <td style="padding: 10px; border: 1px solid #ddd;">تحليل الفيديو واستخراج الإطارات</td>
      <td style="padding: 10px; border: 1px solid #ddd;">`ProctorEye/api/services/` Ex. `video_processor.py`</td>
      <td style="padding: 10px; border: 1px solid #ddd;">- كتابة كود لتحليل الفيديو باستخدام OpenCV.<br>- استخراج الإطارات ذات الجودة العالية التي تحتوي على وجوه واضحة.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">مصعب</td>
      <td style="padding: 10px; border: 1px solid #ddd;">تحسين جودة الصور</td>
      <td style="padding: 10px; border: 1px solid #ddd;">`ProctorEye/api/services/` Ex. `image_enhancer.py`</td>
      <td style="padding: 10px; border: 1px solid #ddd;">- تطبيق تقنيات Super-Resolution لتحسين دقة الصور المستخرجة.<br>- ضمان توافق الصور مع متطلبات التعرف على الوجه.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">هادي وعبدالرحمن</td>
      <td style="padding: 10px; border: 1px solid #ddd;">إنشاء كلاس للمطابقة الجماعية</td>
      <td style="padding: 10px; border: 1px solid #ddd;">`ProctorEye/api/services/` Ex. `face_matcher.py`</td>
      <td style="padding: 10px; border: 1px solid #ddd;">- جلب متجهات الوجه المخزنة من قاعدة البيانات.<br>- استخدام مكتبة FAISS لإجراء المطابقة السريعة بين المتجهات.</td>
    </tr>
  </tbody>
</table>

---

### **تفاصيل الواجهات**

#### **1. واجهة `VideoAnalysis` (مالك وعبدالعزيز):**

- **المكونات الرئيسية:**
  - **مربع عرض الفيديو:** يعرض البث المباشر من الكاميرا باستخدام مكتبة مثل `react-webcam` أو الفيديو المرفوع باستخدام عنصر HTML `<video>`.
  - **زر "Capture":** يقوم بتشغيل عملية استخراج الإطارات.
  - **تأثير بصري:** يتم عرضه على الفيديو (مثل ماسح ضوئي أفقي) للإشارة إلى أن الفيديو قيد المعالجة. يمكن استخدام مكتبة `Lottie` أو تأثيرات CSS المخصصة لتصميم الماسح.
- **ما يحدث عند الضغط على زر "Capture":**

  - يتم تعطيل الزر لمنع الضغط المتكرر.
  - يظهر التأثير البصري أثناء المعالجة.
  - يتم التقاط الإطارات المناسبة وإرسالها إلى API لتحليلها.

- **التقنيات المستخدمة:**
  - مكتبة `react-webcam` للبث المباشر من الكاميرا.
  - مكتبة `Lottie` أو CSS لإنشاء التأثير البصري (الماسح الضوئي).
  - مكتبة `axios` لإرسال البيانات إلى API.

#### **2. واجهة `VideoResults` (مالك وعبدالعزيز):**

- **المكونات الرئيسية:**
  - **عرض النتائج:**
    - إذا تم التعرف على الشخص: يظهر الاسم والصورة المستخرجة.
    - إذا لم يتم التعرف عليه: تظهر رسالة "غير معروف" مع صورة تم التقاطها.
  - **زر "إعادة المحاولة":** يتيح رفع فيديو جديد أو تشغيل الكاميرا مرة أخرى.
- **التقنيات المستخدمة:**
  - مكتبة `TailwindCSS` لتصميم الواجهة.
  - استخدام عناصر مثل `<table>` أو `<div>` لعرض النتائج بشكل منسق.

---

### **تفاصيل الكلاسات الجديدة**

#### **1. `VideoProcessor`**

- **الملف:** `services/video_processor.py`
- **الوصف:** استخراج الإطارات من الفيديو لتحليلها.
- **الدوال الرئيسية:**
  - `extract_frames(video_path)`:
    - **مدخلات:** مسار الفيديو.
    - **عمليات:**
      - استخدام مكتبة OpenCV لتحليل الفيديو واكتشاف الإطارات التي تحتوي على وجوه.
      - اختيار الإطارات ذات الجودة العالية بناءً على وضوح الوجه.
    - **مخرجات:** قائمة بالإطارات المناسبة.
- **التقنيات المستخدمة:**
  - مكتبة OpenCV لتحليل الفيديو واكتشاف الوجوه.
  - أدوات لتحسين الأداء عند التعامل مع فيديوهات طويلة.

#### **2. `ImageEnhancer`**

- **الملف:** `services/image_enhancer.py`
- **الوصف:** تحسين جودة الصور باستخدام تقنيات Super-Resolution.
- **الدوال الرئيسية:**
  - `enhance_image(image)`:
    - **مدخلات:** صورة ذات جودة منخفضة.
    - **عمليات:**
      - استخدام نموذج Super-Resolution مثل ESRGAN.
      - تحسين الوضوح والتفاصيل في الصورة.
    - **مخرجات:** صورة محسنة.
- **التقنيات المستخدمة:**
  - مكتبة OpenCV لقراءة الصور ومعالجتها.
  - مكتبة ESRGAN أو مكتبة أخرى متخصصة في تحسين الصور.

#### **3. `FaceMatcher`**

- **الملف:** `services/face_matcher.py`
- **الوصف:** مطابقة الوجه المستخرج مع قاعدة بيانات الطلاب باستخدام FAISS.
- **الدوال الرئيسية:**
  - `match_face(face_vector)`:
    - **مدخلات:** متجه الوجه.
    - **عمليات:**
      - مقارنة المتجه مع قاعدة بيانات المتجهات المخزنة باستخدام مكتبة FAISS.
      - تحديد أقرب تطابق بناءً على المسافة.
    - **مخرجات:** بيانات الشخص أو رسالة "غير معروف".
- **التقنيات المستخدمة:**
  - مكتبة FAISS لإجراء المطابقات بكفاءة.
  - قاعدة بيانات مثل MySQL أو PostgreSQL لتخزين المتجهات.

#### **4. API لتحليل الفيديو**

- **الملف:** `routes/video_analysis.py`
- **الوصف:** استقبال الفيديوهات أو الصور وتحليلها باستخدام الكلاسات أعلاه.
- **الدوال الرئيسية:**
  - `analyze_video(video)`:
    - **مدخلات:** فيديو أو صورة.
    - **عمليات:**
      1. استخراج الإطارات باستخدام `VideoProcessor`.
      2. تحسين الإطارات باستخدام `ImageEnhancer`.
      3. مطابقة الإطارات باستخدام `FaceMatcher`.
    - **مخرجات:** اسم الشخص أو رسالة "غير معروف".
- **التقنيات المستخدمة:**
  - إطار عمل FastAPI لتصميم واجهة API مرنة وسريعة.
  - مكتبة Pydantic للتحقق من المدخلات.

---

### **الخطة الزمنية**

- **إعداد المكونات:**

  - تصميم واجهة `VideoAnalysis` لتحميل الفيديوهات والبث المباشر.
  - تطوير كود لتحليل الفيديو واستخراج الإطارات باستخدام OpenCV.

- **تكامل المكونات:**

  - تحسين جودة الصور باستخدام `ImageEnhancer`.
  - إنشاء كود المطابقة الجماعية باستخدام مكتبة FAISS.

- **اختبار وتحسين النظام:**
  - بناء API لتحليل الفيديو وربطه بالكلاسات السابقة.
  - اختبار كامل للواجهة الأمامية والخلفية.

---

### **المصادر الموصى بها**

1. **React WebCam:**

   - [GitHub Repository](https://github.com/mozmorris/react-webcam)
   - لاستخدام الكاميرا مباشرة في المتصفح.

2. **OpenCV:**

   - [Documentation](https://docs.opencv.org/)
   - [Get-Start](https://opencv.org/get-started/)
   - مكتبة لتحليل الصور والفيديو.

3. **Lottie Animations:**

   - [Lottie Files](https://lottiefiles.com/)
   - لإنشاء تأثيرات متحركة.

4. **FAISS:**

   - [Facebook AI Similarity Search](https://faiss.ai/)
   - لإجراء البحث عن الجيران الأقرب بسرعة وفعالية.

5. **ESRGAN:**

   - [Enhanced Super-Resolution GAN](https://github.com/xinntao/ESRGAN)
   - لتحسين جودة الصور باستخدام الذكاء الاصطناعي.

6. **TailwindCSS:**
   - [Documentation](https://tailwindcss.com/)
   - لتصميم الواجهات بشكل سريع وجذاب.
