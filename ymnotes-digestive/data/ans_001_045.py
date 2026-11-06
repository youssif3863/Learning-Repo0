# -*- coding: utf-8 -*-
# Answer content, chunk 1 (question ids 1-45)
# a(id, correct, tag(M=Internal Medicine, S=Surgery), page('~' prefix = nearest page, None = not in book),
#   anchor phrase on that page, why=(EN,AR), x={wrong letter:(EN,AR)}, p=pearl (EN,AR), n=question note (EN,AR))
from ans_core import a

a(1, "C", "M", "50", "one of the commonest causes",
  ("Peptic ulcer disease (NSAID/aspirin and H. pylori related) is the leading cause of serious upper GI bleeding.",
   "القرحة الهضمية (بسبب NSAIDs أو H. pylori) هي أشهر سبب لنزيف الجهاز الهضمي العلوي الخطير."),
  {"A": ("Second to PUD overall; it dominates only in cirrhosis.", "أقل شيوعاً عموماً، تسود فقط في تليف الكبد."),
   "B": ("Causes bleeding but less often than ulcers.", "تسبب نزيفاً لكن أقل من القرحة."),
   "D": ("A minority of cases, after forceful retching.", "نسبة قليلة، بعد قيء شديد.")},
  ("In cirrhotics (and in Egypt) varices are the commonest cause of MASSIVE hematemesis.",
     "في مرضى التليف (ومصر) الدوالي هي أشهر سبب للقيء الدموي الغزير."))

a(2, "D", "S", "68", "Gastric Perforation (Ischemic Necrosis)",
  ("The stomach distends, wall perfusion falls, then ischemic necrosis and perforation cause collapse and death.",
   "المعدة تتمدد فيقل تروية الجدار ثم يحدث نخر إقفاري وانثقاب وانهيار دوراني فالوفاة."),
  {"A": ("Not the mechanism of AGD death.", "ليست آلية الوفاة في AGD."),
   "B": ("Aspiration can occur but is not the described mechanism.", "قد تحدث لكنها ليست الآلية الأساسية."),
   "C": ("Renal failure is a late result of shock.", "الفشل الكلوي نتيجة متأخرة للصدمة.")},
  ("Mortality is 80-100% once ischemia or perforation develops, so decompress early.",
   "الوفيات 80-100% بعد الإقفار أو الانثقاب، لذا يجب تفريغ المعدة مبكراً."))

a(3, "A", "M", "62", "Any cause of chronic gastritis",
  ("Atrophic (chronic) gastritis with intestinal metaplasia is the soil for gastric adenocarcinoma.",
   "التهاب المعدة الضموري مع الحؤول المعوي هو الأرضية المؤدية لسرطان المعدة."),
  {"B": ("Duodenal ulcers are almost never malignant.", "قرحة الاثني عشر نادراً ما تتسرطن."),
   "C": ("Acute stress ulcers are not premalignant.", "قرح الإجهاد الحادة ليست سابقة للسرطان."),
   "D": ("Without a mucosal field change the risk is lower.", "بدون تغيّر مخاطي حولها يقل الخطر.")},
  ("Every gastric ulcer must be biopsied and followed until healed to exclude cancer.",
   "كل قرحة معدة تؤخذ منها عينة وتتابع حتى الشفاء لاستبعاد السرطان."))

a(4, "B", "S", None, None,
  ("Richter's hernia traps only the ANTI-mesenteric border of the bowel wall, so the lumen stays open.",
   "فتق ريختر يحبس فقط الحافة المقابلة للمساريق من جدار الأمعاء فتبقى التجويف مفتوحاً."),
  {"A": ("Whole circumference is a complete (ordinary) hernia.", "كامل محيط الأمعاء = فتق عادي."),
   "C": ("Not the mesenteric side.", "ليس جهة المساريق."),
   "D": ("That is a hiatus hernia.", "هذا فتق حجابي.")},
  ("It can strangulate and perforate WITHOUT obstruction, so a normal bowel pattern does not exclude it. "
   "Also: Littre = Meckel's, Amyand = appendix, Maydl = W-loop.",
   "قد يختنق وينثقب بدون انسداد، فلا تطمئن لانتظام الإخراج. أيضاً: Littre ميكل، Amyand الزائدة، Maydl حلقتان في الكيس."))

