# Buton, bağlantı ve arayüz öğeleri

Yolculuk aşaması: sayfaya değil öğeye bağlı kararlar. Bir butonun ne dediği, bir bağlantının nasıl davrandığı, bir ikonun etiketli olup olmadığı her sayfada karşınıza çıkar; bu yüzden ayrı bir dosyada toplanmıştır. Buton rengi ve CTA sayısı `cart-checkout.md`, CTA tekrarı `home-landing.md`, ürün sayfasındaki satın alma butonu `product-detail.md` içindedir.

**Bir uyarı.** Bu dosyadaki değişikliklerin çoğu etki sıralamasının alt kademesindedir (`knowledge/methodology.md` → Fikir üretme merceği): daha yüksek kademeden bir aday varken bunlar birinci sıraya konmaz. Yasak değildir; buradaki bir senaryo, sayfada gözlemlenebilen bir kullanıcı engeline dayanan güçlü bir mekanizmaya sahipse önerilir (ör. kontrastı yetersiz olduğu için gerçekten görülmeyen bir buton). Mekanizması “daha dikkat çekici olur” seviyesinde kalıyorsa önerilmez. Düşük trafikli sayfada bu testler ölçülemeyecek kadar küçük fark arar; orada daha yapısal bir değişiklik tercih edilir (`methodology.md` → Uygunluk tablosu). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Buton metni eylemi mi, kazanılan şeyi mi söylemeli?

Değişken: Buton metninin ifade çerçevesi · Fark: değiştir

Etiket: id=ui-001 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should button copy say the action or what you get?

EN-Variable: Framing of the button copy

“Gönder” butonun ne yaptığını söyler, “Fiyat teklifimi al” tıklandığında ne kazanılacağını söyler. Kazanç ifadesi motive edebilir ama uzar, butonu şişirir ve bazı bağlamlarda abartılı durur. Eylem ifadesi kısadır ve beklentiyi tam karşılar; buna karşılık ilerlemek için bir sebep sunmaz.

**Test edilmesi gerekenler**
- İfade: Kazanç ifadesi tıklamayı artırıyor mu?
- Uzunluk: Uzayan metin butonun tanınmasını zorlaştırıyor mu?
- Beklenti: Kazanç ifadesi tıklandıktan sonra gerçekten karşılanıyor mu?
- Sonraki test: Kazanan çerçeve sabitken birinci tekil kişi eki (“teklifimi al” / “teklif al”) ayrı bir testte tıklamayı değiştiriyor mu?
- Segment: Tıklayınca ne alacağını henüz bilmeyen yeni ziyaretçide kazanç ifadesi, akışı tanıyan dönen kullanıcıdan daha çok mu tıklatıyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Buton metni sonraki adımın tamamlanmasını artırıyor mu?
- CTA Tıklama Oranı: Tıklama artıyor mu?
- Aksiyon Sonrası Dökülme Oranı: Beklentisi karşılanmayan kullanıcı sonraki adımda kaybedilmemeli.
- Geri Dönüş Oranı: Butona tıklayıp geri dönme artmamalı.
- Erişilebilirlik: Ekran okuyucuda tek başına anlamsız kalan buton metni bırakılmamalı.

**Yapılmaması gerekenler**
- Butonda tıklandığında gerçekleşmeyecek bir sonucu vaat etmeyin.
- Aynı testte buton metni ile buton biçimini birlikte değiştirmeyin.
- Metni butona sığmayacak kadar uzatıp iki satıra bölmeyin.
- Aynı sayfadaki iki butonu farklı yaklaşımla yazıp hangisinin etkilediğini karıştırmayın.
- Kazanç ifadesini, tıklamanın bir ödeme veya bağlayıcı işlem başlattığını gizleyecek biçimde yazmayın.


> **Not:** SaaS deneme CTA’sının metni `saas-b2b.md`’de kendi senaryosudur (huni-sonu birincil metrikleriyle); deneme akışı için onu kullanın.

### EN

“Submit” says what the button does, “Get my quote” says what you gain by clicking. A benefit phrase can motivate but it runs long, bloats the button and can sound exaggerated in some contexts. An action phrase is short and sets exactly the right expectation; on the other hand, it gives no reason to move forward.

**What to test**
- Wording: Does the benefit phrase raise clicks?
- Length: Does the longer copy make the button harder to recognize?
- Expectation: Is the benefit phrase actually delivered after the click?
- Next test: With the winning framing fixed, does a first-person form (“get my quote” / “get a quote”) change clicks in a separate test?
- Segment: Does the benefit phrase get more clicks from new visitors who don’t yet know what they will get than from returning users who know the flow?

**KPIs to track**
- Primary Action Completion Rate: Does the button copy raise completion of the next step?
- CTA Click Rate: Do clicks go up?
- Post-Click Drop-off Rate: Users whose expectation isn’t met must not be lost at the next step.
- Back-Navigation Rate: Clicking the button and coming straight back must not increase.
- Accessibility Check: No button copy should be left meaningless on its own for a screen reader.

**What not to do**
- Don’t promise on the button an outcome the click won’t deliver.
- Don’t change the button copy and the button style in the same test.
- Don’t stretch the copy until it no longer fits and wraps onto two lines.
- Don’t write two buttons on the same page with different approaches and blur which one made the difference.
- Don’t word the benefit phrase so that it hides that the click starts a payment or a binding action.

> **Note:** The copy of a SaaS trial CTA is its own scenario in `saas-b2b.md` (with its end-of-funnel primary metrics); use that one for the trial flow.

---
## Dolu buton mu, çerçeveli buton mu daha çok tıklanıyor?

Değişken: Buton dolgu biçimi · Fark: değiştir

Etiket: id=ui-002 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Solid button or outline button: which gets more clicks?

EN-Variable: Button fill style

Dolu buton görsel ağırlığıyla öne çıkar ve birincil aksiyonu işaret eder. Çerçeveli (içi boş) buton sayfayı sakinleştirir ve ikincil aksiyonlar için doğal görünür. İkisini de dolu yapmak hiyerarşiyi yok eder; ikisini de çerçeveli yapmak hiçbirini öne çıkarmaz.

**Test edilmesi gerekenler**
- Biçim: Dolu buton tıklamayı artırıyor mu?
- Hiyerarşi: Birincil ve ikincil aksiyon arasındaki fark yeterince belirgin mi?
- Rekabet: İki dolu buton birbirinin tıklamasını mı yiyor?
- Bağlam: Yoğun bir sayfada çerçeveli buton kayboluyor mu?
- Cihaz: Mobilde biçim farkı hâlâ ayırt ediliyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Birincil aksiyon artıyor mu?
- CTA Tıklama Oranı: Asıl istenen aksiyon artıyor mu?
- İkincil Buton Tıklama Oranı: İkincil aksiyon tamamen kaybolmamalı.
- Yanlış Tıklama Oranı: Belirsizleşen hiyerarşi, yanlış butona tıklayıp hemen geri dönenleri artırmamalı.
- Erişilebilirlik: Buton kenar ve metin kontrastı eşiğin altına inmemeli.

**Yapılmaması gerekenler**
- Aynı testte buton biçimi ile buton rengini birlikte değiştirmeyin.
- Çerçeveli butonu arka planla aynı tona getirip görünmez hâle sokmayın.
- Birincil butonu belirginleştirirken ikincil aksiyonu erişilemez yapmayın.
- Biçim değişikliğini yalnızca bir butonda yapıp sayfadaki diğerlerini eski hâlinde bırakmayın.
- Kontrast eşiğini karşılamayan bir varyantı kazanan ilan etmeyin.

### EN

A solid button stands out through its visual weight and marks the primary action. An outline (hollow) button calms the page and looks natural for secondary actions. Making both solid destroys the hierarchy; making both outline leaves neither standing out.

**What to test**
- Style: Does the solid button raise clicks?
- Hierarchy: Is the difference between the primary and secondary action clear enough?
- Competition: Do two solid buttons eat into each other’s clicks?
- Context: Does the outline button get lost on a dense page?
- Device: Is the style difference still distinguishable on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does the primary action go up?
- CTA Click Rate: Does the action we actually want go up?
- Secondary Button Click Rate: The secondary action must not disappear entirely.
- Misclick Rate: A blurred hierarchy must not increase clicks on the wrong button followed by an immediate return.
- Accessibility Check: Button border and text contrast must not fall below the threshold.

**What not to do**
- Don’t change the button style and the button color in the same test.
- Don’t make the outline button the same tone as the background so that it becomes invisible.
- Don’t emphasize the primary button by making the secondary action unreachable.
- Don’t apply the style change to only one button and leave the others on the page as they were.
- Don’t declare a variant the winner if it fails the contrast threshold.

---
## İkincil aksiyonu bağlantı mı, buton mu yapmalı?

Değişken: İkincil aksiyonun biçimi · Fark: değiştir

Etiket: id=ui-003 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should the secondary action be a link or a button?

EN-Variable: Presentation of the secondary action

Butona benzeyen bir öğe tıklanabilirliğini açıkça duyurur; bağlantı ise daha hafif durur ve birincil aksiyonla rekabet etmez. İkincil aksiyonu buton yapmak onu görünür kılar ama asıl istenen aksiyonun payını azaltabilir. Bağlantı yapmak ise onu tamamen görünmez kılabilir. “Sepet ve ödeme adımlarında tekrarlayan CTA’ları azaltmak dönüşümü artırır mı?” senaryosundan (`cart-checkout.md`) farkı: o senaryo aynı işlevdeki CTA’ların sayısını azaltır, bu senaryo farklı işlevdeki ikincil aksiyonun biçimini değiştirir.

