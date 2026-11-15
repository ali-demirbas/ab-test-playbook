# Sepet ve Ödeme

Yolculuk aşaması: kullanıcı satın almaya karar verdi; sepet, kupon, adres/ödeme formları ve tamamlanma anı. Huninin en pahalı kayıp noktası. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## CTA buton rengi dönüşümü etkiler mi?

Değişken: CTA buton rengi · Fark: değiştir

Etiket: id=cc-001 · mercek=Netlik · düzey=görsel · sektör=e-ticaret · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Does the CTA button color affect conversion?

EN-Variable: CTA button color

Buton rengi klasik bir test konusudur ama genelde yanlış kurulur: “kırmızı mı yeşil mi” sorusunun evrensel bir cevabı yoktur. Test edilen rengin kendisi değil, butonun sayfadaki öbür öğelerden ayrışma derecesidir: ürün sayfasında sepete ekle butonu galeri, fiyat ve indirim etiketleri arasında, sepet ve ödeme adımında ise ikincil butonlar arasında öne çıkmak zorundadır. Riski: yeni renk indirim etiketiyle aynı tona düşüp fiyat bilgisiyle karışabilir, ya da tıklama artışı yalnızca yenilik etkisinden gelip birkaç gün içinde sönebilir. Test tek sayfadaki tek butonun rengini değiştirir; aynı akıştaki öbür sayfaların butonları sabit kalır.

**Test edilmesi gerekenler**
- Kontrast: Sayfanın geri kalanına göre en çok öne çıkan renk tıklamayı artırıyor mu?
- Ayırt edilme: Yeni renk butonu fiyat ve indirim etiketlerinden ayırt edilir kılıyor mu, yoksa onlarla karıştırıyor mu?
- Yenilik etkisi: Renk değişiminin getirdiği tıklama artışı ilk haftadan sonra sönüyor mu, kalıcı mı?
- Cihaz: Butonun ekran genişliğini kapladığı mobilde renk değişimi, butonun küçük kaldığı masaüstüne göre tıklamayı daha az mı etkiliyor?
- Erişilebilirlik: Seçilen renk, buton metniyle arasındaki kontrast oranında (WCAG) eşiği geçiyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Renk değişikliği tamamlanan siparişe yansıyor mu?
- Tıklama Oranı (CTR): Tanı metriği; buton daha çok fark edilip tıklanıyor mu?
- Sepete Ekleme Oranı: İlk aksiyon değişiyor mu?
- Yanlış Tıklama Oranı: Yeni renk ikincil butonlarla karışıp yanlış butona tıklamayı artırmamalı.
- Marka Algısı (anket): Ölçülüyorsa düşmemeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.

**Yapılmaması gerekenler**
- Aynı testte renk ile buton metnini veya boyutunu birlikte değiştirmeyin.
- Erişilebilirlik kontrastını sağlamayan bir renk seçmeyin (görme engelli kullanıcı dışlanır).
- Marka kılavuzuna aykırı rengi test onayı almadan canlıya almayın.
- Tek bir sayfada kazanan rengi tüm siteye otomatik yaymayın; sayfa bağlamı değişir.
- Kazanan rengi ikincil butonlara da uygulayıp birincil ile ikincil buton ayrımını silmeyin.

### EN

The button color is a classic test subject but is usually set up wrong: there is no universal answer to “red or green?”. What is really being tested is not the color itself but how far the button stands apart from everything else on the page. On a product page the add-to-cart button has to stand out among the gallery, price and discount labels; in the cart and payment steps it has to stand out among secondary buttons. Risk: the new color may land in the same tone as the discount label and get mixed up with price information, or the click gain may come purely from novelty and fade within a few days. The test changes the color of one button on one page; buttons on the other pages of the same flow stay fixed.

**What to test**
- Contrast: Does the color that stands out most from the rest of the page raise clicks?
- Distinctness: Does the new color make the button distinguishable from price and discount labels, or does it blend with them?
- Novelty effect: Does the click gain from the color change fade after the first week, or does it last?
- Device: On mobile, where the button spans the screen width, does the color change affect clicks less than on desktop, where the button stays small?
- Accessibility: Does the chosen color pass the WCAG contrast threshold against the button text?

**KPIs to track**
- Conversion Rate (CR): Does the color change show up in completed orders?
- Click-Through Rate (CTR): Diagnostic metric; is the button noticed and clicked more?
- Add-to-Cart Rate: Does the first action change?
- Misclick Rate: The new color must not blend with secondary buttons and raise clicks on the wrong button.
- Brand Perception (survey): If measured, it must not drop. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms, and this is a diagnostic signal.

**What not to do**
- Don’t change the color together with the button text or size in the same test.
- Don’t pick a color that fails accessibility contrast (users with low vision are excluded).
- Don’t put a color that breaks the brand guidelines live without test approval.
- Don’t automatically roll the winning color out across the whole site from a single page; page context changes.
- Don’t apply the winning color to secondary buttons and erase the distinction between primary and secondary buttons.

---

## Sepet ve ödeme adımlarında tekrarlayan CTA’ları azaltmak dönüşümü artırır mı?

Değişken: Tekrarlayan CTA sayısı · Fark: kaldır

Etiket: id=cc-002 · mercek=Netlik · düzey=görsel · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does cutting repeated CTAs in the cart and checkout steps raise conversion?

EN-Variable: Number of repeated CTAs

Aynı adımda aynı işi yapan birden fazla CTA kullanıcı odağını bölerek karar süresini uzatabilir. Burada test edilen CTA sayısıdır: tekrarlayan butonları kaldırmanın dönüşüme etkisi ölçülür. “İkincil aksiyonu bağlantı mı, buton mu yapmalı?” senaryosundan (`ui-elements.md`) farkı: o senaryo farklı işlevdeki ikincil aksiyonun biçimini değiştirir, bu senaryo aynı işlevdeki CTA’ların sayısını azaltır.

**Test edilmesi gerekenler**
- Sayı: Tek CTA mı, birden fazla CTA mı daha çok dönüştürüyor?
- Tekrar: Aynı işlevdeki CTA’lar kaldırılınca odak artıyor mu?
- Akış: Tek CTA ödeme adımlarında ilerlemeyi hızlandırıyor mu?
- Cihaz: Tekrarlayan CTA’ların ekranın çoğunu kapladığı mobilde bunları kaldırmak, masaüstüne göre ilerlemeyi daha çok mu hızlandırıyor?
- Kararsızlık: Fazla CTA’lı sayfada yukarı-aşağı gezinme artıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sade CTA yapısı satın almayı artırıyor mu?
- Tıklama Oranı (CTR): Tek net CTA tıklamayı artırıyor mu?
- Adım Tamamlama Oranı: Bir sonraki adıma geçiş kolaylaşıyor mu?
- Mobil Dönüşüm Oranı (CR): Kalan tek CTA’nın ekran dışında kalabildiği mobilde satın alma düşmemeli.
- Karar Süresi: Belirgin şekilde uzamamalı.

**Yapılmaması gerekenler**
- Tüm CTA’ları birden kaldırmayın; kullanıcı yönsüz kalır.
- Yalnızca tekrarlayan ve işlevsiz CTA’ları çıkarın.
- Aynı testte CTA sayısı ile kalan CTA’nın metnini birlikte değiştirmeyin.
- Mobilde kritik CTA’nın ekran dışına itilmesine izin vermeyin.
- İkincil aksiyonu birincil CTA ile aynı görsel ağırlıkta yapmayın.

### EN

Several CTAs doing the same job in the same step can split the user’s focus and lengthen the decision. What is tested here is the number of CTAs: the effect of removing repeated buttons on conversion. How it differs from the “Should the secondary action be a link or a button?” scenario (`ui-elements.md`): that scenario changes the form of a secondary action with a different function, this one cuts the number of CTAs with the same function.

**What to test**
- Count: Does a single CTA or several CTAs convert more?
- Repetition: Does focus improve when CTAs with the same function are removed?
- Flow: Does a single CTA speed up progress through the payment steps?
- Device: On mobile, where repeated CTAs fill most of the screen, does removing them speed up progress more than on desktop?
- Hesitation: Does up-and-down scrolling increase on a page with too many CTAs?

**KPIs to track**
- Conversion Rate (CR): Does a clean CTA structure raise purchases?
- Click-Through Rate (CTR): Does a single clear CTA raise clicks?
- Step Completion Rate: Does moving to the next step get easier?
- Mobile Conversion Rate (CR): Purchases must not drop on mobile, where the remaining CTA can fall off-screen.
- Time to Decision: Must not lengthen noticeably.

**What not to do**
- Don’t remove all CTAs at once; the user is left without direction.
- Remove only the repeated, non-functional CTAs.
- Don’t change the number of CTAs and the text of the remaining CTA in the same test.
- Don’t let the critical CTA be pushed off-screen on mobile.
- Don’t give the secondary action the same visual weight as the primary CTA.

---

## Ücretsiz kargo çubuğu sepet tutarını artırıyor mu?

Değişken: Ücretsiz kargo ilerleme çubuğu · Fark: ekle

Etiket: id=cc-003 · mercek=Fiyat · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a free-shipping progress bar raise cart value?

EN-Variable: Free-shipping progress bar

Ücretsiz kargoya ne kadar kaldığını göstermek, sepeti büyütme motivasyonunu yükseltebilir. Bu etkinin gerçekte ne kadar olduğu ölçülmelidir.

**Test edilmesi gerekenler**
- Motivasyon: Çubuk “ücretsiz kargoya ulaşmak için ürün ekle” davranışını artırıyor mu?
- Fark edilme: Kullanıcılar çubuğu görüp ücretsiz kargoya kalan tutarı doğru okuyor mu?
- Eşiğe uzaklık: Eşiğe az kalan sepetlerde çubuğun etkisi, eşiğe uzak sepetlerdekinden daha mı büyük?
- Cihaz: Mobil ve masaüstünde karar süresi farklı mı?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çubuk, dönüşümü düşürmeden toplam geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Çubuk sepet toplamını artırıyor mu?
- Sepete Ekleme Oranı: Daha fazla ürün ekleniyor mu?
- Ödeme Adımına Geçiş Oranı: Ödemeye geçiş düşmemeli.
- Sepet Terk Oranı: Yükselmemeli.

