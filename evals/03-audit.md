# Eval 03 — audit akışı

**Girdi:** İki varyant görseli/tarifi: A'da "Baskılı Tişört, 350 TL, (3) yorum"; B'de "Beyaz Tişört, 350 TL, (10) yorum, -%20 rozeti + 'Peşin fiyatına 3 taksit' rozeti". Kullanıcı sorusu: "Taksit rozeti testim doğru kurulmuş mu?"

**Beklenen davranış:**
1. Confound'lar yakalanır: farklı ürün, farklı yorum sayısı, fazladan indirim rozeti — üçü de `[Engelleyici]` olarak listelenir.
2. Her bulgu: tek cümle sorun + tek cümle düzeltme (ürünü eşitle, yorumu eşitle, indirim rozetini kaldır).
3. KPI sorulur veya plan paylaşıldıysa birincil/guardrail denetlenir.
4. Sonda net karar: "Bu haliyle koşulamaz; şu üç eşitleme yapılırsa koşulabilir."

**Düşme koşulları:**
- Confound'lardan herhangi birinin kaçırılması.
- "Genel olarak iyi görünüyor" tarzı kararsız kapanış.
- Var olmayan sorun uydurma (ör. fiyatlar zaten eşitken fiyat farkı bulgusu).
