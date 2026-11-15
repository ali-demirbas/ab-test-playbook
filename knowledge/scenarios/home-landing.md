# Anasayfa ve landing

Yolculuk aşaması: ziyaretçinin siteye ilk düştüğü ekran. Amaç satış değil, bir sonraki adımın alınmasıdır; bu yüzden buradaki birincil metrik çoğu zaman huninin sonu değil, ilk anlamlı aksiyondur. Menü yapısı `search-filtering.md`, pop-up zamanlaması, çıkış niyeti pop-up’ı ve geri sayım sayacı `category-listing.md`, CTA buton rengi `cart-checkout.md` içindedir; burada tekrar edilmezler. Mobil webdeki uygulama indirme banner’ı ile dönen ziyaretçiye özel anasayfa bu dosyadadır, uygulamanın kendi anasayfası `mobile-app.md` içindedir. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Ana CTA ilk ekranda mı görünmeli?

Değişken: Ana CTA’nın konumu · Fark: taşı

Etiket: id=hl-001 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should the main CTA be visible on the first screen?

EN-Variable: Main CTA position

CTA’yı kaydırmadan görünen alana almak aksiyonu erken sunar ve kararı vermiş ziyaretçiyi hemen ilerletir. Karşı argüman: henüz ikna olmamış ziyaretçiye erken sunulan CTA boşa gider, üstelik başlığın ve değer önerisinin yerini daraltır. Uzun ve karmaşık teklifi olan sayfalarda erken CTA tıklansa bile sonraki adımda dökülme yaratabilir.

**Test edilmesi gerekenler**
- Konum: CTA kaydırmadan görünen alanda mı, açıklamadan sonra mı daha çok tıklanıyor?
- Erken tıklama: Erken tıklayanlar sonraki adımı da tamamlıyor mu?
- Yer baskısı: CTA yukarı alınınca başlık ve değer önerisi kısalıyor mu?
- Referans noktası: CTA başlığın hemen altında mı, değer önerisi maddelerinin hemen ardında mı daha çok tamamlatıyor?
- Cihaz: Mobilde görünen alan çok daha dar; kazanan konum masaüstüyle aynı mı?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Sonraki adıma geçen ziyaretçi artıyor mu?
- CTA Tıklama Oranı: Butona tıklama artıyor mu?
- Aksiyon Sonrası Dökülme Oranı: Erken tıklayan kullanıcı sonraki adımda kaybedilmemeli.
- Talep Başına Nitelik Oranı: Açıklamayı okumadan tıklayanların talepleri niteliği düşürmemeli.
- Kaydırma Derinliği: Sayfanın altındaki içeriğin görülmesi kabul edilemez ölçüde düşmemeli.

**Yapılmaması gerekenler**
- Aynı testte CTA konumu ile buton metnini birlikte değiştirmeyin.
- CTA’yı yukarı alırken başlığı da kısaltmayın; hangisinin etkilediği ayrıştırılamaz.
- Mobilde yukarı alınan CTA’yı sabit (yapışkan) bir çubuğa çevirmeyin; o ayrı bir değişkendir.
- Görünen alanı tek bir ekran boyutuna göre tanımlayıp sonucu tüm cihazlara genellemeyin.
- CTA’yı yukarı taşımak için zorunlu bilgiyi (fiyat, kapsam) aşağı itmeyin.

### EN

Moving the CTA into the visible area without scrolling presents the action early and moves a visitor who has already decided forward right away. The counter-argument: a CTA shown early to a visitor who is not yet convinced is wasted, and it also squeezes the space for the headline and the value proposition. On pages with a long or complex offer, an early CTA may be clicked yet cause drop-off at the next step.

**What to test**
- Position: Is the CTA clicked more in the visible area without scrolling or after the explanation?
- Early clicks: Do visitors who click early also complete the next step?
- Space pressure: Do the headline and value proposition get shorter when the CTA moves up?
- Anchor point: Does the CTA convert more right under the headline or right after the value-proposition points?
- Device: The visible area is much narrower on mobile; is the winning position the same as on desktop?

**KPIs to track**
- Primary Action Completion Rate: Do more visitors move on to the next step?
- CTA Click Rate: Does clicking on the button increase?
- Post-Click Drop-off Rate: Users who click early must not be lost at the next step.
- Qualification Rate per Lead: Leads from people who click without reading the explanation must not lower quality.
- Scroll Depth: Views of the content lower on the page must not fall to an unacceptable level.

**What not to do**
- Don’t change the CTA position and the button text in the same test.
- Don’t shorten the headline while moving the CTA up; you can’t tell which one had the effect.
- Don’t turn the CTA moved up on mobile into a fixed (sticky) bar; that is a separate variable.
- Don’t define the visible area for a single screen size and generalize the result to all devices.
- Don’t push required information (price, scope) down to make room for the CTA.

---

## Başlık problemi mi, çözümü mü anlatmalı?

Değişken: Başlığın anlatı çerçevesi · Fark: değiştir

Etiket: id=hl-002 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should the headline describe the problem or the solution?

EN-Variable: Narrative frame of the headline

Problemi adlandıran başlık ziyaretçinin kendini tanımasını sağlar ve “bu benim için” hissi yaratır. Çözümü anlatan başlık ise ne satıldığını hemen netleştirir ve zaman kaybettirmez. Problem odaklı çerçeveleme, ziyaretçi problemini zaten biliyorsa gereksiz bir adım; çözüm odaklı çerçeveleme, ziyaretçi problemin farkında değilse anlamsız gelir.

**Test edilmesi gerekenler**
- Çerçeve: Problemi adlandırmak mı, çözümü söylemek mi daha çok aksiyon getiriyor?
- Farkındalık: Ziyaretçi problemin farkında mı, yoksa önce ikna mı gerekiyor?
- Uzunluk: Problem çerçevesi başlığı uzatıyor mu, uzayan başlık okunuyor mu?
- Sonraki test: Kazanan çerçeve sabitken başlığı soru cümlesi yerine düz bir tespit olarak kurmak ayrı bir testte aksiyonu değiştiriyor mu?
- Segment: Reklamdan gelen ile organik gelen ziyaretçi farklı çerçeveye mi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Çerçeveleme sonraki adımı artırıyor mu?
- Hemen Çıkma Oranı: Yanlış çerçeve ziyaretçiyi kaçırmamalı.
- Kaydırma Derinliği: Başlık okumaya devam ettiriyor mu?
- Sayfada Kalma Süresi: İlgi süresi düşmemeli.
- Talep Başına Nitelik Oranı: Gelen taleplerde satışa ya da hedefe uygun olanların payı düşmemeli.

**Yapılmaması gerekenler**
- Aynı testte başlık ile hero görselini birlikte değiştirmeyin.
- Problemi abartıp korku yaratan bir çerçeve kurmayın.
- Ürünün yapmadığı bir problemi çözüyormuş gibi başlık yazmayın.
- Tek bir trafik kaynağında ölçüp sonucu tüm kaynaklara genellemeyin.
- Başlığı değiştirirken reklam metniyle uyumu bozmayın; mesaj tutarsızlığı ayrı bir kayıp yaratır.

### EN

A headline that names the problem helps visitors recognize themselves and creates a “this is for me” feeling. A headline that describes the solution makes clear right away what is being sold and wastes no time. Problem framing is an unnecessary step if the visitor already knows their problem; solution framing makes no sense if the visitor is not aware of the problem.

**What to test**
- Frame: Does naming the problem or stating the solution bring more action?
- Awareness: Is the visitor aware of the problem, or does persuasion come first?
- Length: Does the problem frame lengthen the headline, and is the longer headline still read?
- Next test: With the winning frame fixed, does phrasing the headline as a plain statement instead of a question change action in a separate test?
- Segment: Do visitors from ads and organic visitors react to different frames?

**KPIs to track**
- Primary Action Completion Rate: Does the framing increase the next step?
- Bounce Rate: The wrong frame must not drive visitors away.
- Scroll Depth: Does the headline keep people reading?
- Time on Page: Time of interest must not drop.
- Qualification Rate per Lead: The share of incoming leads that fit the sale or the goal must not fall.

**What not to do**
- Don’t change the headline and the hero image in the same test.
- Don’t exaggerate the problem into a fear-driven frame.
- Don’t write a headline that claims to solve a problem the product doesn’t solve.
- Don’t measure on a single traffic source and generalize the result to all sources.
- Don’t break consistency with the ad copy when changing the headline; message mismatch causes a separate loss.

---

## Fayda ifadesi soyut mu, somut mu olmalı?

Değişken: Fayda ifadesinin somutluk düzeyi · Fark: değiştir

Etiket: id=hl-003 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should the benefit statement be abstract or concrete?

EN-Variable: Concreteness level of the benefit statement

Soyut fayda (“daha verimli çalışın”) geniş kitleye hitap eder ama kimseye özel gelmez. Somut fayda (“rapor hazırlama süresi yarıya iner”) inandırıcıdır ama dar bir kullanım senaryosunu tarif eder ve diğer ziyaretçileri dışarıda bırakabilir. Somutluk aynı zamanda doğrulanabilir bir iddia yaratır; arkasında veri yoksa risklidir.

**Test edilmesi gerekenler**
- Somutluk: Sayısal veya durumsal somutluk aksiyonu artırıyor mu?
- Kapsam: Somut ifade kendini o senaryoda görmeyeni dışarıda bırakıyor mu?
- İnandırıcılık: Somut iddia kanıtsız sunulduğunda güven düşüyor mu?
- Sonraki test: Somut ifade kazanırsa, rakam veren sürüm ile durum tarif eden sürüm ayrı bir testte karşılaştırıldığında hangisi daha çok aksiyon getiriyor?
- Segment: Benzer bir çözümü daha önce kullanmış ziyaretçi ile ilk kez çözüm arayan ziyaretçi somut ifadeye farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Fayda ifadesi aksiyonu artırıyor mu?
- Aksiyon Sonrası Dökülme Oranı: Somut vaatle gelenlerin sonraki adımda dökülmesi artmamalı.
- Hemen Çıkma Oranı: Dar çerçeve ziyaretçiyi kaçırmamalı.
- Kaydırma Derinliği: İfade okumaya devam ettiriyor mu?
- İade veya İptal Oranı (30 gün): Vaat ile gerçeğin uyumsuzluğu sonradan kayıp yaratmamalı.

**Yapılmaması gerekenler**
- Arkasında ölçüm olmayan bir sayıyı fayda ifadesine yazmayın.
- Aynı testte fayda ifadesi ile CTA metnini birlikte değiştirmeyin.
- Somutluğu tek bir müşteri örneğinden alıp genel vaat gibi sunmayın.
- Vaadi ürünün gerçekte sağlamadığı bir sonuca genişletmeyin.
- Yasal olarak iddia sınırı olan alanlarda (sağlık, finans) hedef pazarın kuralını doğrulamadan somut vaat kurmayın.

### EN

An abstract benefit (“work more efficiently”) appeals to a wide audience but feels personal to no one. A concrete benefit (“cut report preparation time in half”) is believable but describes a narrow use case and may leave other visitors out. Concreteness also creates a verifiable claim; without data behind it, it is risky.

**What to test**
- Concreteness: Does numeric or situational concreteness increase action?
- Scope: Does the concrete statement leave out people who don’t see themselves in that scenario?
- Credibility: Does trust drop when the concrete claim is presented without proof?
- Next test: If the concrete statement wins, which of the version with a number and the version describing a situation brings more action when compared in a separate test?
- Segment: Do visitors who have used a similar solution before and visitors searching for a solution for the first time react differently to the concrete statement?

**KPIs to track**
- Primary Action Completion Rate: Does the benefit statement increase action?
- Post-Click Drop-off Rate: Drop-off at the next step must not rise among those who arrive with the concrete promise.
- Bounce Rate: The narrow frame must not drive visitors away.
- Scroll Depth: Does the statement keep people reading?
- Return or Cancellation Rate (30 days): A mismatch between promise and reality must not cause losses later.

**What not to do**
- Don’t put a number in the benefit statement that has no measurement behind it.
- Don’t change the benefit statement and the CTA text in the same test.
- Don’t take concreteness from a single customer example and present it as a general promise.
- Don’t stretch the promise to an outcome the product doesn’t actually deliver.
- In areas with legal limits on claims (health, finance), don’t write a concrete promise without checking the target market’s rules.

---

## Sayfa sonunda CTA’yı tekrarlamak dönüşümü artırır mı?

Değişken: Sayfa sonundaki ikinci CTA · Fark: ekle

Etiket: id=hl-004 · mercek=Çaba · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does repeating the CTA at the end of the page raise conversion?

EN-Variable: Second CTA at the end of the page

Uzun sayfada aşağı inen ziyaretçi ikna olduğunda yukarı dönmek zorunda kalmamalıdır. Sayfa sonuna ikinci bir CTA koymak bu sürtünmeyi kaldırır. Karşı tarafta: tekrar eden CTA sayfayı satış baskısı gibi hissettirebilir ve iki CTA farklı metin taşırsa mesaj dağılır.

**Test edilmesi gerekenler**
- Tekrar: Sayfa sonuna ikinci CTA eklemek toplam aksiyonu artırıyor mu?
- Sona ulaşanlar: Aksiyon artışı yalnızca sayfa sonuna kadar inen ziyaretçilerde mi ortaya çıkıyor?
- Sonraki test: İkinci CTA kazanırsa, onu sayfa sonundan ikna edici bölümün hemen ardına taşımak ayrı bir testte aksiyonu artırıyor mu?
- Yoğunluk: Üç veya daha fazla tekrar baskı hissi yaratıyor mu?
- Cihaz: Mobilde daha uzun görünen sayfada tekrar daha mı gerekli?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Toplam aksiyon artıyor mu?
- Alt CTA Tıklama Payı: İkinci CTA gerçekten yeni tıklama getiriyor mu, yoksa üsttekini mi bölüyor?
- Kaydırma Derinliği: Sayfa sonuna ulaşan ziyaretçi oranı düşmemeli.
- İade veya İptal Oranı (30 gün): Tekrarlanan çağrıyla alınan aksiyon sonradan iptale dönmemeli.
- Aksiyon Sonrası Tamamlama Oranı: Geç tıklayanların sonraki adımı tamamlaması düşmemeli.

**Yapılmaması gerekenler**
- İki CTA’yı farklı hedefe gönderip hangisinin çalıştığını ölçemez hâle gelmeyin.
- Aynı testte CTA sayısı ile CTA metnini birlikte değiştirmeyin.
- Tekrarı sayfanın her ekranına serpiştirip tek değişken kuralını bozmayın.
- İkinci CTA’yı alt bilgi bağlantılarının arasına sıkıştırıp ayırt edilemez hâle getirmeyin.
- Sayfa sonu CTA’sını kapatılamayan sabit bir çubuğa dönüştürmeyin.

### EN

A visitor who scrolls down a long page and is convinced shouldn’t have to scroll back up. Placing a second CTA at the end of the page removes that friction. On the other side: a repeated CTA can make the page feel like sales pressure, and if the two CTAs carry different text, the message gets scattered.

**What to test**
- Repetition: Does adding a second CTA at the end of the page increase total action?
- Those who reach the end: Does the lift in action appear only among visitors who scroll all the way to the end?
- Next test: If the second CTA wins, does moving it from the end of the page to right after the persuasive section increase action in a separate test?
- Density: Do three or more repetitions create a feeling of pressure?
- Device: On mobile, where the page looks longer, is repetition needed even more?

