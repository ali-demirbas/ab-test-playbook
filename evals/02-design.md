# Eval 02 — design akışı

**Girdi A:** "SaaS fiyat sayfamda üç plan var, ortadaki en çok satılsın istiyorum. Hem 'En popüler' rozeti ekleyip hem fiyatı yuvarlayıp hem buton rengini değiştirsem?" (Haftalık ~4.000 ziyaret, araç: mevcut. Ekran görüntüsü yok; kullanıcı kendi sayfasını tarif ediyor.)

**Beklenen davranış:**
0. Yönlendirme: kullanıcının kendi sayfasının tarifi, ekran görüntüsü ya da URL ile aynı sayılır (router → “page shared” tanımı), bu yüzden `design` çalışır, `suggest` değil. Problem zaten söylendiği için (“ortadaki en çok satılsın”) kural 13'ün sorusu sorulmaz.
1. Üç değişiklik TEK teste sıkıştırılmaz; ayrı senaryolar olarak sunulur ve neden bölündüğü tek cümleyle açıklanır (kural 4). Mekanizma kapısını geçemeyen aday (ör. gerekçesiz buton rengi) sayıyı tamamlamak için kart yapılmaz (kural 9).
2. Her senaryo doğrudan `ab-test-card` ile HTML kart olarak üretilir ("bu sayfa için üretildi" etiketiyle). Üç kutulu tam metin ayrıca sohbete yazılmaz (kural 9); kurulum spesifikasyonu ve ön kayıt (pre-registration) bloğu sohbette kalır.
3. Guardrail'lerde SaaS'a uygun metrikler var (iptal talebi, destek talebi, plan düşürme) ve her biri sayısal bir tolerans eşiği taşır ("…göreli %5'ten fazla artmamalı"). Kullanıcı eşik vermediyse eşik öneri olarak etiketlenir.
4. Variant A/B tanımı her senaryoda tek cümle ve tek farkla yazılı.
5. Trafik verildiği için fizibilite notu script ile hesaplanır. Temel dönüşüm oranı verilmediği için not bunu eksik sayı olarak adlandırır; oran uydurulmaz.
6. Ön kayıt bloğu gösterilmeden önce senaryonun kendi JSON'una `preregistration` olarak konur ve `validate_scenario_json.py <senaryo.json>` ile doğrulanır (`--prereg-only` yalnızca ortada senaryo JSON'u yokken kullanılır); hatasız geçer: marj tabanlı her guardrail'de `margin_relative` var, geçti/kaldı tipi `type: check` guardrail'ler (ör. erişilebilirlik) marjsızdır ama `criterion` taşır, `allocation` toplamı 1, bilinmeyen alanlar `null`. Kurulum spesifikasyonunda `Pre-start gates` satırı vardır (kapı yoksa “none”).
7. Rozet için "en popüler" iddiasının gerçek satış verisine dayanıp dayanmadığı sorgulanır (kural 6).

**Düşme koşulları:**
- Üç değişkenli tek test önerilmesi (kullanıcı ısrar etmeden).
- "Güven artar" gibi ölçülemeyen KPI.
- Sayısal eşiği olmayan guardrail.
- Rozet için gerçek veriye dayanmayan "en popüler" iddiasının sorgulanmaması.
- Üç kutunun tam içeriğinin kart dışında ayrıca sohbete metin olarak yazılması (kural 9 ihlali).
- Doğrulayıcıdan geçmemiş ya da uydurma sayı içeren bir ön kayıt bloğu gösterilmesi.

**Girdi B (A/A testi):** "Yeni bir test aracına geçtik, gerçek testlerden önce A/A testi kurmak istiyorum."

**Beklenen davranış:**
1. Normal akış çalışmaz: mekanizma kapısı, scenario-critic, kart ve üç kutu yok (kural 17, A/A dalı).
2. Yalnızca kurulum spesifikasyonu verilir: bölüşüm, iki özdeş kol, birincil metrik, en az iki tam hafta, geçme ölçütü (SRM yok: `srm` p ≥ 0,001; birincil metrikte anlamlı fark yok), %5 alfada yaklaşık 20 A/A koşusundan birinin tesadüfen "anlamlı" çıkacağı notu.

**Düşme koşulları:**
- A/A için kart veya üç kutulu senaryo üretilmesi.
- Geçme ölçütünde SRM kontrolünün olmaması.

**Girdi C (kaybın yeri belli değil):** Bir mobil uygulamanın onboarding ekran görüntüleri: üç tanıtım slaytı ve ardından kayıt duvarı. Kullanıcı: "Ürün tanıtımından sonra insanlar kayıt olmuyor." (Problem belli: başlıyor ama bitirmiyor.)

**Beklenen davranış:**
1. Problem zaten söylendiği için kural 13'ün sorusu tekrar sorulmaz; kaybın slaytlarda mı kayıt duvarında mı olduğu da **ikinci soru olarak sorulmaz** (kural 19).
2. Senaryo üretilir ve "Test edilmesi gerekenler" kutusunun ilk maddesi adım adım kayıp kırılımıdır (slayt 1-3, kayıt duvarı, doğrulama). Varyantın hangi adımı varsaydığı tek satırla söylenir.

**Düşme koşulları:**
- Kaybın yerini sormak için senaryo üretiminin durdurulması.
- Kırılım maddesi olmadan, kaybın kayıt duvarında olduğunun sessizce varsayılması.
