# Eval 03 — audit akışı

**Girdi A:** İki varyant görseli/tarifi: A'da "Baskılı Tişört, 350 TL, (3) yorum"; B'de "Beyaz Tişört, 350 TL, (10) yorum, -%20 rozeti + 'Peşin fiyatına 3 taksit' rozeti". Kullanıcı sorusu: "Taksit rozeti testim doğru kurulmuş mu?"

**Beklenen davranış:**
1. Confound'lar yakalanır: farklı ürün, farklı yorum sayısı, fazladan indirim rozeti — üçü de `[Engelleyici]` olarak listelenir.
2. Her bulgu: tek cümle sorun + tek cümle düzeltme (ürünü eşitle, yorumu eşitle, indirim rozetini kaldır).
3. KPI sorulur veya plan paylaşıldıysa birincil/guardrail denetlenir.
4. Sonda net karar: "Bu haliyle koşulamaz; şu üç eşitleme yapılırsa koşulabilir."

**Düşme koşulları:**
- Confound'lardan herhangi birinin kaçırılması.
- "Genel olarak iyi görünüyor" tarzı kararsız kapanış.
- Var olmayan sorun uydurma (ör. fiyatlar zaten eşitken fiyat farkı bulgusu).

**Girdi B (dosya olarak gelen kusurlu plan):** `plan.md` dosyası: "Ana sayfaya kampanya banner'ı ekliyoruz, yalnızca B'de görünecek. Birincil metrik: banner tıklama oranı (banner tıklaması / banner gösterimi). Guardrail: sepet terki düşmemeli. Mobil, masaüstü, yeni ve dönen kullanıcıdan hangisi kazanırsa oraya yayınlayacağız."

**Beklenen davranış:**
1. Dosya okunmadan önce `validate_input.py plan.md` çalışır (kural 18).
2. Şu bulgular ayrı ayrı yazılır:
   - Hipotez/mekanizma yok: banner'ın neden davranışı değiştireceği söylenmemiş (`[Ciddi]`).
   - Birincil metrik bir ara vekil: banner tıklaması, değişikliğin asıl hedeflediği sipariş veya ziyaretçi başına gelir değil (`[Ciddi]`).
   - Payda iki kolda aynı değil: A'da banner yok, dolayısıyla "banner gösterimi" paydası yalnızca B'de var; iki kol ana sayfaya gelen herkes üzerinden ölçülmeli (`[Engelleyici]`).
   - Guardrail'in sayısal eşiği yok: "düşmemeli" bir sayı olmadan karara bağlanamaz (`[Ciddi]`).
   - Dört segmentten kazananı seçmek çoklu karşılaştırma sorunudur: önceden tek bir karar segmenti ya da `analyze_results.py interaction` ile resmî etkileşim testi istenir (`[Ciddi]`).
   - "Yapılmaması gerekenler" bloğunun yokluğu bulgu olarak yazılır; plan üç kutuya zorla dökülmez (kural 1).
3. Sonda net karar: "Bu haliyle koşulamaz" ve koşulabilmesi için gereken düzeltmeler.

**Düşme koşulları:**
- Payda uyuşmazlığının kaçırılması.
- Banner tıklamasının birincil metrik olarak kabul edilmesi.
- "En iyi segmente yayınla" planının bulgu yazılmadan geçirilmesi.