**KPIs to track**
- Primary Action Completion Rate: Does total action increase?
- Bottom CTA Click Share: Does the second CTA bring genuinely new clicks, or does it just split the one above?
- Scroll Depth: The share of visitors who reach the end of the page must not fall.
- Return or Cancellation Rate (30 days): Action taken through the repeated call must not turn into cancellation later.
- Post-Click Completion Rate: Completion of the next step by late clickers must not fall.

**What not to do**
- Don’t send the two CTAs to different destinations, which would make it impossible to measure which one works.
- Don’t change the number of CTAs and the CTA text in the same test.
- Don’t scatter the repetition across every screen of the page and break the single-variable rule.
- Don’t squeeze the second CTA between footer links so it becomes indistinguishable.
- Don’t turn the end-of-page CTA into a fixed bar that can’t be dismissed.

---

## Otomatik oynayan tanıtım videosu anlatımı güçlendirir mi?

Değişken: Tanıtım videosunun oynatma biçimi · Fark: değiştir

Etiket: id=hl-005 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does an autoplaying intro video strengthen the message?

EN-Variable: Playback mode of the intro video

Video karmaşık bir ürünü metinden hızlı anlatabilir. Otomatik oynatma dikkat çeker ama ses açıksa rahatsız eder, veri tüketir, sayfa yükünü artırır ve bazı ziyaretçilerin hemen çıkmasına yol açar. Tıklayınca oynayan video ise izlenme oranını düşürür fakat izleyeni gerçekten ilgili kılar.

**Test edilmesi gerekenler**
- Oynatma: Video otomatik mi başlamalı, tıklayınca mı?
- Ses açma: Sessiz başlayan otomatik videoda ziyaretçilerin kaçı sesi açıp anlatımı sonuna kadar izliyor?
- İzleme derinliği: İzlemeyi yarıda bırakanlar aksiyonu alıyor mu?
- Cihaz: Mobilde veri tüketimi ve yükleme süresi sonucu değiştiriyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Video aksiyonu artırıyor mu?
- Video İzlenme Oranı: Videoyu başlatan ziyaretçi oranı ne kadar?
- Sayfa Yüklenme Süresi: Sayfa hızı bozulmamalı.
- Hemen Çıkma Oranı: Otomatik oynatma çıkışı artırmamalı.
- Erişilebilirlik: Altyazı eksik olmamalı, hareket azaltma tercihi yok sayılmamalı.

**Yapılmaması gerekenler**
- Sesi açık otomatik oynatma varyantı kurmayın.
- Videoyu sayfanın kritik yükleme yoluna koyup hız kaybını test sonucuna karıştırmayın.
- Aynı testte video ile hero başlığını birlikte değiştirmeyin.
- Veri tasarrufu modundaki veya yavaş bağlantıdaki ziyaretçide otomatik oynatmayı zorla başlatmayın.
- Durdurulamayan veya kapatılamayan bir video önermeyin.

> **Güncellik notu (2026-11):** Tarayıcılar sesli otomatik oynatmayı yıllardır engelliyor; testin gerçek kolları artık sessiz ve altyazılı otomatik oynatma ile kapak görselli, tıklayınca oynayan videodur. Sessiz otomatik oynatma veri tasarrufu kipinde ve bazı mobil tarayıcılarda hiç başlamayabilir; o ziyaretçi B’de de kapak görselini görür ve fark bu kitlede ölçülmez. Önerilen: kolları bu iki biçimle kurmak, hareketi azaltma tercihine uymak ve otomatik oynatmanın gerçekten başladığı oturumları iki kolda aynı olayla loglamak.

### EN

A video can explain a complex product faster than text. Autoplay grabs attention, but it is annoying if the sound is on, uses data, increases page weight and makes some visitors leave right away. A video that plays on click lowers the view rate but makes the viewer genuinely interested.

**What to test**
- Playback: Should the video start automatically or on click?
- Unmuting: With a muted autoplay video, how many visitors turn the sound on and watch the explanation to the end?
- Viewing depth: Do those who stop watching midway still take the action?
- Device: Do data usage and load time on mobile change the result?

**KPIs to track**
- Primary Action Completion Rate: Does the video increase action?
- Video View Rate: What share of visitors start the video?
- Page Load Time: Page speed must not degrade.
- Bounce Rate: Autoplay must not increase exits.
- Accessibility Check: Captions must not be missing, and the reduced-motion preference must not be ignored.

**What not to do**
- Don’t set up a variant that autoplays with sound on.
- Don’t put the video on the page’s critical loading path and let the speed loss contaminate the test result.
- Don’t change the video and the hero headline in the same test.
- Don’t force autoplay on visitors in data-saver mode or on a slow connection.
- Don’t propose a video that can’t be paused or closed.

> **Freshness note (2026-11):** Browsers have blocked autoplay with sound for years; the real arms of the test are now muted, captioned autoplay and a click-to-play video with a poster image. Muted autoplay may not start at all in data-saver mode and in some mobile browsers; those visitors see the poster image in B as well, so the difference is not measured in this audience. Recommended: build the arms with these two formats, respect the reduced-motion preference, and log the sessions where autoplay actually started with the same event in both arms.

---

## Müşteri logoları güven yaratıyor mu?

Değişken: Müşteri logo bandı · Fark: ekle

Etiket: id=hl-006 · mercek=Güven · düzey=sosyal-kanıt · sektör=b2b · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Do customer logos build trust?

EN-Variable: Customer logo bar

Tanınan kurum logoları hızlı bir güven kısayolu sağlar. Ancak logolar ziyaretçinin tanımadığı kurumlardansa etkisizdir, hedef kitleden farklı ölçekteki kurumlarsa (kurumsal logolar küçük işletme ziyaretçisine) “bu benim için değil” hissi bile yaratabilir. Logo bandı ayrıca sayfanın ilk ekranından değerli yer alır.

**Test edilmesi gerekenler**
- Varlık: Logo bandı eklemek aksiyonu artırıyor mu?
- Tanınırlık: Bandı gören ziyaretçiler kısa ankette logolardaki kurumlardan en az birini tanıdığını söylüyor mu?
- Ölçek uyumu: Kurumsal logolar küçük ölçekli ziyaretçiyi uzaklaştırıyor mu?
- Segment: Logo bandının etkisi, logolardaki kurumlarla aynı sektörden gelen ziyaretçide diğer sektörlerden gelenlere göre daha mı güçlü?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Logolar aksiyonu artırıyor mu?
- Kaydırma Derinliği: Logo bandı ziyaretçiyi durdurmamalı.
- Hemen Çıkma Oranı: Ölçek uyumsuzluğu çıkışı artırmamalı.
- Talep Başına Nitelik Oranı: Hedef profile uyan taleplerin payı düşmemeli.
- Sayfa Yüklenme Süresi: Logo görselleri hızı bozmamalı.

**Yapılmaması gerekenler**
- Gerçekte müşteriniz olmayan kurumların logosunu koymayın; bu yalnızca etik değil hukuki risktir.
- Logo kullanımı için izniniz olup olmadığını varsaymayın.
- Aynı testte logo bandı ile referans yorumlarını birlikte eklemeyin.
- Logoları okunmayacak kadar küçültüp “koyduk” saymayın.
- Tek bir sektörde ölçüp sonucu diğer sektör sayfalarına genellemeyin.

### EN

Logos of recognized organizations provide a quick trust shortcut. But logos are ineffective if the visitor doesn’t know the organizations, and if they come from organizations of a different scale than the target audience (enterprise logos shown to a small-business visitor), they can even create a “this isn’t for me” feeling. A logo bar also takes valuable space on the first screen of the page.

**What to test**
- Presence: Does adding a logo bar increase action?
- Recognition: In a short survey, do visitors who saw the bar say they recognize at least one of the organizations in the logos?
- Scale fit: Do enterprise logos push away small-scale visitors?
- Segment: Is the effect of the logo bar stronger for visitors from the same sector as the logo organizations than for those from other sectors?

**KPIs to track**
- Primary Action Completion Rate: Do the logos increase action?
- Scroll Depth: The logo bar must not stop visitors.
- Bounce Rate: Scale mismatch must not increase exits.
- Qualification Rate per Lead: The share of leads that match the target profile must not fall.
- Page Load Time: Logo images must not degrade speed.

**What not to do**
- Don’t put up logos of organizations that aren’t actually your customers; this is not only an ethical but a legal risk.
- Don’t assume you have permission to use a logo.
- Don’t add the logo bar and customer testimonials in the same test.
- Don’t shrink the logos until they are unreadable and call it done.
- Don’t measure in a single sector and generalize the result to the pages of other sectors.

---

## Uzman veya kurucu görünürlüğü güveni artırır mı?

Değişken: Gerçek kişiyi tanıtan blok · Fark: ekle

Etiket: id=hl-007 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does showing an expert or the founder build trust?

EN-Variable: Block introducing a real person

Arkasında gerçek bir insan olduğunu göstermek (kurucu fotoğrafı ve imzası, alan uzmanının açıklaması) soyut bir markayı somutlaştırır. Karşı tarafta: kişi öne çıkarıldığında marka küçük ölçekli görünebilir, kurumsal alıcıda “tek kişilik iş” algısı yaratabilir ve kişiye bağımlılık riski doğar.

**Test edilmesi gerekenler**
- Varlık: Gerçek bir kişiyi göstermek aksiyonu artırıyor mu?
- Sonraki test: Kişi bloğu kazanırsa, blokta kurucunun mu alan uzmanının mı yer aldığı ayrı bir testte güveni değiştiriyor mu?
- Kişiye yönelme: Bloğu gören ziyaretçiler ürünü denemek yerine doğrudan o kişiyle görüşme talebine mi yöneliyor?
- Ölçek algısı: Kişi vurgusu markayı küçük gösterip kurumsal alıcıyı caydırıyor mu?
- Segment: Bireysel ve kurumsal ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Kişi görünürlüğü aksiyonu artırıyor mu?
- Kurumsal Talep Oranı (atanan ziyaretçi başına): Kurumsal nitelikli talepler düşmemeli.
- Kaydırma Derinliği: Bölüm okunuyor mu?
- Sayfada Kalma Süresi: İlgi süresi düşmemeli.
- İletişim Talebi Oranı (atanan ziyaretçi başına): Soru sorma davranışı artıyor mu?

**Yapılmaması gerekenler**
- Aynı testte kişi bloğunu eklerken müşteri referanslarını veya logo bandını da değiştirmeyin.
- Stok fotoğrafı gerçek kurucu veya uzman gibi sunmayın; kişiye sahip olmadığı unvan veya yetkinlik atfetmeyin.
- Kişinin onaylamadığı bir sözü ondan alıntıymış gibi yazmayın.
- Uzman görüşünü ürün iddiasının yerine geçirip doğrulanamaz bir vaat üretmeyin.
- Düzenlemeye tabi alanlarda (sağlık, finans, hukuk) uzman ifadesini hedef pazarın kuralını doğrulamadan yayınlamayın.

### EN

Showing that a real person stands behind the brand (a founder’s photo and signature, a domain expert’s explanation) makes an abstract brand tangible. On the other side: putting a person forward can make the brand look small, can create a “one-person shop” impression for enterprise buyers, and creates a dependence on that person.

**What to test**
- Presence: Does showing a real person increase action?
- Next test: If the person block wins, does whether the block features the founder or a domain expert change trust in a separate test?
- Pull toward the person: Do visitors who see the block go straight to asking to talk to that person instead of trying the product?
- Scale perception: Does the emphasis on a person make the brand look small and put off enterprise buyers?
- Segment: Do individual and enterprise visitors react differently?

**KPIs to track**
- Primary Action Completion Rate: Does visibility of the person increase action?
- Enterprise Lead Rate (per assigned visitor): Enterprise-grade leads must not fall.
- Scroll Depth: Is the section read?
- Time on Page: Time of interest must not drop.
- Contact Request Rate (per assigned visitor): Does asking questions increase?

**What not to do**
- Don’t also change customer testimonials or the logo bar in the same test while adding the person block.
- Don’t present a stock photo as the real founder or expert; don’t attribute a title or expertise the person doesn’t have.
- Don’t write a statement the person hasn’t approved as if it were a quote from them.
- Don’t use an expert’s opinion in place of a product claim and create an unverifiable promise.
- In regulated areas (health, finance, law), don’t publish expert statements without checking the target market’s rules.

---

## Uzun sayfa mı, kısa sayfa mı daha çok dönüştürüyor?

Değişken: Sayfadaki bölüm sayısı · Fark: değiştir

Etiket: id=hl-008 · mercek=Netlik · düzey=bilgi · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Long page or short page: which converts more?

EN-Variable: Number of sections on the page

Uzun sayfa itirazları tek tek karşılar ve karmaşık ürünü anlatmaya yer bırakır. Kısa sayfa kararı hızlandırır ve dikkat dağınıklığını azaltır. Belirleyici olan uzunluk değil, ziyaretçinin karar vermek için ihtiyaç duyduğu bilgi miktarıdır; bu da ürünün karmaşıklığına ve fiyat seviyesine bağlıdır.

**Test edilmesi gerekenler**
- Uzunluk: Bölüm sayısını azaltmak aksiyonu artırıyor mu?
- İhtiyaç: Çıkarılan bölümler gerçekten okunuyor muydu?
- İtiraz: Kısalan sayfada cevapsız kalan itiraz destek talebine dönüşüyor mu?
- Segment: Yeni ziyaretçi uzun, geri dönen ziyaretçi kısa sayfaya mı daha iyi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Uzunluk aksiyonu değiştiriyor mu?
- Kaydırma Derinliği: Ziyaretçi sayfanın neresine kadar iniyor?
- Destek Talebi: Cevapsız kalan soru yükü artmamalı.
- Talep Başına Nitelik Oranı: Az bilgiyle gelen taleplerde uygun olanların payı düşmemeli.
- Sayfada Kalma Süresi: Karar süresi belirgin şekilde uzamamalı.

**Yapılmaması gerekenler**
- Bölüm çıkarırken kalan bölümlerin sırasını da değiştirmeyin.
- Fiyat, kapsam veya iptal koşulu gibi karar için gerekli bilgiyi kısaltma adına çıkarmayın.
- Kaydırma derinliği düşük diye bölümün gereksiz olduğunu varsaymayın; konumu yanlış olabilir.
- Tek bir ürün sayfasında ölçüp sonucu farklı fiyat seviyesindeki sayfalara genellemeyin.
- Aynı testte hem uzunluğu hem görsel yoğunluğu değiştirmeyin.

### EN

A long page answers objections one by one and leaves room to explain a complex product. A short page speeds up the decision and reduces distraction. What matters is not length but the amount of information the visitor needs to decide, which depends on the product’s complexity and price level.

**What to test**
- Length: Does reducing the number of sections increase action?
- Need: Were the removed sections actually being read?
- Objection: Does an objection left unanswered on the shorter page turn into a support request?
- Segment: Do new visitors respond better to the long page and returning visitors to the short one?

**KPIs to track**
- Primary Action Completion Rate: Does length change action?
- Scroll Depth: How far down the page do visitors go?
- Support Contact Rate: The load of unanswered questions must not rise.
- Qualification Rate per Lead: The share of suitable leads among those arriving with less information must not fall.
- Time on Page: Time to decide must not grow noticeably.

**What not to do**
- Don’t change the order of the remaining sections while removing sections.
- Don’t remove information needed to decide, such as price, scope or cancellation terms, in the name of shortening.
- Don’t assume a section is unnecessary because its scroll depth is low; its position may be wrong.
- Don’t measure on a single product page and generalize the result to pages at a different price level.
- Don’t change both length and visual density in the same test.

---