**Yapılmaması gerekenler**
- İlerleme çubuğunu CTA’nın önüne geçecek şekilde yerleştirmeyin.
- Eşiğe kalan tutarı gerçek sepet hesabından farklı göstermeyin.
- Mobilde çubuğu görünmeyecek kadar aşağı koymayın.
- Aynı testte renk, eşik ve metni birlikte değiştirmeyin.
- Eşiğe ulaşıldığında geri bildirim vermeyi atlamayın.

> **Pazar notu:** Ücretsiz kargo eşiğinin psikolojik ağırlığı pazara göre değişir: kargo ücretinin sepete oranı, teslimat süresi beklentisi ve rakiplerin eşik seviyesi farklı pazarlarda farklıdır. Eşik tutarını başka bir pazarın rakamından kopyalamayın, kendi sepet dağılımınızdan türetin.

### EN

Showing how much is left to reach free shipping can raise the motivation to grow the cart. How large this effect really is has to be measured.

**What to test**
- Motivation: Does the bar increase the “add an item to get free shipping” behavior?
- Noticeability: Do users see the bar and read the remaining amount correctly?
- Distance to threshold: Is the bar’s effect larger on carts close to the threshold than on carts far from it?
- Device: Does decision time differ on mobile and desktop?

**KPIs to track**
- Revenue per Visitor (RPV): Does the bar raise total revenue without lowering conversion?
- Average Order Value (AOV): Does the bar raise the cart total?
- Add-to-Cart Rate: Are more items added?
- Proceed-to-Payment Rate: Must not drop.
- Cart Abandonment Rate: Must not rise.

**What not to do**
- Don’t place the progress bar so that it overshadows the CTA.
- Don’t show a remaining amount that differs from the real cart calculation.
- Don’t put the bar so low on mobile that it goes unseen.
- Don’t change color, threshold and text together in the same test.
- Don’t skip the feedback when the threshold is reached.

> **Market note:** The psychological weight of a free-shipping threshold varies by market: the ratio of shipping fee to cart value, delivery-time expectations and competitors’ threshold levels differ from one market to the next. Don’t copy the threshold amount from another market’s figure; derive it from your own cart distribution.

---

## Açık kupon kodu alanı sepet terkini artırır mı?

Değişken: Kupon kodu alanının görünürlüğü · Fark: değiştir

Etiket: id=cc-004 · mercek=Fiyat · düzey=görsel · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does an open coupon code field increase cart abandonment?

EN-Variable: Visibility of the coupon code field

Görünür bir kupon kutusu, kodu olmayan kullanıcıyı “indirim arayayım” diye siteden çıkarabilir. Kodu bağlantı arkasına almak bu kaçağı kapatabilir ama kampanya kullanımını düşürebilir.

**Test edilmesi gerekenler**
- Kaçak: Kupon alanını bağlantı arkasına almak terk oranını düşürüyor mu?
- Segment: Yeni ve dönen kullanıcıda kupon arama davranışı farklı mı?
- Sonraki test: Kupon alanı bağlantı arkasındayken bağlantı metni (“İndirim kodum var” / “Kupon kullan”) ayrı bir testte kod kullanımını değiştiriyor mu?
- Kampanya: Kampanya dönemlerinde etki tersine dönüyor mu?
- Hata: Kod girip başarısız olan kullanıcının terk oranı ne kadar?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Kaçak kapanırken indirim kullanımındaki değişim toplam geliri artırıyor mu?
- Sipariş Tamamlama Oranı: Kupon kutusu kaçağı kapanıyor mu?
- Kuponlu Sipariş Veren Ziyaretçi Oranı: Kuponu olan kullanıcı alanı bulabilmeli; atanan ziyaretçi başına kuponlu sipariş düşmemeli. Geçti ölçütü: geçerli kod iki kolda da girilir, uygulanır, indirim toplama yansır ve hata mesajı aynıdır.
- Ödeme Adımı Terk Oranı: Doğrudan hedef davranış.
- Duyurulan Aksiyonun Tamamlanma Oranı: Aktif kampanyanın aksiyonunu tamamlayan atanan ziyaretçi oranı düşmemeli.

**Yapılmaması gerekenler**
- Kupon alanını tamamen kaldırmayın; kodu olan kullanıcı öfkelenir.
- Geçersiz kod hatasını belirsiz bırakmayın.
- Kodu olan kullanıcının alanı bulamayıp indirimsiz ödemesini gelir kazancı saymayın.
- Kupon alanını CTA altına gizleyip fark edilmez yapmayın.
- Aynı testte hem konumu hem metni değiştirmeyin.

### EN

A visible coupon box can send a user without a code off the site to “hunt for a discount”. Putting the code behind a link can close this leak but may lower campaign usage.

**What to test**
- Leak: Does putting the coupon field behind a link lower the abandonment rate?
- Segment: Does coupon-hunting behavior differ between new and returning users?
- Next test: With the coupon field behind a link, does the link text (“I have a discount code” / “Use coupon”) change code usage in a separate test?
- Campaign: Does the effect reverse during campaign periods?
- Error: What is the abandonment rate of users who enter a code and fail?

**KPIs to track**
- Revenue per Visitor (RPV): With the leak closed, does the change in discount usage raise total revenue?
- Checkout Completion Rate: Is the coupon box leak closing?
- Visitors Placing a Coupon Order Rate: A user who has a coupon must be able to find the field; coupon orders per assigned visitor must not drop. Pass criterion: a valid code is entered in both arms, applied, the discount reflects in the total, and the error message is the same.
- Payment Step Abandonment Rate: The direct target behavior.
- Announced Action Completion Rate: The share of assigned visitors who complete the action of an active campaign must not drop.

**What not to do**
- Don’t remove the coupon field entirely; a user who has a code gets angry.
- Don’t leave the invalid-code error vague.
- Don’t count a user who couldn’t find the field and paid without the discount as a revenue gain.
- Don’t hide the coupon field under the CTA so it goes unnoticed.
- Don’t change both the position and the text in the same test.

---

## Üye olmadan ödeme seçeneği işe yarar mı?

Değişken: Misafir ödeme seçeneği · Fark: ekle

Etiket: id=cc-005 · mercek=Çaba · düzey=sürtünme · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does a guest checkout option pay off?

EN-Variable: Guest checkout option

Zorunlu üyelik satın alma sürecini uzatır ve terk oranını yükseltebilir. Misafir ödemenin dönüşüme etkisi ölçülmelidir.

**Test edilmesi gerekenler**
- Kayıt dengesi: Misafir seçeneğinin getirdiği ek sipariş, kaybedilen yeni üye kaydını telafi ediyor mu?
- Cihaz: Mobilde misafir ödeme seçeneği masaüstüne göre daha mı çok tercih ediliyor?
- Kategori: Moda ve hızlı tüketimde misafir ödeme daha mı çok tercih ediliyor?
- Kampanya: Yoğun dönemlerde etki değişiyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Misafir ödeme satın almayı artırıyor mu?
- Destek Talebi: Hesapsız siparişte takip ve iade için açılan talepler artmamalı.
- Görev Tamamlama Süresi (checkout): Süreç kısalıyor mu?
- Kayıt Oranı: Ciddi biçimde düşmemeli.
- Tekrar Satın Alma Oranı (60 gün): Misafir kullanıcı geri dönmeli.

**Yapılmaması gerekenler**
- Misafir ödemede gereksiz bilgi istemeyin.
- “Üye olmadan devam et” butonunu küçültmeyin veya gizlemeyin.
- Satın alma sonrası kayıt çağrısını agresif tekrar etmeyin.
- Misafir siparişini sonradan hesaba bağlama yolunu kapatmayın.
- Aynı testte hem misafir seçeneğini hem form alanlarını değiştirmeyin.

### EN

Mandatory registration lengthens the purchase process and can raise abandonment. The effect of guest checkout on conversion has to be measured.

**What to test**
- Sign-up balance: Do the extra orders from the guest option make up for the new account sign-ups lost?
- Device: Is guest checkout chosen more on mobile than on desktop?
- Category: Is guest checkout chosen more in fashion and fast-moving goods?
- Campaign: Does the effect change in peak periods?

**KPIs to track**
- Conversion Rate (CR): Does guest checkout raise purchases?
- Support Contact Rate: Requests for tracking and returns on orders without an account must not rise.
- Task Completion Time (checkout): Does the process get shorter?
- Sign-up Rate: Must not drop sharply.
- Repeat Purchase Rate (60 days): Guest users should come back.

**What not to do**
- Don’t ask for unnecessary information in guest checkout.
- Don’t shrink or hide the “Continue without an account” button.
- Don’t repeat the post-purchase sign-up prompt aggressively.
- Don’t close off the way to link a guest order to an account later.
- Don’t change both the guest option and the form fields in the same test.

---

## Tek sayfa checkout mu, çok adımlı checkout mu?

Değişken: Checkout adım yapısı · Fark: değiştir

Etiket: id=cc-006 · mercek=Çaba · düzey=akış · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: One-page checkout or multi-step checkout?

EN-Variable: Checkout step structure

Ödeme akışında kullanıcı aynı bilgileri (iletişim, adres, kargo seçimi, ödeme) iki biçimde doldurabilir: tek uzun sayfada ya da her biri ayrı ekranda olan adımlarda. Tek sayfa toplam tutarı ve kalan işi baştan gösterir, adımlar arası geçişteki bekleme ve kaybı kaldırır; ama mobilde uzun bir form duvarı gibi görünür ve ekranın dışında kalan bir hata mesajı gözden kaçar. Çok adımlı akış her ekranda tek bir işi sorar ve ilk adımı bitireni ilerletir; ama her geçiş bir yükleme ve bir terk noktasıdır, kargo ücreti son adıma kalırsa sürpriz yaratır. Alanlar, sıraları ve ödeme yöntemleri iki kolda aynıdır; değişen yalnızca aynı alanların ekranlara bölünüp bölünmediğidir. Cüzdanla tek dokunuş ödeme bu iki yapının dışında kalan ayrı bir değişkendir; akışta varsa iki kolda aynı yerde durur. “Çok adımlı form mu, tek sayfa form mu daha çok talep getiriyor?” (`saas-b2b.md`) senaryosundan farkı: orada form bir talep toplar ve sonraki adımı satış ekibi yürütür, burada akış ödemeyle biter ve kargo ile toplam tutar kararı etkiler.

