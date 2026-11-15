# Fiyatlandırma ve fiyat sunumu

Yolculuk aşaması: fiyatın görüldüğü an. Hem abonelik fiyat sayfası hem e-ticarette fiyat gösterimi bu dosyadadır. Ticari strateji kararları (plan varsayılanı, kurumsal fiyatın gizlenmesi, deneme süresi) `saas-b2b.md`, indirim, taksit ve fiyat küsuratı `product-detail.md` içindedir; burada fiyatın kendisinin nasıl çerçevelendiği ele alınır.

**Bu dosyadaki tüm senaryolarda birincil metrik gelir bazlıdır.** Fiyatı ucuz göstermek veya seçenek azaltmak dönüşüm oranını neredeyse her zaman artırır ama geliri düşürebilir; bu yüzden Ziyaretçi Başına Gelir (RPV) birincil, dönüşüm oranı ikincil metriktir (`knowledge/methodology.md` → Dönüşüm oranı geliri gizleyebilir). Her KPI listesinde en az bir madde bozulmaması gereken guardrail’dir.

---

## Gösterilen fiyat planı sayısını azaltmak geliri artırır mı?

Değişken: Gösterilen fiyat planı sayısı · Fark: kaldır

Etiket: id=pr-001 · mercek=Fiyat · düzey=fiyat · sektör=saas · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing fewer pricing plans raise revenue?

EN-Variable: Number of pricing plans shown

Çok sayıda plan farklı ihtiyaçları karşılar ama seçim felcine yol açabilir ve ziyaretçiyi hiçbirini seçmemeye itebilir. Mevcut çok planlı sayfadan (A) en az seçilen planı kaldırmak (B) kararı hızlandırır ve karşılaştırma yükünü azaltır. Plan sayısını değiştirmek aynı zamanda hangi planın ortada kaldığını da değiştirir; bu, seçim dağılımını fiyattan bağımsız olarak kaydırır.

**Test edilmesi gerekenler**
- Sayı: Plan sayısını azaltmak toplam geliri artırıyor mu?
- Dağılım: Hangi plan ne oranda seçiliyor, ortadaki plan avantaj sağlıyor mu?
- Kaybedilen ihtiyaç: Kaldırılan planı seçenler başka plana mı geçiyor, yoksa kayboluyor mu?
- Aşağı kayma: Az seçenek ziyaretçiyi daha ucuz plana mı yönlendiriyor?
- Segment: Bireysel ve kurumsal ziyaretçi farklı sayıda seçeneğe mi ihtiyaç duyuyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Plan sayısı geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Dağılımı: Herhangi bir planı seçen ziyaretçi oranı artıyor mu?
- İptal veya Plan Düşürme Oranı (30 gün): Yanlış plana yönlenen kullanıcı sonradan düşmemeli.
- Destek Talebi: “Hangi planı almalıyım” soruları artmamalı.

**Yapılmaması gerekenler**
- Aynı testte plan sayısı ile plan fiyatlarını birlikte değiştirmeyin.
- Kaldırdığınız planı fiyat sayfasından çıkarıp ödeme adımında veya doğrudan bağlantıyla satılabilir bırakmayın; kol kirlenir.
- Kaldırdığınız planın mevcut abonelerini test kapsamına almayın.
- Plan sayısını değiştirirken plan içeriklerini de yeniden paketlemeyin.
- Seçenek azaltmayı, aslında satmak istediğiniz planı tek çıkış yolu hâline getirmek için kullanmayın.

### EN

Many plans cover different needs but can cause choice paralysis and push the visitor to choose none. Variant B removes the least chosen plan from the current multi-plan page (A), which speeds up the decision and lightens the comparison load. Changing the number of plans also changes which plan sits in the middle, and that shifts the choice distribution independently of price.

**What to test**
- Count: Does reducing the number of plans raise total revenue?
- Distribution: Which plan is chosen at what rate, and does the middle plan gain an advantage?
- Lost need: Do people who would have chosen the removed plan move to another plan, or disappear?
- Downward drift: Do fewer options steer the visitor to a cheaper plan?
- Segment: Do individual and business visitors need a different number of options?

**KPIs to track**
- Revenue per Visitor (RPV): Does the plan count raise revenue?
- Average Plan Value: The average amount of the chosen plan must not drop.
- Plan Mix: Does the share of visitors who choose any plan rise?
- Cancellation or Downgrade Rate (30 days): A user steered to the wrong plan must not downgrade later.
- Support Contact Rate: “Which plan should I buy” questions must not rise.

**What not to do**
- Don’t change the number of plans and the plan prices together in the same test.
- Don’t remove a plan from the pricing page and leave it purchasable at the payment step or through a direct link; the arm gets contaminated.
- Don’t include the existing subscribers of the removed plan in the test scope.
- Don’t repackage the plan contents while changing the number of plans.
- Don’t use the reduction of options to make the plan you actually want to sell the only way out.

---

## Planları karşılaştırma tablosunda mı, ayrı kartlarda mı sunmalı?

Değişken: Plan sunum biçimi · Fark: değiştir

Etiket: id=pr-002 · mercek=Netlik · düzey=görsel · sektör=saas · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should plans be shown in a comparison table or on separate cards?

EN-Variable: Plan presentation format

Karşılaştırma tablosu farkları satır satır görünür kılar ve ayrıntılı değerlendirme yapan ziyaretçiye hitap eder. Ayrı kartlar her planı kendi başına bir teklif gibi sunar, hızlı karar verdirir ama farkları gizler. Tablo aynı zamanda ucuz planda eksik olan her şeyi de görünür kılar; bu hem ikna edici hem caydırıcı olabilir.