**Test edilmesi gerekenler**
- Biçim: İkincil aksiyon buton olduğunda toplam ilerleme artıyor mu?
- Yamyamlık: İkincil aksiyon birincilin tıklamasını mı alıyor?
- Görünürlük: Bağlantı hâlinde kaç kullanıcı öğeyi fark ediyor?
- Cihaz: Mobilde bağlantının dokunma hedefi yeterli mi?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: İki yolun toplamı artıyor mu?
- Birincil Aksiyon Oranı: Asıl istenen aksiyon kabul edilemez ölçüde düşmemeli.
- İkincil Aksiyon Oranı: İkincil yolun kullanımı ne kadar?
- Karar Süresi: Eş ağırlıklı iki seçenek karar süresini kabul edilemez ölçüde uzatmamalı.
- Erişilebilirlik: Dokunma hedefi küçülmemeli, odak görünürlüğü bozulmamalı.

**Yapılmaması gerekenler**
- Gezinme amaçlı bir bağlantıyı buton, işlem yapan bir butonu bağlantı olarak işaretlemeyin; semantik doğru kalmalıdır.
- Aynı testte biçim ile konumu birlikte değiştirmeyin.
- İkincil aksiyonu birincil kadar belirgin yapıp hiyerarşiyi silmeyin.
- Bağlantıyı yalnızca renkle ayırt edilebilir bırakmayın.
- Buton kolunda ikincil aksiyonun metnini uzatıp birincil butonu mobilde alt satıra itmeyin.

### EN

An element that looks like a button announces that it is clickable; a link looks lighter and doesn’t compete with the primary action. Making the secondary action a button makes it visible but can reduce the share of the action we actually want. Making it a link can make it completely invisible. How it differs from the “Does cutting repeated CTAs in the cart and checkout steps raise conversion?” scenario (`cart-checkout.md`): that one reduces the number of CTAs with the same function, this one changes the presentation of a secondary action with a different function.

**What to test**
- Style: Does total progress go up when the secondary action is a button?
- Cannibalization: Does the secondary action take clicks from the primary one?
- Visibility: How many users notice the element when it is a link?
- Device: Is the tap target of the link big enough on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does the sum of the two paths go up?
- Primary Action Rate: The action we actually want must not drop unacceptably.
- Secondary Action Rate: How much is the secondary path used?
- Time to Decision: Two equally weighted options must not lengthen decision time unacceptably.
- Accessibility Check: The tap target must not shrink and focus visibility must not break.

**What not to do**
- Don’t mark a navigation link as a button or an action button as a link; the semantics must stay correct.
- Don’t change the style and the position in the same test.
- Don’t make the secondary action as prominent as the primary one and erase the hierarchy.
- Don’t leave the link distinguishable by color alone.
- In the button arm, don’t lengthen the secondary action’s copy so that it pushes the primary button onto the next line on mobile.

---
## Buton stillerini tüm sayfada tutarlı tutmak fark yaratır mı?

Değişken: Buton stillerinin sayfa içi tutarlılığı · Fark: değiştir

Etiket: id=ui-004 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=klasik · tarih=2026-11

EN: Does keeping button styles consistent across the page make a difference?

EN-Variable: Consistency of button styles across the page

Tutarlı buton stili neyin tıklanabilir olduğunu öğretir ve kullanıcı bir kez öğrendiğinde her yerde uygular. Bölümden bölüme değişen stiller dikkat çekebilir ama tıklanabilirlik işaretini bulanıklaştırır. Tutarlılık aynı zamanda tek tek bölümlerin öne çıkma imkânını azaltır.

**Test edilmesi gerekenler**
- Tutarlılık: Tüm butonları tek stile getirmek toplam aksiyonu artırıyor mu?
- Tanınırlık: Kullanıcı neyin tıklanabilir olduğunu daha hızlı anlıyor mu?
- Vurgu kaybı: Farklılaşan bir bölüm tutarlılık uğruna görünürlük kaybediyor mu?
- Kapsam: Tutarlılık sayfa içinde mi, tüm site genelinde mi kurulmalı?
- Cihaz: Mobilde stil farkları zaten ayırt edilebiliyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Tutarlılık ilerlemeyi artırıyor mu?
- Tıklanabilir Öğe Etkileşim Oranı: Etkileşim artıyor mu?
- Yanlış Tıklama Oranı: Tıklanabilir sanılan öğelere tıklama azalıyor mu?
- Bölüm Bazlı Etkileşim: Belirli bir bölümün etkileşimi kabul edilemez ölçüde düşmemeli.
- Erişilebilirlik: Odak göstergesi hiçbir butonda görünmez hâle gelmemeli.

**Yapılmaması gerekenler**
- Aynı testte stil tutarlılığı ile buton metinlerini birlikte değiştirmeyin.
- Tutarlılık adına birincil ve ikincil ayrımını da silmeyin.
- Tek stile geçerken yıkıcı işlem (sil, iptal) yapan butonu birincil butonla aynı görünüme sokmayın.
- Eski stili kullanmaya devam eden bölümleri test dışında bırakıp sonucu genellemeyin.
- Tutarlılığı, aslında farklı işlev gören öğeleri aynı göstermek için kullanmayın.

### EN

Consistent button styles teach what is clickable, and once the user has learned it they apply it everywhere. Styles that change from section to section can draw attention but blur the signal of clickability. Consistency also reduces the chance of individual sections standing out.

**What to test**
- Consistency: Does bringing all buttons to a single style raise total actions?
- Recognition: Do users understand faster what is clickable?
- Lost emphasis: Does a section that used to stand out lose visibility for the sake of consistency?
- Scope: Should consistency be set within the page or across the whole site?
- Device: Are style differences already distinguishable on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does consistency raise progress?
- Clickable Element Engagement Rate: Does engagement go up?
- Misclick Rate: Do clicks on elements mistaken for clickable go down?
- Section-Level Engagement: The engagement of a particular section must not drop unacceptably.
- Accessibility Check: The focus indicator must not become invisible on any button.

**What not to do**
- Don’t change style consistency and button copy in the same test.
- Don’t erase the primary and secondary distinction in the name of consistency.
- When moving to a single style, don’t make a button that performs a destructive action (delete, cancel) look the same as the primary button.
- Don’t leave out the sections that keep the old style and then generalize the result.
- Don’t use consistency to make elements with different functions look the same.

---
## Büyük taahhüt butonu mu, küçük adım butonu mu daha çok ilerletiyor?

Değişken: CTA’nın taahhüt düzeyi · Fark: değiştir

Etiket: id=ui-005 · mercek=Çaba · düzey=akış · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Big-commitment button or small-step button: which moves more people forward?

EN-Variable: Commitment level of the CTA

“Satın al” doğrudan sonuca gider ama hazır olmayan ziyaretçiyi durdurur. “Önce dene”, “Fiyatı gör” gibi küçük bir adım daha çok tıklanır ama ilerleyen kullanıcıların bir kısmı sonuca hiç ulaşmaz. Doğru cevap, ziyaretçinin karar aşamasına ve ürünün fiyat seviyesine bağlıdır.

**Test edilmesi gerekenler**
- Taahhüt: Küçük adım butonu toplam dönüşümü artırıyor mu?
- Zincir: Küçük adımı atanların kaçı sonuca ulaşıyor?
- Metin: Küçük adımın ne kadar küçük olduğu ifadeden anlaşılıyor mu?
- Segment: Yeni ziyaretçi ile karar aşamasındaki ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Huninin sonundaki tamamlama artıyor mu?
- CTA Tıklama Oranı: İlk aksiyon artıyor mu?
- Ara Adım → Sonuç Geçiş Oranı: Küçük adımı atanların sonuca ulaşma oranı düşmemeli.
- Karar Süresi: Toplam satın alma süresi kabul edilemez ölçüde uzamamalı.
- Aksiyon Kalitesi: Kolaylaşan ilk adım niteliksiz talep getirmemeli.

**Yapılmaması gerekenler**
- Ara adımın tıklamasını nihai dönüşüm gibi raporlamayın; birincil metrik daima huninin sonudur.
- Aynı testte buton taahhüdü ile fiyat gösterimini birlikte değiştirmeyin.
- Küçük adımı, aslında büyük bir taahhüde götüren bir kapı gibi kurmayın.
- İki butonu eşit görsel ağırlıkta verip hiyerarşiyi silmeyin.
- “Fiyatı gör” gibi küçük adım butonunu, fiyatın zaten sayfada yazdığı bir yerde kullanmayın; adımın gerçek bir karşılığı olmalı.

### EN

“Buy” goes straight to the outcome but stops a visitor who isn’t ready. A small step such as “Try first” or “See price” gets more clicks, but some of the users who move forward never reach the outcome. The right answer depends on the visitor’s decision stage and the product’s price level.

**What to test**
- Commitment: Does the small-step button raise total conversion?
- Chain: How many of those who take the small step reach the outcome?
- Copy: Is it clear from the wording how small the small step is?
- Segment: Do new visitors and visitors at the decision stage react differently?