## “Nasıl çalışır” bölümü tereddüdü gideriyor mu?

Değişken: “Nasıl çalışır” bölümü · Fark: ekle

Etiket: id=hl-009 · mercek=Netlik · düzey=bilgi · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a “How it works” section remove hesitation?

EN-Variable: “How it works” section

Sürecin adım adım anlatılması belirsizliği azaltır ve “kaydolunca ne olacak” sorusunu cevaplar. Karşı tarafta: süreci göstermek işin ne kadar emek gerektirdiğini de ortaya koyar ve basit sanılan bir hizmetin karmaşık görünmesine yol açabilir. Adım sayısı burada mesajın kendisidir.

**Test edilmesi gerekenler**
- Varlık: Süreç anlatımı eklemek aksiyonu artırıyor mu?
- Sonraki test: Süreç bölümü kazanırsa, üç adımlık özet ile ayrıntılı anlatım ayrı bir testte karşılaştırıldığında hangisi daha ikna edici?
- Beklenti uyumu: Bölümü gören kullanıcılar kayıttan sonraki ilk adımda takılıp yardım sayfasına daha az mı gidiyor?
- Karmaşıklık algısı: Süreç görünür olunca iş zor mu görünüyor?
- Segment: Ürünü tanımayan ile daha önce benzerini kullanmış ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Süreç anlatımı aksiyonu artırıyor mu?
- Aksiyon Sonrası Tamamlama Oranı: Beklentisi netleşen kullanıcı sonraki adımı bırakmamalı.
- Destek Talebi: “Sonra ne oluyor” soruları azalıyor mu?
- Kaydırma Derinliği: Bölüm görülüyor mu?
- İlk Adım Terk Oranı: Süreci görüp vazgeçme artmamalı.

**Yapılmaması gerekenler**
- Gerçekte daha uzun süren bir süreci kısa gösteren adım anlatımı kurmayın.
- Aynı testte süreç anlatımı ile referansları birlikte eklemeyin.
- Süre vaadi verirken ölçülmemiş bir rakam yazmayın.
- Adımları görselleştirirken sayfa yükünü artırıp hız kaybını sonuca karıştırmayın.
- Zorunlu bir adımı (doğrulama, onay) anlatımdan gizleyip süreci olduğundan basit göstermeyin.

### EN

Explaining the process step by step reduces uncertainty and answers the question “what happens once I sign up?” On the other side: showing the process also reveals how much effort the job takes and can make a service that is thought to be simple look complicated. The number of steps is itself the message here.

**What to test**
- Presence: Does adding a process explanation increase action?
- Next test: If the process section wins, which is more persuasive when a three-step summary and a detailed explanation are compared in a separate test?
- Expectation fit: Do users who see the section get stuck less at the first step after sign-up and visit the help page less?
- Perceived complexity: Does the job look hard once the process is visible?
- Segment: Do people who don’t know the product and visitors who have used something similar before react differently?

**KPIs to track**
- Primary Action Completion Rate: Does the process explanation increase action?
- Post-Click Completion Rate: Users whose expectations are now clear must not drop the next step.
- Support Contact Rate: Do “what happens next” questions decrease?
- Scroll Depth: Is the section seen?
- First-Step Abandonment Rate: Giving up after seeing the process must not increase.

**What not to do**
- Don’t write a step explanation that makes a process that actually takes longer look short.
- Don’t add the process explanation and testimonials in the same test.
- Don’t write an unmeasured figure when promising a duration.
- Don’t add page weight while visualizing the steps and let the speed loss contaminate the result.
- Don’t hide a mandatory step (verification, approval) from the explanation and make the process look simpler than it is.

---

## Ziyaretçinin geldiği kaynağa göre başlığı değiştirmek işe yarar mı?

Değişken: Başlığın trafik kaynağına göre uyarlanması · Fark: değiştir

Etiket: id=hl-010 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does changing the headline to match the visitor’s traffic source pay off?

EN-Variable: Adapting the headline to the traffic source

Reklamdaki veya yönlendiren sayfadaki ifadeyi başlıkta karşılamak beklenti sürekliliği kurar ve “yanlış yere geldim” hissini önler. Riski: kaynak sayısı arttıkça yönetilemez sayıda varyasyon doğar, yanlış eşleştirme alakasız bir başlık gösterir ve kişiselleştirme rahatsız edici bir takip hissi yaratabilir.

**Test edilmesi gerekenler**
- Süreklilik: Kaynağın ifadesini başlıkta karşılamak aksiyonu artırıyor mu?
- Kapsam: Kaç kaynak için ayrı başlık sürdürülebilir?
- Yedek: Tanınmayan kaynaktan gelene hangi başlık gösteriliyor?
- Rahatsızlık: Kişiselleştirme takip edildiği hissi yaratıyor mu?
- Segment: Ücretli ve organik trafik aynı başlığa mı, farklı başlığa mı daha iyi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Kaynağa göre başlık aksiyonu artırıyor mu?
- Hemen Çıkma Oranı: Yanlış eşleşme çıkışı artırmamalı.
- Kaynak Bazlı Dönüşüm Farkı: Hangi kaynakta kazanç var, hangisinde yok?
- Talep Başına Nitelik Oranı: Kaynağa uyumlu mesaj niteliksiz talebin payını artırmamalı.
- Sayfa Yüklenme Süresi: Kişiselleştirme gecikme yaratmamalı.

**Yapılmaması gerekenler**
- Kaynak bilgisini kişisel veriden türetip ziyaretçiye ima etmeyin.
- Yedek başlık tanımlamadan kişiselleştirme kurmayın; tanınmayan kaynakta boş başlık kalmasın.
- Aynı testte hem başlığı hem CTA metnini kaynağa göre değiştirmeyin.
- Kişiselleştirmeyi sunucu tarafında değil istemci tarafında yapıyorsanız başlık değişiminin gözle görülür titremesini yok saymayın.
- Tek bir kaynakta kazandı diye tüm kaynaklara açmayın; kaynak bazında ayrı değerlendirin.

> **Güncellik notu (2026-11):** Tarayıcıların takip kısıtları bazı reklam tıklama kimliklerini adresten siliyor ve yönlendiren sayfanın çoğu zaman yalnız alan adını iletiyor; ölçüm izni vermeyen ziyaretçide kaynak bilgisi hiç toplanamayabilir. Önerilen: başlığı yalnız adresteki kampanya parametresinden eşleştirmek, tanınmayan kaynağa varsayılan başlığı göstermek, varsayılan başlığı gören ziyaretçi payını iki kolda izlemek ve kaynak kırılımını yalnız kaynağı bilinen ziyaretçide okumak.

### EN

Echoing the wording of the ad or the referring page in the headline builds continuity of expectation and prevents the “I’m in the wrong place” feeling. The risk: as the number of sources grows, the variations become unmanageable, a wrong match shows an irrelevant headline, and personalization can create an uncomfortable feeling of being tracked.

**What to test**
- Continuity: Does echoing the source’s wording in the headline increase action?
- Scope: For how many sources can a separate headline be sustained?
- Fallback: Which headline is shown to a visitor from an unrecognized source?
- Discomfort: Does personalization create a feeling of being tracked?
- Segment: Do paid and organic traffic respond better to the same headline or to different ones?

**KPIs to track**
- Primary Action Completion Rate: Does the source-based headline increase action?
- Bounce Rate: A wrong match must not increase exits.
- Per-Source Conversion Gap: In which source is there a gain and in which none?
- Qualification Rate per Lead: A message matched to the source must not raise the share of unqualified leads.
- Page Load Time: Personalization must not add delay.

**What not to do**
- Don’t derive the source information from personal data and hint at it to the visitor.
- Don’t set up personalization without defining a fallback headline; no headline should be left blank for an unrecognized source.
- Don’t change both the headline and the CTA text by source in the same test.
- If you personalize on the client side rather than the server side, don’t ignore the visible flicker of the headline change.
- Don’t roll out to all sources because it won in one; evaluate each source separately.

> **Freshness note (2026-11):** Browser tracking restrictions strip some ad click IDs from the address, and the referring page often passes only the domain name; for a visitor who doesn’t grant measurement consent, source information may not be collected at all. Recommended: match the headline only from the campaign parameter in the address, show the default headline to an unrecognized source, track the share of visitors who see the default headline in both arms, and read the source breakdown only among visitors whose source is known.

---

## Sayfanın bittiği izlenimi veren tasarım kaydırmayı durduruyor mu?

Değişken: İlk ekranda alt bölümün görünürlüğü · Fark: değiştir

Etiket: id=hl-011 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does a design that looks like the end of the page stop scrolling?

EN-Variable: Visibility of the lower section on the first screen

Tam ekran kaplayan bir bölüm veya güçlü bir yatay ayırıcı, ziyaretçide sayfanın sona erdiği izlenimi yaratabilir ve altındaki içerik hiç görülmez. Bu genelde fark edilmeyen bir kayıptır: içerik oradadır, ölçümde “okunmadı” görünür ve içeriğin kendisi suçlanır. Ayırıcıyı yumuşatmak veya alttan bir parça göstermek kaydırmayı sürdürebilir.

**Test edilmesi gerekenler**
- Sonraki test: Alt bölümden parça gösterimi sabitken bölüm ayırıcısını yumuşatmak, ayrı bir testte kaydırma derinliğine ek katkı sağlıyor mu?
- İpucu: Alttaki içerikten bir parça göstermek devam ettiriyor mu?
- Yükseklik: Tam ekran yüksekliğinden vazgeçmek fark yaratıyor mu?
- Sonuç: Artan kaydırma aksiyona dönüşüyor mu, yoksa sadece derinlik mi artıyor?
- Cihaz: Ekran yüksekliği farklı cihazlarda kesinti noktası değişiyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Kaydırma artışı aksiyona dönüşüyor mu?
- Kaydırma Derinliği: Alttaki bölümlerin görülme oranı artıyor mu?
- Alt Bölüm Etkileşim Oranı: Aşağıdaki içerikle etkileşim artıyor mu?
- Sayfada Kalma Süresi: Süre uzarken aksiyon düşmemeli.
- Sayfa Yüklenme Süresi: İlk ekrana giren alt bölümün görselleri yüklenmeyi yavaşlatmamalı.

**Yapılmaması gerekenler**
- Aynı testte hem bölüm yüksekliğini hem içerik sırasını değiştirmeyin.
- Alttan parça göstermek için ilk ekrandaki başlığı veya CTA’yı görünen alanın dışına itmeyin.
- Kaydırmayı zorlamak için sayfayı otomatik kaydıran bir davranış eklemeyin.
- Tek bir ekran yüksekliğinde ölçüp sonucu tüm cihazlara genellemeyin.
- Ayırıcıyı kaldırırken bölümler arası okunabilirliği bozmayın.

### EN

A full-screen section or a strong horizontal divider can give the visitor the impression that the page has ended, and the content below is never seen. This is usually an unnoticed loss: the content is there, the measurement shows “not read”, and the content itself gets blamed. Softening the divider or showing a piece of what lies below can keep people scrolling.

**What to test**
- Next test: With the peek of the lower section fixed, does softening the section divider add further scroll depth in a separate test?
- Hint: Does showing a piece of the content below keep people going?
- Height: Does giving up the full-screen height make a difference?
- Outcome: Does the extra scrolling turn into action, or does only depth increase?
- Device: Does the break point change on devices with different screen heights?

**KPIs to track**
- Primary Action Completion Rate: Does the scroll increase turn into action?
- Scroll Depth: Does the share of views of the lower sections increase?
- Lower-Section Engagement Rate: Does engagement with the content below increase?
- Time on Page: Action must not fall while time grows.
- Page Load Time: Images of the lower section that enters the first screen must not slow loading.

**What not to do**
- Don’t change the section height and the content order in the same test.
- Don’t push the headline or the CTA on the first screen out of the visible area to show a piece from below.
- Don’t add auto-scrolling behavior to force scrolling.
- Don’t measure at a single screen height and generalize the result to all devices.
- Don’t harm readability between sections while removing the divider.

---

## Örnek kullanım senaryoları göstermek karar verdiriyor mu?

Değişken: Kullanım örnekleri bölümü · Fark: ekle

Etiket: id=hl-012 · mercek=Uygunluk · düzey=bilgi · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does showing example use cases help visitors decide?

EN-Variable: Use-case examples section

Ziyaretçi çoğu zaman ürünün ne olduğunu değil, kendi durumunda ne işe yarayacağını anlamakta zorlanır. Somut kullanım örnekleri bu boşluğu doldurur. Karşı tarafta: örnekler dar seçilirse kendini orada görmeyen ziyaretçi elenir ve sayfa uzar.

**Test edilmesi gerekenler**
- Varlık: Kullanım örnekleri eklemek aksiyonu artırıyor mu?
- Sayı: Kaç örnek gösterildiğinde kendini bulma oranı en yüksek?
- Sonraki test: Örnek bölümü kazanırsa, örnekleri ziyaretçinin durumuna göre seçmek ayrı bir testte sabit örneklerden daha çok aksiyon getiriyor mu?
- Aşağı itilen içerik: Örnek bölümü eklenince altında kalan fiyat ve kapsam bölümlerinin görülme oranı düşüyor mu?
- Segment: Farklı kullanıcı tipleri farklı örneklere mi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Örnekler aksiyonu artırıyor mu?
- Örnek Etkileşim Oranı: Örneklerle etkileşim ne kadar?
- Kaydırma Derinliği: Bölüm görülüyor mu?
- Aksiyon Sonrası Dökülme Oranı: Kendini yanlış örnekte bulan kullanıcının erken dökülmesi artmamalı.
- Sayfada Kalma Süresi: Uzayan sayfa ilgiyi düşürmemeli.

**Yapılmaması gerekenler**
- Gerçek olmayan kullanım örneğini gerçek müşteri hikâyesi gibi sunmayın.
- Aynı testte örnek sayısını ve örnek biçimini birlikte değiştirmeyin.
- Örnekleri tek bir sektörden seçip sonucu diğer sektör ziyaretçilerine genellemeyin.
- Örnek anlatımına ölçülmemiş sonuç rakamı eklemeyin.
- Örnekleri sayfanın karar için gerekli bilgisinin (fiyat, kapsam) önüne koymayın.

### EN

Visitors often struggle not to understand what the product is but to see what it will do in their own situation. Concrete use-case examples fill that gap. On the other side: if the examples are chosen too narrowly, visitors who don’t see themselves there drop out, and the page gets longer.

**What to test**
- Presence: Does adding use-case examples increase action?
- Count: At how many examples is the rate of visitors finding themselves highest?
- Next test: If the examples section wins, does choosing examples by the visitor’s situation bring more action than fixed examples in a separate test?
- Content pushed down: When the examples section is added, does the share of views of the price and scope sections below it fall?
- Segment: Do different user types react to different examples?

**KPIs to track**
- Primary Action Completion Rate: Do the examples increase action?
- Example Engagement Rate: How much do visitors engage with the examples?
- Scroll Depth: Is the section seen?
- Post-Click Drop-off Rate: Early drop-off by users who find themselves in the wrong example must not rise.
- Time on Page: The longer page must not lower interest.

**What not to do**
- Don’t present a fictional use case as a real customer story.
- Don’t change the number of examples and the example format in the same test.
- Don’t pick the examples from a single sector and generalize the result to visitors from other sectors.
- Don’t add an unmeasured result figure to an example description.
- Don’t put the examples ahead of the information needed to decide (price, scope).

---

## Uzun sayfada bölüm navigasyonu işe yarıyor mu?

Değişken: Sayfa içi bölüm navigasyonu · Fark: ekle