a(5, "A", "M", "91", "tTG-IgA is the single preferred test",
  ("tTG-IgA, with total IgA, is the single preferred first test in adults who are still eating gluten.",
   "tTG-IgA مع قياس IgA الكلي هو الاختبار الأول المفضل لدى البالغين الذين ما زالوا يأكلون الجلوتين."),
  {"B": ("Scleroderma (CREST).", "مرتبط بالسكليرودرما."),
   "C": ("AMA = primary biliary cholangitis.", "AMA = التهاب الصفراوية الأولي."),
   "D": ("RF = rheumatoid arthritis.", "RF = الروماتويد.")},
  ("If IgA-deficient use IgG-based tests (tTG-IgG or DGP-IgG). The test is valid only on a gluten diet.",
   "لو نقص IgA نستخدم اختبارات IgG. والاختبار صالح فقط أثناء تناول الجلوتين."))

a(6, "B", "S", "~53", "Perforated peptic ulcer",
  ("Perforation is the commonest indication for emergency ulcer surgery.",
   "الانثقاب هو أشهر سبب للجراحة الطارئة في القرحة."),
  {"A": ("Heartburn without complications is treated medically.", "الحرقان غير المصحوب بمضاعفات علاجه دوائي."),
   "C": ("Asymptomatic H. pylori needs eradication, not surgery.", "H. pylori بدون أعراض يُعالج بالاستئصال لا بالجراحة."),
   "D": ("A relative indication, only after failed endoscopic control.", "استطباب نسبي بعد فشل التحكم المنظاري.")},
  ("Anterior duodenal ulcers perforate; posterior ones bleed (gastroduodenal artery).",
   "قرحة الجدار الأمامي تنثقب، والخلفية تنزف (الشريان المعدي الاثني عشري)."))

a(7, "B", "M", "71", "Occurs on top of Barrett",
  ("Barrett's (columnar metaplasia) predisposes to adenocarcinoma, especially in the lower third.",
   "مريء باريت (تحوّل عمودي) يهيّئ للسرطان الغدي خاصة في الثلث السفلي."),
  {"A": ("GIST arises from cells of Cajal.", "GIST ينشأ من خلايا كاجال."),
   "C": ("Small-cell carcinoma is not linked to Barrett's.", "الخلايا الصغيرة غير مرتبط بباريت."),
   "D": ("SCC links to smoking, alcohol and achalasia.", "الحرشفي يرتبط بالتدخين والكحول والأكالازيا.")},
  ("Adenocarcinoma = lower third/GEJ (West); SCC = middle third (worldwide).",
   "الغدي = الثلث السفلي/GEJ، والحرشفي = الثلث الأوسط."))

a(8, "A", "S", "146", "Low-fiber diet and high carbohydrates",
  ("A low-residue (low-fibre) diet raises colonic intraluminal pressure and favors diverticula.",
   "الغذاء قليل الألياف يرفع ضغط القولون الداخلي ويساعد على تكوّن الرتوج."),
  {"B": ("Protein is not the factor; fibre is.", "البروتين ليس العامل، بل قلة الألياف."),
   "C": ("Fat is more linked to colon cancer.", "الدهون ترتبط أكثر بسرطان القولون."),
   "D": ("High residue protects.", "الغذاء كثير الألياف وقائي.")},
  ("Diverticulosis is usually asymptomatic, mostly sigmoid, and the rectum never has it.",
   "الرتوج غالباً بلا أعراض وأغلبها في السيني، والمستقيم لا يصاب أبداً."))

a(9, "C", "M", "46", "Competitive reversible PP inhibition",
  ("Vonoprazan is a P-CAB: it reversibly blocks the K+ site of the proton pump (active and resting pumps).",
   "Vonoprazan من فئة P-CAB: يحجب بشكل عكوس موقع البوتاسيوم في مضخة البروتون (النشطة والخاملة)."),
  {"A": ("Irreversible = PPIs.", "غير عكوس = PPIs."),
   "B": ("Prostaglandin inhibition = NSAIDs.", "تثبيط البروستاجلاندين = NSAIDs."),
   "D": ("H2 blockade = famotidine.", "حجب H2 = famotidine.")},
  ("P-CAB: not a prodrug, acid-stable, no acid activation needed, works before or after meals, T1/2 6-9 h, max effect in 1 day.",
   "P-CAB ليس دواءً سالفاً، ثابت في الحمض، لا يحتاج تنشيطاً، يؤخذ قبل/بعد الأكل، نصف عمره 6-9 ساعات، أقصى تأثير في يوم."))

a(10, "B", "M", "48", "Triple therapy: 10-14 days",
  ("A PPI plus two or more antibiotics eradicates H. pylori, which removes the cause and cuts recurrence.",
   "PPI مع مضادين حيويين أو أكثر يقضي على H. pylori فيزيل السبب ويقلل النكس."),
  {"A": ("Nonsense combination.", "تركيبة غير منطقية."),
   "C": ("Heals the ulcer but it relapses.", "يشفي القرحة لكنها تعود."),
   "D": ("Symptomatic relief only.", "تخفيف أعراض فقط.")},
  ("Test of cure: urea breath test after 4 weeks off antibiotics and 2 weeks off PPI.",
   "اختبار الشفاء: Urea breath test بعد 4 أسابيع من المضادات و2 أسبوع من الـPPI."))