**KPIs to track**
- Conversion Rate (CR): Does completion at the end of the funnel go up?
- CTA Click Rate: Does the first action go up?
- Intermediate Step to Outcome Rate: The share of those who take the small step and reach the outcome must not drop.
- Time to Decision: Total time to purchase must not lengthen unacceptably.
- Action Quality: A first step that has become easier must not bring unqualified leads.

**What not to do**
- Don’t report the click on the intermediate step as a final conversion; the primary metric is always the end of the funnel.
- Don’t change the button commitment and the price display in the same test.
- Don’t build the small step as a gateway that actually leads to a big commitment.
- Don’t give the two buttons equal visual weight and erase the hierarchy.
- Don’t use a small-step button like “See price” where the price is already on the page; the step must have a real payoff.

---
## İkonların yanına yazılı etiket eklemek işe yarar mı?

Değişken: İkon yanındaki yazılı etiket · Fark: ekle

Etiket: id=ui-006 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding a text label next to icons pay off?

EN-Variable: Text label next to icons

İkon yer kazandırır ve dili aşar ama anlamı çoğu zaman öğrenilmiş bir konvansiyona dayanır; tanınmayan bir ikon boş bir kutudur. Etiket eklemek anlamı netleştirir, buna karşılık yer kaplar ve arayüzü kalabalıklaştırır. Özellikle az kullanılan işlevlerde etiketin değeri yükselir.

**Test edilmesi gerekenler**
- Etiket: İkona metin eklemek kullanımı artırıyor mu?
- Tanınırlık: Hangi ikonlar etiketsiz zaten anlaşılıyor?
- Kalabalık: Etiketler diğer öğelerin alanını daraltıyor mu?
- Cihaz: Mobilde etiket için yer kalıyor mu?

**Takip edilecek ana KPI’lar**
- İşlev Kullanım Oranı (ikonun işlevi): İkonun temsil ettiği işlevin kullanımı artıyor mu?
- Ana Aksiyon Tamamlama Oranı: Genel ilerleme düşmemeli.
- Yanlış Tıklama Oranı: Beklenmeyen işleve tıklama azalıyor mu?
- Destek Talebi: “Bunu nerede yapıyorum” soruları azalıyor mu?
- Erişilebilirlik: Etiketsiz ikon erişilebilir adsız kalmamalı.

**Yapılmaması gerekenler**
- Aynı testte etiketi eklerken ikonun kendisini de değiştirmeyin.
- Etiketi yalnızca üzerine gelince görünen bir ipucuna dönüştürüp “etiket eklendi” saymayın.
- Etiket eklerken dokunma hedeflerini küçültmeyin.
- Ekran okuyucu için tanımlı erişilebilir adı görsel etikete bağımlı hâle getirmeyin.
- Etiketi ikonun gerçek işlevinden farklı bir şey vaat edecek biçimde yazmayın.

### EN

An icon saves space and crosses languages, but its meaning often rests on a learned convention; an unrecognized icon is an empty box. Adding a label clarifies the meaning, but it takes space and clutters the interface. The label is worth most for rarely used functions.

**What to test**
- Label: Does adding text to the icon raise usage?
- Recognition: Which icons are already understood without a label?
- Clutter: Do the labels squeeze the space of other elements?
- Device: Is there room for the label on mobile?

**KPIs to track**
- Function Usage Rate (icon function): Does use of the function the icon stands for go up?
- Primary Action Completion Rate: Overall progress must not drop.
- Misclick Rate: Do clicks on an unexpected function go down?
- Support Contact Rate: Do “where do I do this” questions go down?
- Accessibility Check: No unlabeled icon should be left without an accessible name.

**What not to do**
- Don’t change the icon itself while adding the label in the same test.
- Don’t turn the label into a hover-only tooltip and count it as “label added”.
- Don’t shrink the tap targets while adding the label.
- Don’t make the accessible name defined for screen readers depend on the visual label.
- Don’t word the label so that it promises something different from the icon’s real function.

---
## Form ve ödeme akışındaki yardım bağlantılarını yeni sekmede açmak tamamlamayı artırır mı?

Değişken: Akış içi yardım bağlantılarının açıldığı sekme · Fark: değiştir

Etiket: id=ui-007 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does opening help links in a form or checkout flow in a new tab raise completion?

EN-Variable: The tab in which help links inside the flow open

Akışın içindeki yardım, yasal metin veya koşul bağlantısını yeni sekmede açmak kullanıcının yarım kalan formu veya ödemeyi kaybetmemesini sağlar. Karşı tarafta: kullanıcı denetimini elinden alır, geri tuşunu işlevsiz kılar, mobilde sekme yönetimi zordur ve beklenmedik davranış rahatsız eder. İçerik sayfasındaki dış bağlantıları (blog kaynağı, iş ortağı sitesi) yeni sekmede açmak aynı sorunun etkisi küçük bir türüdür ve ayrı bir test olarak önerilmez; burada ölçülen, akış içindeki bağlantının yarım kalan formu ya da ödemeyi koruyup korumadığıdır.

**Test edilmesi gerekenler**
- Davranış: Yeni sekmede açmak asıl akışın tamamlanmasını artırıyor mu?
- Kapsam: Hangi bağlantılar (yasal metin, yardım, dış kaynak) yeni sekmede açılmalı?
- Erişilebilirlik: Ekran okuyucu kullanıcısı bağlantının yeni sekmede açılacağını önceden duyuyor mu, yoksa sekme değişimini fark etmeden mi kalıyor?
- Geri dönüş: Yeni sekmeden asıl akışa dönüş gerçekleşiyor mu?
- Cihaz: Mobilde sekme değişimi kullanıcıyı kaybettiriyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Form veya ödeme tamamlanması artıyor mu?
- Bağlantı Tıklama Oranı: Bağlantıya erişim düşmemeli.
- Akışa Geri Dönüş Oranı: Ayrılan kullanıcının dönüşü artıyor mu?
- Veri Kaybı Oranı: Yarım kalan formdaki veri kaybolmamalı.
- Erişilebilirlik: Yeni sekme davranışı bildirimsiz bırakılmamalı.

**Yapılmaması gerekenler**
- Sitedeki tüm bağlantıları ayrım yapmadan yeni sekmede açmayın.
- Yeni sekme davranışını kullanıcıya bildirmeden uygulamayın.
- Aynı testte sekme davranışı ile bağlantı metnini birlikte değiştirmeyin.
- Yeni sekmeyi, kullanıcının çıkmasını engellemek için kullanmayın.
- Form verisinin korunmasını çözmek yerine yeni sekmeyi yama olarak kullanmayın.

### EN

Opening a help, legal text or terms link inside the flow in a new tab keeps the user from losing a half-finished form or payment. On the other side: it takes control away from the user, breaks the back button, makes tab management hard on mobile and unexpected behavior annoys. Opening external links on a content page (a blog source, a partner site) in a new tab is a small-impact version of the same question and isn’t proposed as a separate test; what is measured here is whether the link inside the flow protects the half-finished form or payment.

**What to test**
- Behavior: Does opening in a new tab raise completion of the main flow?
- Scope: Which links (legal text, help, external source) should open in a new tab?
- Accessibility: Does a screen reader user hear in advance that the link opens in a new tab, or do they miss the tab switch?
- Return: Do users actually get back to the main flow from the new tab?
- Device: Does switching tabs make users get lost on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does form or payment completion go up?
- Link Click Rate: Reach to the link must not drop.
- Return-to-Flow Rate: Do users who left come back more often?
- Data Loss Rate: Data in a half-finished form must not be lost.
- Accessibility Check: The new tab behavior must not go unannounced.

**What not to do**
- Don’t open all links on the site in a new tab without distinction.
- Don’t apply the new tab behavior without telling the user.
- Don’t change the tab behavior and the link copy in the same test.
- Don’t use the new tab to keep the user from leaving.
- Don’t use the new tab as a patch instead of solving form data preservation.

---
## Metin içine yerleştirilen bağlantı tıklanıyor mu?

Değişken: Paragraftaki yolun sunuluş biçimi · Fark: değiştir

Etiket: id=ui-008 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Do links placed inside the text get clicked?

EN-Variable: Presentation of the path in the paragraph

Açıklama metninin içine gömülü bir bağlantı, tam ilgili düşünce oluştuğu anda yol sunar ve ayrı bir buton kadar rahatsız etmez. Riski: metin içinde gözden kaçar, tıklanabilirliği butona göre zayıf işaretlenir ve okuma akışını bölerek kullanıcıyı erken uzaklaştırabilir.

**Test edilmesi gerekenler**
- Yerleşim: Metin içi bağlantı ayrı bir butondan daha mı çok tıklanıyor?
- Görünürlük: Bağlantı yeterince ayırt edilebiliyor mu?
- Erken ayrılma: Bağlantı okuma akışını bölüp asıl mesajı yarıda mı bırakıyor?
- Segment: Okuyan ve tarayan kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Bağlantı asıl hedefe götürüyor mu?
- Bağlantı Tıklama Oranı: Tıklama artıyor mu?
- Kaydırma Derinliği: Metnin okunması kabul edilemez ölçüde düşmemeli.
- Geri Dönüş Oranı: Bağlantıyla erken ayrılan kullanıcı, hedef sayfadan hemen geri dönmemeli.
- Erişilebilirlik: Bağlantı yalnızca renkle işaretlenmemeli.