Etiket: id=hl-013 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does section navigation on a long page pay off?

EN-Variable: In-page section navigation

Sayfa içi bağlantılar (sabit bir bölüm menüsü veya içindekiler) ziyaretçinin aradığı bölüme atlamasını sağlar. Riski: navigasyon ziyaretçiyi tek bir bölüme götürüp geri kalan ikna içeriğini atlatabilir; ayrıca ekranda yer kaplar ve mobilde dar alanda sıkışır.

**Test edilmesi gerekenler**
- Varlık: Bölüm navigasyonu eklemek aksiyonu artırıyor mu?
- Atlama: Kullanıcılar hangi bölüme atlıyor, aradaki içeriği kaybediyor mu?
- Sonraki test: Navigasyon kazanırsa, sabit menü ile sayfa başındaki içindekiler listesi ayrı bir testte karşılaştırıldığında hangisi daha çok kullanılıyor?
- Etiketleme: Bölüm adları ziyaretçinin aradığı kelimelerle eşleşiyor mu?
- Cihaz: Mobilde navigasyon yer kaplayıp içeriği bastırıyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Navigasyon aksiyonu artırıyor mu?
- Navigasyon Kullanım Oranı: Bağlantılar gerçekten kullanılıyor mu?
- Kaydırma Derinliği: Atlanan bölümlerin görülmesi kabul edilemez ölçüde düşmemeli.
- Aranan Bölüme Ulaşma Süresi: Bilgiye ulaşma hızlanıyor mu?
- Aksiyon Sonrası Dökülme Oranı: İkna içeriğini atlayıp tıklayanların sonraki adımda dökülmesi artmamalı.

**Yapılmaması gerekenler**
- Aynı testte navigasyonu eklerken bölüm başlıklarını veya bölüm sırasını birlikte değiştirmeyin.
- Sabit navigasyonu ekranın önemli bir kısmını kaplayacak boyutta kurmayın.
- Navigasyona fiyat veya kayıt sayfası gibi sayfa dışına çıkan bağlantılar eklemeyin; yalnızca sayfa içi bölümlere gitmeli.
- Bağlantı hedeflerini kaydırma sırasında başlığın altında kalacak şekilde bırakmayın.
- Klavye ile gezilemeyen bir navigasyon önermeyin.

### EN

In-page links (a fixed section menu or a table of contents) let the visitor jump to the section they are looking for. The risk: navigation can take the visitor to a single section and skip the rest of the persuasive content; it also takes up screen space and gets cramped in the narrow area on mobile.

**What to test**
- Presence: Does adding section navigation increase action?
- Jumping: Which sections do users jump to, and do they miss the content in between?
- Next test: If the navigation wins, which is used more when a fixed menu and a table of contents at the top of the page are compared in a separate test?
- Labeling: Do the section names match the words visitors are looking for?
- Device: On mobile, does the navigation take up space and crowd out the content?

**KPIs to track**
- Primary Action Completion Rate: Does the navigation increase action?
- Navigation Usage Rate: Are the links actually used?
- Scroll Depth: Views of the skipped sections must not fall to an unacceptable level.
- Time to Reach the Sought Section: Does getting to the information get faster?
- Post-Click Drop-off Rate: Drop-off at the next step must not rise among those who skip the persuasive content and click.

**What not to do**
- Don’t change the section headings or the section order in the same test while adding the navigation.
- Don’t build a fixed navigation so large that it covers a significant part of the screen.
- Don’t add links that leave the page, such as pricing or sign-up pages, to the navigation; it should only go to in-page sections.
- Don’t leave the link targets so that they end up under the header when scrolled to.
- Don’t propose a navigation that can’t be used with a keyboard.

---

## Teklifin yanına açık bir reddetme seçeneği eklemek dönüşümü etkiler mi?

Değişken: Açık “şimdi değil” reddetme seçeneği · Fark: ekle

Etiket: id=hl-014 · mercek=Güven · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding a clear option to decline next to an offer affect conversion?

EN-Variable: Clear “not now” decline option

Bir teklifin yanına açık bir “şimdi değil” seçeneği koymak kullanıcıya kontrol hissi verir ve zorlanma tepkisini azaltır. Sezgiye aykırı olan şudur: reddetmeyi kolaylaştırmak kabul oranını düşürebileceği gibi, güven artışı yoluyla toplam ilişkiyi güçlendirebilir. Ölçülmesi gereken tek seferlik kabul değil, sonraki davranıştır.

**Test edilmesi gerekenler**
- Varlık: Açık bir reddetme seçeneği eklemek kabul oranını nasıl değiştiriyor?
- Sonraki davranış: Reddedenler daha sonra geri dönüp kabul ediyor mu?
- Sonraki test: Reddetme seçeneği kazanırsa, “Şimdi değil” ile “İstemiyorum” ifadeleri ayrı bir testte kabul oranını farklı mı etkiliyor?
- Çıkış yolu: Açık reddetme seçeneği varken teklifi kapatma işaretiyle veya geri tuşuyla geçenlerin payı azalıyor mu?
- Segment: Yeni ziyaretçi ile mevcut kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Toplam Kabul Oranı (30 gün): Atanan kullanıcılarda 30 gün içindeki kümülatif kabul artıyor mu?
- Anlık Kabul Oranı: Tek gösterimdeki kabul oranı ne oluyor?
- Tekrar Ziyaret Oranı: Reddeden kullanıcının siteye dönüşü düşmemeli.
- Şikâyet veya Kapatma Oranı: Rahatsızlık sinyalleri artmamalı.
- İzin İptal Oranı (30 gün): Sonradan izin geri çekme artmamalı.

**Yapılmaması gerekenler**
- Reddetme seçeneğini okunmaz derecede soluk veya küçük yapan bir varyant kurmayın.
- Reddedeni aynı oturumda tekrar tekrar aynı teklifle karşılamayın.
- Reddetme seçeneğine basanı suçlayıcı veya utandırıcı bir metinle (“Hayır, tasarruf istemiyorum”) karşılamayın.
- Yasal izin gerektiren alanlarda (iletişim izni, çerez) reddetme seçeneğini zorlaştırmayı test konusu yapmayın.
- Aynı testte hem reddetme seçeneğini hem teklifin içeriğini değiştirmeyin.

### EN

Putting a clear “not now” option next to an offer gives the user a sense of control and reduces the reaction to being pushed. The counterintuitive part is this: making it easier to decline can lower the acceptance rate, but through increased trust it can strengthen the overall relationship. What needs to be measured is not one-time acceptance but later behavior.

**What to test**
- Presence: How does adding a clear decline option change the acceptance rate?
- Later behavior: Do those who decline come back and accept later?
- Next test: If the decline option wins, do the wordings “Not now” and “No thanks” affect the acceptance rate differently in a separate test?
- Way out: With a clear decline option, does the share of people who get past the offer with the close icon or the back button fall?
- Segment: Do new visitors and existing users react differently?

**KPIs to track**
- Cumulative Acceptance Rate (30 days): Does cumulative acceptance within 30 days among assigned users increase?
- Immediate Acceptance Rate: What is the acceptance rate on a single exposure?
- Return Visit Rate: The return of users who decline must not fall.
- Complaint or Dismissal Rate: Signals of annoyance must not increase.
- Permission Revocation Rate (30 days): Later withdrawal of permission must not increase.

**What not to do**
- Don’t set up a variant that makes the decline option unreadably faint or small.
- Don’t greet someone who declined with the same offer again and again in the same session.
- Don’t answer a click on the decline option with an accusing or shaming text (“No, I don’t want to save”).
- In areas that require legal consent (communication consent, cookies), don’t make making declining harder a test subject.
- Don’t change both the decline option and the content of the offer in the same test.

---

## Sayfanın üstündeki fayda çubuğu aksiyonu artırıyor mu?

Değişken: Sayfa üstündeki fayda çubuğu · Fark: ekle

Etiket: id=hl-015 · mercek=Netlik · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does a benefits bar at the top of the page raise action?

EN-Variable: Benefits bar at the top of the page

Başlığın hemen üstünde veya altında duran ince bir şerit (ücretsiz kargo, iade süresi, teslimat vaadi) en sık sorulan üç soruyu kaydırmadan cevaplar. Karşı tarafta: şerit reklam bandına benzeyip görmezden gelinebilir, dikkat çekerse asıl başlığın önüne geçer ve ekranın en değerli bölümünden yer alır.

**Test edilmesi gerekenler**
- Varlık: Fayda çubuğu eklemek aksiyonu artırıyor mu?
- Fark edilme: Çubuk varken ziyaretçiler kargo ve iade bilgisini yine de sayfanın altında veya yardım sayfasında arıyor mu?
- Görsel ağırlık: Çubuk dikkat çekince başlığın etkisi zayıflıyor mu?
- Cihaz: Kısa mobil ilk ekranda fayda çubuğunun başlığı ve CTA’yı aşağı itmesi, masaüstünde görülmeyen bir aksiyon kaybı yaratıyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Çubuk aksiyonu artırıyor mu?
- Kaydırma Derinliği: Çubuk okumayı durdurmamalı.
- Hemen Çıkma Oranı: Reklam algısı çıkışı artırmamalı.
- Destek Talebi: Çubuktaki konularda gelen sorular azalıyor mu?
- Başlık Etkileşimi: Ana başlığın görülmesi düşmemeli.

**Yapılmaması gerekenler**
- Çubuğa gerçekte sunulmayan bir vaat yazmayın.
- Aynı testte çubuk içeriği ile başlığı birlikte değiştirmeyin.
- Çubuğu kapatılamayan sabit bir katmana çevirmeyin.
- Koşullu bir vaadi (belirli tutar üstü ücretsiz kargo) koşulsuz gibi yazmayın.
- Üçten fazla bilgi sıkıştırıp okunmaz hâle getirmeyin.

### EN

A thin strip just above or below the headline (free shipping, return period, delivery promise) answers the three most frequently asked questions without scrolling. On the other side: the strip can look like an ad banner and be ignored, and if it draws attention it overshadows the real headline and takes space from the most valuable part of the screen.

**What to test**
- Presence: Does adding a benefits bar increase action?
- Noticing: With the bar in place, do visitors still look for shipping and return information at the bottom of the page or on the help page?
- Visual weight: When the bar draws attention, does the headline’s impact weaken?
- Device: On the short mobile first screen, does the benefits bar pushing the headline and CTA down cause an action loss that isn’t seen on desktop?

**KPIs to track**
- Primary Action Completion Rate: Does the bar increase action?
- Scroll Depth: The bar must not stop reading.
- Bounce Rate: The ad-like perception must not increase exits.
- Support Contact Rate: Do questions on the topics in the bar decrease?
- Headline Engagement: Views of the main headline must not fall.

**What not to do**
- Don’t put a promise in the bar that isn’t actually offered.
- Don’t change the bar content and the headline in the same test.
- Don’t turn the bar into a fixed layer that can’t be dismissed.
- Don’t write a conditional promise (free shipping above a certain amount) as if it were unconditional.
- Don’t cram in more than three pieces of information and make it unreadable.

---

## Başlıkta özellik mi, fayda mı önce gelmeli?

Değişken: Başlıkta fayda ile özelliğin sırası · Fark: değiştir

Etiket: id=hl-016 · mercek=Netlik · düzey=metin · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Should the headline lead with the feature or the benefit?

EN-Variable: Order of benefit and feature in the headline

Faydayı öne almak ziyaretçinin kendi sonucunu görmesini sağlar. Özelliği öne almak ise ne olduğunu hemen netleştirir ve ne aradığını bilen ziyaretçiyi hızlandırır. Fayda önde olduğunda ürünün ne olduğu belirsiz kalabilir; özellik önde olduğunda ise “bu bana ne kazandırır” sorusu cevapsız kalır. “Başlık problemi mi, çözümü mü anlatmalı?” senaryosundan farkı: orada başlığın anlatı çerçevesi (problem ya da çözüm) değişir, burada çerçeve sabit kalır ve yalnızca aynı başlıktaki fayda ile özelliğin sırası değişir.

**Test edilmesi gerekenler**
- Sıra: Fayda mı, özellik mi başta durduğunda aksiyon artıyor?
- Netlik: Fayda öne alınınca ürünün ne olduğu anlaşılıyor mu?
- Sonraki test: Kazanan sıra sabitken faydayı ve özelliği tek cümlede birleştiren başlık ayrı bir testte aksiyonu artırıyor mu?
- Uzunluk: Fayda ifadesi başlığı okunmayacak kadar uzatıyor mu?
- Segment: Ürünü tanıyan ile ilk kez görenler farklı sıraya mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Sıralama aksiyonu artırıyor mu?
- Hemen Çıkma Oranı: Belirsizlik çıkışı artırmamalı.
- Kaydırma Derinliği: Okumaya devam etme artıyor mu?
- Talep Başına Nitelik Oranı: Uygun taleplerin payı düşmemeli.
- Sayfada Kalma Süresi: İlgi süresi düşmemeli.

**Yapılmaması gerekenler**
- Ürünün sağlamadığı bir faydayı başa yazmayın.
- Aynı testte başlık sırası ile alt başlığı birlikte değiştirmeyin.
- Fayda ifadesine ölçülmemiş bir sonuç rakamı koymayın.
- Reklam metniyle uyumu bozacak bir sıralama seçmeyin.
- Tek bir ürün sayfasında ölçüp tüm sayfalara kural diye uygulamayın.

### EN

Putting the benefit first lets the visitor see their own outcome. Putting the feature first makes clear right away what the product is and speeds up a visitor who knows what they are looking for. When the benefit comes first, what the product is can stay unclear; when the feature comes first, the question “what do I get out of it?” goes unanswered. How it differs from the “Should the headline describe the problem or the solution?” scenario: there the narrative frame of the headline (problem or solution) changes; here the frame stays fixed and only the order of benefit and feature within the same headline changes.

**What to test**
- Order: Does action increase when the benefit comes first or the feature?
- Clarity: When the benefit is moved up front, is it still clear what the product is?
- Next test: With the winning order fixed, does a headline combining the benefit and the feature in one sentence increase action in a separate test?
- Length: Does the benefit statement stretch the headline until it isn’t read?
- Segment: Do people who know the product and first-time viewers react to different orders?

**KPIs to track**
- Primary Action Completion Rate: Does the ordering increase action?
- Bounce Rate: Uncertainty must not increase exits.
- Scroll Depth: Does continued reading increase?
- Qualification Rate per Lead: The share of suitable leads must not fall.
- Time on Page: Time of interest must not drop.

**What not to do**
- Don’t put a benefit the product doesn’t deliver up front.
- Don’t change the headline order and the subheading in the same test.
- Don’t put an unmeasured result figure in the benefit statement.
- Don’t choose an order that breaks consistency with the ad copy.
- Don’t measure on a single product page and apply it to all pages as a rule.

---

## Güvenceleri madde listesi hâlinde vermek ikna ediyor mu?

Değişken: Güvencelerin sunum biçimi · Fark: değiştir

Etiket: id=hl-017 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does presenting assurances as a bullet list persuade?

EN-Variable: Presentation format of the assurances

Kısa madde listesi (iptal koşulu, veri güvenliği, destek, teslimat) paragraf içinde kaybolan güvenceleri taranabilir hâle getirir. Riski: liste uzarsa hiçbiri okunmaz, ayrıca güvence listesi ziyaretçinin aklına gelmemiş endişeleri hatırlatıp tereddüt yaratabilir.