**Test edilmesi gerekenler**
- Biçim: Tablo mu, kart mı daha yüksek gelir getiriyor?
- Sonraki test: Tablo kazanırsa karşılaştırma satırlarının sayısı ayrı bir testte azaltıldığında plan seçimi artıyor mu?
- Eksiklik vurgusu: Ucuz planda eksik olanları göstermek yukarı mı itiyor, caydırıyor mu?
- Plan dağılımı: Kart biçimi ziyaretçiyi ilk karta mı yığıyor, tablo seçimi daha pahalı planlara mı yayıyor?
- Cihaz: Mobilde tablo yatay kaydırmaya düşüyor mu, kart daha mı iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sunum biçimi geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Dağılımı: Karar veren ziyaretçi oranı artıyor mu?
- Karşılaştırma Etkileşim Oranı: Tablo gerçekten inceleniyor mu?
- Sayfada Kalma Süresi: Karar süresi kabul edilemez ölçüde uzamamalı.

**Yapılmaması gerekenler**
- Aynı testte sunum biçimi ile karşılaştırılan özellik listesini birlikte değiştirmeyin.
- Tabloda ucuz planın eksiklerini abartılı işaretlerle vurgulayıp korku yaratmayın.
- Mobilde tabloyu okunmaz derecede küçültüp kartla karşılaştırmayın.
- Özellik adlarını tabloda ve kartta farklı yazmayın; karşılaştırma bozulur.
- Tabloda gerçekte sunulmayan bir özelliği yer tutucu olarak bırakmayın.

### EN

A comparison table makes differences visible row by row and suits the visitor who evaluates in detail. Separate cards present each plan as an offer in its own right; they get a quick decision but hide differences. A table also makes everything missing from the cheap plan visible, which can be both persuasive and discouraging.

**What to test**
- Format: Does a table or cards bring higher revenue?
- Next test: If the table wins, does cutting the number of comparison rows in a separate test raise plan selection?
- Emphasis on gaps: Does showing what the cheap plan lacks push people up, or put them off?
- Plan distribution: Does the card format pile visitors onto the first card, and does the table spread choices to the more expensive plans?
- Device: On mobile, does the table fall back to horizontal scrolling, and do cards work better?

**KPIs to track**
- Revenue per Visitor (RPV): Does the presentation format raise revenue?
- Average Plan Value: The average amount of the chosen plan must not drop.
- Plan Mix: Does the share of visitors who decide rise?
- Comparison Engagement Rate: Is the table actually examined?
- Time on Page: Decision time must not lengthen to an unacceptable degree.

**What not to do**
- Don’t change the presentation format and the compared feature list together in the same test.
- Don’t highlight the cheap plan’s gaps in the table with exaggerated markers and create fear.
- Don’t shrink the table on mobile until it is unreadable and then compare it with cards.
- Don’t write feature names differently in the table and on the cards; the comparison breaks.
- Don’t leave a feature that is not really offered as a placeholder in the table.

---

## Fiyatı öne çıkarmak mı, faydadan sonra göstermek mi daha iyi çalışıyor?

Değişken: Fiyatın sayfadaki sırası · Fark: taşı

Etiket: id=pr-003 · mercek=Fiyat · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Lead with the price or show it after the benefits: which works better?

EN-Variable: Position of the price on the page

Fiyatı erken göstermek beklentiyi netleştirir ve bütçesi uymayan ziyaretçinin vaktini almaz. Faydayı önce anlatmak, fiyat görüldüğünde algılanan değeri yükseltir. Erken fiyat pahalı algılanan üründe kayıp yaratabilir; geç fiyat ise güvensizlik ve “fiyatı gizliyorlar” hissi doğurabilir.

**Test edilmesi gerekenler**
- Sıra: Fiyat faydadan önce mi, sonra mı gösterilmeli?
- Nitelik: Erken fiyat gelen talebin niteliğini yükseltiyor mu?
- Güven: Fiyatı geciktirmek gizleme algısı yaratıyor mu?
- Segment: Fiyata duyarlı ve değere duyarlı ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sıralama geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Ortalama tutar düşmemeli.
- Dönüşüm Oranı (CR): Satın alan ziyaretçi oranı ne yönde değişiyor?
- Hemen Çıkma Oranı: Erken fiyat çıkışı kabul edilemez ölçüde artırmamalı.
- Talep Başına Nitelik Oranı: Geç fiyat, ödeme gücü olmayan talebi çoğaltmamalı.

**Yapılmaması gerekenler**
- Fiyatı geciktirmeyi, kullanıcı taahhüde girene kadar saklamak için kullanmayın.
- Aynı testte fiyat konumu ile fiyat rakamını birlikte değiştirmeyin.
- Toplam fiyatın bir kısmını (kargo, vergi, kurulum) sonraya bırakıp “fiyat öne alındı” demeyin.
- Yasal olarak fiyatın belirli bir aşamada gösterilmesi gereken pazarlarda kuralı doğrulamadan sıralama değiştirmeyin.
- Fiyat büyütülürken para birimi veya vergi ifadesini küçültmeyin.

### EN

Showing the price early clarifies expectations and doesn’t waste the time of a visitor whose budget doesn’t fit. Explaining the benefit first raises perceived value once the price is seen. An early price can cause losses on a product perceived as expensive; a late price can create distrust and a “they’re hiding the price” feeling.

