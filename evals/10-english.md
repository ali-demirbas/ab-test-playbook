# Eval 10: İngilizce konuşma

Bu dosyadaki girdiler İngilizcedir; kural 7’yi (çıktı dili kullanıcının dilidir), kartın İngilizce çerçevesini ve kapsam dışı cümlesinin İngilizcesini sınar. Beklenen davranış diğer evallerle aynı kuralları izler, yalnızca dil değişir.

**Girdi A (suggest, İngilizce):** "I run a US fashion store. Give me test ideas for my cart page."

**Beklenen davranış:**
1. Bütün çıktı İngilizcedir: beklerken görünen ara satırlar (her biri en çok bir cümle, iç alan ya da adım adı yok), sohbetteki başlık, etiket satırı (“Priority: Medium (<score>/9) · Source: from archive · Evidence: archive pattern”; sektöre dayanan kanıt “industry observation”, asla “sector observation”), “Why: …”, “Must be true: …” ve “Probe first: …” satırları (`validate_scenario_json.py --chat` çıktısından aynen) ve kart dosyası; listeden sonraki satırlar (“Pre-start gates: …”, “Conditional (1): …”), kaydın metinleri ve kartın içeriği. Arşiv bloğunun İngilizce gövdesi varsa o okunur (`read_section.py --lang en`), yoksa İngilizce başlık ve Türkçe gövde okunup bağlama yerelleştirilir; Türkçe cümle kartta kalmaz.
2. Kart `lang: "en"` ile üretilir: başlık, mockup metinleri ve halka etiketleri İngilizcedir, taslak bandı “Preview · not visually checked”, koşullu kartın bandı “CONDITIONAL · needs verification” der. Ayrıntı istenirse sohbette verilen üç kutunun başlıkları da İngilizcedir (“What to test”, “Primary KPIs to track”, “Never do”) ve birincil KPI “Primary” diye işaretlenir.
3. Pazar belli olduğu için (ABD) pazar sorusu sorulmaz; taksit gibi pazara bağlı bir senaryo ABD pazarına uymuyorsa önerilmez ya da bağımlılığı tek satırla yazılır (kural 11: dil pazarı göstermez, burada pazar ayrıca söylenmiştir).
4. Trafik, araç ve marka kılavuzu sorulmaz.

**Düşme koşulları:**
- Kartta ya da sohbette Türkçe kalan başlık, halka etiketi, kutu başlığı ya da senaryo cümlesi.
- İngilizce çıktıda uzun tire (U+2014), ya da “variant_a”, “card.change”, “pipeline step 4” gibi iç adlar taşıyan ara satır (kural 7).
- Türkiye pazarına özgü bir varsayımın (taksit, kapıda ödeme) sorgulanmadan ABD mağazasına taşınması.

**Girdi B (sonuç sorusu, İngilizce):** "Control: 8,000 visitors, 400 orders. Variant: 8,000 visitors, 352 orders. It ran 3 weeks. Is it significant? Can we ship?"

**Beklenen davranış:**
1. Router tek satırlık İngilizce kapsam dışı cümlesini verir: "This playbook proposes, designs, audits and visualizes A/B tests. It doesn’t analyze results or compute sample size, duration, significance or a winner; use your testing tool’s own reporting for that."
2. Hiçbir sayı hesaplanmaz ya da yorumlanmaz: p-değeri, fark, yön veya “ship / don’t ship” kararı verilmez.
3. Kullanıcının bir test planı varsa planı denetleme teklifi turun tek sorusu olabilir.

**Düşme koşulları:**
- Verilen sayılardan herhangi bir istatistik, fark ya da kazanan yorumu üretilmesi.
- Cevabın Türkçe verilmesi.
