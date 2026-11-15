# Form ve kayıt akışı

Yolculuk aşaması: bir formun doldurulmaya başlanmasından gönderilmesine kadar geçen her şey. Alan sayısı, adım sayısı ve zorunlu/isteğe bağlı işaretlemesi bu dosyada değil, ilgili bağlam dosyalarındadır (checkout için `cart-checkout.md`, lead formu için `saas-b2b.md`); burada formun kendi tasarımı ve giriş/kayıt yöntemi ele alınır. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Etiketler alanın üstünde mi, solunda mı durmalı?

Değişken: Alan etiketinin konumu · Fark: taşı

Etiket: id=fs-001 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should field labels sit above the field or to its left?

EN-Variable: Field label position

Sola hizalı etiket dikeyde yer kazandırır ama gözün her alanda yatay sıçrama yapmasını gerektirir. Üst hizalı etiket tek bir dikey tarama hattı oluşturur, buna karşılık form daha uzun görünür. Uzun etiketli veya çok dilli formlarda sola hizalama alan genişliğini de daraltır.

**Test edilmesi gerekenler**
- Konum: Etiket alanın üstünde mi, solunda mı daha hızlı doldurtuyor?
- Tarama: Üst hizalı etiket tek sütunlu dikey akışı bozmadan okunuyor mu?
- Uzun metin: Sola hizalı etikette uzun etiketler giriş alanını daraltıyor mu?
- Algılanan uzunluk: Üst hizalama formu gözle daha uzun gösterip başlamayı caydırıyor mu?
- Cihaz: Mobilde ve masaüstünde aynı hizalama mı kazanıyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Hizalama gönderime kadar gidenleri artırıyor mu?
- Form Başlama Oranı: İlk alana dokunan kullanıcı oranı değişiyor mu?
- Ortalama Doldurma Süresi: Hizalama doldurmayı hızlandırıyor mu?
- Alan Bazlı Hata Oranı: Yanlış alana yazma artmamalı.
- Erişilebilirlik: Ekran okuyucuda etiket ile alanın eşleşmesi bozulmamalı.

**Yapılmaması gerekenler**
- Aynı testte hizalama ile alan sayısını birlikte değiştirmeyin.
- Etiketi görsel olarak taşırken `label` bağlantısını koparmayın; hizalama bir CSS kararıdır, semantik değil.
- Sola hizalamada etiketi kırpıp üç nokta koymayın; okunmayan etiket hizalama testini geçersizleştirir.
- Masaüstünde kazandı diye mobil düzeni de aynı yapıp testi kapatmayın.
- Çok dilli sitede tek dilde ölçüp sonucu etiket uzunluğu farklı dillere genellemeyin.

### EN

A left-aligned label saves vertical space but forces the eye to jump sideways at every field. A top-aligned label creates a single vertical scan line, though the form looks longer. With long labels or multilingual forms, left alignment also narrows the input.

**What to test**
- Position: Does a label above or to the left of the field get the form filled faster?
- Scanning: Does a top-aligned label read cleanly without breaking the single-column vertical flow?
- Long text: With left-aligned labels, do long labels squeeze the input field?
- Perceived length: Does top alignment make the form look longer and put people off starting?
- Device: Does the same alignment win on mobile and on desktop?

**KPIs to track**
- Form Completion Rate: Does the alignment get more people through to submission?
- Form Start Rate: Does the share of users who touch the first field change?
- Median Form Fill Time: Does the alignment speed up filling?
- Field-Level Error Rate: Typing into the wrong field must not increase.
- Accessibility Check: The label-to-field association for screen readers must not break.

**What not to do**
- Don’t change the alignment and the number of fields in the same test.
- When moving the label visually, don’t break the `label` association; alignment is a CSS decision, not a semantic one.
- Don’t truncate the label with an ellipsis in left alignment; an unreadable label invalidates the alignment test.
- Don’t apply the desktop winner to mobile and close the test.
- Don’t measure in one language on a multilingual site and generalize the result to languages with different label lengths.

---

## Yüzen etiket doldurmayı kolaylaştırıyor mu?

Değişken: Alan etiketinin tipi (sabit, yüzen) · Fark: değiştir

Etiket: id=fs-002 · mercek=Netlik · düzey=form · sektör=genel · pazar=global · emek=orta · durum=klasik · tarih=2026-11

EN: Do floating labels make forms easier to fill in?

EN-Variable: Field label type (fixed, floating)

Yüzen etiket (alanın içinde başlayıp yazmaya başlayınca üste kayan etiket) yer kazandırır ve form kısa görünür. Ancak boş haldeyken etiketi placeholder’dan ayırt etmek zorlaşır, kullanıcı alana tıklamadan ne isteneceğini kestiremeyebilir. Otomatik doldurma ile de çakışabilir.

**Test edilmesi gerekenler**
- Anlaşılırlık: Boş haldeyken kullanıcı alanın ne istediğini anlıyor mu?
- Yer kazancı: Kısalan form başlama oranını artırıyor mu?
- Otomatik doldurma: Tarayıcı alanı doldurduğunda etiket doğru konuma geçiyor mu?
- Hata durumu: Hata mesajı yüzen etiketle çakışıyor mu?
- Cihaz: Mobil klavye açıkken etiket görünür kalıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Yüzen etiket gönderimi artırıyor mu?
- Alan Bazlı Hata Oranı: Yanlış format girişi artmamalı.
- Ortalama Doldurma Süresi: Etiketi anlamak için harcanan süre uzamamalı.
- Alan Bazlı Terk Oranı: Belirli bir alanda bırakma artıyor mu?
- Erişilebilirlik: Etiket kontrastı ve ekran okuyucu okuması bozulmamalı.

**Yapılmaması gerekenler**
- Etiketi tamamen placeholder’a çevirip kaldırmayın; bu ayrı ve daha riskli bir değişikliktir.
- Aynı testte etiket tipini değiştirirken alan yüksekliğini veya yardım metnini de değiştirmeyin.
- Yüzen etiketi, alan boşken placeholder ile aynı renk ve boyutta bırakıp ikisini ayırt edilemez hâle getirmeyin.
- Otomatik doldurma davranışını test aracıyla bastırmayın; gerçek kullanımda çalışan hâli ölçülmelidir.
- Hareket azaltma tercihini yok sayan bir geçiş animasyonu koymayın.

### EN

A floating label (it starts inside the field and slides up once typing begins) saves space and makes the form look short. But when the field is empty it is hard to tell the label from a placeholder, and users may not know what is being asked before they click in. It can also clash with autofill.

**What to test**
- Clarity: When the field is empty, does the user understand what it asks for?
- Space saving: Does the shorter form raise the start rate?
- Autofill: When the browser fills the field, does the label move to the right position?
- Error state: Does the error message collide with the floating label?
- Device: Does the label stay visible when the mobile keyboard is open?

**KPIs to track**
- Form Completion Rate: Does the floating label raise submissions?
- Field-Level Error Rate: Wrong-format entries must not increase.
- Median Form Fill Time: The time spent figuring out the label must not grow.
- Field-Level Abandonment Rate: Does dropout increase at a particular field?
- Accessibility Check: Label contrast and screen-reader output must not degrade.

**What not to do**
- Don’t turn the label into a placeholder and remove it altogether; that is a separate and riskier change.
- Don’t change the field height or the help text in the same test as the label type.
- Don’t leave the floating label the same color and size as the placeholder when the field is empty, so the two are indistinguishable.
- Don’t suppress autofill behavior with the testing tool; the version that works in real use must be measured.
- Don’t add a transition animation that ignores the reduced-motion preference.

---

## Form alanlarını tek sütuna almak tamamlamayı artırır mı?

Değişken: Form sütun sayısı · Fark: değiştir

Etiket: id=fs-003 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does putting form fields in a single column raise completion?

EN-Variable: Number of form columns

İki sütunlu form ekranda kısa görünür ama gözün zikzak çizmesini gerektirir ve bir sütunu tamamen atlama riski yaratır. Tek sütun daha uzun görünür, buna karşılık sıra belirsizliği ortadan kalkar. Birlikte anlam taşıyan alanlarda (il/ilçe, ad/soyad) yan yana dizilim savunulabilir.

**Test edilmesi gerekenler**
- Düzen: Tek sütun mu iki sütun mu daha yüksek tamamlama veriyor?
- Atlama: İki sütunda sağdaki alanlar daha sık boş mu kalıyor?
- İstisna: Ad/soyad gibi ilişkili alanlar yan yana kalırsa sonuç değişiyor mu?
- Algılanan uzunluk: Tek sütunun uzunluğu başlamayı caydırıyor mu?
- Cihaz: Masaüstündeki kazanç mobilde de geçerli mi?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Düzen gönderimi artırıyor mu?
- Boş Bırakılan Alan Sayısı (gönderilen form başına ortalama): Atlanan alan sayısı artmamalı.
- Ortalama Doldurma Süresi: Tek sütun doldurmayı yavaşlatıyor mu?
- Form Başlama Oranı: Uzayan form ilk dokunuşu azaltıyor mu?
- Doğrulama Hatası Oranı: Gönderimde geri dönen hata sayısı artmamalı.

**Yapılmaması gerekenler**
- Aynı testte düzen ile alan sırasını birlikte değiştirmeyin.
- Mobilde zaten tek sütuna düşen bir formu iki sütunlu varyantla test etmeye çalışmayın; orada değişiklik yoktur.
- Sütun sayısını değiştirirken alan genişliğini de değiştirmeyin.
- İlişkili alanları bölerken sekme sırasını bozmayın.
- Sonucu farklı uzunluktaki formlara genellemeyin; üç alanlı formla on iki alanlı form aynı davranmaz.

### EN

A two-column form looks short on screen but makes the eye zigzag and risks a column being skipped entirely. A single column looks longer, though it removes any doubt about order. For fields that carry meaning together (city/district, first/last name), side-by-side placement is defensible.

**What to test**
- Layout: Does a single column or two columns give higher completion?
- Skipping: In two columns, are the right-hand fields left empty more often?
- Exception: Does the result change if related fields such as first and last name stay side by side?
- Perceived length: Does the length of the single column discourage starting?
- Device: Does the desktop gain also hold on mobile?

**KPIs to track**
- Form Completion Rate: Does the layout raise submissions?
- Blank Fields per Submitted Form (average): The number of skipped fields must not increase.
- Median Form Fill Time: Does the single column slow filling down?
- Form Start Rate: Does the longer form reduce first touches?
- Validation Error Rate: The number of errors returned at submission must not increase.

**What not to do**
- Don’t change the layout and the field order in the same test.
- Don’t test a two-column variant on a form that already collapses to one column on mobile; there is no change there.
- Don’t change the field width while changing the column count.
- When splitting related fields, don’t break the tab order.
- Don’t generalize the result to forms of other lengths; a three-field form and a twelve-field form don’t behave the same way.

