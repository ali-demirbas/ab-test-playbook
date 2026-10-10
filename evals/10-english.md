# Eval 10: İngilizce konuşma

Bu dosyadaki girdiler İngilizcedir; kural 7'yi (çıktı dili kullanıcının dilidir) ve script'in varsayılan `--lang en` yolunu sınar. Beklenen davranış diğer evallerle aynı kuralları izler, yalnızca dil değişir.

**Girdi A (suggest, İngilizce):** "I run a US fashion store. Give me test ideas for my cart page."

**Beklenen davranış:**
1. Bütün çıktı İngilizcedir: sohbet başlıkları, ICE gerekçesi, kanıt etiketi ("Evidence: archive precedent"), kaynak etiketi ("from archive") ve kartın içeriği. Arşiv Türkçe yazılmıştır; senaryo metni İngilizceye çevrilir ve bağlama yerelleştirilir, Türkçe cümle kartta kalmaz.
2. Kart `lang: "en"` ile üretilir; üç kutunun başlıkları İngilizcedir ("What to test", "Primary KPIs to track", "Never do") ve KPI kutusunda ilk madde birincil diye işaretlidir.
3. Pazar belli olduğu için (ABD) pazar sorusu sorulmaz; taksit gibi pazara bağlı bir senaryo ABD pazarına uymuyorsa önerilmez ya da bağımlılığı tek satırla yazılır (kural 11: dil pazarı göstermez, burada pazar ayrıca söylenmiştir).
4. Trafik, araç ve marka kılavuzu sorulmaz.

**Düşme koşulları:**
- Kartta ya da sohbette Türkçe kalan kutu başlığı, etiket ya da senaryo cümlesi.
- Türkiye pazarına özgü bir varsayımın (taksit, kapıda ödeme) sorgulanmadan ABD mağazasına taşınması.

**Girdi B (results, İngilizce):** "Control: 8,000 visitors, 400 orders. Variant: 8,000 visitors, 352 orders. It ran 3 weeks and hit the planned sample. Is it significant? Can we ship?"

**Beklenen davranış:**
1. Komutlar `--lang` verilmeden ya da `--lang en` ile çalışır; script'in notları ve uyarıları çevrilmeden aktarılabilir. `--lang tr` kullanılmaz.
2. Çıktı: `p_value` 0,07297, `decision_code: not_significant`, `effect_direction: variant_lower`, `relative_lift_pct` −12,0.
3. Skill İngilizce ve net bir cümle kurar: fark anlamlı değil, yön aşağı; “ship” denmez. Örneklem hedefi dolduğu ve süre iki haftayı geçtiği için karar “No significant difference”tır; varyantın daha düşük göründüğü ve kazanan olmadığı açıkça yazılır.
4. Mutlak fark (−0,6 yüzde puan) ve göreli fark (−%12) ayrı ayrı ve etiketli verilir.
5. Test-hafızası satırı teklif edilir; dosya zaten Türkçe değer kümesini kullanıyorsa değer o kümeden (`fark yok`) yazılır, yeni dosyada İngilizce küme kullanılır (dosya başına tek sözlük).

**Düşme koşulları:**
- Türkçe script çıktısının İngilizce konuşmaya aktarılması.
- Yönün söylenmemesi ya da sonucun “ship it” diye sunulması.
