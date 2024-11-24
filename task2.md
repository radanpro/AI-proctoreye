### **Task 2: Multi-Source Person Identification**

#### **Goal:**

Develop a system to identify individuals using multiple input sources:

1. Video files.
2. Multiple uploaded images.
3. Live camera feeds.
4. Surveillance cameras (network-connected).

---

### **Team Members and Responsibilities**

<table
  style="width: 100%; border: 1px solid #ddd; border-collapse: collapse; text-align: center;"
>
  <thead>
    <tr style="background-color: #3073A3FF; text-align: center;">
      <th style="padding: 10px; border: 1px solid #ddd;">Team Members</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Task</th>
      <th style="padding: 10px; border: 1px solid #ddd;">File/Location</th>
      <th style="padding: 10px; border: 1px solid #ddd;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Malik & Abdulaziz</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Develop frontend for multi-source input
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `frontend/src/pages/VideoAnalysis`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Add a dropdown for selecting input type: Video, Images, Camera,
        Surveillance Camera.<br />- Create forms for uploading files or entering
        camera IPs.<br />- Display a preview for the input source.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Malik & Abdulaziz</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Display results dynamically
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `frontend/src/pages/VideoResults`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Show results based on the input source.<br />- Display person identity
        or "Unknown".<br />- Include details like frames processed and faces
        detected.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Hadi</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Develop VideoProcessor for input processing
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `ProctorEye/api/services/video_processor.py`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Process video files and extract frames.<br />- Handle multiple
        uploaded images.<br />- Manage live camera feeds and connect to
        surveillance cameras.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Musab</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Enhance extracted frames
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `ProctorEye/api/services/image_enhancer.py`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Apply Super-Resolution to enhance image quality.<br />- Optimize for
        low-quality inputs from cameras or videos.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Hadi & Abdulrahman</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Improve face matching
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `ProctorEye/api/services/face_matcher.py`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Adapt FAISS-based matching for inputs from multiple sources.<br />-
        Ensure fast and accurate matching for large datasets.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">Abdulrahman</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        Create multi-source API
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        `ProctorEye/api/routes/video_analysis.py`
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        - Handle input sources: Video, Images, Camera, Surveillance Cameras.<br />-
        Integrate with VideoProcessor, ImageEnhancer, and FaceMatcher.<br />-
        Return dynamic results for each source type.
      </td>
    </tr>
  </tbody>
</table>

---

### **Backend Details**

#### **1. `VideoProcessor`**

- **File:** `services/video_processor.py`
- **Description:** Handles video and image input processing.
- **New Functions:**
  - `process_video(video_path)`: Extracts frames from video files.
  - `process_images(image_list)`: Processes multiple uploaded images.
  - `process_camera_feed(camera_ip)`: Manages live feed from cameras.
- **Techniques:**
  - Use OpenCV for frame extraction and image conversion.
  - Handle RTSP streams for surveillance cameras.

---

#### **2. `LiveStreamHandler`**

- **File:** `services/live_stream_handler.py`
- **Description:** Manages live camera feeds and connections to surveillance cameras.
- **New Functions:**
  - `connect_to_camera(ip_address)`: Establishes connection to the camera.
  - `fetch_frames()`: Continuously extracts frames from live feeds.

---

#### **3. `ImageEnhancer`**

- **File:** `services/image_enhancer.py`
- **Description:** Enhances image quality for all input sources.
- **Enhancements:**
  - Support for low-resolution images from surveillance cameras.
  - Optimize image enhancement for real-time processing.

---

#### **4. `FaceMatcher`**

- **File:** `services/face_matcher.py`
- **Description:** Matches input faces with database embeddings.
- **Enhancements:**
  - Adapt FAISS for batch matching of frames or multiple images.
  - Support multi-source data without performance degradation.

---

#### **5. API Updates**

- **File:** `routes/video_analysis.py`
- **New Endpoints:**
  - `/analyze_video`: Handles video uploads.
  - `/analyze_images`: Processes multiple uploaded images.
  - `/analyze_camera_feed`: Analyzes live camera feeds or surveillance streams.

---

### **Frontend Details**

#### **Page: `VideoAnalysis`**

- **New Features:**
  - Dropdown menu to select input source:
    - Video upload.
    - Multiple images.
    - Camera feed.
    - Surveillance camera (IP input).
  - Display preview of the selected input source.