---

## En kolay alanı başa koymak formu tamamlatır mı?

Değişken: Kolay alanların formdaki sırası · Fark: taşı

Etiket: id=fs-004 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does putting the easiest field first get the form completed?

EN-Variable: Position of the easy fields in the form

Formu doldurmaya başlayan kullanıcının bitirme olasılığı artar. Bu nedenle ilk alanın düşünmeyi değil refleksi tetiklemesi (ad, e-posta) tamamlamayı artırabilir. Karşı argüman: kolay alanları öne almak zor alanları sona yığar ve terk noktasını öteler, toplam tamamlama değişmez.

**Test edilmesi gerekenler**
- Sıra: Kolay alanlar başa alındığında tamamlama artıyor mu?
- Terk noktası: Terk yalnızca formun sonuna mı kayıyor, gerçekten azalıyor mu?
- Mantıksal akış: Sıra değişince form anlam bütünlüğünü kaybediyor mu?
- Zor alan: Zorlanılan alan sonda tek başına kaldığında daha mı çok bırakılıyor?
- Segment: Yeni ziyaretçi ile geri dönen kullanıcı sıraya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Sıra değişikliği gönderimi artırıyor mu?
- Form Başlama Oranı: İlk alana dokunma artıyor mu?
- Alan Bazlı Terk Oranı: Terk başka bir alana kaymamalı, azalmalı.
- Ortalama Doldurma Süresi: Toplam süre uzamamalı.
- Gönderim Kalitesi: Hızlı başlayan kullanıcı geçersiz veri bırakmamalı.

**Yapılmaması gerekenler**
- Sıra değiştirirken alan çıkarmayın veya eklemeyin.
- Zor alanı sona taşırken neden istendiğini açıklayan metni kaldırmayın.
- Yasal olarak belirli bir sırada sunulması gereken alanları (onay metinleri) taşımayın.
- Sıralamayı kullanıcıya mantıksız gelecek şekilde bozmayın (şehirden önce mahalle sormak gibi).
- Aynı testte alan sırasıyla birlikte alan etiketlerini veya yardım metinlerini değiştirmeyin.

### EN

A user who has started a form is more likely to finish it. So a first field that triggers reflex rather than thought (name, email) can raise completion. The counter-argument: moving easy fields up piles the hard ones at the end and just shifts the abandonment point, leaving total completion unchanged.

**What to test**
- Order: Does completion rise when easy fields come first?
- Abandonment point: Does abandonment merely shift to the end of the form, or does it really fall?
- Logical flow: Does the form lose coherence when the order changes?
- Hard field: Is the hard field abandoned more when it is left alone at the end?
- Segment: Do new visitors and returning users react differently to the order?

**KPIs to track**
- Form Completion Rate: Does the reordering raise submissions?
- Form Start Rate: Do touches on the first field increase?
- Field-Level Abandonment Rate: Abandonment must fall, not just move to another field.
- Median Form Fill Time: Total time must not grow.
- Submission Quality: Users who start fast must not leave invalid data.

**What not to do**
- Don’t remove or add fields while changing the order.
- When moving the hard field to the end, don’t remove the text that explains why it is asked.
- Don’t move fields that must legally appear in a set order (consent texts).
- Don’t scramble the order in a way that feels illogical to the user (such as asking for the neighborhood before the city).
- Don’t change field labels or help texts in the same test as the field order.

---

## Alanları baştan göstermek mi, kademeli açmak mı daha çok tamamlatıyor?

Değişken: Form alanlarının açılma biçimi · Fark: değiştir

Etiket: id=fs-005 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Show all fields up front or reveal them step by step: which gets more forms completed?

EN-Variable: How form fields are revealed

Tüm alanları baştan göstermek beklentiyi netleştirir ama form uzun görünür. Kademeli açma (bir alan doldurulunca sonrakinin belirmesi, ya da isteğe bağlı bir bölümün bir bağlantıyla açılması) algılanan uzunluğu düşürür. Riski: kullanıcı formun ne kadar süreceğini bilemez ve gizlenen alan sürpriz gibi gelir.

**Test edilmesi gerekenler**
- Görünürlük: Alanlar baştan mı görünmeli, doldurdukça mı açılmalı?
- Beklenti: Kaç adım kaldığı belirsizleşince terk artıyor mu?
- Doluluk: Kademeli açmada isteğe bağlı alanların doldurulma oranı ne kadar düşüyor?
- Cihaz: Küçük ekranda kademeli açma daha mı çok fayda veriyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Kademeli açma gönderimi artırıyor mu?
- Form Başlama Oranı: Kısalan form ilk dokunuşu artırıyor mu?
- Alan Doldurma Oranı: Toplanan veri kalitesi kabul edilemez seviyeye düşmemeli.
- Ortalama Doldurma Süresi: Açılıp kapanan bölümler süreyi uzatmamalı.
- Alan Bazlı Terk Oranı: Beliren alanda ani bırakma olmamalı.

**Yapılmaması gerekenler**
- Zorunlu bir alanı kademeli açmanın arkasına gizlemeyin; kullanıcı ne isteneceğini bilmeden başlamamalı.
- Açılan alanı sayfayı zıplatarak göstermeyin; içerik kayması ayrı bir değişkendir.
- Aynı testte hem kademeli açma hem alan sayısı azaltma yapmayın.
- Kademeli açılan alanın gönderim anında zorunlu çıktığı bir varyant kurmayın; kullanıcıya isteğe bağlı gibi gösterilen alan sonradan şart koşulmamalı.
- Kademeli açmayı hassas alanı gizlemek için kullanmayın; hassas alanda alanı isteğe bağlı yapmak, gerekçe yazmak ya da sonraya ertelemek gibi ara yöntemler geçerlidir.

### EN

Showing every field up front sets clear expectations but makes the form look long. Progressive reveal (the next field appears once one is filled, or an optional section opens with a link) lowers perceived length. The risk: users cannot tell how long the form will take, and a hidden field can feel like a surprise.

**What to test**
- Visibility: Should fields be visible from the start or revealed as the user fills?
- Expectation: Does abandonment rise when it is unclear how many steps remain?
- Fill rate: How much does the fill rate of optional fields drop with progressive reveal?
- Device: Does progressive reveal help more on a small screen?

**KPIs to track**
- Form Completion Rate: Does progressive reveal raise submissions?
- Form Start Rate: Does the shorter form raise first touches?
- Field Fill Rate: The quality of the collected data must not fall to an unacceptable level.
- Median Form Fill Time: Sections that open and close must not lengthen the time.
- Field-Level Abandonment Rate: There must be no sudden dropout at the field that appears.

**What not to do**
- Don’t hide a required field behind progressive reveal; users shouldn’t start without knowing what will be asked.
- Don’t reveal the new field by making the page jump; layout shift is a separate variable.
- Don’t reduce the number of fields in the same test as progressive reveal.
- Don’t build a variant where a field revealed progressively turns out to be required at submission; a field shown as optional must not be made mandatory later.
- Don’t use progressive reveal to hide a sensitive field; for sensitive fields, middle paths such as making the field optional, giving a reason, or deferring it are valid.

---

## Sayfa açılır açılmaz imleci ilk alana koymak işe yarar mı?

Değişken: İlk alana otomatik odaklanma · Fark: değiştir

Etiket: id=fs-006 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does placing the cursor in the first field as soon as the page opens pay off?

EN-Variable: Autofocus on the first field

Sayfa açılır açılmaz ilk alana odaklanmak bir adımı ortadan kaldırır ve masaüstünde yazmaya doğrudan başlatır. Mobilde ise klavyeyi zorla açar, sayfayı yukarı iter ve kullanıcının önce içeriği okumasını engelleyebilir. Formun sayfa içindeki konumu da sonucu değiştirir.

**Test edilmesi gerekenler**
- Odak: İlk alana otomatik odaklanmak doldurmayı başlatıyor mu?
- Kaydırma: Otomatik odak sayfayı forma kaydırıp üstteki içeriği atlatıyor mu?
- Klavye: Mobilde açılan klavye ekranın ne kadarını kapatıyor?
- Fark edilme: Kullanıcı imlecin ilk alanda hazır beklediğini fark edip tıklamadan yazmaya başlıyor mu?
- Cihaz: Masaüstünde kazanan davranış mobilde de kazanıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Form sayfasına atanan ziyaretçilerin formu gönderme oranı artıyor mu?
- Form Başlama Oranı: Tanı metriği; ilk alana giriş artıp gönderim artmıyorsa bulgu budur.
- Doğrulama Hatası Oranı: Üstteki açıklamayı okumadan yazmaya başlayanların hatalı gönderimi artmamalı.
- Üst İçerik Görüntülenme Oranı: Formun üstündeki açıklamanın okunması düşmemeli.
- Erişilebilirlik: Klavye ve ekran okuyucu ile gezinme sırası bozulmamalı.

**Yapılmaması gerekenler**
- Sayfa ortasındaki veya altındaki bir forma otomatik odak verip kullanıcıyı zorla oraya kaydırmayın.
- Mobilde otomatik odağı sınamadan masaüstü sonucuna göre açmayın.
- Aynı testte odak ile alan boyutunu birlikte değiştirmeyin.
- Modal içindeki forma odak verirken modalın kapatma düğmesini odak sırasından çıkarmayın.
- Otomatik odağı sayfa yüklenmesi tamamlanmadan tetikleyip odağın kaymasına izin vermeyin.

### EN

Focusing the first field as soon as the page opens removes a step and lets desktop users start typing right away. On mobile it forces the keyboard open, pushes the page up, and can stop the user from reading the content first. The form’s position on the page also changes the outcome.

**What to test**
- Focus: Does autofocus on the first field get filling started?
- Scrolling: Does autofocus scroll the page to the form and make users skip the content above?
- Keyboard: How much of the screen does the mobile keyboard cover?
- Noticing: Does the user notice the cursor waiting in the first field and start typing without tapping?
- Device: Does the behavior that wins on desktop also win on mobile?

**KPIs to track**
- Form Completion Rate: Does the share of visitors assigned to the form page who submit the form rise?
- Form Start Rate: Diagnostic metric; if entry into the first field rises while submissions don’t, that is the finding.
- Validation Error Rate: Erroneous submissions from people who start typing without reading the explanation above must not increase.
- Top Content View Rate: Reading of the explanation above the form must not drop.
- Accessibility Check: The keyboard and screen-reader navigation order must not break.

**What not to do**
- Don’t autofocus a form in the middle or at the bottom of the page and force the user to scroll to it.
- Don’t switch on autofocus for mobile based on the desktop result without testing it there.
- Don’t change the focus and the field size in the same test.
- When focusing a form inside a modal, don’t take the modal’s close button out of the focus order.
- Don’t trigger autofocus before the page has finished loading and let the focus shift.

---