**Yapılmaması gerekenler**
- Bağlantıyı çevresindeki metinden ayırt edilemeyecek biçimde biçimlendirmeyin.
- Aynı testte bağlantı yerleşimi ile paragraf metnini birlikte değiştirmeyin.
- Bağlantı metnini “buraya tıklayın” gibi bağlamsız bir ifadeye indirgemeyin.
- Aynı paragrafa birden çok bağlantı koyup hangisinin çalıştığını ölçemez hâle gelmeyin.
- Metin içi bağlantıyı yeni sekmede açıp kullanıcıyı okuduğu sayfadan habersizce koparmayın.

### EN

A link embedded in explanatory text offers a path at exactly the moment the relevant thought forms and is less intrusive than a separate button. The risk: it gets overlooked in the text, its clickability is signaled more weakly than a button’s and it can break the reading flow and lead the user away early.

**What to test**
- Placement: Is the in-text link clicked more than a separate button?
- Visibility: Is the link distinguishable enough?
- Early exit: Does the link break the reading flow and leave the main message unfinished?
- Segment: Do readers and scanners react differently?

**KPIs to track**
- Primary Action Completion Rate: Does the link lead to the main goal?
- Link Click Rate: Do clicks go up?
- Scroll Depth: Reading of the text must not drop unacceptably.
- Back-Navigation Rate: A user who leaves early through the link must not bounce straight back from the target page.
- Accessibility Check: The link must not be marked by color alone.

**What not to do**
- Don’t style the link so that it can’t be told apart from the surrounding text.
- Don’t change the link placement and the paragraph text in the same test.
- Don’t reduce the link text to a context-free phrase such as “click here”.
- Don’t put several links in the same paragraph and make it impossible to measure which one works.
- Don’t open the in-text link in a new tab and pull the user away from the page they were reading without notice.

---
## Sık yapılan işlemler için kısayol sunmak işe yarar mı?

Değişken: Sık işlemler için kısayol · Fark: ekle

Etiket: id=ui-009 · mercek=Çaba · düzey=sürtünme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does offering shortcuts for frequent actions pay off?

EN-Variable: Shortcut for frequent actions

Tekrarlanan bir işlemi tek dokunuşa indirmek (tekrar sipariş, son aramayı yükle, kayıtlı adresle devam) deneyimli kullanıcıyı hızlandırır. Riski: kısayol arayüzde yer kaplar, yeni kullanıcı için anlamsızdır ve yanlış varsayımla hazırlanmış bir kısayol hatalı işleme yol açabilir.

**Test edilmesi gerekenler**
- Varlık: Kısayol sunmak tamamlamayı artırıyor mu?
- Hedef kitle: Kısayolu kimler kullanıyor, yeni kullanıcıya faydası var mı?
- Doğruluk: Kısayolun getirdiği varsayılan gerçekten doğru mu?
- Sonraki test: Kısayol kazanırsa, onu yalnızca geçmiş işlemi olan kullanıcıya göstermek ayrı bir testte tamamlamayı artırıyor mu?
- Segment: İlk kez gelen ile tekrar eden kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: İşlem tamamlanması artıyor mu?
- Kısayol Kullanım Oranı: Kısayol gerçekten kullanılıyor mu?
- Hatalı İşlem Oranı: Yanlış varsayılanla yapılan işlem artmamalı.
- İşlem Süresi: Tamamlama süresi kısalıyor mu?
- İptal veya Düzeltme Oranı (30 gün): Sonradan düzeltme talebi artmamalı.

**Yapılmaması gerekenler**
- Kısayolu geri alınamaz bir işlemi tek dokunuşa indirmek için kullanmayın.
- Aynı testte kısayol ile ana akışın adımlarını birlikte değiştirmeyin.
- Kısayolun getirdiği varsayılanı kullanıcıya göstermeden uygulamayın.
- Yeni kullanıcıya anlamsız gelen bir kısayolu ana akışın önüne koymayın.
- Kısayolla tekrarlanan siparişte eski siparişin fiyatını veya stok durumunu güncel gibi göstermeyin.

### EN

Reducing a repeated action to one tap (reorder, load the last search, continue with the saved address) speeds up experienced users. The risk: the shortcut takes up space in the interface, means nothing to a new user and a shortcut prepared on a wrong assumption can lead to a faulty action.

**What to test**
- Presence: Does offering a shortcut raise completion?
- Audience: Who uses the shortcut, and does it help new users?
- Accuracy: Is the default the shortcut brings actually correct?
- Next test: If the shortcut wins, does showing it only to users with a past action raise completion in a separate test?
- Segment: Do first-time and repeat users react differently?

**KPIs to track**
- Primary Action Completion Rate: Does completion of the action go up?
- Shortcut Usage Rate: Is the shortcut actually used?
- Faulty Action Rate: Actions made with a wrong default must not increase.
- Action Time: Does completion time get shorter?
- Cancellation or Correction Rate (30 days): Later correction requests must not increase.

**What not to do**
- Don’t use the shortcut to reduce an irreversible action to one tap.
- Don’t change the shortcut and the steps of the main flow in the same test.
- Don’t apply the default the shortcut brings without showing it to the user.
- Don’t put a shortcut that means nothing to a new user in front of the main flow.
- In a reorder through the shortcut, don’t show the old order’s price or stock status as if it were current.

---
## Bir adım bittiğinde otomatik olarak sonrakine geçmek işe yarar mı?

Değişken: Adımlar arası geçiş davranışı · Fark: değiştir

Etiket: id=ui-010 · mercek=Çaba · düzey=sürtünme · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does moving on to the next step automatically once a step is done pay off?

EN-Variable: Transition behavior between steps

Seçim yapılır yapılmaz sonraki adıma geçmek bir tıklamayı ortadan kaldırır ve akışı hızlandırır. Bedeli: kullanıcı seçimini gözden geçiremez, yanlış dokunuş geri alınamaz bir ilerlemeye dönüşür ve kontrol hissi kaybolur. Geri dönüşün ne kadar kolay olduğu belirleyicidir.

**Test edilmesi gerekenler**
- Otomatik geçiş: Seçimden sonra otomatik ilerleme tamamlamayı artırıyor mu?
- Hata: Yanlış seçimle ilerleme ne sıklıkla oluyor?
- Geri dönüş: Geri dönmek ne kadar kolay, veri korunuyor mu?
- Gecikme: Kısa bir bekleme eklemek hatayı azaltıyor mu?
- Cihaz: Mobilde yanlış dokunma kaynaklı geçiş daha mı sık?

**Takip edilecek ana KPI’lar**
- Akış Tamamlama Oranı: Otomatik geçiş tamamlamayı artırıyor mu?
- Geri Dönüş Oranı: Bir önceki adıma dönme artmamalı.
- Hatalı Seçim Oranı: Yanlış seçimle ilerleme artmamalı.
- Görev Tamamlama Süresi (akış): Akış hızlanıyor mu?
- Erişilebilirlik: Otomatik geçişte odak eski adımda kalmamalı, geçiş duyurusuz olmamalı.

**Yapılmaması gerekenler**
- Geri dönüşü olmayan bir adımda otomatik geçiş kurmayın.
- Ödeme veya onay adımını otomatik geçişe bağlamayın.
- Aynı testte otomatik geçiş ile adım sayısını birlikte değiştirmeyin.
- Otomatik geçişte girilen veriyi korumayan bir uygulama bırakmayın.
- Birden çok seçenek işaretlenebilen veya metin girilen adımda otomatik geçiş kurmayın; kullanıcı girişini bitirmeden ilerler.

### EN

Moving to the next step as soon as a choice is made removes one click and speeds up the flow. The cost: the user can’t review the choice, a wrong tap turns into irreversible progress and the sense of control is lost. How easy it is to go back is what decides it.

**What to test**
- Auto-advance: Does advancing automatically after a choice raise completion?
- Error: How often does a wrong choice lead to progress?
- Going back: How easy is it to go back, and is the data preserved?
- Delay: Does adding a short wait reduce errors?
- Device: Is a transition caused by a mistaken tap more frequent on mobile?

**KPIs to track**
- Flow Completion Rate: Does auto-advance raise completion?
- Back-Navigation Rate: Going back to the previous step must not increase.
- Wrong Choice Rate: Progress with a wrong choice must not increase.
- Task Completion Time (flow): Does the flow get faster?
- Accessibility Check: With auto-advance, focus must not stay on the old step and the transition must not go unannounced.

**What not to do**
- Don’t set up auto-advance on a step with no way back.
- Don’t tie the payment or confirmation step to auto-advance.
- Don’t change auto-advance and the number of steps in the same test.
- Don’t leave an implementation that doesn’t preserve data entered under auto-advance.
- Don’t set up auto-advance on a step where several options can be selected or text is entered; it moves on before the user finishes.

---
## Süreli kampanya duyurusunu site genelinde göstermek işe yarar mı?

Değişken: Site geneli kampanya duyuru şeridi · Fark: ekle

Etiket: id=ui-011 · mercek=Zamanlama · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does showing a time-limited campaign announcement across the site pay off?

EN-Variable: Site-wide campaign announcement bar

Belirli bir süre boyunca tüm sayfalarda görünen bir duyuru şeridi kampanyayı kaçırılmaz kılar. Riski: kullanıcılar reklam bandına benzeyen öğeleri görmezden gelmeyi öğrenmiştir, şerit her sayfada dikey alan yer ve süreklileşen bir duyuru bir süre sonra görünmez hâle gelir. (Kalıcı hizmet vaatlerini; kargo, iade, teslimat; sayfa üstünde göstermek ayrı bir senaryodur: `home-landing.md` → fayda çubuğu.)

