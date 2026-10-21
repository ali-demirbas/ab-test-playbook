# Eval 10: İngilizce konuşma

Bu dosyadaki girdiler İngilizcedir; kural 7’yi (çıktı dili kullanıcının dilidir), kartın İngilizce çerçevesini ve kapsam dışı cümlesinin İngilizcesini sınar. Beklenen davranış diğer evallerle aynı kuralları izler, yalnızca dil değişir.

**Girdi A (suggest, İngilizce):** "I run a US fashion store. Give me test ideas for my cart page."

**Beklenen davranış:**
1. Bütün çıktı İngilizcedir: sohbetteki başlık, etiket satırı (“Priority: Medium · Source: from archive · Evidence: archive pattern”), “Why: …” satırı ve kart dosyası; listeden sonraki satırlar (“Before you start: …”, “Conditional (1): …”), kaydın metinleri ve kartın içeriği. Arşiv Türkçe yazılmıştır; senaryo metni İngilizceye çevrilir ve bağlama yerelleştirilir, Türkçe cümle kartta kalmaz.
2. Kart `lang: "en"` ile üretilir: başlık, mockup metinleri ve halka etiketleri İngilizcedir, taslak bandı “DRAFT · not reviewed”, koşullu kartın bandı “CONDITIONAL · to verify” der. Ayrıntı istenirse sohbette verilen üç kutunun başlıkları da İngilizcedir (“What to test”, “Primary KPIs to track”, “Never do”) ve birincil KPI “Primary” diye işaretlenir.
3. Pazar belli olduğu için (ABD) pazar sorusu sorulmaz; taksit gibi pazara bağlı bir senaryo ABD pazarına uymuyorsa önerilmez ya da bağımlılığı tek satırla yazılır (kural 11: dil pazarı göstermez, burada pazar ayrıca söylenmiştir).
4. Trafik, araç ve marka kılavuzu sorulmaz.

**Düşme koşulları:**
- Kartta ya da sohbette Türkçe kalan başlık, halka etiketi, kutu başlığı ya da senaryo cümlesi.
- Türkiye pazarına özgü bir varsayımın (taksit, kapıda ödeme) sorgulanmadan ABD mağazasına taşınması.

**Girdi B (sonuç sorusu, İngilizce):** "Control: 8,000 visitors, 400 orders. Variant: 8,000 visitors, 352 orders. It ran 3 weeks. Is it significant? Can we ship?"

**Beklenen davranış:**
1. Router tek satırlık İngilizce kapsam dışı cümlesini verir: "This playbook proposes, designs, audits and visualizes A/B tests. It doesn’t analyze results or compute sample size, duration, significance or a winner; use your testing tool’s own reporting for that."
2. Hiçbir sayı hesaplanmaz ya da yorumlanmaz: p-değeri, fark, yön veya “ship / don’t ship” kararı verilmez.
3. Kullanıcının bir test planı varsa planı denetleme teklifi turun tek sorusu olabilir.

**Düşme koşulları:**
- Verilen sayılardan herhangi bir istatistik, fark ya da kazanan yorumu üretilmesi.
- Cevabın Türkçe verilmesi.