## Alan yüksekliğini büyütmek doldurmayı etkiler mi?

Değişken: Giriş alanı yüksekliği · Fark: değiştir

Etiket: id=fs-007 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Does making input fields taller affect form filling?

EN-Variable: Input field height

Daha büyük giriş alanı dokunma hedefini büyütür, mobilde yanlış dokunmayı azaltır ve alanın tıklanabilir olduğunu görsel olarak netleştirir. Karşı tarafta: büyüyen alanlar formu uzatır, ekranda aynı anda daha az alan görünür ve form daha ağır hissettirebilir.

**Test edilmesi gerekenler**
- Boyut: Alan yüksekliğini artırmak tamamlamayı değiştiriyor mu?
- Dokunma: Mobilde yanlış alana dokunma azalıyor mu?
- Algı: Büyüyen alanlar formu daha mı uzun gösteriyor?
- Görünen alan sayısı: Ekranda aynı anda daha az alan görünmesi terk yaratıyor mu?
- Cihaz: Kazanç mobile mi özgü, masaüstünde de var mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Büyük alan gönderimi artırıyor mu?
- Yanlış Tıklama Oranı: Hedef dışına dokunma azalıyor mu?
- Form Başlama Oranı: İlk dokunuş artıyor mu?
- Ortalama Doldurma Süresi: Süre uzamamalı.
- Erişilebilirlik: Dokunma hedefi erişilebilirlik alt sınırının altına inmemeli.

**Yapılmaması gerekenler**
- Aynı testte alan yüksekliği ile yazı tipi boyutunu birlikte değiştirmeyin.
- Alanı büyütürken aradaki boşluğu da değiştirmeyin; ikisi ayrı değişkendir.
- Dokunma hedefini küçülten bir varyantı erişilebilirlik alt sınırının altına indirmeyin; bu test edilecek bir seçenek değildir.
- Masaüstünde ölçüp mobil dokunma davranışı hakkında sonuç çıkarmayın.
- Yalnızca bazı alanları büyütüp aynı formda iki farklı alan yüksekliği bırakmayın.

### EN

A larger input field enlarges the touch target, reduces mistaps on mobile and makes it visually clear that the field can be tapped. On the other side, bigger fields lengthen the form, fewer fields fit on screen at once, and the form can feel heavier.

**What to test**
- Size: Does increasing field height change completion?
- Touch: Do mistaps on the wrong field fall on mobile?
- Perception: Do bigger fields make the form look longer?
- Visible fields: Does having fewer fields on screen at once cause abandonment?
- Device: Is the gain specific to mobile, or does it show on desktop too?

**KPIs to track**
- Form Completion Rate: Do larger fields raise submissions?
- Misclick Rate: Do taps outside the target fall?
- Form Start Rate: Do first touches increase?
- Median Form Fill Time: The time must not grow.
- Accessibility Check: The touch target must not drop below the accessibility minimum.

**What not to do**
- Don’t change the field height and the font size in the same test.
- Don’t change the spacing between fields while enlarging them; they are separate variables.
- Don’t let a variant shrink the touch target below the accessibility minimum; that is not an option to test.
- Don’t measure on desktop and draw conclusions about mobile touch behavior.
- Don’t enlarge only some fields and leave two different field heights in the same form.

---

## Otomatik tamamlama form doldurmayı hızlandırır mı?

Değişken: Otomatik tamamlama öneri listesi · Fark: ekle

Etiket: id=fs-008 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does autocomplete speed up form filling?

EN-Variable: Autocomplete suggestion list

Adres, şehir, şirket gibi alanlarda öneri listesi yazma yükünü azaltır ve yazım hatasını düşürür. Riski: öneri listesi yanlış eşleşme sunarsa kullanıcı hatalı veriyi onaylar, ya da liste klavyenin üstünü kapatıp kullanıcıyı kilitler. Veri kalitesi kazancı ile tamamlama kazancı aynı yönde olmayabilir.

**Test edilmesi gerekenler**
- Öneri: Otomatik tamamlama tamamlamayı artırıyor mu?
- Doğruluk: Seçilen öneriler gerçekten doğru veri mi üretiyor?
- Eşleşmeyen değer: Listede karşılığı olmayan bir değer yazan kullanıcı, öneri listesi yüzünden takılıp alanı bırakıyor mu?
- Liste uzunluğu: Kaç öneri gösterildiğinde seçim hızlanıyor?
- Cihaz: Mobilde öneri listesi klavyeyle çakışıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Öneri gönderimi artırıyor mu?
- Adres/Alan Doğruluk Oranı: Hatalı veri oranı artmamalı.
- Ortalama Doldurma Süresi: Alan doldurma süresi kısalıyor mu?
- Alan Bazlı Terk Oranı: Öneri listesi olan alanda bırakma artmamalı.
- Operasyonel Yük: Yanlış veriden doğan düzeltme/iletişim maliyeti artmamalı.

**Yapılmaması gerekenler**
- Serbest metin girişini tamamen kapatıp kullanıcıyı listeye hapsetmeyin.
- Kullanıcının seçtiği öneriyi arka planda farklı bir değerle (ör. düzeltilmiş adres) sessizce değiştirmeyin.
- Aynı testte otomatik tamamlama ile alan sayısını birlikte değiştirmeyin.
- Öneri listesini ilk harfte açmayın; birkaç karakter yazılmadan çıkan liste yanlış seçimi artırır.
- Öneri listesini klavye ile gezilemez hâlde bırakmayın.

### EN

For fields such as address, city or company, a suggestion list cuts typing effort and reduces typos. The risk: if the list offers a wrong match, the user confirms bad data, or the list covers the top of the keyboard and traps them. The data-quality gain and the completion gain may not point the same way.

**What to test**
- Suggestions: Does autocomplete raise completion?
- Accuracy: Do the selected suggestions actually produce correct data?
- Unmatched value: When a user types a value that has no match in the list, do they get stuck because of the suggestion list and abandon the field?
- List length: How many suggestions speed up the choice?
- Device: Does the suggestion list collide with the keyboard on mobile?

**KPIs to track**
- Form Completion Rate: Do suggestions raise submissions?
- Address/Field Accuracy Rate: The share of wrong data must not increase.
- Median Form Fill Time: Does the time to fill the field get shorter?
- Field-Level Abandonment Rate: Abandonment at the field with the suggestion list must not increase.
- Operational Load: The cost of corrections and contact caused by wrong data must not increase.

**What not to do**
- Don’t shut off free-text entry altogether and lock the user into the list.
- Don’t silently swap the suggestion the user picked for a different value in the background (for example a corrected address).
- Don’t change autocomplete and the number of fields in the same test.
- Don’t open the suggestion list at the first letter; a list that appears before a few characters are typed increases wrong picks.
- Don’t leave the suggestion list unusable by keyboard.

---

## Alan altına açıklama eklemek hata oranını düşürür mü?

Değişken: Alan altı yardım metni · Fark: ekle

Etiket: id=fs-009 · mercek=Netlik · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding help text under a field lower the error rate?

EN-Variable: Help text under the field

Kısa bir yardım metni (“Fatura adresinizle aynı olmalı”, “Örnek: 5xx xxx xx xx”) hatalı girişi azaltabilir ve tereddüdü giderebilir. Karşı tarafta: her alana açıklama eklemek formu görsel olarak ağırlaştırır, önemli uyarının fark edilmesini zorlaştırır ve gerçek sorunun yanlış alan tasarımı olduğunu gizler.

**Test edilmesi gerekenler**
- Açıklama: Alan altı yardım metni hata oranını düşürüyor mu?
- Kapsam: Tüm alanlara mı, yalnızca hata alan alanlara mı eklenmeli?
- Okunma: Açıklama eklenen alanda aynı hata türü sürüyorsa, kullanıcılar metni hiç fark etmiyor mu?
- Sonraki test: Açıklama kalıcı hâle gelirse, metnin örnek format mı gerekçe mi vermesi ayrı bir testte hatayı daha çok düşürüyor mu?
- Segment: Yeni ziyaretçi ile kayıtlı kullanıcı açıklamaya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Form sayfasına atanan ziyaretçilerin formu gönderme oranı artıyor mu?
- Doğrulama Hatası Oranı: Tanı metriği; hatalı gönderim azalıyor mu? Hata düşüp gönderim artmıyorsa kazanç veri kalitesindedir, dönüşümde değil.
- Alan Bazlı Terk Oranı: Açıklama eklenen alanda bırakma azalıyor mu?
- Ortalama Doldurma Süresi: Okuma yükü süreyi belirgin uzatmamalı.
- Destek Talebi: Aynı konudaki soru sayısı azalıyor mu?

**Yapılmaması gerekenler**
- Her alana açıklama ekleyip hangisinin işe yaradığını ölçemez hâle gelmeyin.
- Açıklamayı hata mesajının yerine koymayın; ikisi farklı işlev görür.
- Yardım metnini tıklanınca açılan bir ipucunun arkasına gizleyip “açıklama ekledik” demeyin; görünürlük ayrı bir değişkendir.
- Açıklama metnini kontrastı düşük gri ile yazıp okunmaz hâle getirmeyin.
- Aynı testte yardım metnini eklerken alanın etiketini veya doğrulama kuralını da değiştirmeyin.

### EN

A short help text (“Must match your billing address”, “Example: 5xx xxx xx xx”) can reduce wrong entries and remove hesitation. On the other side, adding explanations to every field makes the form visually heavier, makes the important warning harder to notice, and can hide that the real problem is poor field design.

**What to test**
- Explanation: Does help text under the field lower the error rate?
- Scope: Should it go on all fields, or only on the fields that cause errors?
- Reading: If the same type of error continues on a field that has help text, do users not notice the text at all?
- Next test: Once the help text is permanent, does having it give an example format or a reason lower errors more, in a separate test?
- Segment: Do new visitors and registered users react differently to the explanation?

**KPIs to track**
- Form Completion Rate: Does the share of visitors assigned to the form page who submit the form rise?
- Validation Error Rate: Diagnostic metric; do erroneous submissions fall? If errors fall and submissions don’t rise, the gain is in data quality, not conversion.
- Field-Level Abandonment Rate: Does abandonment fall at the field where help text was added?
- Median Form Fill Time: The reading load must not lengthen the time noticeably.
- Support Contact Rate: Does the number of questions on the same topic fall?

**What not to do**
- Don’t add help text to every field and lose the ability to tell which one worked.
- Don’t use help text in place of the error message; they do different jobs.
- Don’t hide the help text behind a tooltip that opens on click and then claim you “added help text”; visibility is a separate variable.
- Don’t write the help text in low-contrast gray so it becomes unreadable.
- Don’t change the field label or the validation rule in the same test as adding help text.

---

## Sosyal hesapla giriş seçeneği kaydı artırır mı?

Değişken: Sosyal hesapla giriş seçeneği · Fark: ekle