**Test edilmesi gerekenler**
- Varlık: Site geneli duyuru kampanya aksiyonunu artırıyor mu?
- Kapsam: Tüm sayfalarda mı, yalnızca ilgili kategorilerde mi görünmeli?
- Kapatma: Şeridi kapatan kullanıcı, kampanya sayfasına başka bir yoldan yine de ulaşıyor mu?
- Körlük: Çubuk birkaç ziyaretten sonra fark edilmemeye mi başlıyor?
- Cihaz: Her sayfada dikey alan yiyen şerit, ürün listesini mobilde masaüstüne göre daha çok aşağı itip gezinmeyi yavaşlatıyor mu?

**Takip edilecek ana KPI’lar**
- Duyurulan Aksiyonun Tamamlanma Oranı: Çubuğun işaret ettiği eylem artıyor mu?
- Dönüşüm Oranı (CR): Sitenin ana dönüşümü düşmemeli.
- Çubuk Tıklama Oranı: Çubuk gerçekten tıklanıyor mu?
- Kapatma Oranı: Rahatsızlık sinyali olarak kapatma artmamalı.
- Sayfa Yüklenme Süresi: Her sayfaya eklenen şerit ana içeriğin yüklenmesini geciktirmemeli.

**Yapılmaması gerekenler**
- Kapatılamayan bir çubuk kurmayın.
- Aynı testte çubuğun varlığı ile içeriğini birlikte değiştirmeyin.
- Süresi dolunca gerçekten kalkmayan “süreli” kampanya duyurmayın; sayaç ve tarih gerçek olmalı.
- Çubuğu sabitleyip ekranın önemli bir kısmını kalıcı olarak kaplamayın.
- Şeridi ödeme adımında da gösterip kullanıcıyı siparişin ortasında kampanya sayfasına çekmeyin.

### EN

An announcement bar that shows on all pages for a set period makes the campaign hard to miss. The risk: users have learned to ignore elements that look like ad banners, the bar takes vertical space on every page and an announcement that becomes permanent turns invisible after a while. (Showing permanent service promises, such as shipping, returns and delivery, at the top of the page is a separate scenario: `home-landing.md` → benefit bar.)

**What to test**
- Presence: Does a site-wide announcement raise the campaign action?
- Scope: Should it show on all pages or only in the relevant categories?
- Dismissal: Does a user who closes the bar still reach the campaign page another way?
- Blindness: Does the bar start going unnoticed after a few visits?
- Device: Does a bar that eats vertical space on every page push the product list further down on mobile than on desktop and slow browsing?

**KPIs to track**
- Announced Action Completion Rate: Does the action the bar points to go up?
- Conversion Rate (CR): The site’s main conversion must not drop.
- Bar Click Rate: Is the bar actually clicked?
- Dismissal Rate: As a sign of annoyance, dismissals must not increase.
- Page Load Time: The bar added to every page must not delay loading of the main content.

**What not to do**
- Don’t set up a bar that can’t be dismissed.
- Don’t change the presence of the bar and its content in the same test.
- Don’t announce a “time-limited” campaign that doesn’t actually end when the time runs out; the counter and the date must be real.
- Don’t pin the bar and cover a large part of the screen permanently.
- Don’t show the bar in the payment step as well and pull the user to the campaign page in the middle of an order.

---
## Kampanya duyurusu hemen mi, bir süre sonra mı görünmeli?

Değişken: Kampanya şeridinin görünme anı · Fark: değiştir

Etiket: id=ui-012 · mercek=Zamanlama · düzey=görsel · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should a campaign announcement appear at once or after a delay?

EN-Variable: When the campaign bar appears

Çubuğun sayfa açılır açılmaz görünmesi mesajı herkese ulaştırır ama içerikle rekabet eder. Kaydırma sonrası veya birkaç saniye gecikmeyle belirmesi ise ziyaretçi bağlamı kurduktan sonra devreye girer; buna karşılık geç beliren bir öğe içeriği kaydırarak yanlış tıklamaya yol açabilir.

**Test edilmesi gerekenler**
- Zamanlama: Hemen mi, gecikmeli mi gösterim daha çok aksiyon getiriyor?
- Sonraki test: Gecikmeli gösterim kazanırsa, tetikleyici türü (süre / kaydırma derinliği) ayrı bir testte duyurulan aksiyonu değiştiriyor mu?
- Sayfa hareketi: Sonradan beliren çubuk içeriği kaydırıyor mu?
- Erişim: Gecikmeli kolda şeride hiç ulaşmadan ayrılan ziyaretçiler, kazanılan aksiyon artışını dengeliyor mu?
- Cihaz: Mobilde gecikmeli gösterim daha mı az rahatsız edici?

**Takip edilecek ana KPI’lar**
- Duyurulan Aksiyonun Tamamlanma Oranı: Zamanlama aksiyonu artırıyor mu?
- Çubuk Görülme Oranı: Çubuğu gören ziyaretçi oranı ne kadar?
- Yanlış Tıklama Oranı: Kayan içerik kaynaklı yanlış tıklama artmamalı.
- Dönüşüm Oranı (CR): Ana dönüşüm düşmemeli.
- Kapatma Oranı: Gecikmeli beliren şeridi okumadan kapatanların payı artmamalı.

**Yapılmaması gerekenler**
- Beliren çubuğun sayfa içeriğini kaydırmasına izin vermeyin; yer önceden ayrılmalıdır.
- Aynı testte zamanlama ile çubuk içeriğini birlikte değiştirmeyin.
- Aynı oturumda kapatılan çubuğu tekrar tekrar göstermeyin.
- Gecikmeli gösterimi kullanıcı bir aksiyona başladığı anda tetiklemeyin.
- Gecikmeli şeridi, ekran okuyucuya duyurulmadan veya klavye odağını üzerine çekerek belirecek biçimde kurmayın.

### EN

A bar that shows as soon as the page opens reaches everyone but competes with the content. One that appears after scrolling or a few seconds’ delay comes in once the visitor has built context; on the other hand, an element that appears late can shift the content and cause a misclick.

**What to test**
- Timing: Does immediate or delayed display bring more action?
- Next test: If delayed display wins, does the trigger type (time / scroll depth) change the announced action in a separate test?
- Page movement: Does a bar that appears later shift the content?
- Reach: Do visitors who leave the delayed arm without ever reaching the bar offset the gain in action?
- Device: Is delayed display less intrusive on mobile?

**KPIs to track**
- Announced Action Completion Rate: Does the timing raise the action?
- Bar View Rate: What share of visitors see the bar?
- Misclick Rate: Misclicks caused by shifting content must not increase.
- Conversion Rate (CR): The main conversion must not drop.
- Dismissal Rate: The share of those who close the late-appearing bar without reading it must not increase.

**What not to do**
- Don’t let the bar that appears shift the page content; the space must be reserved in advance.
- Don’t change the timing and the bar content in the same test.
- Don’t show a bar again and again that was dismissed in the same session.
- Don’t trigger the delayed display the moment the user starts an action.
- Don’t build the delayed bar so that it appears without being announced to the screen reader or by pulling keyboard focus onto it.

---
## Bildirim işaretini sayı olarak mı, nokta olarak mı göstermeli?

Değişken: Bildirim işaretinin biçimi · Fark: değiştir

Etiket: id=ui-013 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should a notification badge show a number or a dot?

EN-Variable: Format of the notification badge

Sayılı rozet ne kadar bekleyen iş olduğunu söyler ve aciliyeti ölçeklendirir. Sade bir nokta ise yalnızca “yeni bir şey var” der; daha az baskı yaratır ama bilgi vermez. Yüksek sayılar motive etmek yerine bunaltabilir, sıfırlanamayan bir rozet ise kalıcı bir rahatsızlığa dönüşür.

**Test edilmesi gerekenler**
- Biçim: Sayılı rozet mi, sade nokta mı daha çok tıklanıyor?
- Büyüklük: Yüksek sayılar caydırıcı hâle geliyor mu?
- Alışma: Sade nokta birkaç gün sonra görmezden gelinirken sayılı rozet daha uzun süre tıklanmaya devam ediyor mu?
- Cihaz: Mobilde küçük rozet fark ediliyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Teste atanan kullanıcılar içinde bekleyen işi (ör. okunmamış mesajı yanıtlama) tamamlayanların oranı artıyor mu?
- İlgili Bölüm Ziyaret Oranı: Tanı metriği; rozetin işaret ettiği bölüme giriş artıyor mu?
- Rozet Yoksayma Oranı: Sürekli görülüp tıklanmayan rozet oranı artmamalı.
- Tekrar Ziyaret Oranı: Bunaltan rozet, ilan edilen pencerede geri gelen kullanıcı oranını düşürmemeli.
- Erişilebilirlik: Rozet yalnızca renkle anlatılmamalı, ekran okuyucuya duyurusuz kalmamalı.

**Yapılmaması gerekenler**
- Karşılığı olmayan bir rozet göstermeyin; sahte bekleyen iş üretmeyin.
- Aynı testte rozet biçimi ile rozetin konumunu birlikte değiştirmeyin.
- Sıfırlanamayan, kullanıcının kapatamadığı bir rozet kurmayın.
- Rozeti yalnızca kırmızı renkle ayırt edilebilir bırakmayın.
- Sayılı rozette sayıyı, kullanıcı işi bitirdikten sonra da güncellenmeyen eski değerde bırakmayın.