**What to test**
- Order: Should the price be shown before or after the benefit?
- Quality: Does an early price raise the quality of incoming leads?
- Trust: Does delaying the price create a perception of concealment?
- Segment: Do price-sensitive and value-sensitive visitors react differently?

**KPIs to track**
- Revenue per Visitor (RPV): Does the ordering raise revenue?
- Average Order Value (AOV): The average amount must not drop.
- Conversion Rate (CR): In which direction does the share of purchasing visitors move?
- Bounce Rate: An early price must not raise exits to an unacceptable degree.
- Qualification Rate per Lead: A late price must not multiply leads who can’t afford it.

**What not to do**
- Don’t use delaying the price to hide it until the user is committed.
- Don’t change the price position and the price figure together in the same test.
- Don’t leave part of the total price (shipping, tax, setup) for later and call it “price moved forward”.
- In markets where the law requires the price to be shown at a certain stage, don’t change the order without verifying the rule.
- Don’t shrink the currency or the tax wording while enlarging the price.

---

## Abonelik fiyatını aylık birime bölerek göstermek işe yarar mı?

Değişken: Abonelik fiyatının gösterim birimi · Fark: değiştir

Etiket: id=pr-004 · mercek=Fiyat · düzey=bilgi · sektör=saas · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does showing a subscription price as a monthly amount pay off?

EN-Variable: Display unit of the subscription price

Yıllık bir tutarı aylık karşılığıyla göstermek rakamı küçültür ve giriş engelini düşürür. Buna karşılık toplam taahhüdü belirsizleştirir, kullanıcı ödeme anında beklemediği bir tutarla karşılaşabilir ve bu iptal ile itiraza dönüşebilir. Belirleyici olan, toplam tutarın aynı ekranda ne kadar net durduğudur.

**Test edilmesi gerekenler**
- Çerçeve: Aylık birim gösterimi geliri artırıyor mu?
- Sonraki test: Aylık çerçeve sabitken yıllık toplamın punto büyüklüğü ayrı bir testte ilk dönem iptalini azaltıyor mu?
- Beklenti: Ödeme adımında sürpriz tutar itirazı artıyor mu?
- Ayrıntı düzeyi: Aylık yerine daha küçük birime bölmek inandırıcılığı düşürüyor mu?
- Segment: Bireysel ve kurumsal alıcı aynı çerçeveye mi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çerçeveleme geliri artırıyor mu?
- İlk Dönem İptal Oranı (ilk ödemeden sonra 30 gün): Beklenti uyumsuzluğundan doğan iptal artmamalı.
- Ödeme Adımı Terk Oranı: Toplam tutarı görünce bırakma artmamalı.
- Yıllık Plan Seçim Oranı: Uzun taahhüde geçiş artıyor mu?
- İade veya İtiraz Oranı (30 gün): Tutar şaşkınlığı kaynaklı talepler artmamalı.

**Yapılmaması gerekenler**
- Toplam tutarı okunmaz derecede küçük yazıp aylık rakamı tek görünen fiyat hâline getirmeyin.
- Aylık gösterip aylık ödeme seçeneği sunmuyorsanız bunu belirtmeden bırakmayın.
- Aynı testte çerçeveleme ile fiyat seviyesini birlikte değiştirmeyin.
- Fiyat gösterimi yasal olarak düzenlenen pazarlarda kuralı doğrulamadan çerçeve değiştirmeyin.
- Aylık birime bölünen tutarı aşağı yuvarlayıp on iki katı gerçek yıllık tutardan düşük çıkan bir rakam göstermeyin.

### EN

Showing an annual amount as its monthly equivalent makes the figure smaller and lowers the barrier to entry. On the other hand it blurs the total commitment; the user may meet an amount they didn’t expect at payment, and that can turn into cancellation and dispute. What decides it is how clearly the total amount stands on the same screen.

**What to test**
- Framing: Does the monthly-unit display raise revenue?
- Next test: With the monthly framing fixed, does the font size of the annual total reduce first-period cancellation in a separate test?
- Expectation: Do surprise-amount objections rise at the payment step?
- Granularity: Does splitting into a unit smaller than monthly reduce credibility?
- Segment: Do individual and business buyers respond to the same framing?

**KPIs to track**
- Revenue per Visitor (RPV): Does the framing raise revenue?
- First-Period Cancellation Rate (30 days after first payment): Cancellations caused by an expectation mismatch must not rise.
- Payment Step Abandonment Rate: Leaving must not rise when the total amount is seen.
- Annual Plan Selection Rate: Does the move to the longer commitment rise?
- Return or Dispute Rate (30 days): Requests caused by amount surprise must not rise.

**What not to do**
- Don’t write the total amount so small it is unreadable and make the monthly figure the only visible price.
- Don’t show a monthly figure without saying so when you don’t offer a monthly payment option.
- Don’t change the framing and the price level together in the same test.
- In markets where price display is regulated, don’t change the framing without verifying the rule.
- Don’t round the amount divided into the monthly unit down so that twelve times the figure comes out lower than the real annual amount.

---

## Birim fiyat göstermek karşılaştırmayı kolaylaştırıp geliri artırır mı?

Değişken: Paket kartındaki birim fiyat · Fark: ekle

Etiket: id=pr-005 · mercek=Fiyat · düzey=bilgi · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does showing a unit price make comparison easier and raise revenue?

EN-Variable: Unit price on the package card