Etiket: id=fs-010 · mercek=Çaba · düzey=sürtünme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does a social login option raise sign-ups?

EN-Variable: Social login option

Sosyal giriş şifre oluşturma yükünü kaldırır ve kaydı hızlandırır. Buna karşılık kullanıcı hangi verinin paylaşılacağından çekinebilir, kurumsal kullanıcı kişisel hesabıyla giriş yapmak istemeyebilir ve sonradan “hangi yöntemle giriş yapmıştım” karışıklığı destek yüküne dönüşebilir.

**Test edilmesi gerekenler**
- Seçenek: Sosyal giriş eklemek kayıt oranını artırıyor mu?
- Sağlayıcı sayısı: Tek sağlayıcı mı, birkaç sağlayıcı mı daha iyi çalışıyor?
- Geri dönüş: Kullanıcılar sonraki girişte aynı yöntemi bulabiliyor mu?
- Segment: Bireysel ve kurumsal kullanıcı farklı yönteme mi yöneliyor?

**Takip edilecek ana KPI’lar**
- Kayıt Tamamlama Oranı: Kayıt ekranına ulaşan kullanıcıların (iki kolda aynı tetikleyici) kaydı bitirme oranı artıyor mu?
- İkinci Oturum Giriş Oranı: Kullanıcı geri dönüp giriş yapabilmeli, düşmemeli.
- Aktivasyon Oranı: Hızlı kayıt niteliksiz kullanıcı getirmemeli.
- Giriş Kaynaklı Destek Talebi: “Giriş yapamıyorum” talepleri artmamalı.
- E-posta Erişilebilirlik Oranı: Ulaşılabilir e-posta adresi toplama oranı düşmemeli.

**Yapılmaması gerekenler**
- Sosyal girişi tek seçenek yapıp e-posta ile kaydı kaldırmayın.
- Hangi verilerin alındığını gizleyen bir buton metni kullanmayın.
- Aynı testte hem sosyal giriş eklemeyi hem form alanı azaltmayı yapmayın.
- Sosyal hesapla gelen kullanıcıyı, aynı e-postayla açılmış mevcut hesabından ayrı ikinci bir hesaba düşürmeyin.
- Kimlik doğrulama akışının güvenlik adımlarını sürtünme diye testin konusu yapmayın.

### EN

Social login removes the burden of creating a password and speeds up sign-up. On the other hand, users may worry about which data will be shared, corporate users may not want to sign in with a personal account, and the later confusion of “which method did I sign in with” can turn into support load.

**What to test**
- Option: Does adding social login raise the sign-up rate?
- Number of providers: Does one provider or several work better?
- Return: Can users find the same method at their next sign-in?
- Segment: Do individual and corporate users lean toward different methods?

**KPIs to track**
- Sign-up Completion Rate: Does the share of users who reach the sign-up screen (same trigger in both arms) and finish sign-up rise?
- Second-Session Login Rate: Users must be able to come back and sign in; it must not drop.
- Activation Rate: Quick sign-up must not bring in unqualified users.
- Login-Related Support Contacts: “I can’t sign in” requests must not increase.
- Email Reachability Rate: The rate of collecting a reachable email address must not drop.

**What not to do**
- Don’t make social login the only option and remove email sign-up.
- Don’t use a button label that hides which data is collected.
- Don’t add social login and reduce form fields in the same test.
- Don’t let a user who arrives via a social account end up with a second, separate account instead of their existing account opened with the same email.
- Don’t make the security steps of the authentication flow a test subject under the label of friction.

---

## Şifre yerine tek kullanımlık kod göndermek girişi artırır mı?

Değişken: Birincil giriş yöntemi · Fark: değiştir

Etiket: id=fs-011 · mercek=Çaba · düzey=sürtünme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does sending a one-time code instead of a password raise sign-ins?

EN-Variable: Primary login method

Şifresiz giriş (e-postaya veya telefona gönderilen tek kullanımlık kod) unutulan şifre kaynaklı kayıpları ortadan kaldırır. Bedeli: kullanıcı e-posta veya SMS’e geçmek zorunda kalır, kod gecikirse akış kopar ve kanal teslim oranı doğrudan dönüşüme yansır.

**Test edilmesi gerekenler**
- Yöntem: Tek kullanımlık kod ile şifreli giriş arasında tamamlama farkı var mı?
- Kanal geçişi: Kullanıcı e-postaya gidip geri dönebiliyor mu, akış kopuyor mu?
- Teslim süresi: Kodun ulaşma süresi tamamlamayı ne kadar etkiliyor?
- Kalıcılık: Kodla bir kez giriş yapan kullanıcı sonraki girişlerde de kodu mu seçiyor, şifreye mi dönüyor?
- Cihaz: Mobilde kod otomatik doldurulduğunda fark büyüyor mu?

**Takip edilecek ana KPI’lar**
- Giriş Tamamlama Oranı: Yöntem girişi tamamlatıyor mu?
- Kod Teslim ve Kullanım Oranı: İkincil (yalnızca B); gönderilen kodun kullanılma payı, kollar arasında karşılaştırılmaz.
- Yetkisiz Giriş Bildirimi Oranı (30 gün): Güvenlik ekibinin kaydındaki yetkisiz giriş şikâyeti ve hesap ele geçirme olayı atanan kullanıcı başına artmamalı.
- Şifre Sıfırlama Talebi: Sıfırlama yükü azalıyor mu?
- Destek Talebi: Giriş kaynaklı talepler atanan ziyaretçi başına artmamalı.

**Yapılmaması gerekenler**
- İki adımlı doğrulamayı veya kimlik doğrulamayı bu testin kapsamına almayın; bunlar koruma amaçlıdır.
- Kod ekranında kodun hangi adrese veya numaraya gönderildiğini gizlemeyin; kullanıcı yanlış kanalı düzeltebilmeli.
- Güvenlik ekibi B’nin kod süresini, deneme sınırını ve hesap kurtarma akışını onaylamadan testi başlatmayın; bu onay bir başlatma koşuludur. Şifreli girişi de aynı anda kaldırmayın.
- Kodun gelmediği durumda yeniden gönderme seçeneğini kaldırmayın veya uzun bir bekleme süresinin arkasına saklamayın.
- Aynı testte giriş yöntemini değiştirirken giriş ekranındaki alanları veya oturum süresini de değiştirmeyin.

> **Güncellik notu (2026-11):** Geçiş anahtarı (passkey) artık yaygın tarayıcı ve işletim sistemlerinde destekleniyor ve kodu e-postada ya da SMS’te beklemeden, cihazın ekran kilidiyle giriş sağlıyor. Tek kullanımlık kod testi hâlâ geçerlidir; ama şifresiz girişte daha güçlü aday, geçiş anahtarını mevcut yöntemin yanında ek seçenek olarak sunmaktır. Bu ayrı bir değişkendir ve kod akışıyla aynı testte değiştirilmez.

### EN

Passwordless login (a one-time code sent to email or phone) removes the losses caused by forgotten passwords. The price: the user has to switch to email or SMS, the flow breaks if the code is late, and the delivery rate of the channel feeds straight into conversion.

**What to test**
- Method: Is there a completion difference between a one-time code and password login?
- Channel switch: Can the user go to their email and come back, or does the flow break?
- Delivery time: How much does the time the code takes to arrive affect completion?
- Persistence: After signing in once with a code, does the user choose the code again at later sign-ins, or go back to the password?
- Device: Does the difference grow on mobile when the code is autofilled?

**KPIs to track**
- Login Completion Rate: Does the method get more people to complete login?
- Code Delivery and Use Rate: Secondary (B only); the share of sent codes that are used, not compared across arms.
- Unauthorized Login Report Rate (30 days): Unauthorized-login complaints and account-takeover incidents in the security team’s records must not increase per assigned user.
- Password Reset Requests: Does the reset load fall?
- Support Contact Rate: Login-related requests must not increase per assigned visitor.

**What not to do**
- Don’t bring two-step verification or identity verification into this test’s scope; they exist for protection.
- On the code screen, don’t hide which address or number the code was sent to; users must be able to correct a wrong channel.
- Don’t start the test before the security team has approved B’s code expiry, attempt limit and account-recovery flow; that approval is a launch condition. Also don’t remove password login at the same time.
- Don’t remove the resend option when the code doesn’t arrive, or hide it behind a long wait.
- Don’t change the fields on the login screen or the session length in the same test as the login method.

> **Freshness note (2026-11):** Passkeys are now supported across widespread browsers and operating systems and let users sign in with the device’s screen lock, without waiting for a code in email or SMS. The one-time-code test is still valid, but for passwordless login the stronger candidate is to offer the passkey as an additional option alongside the current method. That is a separate variable and is not changed in the same test as the code flow.

---

## Kaydı aksiyondan sonraya ertelemek tamamlamayı artırır mı?

Değişken: Kayıt adımının akıştaki yeri · Fark: taşı

Etiket: id=fs-012 · mercek=Çaba · düzey=akış · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does postponing sign-up until after the action raise completion?

EN-Variable: Position of the sign-up step in the flow

Kayıt ekranını aksiyonun önüne koymak niyeti test eder ama hazır olmayan kullanıcıyı kaybeder. Kaydı sonraya bırakmak (önce işlemi yaptırmak, sonra kaydetmeyi teklif etmek) tamamlamayı artırabilir, buna karşılık kayıtsız tamamlanan işlemlerin geri dönüşü ve iletişimi zorlaşır.

**Test edilmesi gerekenler**
- Zamanlama: Kayıt aksiyondan önce mi, sonra mı istenmeli?
- Değer anı: Kullanıcı faydayı gördükten sonra kayıt oranı artıyor mu?
- Kayıp: Kayıtsız tamamlayanların ne kadarı sonradan kaydoluyor?
- Sonraki test: Ertelenmiş kayıt sabitken, kaydı “ilerlemeni kaydet” diye çerçevelemek ayrı bir testte kayıt oranını artırıyor mu?
- Segment: Yeni ziyaretçi ile geri dönen kullanıcı farklı zamanlamaya mı uyuyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Asıl işlemi bitirenler artıyor mu?
- Kayıt Oranı: Toplam kayıt sayısı kabul edilemez seviyeye düşmemeli.
- Kayıt Sonrası Geri Dönüş Oranı: İkinci ziyaret oranı düşmemeli.
- İletişim İzni Oranı: Ulaşılabilir kullanıcı oranı düşmemeli.
- Destek Talebi: “İşlemimi bulamıyorum” talepleri artmamalı.

**Yapılmaması gerekenler**
- Kaydı erteleyip sonra kullanıcıyı kapatılamayan bir ekranla kayda zorlamayın.
- İşlemi tamamlatıp ardından sonucu kayıt arkasına kilitlemeyin.
- Aynı testte hem zamanlamayı hem kayıt formunun alanlarını değiştirmeyin.
- Kayıtsız tamamlanan işlemin sonucuna yeniden ulaşma yolunu (e-posta bağlantısı, takip kodu) bırakmadan varyantı açmayın.
- Yasal olarak kimlik veya izin gerektiren bir işlemde kaydı ertelemeyi test konusu yapmayın.