**Test edilmesi gerekenler**
- Biçim: Madde listesi mi, paragraf mı daha çok ikna ediyor?
- Sonraki test: Liste biçimi kazanırsa, listedeki güvence sayısı ayrı bir testte etkiyi değiştiriyor mu? (3 / 5 / 7)
- Hatırlanma: Liste hâlindeki güvenceleri gören ziyaretçiler kısa ankette iptal koşulunu paragraf sürümüne göre daha doğru hatırlıyor mu?
- Ters etki: Liste akla gelmemiş endişeyi hatırlatıp tereddüt yaratıyor mu?
- Segment: İlk kez gelen ile geri dönen kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Liste aksiyonu artırıyor mu?
- Destek Talebi: Listedeki konularda soru sayısı azalıyor mu?
- Kaydırma Derinliği: Bölüm görülüyor mu?
- Sayfada Kalma Süresi: Okuma yükü ilgiyi kırmamalı.
- İade veya İptal Oranı (30 gün): Yanlış anlaşılan güvence sonradan sorun yaratmamalı.

**Yapılmaması gerekenler**
- Koşullu bir güvenceyi koşulsuz gibi maddeleştirmeyin.
- Aynı testte madde sayısı ile madde içeriğini birlikte değiştirmeyin.
- Güvence listesini yasal metnin yerine geçirmeyin.
- Maddeleri ikonla süsleyip aynı testte görsel yoğunluğu da değiştirmeyin.
- Listeyi karar için gerekli bilginin (fiyat, kapsam) önüne koymayın.

### EN

A short bullet list (cancellation terms, data security, support, delivery) makes assurances that get lost inside a paragraph scannable. The risk: if the list grows long, none of it is read, and an assurance list can also remind the visitor of worries they hadn’t thought of and create hesitation.

**What to test**
- Format: Does a bullet list or a paragraph persuade more?
- Next test: If the list format wins, does the number of assurances in the list change the effect in a separate test? (3 / 5 / 7)
- Recall: In a short survey, do visitors who see the assurances as a list recall the cancellation terms more accurately than with the paragraph version?
- Backfire: Does the list remind visitors of a worry they hadn’t thought of and create hesitation?
- Segment: Do first-time and returning users react differently?

**KPIs to track**
- Primary Action Completion Rate: Does the list increase action?
- Support Contact Rate: Do questions on the topics in the list decrease?
- Scroll Depth: Is the section seen?
- Time on Page: The reading load must not break interest.
- Return or Cancellation Rate (30 days): A misunderstood assurance must not cause problems later.

**What not to do**
- Don’t turn a conditional assurance into an unconditional bullet.
- Don’t change the number of bullets and the content of the bullets in the same test.
- Don’t use the assurance list in place of the legal text.
- Don’t decorate the bullets with icons and change the visual density in the same test.
- Don’t put the list ahead of the information needed to decide (price, scope).

---

## Güvenceleri tek blokta mı, akışa yayarak mı sunmalı?

Değişken: Güvencelerin sayfadaki yerleşimi · Fark: taşı

Etiket: id=hl-018 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should assurances sit in one block or be spread through the flow?

EN-Variable: Placement of the assurances on the page

Tüm güvenceleri tek bölümde toplamak derli toplu bir cevap verir ama o bölüme ulaşmayan ziyaretçi hiçbirini görmez. Endişenin doğduğu yere yerleştirmek (fiyatın yanına iade koşulu, forma veri güvencesi) her güvenceyi tam ihtiyaç anında sunar; buna karşılık sayfa dağınıklaşabilir ve mesaj tekrarı yorucu gelebilir.

**Test edilmesi gerekenler**
- Dağıtım: Güvenceler tek blokta mı, ilgili noktalara yayılmış mı daha etkili?
- Eşleşme: Her güvence gerçekten endişenin doğduğu yerde mi duruyor?
- Sonraki test: Dağıtılmış yerleşim kazanırsa, aynı güvenceyi birden fazla noktada tekrarlamak ayrı bir testte ek güven mi yaratıyor, yorgunluk mu?
- Görünürlük: Tek bloktaki güvenceleri kaç ziyaretçi görüyor?
- Segment: Tereddütlü ve kararlı ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Dağıtım biçimi aksiyonu artırıyor mu?
- Adım Bazlı Terk Oranı: Endişe noktalarındaki bırakma azalıyor mu?
- Güvence Görülme Oranı: Güvencelerin görülme oranı düşmemeli.
- Destek Talebi: Aynı konudaki sorular azalıyor mu?
- Sayfada Kalma Süresi: Dağınıklık karar süresini uzatmamalı.

**Yapılmaması gerekenler**
- Güvenceleri dağıtırken metinlerini de yeniden yazmayın.
- Aynı güvenceyi farklı yerlerde farklı ifadeyle vermeyin; tutarsızlık güveni bozar.
- Tek bloktan çıkardığınız güvenceyi hiçbir yere koymadan bırakmayın.
- Yasal olarak belirli bir yerde bulunması gereken bilgiyi taşımayın.
- Aynı testte hem yerleşimi hem güvence sayısını değiştirmeyin.

### EN

Collecting all assurances in one section gives a tidy answer, but a visitor who never reaches that section sees none of them. Placing each where the worry arises (the return terms next to the price, the data assurance at the form) delivers every assurance at the moment of need; on the other hand, the page can become scattered and repeating the message can feel tiresome.

**What to test**
- Distribution: Are the assurances more effective in a single block or spread across the relevant points?
- Matching: Does each assurance actually sit where the worry arises?
- Next test: If the distributed placement wins, does repeating the same assurance at more than one point create extra trust or fatigue in a separate test?
- Visibility: How many visitors see the assurances in the single block?
- Segment: Do hesitant and decided visitors react differently?

**KPIs to track**
- Primary Action Completion Rate: Does the distribution format increase action?
- Step-Level Abandonment Rate: Does dropping out at the worry points decrease?
- Assurance View Rate: The view rate of the assurances must not fall.
- Support Contact Rate: Do questions on the same topic decrease?
- Time on Page: Clutter must not lengthen the decision time.

**What not to do**
- Don’t rewrite the assurance texts while distributing them.
- Don’t give the same assurance in different wording in different places; inconsistency breaks trust.
- Don’t take an assurance out of the single block and leave it nowhere.
- Don’t move information that legally has to appear in a specific place.
- Don’t change both the placement and the number of assurances in the same test.

---

## Video referans yazılı referanstan daha mı ikna edici?

Değişken: Müşteri referansının biçimi · Fark: değiştir

Etiket: id=hl-019 · mercek=Güven · düzey=sosyal-kanıt · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Is a video testimonial more persuasive than a written one?

EN-Variable: Format of the customer testimonial

Videoda gerçek bir kişinin konuşması metinden daha inandırıcı gelir ve taklit edilmesi zordur. Bedeli: izlenme oranı okumaya göre düşüktür, üretimi pahalıdır, sayfa yükünü artırır ve videoyu açmayan ziyaretçi hiçbir referans görmemiş olur.

**Test edilmesi gerekenler**
- Biçim: Video referans mı, metin referans mı daha çok aksiyon getiriyor?
- İzlenme: Videoyu kaç ziyaretçi başlatıyor, kaçı bitiriyor?
- Sonraki test: Video biçimi kazanırsa, videonun yanına kısa bir özet metin eklemek ayrı bir testte farkı değiştiriyor mu?
- Algılanan gerçeklik: Aynı anlatım videoda sunulduğunda ziyaretçiler kısa ankette referansı daha gerçek buluyor mu?
- Cihaz: Mobilde video izlenme oranı belirgin düşüyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Referans biçimi aksiyonu artırıyor mu?
- Referans Etkileşim Oranı: Referansla etkileşim artıyor mu?
- Sayfa Yüklenme Süresi: Sayfa hızı bozulmamalı.
- Kaydırma Derinliği: Bölüm görülüyor mu?
- Erişilebilirlik: Altyazı ve metin karşılığı eksik bırakılmamalı.

**Yapılmaması gerekenler**
- Oyuncuya oynatılan bir anlatımı gerçek müşteri referansı gibi sunmayın.
- İzin alınmamış bir müşteri görüntüsünü yayınlamayın.
- Aynı testte referans biçimi ile referans içeriğini birlikte değiştirmeyin.
- Videoyu tek referans kaynağı yapıp açmayan ziyaretçiyi referanssız bırakmayın.
- Video referansı otomatik ve sesli başlatmayın; oynatma biçimi ayrı bir değişkendir.

### EN

A real person speaking on video is more convincing than text and hard to imitate. The cost: the view rate is lower than the read rate, production is expensive, it increases page weight, and a visitor who doesn’t open the video has seen no testimonial at all.

**What to test**
- Format: Does a video testimonial or a text testimonial bring more action?
- Viewing: How many visitors start the video and how many finish it?
- Next test: If the video format wins, does adding a short summary text next to the video change the difference in a separate test?
- Perceived authenticity: When the same account is presented on video, do visitors in a short survey find the testimonial more real?
- Device: Does the video view rate drop noticeably on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does the testimonial format increase action?
- Testimonial Engagement Rate: Does engagement with the testimonial increase?
- Page Load Time: Page speed must not degrade.
- Scroll Depth: Is the section seen?
- Accessibility Check: Captions and a text alternative must not be left out.

**What not to do**
- Don’t present an account performed by an actor as a real customer testimonial.
- Don’t publish footage of a customer who hasn’t given permission.
- Don’t change the testimonial format and the testimonial content in the same test.
- Don’t make the video the only testimonial source and leave visitors who don’t open it with no testimonial.
- Don’t start the video testimonial automatically and with sound; the playback mode is a separate variable.

---

## Referansı sonuç anlatan müşteriden seçmek fark yaratır mı?

Değişken: Referansın içerik türü · Fark: değiştir

Etiket: id=hl-020 · mercek=Güven · düzey=sosyal-kanıt · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does choosing testimonials from customers who describe a result make a difference?

EN-Variable: Content type of the testimonial

“Çok memnun kaldım” diyen genel bir referans duygu bildirir; “şu sorunu şu kadar sürede çözdük” diyen referans ise somut bir sonuç gösterir. Sonuç odaklı referans daha ikna edicidir ama dar bir kullanım senaryosunu tarif eder ve kendini orada görmeyen ziyaretçiyi kapsamayabilir.

**Test edilmesi gerekenler**
- İçerik: Sonuç anlatan referans genel övgüden daha mı etkili?
- Kapsam: Somut referans başka durumdaki ziyaretçiyi dışarıda bırakıyor mu?
- Sonraki test: Sonuç anlatan referans kazanırsa, referans sahibinin rolünü ve sektörünü belirtmek ayrı bir testte etkiyi artırıyor mu?
- Abartı algısı: Referanstaki somut sonuç ziyaretçiye abartılı gelip genel övgüye göre güveni düşürüyor mu?
- Segment: Farklı kullanıcı tipleri farklı referansa mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Referans türü aksiyonu artırıyor mu?
- Aksiyon Sonrası Dökülme Oranı: Dar referansla gelenlerin sonraki adımda dökülmesi artmamalı.
- Referans Etkileşim Oranı: Referanslar okunuyor mu?
- Kaydırma Derinliği: Bölüm görülüyor mu?
- İade veya İptal Oranı (30 gün): Vaat uyumsuzluğu sonradan kayıp yaratmamalı.

**Yapılmaması gerekenler**
- Müşterinin söylemediği bir sonucu referansa yazmayın.
- İzinsiz isim, unvan veya kurum bilgisi yayınlamayın.
- Referanstaki rakamı ölçülmemişse kesin gibi sunmayın.
- Aynı testte referans içeriği ile referans sayısını birlikte değiştirmeyin.
- Tek sektörden referans gösterip sonucu diğer sektörlere genellemeyin.

### EN

A general testimonial saying “I was very happy” conveys a feeling; a testimonial saying “we solved this problem in this much time” shows a concrete result. A result-focused testimonial is more persuasive but describes a narrow use case and may not cover a visitor who doesn’t see themselves there.

**What to test**
- Content: Is a testimonial describing a result more effective than general praise?
- Scope: Does a concrete testimonial leave out visitors in a different situation?
- Next test: If the result-describing testimonial wins, does stating the testimonial author’s role and sector increase the effect in a separate test?
- Perceived exaggeration: Does the concrete result in the testimonial seem exaggerated to the visitor and lower trust compared with general praise?
- Segment: Do different user types react to different testimonials?

**KPIs to track**
- Primary Action Completion Rate: Does the testimonial type increase action?
- Post-Click Drop-off Rate: Drop-off at the next step must not rise among those who arrive through a narrow testimonial.
- Testimonial Engagement Rate: Are the testimonials read?
- Scroll Depth: Is the section seen?
- Return or Cancellation Rate (30 days): A mismatch with the promise must not cause losses later.

**What not to do**
- Don’t write a result into a testimonial that the customer didn’t state.
- Don’t publish a name, title or organization without permission.
- Don’t present a figure in a testimonial as certain if it hasn’t been measured.
- Don’t change the testimonial content and the number of testimonials in the same test.
- Don’t show testimonials from a single sector and generalize the result to other sectors.

---

## Ziyaretçinin geldiği kaynağa uygun referans göstermek işe yarar mı?

Değişken: Referansın trafik kaynağına göre seçimi · Fark: değiştir

Etiket: id=hl-021 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing a testimonial that matches the visitor’s traffic source pay off?

EN-Variable: Selecting the testimonial by traffic source

Ziyaretçiyle aynı sektörden veya aynı kanaldan gelen bir müşterinin referansı “benim gibi biri” etkisi yaratır. Riski: kaynak eşleştirmesi yanlışsa alakasız bir referans gösterilir, ayrıca her kaynak için ayrı referans yönetmek sürdürülemez hâle gelebilir. “Ziyaretçinin geldiği kaynağa göre başlığı değiştirmek işe yarar mı?” senaryosundan farkı: orada kaynağa göre uyarlanan öğe başlıktır, burada başlık sabit kalır ve yalnızca gösterilen referans kaynağa göre seçilir; ikisini aynı testte birlikte uyarlamayın.

**Test edilmesi gerekenler**
- Eşleştirme: Kaynağa uygun referans aksiyonu artırıyor mu?
- Kapsam: Kaç kaynak için ayrı referans sürdürülebilir?
- Yedek: Tanınmayan kaynaktan gelene hangi referans gösteriliyor?
- Sonraki test: Eşleştirme kazanırsa, sektör benzerliğine göre eşleştirme ile ölçek benzerliğine göre eşleştirme ayrı bir testte karşılaştırıldığında hangisi daha etkili?
- Cihaz: Mobilde eşleştirilen referans ilk ekranda görünüyor mu, yoksa kaydırmanın altında mı kalıyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Eşleştirme aksiyonu artırıyor mu?
- Kaynak Bazlı Dönüşüm Farkı: Hangi kaynakta kazanç var, hangisinde yok?
- Hemen Çıkma Oranı: Alakasız referans çıkışı artırmamalı.
- Referans Etkileşim Oranı: Referansla etkileşim artıyor mu?
- Sayfa Yüklenme Süresi: Kişiselleştirme gecikme yaratmamalı.

**Yapılmaması gerekenler**
- Eşleştirilen referansı “size özel seçildi” diye sunmayın; kişiselleştirme iması takip hissi yaratır.
- Yedek referans tanımlamadan eşleştirme kurmayın.
- Aynı testte hem referansı hem başlığı kaynağa göre değiştirmeyin.
- Tek kaynakta kazandı diye tüm kaynaklara açmayın.
- Referans sahibinin izin verdiği kullanım kapsamını aşmayın.

### EN