a(11, "C", "M", "50", "assume hypovolaemia until proven otherwise",
  ("Hypotension (90/60) with tachycardia (110) means hypovolemic shock.",
   "هبوط الضغط (90/60) مع سرعة النبض (110) يدل على صدمة نقص حجم."),
  {"A": ("Normal vitals.", "علامات حيوية طبيعية."),
   "B": ("Hypertension with bradycardia is not shock.", "ارتفاع ضغط مع بطء نبض ليس صدمة."),
   "D": ("Normal vitals.", "علامات حيوية طبيعية.")},
  ("Shock index (pulse/systolic BP) above 1 = significant bleed; beta-blockers can mask tachycardia.",
   "مؤشر الصدمة (النبض ÷ الانقباضي) فوق 1 = نزف كبير؛ حاصرات بيتا تخفي تسرع القلب."))

a(12, "C", "S", "65", "Abdominal ultrasound",
  ("Abdominal ultrasound is a basic staging tool (liver metastases, ascites); endoscopy gives the diagnosis.",
   "الموجات فوق الصوتية أداة أساسية في التقسيم (نقائل الكبد والاستسقاء)؛ والمنظار يعطي التشخيص."),
  {"A": ("Barium shows a defect; biopsy by endoscopy is definitive.", "الباريوم يظهر عيباً فقط، والتشخيص بالمنظار والخزعة."),
   "B": ("CEA/CA 72-4 are for follow-up, not diagnosis.", "الواسمات للمتابعة لا للتشخيص."),
   "D": ("CT does detect liver, lung and nodal metastases.", "الأشعة المقطعية تكشف نقائل الكبد والرئة والعقد.")},
  ("Staging = CT chest/abdomen +/- EUS +/- staging laparoscopy. CA 72-4 is the key marker for recurrence.",
   "التقسيم = CT صدر وبطن ± EUS ± منظار بطن. و CA 72-4 أهم واسم للنكس."))

a(13, "C", "S", "29", "Palliative treatments",
  ("Liver metastasis means incurable disease, so palliation (stent, supportive care, RT/chemo) is the plan.",
   "نقائل الكبد تعني مرضاً غير قابل للشفاء، فالعلاج تلطيفي (دعامة ودعم)."),
  {"A": ("Curative resection is not for M1 disease.", "الاستئصال الشافي لا يناسب النقائل."),
   "B": ("Curative-intent chemoradiation is for locoregional disease.", "العلاج الشافي للمرض الموضعي فقط."),
   "D": ("EMR is only for early mucosal (T1) cancer.", "EMR فقط للسرطان المبكر المخاطي.")},
  ("Stents for dysphagia: Celestin and Souttar tubes, or self-expanding metal stents.",
   "دعامات البلع: أنابيب Celestin وSouttar أو الدعامات المعدنية المتمددة."))

a(14, "D", "M", "80", "Causes of exudative diarrhea",
  ("Exudative diarrhea comes from an inflamed, ulcerated mucosa leaking mucus, blood and pus.",
   "الإسهال الإفرازي الالتهابي ينتج عن مخاطية ملتهبة متقرحة تسرّب مخاطاً ودماً وصديداً."),
  {"A": ("Rapid transit = motility diarrhea.", "السرعة = إسهال حركي."),
   "B": ("Unabsorbed lactose = osmotic.", "اللاكتوز غير الممتص = أسموزي."),
   "C": ("Not a pathological mechanism.", "ليس آلية مرضية.")},
  ("Examples: UC, Crohn's, Salmonella, Shigella, C. difficile. Stool has WBCs/blood.",
   "أمثلة: UC وكرون والسالمونيلا والشيجيلا. البراز فيه كرات بيضاء ودم."))

a(15, "B", "M", "40", "Urea breath test",
  ("The 13C-urea breath test detects bacterial urease: labeled urea becomes labeled CO2 in the breath.",
   "اختبار التنفس باليوريا: بكتيريا H. pylori تحوّل اليوريا الموسومة إلى CO2 موسوم."),
  {"A": ("Fecal elastase tests the pancreas.", "فحص البنكرياس."),
   "C": ("Lactase deficiency test.", "اختبار نقص اللاكتيز."),
   "D": ("Irrelevant.", "غير مرتبط.")},
  ("Sensitivity 90%, specificity 96%. Stop PPIs 2 weeks and antibiotics 4 weeks before.",
   "الحساسية 90% والنوعية 96%. أوقف الـPPI أسبوعين والمضادات 4 أسابيع قبله."))

