# Eval 02 — design akışı

**Girdi:** "SaaS fiyat sayfamda üç plan var, ortadaki en çok satılsın istiyorum. Hem 'En popüler' rozeti ekleyip hem fiyatı yuvarlayıp hem buton rengini değiştirsem?" (Haftalık ~4.000 ziyaret, araç: mevcut.)

**Beklenen davranış:**
1. Üç değişiklik TEK teste sıkıştırılmaz; üç ayrı senaryo olarak sunulur ve neden bölündüğü tek cümleyle açıklanır.
2. Her senaryo doğrudan `ab-test-card` ile HTML kart olarak üretilir ("bu sayfa için üretildi" etiketiyle) — üç kutulu tam metin ayrıca sohbete yazılmaz (kural 9), kurulum spesifikasyonu sohbette kalır.
3. Guardrail'lerde SaaS'a uygun metrikler var (iptal talebi, destek talebi, plan düşürme).
4. Variant A/B tanımı her senaryoda tek cümle ve tek farkla yazılı.
5. Trafik verildiği için kaba süre tahmini yapılabilir; yapıldıysa varsayımı belirtilmiş.

**Düşme koşulları:**
- Üç değişkenli tek test önerilmesi (kullanıcı ısrar etmeden).
- "Güven artar" gibi ölçülemeyen KPI.
- Rozet için gerçek veriye dayanmayan "en popüler" iddiasının sorgulanmaması (etik kural).
- Üç kutunun tam içeriğinin kart dışında ayrıca sohbete metin olarak yazılması (kural 9 ihlali).