**Test edilmesi gerekenler**
- Toplam etki: Tek sayfa akışı, ödemeye başlayanların siparişi tamamlama payını artırıyor mu?
- Hata görünürlüğü: Tek sayfada ekran dışında kalan hata mesajı gönderim denemelerini tekrarlatıyor mu, çok adımlı akışta hata aynı ekranda mı düzeltiliyor?
- Kayıp noktası: Çok adımlı akışta terk hangi geçişte yoğunlaşıyor, tek sayfada kullanıcı formun neresinde duruyor?
- Dönen kullanıcı: Bilgileri kayıtlı dönen kullanıcı tek sayfada, alanları ilk kez dolduran yeni kullanıcı çok adımlı akışta mı daha çok tamamlıyor?
- Cihaz: Tek sayfanın uzun kaydırma gerektirdiği mobilde çok adımlı akış, geniş ekranlı masaüstünde ise tek sayfa akışı mı kazanıyor?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Checkout’a ulaşan ziyaretçilerin (iki kolda aynı tetikleyici) siparişi tamamlama oranı artıyor mu?
- Alan Bazlı Terk Oranı: Tanı metriği; formu bırakanlar son dokundukları alana göre nerede duruyor?
- Görev Tamamlama Süresi (checkout): Checkout’a girişten siparişe kadar geçen süre kısalıyor mu?
- Doğrulama Hatası Oranı: Tek sayfada hata alan gönderim denemeleri artmamalı.
- Destek Talebi: Sipariş ve ödeme sorunlarıyla ilgili talepler yükselmemeli.

**Yapılmaması gerekenler**
- Aynı testte adım yapısıyla birlikte alanların sayısını, sırasını ya da ödeme yöntemi setini değiştirmeyin.
- Cüzdanla tek dokunuş ödemeyi yalnız bir kolda öne almayın; varsa iki kolda aynı yerde durur.
- Çok adımlı kolda adım göstergesini kaldırıp kullanıcıyı kaç adım kaldığını bilmeden bırakmayın.
- Kargo ücretini ve toplam tutarı son adıma saklamayın; iki kolda da ilk görüldükleri yer aynıdır.
- Mobilde klavye açıldığında sipariş özetinin ya da hata mesajının ödeme butonunu kapatmasına izin vermeyin.

### EN

In the payment flow a user can fill in the same information (contact, address, shipping choice, payment) in two ways: on one long page, or in steps that each sit on a separate screen. One page shows the total and the remaining work from the start and removes the waiting and loss between steps, but on mobile it looks like a wall of form fields, and an error message that falls off-screen gets missed. A multi-step flow asks for one thing per screen and moves along whoever finishes the first step, but every transition is a load and a drop-off point, and if the shipping fee is left to the last step it creates a surprise. The fields, their order and the payment methods are the same in both arms; the only difference is whether the same fields are split across screens. One-tap wallet payment is a separate variable outside these two structures; if the flow has it, it stays in the same place in both arms. How it differs from the “Multi-step form or single-page form: which brings more requests?” scenario (`saas-b2b.md`): there the form collects a lead and the sales team runs the next step, here the flow ends in payment and shipping and the total affect the decision.

**What to test**
- Total effect: Does the one-page flow raise the share of people who start payment and complete the order?
- Error visibility: On one page, does an error message that falls off-screen cause repeated submit attempts, and in the multi-step flow is the error fixed on the same screen?
- Drop-off point: In the multi-step flow, at which transition does abandonment concentrate, and on one page where in the form do users stop?
- Returning user: Do returning users with saved details complete more on one page, and new users filling the fields for the first time more in the multi-step flow?
- Device: Does the multi-step flow win on mobile, where one page needs long scrolling, and the one-page flow on wide-screen desktop?

**KPIs to track**
- Checkout Completion Rate: Does the rate at which visitors who reach checkout (same trigger in both arms) complete the order rise?
- Field-Level Abandonment Rate: Diagnostic metric; at which field, by last field touched, do the people who leave the form stop?
- Task Completion Time (checkout): Does the time from entering checkout to the order get shorter?
- Validation Error Rate: Submit attempts that hit errors on one page must not rise.
- Support Contact Rate: Requests about orders and payment problems must not rise.

**What not to do**
- Don’t change the number or order of fields, or the payment method set, in the same test as the step structure.
- Don’t bring one-tap wallet payment forward in only one arm; if it exists, it stays in the same place in both arms.
- Don’t remove the step indicator in the multi-step arm and leave the user not knowing how many steps remain.
- Don’t hide the shipping fee and total until the last step; the place where they are first seen is the same in both arms.
- Don’t let the order summary or an error message cover the payment button when the keyboard opens on mobile.

---

## Adres formundaki alan sayısını azaltmak tamamlamayı artırır mı?

Değişken: Adres formundaki alan sayısı · Fark: kaldır

Etiket: id=cc-007 · mercek=Çaba · düzey=form · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does cutting the number of address form fields raise completion?

EN-Variable: Number of fields in the address form

Her ek form alanı bir sürtünme noktasıdır. Posta koduyla otomatik il/ilçe doldurma veya adres önerisi kullanmak, mobilde yazma yükünü ciddi biçimde azaltabilir.

**Test edilmesi gerekenler**
- Alan sayısı: Azaltmak tamamlama oranını artırıyor mu?
- Sonraki test: Alan sayısı sabitken adres önerisi ile posta kodundan doldurma ayrı bir testte karşılaştırıldığında hangisi daha hızlı tamamlatıyor?
- Birleştirme: Ad ve soyadı tek alanda toplamak hata oranını artırıyor mu?
- Cihaz: Mobilde etki masaüstünden daha mı yüksek?
- Segment: Kayıtlı adresi olan kullanıcıda fark kalıyor mu?

**Takip edilecek ana KPI’lar**
- Adım Tamamlama Oranı (adres adımı): Adres adımına ulaşan kullanıcıların (iki kolda aynı tetikleyici) adımı bitirme oranı artıyor mu?
- Form Doldurma Süresi: Kısalıyor mu?
- Sipariş Tamamlama Oranı: Zincirin sonuna yansıyor mu?
- Hatalı Adres / Teslimat Hatası: Artmamalı; en kritik guardrail.
- Destek Talebi: Adres düzeltme talepleri yükselmemeli.

**Yapılmaması gerekenler**
- Otomatik doldurmayı düzenlenemez yapmayın.
- Kargo için gerçekten gereken alanı kaldırmayın; hassas alanlarda önce ara yöntemleri (isteğe bağlı yapmak, gerekçe yazmak, sonraya ertelemek, daha az veri istemek) değerlendirin.
- Aynı testte hem alan sayısını hem validasyon kurallarını değiştirmeyin.
- Hata mesajlarını alan altından kaldırmayın.
- Posta kodundan doldurulan il/ilçeyi kullanıcıya göstermeden siparişe yazmayın.

### EN

Every extra form field is a friction point. Filling in city and district automatically from the postal code, or using address suggestions, can cut the typing load sharply on mobile.

**What to test**
- Field count: Does cutting fields raise the completion rate?
- Next test: With the field count fixed, which gets users to complete faster when address suggestions and postal-code autofill are compared in a separate test?
- Merging: Does collecting first and last name in one field raise the error rate?
- Device: Is the effect higher on mobile than on desktop?
- Segment: Does the difference remain for users with a saved address?

**KPIs to track**
- Step Completion Rate (address step): Does the share of users who reach the address step (same trigger in both arms) and finish it rise?
- Form Fill Time: Does it get shorter?
- Checkout Completion Rate: Does it carry through to the end of the chain?
- Wrong Address / Delivery Failure Rate: Must not rise; the most critical guardrail.
- Support Contact Rate: Address correction requests must not rise.

**What not to do**
- Don’t make autofill non-editable.
- Don’t remove a field that shipping really needs; for sensitive fields first consider intermediate methods (making it optional, giving a reason, deferring it, asking for less data).
- Don’t change both the number of fields and the validation rules in the same test.
- Don’t remove error messages from under the field.
- Don’t write the city/district filled from the postal code into the order without showing it to the user.

---

## Adet seçiminin görünürlüğü davranışı etkiliyor mu?

Değişken: Adet seçicinin görünürlüğü · Fark: değiştir

Etiket: id=cc-008 · mercek=Netlik · düzey=görsel · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does the visibility of the quantity selector change behavior?

EN-Variable: Visibility of the quantity selector

Sepette adet seçimini daha net sunmak, kullanıcıların adedi artırma davranışını ve sepet değerini etkileyebilir.

**Test edilmesi gerekenler**
- Cihaz: Mobilde ve masaüstünde adet artırma davranışı aynı mı?
- Görünürlük: Görünürlük artınca adet artırma davranışı değişiyor mu?
- Buton: “+ / −” butonlarını belirginleştirmek ekleme hızını artırıyor mu?
- Hata: Net adet alanı yanlışlıkla ürün silmeyi azaltıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Adet görünürlüğü dönüşümü düşürmeden toplam geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Adet artırımı sepet değerini yükseltiyor mu?
- Adet Değişim Oranı: Adet daha sık mı değiştiriliyor?
- Sepetten Silme Oranı: Yanlışlıkla silme artmamalı.
- Sipariş Tamamlama Oranı: Düşmemeli.

**Yapılmaması gerekenler**
- Adet butonlarını CTA’yı gölgede bırakacak kadar büyütmeyin.
- Aynı testte hem silme/favori ikonlarını hem adet alanını değiştirmeyin.
- Silme ikonunu görünmeyen bir yere taşımayın; kontrol kaybı hissi yaratır.
- Adet değişiminde tam sayfa yenileme yapmayın.
- Mobilde adet butonlarının üst üste binmesine izin vermeyin.

### EN

Presenting quantity selection more clearly in the cart can affect how users increase quantity and what the cart is worth.

**What to test**
- Device: Is quantity-increase behavior the same on mobile and desktop?
- Visibility: Does quantity-increase behavior change as visibility goes up?
- Button: Does making the “+ / −” buttons more prominent raise the speed of adding?
- Error: Does a clear quantity field reduce accidental item removal?

**KPIs to track**
- Revenue per Visitor (RPV): Does quantity visibility raise total revenue without lowering conversion?
- Average Order Value (AOV): Does increasing quantity raise cart value?
- Quantity Change Rate: Is quantity changed more often?
- Cart Removal Rate: Accidental removal must not rise.
- Checkout Completion Rate: Must not drop.