a(16, "D", "M", "71", "smoking, alcohol, diet",
  ("Alcohol and smoking are the main risk factors for esophageal squamous cell carcinoma.",
   "الكحول والتدخين أهم عوامل خطر السرطان الحرشفي للمريء."),
  {"A": ("Not linked to the esophagus.", "لا علاقة بالمريء."),
   "B": ("Obesity and Barrett's lead to adenocarcinoma.", "السمنة وباريت للغدي."),
   "C": ("Lactose intolerance is unrelated.", "عدم تحمل اللاكتوز غير مرتبط.")},
  ("Other SCC risks: achalasia, caustic stricture, hot drinks, low vitamins/zinc.",
   "عوامل أخرى: الأكالازيا والتضيق الكاوي والمشروبات الساخنة ونقص الفيتامينات."))

a(17, "D", "M", "50", "NSAIDs/aspirin",
  ("Aspirin and NSAIDs are the commonest drugs causing ulcers and upper GI bleeding.",
   "الأسبرين والـNSAIDs أشهر أدوية تسبب القرح ونزف الجهاز الهضمي العلوي."),
  {"A": ("Antacid.", "مضاد حموضة."),
   "B": ("Paracetamol harms the liver, not the stomach.", "الباراسيتامول يضر الكبد لا المعدة."),
   "C": ("Famotidine treats ulcers.", "Famotidine يعالج القرح.")},
  ("Anticoagulants worsen bleeding from another lesion; they do not usually cause it themselves.",
   "مضادات التجلط تزيد النزف من آفة أخرى ولا تسببه عادة بنفسها."))

a(18, "B", "M", "96", "infrequent bowel movements",
  ("Constipation = infrequent stools with difficult passage, straining or hard stools.",
   "الإمساك = إخراج متباعد مع صعوبة أو إجهاد أو براز صلب."),
  {"A": ("Fecal incontinence.", "سلس برازي."),
   "C": ("Normal bowel habit.", "إخراج طبيعي."),
   "D": ("Diarrhea.", "إسهال.")},
  ("Rome: at least 2 of: fewer than 3 stools/week, straining, hard stool, incomplete evacuation.",
   "معايير روما: اثنان على الأقل: أقل من 3 مرات/أسبوع، إجهاد، براز صلب، شعور بعدم الإفراغ."))

a(19, "A", "S", None, None,
  ("Defect size is the strongest anatomical determinant of recurrence among the options.",
   "حجم الفتحة هو أقوى عامل تشريحي للنكس بين الاختيارات."),
  {"B": ("Fasting time is irrelevant.", "مدة الصيام غير مؤثرة."),
   "C": ("Blood group is irrelevant.", "فصيلة الدم غير مؤثرة."),
   "D": ("Time of surgery is irrelevant.", "وقت العملية غير مؤثر.")},
  ("Other risks: wound infection, obesity, smoking, tension, no mesh. Sublay mesh lowers recurrence.",
   "عوامل أخرى: عدوى الجرح والسمنة والتدخين والشد وعدم استخدام الشبكة."))

a(20, "B", "M", "15", "Peptic stricture",
  ("Chronic acid reflux causes fibrosis and an esophageal (peptic) stricture.",
   "الارتجاع المزمن يسبب تليفاً وتضيقاً بالمريء."),
  {"A": ("Unrelated to reflux.", "غير مرتبط."),
   "C": ("Congenital.", "خلقي."),
   "D": ("A different hernia type.", "نوع آخر من الفتق.")},
  ("GERD complications: stricture, Barrett's, bleeding/ulcer, adenocarcinoma (not SCC).",
   "مضاعفات GERD: تضيق، باريت، نزف/قرحة، سرطان غدي (وليس الحرشفي)."))

a(21, "B", "S", "17", "Sliding hiatus hernia (85 %)",
  ("Sliding hiatus hernia (type I) accounts for about 85% of hiatus hernias.",
   "الفتق الحجابي الانزلاقي (النوع I) يمثل نحو 85% من الفتوق الحجابية."),
  {"A": ("Mixed type is rarer.", "المختلط أقل شيوعاً."),
   "C": ("Type IV has other organs too, and is rare.", "النوع IV نادر ويحوي أعضاء أخرى."),
   "D": ("Rolling type is about 10%.", "نحو 10% فقط.")},
  ("Sliding = reflux. Rolling (paraesophageal) = obstruction/strangulation, so repair even if silent.",
   "الانزلاقي = ارتجاع. الدحرجي = انسداد/اختناق لذا يُصلح حتى لو صامت."))