A testimonial from a customer in the same sector or from the same channel as the visitor creates a “someone like me” effect. The risk: if the source matching is wrong, an irrelevant testimonial is shown, and managing a separate testimonial for every source can become unsustainable. How it differs from the “Does changing the headline to match the visitor’s traffic source pay off?” scenario: there the element adapted to the source is the headline; here the headline stays fixed and only the testimonial shown is chosen by source; don’t adapt both in the same test.

**What to test**
- Matching: Does a source-matched testimonial increase action?
- Scope: For how many sources can a separate testimonial be sustained?
- Fallback: Which testimonial is shown to a visitor from an unrecognized source?
- Next test: If the matching wins, which is more effective when matching by sector similarity and matching by scale similarity are compared in a separate test?
- Device: On mobile, does the matched testimonial appear on the first screen, or does it sit below the fold?

**KPIs to track**
- Primary Action Completion Rate: Does the matching increase action?
- Per-Source Conversion Gap: In which source is there a gain and in which none?
- Bounce Rate: An irrelevant testimonial must not increase exits.
- Testimonial Engagement Rate: Does engagement with the testimonial increase?
- Page Load Time: Personalization must not add delay.

**What not to do**
- Don’t present the matched testimonial as “chosen especially for you”; implying personalization creates a feeling of being tracked.
- Don’t set up matching without defining a fallback testimonial.
- Don’t change both the testimonial and the headline by source in the same test.
- Don’t roll out to all sources because it won in one source.
- Don’t go beyond the scope of use the testimonial author permitted.

---

## Bölümleri zigzag dizmek okumayı sürdürüyor mu?

Değişken: Bölümlerde görsel-metin hizalaması · Fark: değiştir

Etiket: id=hl-022 · mercek=Çaba · düzey=görsel · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Does a zigzag section layout keep people reading?

EN-Variable: Image-text alignment in sections

Görsel ve metnin dönüşümlü olarak sağa sola geçmesi (zigzag) monotonluğu kırar ve her bölümü ayrı bir birim gibi gösterir. Karşı tarafta: göz her bölümde yön değiştirmek zorunda kalır, tarama yavaşlar ve tek sütunlu düzenin sunduğu hızlı okuma kaybolur.

**Test edilmesi gerekenler**
- Düzen: Zigzag mı, tutarlı hizalama mı daha çok okutuyor?
- Bölüm sayısı: Kaç bölümden sonra zigzag yorucu hâle geliyor?
- Görsel ağırlık: Görseller metnin önüne mi geçiyor?
- Tarama: Ziyaretçi bölümleri atlayarak mı geçiyor?
- Cihaz: Mobilde tek sütuna düşen düzende zigzagın karşılığı kalıyor mu?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Düzen aksiyonu artırıyor mu?
- Kaydırma Derinliği: Sayfanın altına ulaşma artıyor mu?
- Bölüm Görülme Oranı: Bölümlerin görülmesi düşmemeli.
- Sayfada Kalma Süresi: Okuma süresi kabul edilemez ölçüde uzamamalı.
- Sayfa Yüklenme Süresi: Ek görseller hızı bozmamalı.

**Yapılmaması gerekenler**
- Aynı testte düzen ile bölüm sayısını birlikte değiştirmeyin.
- Zigzag için bölümlere anlamsız görsel eklemeyin.
- Mobilde zaten tek sütuna düşen düzeni zigzag varyantı sayıp karşılaştırmayın.
- Okuma sırasını (görsel önce mi metin önce mi) bölümden bölüme rastgele değiştirmeyin.
- Klavye ve ekran okuyucu sırasını görsel düzene feda etmeyin.

### EN

Alternating the image and the text from side to side (zigzag) breaks monotony and makes each section look like a separate unit. On the other side: the eye has to change direction in every section, scanning slows down, and the fast reading that a single-column layout offers is lost.

**What to test**
- Layout: Does a zigzag or a consistent alignment get more read?
- Section count: After how many sections does the zigzag become tiring?
- Visual weight: Do the images overshadow the text?
- Scanning: Do visitors skim past the sections?
- Device: On mobile, where the layout collapses to a single column, is there still an equivalent of the zigzag?

**KPIs to track**
- Primary Action Completion Rate: Does the layout increase action?
- Scroll Depth: Does reaching the bottom of the page increase?
- Section View Rate: Views of the sections must not fall.
- Time on Page: Reading time must not grow to an unacceptable level.
- Page Load Time: Extra images must not degrade speed.

**What not to do**
- Don’t change the layout and the number of sections in the same test.
- Don’t add meaningless images to sections just for the zigzag.
- Don’t count the layout that already collapses to a single column on mobile as a zigzag variant and compare it.
- Don’t randomly change the reading order (image first or text first) from section to section.
- Don’t sacrifice the keyboard and screen reader order to the visual layout.

---

## Soyut tema görselleri mi, gerçek ürün ekranları mı daha etkili?

Değişken: Sayfa görsellerinin türü · Fark: değiştir

Etiket: id=hl-023 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Abstract theme images or real product screens: which works better?

EN-Variable: Type of page imagery

Soyut veya kavramsal görseller estetik bir bütünlük kurar ve ürün henüz olgunlaşmamışken işe yarar. Gerçek ürün ekranları ise ne alındığını gösterir ve belirsizliği kaldırır; buna karşılık ekranlar karmaşık görünüp caydırabilir ve hızla eskiyip bakım yükü yaratabilir.

**Test edilmesi gerekenler**
- İçerik: Gerçek ürün görüntüsü aksiyonu artırıyor mu?
- Karmaşıklık: Ekran görüntüsü ürünü zor mu gösteriyor?
- Sonraki test: Gerçek ekran kazanırsa, tam ekran görüntüsü ile ürünün tek bir parçasına yakınlaşan kesit ayrı bir testte karşılaştırıldığında hangisi daha anlaşılır?
- İlk kullanım: Gerçek ekranı görüp kaydolan kullanıcı ilk oturumda temel işlevi daha kısa sürede buluyor mu?
- Segment: Ürünü tanımayan ile deneyimli ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Görsel türü aksiyonu artırıyor mu?
- Aksiyon Sonrası Tamamlama Oranı: Beklentisi netleşen kullanıcı sonraki adımda dökülmemeli.
- Kaydırma Derinliği: Görseller okumayı sürdürüyor mu?
- Sayfa Yüklenme Süresi: Görsel ağırlığı hızı bozmamalı.
- Erişilebilirlik: Görseller metin karşılıksız kalmamalı.

**Yapılmaması gerekenler**
- Üründe bulunmayan bir ekranı gerçek ürün görüntüsü gibi göstermeyin.
- Ekran görüntüsündeki verileri gerçek müşteri verisiymiş gibi sunmayın.
- Aynı testte görsel türü ile görsel sayısını birlikte değiştirmeyin.
- Okunmayacak kadar küçültülmüş ekran görüntüsünü “gerçek ürün gösterildi” saymayın.
- Eskimiş bir ekran görüntüsünü ürünün güncel hâli gibi göstermeyin.

### EN

Abstract or conceptual imagery creates aesthetic coherence and works while the product is still immature. Real product screens show what you get and remove uncertainty; on the other hand, screens can look complicated and put people off, and they age quickly and create a maintenance burden.

**What to test**
- Content: Does showing real product imagery increase action?
- Complexity: Does the screenshot make the product look hard?
- Next test: If the real screen wins, which is clearer when a full-screen capture and a crop zoomed in on a single part of the product are compared in a separate test?
- First use: Do users who sign up after seeing the real screen find the core function faster in their first session?
- Segment: Do people who don’t know the product and experienced visitors react differently?

**KPIs to track**
- Primary Action Completion Rate: Does the image type increase action?
- Post-Click Completion Rate: Users whose expectations are now clear must not drop off at the next step.
- Scroll Depth: Do the images keep people reading?
- Page Load Time: Image weight must not degrade speed.
- Accessibility Check: Images must not be left without a text alternative.

**What not to do**
- Don’t show a screen that doesn’t exist in the product as if it were real product imagery.
- Don’t present the data in a screenshot as if it were real customer data.
- Don’t change the image type and the number of images in the same test.
- Don’t count a screenshot shrunk until it is unreadable as “real product shown”.
- Don’t show an outdated screenshot as the current state of the product.

---

## İndirilebilir bir kaynak sunmak lead sayısını artırır mı?

Değişken: İndirilebilir kaynak teklifi · Fark: ekle

Etiket: id=hl-024 · mercek=Zamanlama · düzey=teklif · sektör=b2b · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does offering a downloadable resource raise lead volume?

EN-Variable: Downloadable resource offer

Rehber, şablon veya kontrol listesi karşılığında iletişim bilgisi istemek, satın almaya hazır olmayan ziyaretçiyi de yakalar. Riski: gelen kayıtların çoğu ürünle değil kaynakla ilgilenir, satış ekibinin yükü artar ve niteliksiz lead oranı yükselir. Asıl ölçülmesi gereken kayıt sayısı değil, atanan ziyaretçi başına nitelikli fırsat oranıdır.

**Test edilmesi gerekenler**
- Varlık: İndirilebilir kaynak sunmak nitelikli talebi artırıyor mu?
- Asıl yoldan sapma: Kaynağı indiren ziyaretçiler deneme veya satın alma adımı yerine kaynakla mı yetiniyor?
- Sonraki test: Kaynak kazanırsa, iletişim bilgisi istemeden serbest sunmak ayrı bir testte nitelikli talebi değiştiriyor mu?
- Nitelik: Gelen kayıtların kaçı gerçekten satışa uygun?
- Segment: Farklı kullanıcı tipleri kaynağa farklı mı ilgi gösteriyor?

**Takip edilecek ana KPI’lar**
- Nitelikli Fırsat Oranı (atanan ziyaretçi başına): Satış ekibinin nitelikli kabul ettiği fırsatların atanan ziyaretçiye oranı artıyor mu?
- Toplam Kayıt Oranı (atanan ziyaretçi başına): Hacim artıyor mu?
- Talep Başına Nitelik Oranı: Niteliksiz kayıt oranı kabul edilemez ölçüde artmamalı.
- Satış Ekibi İş Yükü: Takip edilemeyecek kadar kayıt birikmemeli.
- Ana Aksiyon Tamamlama Oranı: Asıl dönüşüm (deneme, satın alma) düşmemeli.

**Yapılmaması gerekenler**
- Kaynağı asıl dönüşümün önüne koyup satın almaya hazır ziyaretçiyi yavaşlatmayın.
- Vaat edilen içeriğe uymayan bir dosya sunmayın.
- İletişim izni ile indirme iznini tek onaya bağlamayın; izin kuralları pazara göre değişir.
- Aynı testte kaynağın konusu ile kayıt formunu birlikte değiştirmeyin.
- Kaynağı indiren kayıtları satışa hazır talep gibi doğrudan satış ekibine aktarmayın; ayrı bir takip akışına alın.

### EN

Asking for contact details in exchange for a guide, template or checklist also catches visitors who are not ready to buy. The risk: most of the incoming sign-ups are interested in the resource rather than the product, the sales team’s load grows and the share of unqualified leads rises. What really needs to be measured is not the number of sign-ups but the qualified opportunity rate per assigned visitor.

**What to test**
- Presence: Does offering a downloadable resource increase qualified leads?
- Diversion from the main path: Do visitors who download the resource settle for it instead of moving on to the trial or purchase step?
- Next test: If the resource wins, does offering it freely without asking for contact details change qualified leads in a separate test?
- Quality: How many of the incoming sign-ups are genuinely sales-ready?
- Segment: Do different user types show different interest in the resource?

**KPIs to track**
- Qualified Opportunity Rate (per assigned visitor): Does the ratio of opportunities the sales team accepts as qualified to assigned visitors increase?
- Total Sign-up Rate (per assigned visitor): Does volume increase?
- Qualification Rate per Lead: The rate of unqualified sign-ups must not rise to an unacceptable level.
- Sales Team Workload: Sign-ups must not pile up beyond what can be followed up.
- Primary Action Completion Rate: The main conversion (trial, purchase) must not fall.

**What not to do**
- Don’t put the resource ahead of the main conversion and slow down visitors who are ready to buy.
- Don’t offer a file that doesn’t match the promised content.
- Don’t tie contact permission and download permission to a single consent; consent rules vary by market.
- Don’t change the topic of the resource and the sign-up form in the same test.
- Don’t pass sign-ups from resource downloads straight to the sales team as sales-ready leads; put them into a separate follow-up flow.

---

## Para iade garantisini satın alma butonunun yanına taşımak satın almayı artırır mı?

Değişken: Para iade garantisi ifadesinin konumu · Fark: taşı

Etiket: id=hl-025 · mercek=Güven · düzey=güven · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does moving the money-back guarantee next to the buy button raise purchases?

EN-Variable: Position of the money-back guarantee statement

Koşulsuz iade vaadi algılanan riski satıcıya aktarır ve kararsız ziyaretçiyi ilerletir. Bu testte garanti metni aynı kalır; yalnızca sayfanın altındaki yerinden satın alma butonunun hemen yanına taşınır. Bedeli: iade oranı yükselebilir, operasyonel maliyet artabilir ve garanti çok öne çıkarsa ürüne güvenilmediği izlenimi bile doğurabilir. Kazanç, ek satışın iade maliyetini aşıp aşmadığına bağlıdır.

**Test edilmesi gerekenler**
- Konum: Garantiyi satın alma butonunun yanına taşımak satışı artırıyor mu?
- Sonraki test: Yeni konum kazanırsa, garanti süresini uzatmak ayrı bir testte satış ile iade dengesini nasıl değiştiriyor?
- Ters sinyal: Garanti butonun yanına gelince ziyaretçiler kısa ankette ürünün kalitesinden daha çok şüphe ettiğini söylüyor mu?
- Maliyet dengesi: Artan satış artan iadeyi karşılıyor mu?
- Segment: İlk kez alan ile tekrar alan müşteri farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Net Gelir: İade düşüldükten sonra gelir artıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı artıyor mu?
- İade Oranı (30 gün): İade artışı kârlılığı bozacak seviyeye çıkmamalı.
- İade İşlem Maliyeti (30 gün): Operasyonel yük taşınabilir kalmalıdır.
- Tekrar Satın Alma Oranı (60 gün): Güven artışı geri dönüşü düşürmemeli.

**Yapılmaması gerekenler**
- Uygulanmayacak bir garanti sözü vermeyin.
- Garantiyi butonun yanına taşıyıp koşullarını okunmaz küçüklükte yazmayın.
- Aynı testte garantinin konumu ile garanti süresini veya metnini birlikte değiştirmeyin.
- Yalnızca bazı ürünlerde geçerli garantiyi, sayfadaki her ürünü kapsıyormuş gibi butonun yanına koymayın.
- Yasal asgari iade hakkını bir pazarlama vaadi gibi sunmayın; zaten zorunlu olabilir.

### EN

An unconditional refund promise shifts the perceived risk to the seller and moves a hesitant visitor forward. In this test the guarantee text stays the same; it only moves from its place lower on the page to right next to the buy button. The cost: the return rate may rise, operational cost may increase, and if the guarantee is pushed too prominently it can even give the impression that the product isn’t trusted. The gain depends on whether the extra sales outweigh the cost of returns.

**What to test**
- Position: Does moving the guarantee next to the buy button increase sales?
- Next test: If the new position wins, how does extending the guarantee period change the balance between sales and returns in a separate test?
- Reverse signal: Once the guarantee sits next to the button, do visitors in a short survey say they doubt the product’s quality more?
- Cost balance: Do the extra sales cover the extra returns?
- Segment: Do first-time buyers and repeat customers react differently?