### EN

A numbered badge says how much is pending and scales the urgency. A plain dot only says “there is something new”; it creates less pressure but gives no information. High numbers can overwhelm instead of motivating, and a badge that can’t be cleared turns into a permanent annoyance.

**What to test**
- Format: Is the numbered badge or the plain dot clicked more?
- Size: Do high numbers become a deterrent?
- Habituation: Is the plain dot ignored after a few days while the numbered badge keeps getting clicked for longer?
- Device: Is a small badge noticed on mobile?

**KPIs to track**
- Primary Action Completion Rate: Among users assigned to the test, does the share who complete the pending task (e.g. replying to an unread message) go up?
- Related Section Visit Rate: Diagnostic metric; does entry to the section the badge points to go up?
- Badge Ignore Rate: The share of badges that are constantly seen but not clicked must not increase.
- Return Visit Rate: An overwhelming badge must not lower the share of users who come back within the stated window.
- Accessibility Check: The badge must not be conveyed by color alone or go unannounced to the screen reader.

**What not to do**
- Don’t show a badge with nothing behind it; don’t manufacture fake pending work.
- Don’t change the badge format and the badge position in the same test.
- Don’t set up a badge that can’t be cleared or that the user can’t dismiss.
- Don’t leave the badge distinguishable by the color red alone.
- On a numbered badge, don’t leave the number at an old value that isn’t updated after the user finishes the task.

---
## Canlı destek düğmesi eklemek dönüşümü artırır mı?

Değişken: Canlı destek düğmesi · Fark: ekle

Etiket: id=ui-014 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does adding a live support button raise conversion?

EN-Variable: Live support button

Erişilebilir bir destek düğmesi tereddüt eden kullanıcıya çıkış yolu verir ve cevapsız kalan soruyu terke dönüşmeden yakalar. Bedeli: düğme ekranda yer kaplar, mobilde içeriği kapatabilir ve destek yükünü artırır. Ayrıca canlı destek gerçekten canlı değilse (yanıt gecikmesi) güveni düşürür.

**Test edilmesi gerekenler**
- Varlık: Destek düğmesi dönüşümü artırıyor mu?
- Yanıt süresi: Gelen taleplere yanıt süresi vaadi karşılıyor mu?
- Kapsam: Her sayfada mı, yalnızca tereddüt noktalarında mı görünmeli?
- Cihaz: Mobilde düğme içeriği veya ana butonu kapatıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Destek erişimi satışa dönüyor mu?
- Sohbet Başlatma Oranı: Düğme kullanılıyor mu?
- Destek Yanıt Süresi: Yanıt süresi vaat edilen seviyenin altına düşmemeli.
- Sepet Terk Oranı: Sorusu cevapsız kaldığı için sepeti bırakanlar azalıyor mu?
- Ana Buton Görünürlüğü: Destek düğmesi asıl aksiyonu kapatmamalı.

**Yapılmaması gerekenler**
- Destek ekibi hazır değilken canlı destek düğmesi açmayın; yanıtsız sohbet zarar verir.
- Aynı testte düğmenin varlığı ile konumunu birlikte değiştirmeyin.
- Düğmeyi ana aksiyon butonunun üzerine bindirmeyin.
- Sohbet başlatmadan kişisel bilgi zorunluluğu koymayın.
- Düğmeyi, klavyeyle ulaşılamayan veya ekran okuyucuda adsız kalan bir yüzen öğe olarak kurmayın.

### EN

An accessible support button gives a hesitating user a way out and catches an unanswered question before it turns into abandonment. The cost: the button takes screen space, can cover content on mobile and adds support load. Also, if live support isn’t really live (slow replies), it lowers trust.

**What to test**
- Presence: Does the support button raise conversion?
- Response time: Do replies to incoming requests meet the promised time?
- Scope: Should it show on every page or only at hesitation points?
- Device: On mobile, does the button cover content or the main button?

**KPIs to track**
- Conversion Rate (CR): Does access to support turn into sales?
- Chat Start Rate: Is the button used?
- Support Response Time: Response time must not fall below the promised level.
- Cart Abandonment Rate: Do fewer people leave the cart because their question went unanswered?
- Main Button Visibility: The support button must not cover the main action.

**What not to do**
- Don’t open a live support button when the support team isn’t ready; an unanswered chat does harm.
- Don’t change the presence and the position of the button in the same test.
- Don’t overlay the button on the main action button.
- Don’t require personal information before a chat can start.
- Don’t build the button as a floating element that can’t be reached by keyboard or has no name for the screen reader.

---
## Sohbet penceresini kendiliğinden açmak işe yarar mı?

Değişken: Sohbet penceresinin açılma biçimi · Fark: değiştir

Etiket: id=ui-015 · mercek=Zamanlama · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does opening the chat window automatically pay off?

EN-Variable: How the chat window opens

Kendiliğinden açılan sohbet penceresi yardımın varlığını duyurur ve pasif düğmeye göre çok daha fazla sohbet başlatır. Riski: davetsiz açılan bir pencere içeriği kapatır, kullanıcıyı böler ve rahatsızlık yaratır; gelen sohbetlerin niteliği de düşebilir çünkü kullanıcı yardım istemek yerine tepki vermiştir.

**Test edilmesi gerekenler**
- Açılma: Kendiliğinden açılma dönüşümü artırıyor mu?
- Sonraki test: Kendiliğinden açılma kazanırsa, tetikleyici (süre / belirli sayfa / duraksama) ayrı bir testte dönüşümü değiştiriyor mu?
- Nitelik: Gelen sohbetlerin niteliği düşüyor mu?
- Kapatma: Kapatan kullanıcı sonradan tekrar açıyor mu?
- Cihaz: Mobilde açılan pencere ekranın tamamını kapatıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Kendiliğinden açılma satışa dönüyor mu?
- Sohbet Başlatma Oranı: Sohbet sayısı artıyor mu?
- Nitelikli Sohbet Oranı: Anlamsız veya boş sohbet oranı artmamalı.
- Erişilebilirlik: Kendiliğinden açılan pencere klavye odağını çalmamalı, ekran okuyucuya duyurusuz açılmamalı.
- Destek Talebi: Ekibin taşıyabileceği talep seviyesi aşılmamalı.

**Yapılmaması gerekenler**
- Kapatılamayan veya kapatma düğmesi gizlenmiş bir pencere kurmayın.
- Kullanıcı bir form doldururken veya ödeme yaparken pencereyi açmayın.
- Aynı testte açılma davranışı ile karşılama mesajını birlikte değiştirmeyin.
- Kapatılan pencereyi aynı oturumda tekrar açmayın.
- Otomatik karşılama mesajını gerçek bir temsilci yazmış gibi gösterip otomatik olduğunu gizlemeyin.

> **Güncellik notu (2026-11):** Sohbet penceresinin arkasında artık çoğu zaman bir temsilci değil, yapay zekâ destekli bir asistan var: kendiliğinden açılan pencere anında cevap verebilir, ama yanlış ya da uydurma bir cevap kararı bozabilir. Bu senaryo pencerenin açılma biçimini test eder; asistan mı temsilci mi sorusu ayrı bir değişkendir ve iki kolda aynı kalır. Asistan kullanılıyorsa kullanıcıya yapay zekâyla konuştuğu açıkça söylenir ve temsilciye geçiş yolu açık kalır; bu birçok pazarda yasal bir yükümlülüktür, hedef pazarın kuralını doğrulayın.

### EN

A chat window that opens by itself announces that help exists and starts far more chats than a passive button. The risk: an uninvited window covers content, interrupts the user and annoys; the quality of incoming chats can also drop because the user reacted instead of asking for help.

**What to test**
- Opening: Does opening automatically raise conversion?
- Next test: If automatic opening wins, does the trigger (time / specific page / pause) change conversion in a separate test?
- Quality: Does the quality of incoming chats drop?
- Dismissal: Do users who close it reopen it later?
- Device: On mobile, does the window that opens cover the whole screen?

**KPIs to track**
- Conversion Rate (CR): Does automatic opening turn into sales?
- Chat Start Rate: Does the number of chats go up?
- Qualified Chat Rate: The share of meaningless or empty chats must not increase.
- Accessibility Check: The window that opens by itself must not steal keyboard focus or open without being announced to the screen reader.
- Support Contact Rate: Requests must not exceed what the team can handle.

**What not to do**
- Don’t build a window that can’t be closed or whose close button is hidden.
- Don’t open the window while the user is filling in a form or paying.
- Don’t change the opening behavior and the welcome message in the same test.
- Don’t reopen a window that was closed in the same session.
- Don’t present the automatic welcome message as if a real agent wrote it and hide that it is automated.

> **Freshness note (2026-11):** Behind the chat window there is now often not an agent but an AI-powered assistant: a window that opens by itself can answer instantly, but a wrong or made-up answer can spoil the decision. This scenario tests how the window opens; assistant versus agent is a separate variable and stays the same in both arms. If an assistant is used, the user is told plainly that they are talking to an AI and the route to a human agent stays open; in many markets this is a legal obligation, so verify the rule of the target market.

---
## Bilgiyi tablo olarak mı, kutular hâlinde mi sunmalı?

Değişken: Karşılaştırma bilgisinin sunum biçimi · Fark: değiştir