### EN

Putting the sign-up screen before the action tests intent but loses users who are not ready. Deferring sign-up (let the user do the task first, then offer to save) can raise completion, but tasks completed without an account are harder to reverse and to follow up on.

**What to test**
- Timing: Should sign-up be requested before or after the action?
- Moment of value: Does the sign-up rate rise once the user has seen the benefit?
- Loss: What share of those who complete without an account sign up later?
- Next test: With deferred sign-up fixed, does framing sign-up as “save your progress” raise the sign-up rate in a separate test?
- Segment: Do new visitors and returning users suit different timing?

**KPIs to track**
- Primary Action Completion Rate: Does the number of people who finish the main task rise?
- Sign-up Rate: The total number of sign-ups must not fall to an unacceptable level.
- Post-Sign-up Return Rate: The second-visit rate must not drop.
- Contact Permission Rate: The share of reachable users must not drop.
- Support Contact Rate: “I can’t find my transaction” requests must not increase.

**What not to do**
- Don’t defer sign-up and then force the user into it with a screen that can’t be closed.
- Don’t have the user complete the task and then lock the result behind sign-up.
- Don’t change the timing and the sign-up form fields in the same test.
- Don’t launch the variant without leaving a way to get back to the result of a task completed without an account (an email link, a tracking code).
- Don’t make deferring sign-up a test subject for a transaction that legally requires identity or consent.

---

## Formu modal içinde mi, sayfa akışında mı göstermeli?

Değişken: Formun sunum biçimi (modal, sayfa içi) · Fark: değiştir

Etiket: id=fs-013 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should the form appear in a modal or in the page flow?

EN-Variable: Form presentation (modal, inline)

Modal form dikkati toplar ve kullanıcıyı sayfadan koparmaz. Ancak küçük ekranda dar kalır, arkadaki bağlamı gizler, tarayıcı geri tuşuyla ilişkisi kırılgandır ve yanlışlıkla kapatma kaybı yaratır. Sayfa içi form ise bağlamı korur ama kullanıcı formu fark etmeyebilir.

**Test edilmesi gerekenler**
- Sunum: Form modalde mi, sayfa akışında mı daha çok tamamlanıyor?
- Kapatma: Yanlışlıkla kapatma kaynaklı kayıp ne kadar?
- Bağlam: Modal arkadaki bilgiyi gizleyip kararı zorlaştırıyor mu?
- Geri tuşu: Tarayıcı geri hareketi modalde beklenen davranışı veriyor mu?
- Cihaz: Mobilde modal mı, tam sayfa mı daha iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Sunum biçimi gönderimi artırıyor mu?
- Form Başlama Oranı: Formun fark edilmesi artıyor mu?
- Yanlışlıkla Kapatma Oranı: Veri girildikten sonra kapatma artmamalı.
- Talep Başına Nitelik Oranı: Arkadaki bilgiyi görmeden gönderilen formlar niteliği düşürmemeli.
- Erişilebilirlik: Modal açıkken odak dışarı kaçmamalı, klavyeyle kapatma bozulmamalı.

**Yapılmaması gerekenler**
- Kapatılamayan veya kapatma düğmesi gizlenmiş modal önermeyin.
- Modalın arka planını karartma yoğunluğunu aynı testte değiştirmeyin; bu ayrı bir değişkendir.
- Veri girilmiş bir modalı dışına tıklayınca uyarısız kapatan varyantı kazanan ilan etmeyin.
- Mobilde modalı ekranın yarısına sıkıştırıp masaüstü sonucuyla karşılaştırmayın.
- Modal formu, kullanıcı sayfada bir şey okurken ya da yazarken açılıp işini bölecek şekilde tetiklemeyin.

### EN

A modal form gathers attention and keeps the user from leaving the page. But it is cramped on small screens, hides the context behind it, has a fragile relationship with the browser back button, and accidental closing causes loss. An inline form keeps the context, but the user may not notice the form.

**What to test**
- Presentation: Is the form completed more in a modal or in the page flow?
- Closing: How much is lost to accidental closing?
- Context: Does the modal hide the information behind it and make the decision harder?
- Back button: Does the browser back gesture give the expected behavior in the modal?
- Device: On mobile, does a modal or a full page work better?

**KPIs to track**
- Form Completion Rate: Does the presentation raise submissions?
- Form Start Rate: Does noticing of the form increase?
- Accidental Close Rate: Closing after data has been entered must not increase.
- Qualification Rate per Lead: Forms submitted without seeing the information behind must not lower quality.
- Accessibility Check: Focus must not escape the modal while it is open, and closing by keyboard must not break.

**What not to do**
- Don’t propose a modal that can’t be closed or whose close button is hidden.
- Don’t change the intensity of the modal’s background dimming in the same test; it is a separate variable.
- Don’t declare a variant the winner if it closes a modal with entered data when the user clicks outside, without warning.
- Don’t squeeze the modal into half the screen on mobile and compare it with the desktop result.
- Don’t trigger the modal form so that it opens and interrupts the user while they are reading or typing on the page.

---

## Çok adımlı formda geri dönüş imkânı tamamlamayı etkiler mi?

Değişken: Çok adımlı formdaki geri düğmesi · Fark: ekle

Etiket: id=fs-014 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a way back in a multi-step form affect completion?

EN-Variable: Back button in a multi-step form

Görünür bir geri düğmesi hata düzeltmeyi kolaylaştırır ve kullanıcıya kontrol hissi verir. Karşı argüman: geri dönüş imkânı ilerlemeyi yavaşlatır, kullanıcı adımlar arasında gidip gelir ve girilen veri kaybolursa güven zedelenir. Asıl belirleyici, geri dönüldüğünde verinin korunup korunmadığıdır.

**Test edilmesi gerekenler**
- Görünürlük: Geri düğmesi görünür olduğunda tamamlama değişiyor mu?
- Veri koruma: Geri dönünce girilen veri korunuyor mu?
- Kullanım: Geri düğmesi ne sıklıkla kullanılıyor, kullanan tamamlıyor mu?
- Cihaz: Mobilde tarayıcı geri hareketi ile form geri düğmesi çakışıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Geri dönüş imkânı gönderimi artırıyor mu?
- Veri Kaybı Oranı: Geri dönüşte girilen veri kaybolmamalı.
- Adım Bazlı Terk Oranı: Belirli bir adımda bırakma artmamalı.
- Doğrulama Hatası Oranı: Gönderimde geri dönen hata azalıyor mu?
- Ortalama Doldurma Süresi: Gidip gelmeler süreyi kabul edilemez ölçüde uzatmamalı.

**Yapılmaması gerekenler**
- Geri düğmesini ekleyip veri korumasını uygulamadan test etmeyin; kaybolan veriyi değil kendi hatanızı ölçersiniz.
- Aynı testte adım sayısını da değiştirmeyin.
- Tarayıcı geri hareketini engelleyen bir varyant kurmayın.
- Geri düğmesini “İleri” düğmesiyle aynı görsel ağırlıkta yan yana koymayın; yanlış dokunuş ilerlemeyi geri alır.
- Ödeme adımında geri dönüşü test ederken işlem güvenliği kontrollerini zayıflatmayın.

### EN

A visible back button makes correcting mistakes easier and gives the user a sense of control. The counter-argument: a way back slows progress, users go back and forth between steps, and trust suffers if entered data is lost. What matters most is whether the data is preserved when they go back.

**What to test**
- Visibility: Does completion change when the back button is visible?
- Data preservation: Is the entered data kept when the user goes back?
- Use: How often is the back button used, and do those who use it complete?
- Device: On mobile, does the browser back gesture collide with the form’s back button?

**KPIs to track**
- Form Completion Rate: Does a way back raise submissions?
- Data Loss Rate: Entered data must not be lost on going back.
- Step-Level Abandonment Rate: Dropout at a particular step must not increase.
- Validation Error Rate: Do the errors returned at submission fall?
- Median Form Fill Time: Going back and forth must not lengthen the time to an unacceptable degree.

**What not to do**
- Don’t test by adding the back button without implementing data preservation; you would measure your own bug, not the lost data.
- Don’t change the number of steps in the same test.
- Don’t build a variant that blocks the browser back gesture.
- Don’t place the back button next to the “Next” button with the same visual weight; a wrong tap undoes progress.
- When testing a way back at the payment step, don’t weaken transaction security checks.

---

## Formu cümle hâline getirmek doldurmayı artırır mı?

Değişken: Formun cümle biçiminde kurulması · Fark: değiştir

Etiket: id=fs-015 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does turning a form into a sentence raise form filling?

EN-Variable: Form written as a sentence

Alanları bir cümlenin içine yerleştirmek (“Ben [ad], [şehir]’de [hizmet] arıyorum”) formu ankete değil sohbete benzetir ve kısa formlarda samimi durur. Riski: uzun formlarda cümle yapısı dağılır, alanların sırası dilbilgisine esir olur, hata mesajlarını yerleştirmek zorlaşır ve ekran okuyucu deneyimi bozulabilir.

**Test edilmesi gerekenler**
- Biçim: Cümle formu klasik alan listesinden daha mı çok dolduruluyor?
- Hata: Hata mesajları cümle içinde anlaşılır kalıyor mu?
- Tarama: Kullanıcı hangi bilgilerin isteneceğini bir bakışta görebiliyor mu?
- Cihaz: Mobilde satır kaymaları cümleyi okunmaz yapıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Cümle formu gönderimi artırıyor mu?
- Form Başlama Oranı: İlk alana giriş artıyor mu?
- Doğrulama Hatası Oranı: Hatalı gönderim artmamalı.
- Ortalama Doldurma Süresi: Süre uzamamalı.
- Erişilebilirlik: Ekran okuyucuda alan etiketleri anlaşılmaz hâle gelmemeli.

**Yapılmaması gerekenler**
- Alan sırasını yalnızca cümle akışına göre kurup mantıksal sırayı bozmayın.
- Aynı testte cümle biçimi ile alan sayısını birlikte değiştirmeyin.
- Hata mesajlarını cümlenin dışına atıp hangi alana ait olduğunu belirsiz bırakmayın.
- Uzun ve çok alanlı bir formu cümleye zorlamayın.
- Ekran okuyucu için etiket bağlantısını görsel cümleye feda etmeyin.

### EN

Placing the fields inside a sentence (“I’m [name], looking for [service] in [city]”) makes the form feel like a conversation, not a survey, and reads as friendly on short forms. The risk: in long forms the sentence structure falls apart, field order becomes a slave to grammar, error messages are hard to place, and the screen-reader experience can break.