a(22, "B", "M", "4", "Melena: black, tarry stool",
  ("Melena is black tarry stool from altered blood, usually bleeding proximal to the right colon.",
   "Melena براز أسود قطراني بسبب دم متحول، عادة من نزف أعلى القولون الأيمن."),
  {"A": ("Pale stools = obstructive jaundice.", "براز شاحب = انسداد صفراوي."),
   "C": ("Fresh rectal blood = hematochezia.", "دم أحمر طازج = hematochezia."),
   "D": ("Fatty stools = steatorrhea.", "براز دهني = steatorrhea.")},
  ("It needs more than 50 mL of blood. Massive upper bleeding can even give fresh blood per rectum with shock.",
   "يحتاج أكثر من 50 مل دم. النزف العلوي الغزير قد يعطي دماً أحمر مع صدمة."))

a(23, "D", "M", "45", "Should be taken 30",
  ("PPIs only block ACTIVE pumps, so give them 30-60 min before the first meal.",
   "الـPPI يثبط المضخات النشطة فقط، فيؤخذ قبل أول وجبة بـ30-60 دقيقة."),
  {"A": ("Food lowers bioavailability by about 50%.", "الأكل يقلل الامتصاص نحو 50%."),
   "B": ("Pumps are quiet while fasting overnight.", "المضخات خاملة أثناء الصيام الليلي."),
   "C": ("Needs repeated dosing; PRN is ineffective.", "يحتاج جرعات متكررة وليس عند اللزوم.")},
  ("Maximal effect after 3-5 days; vonoprazan (P-CAB) does not need this timing.",
   "أقصى تأثير بعد 3-5 أيام؛ وvonoprazan لا يحتاج هذا التوقيت."))

a(24, "B", "M", "77", "Diarrhea lasting >4 weeks",
  ("Diarrhea lasting more than 4 weeks (about 30 days) is chronic.",
   "الإسهال لأكثر من 4 أسابيع (نحو 30 يوماً) يعتبر مزمناً."),
  {"A": ("7 days is acute.", "7 أيام = حاد."),
   "C": ("14 days is acute/persistent.", "14 يوماً = حاد/مستمر."),
   "D": ("Far longer than required.", "أطول بكثير من المطلوب.")},
  ("Most chronic diarrhea is NON-infectious; about 80% of acute diarrhea is infectious.",
   "معظم الإسهال المزمن غير معدٍ؛ ونحو 80% من الحاد معدٍ."))

a(25, "B", "M", "71", "Occurs on top of Barrett",
  ("Esophageal adenocarcinoma is the cancer that arises from Barrett's metaplasia.",
   "السرطان الغدي للمريء هو الذي ينشأ من تحوّل باريت."),
  {"A": ("Not related.", "غير مرتبط."), "C": ("Not related.", "غير مرتبط."), "D": ("Not related.", "غير مرتبط.")},
  ("Only a small proportion of Barrett's progresses, hence surveillance endoscopy.",
   "نسبة قليلة فقط تتحول، لذلك يلزم منظار متابعة."))

a(26, "B", "S", "29", "infiltration of surrounding structures",
  ("Invasion of the trachea/bronchus (T4) makes the tumor unresectable.",
   "غزو القصبة الهوائية/الشعب (T4) يجعل الورم غير قابل للاستئصال."),
  {"A": ("Minor finding.", "علامة بسيطة."),
   "C": ("Early mucosal disease is resectable/endoscopic.", "المرض المخاطي المبكر قابل للاستئصال."),
   "D": ("Small superficial lesions are resectable.", "الآفة الصغيرة السطحية قابلة للاستئصال.")},
  ("Unresectable also: aorta invasion, distant metastasis, celiac or distant nodes.",
   "غير قابل أيضاً: غزو الأبهر ونقائل بعيدة وعقد بعيدة."))

a(27, "A", "M", "116", "disease in the ileum and cecum",
  ("The commonest Crohn's pattern is ileocecal disease (about 40%).",
   "أشهر نمط لكرون هو اللفائفي-الأعوري (نحو 40%)."),
  {"B": ("Rectal-only is typical of UC proctitis.", "المستقيم فقط يميز UC."),
   "C": ("Rare.", "نادر."), "D": ("Rare.", "نادر.")},
  ("Three patterns: ileocecal (40%), small bowel only, colon only (25%).",
   "ثلاثة أنماط: لفائفي-أعوري (40%)، أمعاء دقيقة فقط، قولون فقط (25%)."))