**KPIs to track**
- Net Revenue per Visitor: Does revenue increase after returns are deducted?
- Conversion Rate (CR): Does the purchase rate increase?
- Return Rate (30 days): The rise in returns must not reach a level that hurts profitability.
- Return Handling Cost (30 days): The operational load must stay manageable.
- Repeat Purchase Rate (60 days): The trust gain must not lower return visits.

**What not to do**
- Don’t make a guarantee promise that won’t be honored.
- Don’t move the guarantee next to the button and write its terms in unreadably small type.
- Don’t change the position of the guarantee and the guarantee period or text in the same test.
- Don’t put a guarantee valid only for some products next to the button as if it covered every product on the page.
- Don’t present the legal minimum right of return as a marketing promise; it may already be mandatory.

---

## Ziyaretçiyi kendi diliyle karşılamak işe yarar mı?

Değişken: Karşılama ifadesinin dili · Fark: değiştir

Etiket: id=hl-026 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does greeting visitors in their own language pay off?

EN-Variable: Language of the greeting

Tarayıcı diline veya konuma göre karşılama ifadesini uyarlamak yakınlık kurar ve doğru yere geldiğini hissettirir. Riski: yanlış tespit edilen dil rahatsız eder, yarım çevrilmiş bir sayfa güveni düşürür ve karşılama dili ile içerik dili farklı olursa kafa karışıklığı yaratır.

**Test edilmesi gerekenler**
- Karşılama: Ziyaretçinin diliyle karşılamak aksiyonu artırıyor mu?
- Doğruluk: Dil tespiti ne oranda doğru çalışıyor?
- Tutarlılık: Karşılama çevrildiği hâlde içerik çevrilmemişse etkisi ne oluyor?
- Sonraki test: Dil uyarlaması kazanırsa, görünür bir dil değiştirme seçeneği eklemek ayrı bir testte farkı değiştiriyor mu?
- Segment: Çok dilli pazarlarda hangi ziyaretçi grubu daha çok fayda görüyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Karşılama aksiyonu artırıyor mu?
- Hemen Çıkma Oranı: Yanlış dil çıkışı artırmamalı.
- Dil Değiştirme Oranı: Ziyaretçilerin dili elle değiştirmesi artmamalı.
- Sayfa Yüklenme Süresi: Tespit gecikme yaratmamalı.
- Dil Bazlı Dönüşüm Farkı: Hangi dilde kazanç var, hangisinde yok?

**Yapılmaması gerekenler**
- Dil tespitini konum bilgisinden türetip ziyaretçiye bunu ima etmeyin.
- İçeriğin tamamı çevrilmemişken yalnızca karşılamayı çevirmeyi kalıcı çözüm saymayın.
- Ziyaretçinin seçtiği dili otomatik tespitle ezmeyin.
- Aynı testte hem dili hem içerik düzenini değiştirmeyin.
- Tek dilde ölçüp sonucu tüm dillere genellemeyin.

### EN

Adapting the greeting to the browser language or location builds familiarity and makes the visitor feel they are in the right place. The risk: a wrongly detected language is irritating, a half-translated page lowers trust, and when the greeting language differs from the content language, it creates confusion.

**What to test**
- Greeting: Does greeting visitors in their own language increase action?
- Accuracy: How accurately does the language detection work?
- Consistency: What is the effect when the greeting is translated but the content isn’t?
- Next test: If the language adaptation wins, does adding a visible language switcher change the difference in a separate test?
- Segment: In multilingual markets, which visitor group benefits more?

**KPIs to track**
- Primary Action Completion Rate: Does the greeting increase action?
- Bounce Rate: The wrong language must not increase exits.
- Language Switch Rate: Manual language changes by visitors must not increase.
- Page Load Time: Detection must not add delay.
- Per-Language Conversion Gap: In which language is there a gain and in which none?

**What not to do**
- Don’t derive the language detection from location information and hint at that to the visitor.
- Don’t treat translating only the greeting as a permanent solution while the content is not fully translated.
- Don’t override the language the visitor chose with automatic detection.
- Don’t change both the language and the content layout in the same test.
- Don’t measure in a single language and generalize the result to all languages.

---

## Referansları kaydırıcıda mı, hepsi görünür hâlde mi sunmalı?

Değişken: Referansların sunum düzeni · Fark: değiştir

Etiket: id=hl-027 · mercek=Güven · düzey=sosyal-kanıt · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Testimonials in a carousel or all visible: which works better?

EN-Variable: Presentation layout of testimonials

Kaydırıcı çok sayıda referansı az yerde barındırır ve sayfayı kısaltır. Bedeli: ilk kartın ötesini çok az ziyaretçi görür, otomatik ilerleyen kaydırıcı okumayı yarıda keser ve kaydırılabilir olduğu fark edilmezse geri kalan içerik boşa gider. Hepsini göstermek ise sayfayı uzatır ama tamamının görülmesini sağlar.

**Test edilmesi gerekenler**
- Biçim: Kaydırıcı mı, hepsi görünür düzen mi daha çok aksiyon getiriyor?
- Görülme: Kaydırıcıda ilk kartın ötesini kaç ziyaretçi görüyor?
- Otomatik ilerleme: Kendiliğinden dönen kaydırıcı okumayı kesiyor mu?
- Sonraki test: Kazanan düzen sabitken gösterilen referans sayısı ayrı bir testte etkiyi değiştiriyor mu? (3 / 6 / 9)
- Cihaz: Mobilde kaydırıcı parmakla gezinmeye daha mı uygun?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Sunum biçimi aksiyonu artırıyor mu?
- Referans Görülme Oranı: Görülen referans sayısı düşmemeli.
- Referans Etkileşim Oranı: Referanslarla etkileşim artıyor mu?
- Kaydırma Derinliği: Uzayan sayfa altına inmeyi azaltmamalı.
- Erişilebilirlik: Kaydırıcı klavyeyle gezilemez olmamalı, otomatik ilerleme durdurulamaz olmamalı.

**Yapılmaması gerekenler**
- Otomatik ilerleyen ve durdurulamayan bir kaydırıcı kurmayın.
- Aynı testte sunum biçimi ile referans sayısını birlikte değiştirmeyin.
- Kaydırılabilir olduğunu gösteren işareti kaldırmayın.
- En güçlü referansı bir kolda başa, diğer kolda sona koymayın; referans sırası iki kolda aynı kalmalı.
- Hareket azaltma tercihini yok sayan bir geçiş animasyonu kullanmayın.

### EN

A carousel holds many testimonials in little space and shortens the page. The cost: few visitors see beyond the first card, an auto-advancing carousel interrupts reading, and if it isn’t noticed that it can be scrolled, the rest of the content is wasted. Showing everything makes the page longer but ensures all of it is seen.

**What to test**
- Format: Does a carousel or an all-visible layout bring more action?
- Visibility: How many visitors see beyond the first card in the carousel?
- Auto-advance: Does a carousel that rotates on its own interrupt reading?
- Next test: With the winning layout fixed, does the number of testimonials shown change the effect in a separate test? (3 / 6 / 9)
- Device: Is a carousel better suited to finger navigation on mobile?

**KPIs to track**
- Primary Action Completion Rate: Does the presentation format increase action?
- Testimonial View Rate: The number of testimonials seen must not fall.
- Testimonial Engagement Rate: Does engagement with the testimonials increase?
- Scroll Depth: The longer page must not reduce scrolling to the bottom.
- Accessibility Check: The carousel must not become impossible to navigate by keyboard, and auto-advance must not become impossible to stop.

**What not to do**
- Don’t build a carousel that auto-advances and can’t be paused.
- Don’t change the presentation format and the number of testimonials in the same test.
- Don’t remove the cue that shows the carousel can be scrolled.
- Don’t put the strongest testimonial first in one arm and last in the other; the testimonial order must stay the same in both arms.
- Don’t use a transition animation that ignores the reduced-motion preference.

---

## Sosyal medya takipçi veya beğeni sayısını göstermek güveni artırır mı?

Değişken: Sosyal medya takipçi sayısı göstergesi · Fark: ekle

Etiket: id=hl-028 · mercek=Güven · düzey=sosyal-kanıt · sektör=genel · pazar=global · emek=düşük · durum=klasik · tarih=2026-11

EN: Does showing social media follower or like counts build trust?

EN-Variable: Social media follower count indicator

Bir marka sayfasının yanında görünen takipçi veya beğeni sayısı, ürünün başkaları tarafından da tercih edildiğini gösteren dolaylı bir sosyal kanıttır. Risk, sayının küçük veya büyümekte olduğu bir markada beklenenin tersi bir etki yaratmasıdır; düşük bir sayı, kanıt yerine şüphe uyandırabilir.

**Test edilmesi gerekenler**
- Eşik: Sayı belirli bir büyüklüğün altındaysa (ör. 500’ün altı) göstermek zarar mı veriyor?
- Sonraki test: Sayaç kazanırsa, ham sayı ile yuvarlanmış kısaltma (ör. “12 bin+”) ayrı bir testte karşılaştırıldığında hangisi daha güvenilir bulunuyor?
- Dış platforma kaçış: Sayaca tıklayıp sosyal medya sayfasına giden ziyaretçilerin kaçı siteye dönüp aksiyonu tamamlıyor?
- Ziyaretçi tipi: Markayı zaten tanıyan geri dönen ziyaretçi ile ilk kez gelen ziyaretçi sayaca farklı mı tepki veriyor?
- Cihaz: Mobilde sayaç dikkat dağıtıp asıl CTA’dan uzaklaştırıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sayaç göstermek satın alma veya kayıt oranını artırıyor mu?
- Sayfa Yüklenme Süresi: Sosyal platformdan çekilen sayaç bileşeni sayfayı yavaşlatmamalı.
- Güven Algısı (anket): Sayaç güveni artırdığını hissettiriyor mu? Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Tıklama Oranı (CTR): Sayaç kendisi tıklanıp dış platforma gidiş yaratıyor mu? Gidiyorsa bu bir kayıp noktasıdır.
- Sayfada Kalma Süresi: Sayaç dikkat dağıtıp asıl aksiyonu geciktirmemeli.

**Yapılmaması gerekenler**
- Gerçek olmayan veya şişirilmiş bir sayıyı göstermeyin.
- Aynı testte sayacın biçimini ve konumunu birlikte değiştirmeyin.
- Sayı küçükken büyük bir görsel ağırlıkla öne çıkarmayın; ağırlığı sayının gerçek gücüne göre ayarlayın.
- Farklı platformlardan gelen sayıları tek bir toplam gibi birleştirip yanıltıcı bir büyüklük izlenimi yaratmayın.
- Sayacı otomatik güncellemiyorsanız güncel olmayan bir tarihte donmuş hâlde bırakmayın.

### EN

A follower or like count shown next to a brand page is an indirect form of social proof, showing that others also prefer the product. The risk is that on a brand where the number is small or still growing, it has the opposite of the expected effect; a low number can raise suspicion instead of proof.

**What to test**
- Threshold: If the number is below a certain size (e.g. under 500), does showing it do harm?
- Next test: If the counter wins, which is found more trustworthy when the raw number and a rounded shorthand (e.g. “12K+”) are compared in a separate test?
- Leaving for an outside platform: Of the visitors who click the counter and go to the social media page, how many come back to the site and complete the action?
- Visitor type: Do returning visitors who already know the brand and first-time visitors react differently to the counter?
- Device: On mobile, does the counter distract and pull people away from the main CTA?

**KPIs to track**
- Conversion Rate (CR): Does showing the counter increase the purchase or sign-up rate?
- Page Load Time: A counter component pulled from the social platform must not slow the page.
- Trust Perception (survey): Does the counter make people feel it increased trust? The denominator is the visitors who answer the survey; the response rate (responders / assigned visitors) is tracked in both arms and is a diagnostic signal.
- Click-Through Rate (CTR): Is the counter itself clicked, sending people to the outside platform? If so, that is a point of loss.
- Time on Page: The counter must not distract and delay the main action.

**What not to do**
- Don’t show a number that isn’t real or is inflated.
- Don’t change the format and the position of the counter in the same test.
- Don’t make a small number stand out with heavy visual weight; set the weight according to the number’s real strength.
- Don’t combine numbers from different platforms into a single total and create a misleading impression of size.
- If you don’t update the counter automatically, don’t leave it frozen at an outdated date.

---

## Sayfa açılışında içeriği kısmen kaplayan büyük bir karşılama ekranı ilgiyi artırır mı?

Değişken: Açılıştaki kısmi karşılama ekranı · Fark: ekle

Etiket: id=hl-029 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=klasik · tarih=2026-11

EN: Does a large welcome screen that partly covers the content on page load raise interest?

EN-Variable: Partial welcome screen on page open

Küçük bir pop-up’tan farklı olarak, kısmi karşılama ekranı sayfanın büyük bir kısmını (genelde ilk ekranın tamamına yakınını) tek bir mesaj veya teklifle kaplar, altındaki içeriğin bir kısmı kenarlarda görünür kalır. Amaç dikkati tek bir noktaya toplamaktır; risk, ziyaretçinin asıl sayfaya hiç ulaşmadan ayrılmasıdır.

**Test edilmesi gerekenler**
- Kapsam: Ekranın ne kadarını kaplamalı; tamamı mı, büyük bir kısmı mı?
- Kapatma sonrası: Ekranı kapatan ziyaretçiler asıl sayfada kaydırmaya devam ediyor mu, yoksa ilk ekranda mı ayrılıyor?
- Kapatma: Kapatma işareti yeterince görünür mü, yoksa yanlışlıkla mı atlanıyor?
- Sonraki test: Karşılama ekranı kazanırsa, ekranı kısa bir gecikmeyle göstermek ayrı bir testte rahatsızlığı azaltıyor mu?
- Segment: İlk kez gelen ile daha önce siteyi ziyaret etmiş kullanıcıya aynı ekran mı gösterilmeli?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Sayfaya atanan ziyaretçilerin sayfanın ana aksiyonunu tamamlama oranı artıyor mu? Payda ekranı geçenler değil, iki koldaki tüm ziyaretçilerdir.
- Hemen Çıkma Oranı: Karşılama ekranı kaynaklı hemen çıkma artmamalı.
- Teklif Kabul Oranı: Ekrandaki teklifi kabul eden ziyaretçi oranı nedir?
- Sayfa Yüklenme Algısı (anket): Ekran, sayfanın yavaş açıldığı hissini vermemeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Tekrar Ziyaret Oranı: Atanan ziyaretçilerin siteye tekrar dönüş oranı düşmemeli.

**Yapılmaması gerekenler**
- Kapatma işaretini gizleyip ziyaretçiyi teklifi kabul etmeye zorlamayın.
- Aynı testte ekranın kapsamını ve içeriğini birlikte değiştirmeyin.
- Ekranı, arama motoru botlarının asıl içeriği görmesini engelleyecek şekilde kurmayın.
- Mobilde ekranı kapatma alanını dokunma hedefi için çok küçük bırakmayın.
- Ziyaretçi bir kez kapattıysa aynı oturumda tekrar göstermeyin.

### EN

Unlike a small pop-up, a partial welcome screen covers a large part of the page (usually nearly the whole first screen) with a single message or offer, while some of the content beneath remains visible at the edges. The aim is to focus attention on one point; the risk is that the visitor leaves without ever reaching the actual page.

**What to test**
- Coverage: How much of the screen should it cover, all of it or a large part?
- After dismissal: Do visitors who dismiss the screen keep scrolling on the actual page, or do they leave on the first screen?
- Dismissal: Is the close icon visible enough, or is it skipped by accident?
- Next test: If the welcome screen wins, does showing it after a short delay reduce the annoyance in a separate test?
- Segment: Should first-time visitors and users who have visited the site before be shown the same screen?