Birim başına fiyat (kilogram, adet, kullanıcı, ay) farklı boyuttaki paketleri karşılaştırılabilir kılar ve büyük paketin avantajını görünür yapar. Riski: birim fiyat küçük paketi pahalı gösterir ve ziyaretçiyi bütçesini aşan bir pakete iter; ayrıca fiyat alanını kalabalıklaştırıp asıl tutarın okunmasını zorlaştırabilir.

**Test edilmesi gerekenler**
- Varlık: Birim fiyat göstermek geliri artırıyor mu?
- Yönlenme: Ziyaretçi daha büyük pakete mi kayıyor?
- Okunabilirlik: İki fiyatın yan yana durması asıl tutarı gölgeliyor mu?
- Sonraki test: Birim fiyat kazanırsa farklı birimler (adet / ağırlık / kullanıcı) ayrı bir testte denendiğinde hangisi paket seçimini daha çok kolaylaştırıyor?
- Cihaz: Mobilde birim fiyat satırı asıl fiyatın altına kaydığında etkisi değişiyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Birim fiyat geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Büyük pakete kayma tutarı artırıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı düşmemeli.
- İade veya İptal Oranı (30 gün): Bütçesini aşan alım sonradan geri dönmemeli.
- Fiyat Alanı Etkileşimi: Asıl fiyatın okunması zorlaşmamalı.

**Yapılmaması gerekenler**
- Birim fiyatı asıl fiyattan daha büyük puntoyla göstermeyin.
- Birim hesabını yuvarlayarak gerçek orandan sapan bir rakam üretmeyin.
- Aynı testte birim fiyat ile paket boyutlarını birlikte değiştirmeyin.
- Farklı ürünlerde farklı birim kullanıp karşılaştırmayı bozmayın.
- Birim fiyatın zorunlu olduğu pazarlarda bunu bir test değişkeni gibi ele almayın; orada zorunluluktur.

### EN

A price per unit (kilogram, piece, user, month) makes packages of different sizes comparable and shows the advantage of the larger package. Risk: the unit price makes the small package look expensive and pushes the visitor to a package beyond their budget; it can also crowd the price area and make the main amount harder to read.

**What to test**
- Presence: Does showing a unit price raise revenue?
- Steering: Does the visitor slide toward the larger package?
- Legibility: Does having two prices side by side overshadow the main amount?
- Next test: If the unit price wins, which unit (piece / weight / user) makes package choice easier when tried in a separate test?
- Device: Does the effect change when the unit price line slips below the main price on mobile?

**KPIs to track**
- Revenue per Visitor (RPV): Does the unit price raise revenue?
- Average Order Value (AOV): Does the slide to the larger package raise the amount?
- Conversion Rate (CR): The purchase rate must not drop.
- Return or Cancellation Rate (30 days): A purchase beyond the buyer’s budget must not come back later.
- Price Area Engagement: Reading the main price must not get harder.

**What not to do**
- Don’t show the unit price in a larger font than the main price.
- Don’t round the unit calculation into a figure that departs from the real ratio.
- Don’t change the unit price and the package sizes together in the same test.
- Don’t use different units for different products and break the comparison.
- In markets where unit price is mandatory, don’t treat it as a test variable; there it is an obligation.

---

## Ödemenin tek seferlik olduğunu açıkça yazmak dönüşümü artırır mı?

Değişken: Tek seferlik ödeme ifadesi · Fark: ekle

Etiket: id=pr-006 · mercek=Güven · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does stating clearly that the payment is one-off raise conversion?

EN-Variable: One-off payment wording

Abonelik yorgunluğu yaşayan kullanıcı, her ödemenin tekrarlayacağını varsayabilir. “Tek seferlik ödeme, otomatik yenileme yok” gibi bir ifade bu tereddüdü kaldırabilir. Karşı tarafta: bu ifade abonelik seçeneğini de akla getirip karşılaştırma yükü yaratabilir, ya da tekrar satın alma ihtimalini zayıflatabilir.

**Test edilmesi gerekenler**
- İfade: Tek seferlik olduğunu belirtmek geliri artırıyor mu?
- Karşılaştırma yükü: Abonelik seçeneği de sunulan sayfada ifade, ziyaretçiyi iki ödeme modeli arasında kararsız bırakıp karar süresini uzatıyor mu?
- Yan etki: İfade tekrar satın alma veya abonelik geçişini azaltıyor mu?
- Segment: Yeni ziyaretçi ile daha önce satın almış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İfade geliri artırıyor mu?
- Ödeme Tamamlama Oranı: Ödemeyi bitiren oranı artıyor mu?
- Tekrar Satın Alma Oranı (60 gün): İleriki dönemde tekrar alım düşmemeli.
- Abonelik Geçiş Oranı: Abonelik satıyorsanız bu oran kabul edilemez ölçüde düşmemeli.
- İade veya İtiraz Oranı (30 gün): Beklenti kaynaklı itirazlar azalıyor mu?

**Yapılmaması gerekenler**
- Gerçekte tekrarlayan bir ödeme varken tek seferlik ifadesi kullanmayın.
- Aynı testte ifade ile fiyatı birlikte değiştirmeyin.
- İfadeyi ödeme koşullarının yerine geçirmeyin; koşul metni ayrıca bulunmalıdır.
- “Otomatik yenileme yok” ifadesini, aynı sayfada önceden işaretli gelen bir abonelik veya ek hizmet kutusuyla birlikte göstermeyin.
- Abonelik iptali kurallarının düzenlendiği pazarlarda ifadeyi hukuki kontrol olmadan yayınlamayın.

### EN