a(28, "B", "S", "143", "the source of bleed is often",
  ("Meckel's bleeding comes from ulceration of the adjacent ileum, due to acid from ectopic gastric mucosa.",
   "نزف ميكل ينتج عن تقرح اللفائفي المجاور بسبب حمض الغشاء المعدي الهاجر."),
  {"A": ("Variceal bleeding is portal hypertension.", "نزف الدوالي = ارتفاع الضغط البابي."),
   "C": ("Not a gastric polyp.", "ليس من سليلة معدية."),
   "D": ("Appendicitis does not bleed.", "التهاب الزائدة لا ينزف.")},
  ("Rule of 2s; painless bleeding in a child under 5; Tc-99m pertechnetate scan is most accurate.",
   "قاعدة الـ2؛ نزف بلا ألم عند طفل أقل من 5؛ أدق فحص Tc-99m."))

a(29, "B", "M", "88", "low serum vitamin B12 levels but normal or high folate",
  ("In bacterial overgrowth B12 is LOW but folate is normal/high; in tropical sprue both are low.",
   "في فرط النمو البكتيري B12 منخفض والفولات طبيعي/مرتفع؛ وفي Tropical sprue كلاهما منخفض."),
  {"A": ("Reversed pattern.", "عكس الصحيح."),
   "C": ("Not seen.", "لا يحدث."),
   "D": ("Low both = tropical sprue.", "كلاهما منخفض = tropical sprue.")},
  ("Bacteria consume B12 and make folate.",
   "البكتيريا تستهلك B12 وتصنع الفولات."))

a(30, "D", "M", "116", "dominant symptom in ulcerative colitis",
  ("UC is limited to the colon and is mucosal (continuous from the rectum).",
   "UC يقتصر على القولون ويصيب الغشاء المخاطي (متصل من المستقيم)."),
  {"A": ("Esophageal motility disorder.", "اضطراب حركة المريء."),
   "B": ("An enzyme deficiency.", "نقص إنزيم."),
   "C": ("Crohn's is transmural and can hit any site.", "كرون يصيب كل الطبقات وأي موضع.")},
  ("UC = mucosal + continuous + rectum first; Crohn's = transmural + skip lesions.",
   "UC مخاطي ومتصل ويبدأ بالمستقيم؛ كرون كل الطبقات وبقع متفرقة."))

a(31, "B", "M", "38", "Antral gastritis is the usual effect of H. pylori",
  ("Antral-predominant chronic gastritis with epigastric pain is the classic picture of H. pylori.",
   "التهاب معدة مزمن يغلب على الغار مع ألم شرسوفي هو الصورة الكلاسيكية لـ H. pylori."),
  {"A": ("CMV is seen in immunocompromised patients.", "CMV لدى المناعة المنخفضة."),
   "C": ("Autoimmune gastritis affects body/fundus.", "المناعي يصيب الجسم/القاع."),
   "D": ("Pancreatitis does not cause antral erythema.", "التهاب البنكرياس لا يسبب احمرار الغار.")},
  ("H. pylori = antrum (duodenal ulcer); autoimmune = body/fundus (pernicious anemia).",
   "H. pylori = الغار؛ المناعي = الجسم والقاع (أنيميا خبيثة)."))

a(32, "A", "M", "87", "Unabsorbed lactose is osmotically active",
  ("Unabsorbed lactose is osmotically active and pulls water into the lumen (osmotic diarrhea).",
   "اللاكتوز غير الممتص يسحب الماء إلى التجويف (إسهال أسموزي)."),
  {"B": ("Secretory mechanism.", "آلية إفرازية."),
   "C": ("Steatorrhea mechanism.", "آلية الإسهال الدهني."),
   "D": ("Exudative mechanism.", "آلية التهابية.")},
  ("Osmotic diarrhea stops on fasting and responds to a lactose-free diet.",
   "الإسهال الأسموزي يتوقف بالصيام ويتحسن بنظام خالٍ من اللاكتوز."))

a(33, "A", "M", "97", "red flag features",
  ("Anemia (iron deficiency) is a red flag that mandates colorectal cancer work-up.",
   "الأنيميا (نقص حديد) علامة إنذار تستوجب البحث عن سرطان القولون."),
  {"B": ("Common, benign.", "شائع وحميد."),
   "C": ("Part of constipation itself.", "جزء من الإمساك نفسه."),
   "D": ("Part of constipation itself.", "جزء من الإمساك نفسه.")},
  ("Red flags: bleeding, weight loss, anemia, change in stool caliber, rectal mass, age over 50.",
   "علامات الإنذار: نزف، فقدان وزن، أنيميا، تغير قطر البراز، كتلة مستقيم، عمر فوق 50."))