**What not to do**
- Don’t enlarge the quantity buttons so far that they overshadow the CTA.
- Don’t change both the delete/favorite icons and the quantity field in the same test.
- Don’t move the delete icon somewhere it can’t be seen; it creates a feeling of lost control.
- Don’t reload the whole page on a quantity change.
- Don’t let the quantity buttons overlap on mobile.

---

## Sepetteki ürün önerileri satın almayı artırır mı?

Değişken: Sepetteki tamamlayıcı ürün önerileri · Fark: ekle

Etiket: id=cc-009 · mercek=Uygunluk · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Do product recommendations in the cart raise purchases?

EN-Variable: Complementary product recommendations in the cart

Sepet adımında tamamlayıcı ürün göstermek ortalama sepet tutarını yükseltebilir ama asıl akıştan uzaklaştırma riski taşır.

**Test edilmesi gerekenler**
- Cihaz: Mobil dar ekranda öneri alanı sipariş özetini ve CTA’yı aşağı itiyor mu?
- Etkileşim: Kullanıcılar öneri alanına tıklayıp inceliyor mu?
- Akıştan sapma: Öneri kartına tıklayan kullanıcılar ürün sayfasına gidip sepete geri dönmeden ayrılıyor mu?
- Sayı: Öneri sayısı kaç olmalı? (2 / 4 / 6)

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Öneriler dönüşümü düşürmeden toplam geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Öneriler sepet değerini yükseltiyor mu?
- Öneriden Sepete Ekleme Oranı: Önerilerden ekleme yapılıyor mu?
- Sipariş Tamamlama Oranı: Öneri alanı akışı bozup tamamlamayı düşürmemeli.
- Öneri Tıklama Oranı: Tanı metriği; kullanıcılar önerilere tıklıyor mu?

**Yapılmaması gerekenler**
- Sepet alanını kalabalıklaştırmayın; asıl akıştan uzaklaştırır.
- Alakasız veya stokta olmayan ürün önermeyin.
- Aynı testte öneri alanını eklerken sipariş özetinin veya CTA’nın yerini de değiştirmeyin.
- Öneri kartında, eklenince değişecek toplam tutarı veya kargo ücretini gizlemeyin.
- Önerileri “Siparişi Tamamla” butonunun üstüne koymayın.

### EN

Showing complementary products in the cart step can raise average order value but risks drawing users away from the main flow.

**What to test**
- Device: On a narrow mobile screen, does the recommendation area push the order summary and the CTA down?
- Engagement: Do users click into and look through the recommendation area?
- Flow diversion: Do users who click a recommendation card go to the product page and leave without returning to the cart?
- Count: How many recommendations should there be? (2 / 4 / 6)

**KPIs to track**
- Revenue per Visitor (RPV): Do the recommendations raise total revenue without lowering conversion?
- Average Order Value (AOV): Do the recommendations raise cart value?
- Recommendation Add-to-Cart Rate: Are items added from the recommendations?
- Checkout Completion Rate: The recommendation area must not disrupt the flow and lower completion.
- Recommendation Click Rate: Diagnostic metric; do users click the recommendations?

**What not to do**
- Don’t crowd the cart area; it pulls users away from the main flow.
- Don’t recommend irrelevant or out-of-stock products.
- Don’t move the order summary or the CTA in the same test in which you add the recommendation area.
- Don’t hide, on the recommendation card, the total or shipping fee that will change once the item is added.
- Don’t put the recommendations above the “Complete Order” button.

---

## Kargo eşiğini yükseltmek sepet ortalamasını artırır mı?

Değişken: Ücretsiz kargo eşik tutarı · Fark: değiştir

Etiket: id=cc-010 · mercek=Fiyat · düzey=teklif · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does raising the free-shipping threshold raise average order value?

EN-Variable: Free-shipping threshold amount

Ücretsiz kargo sınırı sepeti büyütmek için güçlü bir teşviktir, ancak eşik fazla yükselirse kullanıcıyı kaçırır. Dengenin nerede olduğu ölçülmelidir.

**Test edilmesi gerekenler**
- Eşik: 500, 750 ve 1.000 TL’de davranış nasıl değişiyor?
- Sonraki test: Yeni eşik sabitken eşik bilgisinin ürün sayfasında mı sepette mi duyurulduğu ayrı bir testte sepet tutarını değiştiriyor mu?
- Kampanya: İndirim döneminde eşiğe yaklaşma isteği artıyor mu?
- Segment: Sadık müşteri ile yeni kullanıcı aynı tepkiyi mi veriyor?
- Eşik altı davranış: Sepeti yeni eşiğin hemen altında kalan kullanıcılar ürün ekliyor mu, yoksa siparişi bırakıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Eşik artışı AOV’yi şişirirken toplam geliri düşürmüyor mu?
- Ortalama Sepet Tutarı (AOV): Kullanıcılar eşiğe ulaşmak için daha çok ekliyor mu?
- Dönüşüm Oranı (CR): Eşik değişimi satın almayı düşürüyor mu?
- Ödeme Adımına Geçiş Oranı: Sepetten ödeme adımına geçiş artıyor mu?
- Kargo Maliyeti: Birim başına kargo gideri marjı eritmemeli.

**Yapılmaması gerekenler**
- Eşik yükselişini, sepetteki ürünlerin kargo durumunu habersizce değiştirecek şekilde uygulamayın.
- “Ücretsiz kargo” mesajını yanlış beklenti yaratacak şekilde kurmayın.
- Eşiği aşırı yükseltmeyin; kullanıcıyı kaçırır.
- Aynı testte eşik tutarı ile kalan tutar mesajını birlikte değiştirmeyin.
- Aynı kullanıcıya farklı oturumda veya cihazda farklı eşik göstermeyin; tutarsız eşik güveni bozar.

> Not: Bu senaryo, “Ücretsiz kargo çubuğu sepet tutarını artırıyor mu?” senaryosuyla ilişkilidir; o çubuğun varlığını, bu ise doğru eşik değerini test eder. İkisini aynı anda değiştirmeyin.

> **Pazar notu:** Kargo maliyetinin sepete oranı ve tüketicinin ücretsiz kargo beklentisi pazara göre değişir; bir pazarda kabul gören eşik artışı, başka bir pazarda doğrudan terke dönüşebilir.

### EN

A free-shipping threshold is a strong incentive to grow the cart, but set too high it drives the user away. Where the balance lies has to be measured.

**What to test**
- Threshold: How does behavior change at 500, 750 and 1,000 TL?
- Next test: With the new threshold fixed, does announcing it on the product page rather than in the cart change cart value in a separate test?
- Campaign: Does the urge to reach the threshold grow during a sale?
- Segment: Do loyal customers and new users react the same way?
- Below the threshold: Do users whose cart sits just under the new threshold add items, or abandon the order?

**KPIs to track**
- Revenue per Visitor (RPV): Does total revenue hold up while the higher threshold inflates AOV?
- Average Order Value (AOV): Do users add more to reach the threshold?
- Conversion Rate (CR): Does the threshold change lower purchases?
- Proceed-to-Payment Rate: Does the move from cart to the payment step increase?
- Shipping Cost: Shipping cost per unit must not erode the margin.

**What not to do**
- Don’t roll out the higher threshold in a way that silently changes the shipping status of items already in the cart.
- Don’t word the “Free shipping” message so that it sets a false expectation.
- Don’t raise the threshold too far; it drives users away.
- Don’t change the threshold amount and the remaining-amount message in the same test.
- Don’t show the same user a different threshold in another session or on another device; an inconsistent threshold breaks trust.

> Note: This scenario is related to the “Does a free-shipping progress bar raise cart value?” scenario; that one tests whether the bar exists, this one tests the right threshold value. Don’t change both at once.

> **Market note:** The ratio of shipping cost to cart value and shoppers’ free-shipping expectations vary by market; a threshold increase accepted in one market can turn straight into abandonment in another.

---

## Microcopy kullanıcı davranışını nasıl etkiliyor?

Değişken: Buton altı microcopy metni · Fark: değiştir

Etiket: id=cc-011 · mercek=Güven · düzey=metin · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: How does microcopy affect user behavior?

EN-Variable: Microcopy text under the button

Küçük metin değişiklikleri bile karar hızını, güven algısını ve yönlendirilme davranışını etkileyebilir. Bu test, buton altı mesajların ve güven verici ifadelerin dönüşüme etkisini ölçer.

**Test edilmesi gerekenler**
- Güven Mesajları: “Ücret alınmayacak” gibi ifadeler tıklama oranını artırıyor mu?
- Kullanıcı tipi: Yeni ve dönen kullanıcıda güven mesajının etkisi farklı mı?
- Yönlendirme: “Sadece 1 adım kaldı” gibi ifadeler ilerleme hızını artırıyor mu?
- Fiyat Şeffaflığı: “Vergiler dahil”, “İptal ücretsiz” bilgileri tamamlamayı artırıyor mu?
- Ton: Sıcak ve bilgilendirici üslup dönüşümü değiştiriyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Microcopy satın almaya yönlendiriyor mu?
- Tıklama Oranı (CTR): Butona tıklama artıyor mu?
- Form Tamamlama Oranı: Formu bitirme artıyor mu?
- İade veya İptal Oranı (30 gün): Metnin kurduğu beklenti (“İptal ücretsiz”, “Ücret alınmayacak”) sipariş sonrası iptali artırmamalı.
- Görev Tamamlama Süresi (adım): Uzamamalı.

**Yapılmaması gerekenler**
- Yanıltıcı, aşırı iddialı veya baskıcı ifadeler kullanmayın.
- Çok uzun microcopy yazmayın; okunabilirliği düşürür.
- Aynı testte microcopy, fiyat ve görseli birlikte değiştirmeyin.
- Microcopy’i ürünle alakasız kampanya mesajlarıyla doldurmayın.
- Mobilde microcopy alanını ekranı sıkıştıracak şekilde konumlandırmayın.

### EN

Even small text changes can affect decision speed, perceived trust and how users are guided. This test measures the effect on conversion of messages under the button and reassuring phrases.

**What to test**
- Trust messages: Do phrases such as “You won’t be charged” raise the click rate?
- User type: Does the effect of a trust message differ between new and returning users?
- Guidance: Do phrases such as “Just 1 step left” speed up progress?
- Price transparency: Does information such as “Taxes included” and “Free cancellation” raise completion?
- Tone: Does a warm, informative tone change conversion?

