# Eval 01: suggest akışı

**Girdi A:** "Moda e-ticaret sitem var, sepet sayfam için test öner." (Trafik verilmemiş, sayfa paylaşılmamış: ekran görüntüsü, URL ya da sayfanın tarifi yok, yalnızca sayfa tipi var. Router tanımına göre bu “sayfa yok” durumudur ve `suggest` çalışır.)

**Beklenen davranış:**
1. Ön kapı: trafik, test aracı veya kurulum bilgisi **sorulmaz** (trafik: kural 5; araç/kurulum: senaryo üretimi için gerekli değildir, `ab-test-suggest` adım 1). Sayfa paylaşılmadığı için kural 13’ün problem sorusu da zorunlu değildir; senaryo doğrudan üretilir.
2. `cart-checkout.md` baştan sona okunmaz. Önce `grep -nE '^(## |Değişken:|Etiket:|EN:)'` ile başlıklar ve etiket satırları listelenir, yalnızca seçilen senaryo blokları `read_section.py --line … --lang tr` ile, İngilizce gövdeleri olmadan okunur. `durum=klasik` bir blok kullanıcı adını anmadıkça seçilmez; seçilen üç fikirden ikisi aynı öğe düzeyinde (`düzey`, ör. iki `metin`) olmaz; kaydın `priority.inputs.effort` değeri bloğun `emek` etiketinden gelir. Form tasarımına dair aday çıkarsa `forms-signup.md` için de aynı yol izlenir.
3. En fazla 3 **güçlü aday** gelir (mekanizma kapısını geçen ve önceliği en az Orta olan); adaylar önceliğe göre sıralanır, her birinin önceliği kayıtta tek cümleyle gerekçelendirilir. Aynı davranışsal mekanizmaya dayanan iki öneri gelmez. Sayıyı tamamlamak için zayıf aday eklenmez; tek güçlü senaryo da tam bir yanıttır (kural 9).
4. Sayfa paylaşılmadığı için her kaydın `problem` cümlesi sepet sayfası tipinde tipik olan engeli, kendi sayfada doğrulanacak bir varsayım olarak adlandırır. Sohbete bunun için ayrı satır yazılmaz; kartların temsili olduğu satırı yalnızca kullanıcı mockup’ı kendi sayfası sanabilecekse (sitesini ya da ürününü adlandırdıysa) yazılır.
5. Her senaryo kısa bir kayıttır ve doğrudan `ab-test-card` ile HTML kart olarak üretilir (“arşivden” ya da “arşivden uyarlandı” etiketiyle). Sohbette senaryo başına yalnızca başlık, tek etiket satırı, mekanizmayı sade sözlerle anlatan tek `Neden:` satırı (en fazla 140 karakter, sayı ya da artış iddiası yok), `Doğru olmalı:` ve `Önce yokla:` satırları (B’nin dayandığı inanç ve testten önce ucuz bir yoklama; örneklem ya da süre yok) ve kart dosyası kalır; KPI, guardrail, öncelik gerekçesi ya da üç kutu sohbete yazılmaz (kural 9).
6. Marka kılavuzu **sorulmaz**: nötr palet kullanılır; ne kartta ne sohbette marka ya da yeniden renklendirme notu vardır (kural 12).
7. Her kaydın birincil KPI’ı paydasıyla yazılır; guardrail “…memeli” kalıbındadır ve birincilin tümleyeni değildir. Kart bunları göstermez: yalnızca başlık, yan yana iki mockup, halka ve kısa etiketi vardır.
8. Örnekler moda bağlamına yerelleştirilmiş (kulaklık örneği geçmiyor).
9. `agents/mockup-reviewer` kart başına ayrı ayrı değil, turun bütün kartları için bir kez çalışır.
10. `agents/scenario-critic` çağrısına eksiksiz girdi verilir (senaryo kaydı: başlık, problem, mekanizma, değişken ve fark türü, varyantlar, birincil KPI, guardrail, kaynak ve kanıt etiketi, gerekçeli öncelik, varsa uyarılar; ayrıca itiraz, sayfa bağlamı, test hafızası, açıkça istenen testler ve planlanan sohbetin tamamı); `FIX: input missing` dönmez. Aynı ekrana düşen iki öneri varsa sohbet bunu bir kez, sıra satırıyla söyler (“Sıra: 1 → 2, aynı kullanıcılarda üst üste binmeden. 1 kazanırsa sıradaki …; kaybederse …”); bilgi başka satırda tekrarlanmaz. Eleştirmen tek tur çalışır: `[fixable]` satırlarını ana oturum olduğu gibi uygular ve damga geçerli kalır; eleştirmen yalnızca `[blocking]` bulgu için, en fazla iki kez yeniden çağrılır (kural 17).
11. Tur en fazla bir soru sorar, tek cümleyle: backlog teklifi ya da "N güçlü aday daha var" teklifi, ikisi birden değil ve iki soru tek cümlede birleştirilmez (kural 19).

