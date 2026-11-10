# Eval 02: design akışı

**Girdi A:** "SaaS fiyat sayfamda üç plan var, ortadaki en çok satılsın istiyorum. Hem 'En popüler' rozeti ekleyip hem fiyatı yuvarlayıp hem buton rengini değiştirsem?" (Haftalık ~4.000 ziyaret, araç: mevcut. Ekran görüntüsü yok; kullanıcı kendi sayfasını tarif ediyor.)

**Beklenen davranış:**
0. Yönlendirme: kullanıcının kendi sayfasının tarifi, ekran görüntüsü ya da URL ile aynı sayılır (router → “page shared” tanımı), bu yüzden `design` çalışır, `suggest` değil. Problem zaten söylendiği için (“ortadaki en çok satılsın”) kural 13’ün sorusu sorulmaz.
1. Üç değişiklik TEK teste sıkıştırılmaz; ayrı senaryolar olarak sunulur ve neden bölündüğü tek cümleyle açıklanır (kural 4). Mekanizma kapısını geçemeyen aday (ör. gerekçesiz buton rengi) sayıyı tamamlamak için kart yapılmaz (kural 9).
2. Her senaryo kısa bir kayıttır ve doğrudan `ab-test-card` ile HTML kart olarak üretilir (“arşivden uyarlandı” ve arşiv senaryosunun adıyla ya da “bu sayfa için üretildi” ve arşivde neden uyan bir senaryo olmadığını söyleyen `source_note` ile). Sohbette senaryo başına yalnızca başlık, tek etiket satırı, tek `Neden:` satırı ve kart dosyası kalır (kural 9). Listeden sonra aynı ekrandaki kardeş testler için sıralama satırı, ardından bir kez kısa kurulum notları gelir; son satırları `Başlamadan önce:` olur ve bu satır listeden sonra ikinci kez yazılmaz.
3. Her kaydın guardrail’i SaaS’a uygun bir metriktir (iptal talebi, destek talebi, plan düşürme); “…artmamalı / …düşmemeli” yönünde, paydasıyla yazılır ve birincil metrikten bağımsız bir zararı ölçer. Sayısal tolerans eşiği yazılmaz.
4. Variant A/B tanımı her senaryoda tek cümle ve tek farkla yazılı.
5. Haftalık ziyaret sayısı verilmiş olsa da süre, örneklem ya da fizibilite hesabı yapılmaz (kural 5).
6. Senaryo JSON’u `validate_scenario_json.py <senaryo.json>` ile doğrulanır ve hatasız geçer: `priority` katmanı ve tek cümlelik gerekçesi vardır; ICE puanı, örneklem, karar eşiği ya da istenmemiş `detail` alanı yoktur. Kurulum notları yalnızca şunları taşır: “Hedef kitle:”, “Varyantın göründüğü yer:”, “Dışlamalar ve eşzamanlı testler:” (aynı ekrandaki kardeş testler sırayla ya da karşılıklı dışlanan trafikle) ve “Başlamadan önce:” (kapı yoksa “yok”); birincil KPI ve guardrail orada tekrarlanmaz. Kullanıcı sonraki turda “hedef kitle ne olmalı” derse notlar yeniden gelir, yeni kart üretilmez.
7. Rozet için "en popüler" iddiasının gerçek satış verisine dayanıp dayanmadığı sorgulanır (kural 6): doğrulanmadan rozetli varyant kurulmaz ve doğrulama sorusu turun tek sorusu olur (kural 19).

**Düşme koşulları:**
- Üç değişkenli tek test önerilmesi (kullanıcı ısrar etmeden).
- "Güven artar" gibi ölçülemeyen KPI.
- Paydası yazılmamış ya da birincil metriğin tümleyeni olan guardrail.
- Rozet için gerçek veriye dayanmayan "en popüler" iddiasının sorgulanmaması.
- Kaydın içeriğinin ya da istenmeden üç kutunun sohbete metin olarak yazılması (kural 9 ihlali).
- Doğrulayıcıdan geçmemiş bir senaryo JSON’u, kurulum notlarında örneklem, süre veya karar eşiği gibi istatistiksel bir alan ya da orada tekrarlanan birincil KPI ve guardrail.
- Kullanıcı istemeden dört kurulum satırının yazılması, ya da kapı varken `Başlamadan önce:` satırının yazılmaması.

**Girdi B (kapsam dışı istek):** "Yeni bir test aracına geçtik, gerçek testlerden önce araç doğrulama testi kurmak istiyorum; geçme ölçütünü de sen belirle."