**KPIs to track**
- Primary Action Completion Rate: Does the rate at which visitors assigned to the page complete its main action increase? The denominator is all visitors in both arms, not those who get past the screen.
- Bounce Rate: Bounces caused by the welcome screen must not increase.
- Offer Acceptance Rate: What share of visitors accept the offer on the screen?
- Page Load Perception (survey): The screen must not give the feeling that the page opens slowly. The denominator is the visitors who answer the survey; the response rate (responders / assigned visitors) is tracked in both arms and is a diagnostic signal.
- Return Visit Rate: The rate at which assigned visitors come back to the site must not fall.

**What not to do**
- Don’t hide the close icon and force the visitor to accept the offer.
- Don’t change the coverage and the content of the screen in the same test.
- Don’t build the screen in a way that stops search engine bots from seeing the actual content.
- On mobile, don’t leave the close area too small for a touch target.
- If a visitor has dismissed it once, don’t show it again in the same session.

---

## Anasayfayı tek bir anlatı yerine ziyaretçi tipine göre ayrı bloklara bölmek ilerlemeyi artırır mı?

Değişken: Anasayfanın ziyaretçi tipine göre bölünmesi · Fark: değiştir

Etiket: id=hl-030 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does splitting the homepage into separate blocks per visitor type, instead of one narrative, raise progress?

EN-Variable: Splitting the homepage by visitor type

Çoğu anasayfa tek bir ziyaretçi profilini varsayıp doğrusal bir anlatı kurar (başlık → fayda → sosyal kanıt → CTA). Farklı ziyaretçi tipleri (ör. bireysel kullanıcı / kurumsal alıcı, yeni müşteri / mevcut müşteri) farklı sorularla geldiğinde bu tek anlatı hiçbirine tam oturmaz. Sayfayı bir yönlendirme sayfası gibi kurup her tipe ayrı bir blok sunmak (ör. “Bireysel kullanım için” / “Ekibiniz için” iki ayrı kart) ilgili ziyaretçiyi daha hızlı doğru içeriğe taşıyabilir; riski, tek bir net mesaj yerine sayfanın başında birden fazla seçenek sunmanın kararsızlık yaratmasıdır. Bu, “Ziyaretçinin geldiği kaynağa göre başlığı değiştirmek işe yarar mı?” senaryosundan farklıdır: orada tek başlık ziyaretçiye göre değişir, burada ekranda aynı anda birden fazla yol görünür durur.

**Test edilmesi gerekenler**
- Yapı: Ziyaretçi tipine göre ayrı bloklar sunmak toplam ilerlemeyi artırıyor mu?
- Kararsızlık: Birden fazla yol sunmak, hangisini seçeceğini bilemeyen ziyaretçi yaratıyor mu?
- Sonraki test: Blok yapısı kazanırsa, hangi ziyaretçi tipi bloğunun üstte durduğu ayrı bir testte ilerlemeyi değiştiriyor mu?
- Atlanan anlatı: Bloğa tıklayıp ilerleyen ziyaretçi, tek anlatıdaki fayda ve sosyal kanıt bölümlerini görmeden mi karar veriyor?
- Segment: Reklamdan gelen ile organik gelen ziyaretçi doğru bloğu aynı oranda mı buluyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı: Blok yapısı toplam ilerlemeyi artırıyor mu?
- İlgili Bloğa Tıklama Oranı (tanısal): Ziyaretçi kendi profiline uyan bloğu buluyor mu?
- Yanlış Blok Oranı: Yanlış bloğa girip geri dönen ziyaretçi oranı artmamalı.
- Hemen Çıkma Oranı: Kararsızlık kaynaklı çıkış artmamalı.
- Karar Süresi: İlk tıklamaya kadar geçen süre kabul edilemez ölçüde uzamamalı.

**Yapılmaması gerekenler**
- Aynı testte blok sayısını ve sayfanın geri kalanındaki mesajı birlikte değiştirmeyin.
- İkiden fazla ziyaretçi tipi bloğunu aynı ekranda sıkıştırıp seçim felcine yol açmayın.
- Bloklardan birini gerçek trafik dağılımıyla orantısız büyüklükte öne çıkarmayın.
- Mobilde blokları küçültüp aralarındaki dokunma alanını daraltmayın.
- Yanlış bloğa giren ziyaretçinin doğru bloğa geçişini zorlaştıran bir yapı kurmayın.

### EN

Most homepages assume a single visitor profile and build a linear narrative (headline → benefit → social proof → CTA). When different visitor types (e.g. individual user / enterprise buyer, new customer / existing customer) arrive with different questions, this single narrative fits none of them well. Building the page like a routing page and giving each type its own block (e.g. two separate cards, “For personal use” / “For your team”) can move the relevant visitor to the right content faster; the risk is that offering several options at the top of the page instead of one clear message creates indecision. This differs from the “Does changing the headline to match the visitor’s traffic source pay off?” scenario: there a single headline changes by visitor, here several paths stay visible on the screen at the same time.

**What to test**
- Structure: Does offering separate blocks by visitor type increase overall progress?
- Indecision: Does offering more than one path create visitors who can’t decide which to choose?
- Next test: If the block structure wins, does which visitor-type block sits on top change progress in a separate test?
- Skipped narrative: Does a visitor who clicks a block and moves on decide without seeing the benefit and social-proof sections of the single narrative?
- Segment: Do visitors from ads and organic visitors find the right block at the same rate?

**KPIs to track**
- Primary Action Completion Rate: Does the block structure increase overall progress?
- Relevant Block Click Rate (diagnostic): Does the visitor find the block that matches their profile?
- Wrong Block Rate: The share of visitors who enter the wrong block and come back must not rise.
- Bounce Rate: Exits caused by indecision must not increase.
- Time to Decision: The time to the first click must not grow to an unacceptable level.

**What not to do**
- Don’t change the number of blocks and the message on the rest of the page in the same test.
- Don’t cram more than two visitor-type blocks onto the same screen and cause choice paralysis.
- Don’t make one of the blocks disproportionately large compared with the real traffic split.
- On mobile, don’t shrink the blocks and narrow the touch area between them.
- Don’t build a structure that makes it hard for a visitor who enters the wrong block to switch to the right one.

---

## Yeni ve dönen kullanıcıya farklı anasayfa göstermek işe yarar mı?

Değişken: Kullanıcı tipine göre anasayfa ayrımı · Fark: değiştir

Etiket: id=hl-031 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing new and returning visitors different homepages pay off?

EN-Variable: Homepage split by user type

Yeni ziyaretçinin marka bilgisine, dönen ziyaretçinin ise hızlı devam yoluna ihtiyacı vardır. Aynı anasayfayı ikisine de göstermek her iki grubu da yarı yolda bırakabilir.

**Test edilmesi gerekenler**
- Devam bloğu: Dönen kullanıcıya “kaldığın yerden devam” göstermek dönüşümü artırıyor mu?
- Sonraki test: Ayrım kazanırsa, yeni kullanıcının anasayfası (marka vitrini / doğrudan ürün) ayrı bir testte dönüşümü değiştiriyor mu?
- Sinyal: Segment ayrımı hangi veriyle yapılmalı? (çerez / giriş / sepet)
- Derinlik: Kişiselleştirme arttıkça etki artıyor mu, doyuma mı ulaşıyor?
- Hata payı: Yanlış segmentlenen kullanıcıda deneyim bozuluyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Segment bazlı okunmalı.
- Anasayfa Tıklama Oranı: İlk blok fark ediliyor mu?
- Sepete Dönüş Oranı: Dönen kullanıcı akışı.
- Yeni Kullanıcı Dönüşümü: Düşmemeli.
- Sayfa Yüklenme Süresi: Kişiselleştirme LCP’yi bozmamalı.

**Yapılmaması gerekenler**
- Dönen kullanıcıya “kaldığın yerden devam” bloğunda artık satışta olmayan bir ürünü göstermeyin.
- Kişisel veriyi anasayfada açıkça göstermeyin (isim, adres).
- Yanlış segmentte varsayılan deneyimi bozmayın.
- Aynı testte hem segmenti hem içerik bloklarını değiştirmeyin.
- Kişiselleştirmeyi önbellek dışı bırakıp sayfayı yavaşlatmayın.

### EN

A new visitor needs brand information, while a returning visitor needs a quick way to continue. Showing the same homepage to both can leave both groups halfway there.

**What to test**
- Continue block: Does showing returning users a “pick up where you left off” block increase conversion?
- Next test: If the split wins, does the new user’s homepage (brand showcase / straight to products) change conversion in a separate test?
- Signal: What data should the segment split be based on? (cookie / login / cart)
- Depth: As personalization deepens, does the effect grow or reach saturation?
- Margin of error: Is the experience broken for a wrongly segmented user?

**KPIs to track**
- Revenue per Visitor (RPV): Should be read by segment.
- Homepage Click Rate: Is the first block noticed?
- Return-to-Cart Rate: The returning user flow.
- New User Conversion: Must not fall.
- Page Load Time: Personalization must not hurt LCP (Largest Contentful Paint).

**What not to do**
- Don’t show a product that is no longer on sale in the “pick up where you left off” block for a returning user.
- Don’t display personal data openly on the homepage (name, address).
- Don’t break the default experience for a wrongly segmented user.
- Don’t change both the segment and the content blocks in the same test.
- Don’t leave personalization outside the cache and slow down the page.

---

## Son gezilen ürünler şeridi geri dönüşü artırır mı?

Değişken: Son gezilen ürünler şeridi · Fark: ekle

Etiket: id=hl-032 · mercek=Çaba · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a recently viewed products strip help visitors pick up where they left off?

EN-Variable: Recently viewed products strip

Dönen ziyaretçinin anasayfada ilk aradığı çoğu zaman bir önceki ziyarette baktığı üründür; onu bulmak için aramayı ya da kategoriyi baştan yürümesi gerekir. Anasayfaya son gezilen ürünler şeridi eklemek bu yolu tek dokunuşa indirir ve kişinin kendi geçmişine dayandığı için algoritmik öneriden daha alakalıdır. Riski: şerit çok satanlar ve kampanya bloklarını aşağı iter; satın alınmış ya da tükenmiş ürünü tekrar göstermek deneyimi bozar.

**Test edilmesi gerekenler**
- Sayı: Kaç ürün göstermek optimum? (3 / 6 / 10)
- Varlık: Son gezilen ürünler şeridi, dönen kullanıcının satın almasını artırıyor mu?
- Yamyamlık: Şerit çok satanlar bloğunun performansını yiyor mu?
- Cihaz: Ekranın dar olduğu mobilde şerit, masaüstüne göre çok satanlar bloğunu daha mı çok aşağı itip tıklamasını azaltıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Geri dönen kullanıcı satın alıyor mu?
- Şerit Tıklama Oranı: Blok fark ediliyor mu?
- Ürün Detay Geçiş Oranı: Trafik nereye kayıyor?
- Çok Satanlar Tıklaması: Yamyamlık olmamalı.
- Anasayfa Çıkış Oranı: Artmamalı.

**Yapılmaması gerekenler**
- Satın alınmış ürünü tekrar göstermeyin.
- Stokta olmayan ürünü şeritte bırakmayın.
- Şeridi ilk ekranın tamamını kaplayacak kadar büyütmeyin.
- Aynı testte öneri algoritmasını da değiştirmeyin.
- Gizli gezinme oturumlarını şeride dahil etmeyin.

### EN

What a returning visitor looks for first on the homepage is often the product they looked at on the previous visit; to find it they have to walk through search or the category again. Adding a recently viewed products strip to the homepage cuts that path to a single tap, and because it is based on the person’s own history it is more relevant than an algorithmic recommendation. The risk: the strip pushes the best sellers and campaign blocks down, and showing a product that was already bought or is out of stock again spoils the experience.

**What to test**
- Count: How many products is optimal? (3 / 6 / 10)
- Presence: Does the recently viewed products strip increase purchases by returning users?
- Cannibalization: Does the strip eat into the performance of the best-sellers block?
- Device: On mobile, where the screen is narrow, does the strip push the best-sellers block down more than on desktop and reduce its clicks?

**KPIs to track**
- Conversion Rate (CR): Does the returning user buy?
- Strip Click Rate: Is the block noticed?
- Product Detail Transition Rate: Where does the traffic shift?
- Best-Seller Clicks: There must be no cannibalization.
- Homepage Exit Rate: Must not increase.

**What not to do**
- Don’t show a product that has been purchased again.
- Don’t leave an out-of-stock product in the strip.
- Don’t enlarge the strip until it covers the whole first screen.
- Don’t change the recommendation algorithm in the same test.
- Don’t include private browsing sessions in the strip.

---

## Mobil webe uygulama indirme banner’ı eklemek web dönüşümünü düşürüyor mu?

Değişken: Uygulama indirme banner’ı · Fark: ekle

Etiket: id=hl-033 · mercek=Zamanlama · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does adding an app download banner to the mobile web lower web conversion?

EN-Variable: App download banner

Mobil webe eklenen uygulama indirme banner’ı kurulum sayısını artırır ama devam eden oturumu böler. Bu test iki hedefin çakıştığı klasik bir örnektir; tek metrikle okunursa yanlış karar verilir.

**Test edilmesi gerekenler**
- Kazanç: Banner uygulama kurulumunu ne kadar artırıyor?
- Kayıp: Aynı oturumdaki web dönüşümü ne kadar düşüyor?
- Segment: Sadece yeni ziyaretçiye göstermek dengeyi kuruyor mu?
- Kurulum sonrası: Banner’dan uygulamayı kuran kullanıcı, webde yarım kalan işlemini uygulamada tamamlıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İki kanalı birlikte okuyan metrik.
- Uygulama Kurulum Oranı: Banner’ın ana amacı.
- Web Dönüşüm Oranı (CR): Kayıp tarafı.
- Oturum Devam Oranı: Kullanıcı akıştan kopmamalı.
- 7. Gün Elde Tutma: Kurulum kalıcı mı?

**Yapılmaması gerekenler**
- Uygulaması zaten kurulu olan kullanıcıya indirme banner’ı göstermeyin; uygulamayı açma bağlantısı ayrı bir durumdur.
- Banner’ı kapatılamaz yapmayın.
- Ödeme akışının içinde göstermeyin.
- Her sayfada tekrar tekrar açmayın.
- Aynı testte banner’ı eklerken web fiyatını veya uygulamaya özel indirim teklifini de değiştirmeyin.

### EN

An app download banner added to the mobile web raises the number of installs but interrupts the ongoing session. This test is a classic case of two goals colliding; read with a single metric, it leads to the wrong decision.

**What to test**
- Gain: How much does the banner increase app installs?
- Loss: How much does web conversion in the same session fall?
- Segment: Does showing it only to new visitors strike the balance?
- After install: Does a user who installs the app from the banner finish in the app the action left unfinished on the web?

**KPIs to track**
- Revenue per Visitor (RPV): The metric that reads both channels together.
- App Install Rate: The banner’s main purpose.
- Web Conversion Rate (CR): The loss side.
- Session Continuation Rate: The user must not be pulled out of the flow.
- Day-7 Retention: Is the install lasting?

**What not to do**
- Don’t show a download banner to a user who already has the app installed; an open-the-app link is a separate case.
- Don’t make the banner impossible to close.
- Don’t show it inside the payment flow.
- Don’t pop it open again and again on every page.
- Don’t also change the web price or an app-only discount offer in the same test while adding the banner.