A user with subscription fatigue may assume every payment will repeat. A phrase such as “One-time payment, no auto-renewal” can remove that hesitation. On the other side: the phrase can also bring the subscription option to mind and create a comparison load, or weaken the chance of a repeat purchase.

**What to test**
- Wording: Does stating that it is one-off raise revenue?
- Comparison load: On a page that also offers a subscription option, does the phrase leave the visitor undecided between two payment models and lengthen the decision?
- Side effect: Does the phrase reduce repeat purchases or the switch to a subscription?
- Segment: Do new visitors and users who have bought before react differently?

**KPIs to track**
- Revenue per Visitor (RPV): Does the wording raise revenue?
- Payment Completion Rate: Does the share who finish payment rise?
- Repeat Purchase Rate (60 days): Repeat purchases later on must not drop.
- Subscription Switch Rate: If you sell a subscription, this rate must not drop to an unacceptable degree.
- Return or Dispute Rate (30 days): Do expectation-driven objections decrease?

**What not to do**
- Don’t use the one-off wording when the payment actually recurs.
- Don’t change the wording and the price together in the same test.
- Don’t let the wording stand in for the payment terms; the terms text must exist separately.
- Don’t show the “No auto-renewal” wording alongside a subscription or add-on box that comes pre-ticked on the same page.
- In markets where subscription cancellation rules are regulated, don’t publish the wording without a legal check.

---

## Fiyatı vergi dahil mi, hariç mi göstermeli?

Değişken: Fiyatta verginin gösterim şekli · Fark: değiştir

Etiket: id=pr-007 · mercek=Fiyat · düzey=bilgi · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should prices be shown with tax included or excluded?

EN-Variable: How tax is shown in the price

Vergi hariç fiyat rakamı küçük gösterir ve kurumsal alıcının zaten hariç düşündüğü pazarlarda doğaldır. Vergi dahil fiyat ise ödenecek gerçek tutarı verir ve ödeme adımında sürpriz yaşatmaz. Bu tercih büyük ölçüde pazara ve alıcı tipine bağlıdır; birçok pazarda ise tüketiciye dahil fiyat göstermek zorunludur.

**Test edilmesi gerekenler**
- Gösterim: Vergi dahil fiyat toplam geliri nasıl etkiliyor?
- Sürpriz: Ödeme adımında tutar artışı terk yaratıyor mu?
- İkili gösterim: Hem dahil hem hariç göstermek karışıklık mı yaratıyor, netlik mi?
- Alıcı tipi: Kurumsal alıcı hariç fiyatı mı bekliyor?
- Segment: Farklı pazarlardaki ziyaretçilere farklı gösterim mi gerekiyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Gösterim geliri artırıyor mu?
- Ödeme Adımı Terk Oranı: Tutar artışı kaynaklı bırakma artmamalı.
- Dönüşüm Oranı (CR): Satın alma oranı ne yönde değişiyor?
- Fiyat Kaynaklı Destek Talebi: “Neden farklı tutar çıktı” soruları artmamalı.
- İade veya İtiraz Oranı (30 gün): Tutar şaşkınlığı kaynaklı itirazlar artmamalı.

**Yapılmaması gerekenler**
- Tüketiciye vergi dahil gösterimin zorunlu olduğu pazarlarda bunu test değişkeni yapmayın; orada seçim yoktur.
- Hedef pazarın kuralını doğrulamadan varyant kurmayın.
- Vergi hariç gösterip bunu belirten ifadeyi okunmaz küçüklükte yazmayın.
- Aynı testte vergi gösterimi ile kargo ücreti gösterimini birlikte değiştirmeyin.
- Tek pazarda ölçüp sonucu diğer pazarlara taşımayın.

### EN

A price excluding tax makes the figure look smaller and is natural in markets where the business buyer already thinks in net terms. A price including tax gives the real amount to be paid and holds no surprise at the payment step. This choice depends largely on the market and the buyer type; in many markets showing consumers the tax-inclusive price is mandatory.

**What to test**
- Display: How does the tax-inclusive price affect total revenue?
- Surprise: Does the amount increase at the payment step cause abandonment?
- Dual display: Does showing both inclusive and exclusive create confusion or clarity?
- Buyer type: Does the business buyer expect the exclusive price?
- Segment: Do visitors in different markets need a different display?

**KPIs to track**
- Revenue per Visitor (RPV): Does the display raise revenue?
- Payment Step Abandonment Rate: Leaving caused by the amount increase must not rise.
- Conversion Rate (CR): In which direction does the purchase rate move?
- Price-Related Support Contact Rate: “Why did a different amount come up” questions must not rise.
- Return or Dispute Rate (30 days): Objections caused by amount surprise must not rise.

**What not to do**
- In markets where showing consumers the tax-inclusive price is mandatory, don’t make it a test variable; there is no choice there.
- Don’t set up a variant without verifying the rule of the target market.
- Don’t write the wording that says the price is tax-exclusive in unreadably small type.
- Don’t change the tax display and the shipping fee display together in the same test.
- Don’t measure in one market and carry the result to other markets.

---

## Pakete dahil olanların parasal değerini göstermek algılanan değeri artırır mı?

Değişken: Paket içeriğinin parasal değer gösterimi · Fark: ekle

Etiket: id=pr-008 · mercek=Fiyat · düzey=bilgi · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does showing the money value of what the package includes raise perceived value?

EN-Variable: Money value of the package contents