#### **Page: `VideoResults`**

- **New Features:**
  - Show results based on input type:
    - Display person name or "Unknown".
    - Include frame counts and detected faces.
  - Retry button to switch source or upload new data.

---

### **Integration Timeline**

1. **Setup Components:**

   - Design multi-source input in `VideoAnalysis`.
   - Add frame processing for live feeds and surveillance cameras.

2. **Integration:**

   - Enhance API for handling multiple sources.
   - Optimize face matching for diverse inputs.

3. **Testing:**
   - Validate functionality for each source type.
   - Ensure smooth transitions between frontend and backend.

---

### **Final Deliverables**

- Multi-source person identification system.
- Support for videos, images, cameras, and surveillance streams.
- Integrated frontend and backend with dynamic result handling.

---

# Arabic

### **المهمة الثانية: التعرف على الأشخاص من مصادر متعددة**

#### **الهدف:**

تطوير نظام للتعرف على الأشخاص باستخدام مصادر متعددة:

1. ملفات الفيديو.
2. مجموعة من الصور المرفوعة.
3. بث مباشر من الكاميرا.
4. كاميرات المراقبة المتصلة بالشبكة.

---

### **الأعضاء والمسؤوليات**

<style>
  td, th {
    border: 1px solid #31B57EFF; /* إطار حول كل خلية */
    padding: 10px;
    border-radius: 5px; /* الزوايا المنحنية */
  }
</style>

<table style="width: 100%; text-align: right; border-collapse: separate; border-spacing: 10px; ">
  <thead >
    <tr style="background-color: #86B7DBFF; text-align: center;">
      <th style="padding: 10px; border: 1px solid #31B57EFF;">الأعضاء</th>
      <th style="padding: 10px; border: 1px solid #31B57EFF;">المهمة</th>
      <th style="padding: 10px; border: 1px solid #31B57EFF;">الملف/الموقع</th>
      <th style="padding: 10px; border: 1px solid #31B57EFF;">الوصف</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2" style="padding: 10px; border: 1px solid #31B57EFF;">مالك وعبدالعزيز</td>
      <td  style="padding: 10px; border: 1px solid #31B57EFF;">تطوير واجهة إدخال متعددة المصادر</td>
      <td rowspan="2" style="padding: 10px; border: 1px solid #31B57EFF;">`frontend/src/pages/` Ex. `VideoAnalysis`</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- إضافة قائمة منسدلة لاختيار نوع الإدخال (فيديو، صور، كاميرا، كاميرات المراقبة).<br>- إنشاء نماذج لرفع الملفات أو إدخال عنوان الـ IP.<br>- عرض معاينة للمصدر المدخل.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">عرض النتائج بشكل ديناميكي</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- عرض النتائج بناءً على نوع المدخل.<br>- عرض هوية الشخص أو "غير معروف".<br>- تضمين تفاصيل مثل عدد الإطارات التي تمت معالجتها وعدد الوجوه المكتشفة.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">هادي</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">تطوير معالجة المدخلات في VideoProcessor</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">`ProctorEye/api/services/video_processor.py`</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- معالجة ملفات الفيديو واستخراج الإطارات.<br>- التعامل مع الصور المرفوعة.<br>- إدارة بث الكاميرات المباشرة والاتصال بكاميرات المراقبة.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">مصعب</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">تحسين جودة الإطارات المستخرجة</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">`ProctorEye/api/services/image_enhancer.py`</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- تطبيق Super-Resolution لتحسين جودة الصور.<br>- تحسين الصور منخفضة الجودة القادمة من الكاميرات أو الفيديوهات.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">هادي وعبدالرحمن</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">تحسين المطابقة الجماعية للوجوه</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">`ProctorEye/api/services/face_matcher.py`</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- تكييف مطابقة الوجه باستخدام FAISS لدعم المدخلات متعددة المصادر.<br>- ضمان سرعة ودقة عالية للمطابقة حتى مع قواعد بيانات ضخمة.</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">عبدالرحمن</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">إنشاء واجهة API متعددة المصادر</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">`ProctorEye/api/routes/video_analysis.py`</td>
      <td style="padding: 10px; border: 1px solid #31B57EFF;">- إدارة المصادر المدخلة: الفيديو، الصور، الكاميرا، كاميرات المراقبة.<br>- التكامل مع VideoProcessor وImageEnhancer وFaceMatcher.<br>- إرجاع النتائج الديناميكية لكل نوع مدخل.</td>
    </tr>
  </tbody>
