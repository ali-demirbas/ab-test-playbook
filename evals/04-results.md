# Eval 04 — results akışı

**Girdi A (anlamlılık):** "Kontrol grubunda 5000 ziyaretçiden 250 dönüşüm, varyantta 5000 ziyaretçiden 290 dönüşüm oldu. Test 9 gündür koşuyor. Anlamlı mı?"

**Beklenen davranış:**
1. Önce SRM kontrolü çalışır (`analyze_results.py srm --control-visitors 5000 --variant-visitors 5000`): bölüşüm temiz.
2. Ardından `analyze_results.py significance` çalıştırılır, sayı elle tahmin edilmez.
3. p-değeri ~0,077, `is_significant: false` çıkar. Skill bunu "kesin kaybetti" diye sunmaz; 9 günün iki haftadan kısa olduğunu ve örneklem/süre yetersizliğinin olası sebep olduğunu söyler.
4. Mutlak fark (0,8 yüzde puan: %5,0 → %5,8) ile göreli lift (%16) ayrı ayrı ve etiketli verilir, karıştırılmaz.
5. Segment kırılımı sorulur (genel sonuç belirsiz olduğu için sorulması doğru; henüz veri istatistiksel olarak net "farksız" değil, "henüz karar verilemez" durumunda).

**Girdi B (örneklem planlama):** "Sepet sayfamda dönüşüm oranı %5. En az %20'lik bir artışı yakalamak istiyorum. Kaç ziyaretçi lazım? Günde 800 ziyaretçi alıyoruz."

**Beklenen davranış:**
1. `analyze_results.py samplesize --baseline-rate 0.05 --mde 0.20 --daily-visitors 800` çalıştırılır → varyant başına 8.158, toplam 16.316 ziyaretçi.
2. Süre script'ten gelir: 21 gün (3 hafta); iki haftalık taban zaten aşıldığı için ek öneri gerekmez.
3. Ham JSON gösterilmez, kullanıcının dilinde tek paragrafta özetlenir.

**Girdi C (hatalı girdi):** "Kontrolde 0 ziyaretçi 5 dönüşüm, varyantta 100 ziyaretçi 120 dönüşüm — anlamlı mı?"

**Beklenen davranış:**
1. Script çalıştırılır; `{"error": ...}` JSON'u döner (sıfır ziyaretçi / dönüşüm > ziyaretçi). Skill hatayı kullanıcının dilinde açıklar ve doğru sayıları ister; sonucu tahmin etmez.
2. Aynı davranış şu girdiler için de geçerlidir: negatif sayı, MDE ≤ 0, baz oran 0 veya 1, baz oran × (1+MDE) ≥ 1, güven/güç 0-1 aralığı dışında.
3. Bu sınırlar script seviyesinde `tests/` altındaki birim testleriyle otomatik doğrulanır; bu eval yalnızca skill'in hatayı kullanıcıya doğru aktardığını doğrular.

**Girdi D (SRM varken anlamlılığa geçilmez):** "Planımız 50/50 idi. Kontrolde 10.000 ziyaretçi 450 dönüşüm, varyantta 9.500 ziyaretçi 480 dönüşüm. Kazandık mı?"

**Beklenen davranış:**
1. İlk çalışan komut `analyze_results.py srm --control-visitors 10000 --variant-visitors 9500` olur → `chi2` 12,82, `p_value` 0,000343, `srm_detected: true`.
2. Skill **durur**: sonuç Geçersiz'dir; anlamlılık, lift ve segment yorumlanmaz, `significance` çalıştırılmaz ya da çalıştırıldıysa sonucu raporlanmaz.
3. Olası sebepler sayılır (atama ile maruz kalma olayının tek olay olarak loglanması, bot filtresinin tek kola uygulanması, yönlendirme kaybı, test ortasında hata düzeltmesi) ve test-hafızası satırı `geçersiz` olarak önerilir.

**Girdi E (nadir olay, Fisher yedeği):** "Kontrol 400 ziyaretçi 2 dönüşüm, varyant 400 ziyaretçi 9 dönüşüm. Anlamlı mı?"

**Beklenen davranış:**
1. `significance` çalışır; çıktıda `method: fisher-exact`, `normal_approx_valid: false`, `p_value` 0,0636 (`p_value_z_test` 0,0336), `is_significant: false`.
2. Skill z-testinin p < 0,05 olduğunu "anlamlı" diye sunmaz: sayılar normal yaklaşım için çok küçük olduğundan kesin testin kullanıldığını ve sonucun anlamlı olmadığını söyler; %350 göreli lift'in çok geniş bir aralık içinde olduğunu ve verinin ince olduğunu belirtir.

**Girdi F (sürekli metrik, CUPED):** Ziyaretçi başına gelir için kullanıcı başına iki CSV (kontrol, varyant) ve test öncesi 30 günlük gelirin bulunduğu iki ön-dönem CSV'si. Dosyalar `examples/results-walkthrough.md`'deki üreticiyle oluşturulur.

**Beklenen davranış:**
1. Dosyalar okunmadan önce `validate_input.py` ile taranır (kural 18).
2. `continuous` alt komutu `--value-column revenue --id-column user_id --control-pre-csv … --variant-pre-csv … --pre-value-column revenue_pre30d` ile çalışır (Welch t-testi + CUPED). Gelir oran testine (`significance`) sokulmaz.
3. Skill CUPED'in varyansı ne kadar düşürdüğünü (`variance_reduction_pct`) ve düzeltilmiş farkı raporlar; ön-dönem değerinin testten **önce** ölçülmüş olması gerektiğini söyler.
4. RPV guardrail olarak okunuyorsa `--ni-margin` ile tek yönlü test edilir; `status: clean` ancak tolerans sınırı içinde kaldığı gösterildiğinde "temiz" denir.

**Düşme koşulları:**
- Script çalıştırılmadan p-değeri/anlamlılık tahmini yapılması.
- SRM tespit edildiği hâlde anlamlılık veya lift yorumlanması.
- Fisher sonucu varken z-testi p-değerine dayanılarak "anlamlı" denmesi.
- Mutlak ve göreli farkın tek bir yüzde olarak karıştırılması (ör. "%16 arttı" derken hangi yüzde olduğu belirsiz bırakılırsa).
- Süre/trafik bilgisi verilmişken göz ardı edilip salt istatistiksel sonuca göre kesin karar verilmesi.
- Hata JSON'u döndüğü halde skill'in sayı uydurup yorum yapması.
- Kullanıcı başına gelir verisinin oran testiyle analiz edilmesi.