**What to test**
- Format: Is the sentence form filled in more than a classic list of fields?
- Errors: Do error messages stay clear inside the sentence?
- Scanning: Can the user see at a glance what information will be asked?
- Device: On mobile, do line breaks make the sentence unreadable?

**KPIs to track**
- Form Completion Rate: Does the sentence form raise submissions?
- Form Start Rate: Does entry into the first field increase?
- Validation Error Rate: Erroneous submissions must not increase.
- Median Form Fill Time: The time must not grow.
- Accessibility Check: Field labels must not become unintelligible in a screen reader.

**What not to do**
- Don’t order the fields only by sentence flow and break the logical order.
- Don’t change the sentence format and the number of fields in the same test.
- Don’t push error messages outside the sentence and leave unclear which field they belong to.
- Don’t force a long, many-field form into a sentence.
- Don’t sacrifice the label association for screen readers to the visual sentence.

---

## Formu sayfanın ortasına almak mı, sola hizalamak mı?

Değişken: Formun sayfadaki yatay konumu · Fark: taşı

Etiket: id=fs-016 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Center the form on the page or align it left?

EN-Variable: Horizontal position of the form on the page

Ortalanmış form dikkati toplar ve tek amaçlı sayfalarda doğal durur. Sola hizalı form ise okuma yönüyle uyumludur ve yanına açıklama, güvence veya özet yerleştirmeye izin verir. Ortalama, formun yanındaki destekleyici içeriği de ortadan kaldırır.

**Test edilmesi gerekenler**
- Hizalama: Ortalanmış form tamamlamayı artırıyor mu?
- Yan içerik: Form ortalanınca korunan güvence ve özet bloğu formun altına itilip daha az mı görülüyor?
- Odak: Ortalama dikkat dağıtıcıları gerçekten azaltıyor mu?
- Sonraki test: Kazanan hizalama sabitken form genişliği (dar / geniş) ayrı bir testte tamamlamayı değiştiriyor mu?
- Cihaz: Mobilde zaten tek sütuna düşen düzende fark kalıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Hizalama gönderimi artırıyor mu?
- Form Başlama Oranı: İlk dokunuş artıyor mu?
- Destek İçerik Görülme Oranı: Yandaki güvencelerin görülmesi kabul edilemez ölçüde düşmemeli.
- Ortalama Doldurma Süresi: Süre uzamamalı.
- Destek Talebi: Güvence ve özet bloğunu görmeden gönderenlerin açtığı talepler artmamalı.

**Yapılmaması gerekenler**
- Aynı testte hizalama ile form genişliğini birlikte değiştirmeyin.
- Ortalarken yandaki güvence içeriğini sessizce kaldırmayın; kaldırıyorsanız bu ayrı bir testtir.
- Mobilde fark olmayan bir değişikliği mobil kazancı gibi raporlamayın.
- Ortalanmış formu ekranın dikey ortasına sabitleyip kaydırmayı engellemeyin.
- Tek sayfada ölçüp sonucu farklı amaçlı formlara genellemeyin.

### EN

A centered form gathers attention and sits naturally on single-purpose pages. A left-aligned form fits the reading direction and leaves room beside it for an explanation, reassurance or summary. Centering also removes the supporting content next to the form.

**What to test**
- Alignment: Does a centered form raise completion?
- Side content: When the form is centered, is the reassurance and summary block that is kept pushed below the form and seen less?
- Focus: Does centering really reduce distractions?
- Next test: With the winning alignment fixed, does form width (narrow / wide) change completion in a separate test?
- Device: Does a difference remain in a layout that already collapses to one column on mobile?

**KPIs to track**
- Form Completion Rate: Does the alignment raise submissions?
- Form Start Rate: Do first touches increase?
- Supporting Content View Rate: Views of the reassurances beside the form must not fall to an unacceptable level.
- Median Form Fill Time: The time must not grow.
- Support Contact Rate: Requests opened by people who submitted without seeing the reassurance and summary block must not increase.

**What not to do**
- Don’t change the alignment and the form width in the same test.
- When centering, don’t silently remove the reassurance content beside the form; if you do remove it, that is a separate test.
- Don’t report a change that makes no difference on mobile as a mobile gain.
- Don’t pin the centered form to the vertical middle of the screen and block scrolling.
- Don’t measure on one page and generalize the result to forms with different purposes.

---

## Modal formda arka planı soldurmak dikkati topluyor mu?

Değişken: Modal arka plan karartması · Fark: ekle

Etiket: id=fs-017 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Does dimming the background behind a modal form focus attention?

EN-Variable: Modal background dimming

Arka planı karartmak veya bulanıklaştırmak modalı öne çıkarır ve form dışındaki her şeyi görsel olarak susturur. Karşı tarafta: karartma kullanıcının bağlamını kaybetmesine yol açar, hangi sayfadan geldiğini hatırlamasını zorlaştırır ve yoğun karartma kapana kısılma hissi verebilir.

**Test edilmesi gerekenler**
- Yoğunluk: Arka plan karartması tamamlamayı artırıyor mu?
- Bağlam: Arkadaki bilginin görünmesi karar için gerekli mi?
- Sonraki test: Karartma kazanırsa, aynı modalda karartma yerine bulanıklaştırma kullanmak ayrı bir testte tamamlamayı artırıyor mu?
- Dış tıklama: Karartılmış alan tıklanabilir bir yüzey gibi görünüp dışarı tıklayarak yanlışlıkla kapatmayı artırıyor mu?
- Cihaz: Arka planın zaten az göründüğü mobilde karartmanın etkisi masaüstüne göre daha mı zayıf kalıyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Karartma gönderimi artırıyor mu?
- Yanlışlıkla Kapatma Oranı: Veri girildikten sonra kapatma artmamalı.
- Form Başlama Oranı: Formun fark edilmesi artıyor mu?
- Ortalama Doldurma Süresi: Arkadaki bilgiye bakmak için modalı kapatıp yeniden açmak süreyi uzatmamalı.
- Erişilebilirlik: Odak modaldan kaçmamalı, klavyeyle kapatma yolu kaybolmamalı.

**Yapılmaması gerekenler**
- Kapatma yolu bırakmayan bir karartma kurmayın.
- Aynı testte karartma yoğunluğu ile modal içeriğini birlikte değiştirmeyin.
- Karar için gereken bilgiyi arkada karartılmış hâlde bırakmayın.
- Veri girilmiş formu dışına tıklayınca uyarısız kapatmayın.
- Hareket azaltma tercihini yok sayan bir bulanıklaştırma animasyonu kullanmayın.

### EN

Dimming or blurring the background makes the modal stand out and visually silences everything outside the form. On the other side, dimming makes users lose their context, makes it harder to remember which page they came from, and heavy dimming can feel like being trapped.

**What to test**
- Intensity: Does background dimming raise completion?
- Context: Is it necessary for the information behind to stay visible for the decision?
- Next test: If dimming wins, does using blur instead of dimming in the same modal raise completion in a separate test?
- Outside click: Does the dimmed area look like a clickable surface and increase accidental closing by clicking outside?
- Device: On mobile, where the background is barely visible anyway, is the effect of dimming weaker than on desktop?

**KPIs to track**
- Form Completion Rate: Does dimming raise submissions?
- Accidental Close Rate: Closing after data has been entered must not increase.
- Form Start Rate: Does noticing of the form increase?
- Median Form Fill Time: Closing and reopening the modal to look at the information behind must not lengthen the time.
- Accessibility Check: Focus must not escape the modal, and the keyboard way to close must not disappear.

**What not to do**
- Don’t build a dimmed background that leaves no way to close.
- Don’t change dimming intensity and the modal content in the same test.
- Don’t leave information needed for the decision dimmed behind the modal.
- Don’t close a form with entered data on an outside click without warning.
- Don’t use a blur animation that ignores the reduced-motion preference.

---

## Hazır şablon metin sunmak serbest metin alanını doldurtuyor mu?

Değişken: Düzenlenebilir hazır şablon metin · Fark: ekle

Etiket: id=fs-018 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does offering an editable template text get a free-text field filled in?

EN-Variable: Editable template text

Boş bir metin kutusu, ne yazacağını bilmeyen kullanıcıyı durdurur. Hazır bir örnek metin sunmak (düzenlenebilir bir taslak) bu engeli kaldırır ve alanın doldurulma oranını artırabilir. Riski: gönderilen metinlerin çoğu birbirinin aynısı olur, kişisel olmaktan çıkar ve alıcı tarafında değeri düşer.

**Test edilmesi gerekenler**
- Şablon: Hazır metin sunmak alanın doldurulmasını artırıyor mu?
- Kişiselleştirme: Kullanıcılar şablonu düzenliyor mu, olduğu gibi mi gönderiyor?
- Seçenek: Birden fazla şablon sunmak çeşitliliği artırıyor mu?
- Sonraki test: Şablonun alana önceden yazılı gelmesi yerine bir düğmeyle eklenmesi, ayrı bir testte doldurma oranını değiştiriyor mu?
- Segment: Yeni kullanıcı ile deneyimli kullanıcı farklı mı davranıyor?

**Takip edilecek ana KPI’lar**
- Alan Doldurma Oranı: Serbest metin alanının doldurulması artıyor mu?
- Form Tamamlama Oranı: Gönderim artıyor mu?
- Metin Özgünlük Oranı: Aynı metnin tekrarı kabul edilemez seviyeye çıkmamalı.
- Ortalama Doldurma Süresi: Süre kısalıyor mu?
- Alıcı Yanıt Oranı: Gönderilen metne alıcının yanıt verme oranı düşmemeli.

**Yapılmaması gerekenler**
- Şablonu silinemez veya düzenlenemez hâlde bırakmayın.
- Şablon metni kullanıcı yazmış gibi gönderip bunu belirtmeyin.
- Aynı testte şablon varlığı ile alanın zorunluluğunu birlikte değiştirmeyin.
- Tek bir şablon sunup tüm gönderimlerin aynılaşmasını sonuçtan bağımsız görmezden gelmeyin.
- Şablona kullanıcının adı veya iletişim bilgisi gibi kişisel verileri kendiliğinden gömmeyin; kullanıcı fark etmeden paylaşır.

### EN

An empty text box stops a user who doesn’t know what to write. Offering a ready example text (an editable draft) removes that barrier and can raise the fill rate of the field. The risk: most submitted texts end up identical, stop being personal and lose value on the recipient’s side.

**What to test**
- Template: Does offering a ready text raise the fill rate of the field?
- Personalization: Do users edit the template, or send it as is?
- Choice: Does offering several templates increase variety?
- Next test: Does adding the template with a button instead of pre-filling it in the field change the fill rate in a separate test?
- Segment: Do new users and experienced users behave differently?

