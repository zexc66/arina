import re

with open('website.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build Varieties Guide HTML
guide_html = '''  <!-- ========================================================================= -->
  <!-- 6. LUXURY OLIVE & PICKLE VARIETIES COMPENDIUM (دليل أصناف الزيتون والمخللات الشامل والفاخر) -->
  <!-- ========================================================================= -->
  <section id="varieties-guide" class="py-28 bg-brand-forest-obsidian border-t border-brand-gold/30 relative overflow-hidden">
    <!-- Atmospheric Ambient Glows -->
    <div class="absolute -top-40 left-1/2 -translate-x-1/2 w-[900px] h-[450px] bg-gradient-to-b from-brand-gold/15 to-transparent blur-[140px] pointer-events-none"></div>
    <div class="absolute bottom-0 right-10 w-[500px] h-[500px] bg-brand-forest/20 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- Section Header -->
      <div class="text-center max-w-3xl mx-auto space-y-4 mb-14">
        <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-brand-gold/10 border border-brand-gold/30 text-[10px] sm:text-[11px] font-bold uppercase tracking-[0.22em] text-brand-gold font-display">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-gold animate-pulse"></span>
          <span data-i18n="guide_kicker">دليل الجودة والأصناف المعتمدة • TIER-1 MASTER REFERENCE</span>
        </div>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-brand-ivory" data-i18n="guide_title">
          دليل أصناف الزيتون والمخللات الشامل والفاخر
        </h2>
        <p class="text-brand-gold text-base sm:text-lg font-medium leading-relaxed" data-i18n="guide_subtitle">
          قائمة مرجعية متكاملة مع المواصفات والاستخدامات وأماكن الصور لكافة أصناف أرينا الزراعية الفاخرة
        </p>
      </div>

      <!-- Controls Bar: Filter Tabs & Real-Time Search -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-12 pb-6 border-b border-brand-gold/20">
        
        <!-- Filter Tabs -->
        <div class="flex flex-wrap items-center gap-2.5 w-full md:w-auto justify-center md:justify-start">
          <button id="guide-tab-all" onclick="filterVarieties('all')" class="guide-filter-btn active-filter px-5 py-2.5 rounded-full text-xs font-bold transition-all border border-brand-gold bg-brand-gold text-brand-forest-obsidian shadow-md cursor-pointer">
            <span data-i18n="guide_filter_all">عرض كافة الأصناف (14)</span>
          </button>
          <button id="guide-tab-olives" onclick="filterVarieties('olives')" class="guide-filter-btn px-5 py-2.5 rounded-full text-xs font-bold transition-all border border-brand-gold/30 bg-brand-forest-dark/70 text-brand-ivory hover:border-brand-gold hover:text-brand-gold cursor-pointer">
            <span data-i18n="guide_filter_olives">أولاً: أصناف الزيتون (6)</span>
          </button>
          <button id="guide-tab-pickles" onclick="filterVarieties('pickles')" class="guide-filter-btn px-5 py-2.5 rounded-full text-xs font-bold transition-all border border-brand-gold/30 bg-brand-forest-dark/70 text-brand-ivory hover:border-brand-gold hover:text-brand-gold cursor-pointer">
            <span data-i18n="guide_filter_pickles">ثانياً: أنواع المخللات المشكلة والمميزة (8)</span>
          </button>
        </div>

        <!-- Search Input -->
        <div class="relative w-full md:w-80">
          <input type="text" id="guide-search-input" oninput="searchVarieties(this.value)" placeholder="ابحث عن الصنف، المذاق، أو الاستخدام..." data-i18n-placeholder="guide_search_placeholder" class="w-full ps-10 pe-4 py-2.5 rounded-full bg-brand-forest-dark/90 border border-brand-gold/30 text-xs text-brand-ivory focus:border-brand-gold focus:outline-none placeholder-brand-ivory/45 transition-colors">
          <svg class="w-4 h-4 text-brand-gold absolute start-3.5 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>

      </div>

      <!-- Varieties Grid (14 Master Cards) -->
      <div id="varieties-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
'''

varieties_data = [
    # --- أولاً: أصناف الزيتون ---
    {
        "id": "kalamata",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "01",
        "name_ar": "1. زيتون كالاماتا (Kalamata)",
        "name_en": "Royal Kalamata Olives",
        "desc_ar": "زيتون يوناني شهير ذو لون بنفسجي غامق ورائحة مميزة، يتميز بحبة كبيرة وشكل لوزي وقوام لحمي غني.",
        "desc_en": "Famous Greek olive variety with deep purple lustrous color, distinctive aroma, large almond silhouette, and luscious meaty texture.",
        "taste_ar": "غني، مالح، ويحتوي على نكهة فاكهية عميقة.",
        "taste_en": "Rich, balanced salinity, layered with profound fruity undertones.",
        "use_ar": "ممتاز كمقبلات مع الجبن، وفي السلطات اليونانية.",
        "use_en": "Superb table appetizer paired with artisanal cheeses and authentic Mediterranean salads.",
        "img": "output/imagery/arina_royal_kalamata_olives_white_studio_hero_4k.jpg"
    },
    {
        "id": "toffahi",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "02",
        "name_ar": "2. زيتون تفاحي أخضر",
        "name_en": "Egyptian Green Toffahi Olives",
        "desc_ar": "زيتون مصري أصيل حباته مستديرة وكبيرة تشبه التفاح، ذو قشرة سميكة ولحم وفير.",
        "desc_en": "Authentic Egyptian heirloom olive with large round apple-like shape, thick crisp skin, and abundant succulent flesh.",
        "taste_ar": "مقرمش، قليل المرارة، ومثالي للتخليل السريع.",
        "taste_en": "Extra crunchy, mild delicate bitterness, ideal for express cure preservation.",
        "use_ar": "يُفضل حجماً ومذاقاً للتخليل المَحشي (بالجزر والفلفل).",
        "use_en": "Premium choice for hand-stuffed cured preparations (carrots, peppers & herbs).",
        "img": "output/imagery/arina_pitted_green_olives_white_studio_hero_4k.jpg"
    },
    {
        "id": "azizi",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "03",
        "name_ar": "3. زيتون العزيزي",
        "name_en": "Egyptian Azizi Estate Olives",
        "desc_ar": "من أجود أنواع الزيتون المصري، حباته بيضاوية الشكل ولونه يميل للأصفر الفاتح عند النضج.",
        "desc_en": "Finest heirloom Egyptian estate olive, featuring oval geometry and pale golden-green hues upon optimal maturity.",
        "taste_ar": "نسبة الزيت فيه عالية جداً، ومذاقه غني ودسم.",
        "taste_en": "Exceptionally high natural oil concentration with deep buttery, rich palate density.",
        "use_ar": "يُستخدم للكبس والتخليل وأيضاً لاستخراج أفضل زيت زيتون.",
        "use_en": "Exceptional for barrel curing, table pickling, and pressing into premier extra virgin olive oil.",
        "img": "output/imagery/arina_sliced_green_olives_white_studio_hero_4k.jpg"
    },
    {
        "id": "spanish_black",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "04",
        "name_ar": "4. زيتون أسود إسباني (مخلوط/ناضج)",
        "name_en": "Spanish Ripe Black Olives",
        "desc_ar": "حبات متساوية الحجم، معالجة بطريقة خاصة لتفقد مرارتها تماماً وتصبح طرية.",
        "desc_en": "Uniformly calibrated ripe olives, specially cured to eliminate bitterness and yield a velvety tender bite.",
        "taste_ar": "ناعم، مالح بدرجة معتدلة، وغير لاذع.",
        "taste_en": "Velvety smooth, mild gentle salinity, and beautifully mellow non-astringent profile.",
        "use_ar": "مثالي لتزيين البيتزا، الساندويتشات، وسلطات المعكرونة.",
        "use_en": "Perfect garnish for artisan pizzas, deli sandwiches, and gourmet pasta salads.",
        "img": "output/imagery/arina_natural_black_olives_white_studio_hero_4k.jpg"
    },
    {
        "id": "dolce",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "05",
        "name_ar": "5. زيتون دولسي (المحلى / الأخضر المفرغ)",
        "name_en": "Dolce Sweet Pitted Green Olives",
        "desc_ar": "زيتون أخضر مفرغ النواة ومُعالج خصيصاً ليصبح حلو المذاق وخالياً تماماً من المرارة.",
        "desc_en": "Precision-pitted whole green olives, uniquely cured to achieve a delicate sweet profile zero bitterness.",
        "taste_ar": "طري، خفيف، ونظيف الطعم.",
        "taste_en": "Tender, light, crisp, and exceptionally clean gastronomic flavor.",
        "use_ar": "مثالي جداً للحشو السريع وإضافته للأطباق الإيطالية.",
        "use_en": "Ideal for rapid gourmet stuffing, antipasti platters, and authentic Italian pasta preparations.",
        "img": "output/imagery/arina_pitted_green_olives_solo_4k.jpg"
    },
    {
        "id": "picual",
        "category": "olives",
        "category_badge_ar": "أولاً: أصناف الزيتون",
        "category_badge_en": "Part 1: Olive Varieties",
        "num": "06",
        "name_ar": "6. زيتون بيكول (الرفيع المائل للطول)",
        "name_en": "Elongated Picual Olives",
        "desc_ar": "زيتون رفيع وطويل الشكل يتميز بكثافة اللحم بالنسبة للحجم وقوام صلب.",
        "desc_en": "Slender elongated olive variety boasting superior flesh-to-pit ratio and a remarkably firm, crisp bite.",
        "taste_ar": "حاد، غني، ونكهته تتركز بقوة.",
        "taste_en": "Piquant, robust, and intensely concentrated authentic olive terroir.",
        "use_ar": "رائع في أطباق البار ووجبات السناك الخفيفة.",
        "use_en": "Superb for luxury bar tapas, charcuterie boards, and gourmet finger snacks.",
        "img": "output/imagery/arina_sliced_black_olives_white_studio_hero_4k.jpg"
    },
    # --- ثانياً: أنواع المخللات المشكلة والمميزة ---
    {
        "id": "lemon_asfar",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "07",
        "name_ar": "1. مخلل الليمون المعصفر",
        "name_en": "Preserved Lemon with Safflower",
        "desc_ar": "ليمون بلدي كامل محشو بخليط من العصفر، حبة البركة، والملح الخشن.",
        "desc_en": "Whole authentic Egyptian baladi lemons hand-stuffed with aromatic saffron florets, nigella black seed, and coarse sea crystals.",
        "taste_ar": "حامض، غني بالنكهات الشرقية والزيوت العطرية لقشور الليمون.",
        "taste_en": "Tangy citrus zing infused with warm oriental aromatics and essential zest oils.",
        "use_ar": "مرافق أساسي للمشويات والأطباق الشعبية الدسمة.",
        "use_en": "Essential companion to charcoal-grilled meats, tagines, and traditional feast dishes.",
        "img": "output/imagery/arina_ruby_and_emerald_duo_spectacle_4k.jpg"
    },
    {
        "id": "cucumber",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "08",
        "name_ar": "2. مخلل الخيار المقرمش",
        "name_en": "Acoustic Crisp Baby Cucumbers",
        "desc_ar": "خيار رفيع وصغير الحجم، مخلل مع الثوم وأوراق النعناع أو الكرفس الطازجة.",
        "desc_en": "Slender petite greenhouse cucumbers cured with fresh crushed garlic cloves, garden mint leaves, and crisp celery stalks.",
        "taste_ar": "شديد القرمشة، منعش، وحامض بانتظام.",
        "taste_en": "Ultra-crunchy acoustic snap, lively freshness, and harmonious calibrated acidity.",
        "use_ar": "مثالي بجانب البرجر، الساندويتشات السريعة، والمقبلات الشامية.",
        "use_en": "Benchmark pairing for gourmet burgers, deli panini, and Levantine mezze spreads.",
        "img": "output/imagery/arina_crisp_baby_cucumbers_white_studio_hero_4k.jpg"
    },
    {
        "id": "turnip",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "09",
        "name_ar": "3. مخلل اللفت الشتوي",
        "name_en": "Winter Wild Turnip in Ruby Beetroot",
        "desc_ar": "قطع لفت مقطعة على شكل أصابع أو مكعبات، مخللة مع قطع البنجر (الشمندر) التي تمنحه اللون الوردي الجذاب.",
        "desc_en": "Hand-batoned winter turnips cured naturally with fresh organic beetroot slices, imparting radiant ruby pigmentation.",
        "taste_ar": "طري، مقرمش، بنكهة ترابية خفيفة وحموضة متوازنة.",
        "taste_en": "Crisp tender bite, subtle earthy sweetness, and exquisitely balanced brine acidity.",
        "use_ar": "طبق جانبي لا غنى عنه مع الفول، الفلافل، والمشويات.",
        "use_en": "Indispensable classic side accompaniment for falafel, breakfast mezze, and rotisserie meats.",
        "img": "output/imagery/arina_wild_turnip_beetroot_white_studio_hero_4k.jpg"
    },
    {
        "id": "carrot_chili",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "10",
        "name_ar": "4. مخلل الجزر والفلفل الحار (مكس)",
        "name_en": "Royal Mixed Pickles (Carrot & Hot Chili)",
        "desc_ar": "شرائح جزر مقرمشة ممزوجة مع قرون الفلفل الأخضر أو الأحمر الحار والثوم.",
        "desc_en": "Crinkle-cut sweet carrots tossed with fiery whole red and green chilies, bay aromatics, and crushed garlic.",
        "taste_ar": "حار، لاذع، ومقرمش يفتح الشهية.",
        "taste_en": "Fiery, appetizingly piquant, and intensely crunchy palate stimulator.",
        "use_ar": "يضيف نكهة قوية ومميزة لأطباق الأرز والكبسة والأكلات الشعبية.",
        "use_en": "Adds vivid zest and crunch to spiced basmati rice, kabsa, and hearty sharing dishes.",
        "img": "output/imagery/arina_royal_mixed_pickles_white_studio_hero_4k.jpg"
    },
    {
        "id": "pearl_onion",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "11",
        "name_ar": "5. مخلل البصل الصغير (البصل البلدي)",
        "name_en": "Hand-Peeled Baladi Pearl Onions",
        "desc_ar": "بصل صغير كامل ومقشر، مخلل بعناية ليحتفظ بقوامه الصلب دون أن يترهل.",
        "desc_en": "Petite whole hand-peeled baladi onions, cured with precision to preserve maximum cellular crunch without softening.",
        "taste_ar": "مقرمش، ذو حموضة ممتازة ونكهة بصلية محببة.",
        "taste_en": "Briskly crunchy, pristine vinegar bite, and delightful sweet allium undertone.",
        "use_ar": "ممتاز بجانب المشاوي والسندويتشات الشرقية.",
        "use_en": "Magnificent accompaniment to char-grilled kebabs, shawarma, and deli wraps.",
        "img": "output/imagery/arina_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg"
    },
    {
        "id": "hot_pepper",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "12",
        "name_ar": "6. مخلل الفلفل الحار الكامل",
        "name_en": "Whole Fiery Baladi Chili Peppers",
        "desc_ar": "قرون فلفل حار بلدية كاملة (أخضر أو أحمر)، مخللة في محلول ملحي مركز.",
        "desc_en": "Whole local farm hot chili peppers (emerald green and ruby red) preserved in concentrated artisanal sea salt brine.",
        "taste_ar": "لاذع جداً، حار، ويحفز الشهية.",
        "taste_en": "Fiery hot, exhilarating piquant burst, stimulating the appetite.",
        "use_ar": "محبوب جداً بجانب الأكلات الشعبية والمقبلات.",
        "use_en": "Highly sought-after condiment for street food delicacies, grilled dishes, and sharing mezze.",
        "img": "output/imagery/arina_royal_mixed_pickles_petite_210g_white_studio_hero_4k.jpg"
    },
    {
        "id": "stuffed_olive",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "13",
        "name_ar": "7. مخلل الزيتون المشكل المحشي",
        "name_en": "Hand-Stuffed Gourmet Green Olives",
        "desc_ar": "زيتون أخضر كبير الحجم محشو بخليط الجزر المبشور والمكسرات أو الفلفل المفروم.",
        "desc_en": "Colossal green table olives meticulously stuffed with julienned carrots, roasted nuts, or minced red pimento peppers.",
        "taste_ar": "غني، متنوع النكهات، وممتاز الشكل.",
        "taste_en": "Luxurious multi-textured flavor symphony, buttery olive body, and vibrant savoury crunch.",
        "use_ar": "يُقدم في السفرات الفاخرة والبوفيهات المفتوحة.",
        "use_en": "Star presentation centerpieces for luxury banquets, 5-star hotel buffets, and VIP grazing tables.",
        "img": "output/imagery/arina_almond_stuffed_olives_white_studio_hero_4k.jpg"
    },
    {
        "id": "eggplant",
        "category": "pickles",
        "category_badge_ar": "ثانياً: أنواع المخللات المشكلة والمميزة",
        "category_badge_en": "Part 2: Specialty & Mixed Pickles",
        "num": "14",
        "name_ar": "8. مخلل الباذنجان البلدي (بالخلطة الحمراء)",
        "name_en": "Baladi Pickled Eggplant with Red Dressing",
        "desc_ar": "باذنجان مسلوق ومحشو بخلطة الثوم المفروم، الفلفل الأحمر، الليمون، والكمون.",
        "desc_en": "Tender poached petite baladi eggplants slit and filled with crushed garlic, fiery red peppers, lemon juice, and ground cumin.",
        "taste_ar": "غني جداً بالثوم والحموضة الشرقية الأصيلة.",
        "taste_en": "Deeply aromatic with fresh garlic, vivid cumin warmth, and authentic Egyptian citrus tang.",
        "use_ar": "مقبلات شعبية أساسية على السفرة المصرية.",
        "use_en": "Revered flagship appetizer and centerpiece on authentic Egyptian gastronomic tables.",
        "img": "output/imagery/arina_garlic_stuffed_olives_white_studio_hero_4k.jpg"
    }
]

for item in varieties_data:
    card = f'''        <!-- Variety Card: {item['id']} -->
        <div class="variety-card tilt-card rounded-[2rem] p-1.5 glass-card-shell overflow-hidden transition-all duration-300 hover:shadow-[0_20px_50px_rgba(218,172,54,0.15)] flex flex-col" data-category="{item['category']}" data-search="{item['name_ar']} {item['name_en']} {item['desc_ar']} {item['desc_en']} {item['taste_ar']} {item['taste_en']} {item['use_ar']} {item['use_en']}">
          <div class="rounded-[calc(2rem-0.375rem)] bg-gradient-to-b from-brand-forest-dark/95 to-brand-forest-obsidian/95 p-5 sm:p-6 flex flex-col justify-between h-full border border-brand-gold/15 group">
            
            <div>
              <!-- Header Pill & Index -->
              <div class="flex items-center justify-between gap-2 mb-4">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-gold/10 border border-brand-gold/30 text-[10px] font-bold text-brand-gold uppercase tracking-wider">
                  <span class="w-1.5 h-1.5 rounded-full bg-brand-gold"></span>
                  <span data-i18n="variety_{item['id']}_badge">{item['category_badge_ar']}</span>
                </span>
                <span class="text-xs font-mono font-bold text-brand-gold/40">#{item['num']}</span>
              </div>

              <!-- Product Studio Packshot [ضع صورة الصنف هنا] -->
              <div class="relative w-full aspect-[4/3] rounded-2xl bg-white p-3 mb-4 flex items-center justify-center overflow-hidden cursor-pointer group/img shadow-md border border-brand-gold/20" onclick="openLightbox('{item['img']}', '{item['name_en']}', '{item['name_ar']}', '{item['desc_en']}', '{item['desc_ar']}')">
                <img src="{item['img']}" alt="{item['name_en']}" loading="lazy" decoding="async" class="h-full w-full object-contain transition-transform duration-500 group-hover/img:scale-105">
                <div class="absolute bottom-2 end-2 bg-brand-forest-obsidian/90 border border-brand-gold/40 text-brand-gold text-[10px] font-bold px-2.5 py-1 rounded-full backdrop-blur-md opacity-0 group-hover/img:opacity-100 transition-opacity flex items-center gap-1.5 shadow-lg">
                  <svg class="w-3 h-3 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"/></svg>
                  <span data-i18n="guide_zoom_label">تكبير 4K</span>
                </div>
              </div>

              <!-- Title -->
              <div class="mb-4 text-start">
                <h3 class="text-lg sm:text-xl font-bold font-serif text-brand-ivory group-hover:text-brand-gold transition-colors leading-snug" data-i18n="variety_{item['id']}_name">
                  {item['name_ar']}
                </h3>
                <div class="text-[11px] text-brand-gold/80 font-medium tracking-wide mt-0.5" data-i18n="variety_{item['id']}_sub">
                  {item['name_en']}
                </div>
              </div>

              <!-- Technical Specifications & Palate Details -->
              <div class="space-y-3 text-xs leading-relaxed text-start">
                
                <!-- 1. Description (الوصف) -->
                <div class="p-3 rounded-xl bg-brand-forest-obsidian/80 border border-brand-gold/15">
                  <div class="flex items-center gap-1.5 text-brand-gold font-bold text-[11px] mb-1">
                    <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    <span data-i18n="guide_desc_label">الوصف:</span>
                  </div>
                  <p class="text-brand-ivory/85 text-[11.5px]" data-i18n="variety_{item['id']}_desc">{item['desc_ar']}</p>
                </div>

                <!-- 2. Taste (المذاق) -->
                <div class="p-3 rounded-xl bg-brand-forest-obsidian/80 border border-brand-gold/15">
                  <div class="flex items-center gap-1.5 text-brand-gold font-bold text-[11px] mb-1">
                    <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                    <span data-i18n="guide_taste_label">المذاق:</span>
                  </div>
                  <p class="text-brand-ivory/85 text-[11.5px]" data-i18n="variety_{item['id']}_taste">{item['taste_ar']}</p>
                </div>

                <!-- 3. Culinary Use (الاستخدام) -->
                <div class="p-3 rounded-xl bg-brand-forest-obsidian/80 border border-brand-gold/15">
                  <div class="flex items-center gap-1.5 text-brand-gold font-bold text-[11px] mb-1">
                    <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                    <span data-i18n="guide_use_label">الاستخدام:</span>
                  </div>
                  <p class="text-brand-ivory/85 text-[11.5px]" data-i18n="variety_{item['id']}_use">{item['use_ar']}</p>
                </div>

              </div>
            </div>

            <!-- Action Button -->
            <button onclick="requestVarietyRFQ('{item['name_ar']}')" class="w-full mt-4 py-2.5 px-4 rounded-xl border border-brand-gold/40 bg-brand-gold/10 hover:bg-brand-gold hover:text-brand-forest-obsidian text-brand-gold text-xs font-bold transition-all duration-300 flex items-center justify-center gap-2 group/btn cursor-pointer">
              <span data-i18n="guide_rfq_btn">طلب تسعير الصنف</span>
              <svg class="w-3.5 h-3.5 group-hover/btn:translate-x-1 rtl:group-hover/btn:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>

          </div>
        </div>
'''
    guide_html += card

guide_html += '''      </div>

    </div>
  </section>
'''

# Replace the video section in html
video_section_pattern = re.compile(r'<!-- ={10,}\s*-->\s*<!-- 6\. COMMERCIAL 4K VIDEO THEATER -->\s*<!-- ={10,}\s*-->\s*<section id="videos".*?</section>', re.DOTALL)

if not video_section_pattern.search(html):
    print("Could not find video section with regex, trying substring find...")
    idx1 = html.find('<!-- 6. COMMERCIAL 4K VIDEO THEATER -->')
    idx2 = html.find('<!-- 7. WHOLESALE RFQ & REAL-TIME PROFORMA TICKET -->')
    assert idx1 != -1 and idx2 != -1
    # Find the comment start before idx1
    start_pos = html.rfind('<!-- ===', 0, idx1)
    new_html = html[:start_pos] + guide_html + '\n\n' + html[idx2:]
else:
    new_html = video_section_pattern.sub(guide_html.strip(), html)

print("Video section replaced with Varieties Guide!")
with open('website.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated website.html saved!")