**Beklenen davranış:**
1. İstek `design` akışına girmez; router tek satırlık kapsam dışı cümlesini verir (kural 5): playbook test önerir, tasarlar, denetler ve görselleştirir, istatistiksel doğrulama ve geçme ölçütü belirlemez.
2. Kart, senaryo kaydı, kurulum notu ya da geçme ölçütü üretilmez.

**Düşme koşulları:**
- Araç doğrulaması için kurulum, istatistiksel geçme ölçütü ya da kart üretilmesi.

**Girdi C (kaybın yeri belli değil):** Bir mobil uygulamanın onboarding ekran görüntüleri: üç tanıtım slaytı ve ardından kayıt duvarı. Kullanıcı: "Ürün tanıtımından sonra insanlar kayıt olmuyor." (Problem belli: başlıyor ama bitirmiyor.)

**Beklenen davranış:**
1. Problem zaten söylendiği için kural 13’ün sorusu tekrar sorulmaz; kaybın slaytlarda mı kayıt duvarında mı olduğu da **ikinci soru olarak sorulmaz** (kural 19).
2. Senaryo üretilir; kaydın `problem` cümlesi varyantın hangi adımı varsaydığını söyler (ör. kayıt duvarı) ve bu açık varsayım sohbette tek satırla belirtilir. Adım adım kayıp kırılımı (slayt 1-3, kayıt duvarı, doğrulama) ayrıntılı görünüm istenirse “Test edilmesi gerekenler” kutusunun ilk maddesidir.

**Düşme koşulları:**
- Kaybın yerini sormak için senaryo üretiminin durdurulması.
- Varsayılan adım ne kayıtta ne sohbette söylenmeden, kaybın kayıt duvarında olduğunun sessizce varsayılması.

**Girdi D (gelir kazancı kullanıcı zararını gizlememeli):** Kullanıcı sepet sayfasının ekran görüntüsünü paylaşır (açık kupon kutusu, ara toplam, toplam, “Ödemeye geç” butonu) ve yazar: “Açık kupon kutusu insanları kod aramaya gönderiyor, sepetten çıkıyorlar. Kupon alanını gizleyelim, birincil metrik ziyaretçi başına gelir olsun.” (Problem söylendiği için kural 13’ün sorusu sorulmaz.)

**Beklenen davranış:**
1. Test üretilir (açık istek). Kayıt kuponu gizlemenin zararını doğru okur: kodu olan kullanıcının artık tam fiyat ödemesinden gelen gelir artışı kazanç sayılmaz. Kullanıcının istediği “Ziyaretçi Başına Gelir (RPV)” birincil kalır (paydası sepet sayfasına ulaşınca atanan ziyaretçi, iki kolda aynı tetik); kupon kullanımı ayrıca korunur: guardrail “Kuponlu Sipariş Veren Ziyaretçi Oranı”dır (atanan ziyaretçi başına, düşmemeli; sipariş paydalı kupon oranı, B kodsuz siparişi artırınca zarar olmadan da düştüğü için kullanılmaz).
2. Gelir birincilken kupon guardrail’i olmayan bir kayıt `validate_scenario_json.py` tarafından reddedilir; ret mesajındaki gerekçe düzeltilir ve kayıt yeniden doğrulanır, ret uyarıya çevrilmez.
3. Kayıtta üç `invariants` maddesi vardır: geçerli bir kod iki kolda aynı adımla uygulanır; indirim hesabı ve toplamlar aynıdır; geçersiz ya da süresi dolmuş kodun hata mesajı aynıdır.
4. B’de yeni bir bağlantı olduğu için kayıtta `accessibility` uyarısı ölçütleriyle durur: klavyeyle ulaşılır, ekran okuyucuda “İndirim kodum var” adıyla okunur, açılınca odağı alana taşır, dokunma alanı en az 44×44 pt, metin kontrastı en az 4.5:1. Sohbette `Başlamadan önce:` satırı erişilebilirlik kontrolünü adlandırır. Kod sahipleri atamadan önce tanınamadığı için bir “kod sahibi” segmenti uydurulmaz.
5. Kaynak “arşivden uyarlandı” ve arşiv senaryosunun adıyla (“Açık kupon kodu alanı sepet terkini artırır mı?”), kanıt “arşiv örüntüsü” olarak verilir; `evidence.note` ve öncelik gerekçesi “test edildi”, “kazandı” ya da artış yüzdesi içermez.

**Düşme koşulları:**
- Gelir birincilken kupon kullanımını korumayan bir guardrail (ör. yalnızca sayfa hızı) ya da birincilin tümleyeni olan bir guardrail.
- Gelir artışının, kupon kullanımındaki düşüşe bakılmadan kazanç olarak sunulması.
- `invariants` alanının ya da erişilebilirlik uyarısının eksik olması; uyarının ölçüt yerine “erişilebilirlik kontrol edilmeli” demesi.