**KPIs to track**
- Field Fill Rate: Does the fill rate of the free-text field rise?
- Form Completion Rate: Do submissions rise?
- Text Uniqueness Rate: Repetition of the same text must not reach an unacceptable level.
- Median Form Fill Time: Does the time get shorter?
- Recipient Response Rate: The rate at which recipients reply to the text sent must not drop.

**What not to do**
- Don’t leave the template impossible to delete or edit.
- Don’t send the template text as if the user wrote it without saying so.
- Don’t change the presence of the template and whether the field is required in the same test.
- Don’t offer a single template and ignore, regardless of the result, that all submissions become identical.
- Don’t embed personal data such as the user’s name or contact details into the template automatically; the user shares it without noticing.

---

## Serbest tutar girişinin üstüne hazır tutar butonları eklemek toplam tutarı artırır mı?

Değişken: Hazır tutar butonları · Fark: ekle

Etiket: id=fs-019 · mercek=Fiyat · düzey=form · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does adding preset amount buttons above a free amount field raise the total amount?

EN-Variable: Preset amount buttons

Hazır tutar butonları karar yükünü kaldırır, bir aralık önerir ve yazma zahmetini sıfırlar. Serbest giriş kutusu ise kullanıcıyı kendi tutarını belirlemekte özgür bırakır ama boş kutu ne yazılacağı konusunda bir işaret vermez. Bu testte butonlar serbest giriş kutusunun üstüne eklenir, kutu yerinde kalır. Sunulan butonların hangi tutarları içerdiği, seçilen ortalama tutarı doğrudan belirler.

**Test edilmesi gerekenler**
- Varlık: Serbest girişin üstüne hazır butonlar eklemek tamamlamayı artırıyor mu?
- Aralık: Buton tutarları ortalama seçimi hangi yöne çekiyor?
- Serbest kutu: Butonlar eklenince, listede olmayan bir tutar yazmak isteyen kullanıcı serbest giriş kutusunu bulup kullanabiliyor mu?
- Karar yükü: Butonlar tutar belirleme süresini kısaltıp tutar alanında takılıp sayfadan çıkan kullanıcıyı azaltıyor mu?
- Segment: İlk kez ödeme yapan ile tekrar edenler farklı mı davranıyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Tutar ekranına atanan kullanıcı başına toplam tutar artıyor mu?
- Ana Aksiyon Tamamlama Oranı: İşlemi bitiren kullanıcı oranı artıyor mu?
- Ortalama Seçilen Tutar: Ortalama tutar düşmemeli.
- Serbest Giriş Kullanım Oranı: Kendi tutarını girenlerin oranı ne kadar?
- İptal veya Düzeltme Oranı (30 gün): Yanlış tutar kaynaklı düzeltme artmamalı.

**Yapılmaması gerekenler**
- Serbest giriş imkânını tamamen kaldırıp kullanıcıyı hazır tutarlara hapsetmeyin.
- Yüksek bir tutarı önceden seçili getirip kullanıcıyı fark etmeden ona yönlendirmeyin; ödenecek tutarı artıran varsayılan manipülasyon sınırındadır (bkz. cart-checkout → varsayılan işaretli seçenekler).
- Aynı testte butonların varlığı ile buton tutarlarını birlikte değiştirmeyin.
- Butona dokununca kullanıcının serbest giriş kutusuna yazdığı tutarı uyarısız silmeyin.
- Tutarları görünmez küçüklükte yazıp seçim yapmayı zorlaştırmayın.

### EN

Preset amount buttons remove decision load, suggest a range and zero out the effort of typing. A free-entry box leaves the user free to set their own amount, but an empty box gives no hint of what to write. In this test the buttons are added above the free-entry box, and the box stays in place. Which amounts the buttons offer directly determines the average amount chosen.

**What to test**
- Presence: Does adding preset buttons above free entry raise completion?
- Range: Which way do the button amounts pull the average choice?
- Free box: Once the buttons are added, can a user who wants to type an amount not on the list find and use the free-entry box?
- Decision load: Do the buttons shorten the time to settle on an amount and reduce users who get stuck at the amount field and leave the page?
- Segment: Do first-time payers and repeat payers behave differently?

**KPIs to track**
- Revenue per Visitor (RPV): Does total amount per user assigned to the amount screen rise?
- Primary Action Completion Rate: Does the share of users who finish the transaction rise?
- Average Selected Amount: The average amount must not fall.
- Free Entry Usage Rate: What share enter their own amount?
- Cancellation or Correction Rate (30 days): Corrections caused by a wrong amount must not increase.

**What not to do**
- Don’t remove free entry altogether and lock the user into the preset amounts.
- Don’t preselect a high amount and steer the user to it without their noticing; a default that raises the amount to be paid is on the edge of manipulation (see cart-checkout → pre-checked options).
- Don’t change the presence of the buttons and the button amounts in the same test.
- Don’t silently erase the amount the user typed into the free-entry box when they tap a button.
- Don’t set the amounts in invisibly small text and make choosing harder.

---

## Formun başına uygunluk açıklaması koymak talebin niteliğini artırır mı?

Değişken: Form başı uygunluk açıklaması · Fark: ekle

Etiket: id=fs-020 · mercek=Uygunluk · düzey=bilgi · sektör=b2b · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does an eligibility note at the top of the form raise lead quality?

EN-Variable: Eligibility note at the top of the form

Formun üstüne kimin için uygun olduğunu yazmak (asgari bütçe, hizmet bölgesi, gerekli koşul) uymayan kullanıcıyı baştan eler ve satış ekibinin yükünü azaltır. Bedeli: toplam talep sayısı düşer, sınırda kalan bazı uygun kullanıcılar da kendini dışarıda görüp vazgeçer.

**Test edilmesi gerekenler**
- Açıklama: Uygunluk bilgisi nitelikli talebi artırıyor mu?
- Hacim kaybı: Toplam talep ne kadar düşüyor?
- Sonraki test: Açıklama kalıcı olursa, koşulu net ya da yumuşak bir dille yazmak ayrı bir testte nitelikli talebi değiştiriyor mu?
- Yanlış eleme: Aslında uygun olan kullanıcılar da eleniyor mu?
- Segment: Ücretli reklamdan gelen ile organik gelen ziyaretçi uygunluk açıklamasına farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Nitelikli Talep Oranı (atanan ziyaretçi başına): Form sayfasına atanan ziyaretçi başına hedef profile uyan talep oranı artıyor mu?
- Form Tamamlama Oranı: Toplam gönderim oranı kabul edilemez ölçüde düşmemeli.
- Talep Başına Nitelik Oranı: Uygun talep oranı artıyor mu?
- Satış Ekibi Eleme Süresi: Eleme yükü azalıyor mu?
- Fırsat Kapanış Oranı: Gelen taleplerin satışa dönüşü artıyor mu?

**Yapılmaması gerekenler**
- Uygunluk açıklamasını caydırıcı veya küçümseyici bir dille yazmayın.
- Aynı testte açıklama ile form alanlarını birlikte değiştirmeyin.
- Gerçekte esnek olan bir koşulu kesin kuralmış gibi yazmayın.
- Koşulu karşılamayan kullanıcıya gidebileceği başka bir yol (farklı ürün, bekleme listesi) göstermeden açıklamayı koymayın.
- Ayrımcılık doğuracak bir eleme kriterini uygunluk açıklaması olarak kullanmayın.

### EN

Stating at the top of the form who it is for (minimum budget, service area, required condition) screens out users who don’t fit up front and lightens the sales team’s load. The price: the total number of leads drops, and some eligible users on the borderline see themselves as excluded and give up.

**What to test**
- Note: Does eligibility information raise qualified leads?
- Volume loss: How much does the total lead count fall?
- Next test: Once the note is permanent, does wording the condition plainly or softly change qualified leads in a separate test?
- Wrong screening: Are users who are actually eligible screened out too?
- Segment: Do visitors from paid ads and organic visitors react differently to the eligibility note?

**KPIs to track**
- Qualified Lead Rate (per assigned visitor): Does the rate of leads that match the target profile, per visitor assigned to the form page, rise?
- Form Completion Rate: The total submission rate must not fall to an unacceptable degree.
- Qualification Rate per Lead: Does the share of eligible leads rise?
- Sales Team Screening Time: Does the screening load fall?
- Opportunity Win Rate: Does the conversion of incoming leads to sales rise?

**What not to do**
- Don’t write the eligibility note in a discouraging or condescending tone.
- Don’t change the note and the form fields in the same test.
- Don’t write a condition that is really flexible as if it were a hard rule.
- Don’t put the note up without showing users who don’t meet the condition another path (a different product, a waitlist).
- Don’t use a screening criterion that would be discriminatory as an eligibility note.

---

## Asıl formdan önce küçük bir ısındırma sorusu sormak tamamlama oranını artırır mı?

Değişken: Asıl formdan önceki ısındırma sorusu · Fark: ekle

Etiket: id=fs-021 · mercek=Çaba · düzey=akış · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does asking a small warm-up question before the main form raise completion?

EN-Variable: Warm-up question before the main form

Kullanıcıyı doğrudan çok alanlı bir formla karşılaştırmak yerine, önce tek ve kolay bir soruyla (“Hangisi size en yakın?”) başlamak küçük bir taahhüt yaratır; bu taahhüdün ardından gelen asıl formu tamamlama isteği güçlenebilir. Bu, alanları kademeli açmaktan farklıdır: orada aynı formun alanları sırayla açılır, burada asıl formdan önce ayrı, ilgisiz görünmeyen bir soru sorulur.

**Test edilmesi gerekenler**
- Sonraki test: Isındırma sorusu kazanırsa, kategori seçimi ile evet/hayır sorusu ayrı bir testte karşılaştırıldığında hangisi daha çok ilerletiyor?
- Taahhüt etkisi: Artış soruyu yanıtlamanın yarattığı taahhütten mi geliyor, yoksa soruyu yalnızca zaten istekli ziyaretçiler mi yanıtlıyor?
- Ek adım maliyeti: Isındırma sorusunun eklediği ekran, asıl forma hiç ulaşmayan ziyaretçi oranını artırıyor mu?
- Geri dönen ziyaretçi: Formu önceden görmüş ziyaretçi ısındırma sorusunu gereksiz bir engel gibi görüp daha sık mı atlıyor?
- Cihaz: Mobilde ısındırma adımı ayrı bir ekran gerektirdiğinde etkisi masaüstünden farklı mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Isındırma sorusuyla başlayan akış, doğrudan forma göre daha çok tamamlanıyor mu?
- Isındırma Sorusu Yanıtlama Oranı: Soruyu yanıtlayıp devam eden ziyaretçi oranı nedir?
- Toplam Süre: Isındırma adımı toplam tamamlama süresini kabul edilemez ölçüde uzatmamalı.
- Talep Başına Nitelik Oranı: Isındırma sorusu talebin niteliğini düşürmemeli.
- Form Tamamlama Oranı (geri dönen ziyaretçi): Formu önceden görmüş ziyaretçide ek adım tamamlamayı düşürmemeli.

