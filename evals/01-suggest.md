# Eval 01 — suggest akışı

**Girdi:** "Moda e-ticaret sitem var, sepet sayfam için test öner." (Trafik verilmemiş.)

**Beklenen davranış:**
1. Ön kapı: trafik, test aracı veya kurulum bilgisi **sorulmaz** (trafik: kural 5; araç/kurulum: senaryo üretimi için gerekli değildir, `abtest-suggest` adım 1). Sayfa paylaşılmadığı için kural 13'ün problem sorusu da zorunlu değildir; senaryo doğrudan üretilir.
2. `knowledge/scenarios/cart-checkout.md` okunur; form tasarımına dair aday çıkarsa `forms-signup.md` de okunur.
3. 3-5 senaryo, ICE gerekçeli ve sıralı gelir; her biri üç kutu formatında, "arşivden" etiketiyle.
4. Her KPI listesinde ilk madde birincil diye işaretli, en az bir guardrail "…memeli" kalıbında.
5. Örnekler moda bağlamına yerelleştirilmiş (kulaklık örneği geçmiyor).

**Düşme koşulları:**
- Ön kapıda trafik, test aracı veya kurulum sorusu sorulması (trafik için kural 5 ihlali; araç/kurulum hiçbir akışta ön koşul değildir).
- Trafik verilmediği hâlde "2 haftada sonuç alırsın" tarzı süre/örneklem vaadi.
- Eksik bilginin çıktının önüne "önce şunu öğrenmem lazım" diye konması.
- Üç kutudan biri eksik senaryo.
- 5'ten fazla senaryonun tek seferde dökülmesi.
- Çoklu öneri listesi aşamasında kart üretilmesi (kural 9 istisnası).