</table>

---

### **تفاصيل المكونات الخلفية (Backend)**

#### **1. `VideoProcessor`**

- **الملف:** `services/video_processor.py`
- **الوصف:** إدارة معالجة المدخلات من فيديوهات، صور، أو كاميرات مراقبة.
- **الدوال الجديدة:**
  - `process_video(video_path)`: استخراج الإطارات من ملفات الفيديو.
  - `process_images(image_list)`: معالجة مجموعة من الصور المرفوعة.
  - `process_camera_feed(camera_ip)`: التعامل مع البث المباشر من الكاميرات.
- **التقنيات المستخدمة:**
  - مكتبة OpenCV لتحليل الفيديو واستخراج الإطارات.
  - التعامل مع بروتوكول RTSP للاتصال بكاميرات المراقبة.

---

#### **2. `LiveStreamHandler`**

- **ملف جديد:** `services/live_stream_handler.py`
- **الوصف:** إدارة الاتصال بالبث الحي من الكاميرات.
- **الدوال الجديدة:**
  - `connect_to_camera(ip_address)`: إنشاء اتصال مع الكاميرا.
  - `fetch_frames()`: استخراج الإطارات بشكل مستمر من البث.

---

#### **3. `ImageEnhancer`**

- **الملف:** `services/image_enhancer.py`
- **الوصف:** تحسين جودة الصور المستخرجة من جميع المصادر.
- **التحسينات:**
  - دعم الصور منخفضة الجودة من كاميرات المراقبة.
  - تحسين الأداء لمعالجة الصور في الوقت الفعلي.

---

#### **4. `FaceMatcher`**

- **الملف:** `services/face_matcher.py`
- **الوصف:** مطابقة الوجه المستخرج مع قاعدة بيانات الطلاب.
- **التحسينات:**
  - تكييف FAISS لدعم المطابقة الجماعية للإطارات أو الصور.
  - دعم البيانات من مصادر متعددة بدون التأثير على الأداء.

---

#### **5. تحديث API**

- **الملف:** `routes/video_analysis.py`
- **النقاط الجديدة:**
  - `/analyze_video`: استقبال وتحليل الفيديوهات.
  - `/analyze_images`: معالجة مجموعة من الصور.
  - `/analyze_camera_feed`: تحليل البث الحي من الكاميرات.

---

### **تفاصيل الواجهات (Frontend)**

#### **صفحة `VideoAnalysis`**

- **المميزات الجديدة:**
  - قائمة منسدلة لاختيار نوع الإدخال:
    - رفع فيديو.
    - رفع مجموعة صور.
    - بث مباشر من الكاميرا.
    - إدخال عنوان IP لكاميرات المراقبة.
  - عرض معاينة للمصدر المدخل.
  - زر "تحليل" لبدء عملية الفحص.

#### **صفحة `VideoResults`**

- **المميزات الجديدة:**
  - عرض النتائج بناءً على نوع المدخل:
    - عرض هوية الشخص أو "غير معروف".
    - تفاصيل مثل عدد الإطارات أو الصور التي تم تحليلها.
  - زر لإعادة المحاولة أو تغيير المصدر.

---

### **الخطة الزمنية المعدلة**

- **الإعداد:**

  - تطوير واجهة إدخال متعددة المصادر في `VideoAnalysis`.
  - إعداد الاتصال مع الكاميرات.

- **التكامل:**

  - تطوير الكلاسات الجديدة ومعالجة المدخلات.
  - تعديل API لدعم المدخلات المختلفة.

- **الاختبار:**
  - اختبار النظام باستخدام فيديوهات، صور، كاميرات مباشرة، وكاميرات مراقبة.
  - التأكد من دقة الأداء وسرعة المعالجة.

---

### **النتائج النهائية:**

- نظام يدعم التعرف على الأشخاص من مصادر متعددة.
- تكامل كامل بين الواجهة الأمامية والخلفية.
- تحسين الأداء مع دعم مصادر الإدخال المختلفة.