Fiyatın yanında “içindekilerin toplam değeri” göstermek alınan şeyin büyüklüğünü somutlaştırır. Riski: karşılaştırma değeri gerçekçi değilse güven kaybı yaratır, ayrıca şişirilmiş referans değer bazı pazarlarda yanıltıcı fiyat gösterimi sayılır. Değer iddiası doğrulanabilir olmalıdır.

**Test edilmesi gerekenler**
- Varlık: Dahil olanların değerini göstermek geliri artırıyor mu?
- İnandırıcılık: Belirtilen değer gerçekçi bulunuyor mu?
- Sonraki test: Değer gösterimi kazanırsa toplam tutar ile kalem kalem döküm ayrı bir testte karşılaştırıldığında hangisi daha inandırıcı bulunuyor?
- Oran: Değer ile fiyat arasındaki fark büyüdükçe güven düşüyor mu?
- Segment: Farklı kullanıcı tipleri değer iddiasına farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Değer gösterimi geliri artırıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı artıyor mu?
- İade Oranı (30 gün): Abartılı değer algısı sonradan hayal kırıklığı yaratmamalı.
- Ortalama Sepet Tutarı (AOV): Ortalama tutar düşmemeli.
- Güven Kaynaklı Destek Talebi: Değer iddiasını sorgulayan talepler artmamalı.

**Yapılmaması gerekenler**
- Ayrı satılmayan bir kalemin “ayrı fiyatı” varmış gibi bir değer üretmeyin.
- Doğrulanamayan bir referans değeri fiyatın yanına yazmayın.
- Aynı testte değer gösterimi ile paket içeriğini birlikte değiştirmeyin.
- Referans fiyat gösteriminin düzenlendiği pazarlarda kuralı doğrulamadan yayınlamayın.
- Değer toplamına, kullanıcının zaten ücretsiz aldığı kalemleri (ör. standart kargo) parasal değer biçip eklemeyin.

### EN

Showing “the total value of what’s included” next to the price makes the size of what is received concrete. Risk: if the comparison value is unrealistic it loses trust, and an inflated reference value counts as misleading price display in some markets. The value claim must be verifiable.

**What to test**
- Presence: Does showing the value of what is included raise revenue?
- Credibility: Is the stated value found realistic?
- Next test: If the value display wins, which is found more credible when a single total and an itemized breakdown are compared in a separate test?
- Ratio: Does trust fall as the gap between the value and the price grows?
- Segment: Do different user types react differently to the value claim?

**KPIs to track**
- Revenue per Visitor (RPV): Does the value display raise revenue?
- Conversion Rate (CR): Does the purchase rate rise?
- Return Rate (30 days): An exaggerated sense of value must not create disappointment later.
- Average Order Value (AOV): The average amount must not drop.
- Trust-Related Support Contact Rate: Requests that question the value claim must not rise.

**What not to do**
- Don’t invent a value as if an item that is not sold separately had a “separate price”.
- Don’t put an unverifiable reference value next to the price.
- Don’t change the value display and the package contents together in the same test.
- In markets where reference price display is regulated, don’t publish without verifying the rule.
- Don’t add to the value total items the user already gets free (e.g. standard shipping) by putting a money value on them.

---

## Üçüncü bir çekici-alternatif plan eklemek orta planın seçilme oranını artırıyor mu?

Değişken: Çekici-alternatif üçüncü plan · Fark: ekle

Etiket: id=pr-009 · mercek=Fiyat · düzey=fiyat · sektör=saas · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does adding a decoy third plan raise the share choosing the middle plan?

EN-Variable: Decoy third plan

İki plan arasında seçim yapmak zordur çünkü karşılaştırılacak ortak bir ölçüt yoktur. Orta plana yakın fiyatlı ama daha az içerikli üçüncü bir plan eklemek, orta planı “açık ara daha iyi seçenek” gibi gösterebilir; üçüncü planın kendisi neredeyse hiç seçilmez, işlevi karşılaştırma çıpası olmaktır. Bu, yeni bir avantaj eklemez; var olan iki planın algısını üçüncüsüne göre değiştirir.

**Test edilmesi gerekenler**
- Fiyat farkı: Çekici-alternatif ile orta plan arasındaki fark küçüldükçe etki güçleniyor mu?
- Gerçek talep: Çekici-alternatif planın kendisi ciddi bir oranda seçiliyor mu, yoksa beklendiği gibi arka planda mı kalıyor?
- Algı: Üç seçenek göstermek genel fiyat algısını pahalı mı gösteriyor?
- Segment: Kurumsal ve bireysel alıcı üç seçenekli yapıya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çekici-alternatif eklemek geliri artırıyor mu?
- Orta Plan Seçim Oranı: Orta planı seçen ziyaretçi oranı yükseliyor mu?
- Çekici-Alternatif Seçilme Oranı: Bu planın kendisi ciddi talep almamalı; aldıysa yapı yanlış kurulmuş demektir.
- En Pahalı Plan Satışı: Gerçek en pahalı planın satışı düşmemeli.
- Destek Talebi: “Hangi planı seçmeliyim” soruları artmamalı.

**Yapılmaması gerekenler**
- Çekici-alternatif planı satın alınamaz hâle getirmeyin veya içeriğini gerçek dışı bırakmayın; gerçek, kullanılabilir bir plan olmalı, yalnızca konumlandırması zayıf kurulur.
- Aynı testte üçüncü planı eklerken orta planın fiyatını da değiştirmeyin; seçim artışı çıpadan mı, yeni fiyattan mı geldi ayrılamaz.
- Çekici-alternatif planı gerçek maliyetinin altında fiyatlandırıp asıl planları yapay biçimde pahalı göstermeyin.
- Orta planın içeriğini test sırasında zenginleştirmeyin; tek değişken üçüncü seçeneğin varlığıdır.
- Kurumsal fiyat sayfası gizliyse bu senaryoyu `saas-b2b.md`’deki plan-varsayılanı senaryosuyla karıştırmayın; ikisi ayrı testtir.