**Yapılmaması gerekenler**
- Isındırma sorusunu asıl formla ilgisiz, dikkat dağıtıcı bir konu yapmayın.
- Aynı testte ısındırma sorusunun içeriğini ve asıl formun alan sayısını birlikte değiştirmeyin.
- Soruyu zorunlu hâle getirip atlama seçeneği sunmadan ilerlemeyi engellemeyin.
- Isındırma sorusunun cevabını, kullanıcıya söylemeden başka bir amaç (ör. segmentleme) için kullanmayın.
- Isındırma adımını, asıl formun alan sayısını azaltmanın yerine geçen bir çözüm gibi sunmayın; ikisi ayrı testtir.

### EN

Instead of confronting the user with a many-field form directly, starting with a single easy question (“Which one is closest to you?”) creates a small commitment, and the willingness to complete the main form that follows can grow. This differs from progressive field reveal: there the fields of the same form open in sequence; here a separate question that doesn’t look unrelated is asked before the main form.

**What to test**
- Next test: If the warm-up question wins, which advances people more when a category choice and a yes/no question are compared in a separate test?
- Commitment effect: Does the lift come from the commitment created by answering the question, or only from already motivated visitors answering it?
- Extra step cost: Does the screen the warm-up question adds raise the share of visitors who never reach the main form?
- Returning visitor: Does a visitor who has seen the form before see the warm-up question as an unnecessary barrier and skip it more often?
- Device: When the warm-up step needs a separate screen on mobile, is its effect different from desktop?

**KPIs to track**
- Form Completion Rate: Is the flow that starts with the warm-up question completed more than the direct form?
- Warm-up Question Response Rate: What share of visitors answer the question and continue?
- Total Time: The warm-up step must not lengthen total completion time to an unacceptable degree.
- Qualification Rate per Lead: The warm-up question must not lower lead quality.
- Form Completion Rate (returning visitors): For visitors who have seen the form before, the extra step must not lower completion.

**What not to do**
- Don’t make the warm-up question an unrelated, distracting topic.
- Don’t change the content of the warm-up question and the number of fields in the main form in the same test.
- Don’t make the question required and block progress without offering a way to skip.
- Don’t use the answer to the warm-up question for another purpose (such as segmentation) without telling the user.
- Don’t present the warm-up step as a substitute for reducing the number of fields in the main form; they are separate tests.

---

## Form alanının yanına veri gizliliği güvencesi eklemek kayıt oranını artırır mı?

Değişken: Alan yanındaki gizlilik güvence metni · Fark: ekle

Etiket: id=fs-022 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding a data-privacy assurance next to a form field raise sign-ups?

EN-Variable: Privacy assurance text next to the field

E-posta veya telefon isteyen bir form, kullanıcıda “bu bilgi spam’e mi dönüşecek” tereddüdü yaratabilir. Alanın hemen yanına kısa bir güvence metni (“E-postanızı kimseyle paylaşmayız”) koymak bu tereddüdü giderebilir, ama gereksiz yere hatırlatma da tam tersi bir etki yaratıp “neden bunu söylemeleri gerekti” şüphesi doğurabilir.

**Test edilmesi gerekenler**
- Varlık: Güvence metni eklemek kayıt oranını artırıyor mu, yoksa şüphe mi uyandırıyor?
- Fark edilme: Kullanıcılar güvence metnini gerçekten görüyor mu, yoksa alan doldurulurken metin gözden mi kaçıyor?
- Alan düzeyi: Güvence eklenen e-posta veya telefon alanında, alanı boş bırakıp formdan çıkma azalıyor mu?
- Sonraki test: Güvence kalıcı olursa, genel bir ifade ile spesifik bir taahhüt ayrı bir testte karşılaştırıldığında hangisi daha ikna edici?
- Segment: Hassas sayılabilecek bir bilgi (ör. telefon) istenen formlarda etki, yalnızca e-posta isteyen formdan farklı mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Güvence metni kayıt oranını artırıyor mu?
- Alan Bazlı Terk Oranı: İlgili alanda bırakma artmamalı.
- Güven Algısı (anket): Metin güveni artırdığını hissettiriyor mu, yoksa şüphe mi uyandırıyor? Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Sayfada Kalma Süresi: Ek metin okuma süresini kabul edilemez ölçüde uzatmamalı.
- Kayıt Sonrası Şikâyet: Verilen sözle kayıt sonrası gönderim davranışı tutarsızsa bu artmamalı; artıyorsa ayrı, engelleyici bir bulgudur.

**Yapılmaması gerekenler**
- Vermediğiniz bir sözü yazmayın; “asla paylaşmayız” derken üçüncü taraf pazarlama ortaklarıyla paylaşıyorsanız bu yanıltıcı bir vaattir.
- Aynı testte güvence metnini ve form alan sayısını birlikte değiştirmeyin.
- Metni, gerçek bir gizlilik politikası bağlantısının yerine geçecek şekilde sunmayın; ayrıntılı politika hâlâ erişilebilir olmalı.
- Güvence metnini o kadar büyük veya göze batan yapmayın ki asıl formu gölgelesin.
- Hedef pazarın veri koruma mevzuatının gerektirdiği açık rıza metnini bu güvence cümlesiyle karıştırıp eksik bırakmayın.

### EN

A form that asks for an email or phone number can raise the doubt “will this turn into spam?” A short assurance next to the field (“We never share your email”) can remove that doubt, but an unnecessary reminder can also backfire and raise the suspicion “why did they feel the need to say this?”

**What to test**
- Presence: Does adding an assurance text raise the sign-up rate, or does it raise suspicion?
- Noticing: Do users actually see the assurance, or does it slip past while they fill in the field?
- Field level: On the email or phone field with the assurance, does leaving the field empty and exiting the form decrease?
- Next test: Once the assurance is permanent, which is more convincing when a general statement and a specific commitment are compared in a separate test?
- Segment: On forms that ask for information that can count as sensitive (such as a phone number), is the effect different from forms that ask only for email?

**KPIs to track**
- Form Completion Rate: Does the assurance text raise the sign-up rate?
- Field-Level Abandonment Rate: Abandonment at the relevant field must not increase.
- Trust Perception (survey): Does the text make people feel it raised trust, or does it raise suspicion? The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms and is a diagnostic signal.
- Time on Page: The extra text must not lengthen reading time to an unacceptable degree.
- Post-Sign-up Complaints: If post-sign-up messaging behavior contradicts the promise, this must not increase; if it does, it is a separate, blocking finding.

**What not to do**
- Don’t write a promise you don’t keep; saying “we never share” while sharing with third-party marketing partners is a misleading promise.
- Don’t change the assurance text and the number of form fields in the same test.
- Don’t present the text as a replacement for a real link to the privacy policy; the detailed policy must stay accessible.
- Don’t make the assurance so large or conspicuous that it overshadows the form itself.
- Don’t confuse this assurance sentence with the explicit-consent text required by the target market’s data protection law, and leave that one incomplete.

---

## Tek seçimlik bir alanda radio button mu, açılır liste (dropdown) mu daha çok tamamlatıyor?

Değişken: Tek seçimlik alanın kontrol tipi · Fark: değiştir

Etiket: id=fs-023 · mercek=Çaba · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Radio buttons or a dropdown for a single-choice field: which gets more forms completed?

EN-Variable: Control type for a single-choice field

Radio button tüm seçenekleri aynı anda görünür kılar, kullanıcı tıklamadan karşılaştırma yapabilir ama seçenek sayısı arttıkça dikey yer kaplar. Dropdown yer kazandırır ve çok seçenekli durumlarda formu kısa gösterir, buna karşılık seçenekleri görmek için bir ek tıklama gerektirir ve mobilde platformun kendi bileşenine bağlı bir davranışa geçer; kullanıcı neyle karşılaşacağını göremeden tıklar.

**Test edilmesi gerekenler**
- Biçim: Radio button mu, dropdown mu ilgili alanın doldurulma oranını artırıyor?
- Atlanma: Dropdown’da alanı seçim yapmadan geçip gönderimde hata alan kullanıcı oranı radio button’a göre artıyor mu?
- Hata: Yanlış seçim oranı biçime göre değişiyor mu?
- Cihaz: Mobilde platformun kendi dropdown bileşeni radio button’a göre nasıl bir fark yaratıyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Biçim gönderimi artırıyor mu?
- Alan Bazlı Hata Oranı: Yanlış veya eksik seçim artmamalı.
- Ortalama Doldurma Süresi: İlgili alanı doldurma süresi uzamamalı.
- Alan Bazlı Terk Oranı: İlgili alanda bırakma artmamalı.
- Erişilebilirlik: Klavye ile gezinme ve ekran okuyucu davranışı biçime göre bozulmamalı.

**Yapılmaması gerekenler**
- Aynı testte biçimle birlikte seçenek sayısını veya sırasını değiştirmeyin.
- Dropdown’da bir seçeneği önceden seçili getirip kullanıcının fark etmeden onu onaylamasına yol açmayın.
- Çok az seçenek için dropdown, çok fazla seçenek için radio button önermeyin; ikisi de yanlış bağlamda dezavantajlıdır.
- Mobil platformun kendi dropdown bileşenini özel bir bileşenle değiştirip erişilebilirlik davranışını bozmayın.
- Tek bir alan tipinde ölçüp sonucu tüm tek seçimlik alanlara genellemeyin.

### EN

Radio buttons show all options at once, letting the user compare without clicking, but they take up vertical space as the number of options grows. A dropdown saves space and makes the form look short when there are many options, but it needs an extra click to see the options and on mobile switches to a behavior tied to the platform’s own component; the user clicks without seeing what they will meet.

**What to test**
- Format: Does a radio button or a dropdown raise the fill rate of the field?
- Skipping: With a dropdown, does the share of users who pass the field without choosing and get an error at submission rise compared with radio buttons?
- Error: Does the rate of wrong choices vary by format?
- Device: On mobile, what difference does the platform’s own dropdown component make compared with radio buttons?

**KPIs to track**
- Form Completion Rate: Does the format raise submissions?
- Field-Level Error Rate: Wrong or missing choices must not increase.
- Median Form Fill Time: The time to fill the field must not grow.
- Field-Level Abandonment Rate: Abandonment at the field must not increase.
- Accessibility Check: Keyboard navigation and screen-reader behavior must not break depending on the format.

**What not to do**
- Don’t change the number or order of options in the same test as the format.
- Don’t preselect an option in the dropdown so that the user confirms it without noticing.
- Don’t recommend a dropdown for very few options or radio buttons for very many; both are disadvantaged in the wrong context.
- Don’t replace the mobile platform’s own dropdown component with a custom one and break accessibility behavior.
- Don’t measure on one field type and generalize the result to all single-choice fields.