**KPIs to track**
- Conversion Rate (CR): Does the microcopy push users toward purchase?
- Click-Through Rate (CTR): Do clicks on the button rise?
- Form Completion Rate: Does finishing the form rise?
- Return or Cancellation Rate (30 days): The expectation the copy sets (“Free cancellation”, “You won’t be charged”) must not raise post-order cancellations.
- Task Completion Time (step): Must not lengthen.

**What not to do**
- Don’t use misleading, overclaiming or pushy phrases.
- Don’t write very long microcopy; it hurts readability.
- Don’t change microcopy, price and imagery together in the same test.
- Don’t fill the microcopy with campaign messages unrelated to the product.
- Don’t position the microcopy area on mobile so that it squeezes the screen.

---

## Kayıtlı kartla hızlı ödeme dönüşümü artırıyor mu?

Değişken: Kayıtlı kartla hızlı ödeme seçeneği · Fark: ekle

Etiket: id=cc-012 · mercek=Çaba · düzey=sürtünme · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does fast payment with a saved card raise conversion?

EN-Variable: Fast payment option with a saved card

Kayıtlı kartla tek tıkla ödeme, veri girişini ortadan kaldırarak süreci hızlandırır ve sürtünmeyi azaltır. Bu kolaylığın dönüşüme ne kadar yansıdığı ölçülmelidir.

**Test edilmesi gerekenler**
- Otomatik gösterim: Kayıtlı kartın otomatik gelmesi tamamlamayı artırıyor mu?
- Benimsenme: Kayıtlı kartı olan kullanıcıların ne kadarı hızlı ödemeyi seçiyor, ne kadarı kartı yine elle giriyor?
- Cihaz: Mobilde hızlı ödemenin etkisi masaüstünden daha mı yüksek?
- Sağlayıcı: Kayıtlı-kart cüzdan çözümlerinde etki değişiyor mu?

**Takip edilecek ana KPI’lar**
- Ödeme Tamamlama Oranı: Hızlı ödeme satın almayı artırıyor mu?
- Ödeme Yöntemi Seçim Oranı: Hangi yöntem seçiliyor?
- Görev Tamamlama Süresi (ödeme adımı): Ödeme adımı kısalıyor mu?
- Hata / Reddedilme Oranı: Artmamalı.
- Sipariş İptal Oranı (30 gün): Yükselmemeli.

**Yapılmaması gerekenler**
- Hızlı ödemeyi zorunlu kılmayın; manuel giriş seçeneği kalmalı.
- Görünürlüğü bozacak büyük uyarı kutuları eklemeyin.
- Aynı testte hızlı ödeme ile kart giriş alanlarının tasarımını birlikte değiştirmeyin.
- Mobilde hızlı ödeme kutusunu ekranı sıkıştıracak kadar büyütmeyin.
- Kayıtlı kartı kullanıcı onayı olmadan varsayılan yapmayın.

### EN

One-click payment with a saved card removes data entry, which speeds up the process and cuts friction. How far this convenience shows up in conversion has to be measured.

**What to test**
- Auto display: Does showing the saved card automatically raise completion?
- Adoption: Of users with a saved card, how many choose fast payment and how many still enter the card by hand?
- Device: Is the effect of fast payment higher on mobile than on desktop?
- Provider: Does the effect change across saved-card wallet solutions?

**KPIs to track**
- Payment Completion Rate: Does fast payment raise purchases?
- Payment Method Selection Rate: Which method gets chosen?
- Task Completion Time (payment step): Does the payment step get shorter?
- Error / Decline Rate: Must not rise.
- Order Cancellation Rate (30 days): Must not go up.

**What not to do**
- Don’t make fast payment mandatory; a manual entry option must remain.
- Don’t add large warning boxes that hurt visibility.
- Don’t change fast payment and the design of the card entry fields together in the same test.
- Don’t enlarge the fast-payment box on mobile so far that it squeezes the screen.
- Don’t make the saved card the default without the user’s consent.

---

## İlerleme çubuğu tamamlama oranını artırıyor mu?

Değişken: Checkout ilerleme çubuğu · Fark: ekle

Etiket: id=cc-013 · mercek=Netlik · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a progress bar raise completion?

EN-Variable: Checkout progress bar

İlerleme çubuğu kullanıcıya konumunu ve kalan adımı gösterir, süreçten vazgeçmeyi azaltabilir. Özellikle ödeme ve adres adımlarında etkisi ölçülmelidir.

**Test edilmesi gerekenler**
- Kavrayış: Çubuk görünür olunca kullanıcı hangi adımda olduğunu anlıyor mu?
- Motivasyon: “Ne kadar kaldığı” devam etme isteğini artırıyor mu?
- Kritik adım: Ödeme ve adres adımında terk oranı düşüyor mu?
- Mobil: Dar ekranda eklenen çubuk form alanlarını aşağı itip mobil terk oranını artırıyor mu?
- Sonraki test: Çubuk kazanırsa tamamlanan adımlara tik işareti koymak ayrı bir testte devam etme isteğini artırıyor mu?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Checkout’a ulaşan kullanıcıların (iki kolda aynı tetikleyici) siparişi bitirme oranı yükseliyor mu?
- Adım Bazlı Terk Oranı: Adımlar daha az mı terk ediliyor?
- Görev Tamamlama Süresi (adım): Adımlar daha hızlı mı tamamlanıyor?
- Geri Dönüş Oranı: Önceki adıma dönüş artmamalı.
- Sayfa Yüklenme Süresi: Çubuk yavaşlatmamalı.

**Yapılmaması gerekenler**
- Gereğinden fazla adım göstermeyin; süreç uzun hissettirir.
- Adım isimlerini teknik veya anlaşılmaz yazmayın.
- Mobilde çubuğa çok fazla ekran alanı ayırmayın.
- Aynı testte çubuğu eklerken funnel adımlarının sayısını birlikte değiştirmeyin.
- Aşırı animasyonlu veya yavaş yüklenen çubuk kullanmayın.

> **Ölçüm notu:** Bu senaryoda ilk adımın tamamlanma oranı neredeyse her zaman yükselir; asıl soru yükselen adımın siparişe dönüp dönmediğidir. Adım metriği testin fotoğrafını çeker, sonucunu değil; birincil metrik huninin sonunda kalır.

### EN

A progress bar shows the user where they are and what is left, and can reduce giving up on the process. Its effect has to be measured especially at the payment and address steps.

**What to test**
- Understanding: With the bar visible, do users understand which step they are on?
- Motivation: Does seeing “how much is left” raise the willingness to continue?
- Critical step: Does abandonment drop at the payment and address steps?
- Mobile: On a narrow screen, does the added bar push the form fields down and raise mobile abandonment?
- Next test: If the bar wins, does adding a check mark to completed steps raise the willingness to continue in a separate test?

**KPIs to track**
- Checkout Completion Rate: Does the rate at which users who reach checkout (same trigger in both arms) finish the order rise?
- Step-Level Abandonment Rate: Are steps abandoned less?
- Task Completion Time (step): Are steps completed faster?
- Back-Navigation Rate: Going back to the previous step must not rise.
- Page Load Time: The bar must not slow the page.

**What not to do**
- Don’t show more steps than needed; the process feels long.
- Don’t name steps in a technical or confusing way.
- Don’t give the bar too much screen space on mobile.
- Don’t change the number of funnel steps in the same test in which you add the bar.
- Don’t use a bar that is heavily animated or slow to load.

> **Measurement note:** In this scenario the completion rate of the first step almost always rises; the real question is whether the step that rises turns into orders. A step metric takes a snapshot of the test, not its result; the primary metric stays at the end of the funnel.

---

## Otomatik indirim kodu davranışı nasıl etkiler?

Değişken: İndirim kodunun otomatik uygulanması · Fark: değiştir

Etiket: id=cc-014 · mercek=Çaba · düzey=sürtünme · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: How does applying a discount code automatically affect behavior?

EN-Variable: Automatic application of the discount code

İndirim kodunun otomatik uygulanması ödeme sürecini kısaltarak dönüşümü artırabilir. Gerçek karşılığı ölçülmelidir.

**Test edilmesi gerekenler**
- Hız: Otomatik kod ödeme adımına geçişi hızlandırıyor mu?
- Farkındalık: Kampanya farkındalığı tamamlama ile ilişkili mi?
- Cihaz: Kodu kopyalayıp yapıştırmanın zahmetli olduğu mobilde otomatik uygulama, masaüstüne göre tamamlamayı daha çok mu artırıyor?
- Güven: Otomatik uygulandı mesajı güven veriyor mu?
- Kod çakışması: Otomatik kod uygulanmışken kullanıcılar manuel alana ikinci bir kod girmeye çalışıp hata alıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Otomatik kod, indirim maliyetine rağmen atanan ziyaretçi başına geliri artırıyor mu? Birincil metrik bu; CR tek başına kazanan seçmez.
- Dönüşüm Oranı (CR): Otomatik kod satın almayı artırıyor mu? RPV ile birlikte okunur.
- Kupon Kullanım Oranı: Otomatik uygulama kullanımı artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Sepet değeri değişiyor mu?
- Brüt Marj: Otomatik indirim marjı eritmemeli.

**Yapılmaması gerekenler**
- Aynı testte kodu otomatik uygularken indirim oranını veya kampanya koşulunu da değiştirmeyin.
- Aynı ekranda birden fazla indirim kodu alanı göstermeyin.
- Kod uygulandı mesajını geciktirmeyin; güveni azaltır.
- Otomatik uygulandı denen indirimi gerçek tutarından farklı göstermeyin veya ödemede sessizce düşürmeyin.
- Manuel kod girme yolunu tamamen kapatmayın.

### EN

Applying a discount code automatically can shorten the payment process and raise conversion. Its real return has to be measured.

**What to test**
- Speed: Does the automatic code speed up the move to the payment step?
- Awareness: Is campaign awareness related to completion?
- Device: On mobile, where copying and pasting a code is a hassle, does automatic application raise completion more than on desktop?
- Trust: Does a “Code applied automatically” message build trust?
- Code clash: With an automatic code applied, do users try to enter a second code in the manual field and hit an error?

**KPIs to track**
- Revenue per Visitor (RPV): Despite the discount cost, does the automatic code raise revenue per assigned visitor? This is the primary metric; CR alone does not pick a winner.
- Conversion Rate (CR): Does the automatic code raise purchases? Read together with RPV.
- Coupon Usage Rate: Does automatic application raise usage?
- Average Order Value (AOV): Does cart value change?
- Gross Margin: The automatic discount must not erode the margin.