### EN

Choosing between two plans is hard because there is no common yardstick to compare them by. Adding a third plan priced close to the middle plan but with less in it can make the middle plan look like “clearly the better option”; the third plan itself is almost never chosen, its job is to be a comparison anchor. It adds no new advantage; it changes how the existing two plans are perceived relative to the third.

**What to test**
- Price gap: Does the effect strengthen as the gap between the decoy and the middle plan shrinks?
- Real demand: Does the decoy plan itself get chosen at a notable rate, or stay in the background as expected?
- Perception: Does showing three options make the overall price look expensive?
- Segment: Do business and individual buyers react differently to the three-option structure?

**KPIs to track**
- Revenue per Visitor (RPV): Does adding the decoy raise revenue?
- Middle Plan Selection Rate: Does the share of visitors who choose the middle plan rise?
- Decoy Selection Rate: The plan itself must not draw notable demand; if it does, the structure was built wrong.
- Top-Tier Plan Sales: Sales of the real most expensive plan must not drop.
- Support Contact Rate: “Which plan should I choose” questions must not rise.

**What not to do**
- Don’t make the decoy plan unpurchasable or give it unreal contents; it must be a real, usable plan, only weakly positioned.
- Don’t change the price of the middle plan in the same test in which you add the third plan; you can’t tell whether the choice gain came from the anchor or the new price.
- Don’t price the decoy plan below its real cost and make the main plans look artificially expensive.
- Don’t enrich the contents of the middle plan during the test; the only variable is the presence of the third option.
- If the business pricing page is hidden, don’t confuse this scenario with the plan-default scenario in `saas-b2b.md`; they are separate tests.

---

## Fiyat planlarını ucuzdan pahalıya mı, pahalıdan ucuza mı sıralamalı?

Değişken: Fiyat planlarının sıralama yönü · Fark: değiştir

Etiket: id=pr-010 · mercek=Fiyat · düzey=görsel · sektör=saas · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should pricing plans run from cheapest to most expensive or the other way round?

EN-Variable: Sort direction of the pricing plans

Planların soldan sağa hangi sırayla dizildiği, karşılaştırma sırasında hangi planın çapa görevi göreceğini belirler. Pahalı plan önce görünürse sonraki planlar daha uygun hissettirebilir; ucuz plan önce görünürse ziyaretçi bütçe eksenli düşünmeye başlar. Bu, plan sayısından ve tablo/kart biçiminden ayrı bir değişkendir; sıralama, ne gösterildiğini değil hangi sırayla görüldüğünü test eder.

**Test edilmesi gerekenler**
- Yön: Ucuzdan pahalıya mı, pahalıdan ucuza mı toplam geliri artırıyor?
- Çapa etkisi: İlk görülen plan sonraki planların algılanan değerini nasıl değiştiriyor?
- Öne çıkan plan: Sıra değişince “önerilen” plan etiketi hâlâ doğru planda mı duruyor?
- Kaydırma: Mobilde ilk görülen plan, kaydırmadan görünen tek plan oluyor mu?
- Segment: Kurumsal ve bireysel ziyaretçi farklı bir sıradan mı etkileniyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sıralama geliri artırıyor mu?
- Önerilen Plan Seçim Oranı: Öne çıkarılan planın seçilme oranı değişiyor mu?
- En Ucuz Plan Seçim Oranı: Aşağı kayma artmamalı.
- Karar Süresi: Sayfada karar verme süresi kabul edilemez ölçüde uzamamalı.
- Destek Talebi: “Hangi planı seçmeliyim” soruları artmamalı.

**Yapılmaması gerekenler**
- Aynı testte plan sırasını ve hangi planın “önerilen” olarak etiketlendiğini birlikte değiştirmeyin.
- Sıralamayı, plan içeriklerini veya fiyatlarını aynı anda değiştirerek test etmeyin.
- Pahalı planı önce göstererek ucuz planı yapay biçimde küçük veya eksik göstermeyin.
- Pahalıdan ucuza sıralamada mobilde yalnızca en pahalı planın görüneceği bir düzeni, diğer planlara geçiş ipucu vermeden yayınlamayın.
- Enterprise/kurumsal planı bu sıralamaya dahil ediyorsanız `saas-b2b.md`’deki fiyat gizleme senaryosuyla çelişmeyin.

### EN

The order in which plans are laid out from left to right decides which plan acts as the anchor during comparison. If the expensive plan is seen first, the following plans can feel more affordable; if the cheap plan is seen first, the visitor starts thinking along the budget axis. This is a separate variable from the number of plans and from the table/card format; ordering tests not what is shown but the order in which it is seen.

**What to test**
- Direction: Does cheapest to most expensive, or most expensive to cheapest, raise total revenue?
- Anchor effect: How does the first plan seen change the perceived value of the plans after it?
- Highlighted plan: When the order changes, is the “recommended” plan label still on the right plan?
- Scrolling: On mobile, does the first plan seen become the only plan visible without scrolling?
- Segment: Are business and individual visitors affected by a different order?