a(34, "C", "S", "57", "exploration of the bleeding duodenal ulcer",
  ("Open the duodenum and under-run (over-sew) the ulcer base to control the vessel.",
   "فتح الاثني عشر وخياطة قاع القرحة للسيطرة على الوعاء النازف."),
  {"A": ("Nissen is for reflux.", "Nissen لعلاج الارتجاع."),
   "B": ("Fundal wedge is for other lesions.", "لآفات أخرى."),
   "D": ("Vagotomy alone does not stop a bleeding vessel.", "قطع المبهم وحده لا يوقف النزف.")},
  ("Bleeding suspicious gastric ulcer: partial gastrectomy.",
   "قرحة معدة مشتبه بها: استئصال جزئي للمعدة."))

a(35, "D", "M", "116", "is marked by one of three major patterns",
  ("Skip areas of inflammation with normal mucosa in between are typical of Crohn's.",
   "مناطق التهاب متفرقة بينها مخاطية طبيعية (skip lesions) مميزة لكرون."),
  {"A": ("UC is continuous.", "UC متصل."),
   "B": ("Reflux is esophageal.", "الارتجاع مريئي."),
   "C": ("Lactose malabsorption has a normal mucosa.", "سوء امتصاص اللاكتوز مخاطية طبيعية.")},
  ("Crohn's: skip lesions, cobblestone, transmural, granulomas, perianal disease.",
   "كرون: skip lesions، cobblestone، كل الطبقات، حبيبومات، آفات حول الشرج."))

a(36, "C", "M", "116", "dominant symptom in ulcerative colitis",
  ("Bloody diarrhea with continuous rectal inflammation in a young adult is ulcerative colitis.",
   "إسهال دموي مع التهاب مستقيمي متصل لدى شاب = التهاب القولون التقرحي."),
  {"A": ("Crohn's is patchy with perianal disease.", "كرون متقطع مع آفات شرجية."),
   "B": ("Ischemic colitis affects older patients.", "الإقفاري لكبار السن."),
   "D": ("Infectious colitis is short and acute.", "المعدي حاد وقصير.")},
  ("UC peaks at 15-25 and again at 55-65 years.",
   "UC له ذروتان: 15-25 سنة و55-65 سنة."))

a(37, "C", "S", "59", "Truncal vagotomy and gastro-jejunostomy",
  ("A fibrotic pyloric obstruction that fails dilation needs surgical drainage (vagotomy + gastrojejunostomy).",
   "انسداد البواب التليفي الذي فشل معه التوسيع يحتاج تصريفاً جراحياً (قطع مبهم + مفاغرة معدية صائمية)."),
  {"A": ("Colectomy is unrelated.", "غير مرتبط."),
   "B": ("Repeating dilation without reassessment is wrong.", "تكرار التوسيع بلا إعادة تقييم خطأ."),
   "D": ("Fundoplication treats reflux.", "لعلاج الارتجاع.")},
  ("Add post-operative PPI; partial gastrectomy if the stomach is hugely dilated.",
   "يضاف PPI بعد العملية؛ واستئصال جزئي لو المعدة متمددة جداً."))

a(38, "B", "M", "36", "blocking the synthesis of prostaglandin E2",
  ("NSAIDs inhibit COX-1, so PGE2 falls, mucus/bicarbonate drop and acid output rises.",
   "الـNSAIDs تثبط COX-1 فينقص PGE2 والمخاط والبيكربونات ويزداد الحمض."),
  {"A": ("H2 blockers are treatment, not a cause.", "حاصرات H2 علاج لا سبب."),
   "C": ("NSAIDs reduce mucus.", "ينقصون المخاط."),
   "D": ("They decrease PG synthesis.", "ينقصون تصنيع PG.")},
  ("Misoprostol (PGE1 analogue) or a PPI protects high-risk NSAID users.",
   "Misoprostol (نظير PGE1) أو PPI يحمي المرضى عاليي الخطورة."))

a(39, "C", "M", "5", "Investigation of choice for most upper GI disorders",
  ("Upper endoscopy (EGD) both diagnoses (biopsy) and treats (hemostasis, dilation) upper GI disorders.",
   "المنظار العلوي يشخص (خزعة) ويعالج (إيقاف نزف وتوسيع) أمراض الجهاز الهضمي العلوي."),
  {"A": ("CT cannot treat.", "CT لا يعالج."),
   "B": ("Barium only images.", "الباريوم تصوير فقط."),
   "D": ("Manometry is diagnostic only.", "للتشخيص فقط.")},
  ("Gastroscopy is more sensitive than barium meal and allows biopsy.",
   "المنظار أدق من الباريوم ويسمح بالخزعة."))