**What not to do**
- Don’t change the discount rate or the campaign condition in the same test in which you apply the code automatically.
- Don’t show more than one discount code field on the same screen.
- Don’t delay the “Code applied” message; it reduces trust.
- Don’t show a discount said to be applied automatically at an amount different from its real value, or silently reduce it at payment.
- Don’t close off the manual code entry route entirely.

---

## Ödeme adımındaki güven rozetleri tamamlamayı artırır mı?

Değişken: Ödeme adımındaki güven rozeti şeridi · Fark: ekle

Etiket: id=cc-015 · mercek=Güven · düzey=güven · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Do trust badges at the payment step raise completion?

EN-Variable: Trust badge strip at the payment step

Kart bilgisi girilen ekran, terk oranının en yüksek olduğu andır. Güvenli ödeme, iade garantisi ve 3D Secure gibi görsel sinyaller tereddüdü azaltabilir; fazlası ise şüphe uyandırabilir.

**Test edilmesi gerekenler**
- Sayı: Kaç rozet optimum? (1 / 3 / 5)
- Fark edilme: Kart bilgisini giren kullanıcılar rozet şeridini fark ediyor mu, oturum kayıtları bunu doğruluyor mu?
- Tereddüt anı: Rozet şeridi, kart numarası alanında duraksayıp sayfadan çıkan kullanıcı oranını azaltıyor mu?
- Segment: İlk kez kart bilgisi giren yeni kullanıcıda rozet şeridi, önceden ödeme yapmış dönen kullanıcıya göre terki daha çok mu azaltıyor?

**Takip edilecek ana KPI’lar**
- Ödeme Tamamlama Oranı: Kart ekranına ulaşanların (iki kolda aynı tetikleyici) ödemeyi bitirme oranı artıyor mu?
- Ödeme Adımı Terk Oranı: Düşüyor mu?
- Görev Tamamlama Süresi (adım): Tereddüt kısalıyor mu?
- Hata / Reddedilme Oranı: Değişmemeli.
- Sipariş İptal Oranı (30 gün): Yükselmemeli.

**Yapılmaması gerekenler**
- Gerçekte sahip olmadığınız sertifika rozetlerini göstermeyin.
- Rozetleri CTA’nın önüne geçecek boyutta kullanmayın.
- Çok fazla rozet koyup “fazla ısrarcı” algısı yaratmayın.
- Aynı testte rozetlerin konumu ile sayısını birlikte değiştirmeyin.
- Klavye açılınca rozet şeridi CTA’yı kapatmamalı.

> **Pazar notu:** Hangi sinyalin güven verdiği pazara bağlıdır: bazı pazarlarda banka ve kart doğrulama logoları tanıdık ve rahatlatıcıyken, bazılarında ödeme sağlayıcısı veya bağımsız güvenlik mührü daha güçlü sinyaldir. Rozet setini kendi pazarınızın tanıdığı kurumlardan seçin.

### EN

The screen where card details are entered is the point with the highest abandonment. Visual signals such as secure payment, a returns guarantee and 3D Secure can reduce hesitation; too many can raise suspicion.

**What to test**
- Count: How many badges are optimal? (1 / 3 / 5)
- Noticeability: Do users entering card details notice the badge strip, and do session recordings confirm it?
- Moment of hesitation: Does the badge strip reduce the share of users who pause at the card number field and leave the page?
- Segment: For new users entering card details for the first time, does the badge strip cut abandonment more than for returning users who have paid before?

**KPIs to track**
- Payment Completion Rate: Does the rate at which users who reach the card screen (same trigger in both arms) finish payment rise?
- Payment Step Abandonment Rate: Does it drop?
- Task Completion Time (step): Does hesitation get shorter?
- Error / Decline Rate: Must not change.
- Order Cancellation Rate (30 days): Must not go up.

**What not to do**
- Don’t show certificate badges you don’t actually hold.
- Don’t use badges so large they overshadow the CTA.
- Don’t put in so many badges that you create an “overly insistent” impression.
- Don’t change the position and the number of the badges together in the same test.
- The badge strip must not cover the CTA when the keyboard opens.

> **Market note:** Which signal builds trust depends on the market: in some markets bank and card verification logos are familiar and reassuring, while in others the payment provider or an independent security seal is the stronger signal. Pick the badge set from institutions your own market recognizes.

---

## Zorunlu ve isteğe bağlı alanları açıkça işaretlemek doldurma oranını artırır mı?

Değişken: Alanların zorunluluk etiketi · Fark: ekle

Etiket: id=cc-016 · mercek=Netlik · düzey=form · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does clearly marking required and optional fields raise form completion?

EN-Variable: Required-field labels

Formdaki hangi alanın zorunlu, hangisinin isteğe bağlı olduğu genelde belirsizdir; kullanıcı emin olmadığı alanı da doldurur ya da doldurmayıp hata mesajıyla karşılaşır. İkisini de açıkça işaretlemek bu belirsizliği kaldırabilir.

**Test edilmesi gerekenler**
- Etiket: “(isteğe bağlı)” etiketi eklemek tamamlama süresini/hata oranını düşürüyor mu?
- Kapsam: Sadece isteğe bağlı alanları mı, yoksa zorunlu alanları da yıldızla mı işaretlemeli?
- Cihaz: Mobilde dar ekranda etiket yer kaplaması okunabilirliği bozuyor mu?
- Tutarlılık: Formun tamamında aynı işaretleme kuralı uygulandığında etki büyüyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Form adımına atanan kullanıcıların formu gönderme oranı artıyor mu? Birincil metrik.
- Doğrulama Hatası Oranı: Yükselmemeli; yanlış doldurulan/boş bırakılan zorunlu alan azalmalı.
- Form Doldurma Süresi: Kısalıyor mu?
- Alan Bazlı Terk Oranı: Hangi alanda kayıp azalıyor?
- Destek Talebi: Form doldurmayla ilgili talepler artmamalı.

**Yapılmaması gerekenler**
- Etiketleri form doğrulama kurallarıyla aynı testte değiştirmeyin.
- İsteğe bağlı bir alanı arka planda zorunlu tutup öyle işaretlemeyin.
- Etiketi form tasarımının geri kalanıyla tutarsız bir stilde göstermeyin.
- Mobilde etiketi alan metnini kesecek kadar uzun yazmayın.
- Zorunlu bir alanı “isteğe bağlı” diye etiketleyip gönderimde hata vermeyin.

> **Not:** Büyük ölçekli bağımsız checkout kullanılabilirliği araştırmaları, bu işaretlemenin sitelerin yalnızca küçük bir kısmında (ve mobilde daha da az) uygulandığını, buna rağmen düşük maliyetli ve uzun süredir çözülmemiş bir sorun olduğunu gösteriyor.

### EN

It is usually unclear which form field is required and which is optional; users either fill in a field they are unsure about, or leave it empty and meet an error message. Marking both clearly can remove this ambiguity.

**What to test**
- Label: Does adding an “(optional)” label lower completion time or the error rate?
- Scope: Should only optional fields be marked, or required fields too with an asterisk?
- Device: On a narrow mobile screen, does the space the label takes hurt readability?
- Consistency: Does the effect grow when the same marking rule is applied across the whole form?

**KPIs to track**
- Form Completion Rate: Does the rate at which users assigned to the form step submit the form rise? The primary metric.
- Validation Error Rate: Must not rise; required fields filled in wrongly or left blank should decrease.
- Form Fill Time: Does it get shorter?
- Field-Level Abandonment Rate: At which field does the loss fall?
- Support Contact Rate: Requests about filling in the form must not rise.

**What not to do**
- Don’t change the labels in the same test as the form validation rules.
- Don’t mark a field as optional while quietly requiring it behind the scenes.
- Don’t show the label in a style inconsistent with the rest of the form design.
- Don’t write the label so long on mobile that it cuts off the field text.
- Don’t label a required field “optional” and then throw an error on submit.

> **Note:** Large-scale independent checkout usability studies show that this kind of marking is applied on only a small share of sites (and even fewer on mobile), yet it is a low-cost problem that has gone unsolved for a long time.

---

## Ödeme yöntemini adres bilgisinden önce sormak işe yarar mı?

Değişken: Ödeme yöntemi adımının sırası · Fark: taşı

Etiket: id=cc-017 · mercek=Çaba · düzey=akış · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does asking for the payment method before the address pay off?

EN-Variable: Order of the payment method step

Ödeme adımını öne almak, taahhüdü erken alır ve ödeme yöntemini seçmiş kullanıcının akıştan kopma ihtimalini azaltabilir. Karşı tarafta: kullanıcı toplam tutarı (kargo dahil) görmeden ödeme bilgisi vermeye zorlanır, bu güvensizlik yaratır ve bazı ödeme yöntemleri teslimat adresine bağlı olduğu için teknik olarak da sorun çıkarabilir.

**Test edilmesi gerekenler**
- Sıra: Ödeme adımı öne alındığında tamamlama artıyor mu?
- Toplam tutar: Kullanıcı kargo dahil tutarı ödeme öncesi görebiliyor mu?
- Güven: Erken ödeme bilgisi istemek tereddüt yaratıyor mu?
- Yöntem uyumu: Adrese bağlı ödeme yöntemleri bu sırada çalışıyor mu?
- Cihaz: Mobilde sıra değişikliği farklı mı sonuç veriyor?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Sıra değişikliği tamamlamayı artırıyor mu?
- Adım Bazlı Terk Oranı: Terk başka adıma kaymamalı, azalmalı.
- Ödeme Hata Oranı: Yöntem uyumsuzluğundan doğan hata artmamalı.
- Ziyaretçi Başına Gelir (RPV): Gelir düşmemeli.
- Destek Talebi: “Toplam tutarı göremedim” türü talepler artmamalı.

**Yapılmaması gerekenler**
- Toplam tutarı ödeme bilgisi alındıktan sonra göstermeyin; gizlenen fiyat kabul edilemez.
- Aynı testte adım sırası ile adım sayısını birlikte değiştirmeyin.
- Ödeme güvenlik doğrulamalarını sıralama testinin kapsamına almayın.
- Adrese bağlı yöntemleri test öncesi teknik olarak doğrulamadan varyantı açmayın.
- Adres girilince geçersiz kalan ödeme yöntemi seçimini sessizce sıfırlamayın; kullanıcıya nedenini gösterin.