**KPIs to track**
- Revenue per Visitor (RPV): Does the ordering raise revenue?
- Recommended Plan Selection Rate: Does the selection rate of the highlighted plan change?
- Cheapest Plan Selection Rate: Downward drift must not rise.
- Time to Decision: The time to decide on the page must not lengthen to an unacceptable degree.
- Support Contact Rate: “Which plan should I choose” questions must not rise.

**What not to do**
- Don’t change the plan order and which plan is labeled “recommended” together in the same test.
- Don’t test the ordering by changing plan contents or prices at the same time.
- Don’t show the expensive plan first and make the cheap plan look artificially small or incomplete.
- Don’t ship a layout in the most-expensive-first order where only the most expensive plan is visible on mobile, without a cue to reach the other plans.
- If you include the enterprise/business plan in this ordering, don’t contradict the price-hiding scenario in `saas-b2b.md`.

---

## Fiyattan önce yüksek bir referans sayı göstermek algılanan değeri artırır mı?

Değişken: Fiyattan önce gösterilen referans sayı · Fark: ekle

Etiket: id=pr-011 · mercek=Fiyat · düzey=bilgi · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does showing a high reference number before the price raise perceived value?

EN-Variable: Reference number shown before the price

Bir fiyat, yanında yüksek bir referans sayı (“piyasa ortalaması ₺X”, “benzer hizmetler ₺Y’ye kadar”) olmadan gösterildiğinde ziyaretçi değeri tek başına yargılar; referans sayı önce görüldüğünde asıl fiyat ona göre daha uygun hissedilebilir. Bu, üstü çizili “eski fiyat” göstermekten farklıdır; burada referans sizin geçmiş fiyatınız değil, dış bir karşılaştırma noktasıdır ve doğruluğu ayrıca doğrulanmalıdır.

**Test edilmesi gerekenler**
- Varlık: Referans sayı göstermek satın alma oranını artırıyor mu?
- Sonraki test: Referans sayı kazanırsa kaynağını (piyasa ortalaması / bağımsız ölçüm) belirtmek ayrı bir testte inandırıcılığı artırıyor mu?
- Fark büyüklüğü: Referans ile asıl fiyat arasındaki fark büyüdükçe etki güçleniyor mu, yoksa güven mi düşüyor?
- Şüphe etkisi: Referans sayıyı gören ziyaretçiler karşılaştırmayı sorgulayıp fiyatı başka yerde aramaya mı gidiyor?
- Segment: Piyasa fiyatını zaten bilen fiyata duyarlı ziyaretçide referans sayı, fiyat bilgisi olmayan ziyaretçiye göre daha az mı etkili?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Referans sayı geliri artırıyor mu?
- Dönüşüm Oranı (CR): Referans sayı satın alma oranını artırıyor mu?
- Güven Algısı (anket): Referans sayı inandırıcı bulunuyor mu, yoksa şüphe mi uyandırıyor? Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- İade veya İtiraz Oranı (30 gün): “Yanıltıcı karşılaştırma” şikâyeti artmamalı.
- Ortalama Sepet Tutarı (AOV): Referans sayı ortalama tutarı düşürmemeli.

**Yapılmaması gerekenler**
- Doğrulanamayan veya uydurma bir referans sayı göstermeyin; piyasa ortalaması veya rakip fiyatı iddiası gerçek, güncel bir kaynağa dayanmalı.
- Aynı testte referans sayının varlığını ve asıl fiyat seviyesini birlikte değiştirmeyin.
- Referans sayıyı gerçekçi olmayacak kadar büyük seçip asıl fiyatı yapay biçimde ucuz göstermeyin.
- Rakip fiyatını isim vererek gösteriyorsanız haksız rekabet veya karşılaştırmalı reklam kurallarını hedef pazarda doğrulamadan yayınlamayın.
- Referans sayıyı güncellemiyorsanız eski veya geçersiz bir rakamda donmuş bırakmayın.

### EN

When a price is shown without a high reference number beside it (“market average ₺X”, “similar services up to ₺Y”), the visitor judges the value alone; when the reference number is seen first, the real price can feel more reasonable by comparison. This differs from showing a struck-through “old price”; here the reference is not your own past price but an external comparison point, and its accuracy has to be verified separately.

**What to test**
- Presence: Does showing a reference number raise the purchase rate?
- Next test: If the reference number wins, does stating its source (market average / independent measurement) raise credibility in a separate test?
- Size of the gap: Does the effect strengthen as the gap between the reference and the real price grows, or does trust fall?
- Suspicion effect: Do visitors who see the reference number question the comparison and go looking for the price elsewhere?
- Segment: For a price-sensitive visitor who already knows the market price, is the reference number less effective than for a visitor with no price knowledge?

**KPIs to track**
- Revenue per Visitor (RPV): Does the reference number raise revenue?
- Conversion Rate (CR): Does the reference number raise the purchase rate?
- Trust Perception (survey): Is the reference number found credible, or does it raise suspicion? The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms, and this is a diagnostic signal.
- Return or Dispute Rate (30 days): “Misleading comparison” complaints must not rise.
- Average Order Value (AOV): The reference number must not lower the average amount.

**What not to do**
- Don’t show an unverifiable or made-up reference number; a market average or competitor price claim must rest on a real, current source.
- Don’t change the presence of the reference number and the real price level together in the same test.
- Don’t choose a reference number so large it is unrealistic and make the real price look artificially cheap.
- If you show a competitor’s price by name, don’t publish without verifying the unfair competition or comparative advertising rules in the target market.
- If you don’t keep the reference number up to date, don’t leave it frozen at an old or invalid figure.