Etiket: id=ui-016 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Present information as a table or as cards?

EN-Variable: Presentation format of comparison information

Tablo satır ve sütun mantığıyla doğrudan karşılaştırma kurar; çok sayıda özelliği yan yana koymak gerektiğinde en verimli biçimdir. Kutular her seçeneği bağımsız bir teklif gibi gösterir ve tarama kolaylığı sağlar ama farkların bulunmasını zorlaştırır. Yatay ve dikey yönelim de aynı içeriği farklı okutur.

**Test edilmesi gerekenler**
- Biçim: Tablo mu, kutu mu, madde listesi mi daha çok aksiyon getiriyor?
- Sonraki test: Kazanan biçim sabitken düzenin yönelimi (yatay / dikey) ayrı bir testte okunabilirliği değiştiriyor mu?
- İçerik yoğunluğu: Çok özellikli sayfalarda tablonun kutulara karşı üstünlüğü, az özellikli sayfalara göre büyüyor mu?
- Farkların bulunması: Kullanıcı seçenekler arası farkı bulabiliyor mu?
- Cihaz: Mobilde tablo yatay kaydırmaya düşüyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Sunum biçimi seçim yapmayı artırıyor mu?
- Karşılaştırma Etkileşim Oranı: İçerik gerçekten inceleniyor mu?
- Karar Süresi: Seçim süresi kabul edilemez ölçüde uzamamalı.
- İade veya İptal Oranı (30 gün): Farkları bulamayıp yanlış seçeneği alanların iade veya iptali artmamalı.
- Erişilebilirlik: Tablo yapısı ekran okuyucuda anlamsız hâle gelmemeli.

**Yapılmaması gerekenler**
- Aynı testte sunum biçimi ile karşılaştırılan içeriği birlikte değiştirmeyin.
- Düzen amaçlı tabloyu semantik tablo olarak işaretlemeyin veya tersini yapmayın.
- Mobilde tabloyu okunmaz derecede küçültüp kutu düzeniyle karşılaştırmayın.
- Kutu düzeninde farkları yalnızca sıralamayla ima edip yazılı olarak vermemezlik etmeyin.
- Tabloda bir seçeneğin olumsuz satırını (ör. ek ücret) silik biçimlendirip gizlemeyin.

> **Not:** Fiyat planlarının tablo/kart karşılaştırması `pricing.md` → “Planları karşılaştırma tablosunda mı, ayrı kartlarda mı sunmalı?” senaryosunun konusudur; fiyat sayfası için bu senaryoyu değil onu kullanın.

### EN

A table builds a direct comparison through rows and columns; it is the most efficient format when many features have to sit side by side. Cards show each option as an independent offer and make scanning easy but make differences harder to find. Horizontal and vertical orientation also make the same content read differently.

**What to test**
- Format: Does a table, cards or a bullet list bring more action?
- Next test: With the winning format fixed, does the layout orientation (horizontal / vertical) change readability in a separate test?
- Content density: On pages with many features, does the table’s edge over cards grow compared with pages with few features?
- Finding differences: Can the user spot the differences between options?
- Device: Does the table fall back to horizontal scrolling on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does the presentation format raise choosing?
- Comparison Engagement Rate: Is the content actually examined?
- Time to Decision: Time to choose must not lengthen unacceptably.
- Return or Cancellation Rate (30 days): Returns or cancellations by those who couldn’t find the differences and took the wrong option must not increase.
- Accessibility Check: The table structure must not become meaningless to a screen reader.

**What not to do**
- Don’t change the presentation format and the compared content in the same test.
- Don’t mark a layout table as a semantic table or the reverse.
- Don’t shrink the table on mobile until it is unreadable and then compare it with the card layout.
- In the card layout, don’t only hint at the differences through ordering instead of stating them in writing.
- In the table, don’t hide an option’s negative row (e.g. an extra fee) by styling it faintly.

> **Note:** The table-versus-card comparison of pricing plans is the subject of the “Should plans be shown in a comparison table or on separate cards?” scenario in `pricing.md`; for a pricing page use that one, not this one.

---
## Buton metnini komut kipiyle mi (“Başlat”), birinci şahıs bildirimiyle mi (“Başlıyorum”) yazmalı?

Değişken: Buton metninin kipi · Fark: değiştir

Etiket: id=ui-017 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should button copy be a command (“Start”) or a first-person statement (“I’m starting”)?

EN-Variable: Grammatical mood of the button copy

Bir CTA’nın emir kipiyle mi (“Başlat”), yoksa kullanıcının kendi ağzından söylediği birinci şahıs bildirimiyle mi (“Başlıyorum”) yazıldığı, kararı kimin verdiği hissini değiştirebilir; emir kipi siteden gelen bir talimat gibi okunurken, birinci şahıs ifade kullanıcının kendi kararını onayladığı bir cümle gibi okunur. Etkisi küçük ama tutarlı bir mikro-copy farkıdır; markanın genel ses tonuyla uyumlu olmayan bir kalıp tuhaf durabilir. “Buton metni eylemi mi, kazanılan şeyi mi söylemeli?” senaryosundan farkı: o senaryo metnin içeriğini (eylem mi kazanç mı), bu senaryo aynı içeriğin dilbilgisel kipini değiştirir.

**Test edilmesi gerekenler**
- Kip: Emir kipi mi, birinci şahıs bildirimi mi tıklama oranını artırıyor?
- Bağlam: Etki ücretsiz/düşük riskli aksiyonlarda mı, ücretli/yüksek riskli aksiyonlarda mı daha güçlü?
- Ton tutarlılığı: Marka sesi resmi olduğunda birinci şahıs ifade garip mi duruyor?
- Uzunluk: Birinci şahıs ifade buton genişliğini büyütüp mobilde sıkışıklık mı yaratıyor?
- Segment: Yeni ziyaretçi ile daha önce siteyi kullanmış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Buton metni, tıklamadan sonraki adımın tamamlanmasını artırıyor mu?
- Tıklama Oranı (CTR): Tanı metriği; buton metni tıklamayı artırıyor mu?
- Marka Algısı (anket): İfade markayı samimiyetsiz veya tuhaf hissettirmemeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Destek Talebi: “Yanlışlıkla başlattım” türü talepler artmamalı; ifade, verilmemiş bir kararı verilmiş gibi göstermemeli.
- Tekrar Ziyaret Oranı: Kısa vadeli tıklama artışı uğruna marka algısı zedelenmemeli.

**Yapılmaması gerekenler**
- Aynı testte buton metninin kipini ve rengini veya boyutunu birlikte değiştirmeyin.
- Birinci şahıs ifadeyi, kullanıcının henüz vermediği bir kararı vermiş gibi göstermek için kullanmayın; ücretli bir işlemde onay adımı hâlâ ayrıca gösterilmeli.
- Marka sesi ile tutarsız bir kip seçip sayfanın geri kalanıyla çelişen bir ton yaratmayın.
- Farklı butonlarda farklı kipler kullanıp sayfa içi tutarlılığı bozmayın.
- Birinci şahıs kipi reddetme butonunda (“Hayır, indirim istemiyorum”) kullanıcıyı suçlayan bir ifadeye çevirmeyin.

### EN

Whether a CTA is written in the imperative (“Start”) or as a first-person statement in the user’s own voice (“I’m starting”) can change the feeling of who made the decision; the imperative reads like an instruction from the site, while the first-person phrase reads like a sentence in which the user confirms their own decision. The effect is a small but consistent micro-copy difference; a form that doesn’t fit the brand’s overall tone can feel odd. How it differs from the “Should button copy say the action or what you get?” scenario: that one changes the content of the text (action or benefit), this one changes the grammatical mood of the same content.

**What to test**
- Mood: Does the imperative or the first-person statement raise the click rate?
- Context: Is the effect stronger for free or low-risk actions, or for paid or high-risk ones?
- Tone consistency: When the brand voice is formal, does the first-person phrase look awkward?
- Length: Does the first-person phrase widen the button and cause crowding on mobile?
- Segment: Do new visitors and users who have used the site before react differently?

**KPIs to track**
- Conversion Rate (CR): Does the button copy raise completion of the step after the click?
- Click-Through Rate (CTR): Diagnostic metric; does the button copy raise clicks?
- Brand Perception (survey): The wording must not make the brand feel insincere or odd. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Support Contact Rate: “I started it by mistake” requests must not increase; the wording must not present a decision that hasn’t been made as made.
- Return Visit Rate: Brand perception must not be damaged for the sake of a short-term click gain.

**What not to do**
- Don’t change the mood of the button copy together with its color or size in the same test.
- Don’t use the first-person phrase to present a decision the user hasn’t made yet as made; for a paid action the confirmation step must still be shown separately.
- Don’t choose a mood that is inconsistent with the brand voice and create a tone that clashes with the rest of the page.
- Don’t use different moods on different buttons and break consistency within the page.
- On a decline button (“No, I don’t want the discount”), don’t turn the first-person mood into a phrase that blames the user.

---
## İç promosyon banner’ı tek bir motivasyona mı, birden fazla seçeneğe mi odaklanmalı?

Değişken: Promosyon banner’ının mesaj odağı · Fark: değiştir

Etiket: id=ui-018 · mercek=Netlik · düzey=metin · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should an internal promo banner focus on one motivation or on several options?

EN-Variable: Message focus of the promo banner