a(40, "C", "M", "101", "Disorders of Gut",
  ("IBS is a disorder of gut-brain interaction: symptoms without structural damage.",
   "IBS اضطراب في التفاعل الدماغي المعوي: أعراض بدون تلف بنيوي."),
  {"A": ("It is benign.", "حميد."),
   "B": ("No mechanical obstruction.", "لا انسداد ميكانيكي."),
   "D": ("Not renal.", "ليس كلوياً.")},
  ("Diagnosis is clinical (Rome criteria); routine tests are normal.",
   "التشخيص إكلينيكي (معايير روما) والتحاليل الروتينية طبيعية."))

a(41, "B", "M", "190", "Adenomatous polyp",
  ("Adenomatous polyps (tubular, villous) are neoplastic and can become malignant.",
   "الأورام الغدية (أنبوبية، زغابية) نيوبلازمية وقد تتسرطن."),
  {"A": ("Hyperplastic: little or no risk.", "فرط التنسج: خطر ضئيل."),
   "C": ("Hamartoma: low risk.", "هامارتوم: خطر منخفض."),
   "D": ("Inflammatory polyps are not neoplastic.", "ليست نيوبلازمية.")},
  ("Villous > tubular in malignant potential; polyp size above 2 cm is high risk.",
   "الزغابي أخطر من الأنبوبي؛ الحجم فوق 2 سم عالي الخطورة."))

a(42, "A", "S", "68", "Eating Disorders: Anorexia nervosa, bulimia nervosa",
  ("Among the options, SMA syndrome is the one linked to eating disorders (weight loss) and gives epigastric distension and vomiting.",
   "بين الاختيارات، متلازمة SMA هي المرتبطة باضطرابات الأكل (فقدان وزن) وتعطي انتفاخاً وقيئاً."),
  {"B": ("Needs an ulcer history.", "تحتاج تاريخ قرحة."),
   "C": ("Volvulus is acute, with pain and failed NG passage.", "الانفتال حاد وألم وصعوبة تمرير الأنبوب."),
   "D": ("Pancreatitis presents with back pain and high amylase.", "التهاب البنكرياس بألم ظهر وأميليز مرتفع.")},
  ("Wording issue: the book lists bulimia as a functional cause of ACUTE GASTRIC DILATATION, which is not offered here.",
   "ملاحظة: الكتاب يذكر الـbulimia كسبب وظيفي لـAcute Gastric Dilatation وهو غير موجود بالاختيارات."),
  ("Question flaw: expected answer is acute gastric dilatation (not listed).",
   "السؤال به عيب: الإجابة المتوقعة acute gastric dilatation وهي غير مذكورة."))

a(43, "B", "M", "45", "converted by acid into active form",
  ("Omeprazole is a prodrug converted in acid to an agent that irreversibly inhibits H+/K+ ATPase.",
   "Omeprazole دواء سالف يتحول بالحمض ويثبط H+/K+ ATPase بشكل غير عكوس."),
  {"A": ("That is vonoprazan (P-CAB).", "هذا vonoprazan."),
   "C": ("Muscarinic block is anticholinergic action.", "حجب المسكارينيك دواء آخر."),
   "D": ("H2 blockade is famotidine.", "حجب H2 = famotidine.")},
  ("Long action (24 h) because new pumps take 24 h to be made, though T1/2 is only 1-2 h.",
   "تأثيره 24 ساعة لأن بناء مضخات جديدة يحتاج 24 ساعة رغم أن نصف عمره 1-2 ساعة."))

a(44, "B", "M", "~89", "Celiac disease",
  ("Celiac biopsy shows villous atrophy with crypt hyperplasia and intraepithelial lymphocytes.",
   "خزعة السيلياك: ضمور الزغابات مع فرط تنسج الخبايا وزيادة اللمفاويات."),
  {"A": ("Reversed.", "عكسه."),
   "C": ("Not celiac.", "غير صحيح."),
   "D": ("Granulomas suggest Crohn's.", "الحبيبومات تدل على كرون.")},
  ("Biopsy is done on a gluten diet; the target is the duodenum (Marsh classification).",
   "الخزعة تؤخذ والمريض على الجلوتين من الاثني عشر (Marsh)."))

a(45, "D", "M", "7", "Capsule endoscopy",
  ("A swallowed capsule endoscope images the whole small bowel as it passes.",
   "كبسولة المنظار تُبتلع وتصور الأمعاء الدقيقة بالكامل أثناء مرورها."),
  {"A": ("NG tube suctions only.", "للشفط فقط."),
   "B": ("ECG leads record the heart.", "تسجل القلب."),
   "C": ("Not an imaging device.", "ليس جهاز تصوير.")},
  ("Used for obscure GI bleeding after negative gastroscopy and colonoscopy.",
   "يستخدم للنزف الغامض بعد منظار علوي وسفلي سلبيين."))