**Düşme koşulları:**
- Ön kapıda trafik, test aracı, kurulum veya marka kılavuzu sorusu sorulması.
- Trafik verilmediği hâlde "2 haftada sonuç alırsın" tarzı süre/örneklem vaadi.
- Eksik bilginin çıktının önüne "önce şunu öğrenmem lazım" diye konması.
- On bilgiden biri eksik kayıt (ör. paydası olmayan birincil KPI, guardrail’siz ya da kanıt etiketsiz öneri).
- Kaydın içeriğinin (KPI, guardrail, öncelik gerekçesi) ya da istenmeden üç kutunun sohbete metin olarak yazılması; `Neden:` satırının 140 karakteri aşması ya da sayı veya artış iddiası taşıması (kural 9, 10).
- 3’ten fazla senaryonun sorulmadan üretilmesi ya da sayıyı doldurmak için zayıf aday eklenmesi (kural 9).
- Aynı turda birden fazla soru (kural 19).

**Girdi B (gönüllü verilen trafik):** "Sepet sayfam ayda ~40 bin ziyaretçi alıyor, dönüşüm %3. Test öner."

**Beklenen davranış:**
1. Senaryolar Girdi A’daki gibi gelir. Kullanıcı rakamları kendisi verdiği için `feasibility.py --rate 3% --visitors 40000 --per month` bir kez çalıştırılır ve iki satırı olduğu gibi yazılır (kaba aralık ve tek satırlık uyarı); el ile tahmin, örneklem ya da süre yazılmaz (kural 5).
2. Kullanıcı ayrıca süre sorarsa tek satırlık kapsam dışı cümlesi verilir: playbook örneklem, süre, anlamlılık veya kazanan hesaplamaz, bunun için test aracının kendi raporu kullanılır.

**Düşme koşulları:**
- Verilen sayılardan örneklem, süre ya da “kaç haftada sonuç alırsın” tahmini üretilmesi; fizibilitenin betik çalıştırılmadan el ile hesaplanması ya da sonuç sözü gibi yazılması.
- Trafik bilgisinin senaryoların önüne “önce bunu çözelim” diye konması.

**Girdi C (pazara bağlı aday, pazar bilinmiyor):** "Ödeme sayfamda taksit seçeneğini öne çıkaran testler öner." (Pazar belirtilmemiş, sayfa yok.)

**Beklenen davranış:**
1. Taksit senaryosu bekletilmez: kart üretilir ve kayıtta `market` türünde tek cümlelik bir uyarı bulunur (“Taksitin yaygın olduğu bir pazar varsayıldı.”).
2. Pazar sorusu turun **tek** sorusu olarak sorulur (kural 11, kural 19 önceliğiyle).

**Düşme koşulları:**
- Pazar cevabı gelene kadar hiçbir senaryonun üretilmemesi.
- Pazar uyarısının hiç yazılmaması.

**Girdi D (kısa kayıt):** “Ürün detay sayfam için test öner.” (Sayfa paylaşılmamış; `product-detail.md` içinde uyan çok sayıda senaryo var.)

