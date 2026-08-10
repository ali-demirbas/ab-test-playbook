# Eval 04 — results akışı

**Girdi A (anlamlılık):** "Kontrol grubunda 5000 ziyaretçiden 250 dönüşüm, varyantta 5000 ziyaretçiden 290 dönüşüm oldu. Test 9 gündür koşuyor. Anlamlı mı?"

**Beklenen davranış:**
1. `analyze_results.py significance` script'i çalıştırılır, sayı elle tahmin edilmez.
2. p-değeri ~0.077, `is_significant: false` çıkar. Skill bunu "kesin kaybetti" diye sunmaz; 9 günün iki haftadan kısa olduğunu ve örneklem/süre yetersizliğinin olası sebep olduğunu söyler.
3. Mutlak fark (0,8 yüzde puan: %5,0 → %5,8) ile göreli lift (%16) ayrı ayrı ve etiketli verilir, karıştırılmaz.
4. Segment kırılımı sorulur (genel sonuç belirsiz olduğu için sorulması doğru; henüz veri istatistiksel olarak net "farksız" değil, "henüz karar verilemez" durumunda).

**Girdi B (örneklem planlama):** "Sepet sayfamda dönüşüm oranı %5. En az %20'lik bir artışı yakalamak istiyorum. Kaç ziyaretçi lazım? Günde 800 ziyaretçi alıyoruz."

**Beklenen davranış:**
1. `analyze_results.py samplesize --baseline-rate 0.05 --mde 0.20` çalıştırılır → varyant başına ~8158 gerekiyor.
2. Toplam ~16316 ziyaretçi, günlük 800 ile ~20-21 gün sürer hesabı yapılır ve iki haftadan uzun olduğu için ek öneri gerekmez (zaten yeterli).
3. Ham JSON gösterilmez, Türkçeleştirilip tek paragrafta özetlenir.

**Girdi C (hatalı girdi):** "Kontrolde 0 ziyaretçi 5 dönüşüm, varyantta 100 ziyaretçi 120 dönüşüm — anlamlı mı?"

**Beklenen davranış:**
1. Script çalıştırılır; `{"error": ...}` JSON'u döner (sıfır ziyaretçi / dönüşüm > ziyaretçi). Skill hatayı Türkçe açıklar ve doğru sayıları ister; sonucu tahmin etmez.
2. Aynı davranış şu girdiler için de geçerlidir: negatif sayı, MDE ≤ 0, baz oran 0 veya 1, baz oran × (1+MDE) ≥ 1, güven/güç 0-1 aralığı dışında.
3. Bu sınırlar script seviyesinde `tests/test_analyze_results.py` ile otomatik test edilir; bu eval yalnızca skill'in hatayı kullanıcıya doğru aktardığını doğrular.

**Düşme koşulları:**
- Script çalıştırılmadan p-değeri/anlamlılık tahmini yapılması.
- Mutlak ve göreli farkın tek bir yüzde olarak karıştırılması (ör. "%16 arttı" derken hangi yüzde olduğu belirsiz bırakılırsa).
- Süre/trafik bilgisi verilmişken göz ardı edilip salt istatistiksel sonuca göre kesin karar verilmesi.
- Hata JSON'u döndüğü halde skill'in sayı uydurup yorum yapması.