### EN

Moving the payment step forward takes the commitment early and may reduce the chance that a user who has chosen a payment method drops out of the flow. On the other side: the user is pushed to give payment details before seeing the total (shipping included), which creates distrust, and because some payment methods depend on the delivery address, it can also cause technical problems.

**What to test**
- Order: Does completion rise when the payment step is moved forward?
- Total: Can the user see the amount, shipping included, before paying?
- Trust: Does asking for payment details early create hesitation?
- Method fit: Do address-dependent payment methods work in this order?
- Device: Does the order change give a different result on mobile?

**KPIs to track**
- Checkout Completion Rate: Does the order change raise completion?
- Step-Level Abandonment Rate: Abandonment must decrease, not just shift to another step.
- Payment Error Rate: Errors from method mismatch must not rise.
- Revenue per Visitor (RPV): Revenue must not drop.
- Support Contact Rate: Requests like “I couldn’t see the total” must not rise.

**What not to do**
- Don’t show the total after payment details have been taken; a hidden price is not acceptable.
- Don’t change the step order and the number of steps together in the same test.
- Don’t include payment security verifications in the scope of the ordering test.
- Don’t open the variant without technically verifying the address-dependent methods before the test.
- Don’t silently reset a payment method selection that becomes invalid once the address is entered; show the user why.

---

## Ödeme akışında menü ve bağlantıları kaldırmak tamamlamayı artırır mı?

Değişken: Checkout’taki gezinme bağlantıları · Fark: kaldır

Etiket: id=cc-018 · mercek=Netlik · düzey=akış · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does removing the menu and links from the checkout flow raise completion?

EN-Variable: Navigation links in checkout

Checkout sırasında üst menüyü, kategori bağlantılarını ve alt bilgi bağlantılarını kaldırmak (tünel akışı) dikkat dağıtıcıları temizler ve kullanıcıyı tek yolda tutar. Riski: kullanıcı bilgiye ulaşamaz (iade koşulu, iletişim), kaybolmuş hisseder ve sitede kapana kısıldığı algısı güveni düşürür.

**Test edilmesi gerekenler**
- Sadeleştirme: Bağlantıları kaldırmak tamamlamayı artırıyor mu?
- Kayıp bilgi: Hangi bağlantıların kaldırılması sorulara yol açıyor?
- Güven: Sadeleşen sayfa güven sinyallerini de götürüyor mu?
- Çıkış yolu: Kullanıcı sepete geri dönebiliyor mu?
- Cihaz: Mobilde zaten sade olan akışta değişiklik anlamlı mı?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Tünel akışı tamamlamayı artırıyor mu?
- Adım Bazlı Terk Oranı: Bırakma azalıyor mu?
- Destek Talebi: Bilgiye ulaşamama kaynaklı talepler artmamalı.
- Sepete Geri Dönüş Oranı: Sepeti düzenleme imkânı kaybolmamalı.
- Ziyaretçi Başına Gelir (RPV): Gelir düşmemeli.

**Yapılmaması gerekenler**
- Kullanıcının akıştan çıkmasını tamamen engelleyen bir tasarım kurmayın.
- Yasal olarak bulunması gereken bağlantıları (mesafeli satış, iade, gizlilik) kaldırmayın.
- Aynı testte bağlantı temizliği ile adım sayısını birlikte değiştirmeyin.
- Güven rozetlerini ve iletişim bilgisini dikkat dağıtıcı sayıp birlikte kaldırmayın.
- Sepeti düzenleme yolunu kapatıp tamamlama artışını kazanç saymayın.

### EN

Removing the top menu, category links and footer links during checkout (a tunnel flow) clears distractions and keeps the user on a single path. Risk: the user can’t reach information (return terms, contact), feels lost, and the sense of being trapped on the site lowers trust.

**What to test**
- Simplification: Does removing the links raise completion?
- Missing information: Which removed links lead to questions?
- Trust: Does the simplified page also take away trust signals?
- Way out: Can the user go back to the cart?
- Device: Is the change meaningful on mobile, where the flow is already clean?

**KPIs to track**
- Checkout Completion Rate: Does the tunnel flow raise completion?
- Step-Level Abandonment Rate: Does leaving decrease?
- Support Contact Rate: Requests caused by not being able to reach information must not rise.
- Return-to-Cart Rate: The ability to edit the cart must not be lost.
- Revenue per Visitor (RPV): Revenue must not drop.

**What not to do**
- Don’t build a design that completely prevents the user from leaving the flow.
- Don’t remove the links that must legally be present (distance sales terms, returns, privacy).
- Don’t change the link cleanup and the number of steps together in the same test.
- Don’t treat trust badges and contact details as distractions and remove them as well.
- Don’t close the route to editing the cart and then count the completion gain as a win.

---

## Seçimi onaylayan geri bildirim vermek hatayı azaltır mı?

Değişken: Seçim onayı geri bildirimi · Fark: ekle

Etiket: id=cc-019 · mercek=Netlik · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does feedback that confirms a selection reduce errors?

EN-Variable: Selection confirmation feedback

Kullanıcı bir seçim yaptığında (beden, adet, teslimat günü) bunun alındığını açıkça göstermek belirsizliği kaldırır ve tekrar tıklamayı önler. Karşı tarafta: her seçime eklenen onay öğesi arayüzü kalabalıklaştırır, sayfa zıplamasına yol açabilir ve deneyimli kullanıcıyı yavaşlatır.

**Test edilmesi gerekenler**
- Geri bildirim: Seçim onayı hata oranını düşürüyor mu?
- Sonraki test: Onay eklemek kazanırsa yazılı mesaj ile ikonlu kısa etiket ayrı bir testte karşılaştırıldığında hangisi hatalı seçimi daha çok azaltıyor?
- Deneyimli kullanıcı: Onay öğesi, daha önce sipariş vermiş kullanıcının seçim adımını yavaşlatıyor mu?
- Sayfa hareketi: Beliren onay içeriği kaydırıp yanlış tıklamaya yol açıyor mu?
- Cihaz: Mobilde onay öğesi ekranda görünüyor mu?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Onay geri bildirimi tamamlamayı artırıyor mu?
- Hatalı Seçim Oranı: Yanlış varyantla sipariş azalıyor mu?
- Tekrar Tıklama Oranı: Aynı seçeneğe tekrar tıklama azalıyor mu?
- İade Oranı (30 gün): Yanlış seçim kaynaklı iade artmamalı.
- Erişilebilirlik: Onay yalnızca renkle verilmemeli, ekran okuyucuya duyurusuz kalmamalı.

**Yapılmaması gerekenler**
- Onayı yalnızca renk değişimiyle verip başka bir işaret bırakmayın.
- Beliren onayın sayfayı zıplatmasına izin vermeyin.
- Aynı testte onay biçimi ile seçim öğesinin tasarımını birlikte değiştirmeyin.
- Onay mesajını, seçim gerçekte kaydedilmeden göstermeyin.
- Onayı birkaç saniyede kaybolan bir bildirimle verip seçimin ekranda kalıcı işaretini kaldırmayın.

### EN

When a user makes a selection (size, quantity, delivery day), showing clearly that it was received removes ambiguity and prevents repeated clicking. On the other side: a confirmation element added to every selection clutters the interface, can make the page jump, and slows down the experienced user.

**What to test**
- Feedback: Does selection confirmation lower the error rate?
- Next test: If adding confirmation wins, which cuts wrong selections more when a written message and a short label with an icon are compared in a separate test?
- Experienced user: Does the confirmation element slow the selection step of a user who has ordered before?
- Page movement: Does the confirmation content that appears shift the page and cause a wrong click?
- Device: Is the confirmation element visible on screen on mobile?

**KPIs to track**
- Checkout Completion Rate: Does confirmation feedback raise completion?
- Wrong Selection Rate: Do orders with the wrong variant decrease?
- Repeat Click Rate: Does repeated clicking on the same option decrease?
- Return Rate (30 days): Returns caused by a wrong selection must not rise.
- Accessibility Check: The confirmation must not be given by color alone, and must not go unannounced to a screen reader.

**What not to do**
- Don’t give the confirmation through a color change alone without another cue.
- Don’t let the confirmation that appears make the page jump.
- Don’t change the confirmation form and the design of the selection element together in the same test.
- Don’t show the confirmation message before the selection is actually saved.
- Don’t give the confirmation as a notification that disappears in a few seconds and remove the persistent on-screen mark of the selection.

---

## Varsayılan olarak işaretli gelen seçenekler kabul edilebilir mi?

Değişken: Tarafsız seçeneğin varsayılan seçimi · Fark: değiştir

Etiket: id=cc-020 · mercek=Çaba · düzey=sürtünme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Are options that come pre-selected by default acceptable?

EN-Variable: Default selection of a neutral option

Bir kutunun önceden işaretli gelmesi kullanıcıyı hızlandırabilir, ama bu tekniğin sınırı nettir: pazarlama izni, veri paylaşımı ve ek ücretli hizmetler önceden işaretlenemez; birçok pazarda bu yasaktır ve kullanıcının açık iradesi gerekir. Test edilebilir olan yalnızca tarafsız tercihlerdir (teslimat günü, ücretsiz ya da aynı fiyatlı kargo seçenekleri arasında kargo yöntemi, adet); fiyatı değiştiren bir kargo seçeneği tarafsız değildir.

**Test edilmesi gerekenler**
- Varsayılan: Tarafsız bir seçeneğin önceden seçili gelmesi tamamlamayı artırıyor mu?
- Doğruluk: Varsayılan çoğu kullanıcı için gerçekten doğru mu?
- Farkındalık: Kullanıcı varsayılanı fark edip değiştirebiliyor mu?
- Değiştirme oranı: Varsayılanı değiştirenlerin oranı ne kadar?
- Segment: Farklı kullanıcı tipleri için farklı varsayılan mı doğru?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Varsayılan tamamlamayı artırıyor mu?
- Varsayılan Değiştirme Oranı: İkincil (yalnızca B); yüksek değiştirme oranı yanlış varsayılana işarettir, kollar arasında karşılaştırılmaz.
- İade veya İptal Oranı (30 gün): İstenmeyen seçim kaynaklı iptal artmamalı.
- Destek Talebi: “Bunu ben seçmedim” türü talepler atanan ziyaretçi başına artmamalı.
- Ziyaretçi Başına Gelir (RPV): Gelir düşmemeli.