Bir sitenin herhangi bir noktasındaki tanıtım banner’ı genellikle birden fazla fayda veya seçeneği aynı anda listeler (“Ücretsiz kargo, yeni koleksiyon, üyelik avantajları”). Banner’ı tek bir net motivasyona kilitlemek (yalnızca “Bugüne özel: ilk siparişte %15”) mesajı netleştirebilir ama diğer tekliflerin görünürlüğünü tamamen kaybettirebilir. Bu, “Süreli kampanya duyurusunu site genelinde göstermek işe yarar mı?” senaryosundan farklıdır: o senaryo banner’ın var olup olmamasını ve zamanlamasını, bu senaryo banner içeriğinin tek mi çok mu odaklı olacağını test eder.

**Test edilmesi gerekenler**
- Odak: Tek motivasyona kilitli banner çok seçenekli olana göre daha mı çok tıklanıyor?
- İçerik kaybı: Banner’dan çıkarılan diğer teklifler başka bir yerde fark ediliyor mu?
- Görsel hizalama: Banner’ın görseli ve metni aynı tek motivasyonu mu anlatıyor?
- Sonraki test: Tek odak kazanırsa, seçilen motivasyon (fiyat / yenilik / ayrıcalık) ayrı bir testte tıklamayı değiştiriyor mu?
- Segment: Yeni ziyaretçi ile mevcut müşteri aynı motivasyona mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Duyurulan Aksiyonun Tamamlanma Oranı: Banner’ın çağırdığı hedef aksiyonu tamamlayan atanan ziyaretçi oranı (banner’a tıklayanlar değil) artıyor mu?
- Banner Tıklama Oranı: Tanı metriği; tek odaklı banner tıklamayı artırıyor mu?
- Dönüşüm Oranı (CR): Banner odağı sitenin ana dönüşümünü düşürmemeli.
- Kaybolan Teklif Farkındalığı (anket): Banner’dan çıkarılan diğer tekliflerin bilinirliği kabul edilemez ölçüde düşmemeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Brüt Marj: Tek mesaj indirime kilitlenince indirimli sipariş payı marjı eritmemeli.

**Yapılmaması gerekenler**
- Aynı testte banner’ın odağı ile konumunu/boyutunu birlikte değiştirmeyin.
- Gerçekte sınırlı olmayan bir teklifi “bugüne özel” gibi göstermeyin.
- Çıkarılan diğer teklifleri sitenin hiçbir yerinde göstermeyip tamamen kaybettirmeyin; en azından ilgili sayfada bulunabilir olmalılar.
- Tek motivasyonlu banner’ı, vaat ettiği teklifin geçerli olmadığı bir ürün veya kategori sayfasına bağlamayın.
- Tek motivasyonu, aslında farklı ziyaretçi segmentlerine göre değişmesi gereken bir mesajı zorla tekleştirmek için kullanmayın.

### EN

A promo banner anywhere on a site often lists several benefits or options at once (“Free shipping, new collection, membership perks”). Locking the banner to a single clear motivation (only “Today only: 15% off your first order”) can sharpen the message but can make the other offers lose their visibility altogether. This differs from the “Does showing a time-limited campaign announcement across the site pay off?” scenario: that one tests whether the banner exists and its timing, this one tests whether the banner content is single-focus or multi-focus.

**What to test**
- Focus: Is a banner locked to one motivation clicked more than a multi-option one?
- Lost content: Are the other offers removed from the banner noticed elsewhere?
- Visual alignment: Do the banner’s image and text tell the same single motivation?
- Next test: If the single focus wins, does the chosen motivation (price / novelty / privilege) change clicks in a separate test?
- Segment: Do new visitors and existing customers respond to the same motivation?

**KPIs to track**
- Announced Action Completion Rate: Does the share of assigned visitors who complete the target action the banner calls for (not those who clicked the banner) go up?
- Banner Click Rate: Diagnostic metric; does the single-focus banner raise clicks?
- Conversion Rate (CR): The banner focus must not lower the site’s main conversion.
- Lost-Offer Awareness (survey): Awareness of the other offers removed from the banner must not drop unacceptably. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Gross Margin: When a single message locks onto a discount, the share of discounted orders must not erode the margin.

**What not to do**
- Don’t change the banner’s focus and its position or size in the same test.
- Don’t present an offer that isn’t actually limited as “today only”.
- Don’t drop the removed offers from every place on the site; they must at least be findable on the relevant page.
- Don’t link the single-motivation banner to a product or category page where the offer it promises doesn’t apply.
- Don’t use the single motivation to force into one a message that should actually vary by visitor segment.

---
## Birden fazla seçenek arasından birini görsel ağırlıkla öne çıkarmak seçimi hızlandırır mı?

Değişken: Seçeneklerden birine verilen görsel ağırlık · Fark: değiştir

Etiket: id=ui-019 · mercek=Çaba · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does giving one of several options more visual weight speed up the choice?

EN-Variable: Visual weight given to one of the options

Kullanıcıya birden fazla eşdeğer seçenek (ör. ürün varyantı, özellik kartı, indirilecek kaynak) sunulduğunda hepsini aynı görsel ağırlıkta göstermek nötr durur ama karar yükünü tamamen kullanıcıya bırakır. Seçeneklerden birini boyut, renk veya konumla diğerlerinden görünür biçimde ağır göstermek seçimi hızlandırabilir; riski, öne çıkarılan seçeneğin gerçekten çoğunluğun ihtiyacına uymamasıdır; bu durumda ağırlık seçimi değil yalnızca tıklamayı yönlendirmiş olur. Bu, `pricing.md`’deki plan sırası veya “en popüler” rozeti senaryolarından farklıdır: onlar fiyat planlarına özgüdür, bu senaryo fiyat içermeyen herhangi bir çoklu seçenek sunumuna uygulanır.

**Test edilmesi gerekenler**
- Ağırlık: Bir seçeneği görsel olarak öne çıkarmak toplam seçim hızını artırıyor mu?
- Doğruluk: Öne çıkarılan seçenek gerçekten çoğunluğun tercih ettiği mi?
- Sonraki test: Öne çıkarma kazanırsa, ağırlık yöntemi (boyut / renk / konum) ayrı bir testte seçim hızını değiştiriyor mu?
- Pişmanlık: Öne çıkarılanı seçenlerin sonradan değiştirme oranı yükseliyor mu?
- Segment: Deneyimli kullanıcı ile ilk kez gelen ziyaretçi ağırlığa aynı tepkiyi mi veriyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Seçim ekranına atanan ziyaretçilerin seçimi yapıp akışı tamamlama oranı artıyor mu?
- Seçim Tamamlama Süresi: Tanı metriği; görsel ağırlık karar süresini kısaltıyor mu?
- Seçim Sonrası Değiştirme/İptal Oranı (30 gün): Öne çıkarılan seçeneği alanların vazgeçme oranı artmamalı.
- Diğer Seçeneklerin Görülme Oranı: Öne çıkarılmayan seçenekler tamamen gözden kaçmamalı.
- Memnuniyet (anket): Seçim sonrası memnuniyet öne çıkarma nedeniyle düşmemeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.

**Yapılmaması gerekenler**
- Gerçek veriye dayanmayan bir seçeneği “en çok tercih edilen” gibi göstermeyin.
- Aynı testte ağırlık yöntemini (boyut/renk/konum) ve seçeneklerin içeriğini birlikte değiştirmeyin.
- Diğer seçenekleri tıklanamayacak veya bulunamayacak kadar küçültmeyin.
- Öne çıkarma ağırlığını kullanıcıyı gerçek ihtiyacından farklı bir seçeneğe yönlendirmek için kullanmayın.
- Mobilde öne çıkarılan seçeneği büyütürken diğerlerini ekran dışına taşırmayın.

### EN

When a user is shown several equivalent options (e.g. a product variant, a feature card, a resource to download), showing them all at the same visual weight looks neutral but leaves the whole decision load on the user. Making one option visibly heavier than the others through size, color or position can speed up the choice; the risk is that the highlighted option doesn’t actually fit most people’s need, in which case the weight has steered only the click, not the choice. This differs from the plan order or “most popular” badge scenarios in `pricing.md`: those are specific to pricing plans, while this scenario applies to any multi-option presentation without prices.

**What to test**
- Weight: Does visually highlighting one option raise overall choice speed?
- Accuracy: Is the highlighted option really the one most people prefer?
- Next test: If highlighting wins, does the weighting method (size / color / position) change choice speed in a separate test?
- Regret: Does the rate at which those who chose the highlighted option change it later go up?
- Segment: Do experienced users and first-time visitors react to the weight the same way?

**KPIs to track**
- Conversion Rate (CR): Does the share of visitors assigned to the choice screen who make a choice and complete the flow go up?
- Choice Completion Time: Diagnostic metric; does the visual weight shorten decision time?
- Post-Choice Change or Cancellation Rate (30 days): The rate at which those who took the highlighted option back out must not increase.
- Other-Option View Rate: The options that aren’t highlighted must not go completely unseen.
- Satisfaction (survey): Post-choice satisfaction must not drop because of the highlight. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.

**What not to do**
- Don’t present an option that isn’t based on real data as “most preferred”.
- Don’t change the weighting method (size/color/position) and the content of the options in the same test.
- Don’t shrink the other options until they can’t be clicked or found.
- Don’t use the highlight weight to steer the user toward an option different from their real need.
- On mobile, when enlarging the highlighted option, don’t push the others off screen.