**Beklenen davranış:**
1. Arşiv yalnızca `grep -nE '^(## |Değişken:|Etiket:|EN:)' <dosya>` ile listelenen başlıklar ve kısa listeye giren bloklar (başlık satırından sonraki `---` ayracına kadar, `python3 scripts/read_section.py <dosya> --line <başlık satırı> --lang tr` ile) üzerinden okunur; hiçbir aşama dosyası baştan sona, bütün dosyalar hiçbir zaman okunmaz. KPI adı `kpi-glossary.md` içinde `grep` ile aranır, sözlük bütün olarak okunmaz. `methodology.md` turun başında okunmaz; bir karar gerektirdiğinde (düzenleme, erişilebilirlik, hassas alan, etik) yalnızca ilgili bölüm okunur. Bunlar araç çağrıları kaydında görülür.
2. Tur en fazla 3 kayıt döndürür. Her kayıt `validate_scenario_json.py` ile hatasız geçer ve on bilgiyi taşır: soru biçiminde `title`, `problem`, tek cümlelik `mechanism`, `variable`, iki varyant ve `difference`, paydasıyla `primary_kpi`, `guardrail`, `source` (`adapted_from` ile) ve `evidence`, gerekçeli `priority`, yalnızca gerekiyorsa `warnings`. Kayıtta `detail` yoktur; üç kutu yeniden üretilmez.
3. Sohbet her senaryo için tam olarak altı satırdır; kart dosyası dışındakiler `validate_scenario_json.py --chat` çıktısından aynen kopyalanır (araç çağrıları kaydında görülür):
   ```
   **1. <başlık>**
   Öncelik: Orta (<puan>/9) · Kaynak: arşivden · Kanıt: arşiv örüntüsü
   Neden: <mekanizma, sade sözlerle, tek cümle>
   Doğru olmalı: <B’nin dayandığı inanç>
   Önce yokla: <ucuz yoklama>
   `<kart dosyası>`
   ```
   Senaryo başına başka metin yazılmaz: KPI, öncelik gerekçesi, eleme gerekçesi ya da denetçi raporu yok (kullanıcı isterse verilir). Kanıt etiketi kural 10’daki dört addan biridir (İngilizcede “industry observation”, asla “sector observation”). Listeden sonra `Başlamadan önce:` satırı (kapı yoksa “yok”) ve yalnızca geçerli olan satırlar gelir (ör. `Koşullu (<n>):`, sıra satırı), her biri tek satır ve her bilgi bir kez. Kayıtlar `new_record.py` iskeletinden başlar: ilk doğrulamada `⟦…⟧` ipucu kalmaz.
4. 3’ten fazla güçlü aday varsa sıralamada kalan en güçlü aday tek satırla adlandırılır (“Sıralamada kalan güçlü aday: <başlık>.”), kalanların sayısı söylenir ve devam teklifi turun tek sorusu olur (kural 19, tür 8). Daha yüksek türden bir soru varken de o satır yazılır.
5. Paydaş özeti yalnızca 1. senaryo içindir; ardından tek satır gelir: “2 ve 3 için karar özetini istersen yazarım.”

**Düşme koşulları:**
- Bir arşiv dosyasının baştan sona ya da bütün aşama dosyalarının okunması; sözlüğün bütün olarak okunması.
- 3’ten fazla kayıt ya da kullanıcı istemeden `detail` alanı dolu, üç kutusu yeniden yazılmış bir kayıt.
- Sohbette senaryo başına beş satırdan fazlası, `Doğru olmalı:` satırının eksik olması ya da örneklem, süre veya artış iddiası taşıması.
- Sıralamada kalan güçlü adayın hiç anılmaması; birden çok senaryo varken diğerlerinin özetinin istenebileceğini söyleyen satırın olmaması.
- Eleme gerekçelerinin ya da scenario-critic raporunun istenmeden sohbete dökülmesi.

**Girdi E (kendi fikirleri ve fazlası, doğrudan çağrı):** Kullanıcı `/ab-test-suggest` ile yazar: “Sepet sayfamızda kupon kutusu açık duruyor, ödeme butonu da ilk ekranda görünmüyor. Ekip önce butonu sabitlemeyi, sonra kuponu bağlantı arkasına almayı düşünüyor; bunları değerlendir, başka ne test edebiliriz?”

**Beklenen davranış:**
1. İstek `ab-test-design`’a aktarılmaz: doğrudan çağrı tarif edilen sayfayla `suggest`’te kalır; A tarif edilen mevcut hâldir (`is_current: true`, `card.mockup_basis: described`).
2. Sıra: önce kullanıcının açık istekleri, istendiği sırayla (buton sabitleme, sonra kupon), ardından playbook’un kendi adayları önceliğe göre. Başka aday eşiği geçmezse listeden sonra tek satır yazılır: “Bu sayfa için başka güçlü aday bulamadım.”
3. scenario-critic planlanan sohbetin tamamını alır (her senaryo bloğu ve listeden sonraki her satır); kaydı tekrar eden ya da `Neden:` satırı 140 karakteri aşan bir sohbet `FIX` alır.

**Düşme koşulları:**
- Açık isteklerin playbook’un adaylarının arkasına ya da istenenden farklı bir sıraya konması.
- Başka güçlü aday yokken bunun söylenmemesi ya da sayıyı doldurmak için zayıf aday eklenmesi.
- Sohbetin kaydın içeriğini (KPI, guardrail, öncelik gerekçesi) tekrar etmesi.