**Yapılmaması gerekenler**
- Pazarlama izni, veri paylaşımı veya ek ücretli hizmeti önceden işaretli getirmeyin; bu bir test değişkeni değildir.
- Kullanıcının ödeyeceği tutarı artıran bir seçeneği varsayılan yapmayın.
- Varsayılanı fark edilmeyecek kadar silik göstermeyin.
- Aynı testte varsayılan ile seçeneklerin sırasını birlikte değiştirmeyin.
- Hedef pazarın izin kurallarını doğrulamadan varyant kurmayın.

### EN

A pre-ticked box can speed the user up, but the limit of this technique is clear: marketing permission, data sharing and paid extras cannot be pre-ticked; in many markets this is prohibited and the user’s explicit will is required. Only neutral preferences can be tested (delivery day, shipping method among free or same-price options, quantity); a shipping option that changes the price is not neutral.

**What to test**
- Default: Does a neutral option coming pre-selected raise completion?
- Correctness: Is the default really right for most users?
- Awareness: Does the user notice the default and can they change it?
- Override rate: What share of users change the default?
- Segment: Is a different default right for different user types?

**KPIs to track**
- Checkout Completion Rate: Does the default raise completion?
- Default Override Rate: Secondary (B only); a high override rate signals a wrong default, and it is not compared between arms.
- Return or Cancellation Rate (30 days): Cancellations caused by an unwanted selection must not rise.
- Support Contact Rate: Requests like “I didn’t choose this” must not rise per assigned visitor.
- Revenue per Visitor (RPV): Revenue must not drop.

**What not to do**
- Don’t bring marketing permission, data sharing or a paid extra pre-ticked; this is not a test variable.
- Don’t make an option that raises the amount the user pays the default.
- Don’t show the default so faintly that it goes unnoticed.
- Don’t change the default and the order of the options together in the same test.
- Don’t set up a variant without checking the permission rules of the target market.

---

## Ödeme işlenirken adımları gösteren bir yükleme ekranı güveni artırıyor mu?

Değişken: Ödeme yükleme ekranının biçimi · Fark: değiştir

Etiket: id=cc-021 · mercek=Güven · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a loading screen that shows the steps while payment is processed build trust?

EN-Variable: Format of the payment loading screen

Tek bir dönen ikon, arka planda ne olduğu hakkında hiçbir şey söylemez ve bekleme süresini belirsiz hissettirir. “Kart doğrulanıyor”, “banka onayı bekleniyor”, “sipariş oluşturuluyor” gibi gerçek adımları sırayla göstermek, işlemin özenle yapıldığını hissettirip aynı bekleme süresini daha kısa algılatabilir; görünür emek, güven inşa eder. Risk, adımların gerçek işlem sırasını yansıtmaması veya süreyi yapay olarak uzatmak için kullanılmasıdır.

**Test edilmesi gerekenler**
- Biçim: Adım adım ilerleyen bir yükleme ekranı tek bir dönen ikona göre terk oranını düşürüyor mu?
- Süre algısı: Adımlı ekran, gerçek süre değişmeden bekleme süresini daha kısa hissettiriyor mu?
- Doğruluk: Gösterilen adımlar gerçek işlem sırasına mı uyuyor?
- Hata anı: İşlem başarısız olursa adımlı ekran hatayı daha mı anlaşılır kılıyor?
- Cihaz: Mobilde yavaş bağlantıda adımlı ekranın etkisi masaüstünden farklı mı?

**Takip edilecek ana KPI’lar**
- Ödeme Adımı Terk Oranı: Adımlı ekran bekleme sırasında ayrılan kullanıcı oranını düşürüyor mu?
- Algılanan Süre (anket): Kullanıcı bekleme süresini kısa mı buluyor? Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Gerçek İşlem Süresi: Adımlı ekran gerçek işlem süresini uzatmamalı.
- Hata Sonrası Destek Talebi: Başarısız işlemlerde destek talebi artmamalı.
- Ödeme Başarı Oranı: Genel ödeme tamamlama oranı düşmemeli.

**Yapılmaması gerekenler**
- Gerçek işlemi yapay olarak yavaşlatıp adımları uzatmayın; gösterilen süre gerçek işlem süresini aşarsa bu manipülasyondur.
- Gerçekleşmeyen bir adımı (ör. çalışmayan bir “dolandırıcılık taraması”) ekrana koymayın.
- Aynı testte yükleme ekranı biçimi ile ödeme akışının adım sayısını birlikte değiştirmeyin.
- Hata durumunda kullanıcıyı adımlı ekranda takılı bırakmayın; başarısızlık anında net bir hata mesajına geçin.
- Yükleme ekranını güvenlik doğrulamasını (3D Secure, OTP vb.) atlatma veya gizleme amacıyla kullanmayın.

### EN

A single spinning icon says nothing about what is happening in the background and makes the wait feel uncertain. Showing real steps in order, such as “Verifying card”, “Waiting for bank approval” and “Creating order”, can make the process feel carefully handled and make the same wait feel shorter; visible effort builds trust. The risk is that the steps don’t reflect the real processing order or are used to stretch the time artificially.

**What to test**
- Format: Does a step-by-step loading screen lower abandonment compared with a single spinning icon?
- Perceived time: With the real duration unchanged, does the stepped screen make the wait feel shorter?
- Accuracy: Do the steps shown match the real processing order?
- Failure moment: If the process fails, does the stepped screen make the error clearer?
- Device: Does the effect of the stepped screen on a slow mobile connection differ from desktop?

**KPIs to track**
- Payment Step Abandonment Rate: Does the stepped screen lower the share of users who leave during the wait?
- Perceived Wait Time (survey): Do users find the wait short? The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms, and this is a diagnostic signal.
- Actual Processing Time: The stepped screen must not lengthen the real processing time.
- Post-Error Support Contact Rate: Support contacts after failed transactions must not rise.
- Payment Success Rate: The overall payment completion rate must not drop.

**What not to do**
- Don’t artificially slow the real process and stretch the steps; if the time shown exceeds the real processing time, that is manipulation.
- Don’t put a step that doesn’t happen on screen (e.g. a “fraud scan” that isn’t running).
- Don’t change the loading screen format and the number of steps in the payment flow together in the same test.
- Don’t leave the user stuck on the stepped screen when something fails; switch to a clear error message the moment it fails.
- Don’t use the loading screen to bypass or hide a security verification (3D Secure, OTP and the like).

---

## Sepet sayfasına ödeme yöntemi ikonları eklemek güveni artırır mı?

Değişken: Sepet sayfasındaki ödeme yöntemi ikonları · Fark: ekle

Etiket: id=cc-022 · mercek=Güven · düzey=güven · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding payment method icons to the cart page build trust?

EN-Variable: Payment method icons on the cart page

Kullanıcı ödeme adımına gelmeden önce hangi kartların veya yöntemlerin kabul edildiğini bilmek ister; bu bilgi genelde yalnızca ödeme sayfasında ortaya çıkar. İkonları bir adım önce, sepet sayfasında göstermek, desteklenmeyen bir yöntemi kullanan ziyaretçinin ödeme adımında sürprizle karşılaşmasını önleyebilir; ama fazla ikon görsel gürültü yaratabilir.

**Test edilmesi gerekenler**
- Sayı: Tüm yöntemler mi, yalnızca en çok kullanılan 3-4’ü mü daha iyi çalışıyor?
- Terkin yer değiştirmesi: Desteklenmeyen yöntemi kullanan ziyaretçi artık sepette mi ayrılıyor, yani terk yalnızca öne mi kayıyor?
- Sepet tutarı: Yüksek tutarlı sepetlerde kabul edilen kartları erken görmek ödeme adımına geçişi daha çok artırıyor mu?
- Cihaz: Mobilde ikon şeridi ekran alanını gereğinden fazla mı kaplıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sepete atanan ziyaretçilerin siparişi tamamlama oranı artıyor mu?
- Ödeme Adımına Geçiş Oranı: Tanı metriği; sepete ulaşan ziyaretçilerin (ikonları görenler değil) ödeme adımına geçme oranı artıyor mu?
- Ödeme Adımı Terk Oranı: Desteklenmeyen yöntem yüzünden son adımda terk azalıyor mu?
- Destek Talebi: “Bu kartla ödeyebilir miyim?” türü sorular artmamalı.
- Sayfa Yüklenme Süresi: Ek görsel sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Gerçekte kabul etmediğiniz bir ödeme yöntemini ikon olarak göstermeyin.
- Aynı testte ikonların konumunu ve sayısını birlikte değiştirmeyin.
- İkon şeridini sipariş özetinin veya CTA’nın önüne geçirip hiyerarşiyi bozmayın.
- Ödeme sağlayıcı marka kurallarına uymayan boyutta veya biçimde logo kullanmayın.
- Mobilde ikonları okunmaz derecede küçültüp yalnızca dekoratif hâle getirmeyin.

### EN

Before reaching the payment step, users want to know which cards or methods are accepted; this information usually appears only on the payment page. Showing the icons one step earlier, on the cart page, can prevent a visitor who uses an unsupported method from meeting a surprise at the payment step; but too many icons can create visual noise.

**What to test**
- Count: Does showing all methods or only the 3-4 most used work better?
- Displaced abandonment: Does a visitor with an unsupported method now leave at the cart, meaning abandonment just moves earlier?
- Cart value: On high-value carts, does seeing the accepted cards early raise the move to the payment step more?
- Device: On mobile, does the icon strip take up more screen space than it should?

**KPIs to track**
- Conversion Rate (CR): Does the rate at which visitors assigned to the cart complete the order rise?
- Proceed-to-Payment Rate: Diagnostic metric; does the rate at which visitors who reach the cart (not those who see the icons) move to the payment step rise?
- Payment Step Abandonment Rate: Does abandonment at the last step caused by an unsupported method decrease?
- Support Contact Rate: Questions like “Can I pay with this card?” must not rise.
- Page Load Time: The extra imagery must not slow the page.

**What not to do**
- Don’t show an icon for a payment method you don’t actually accept.
- Don’t change the position and the number of the icons together in the same test.
- Don’t let the icon strip overshadow the order summary or the CTA and break the hierarchy.
- Don’t use logos at a size or in a form that breaks the payment provider’s brand rules.
- Don’t shrink the icons on mobile until they are unreadable and merely decorative.
