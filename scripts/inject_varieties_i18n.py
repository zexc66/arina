import json

with open('website.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace playVideo with new variety helper functions if not already replaced
old_play_video = """    // -------------------------------------------------------------------------
    // 8. COMMERCIAL VIDEO CINEMA THEATER
    // -------------------------------------------------------------------------
    function playVideo(videoSrc, title) {
      const player = document.getElementById('main-video-player');
      if (player) {
        player.src = videoSrc;
        player.play().catch(e => console.log('Autoplay prevented by browser:', e));
      }

      document.querySelectorAll('.vid-btn').forEach(btn => {
        const onClickAttr = btn.getAttribute('onclick') || '';
        if (onClickAttr.includes(videoSrc)) {
          btn.className = 'vid-btn active-vid w-full p-3.5 rounded-xl border border-brand-gold bg-brand-forest/60 text-left rtl:text-right transition-all hover:bg-brand-forest flex items-start space-x-3 rtl:space-x-reverse group shadow-md';
        } else {
          btn.className = 'vid-btn w-full p-3.5 rounded-xl border border-brand-gold/30 bg-brand-forest/30 text-left rtl:text-right transition-all hover:bg-brand-forest flex items-start space-x-3 rtl:space-x-reverse group';
        }
      });
    }"""

new_helpers = """    // -------------------------------------------------------------------------
    // 8. LUXURY VARIETIES GUIDE & COMPENDIUM
    // -------------------------------------------------------------------------
    function filterVarieties(category) {
      const cards = document.querySelectorAll('.variety-card');
      cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });

      document.querySelectorAll('.guide-filter-btn').forEach(btn => {
        btn.className = 'guide-filter-btn px-5 py-2.5 rounded-full text-xs font-bold transition-all border border-brand-gold/30 bg-brand-forest-dark/70 text-brand-ivory hover:border-brand-gold hover:text-brand-gold cursor-pointer';
      });
      const activeBtn = document.getElementById(`guide-tab-${category}`);
      if (activeBtn) {
        activeBtn.className = 'guide-filter-btn active-filter px-5 py-2.5 rounded-full text-xs font-bold transition-all border border-brand-gold bg-brand-gold text-brand-forest-obsidian shadow-md cursor-pointer';
      }
    }

    function searchVarieties(query) {
      const q = (query || '').toLowerCase().trim();
      const cards = document.querySelectorAll('.variety-card');
      cards.forEach(card => {
        const text = (card.getAttribute('data-search') || '').toLowerCase();
        if (!q || text.includes(q)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    function requestVarietyRFQ(varietyName) {
      const notesField = document.getElementById('rfq-notes');
      if (notesField) {
        const currentVal = notesField.value.trim();
        const addition = (currentLang === 'ar' ? 'طلب تسعير ومواصفات وتوافر كميات لصنف: ' : 'Inquiry for wholesale pricing & spec of: ') + varietyName;
        notesField.value = currentVal ? currentVal + '\\n• ' + addition : '• ' + addition;
      }
      showToast(currentLang === 'ar' ? `تمت إضافة (${varietyName}) إلى تفاصيل طلب التسعير!` : `Added (${varietyName}) to RFQ details!`);
      const rfqEl = document.getElementById('rfq');
      if (rfqEl) {
        rfqEl.scrollIntoView({ behavior: 'smooth' });
      }
    }"""

if old_play_video in html:
    html = html.replace(old_play_video, new_helpers)
    print("Replaced playVideo with Varieties Guide JS helpers!")
elif 'function filterVarieties(' in html:
    print("Varieties Guide JS helpers already present!")
else:
    import re
    html = re.sub(r'// -{5,}\s*// 8\. COMMERCIAL VIDEO CINEMA THEATER\s*// -{5,}\s*function playVideo\(.*?\n    \}', new_helpers, html, flags=re.DOTALL)
    print("Replaced playVideo with regex!")

varieties_data = [
    {
        "id": "kalamata",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "1. زيتون كالاماتا (Kalamata)",
        "name_en": "Royal Kalamata Olives",
        "desc_ar": "زيتون يوناني شهير ذو لون بنفسجي غامق ورائحة مميزة، يتميز بحبة كبيرة وشكل لوزي وقوام لحمي غني.",
        "desc_en": "Famous Greek olive variety with deep purple lustrous color, distinctive aroma, large almond silhouette, and luscious meaty texture.",
        "taste_ar": "غني، مالح، ويحتوي على نكهة فاكهية عميقة.",
        "taste_en": "Rich, balanced salinity, layered with profound fruity undertones.",
        "use_ar": "ممتاز كمقبلات مع الجبن، وفي السلطات اليونانية.",
        "use_en": "Superb table appetizer paired with artisanal cheeses and authentic Mediterranean salads."
    },
    {
        "id": "toffahi",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "2. زيتون تفاحي أخضر",
        "name_en": "Egyptian Green Toffahi Olives",
        "desc_ar": "زيتون مصري أصيل حباته مستديرة وكبيرة تشبه التفاح، ذو قشرة سميكة ولحم وفير.",
        "desc_en": "Authentic Egyptian heirloom olive with large round apple-like shape, thick crisp skin, and abundant succulent flesh.",
        "taste_ar": "مقرمش، قليل المرارة، ومثالي للتخليل السريع.",
        "taste_en": "Extra crunchy, mild delicate bitterness, ideal for express cure preservation.",
        "use_ar": "يُفضل حجماً ومذاقاً للتخليل المَحشي (بالجزر والفلفل).",
        "use_en": "Premium choice for hand-stuffed cured preparations (carrots, peppers & herbs)."
    },
    {
        "id": "azizi",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "3. زيتون العزيزي",
        "name_en": "Egyptian Azizi Estate Olives",
        "desc_ar": "من أجود أنواع الزيتون المصري، حباته بيضاوية الشكل ولونه يميل للأصفر الفاتح عند النضج.",
        "desc_en": "Finest heirloom Egyptian estate olive, featuring oval geometry and pale golden-green hues upon optimal maturity.",
        "taste_ar": "نسبة الزيت فيه عالية جداً، ومذاقه غني ودسم.",
        "taste_en": "Exceptionally high natural oil concentration with deep buttery, rich palate density.",
        "use_ar": "يُستخدم للكبس والتخليل وأيضاً لاستخراج أفضل زيت زيتون.",
        "use_en": "Exceptional for barrel curing, table pickling, and pressing into premier extra virgin olive oil."
    },
    {
        "id": "spanish_black",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "4. زيتون أسود إسباني (مخلوط/ناضج)",
        "name_en": "Spanish Ripe Black Olives",
        "desc_ar": "حبات متساوية الحجم، معالجة بطريقة خاصة لتفقد مرارتها تماماً وتصبح طرية.",
        "desc_en": "Uniformly calibrated ripe olives, specially cured to eliminate bitterness and yield a velvety tender bite.",
        "taste_ar": "ناعم، مالح بدرجة معتدلة، وغير لاذع.",
        "taste_en": "Velvety smooth, mild gentle salinity, and beautifully mellow non-astringent profile.",
        "use_ar": "مثالي لتزيين البيتزا، الساندويتشات، وسلطات المعكرونة.",
        "use_en": "Perfect garnish for artisan pizzas, deli sandwiches, and gourmet pasta salads."
    },
    {
        "id": "dolce",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "5. زيتون دولسي (المحلى / الأخضر المفرغ)",
        "name_en": "Dolce Sweet Pitted Green Olives",
        "desc_ar": "زيتون أخضر مفرغ النواة ومُعالج خصيصاً ليصبح حلو المذاق وخالياً تماماً من المرارة.",
        "desc_en": "Precision-pitted whole green olives, uniquely cured to achieve a delicate sweet profile zero bitterness.",
        "taste_ar": "طري، خفيف، ونظيف الطعم.",
        "taste_en": "Tender, light, crisp, and exceptionally clean gastronomic flavor.",
        "use_ar": "مثالي جداً للحشو السريع وإضافته للأطباق الإيطالية.",
        "use_en": "Ideal for rapid gourmet stuffing, antipasti platters, and authentic Italian pasta preparations."
    },
    {
        "id": "picual",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "name_ar": "6. زيتون بيكول (الرفيع المائل للطول)",
        "name_en": "Elongated Picual Olives",
        "desc_ar": "زيتون رفيع وطويل الشكل يتميز بكثافة اللحم بالنسبة للحجم وقوام صلب.",
        "desc_en": "Slender elongated olive variety boasting superior flesh-to-pit ratio and a remarkably firm, crisp bite.",
        "taste_ar": "حاد، غني، ونكهته تتركز بقوة.",
        "taste_en": "Piquant, robust, and intensely concentrated authentic olive terroir.",
        "use_ar": "رائع في أطباق البار ووجبات السناك الخفيفة.",
        "use_en": "Superb for luxury bar tapas, charcuterie boards, and gourmet finger snacks."
    },
    {
        "id": "lemon_asfar",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "1. مخلل الليمون المعصفر",
        "name_en": "Preserved Lemon with Safflower",
        "desc_ar": "ليمون بلدي كامل محشو بخليط من العصفر، حبة البركة، والملح الخشن.",
        "desc_en": "Whole authentic Egyptian baladi lemons hand-stuffed with aromatic saffron florets, nigella black seed, and coarse sea crystals.",
        "taste_ar": "حامض، غني بالنكهات الشرقية والزيوت العطرية لقشور الليمون.",
        "taste_en": "Tangy citrus zing infused with warm oriental aromatics and essential zest oils.",
        "use_ar": "مرافق أساسي للمشويات والأطباق الشعبية الدسمة.",
        "use_en": "Essential companion to charcoal-grilled meats, tagines, and traditional feast dishes."
    },
    {
        "id": "cucumber",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "2. مخلل الخيار المقرمش",
        "name_en": "Acoustic Crisp Baby Cucumbers",
        "desc_ar": "خيار رفيع وصغير الحجم، مخلل مع الثوم وأوراق النعناع أو الكرفس الطازجة.",
        "desc_en": "Slender petite greenhouse cucumbers cured with fresh crushed garlic cloves, garden mint leaves, and crisp celery stalks.",
        "taste_ar": "شديد القرمشة، منعش، وحامض بانتظام.",
        "taste_en": "Ultra-crunchy acoustic snap, lively freshness, and harmonious calibrated acidity.",
        "use_ar": "مثالي بجانب البرجر، الساندويتشات السريعة، والمقبلات الشامية.",
        "use_en": "Benchmark pairing for gourmet burgers, deli panini, and Levantine mezze spreads."
    },
    {
        "id": "turnip",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "3. مخلل اللفت الشتوي",
        "name_en": "Winter Wild Turnip in Ruby Beetroot",
        "desc_ar": "قطع لفت مقطعة على شكل أصابع أو مكعبات، مخللة مع قطع البنجر (الشمندر) التي تمنحه اللون الوردي الجذاب.",
        "desc_en": "Hand-batoned winter turnips cured naturally with fresh organic beetroot slices, imparting radiant ruby pigmentation.",
        "taste_ar": "طري، مقرمش، بنكهة ترابية خفيفة وحموضة متوازنة.",
        "taste_en": "Crisp tender bite, subtle earthy sweetness, and exquisitely balanced brine acidity.",
        "use_ar": "طبق جانبي لا غنى عنه مع الفول، الفلافل، والمشويات.",
        "use_en": "Indispensable classic side accompaniment for falafel, breakfast mezze, and rotisserie meats."
    },
    {
        "id": "carrot_chili",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "4. مخلل الجزر والفلفل الحار (مكس)",
        "name_en": "Royal Mixed Pickles (Carrot & Hot Chili)",
        "desc_ar": "شرائح جزر مقرمشة ممزوجة مع قرون الفلفل الأخضر أو الأحمر الحار والثوم.",
        "desc_en": "Crinkle-cut sweet carrots tossed with fiery whole red and green chilies, bay aromatics, and crushed garlic.",
        "taste_ar": "حار، لاذع، ومقرمش يفتح الشهية.",
        "taste_en": "Fiery, appetizingly piquant, and intensely crunchy palate stimulator.",
        "use_ar": "يضيف نكهة قوية ومميزة لأطباق الأرز والكبسة والأكلات الشعبية.",
        "use_en": "Adds vivid zest and crunch to spiced basmati rice, kabsa, and hearty sharing dishes."
    },
    {
        "id": "pearl_onion",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "5. مخلل البصل الصغير (البصل البلدي)",
        "name_en": "Hand-Peeled Baladi Pearl Onions",
        "desc_ar": "بصل صغير كامل ومقشر، مخلل بعناية ليحتفظ بقوامه الصلب دون أن يترهل.",
        "desc_en": "Petite whole hand-peeled baladi onions, cured with precision to preserve maximum cellular crunch without softening.",
        "taste_ar": "مقرمش، ذو حموضة ممتازة ونكهة بصلية محببة.",
        "taste_en": "Briskly crunchy, pristine vinegar bite, and delightful sweet allium undertone.",
        "use_ar": "ممتاز بجانب المشاوي والسندويتشات الشرقية.",
        "use_en": "Magnificent accompaniment to char-grilled kebabs, shawarma, and deli wraps."
    },
    {
        "id": "hot_pepper",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "6. مخلل الفلفل الحار الكامل",
        "name_en": "Whole Fiery Baladi Chili Peppers",
        "desc_ar": "قرون فلفل حار بلدية كاملة (أخضر أو أحمر)، مخللة في محلول ملحي مركز.",
        "desc_en": "Whole local farm hot chili peppers (emerald green and ruby red) preserved in concentrated artisanal sea salt brine.",
        "taste_ar": "لاذع جداً، حار، ويحفز الشهية.",
        "taste_en": "Fiery hot, exhilarating piquant burst, stimulating the appetite.",
        "use_ar": "محبوب جداً بجانب الأكلات الشعبية والمقبلات.",
        "use_en": "Highly sought-after condiment for street food delicacies, grilled dishes, and sharing mezze."
    },
    {
        "id": "stuffed_olive",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "7. مخلل الزيتون المشكل المحشي",
        "name_en": "Hand-Stuffed Gourmet Green Olives",
        "desc_ar": "زيتون أخضر كبير الحجم محشو بخليط الجزر المبشور والمكسرات أو الفلفل المفروم.",
        "desc_en": "Colossal green table olives meticulously stuffed with julienned carrots, roasted nuts, or minced red pimento peppers.",
        "taste_ar": "غني، متنوع النكهات، وممتاز الشكل.",
        "taste_en": "Luxurious multi-textured flavor symphony, buttery olive body, and vibrant savoury crunch.",
        "use_ar": "يُقدم في السفرات الفاخرة والبوفيهات المفتوحة.",
        "use_en": "Star presentation centerpieces for luxury banquets, 5-star hotel buffets, and VIP grazing tables."
    },
    {
        "id": "eggplant",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "name_ar": "8. مخلل الباذنجان البلدي (بالخلطة الحمراء)",
        "name_en": "Baladi Pickled Eggplant with Red Dressing",
        "desc_ar": "باذنجان مسلوق ومحشو بخلطة الثوم المفروم، الفلفل الأحمر، الليمون، والكمون.",
        "desc_en": "Tender poached petite baladi eggplants slit and filled with crushed garlic, fiery red peppers, lemon juice, and ground cumin.",
        "taste_ar": "غني جداً بالثوم والحموضة الشرقية الأصيلة.",
        "taste_en": "Deeply aromatic with fresh garlic, vivid cumin warmth, and authentic Egyptian citrus tang.",
        "use_ar": "مقبلات شعبية أساسية على السفرة المصرية.",
        "use_en": "Revered flagship appetizer and centerpiece on authentic Egyptian gastronomic tables."
    }
]

en_additions = {
    "nav_varieties_guide": "Varieties Guide",
    "guide_kicker": "ESTATE VARIETIES & QUALITY SPECIFICATIONS • TIER-1 MASTER REFERENCE",
    "guide_title": "Luxury Olive & Artisan Pickles Connoisseur Guide",
    "guide_subtitle": "Comprehensive Master Reference with Taste Profiles, Culinary Applications & Verified Studio Packshots",
    "guide_filter_all": "All Varieties (14)",
    "guide_filter_olives": "Part 1: Olive Varieties (6)",
    "guide_filter_pickles": "Part 2: Specialty & Mixed Pickles (8)",
    "guide_search_placeholder": "Search variety, flavor, or application...",
    "guide_zoom_label": "Zoom 4K",
    "guide_desc_label": "Description:",
    "guide_taste_label": "Taste & Palate:",
    "guide_use_label": "Culinary Use:",
    "guide_rfq_btn": "Request Wholesale Quote"
}

ar_additions = {
    "nav_varieties_guide": "دليل الأصناف الفاخر",
    "guide_kicker": "دليل الجودة والأصناف المعتمدة • TIER-1 MASTER REFERENCE",
    "guide_title": "دليل أصناف الزيتون والمخللات الشامل والفاخر",
    "guide_subtitle": "قائمة مرجعية متكاملة مع المواصفات والاستخدامات وأماكن الصور لكافة أصناف أرينا الزراعية الفاخرة",
    "guide_filter_all": "عرض كافة الأصناف (14)",
    "guide_filter_olives": "أولاً: أصناف الزيتون (6)",
    "guide_filter_pickles": "ثانياً: أنواع المخللات المشكلة والمميزة (8)",
    "guide_search_placeholder": "ابحث عن الصنف، المذاق، أو الاستخدام...",
    "guide_zoom_label": "تكبير 4K",
    "guide_desc_label": "الوصف:",
    "guide_taste_label": "المذاق:",
    "guide_use_label": "الاستخدام:",
    "guide_rfq_btn": "طلب تسعير الصنف"
}

for item in varieties_data:
    vid = item['id']
    en_additions[f"variety_{vid}_badge"] = item['category_badge_en']
    en_additions[f"variety_{vid}_name"] = item['name_en']
    en_additions[f"variety_{vid}_sub"] = item['name_ar']
    en_additions[f"variety_{vid}_desc"] = item['desc_en']
    en_additions[f"variety_{vid}_taste"] = item['taste_en']
    en_additions[f"variety_{vid}_use"] = item['use_en']

    ar_additions[f"variety_{vid}_badge"] = item['category_badge_ar']
    ar_additions[f"variety_{vid}_name"] = item['name_ar']
    ar_additions[f"variety_{vid}_sub"] = item['name_en']
    ar_additions[f"variety_{vid}_desc"] = item['desc_ar']
    ar_additions[f"variety_{vid}_taste"] = item['taste_ar']
    ar_additions[f"variety_{vid}_use"] = item['use_ar']

en_insert_str = ",\n" + ",\n".join([f'        "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in en_additions.items()])
if '"nav_videos": "Theater"' in html:
    html = html.replace('"nav_videos": "Theater"', '"nav_videos": "Theater"' + en_insert_str)
    print("Injected EN translations!")
else:
    print("Could not find nav_videos in EN")

ar_insert_str = ",\n" + ",\n".join([f'        "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in ar_additions.items()])
if '"nav_videos": "السينما"' in html:
    html = html.replace('"nav_videos": "السينما"', '"nav_videos": "السينما"' + ar_insert_str)
    print("Injected AR translations!")
else:
    print("Could not find nav_videos in AR")

with open('website.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated website.html saved with all i18n & scripts!")
