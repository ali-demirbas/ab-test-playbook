# Mobil Uygulama

Yolculuk aşaması: yüklü uygulamanın içindeki akışlar (onboarding, izinler, uygulama anasayfasının düzeni). Mobil web anları (uygulama indirme banner’ı, çıkış niyeti pop-up’ı, son gezilen ürünler şeridi, yeni ve dönen ziyaretçiye ayrı anasayfa) web dosyalarındadır: `home-landing.md` ve `category-listing.md`. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Servis ikonlarını büyütmek davranışı değiştirir mi?

Değişken: Öncelikli servis ikonunun boyutu · Fark: değiştir

Etiket: id=ma-001 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does enlarging service icons change behavior?

EN-Variable: Size of the priority service icon

Tüm servisleri eşit boyutta göstermek nötr bir deneyim yaratır. Öncelikli servisleri büyütmek o servislere yönelmeyi artırabilir ama diğerlerini gölgeleyebilir.

**Test edilmesi gerekenler**
- Vurgu: Öncelikli servisin ikonunu büyütmek tıklamayı artırıyor mu?
- Segment: Öncelikli servisi daha önce kullanmış kullanıcı ile hiç kullanmamış kullanıcı büyük ikona farklı mı tepki veriyor?
- Yan etki: Diğer servislerin tıklanması azalıyor mu?
- Sayı: Kaç servisi öne çıkarmak optimum? (1 / 2 / 3)

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Öne çıkarılan servisin tamamlama oranı yükseliyor mu?
- İkon Tıklama Oranı (CTR): Büyütülen ikon daha çok tıklanıyor mu?
- Kategori Giriş Oranı: Servise giriş hızlanıyor mu?
- Diğer Servis Kullanım Oranı: Gölgelenen servisleri kullanan atanan kullanıcıların payı düşmemeli.
- Navigasyon Verimliliği: Hedef sayfaya daha az adımda ulaşılıyor mu?

**Yapılmaması gerekenler**
- Aynı anda çok fazla servisi farklılaştırmayın; ikiyi geçmeyin.
- Büyük ikonun diğer kategorilerin erişimini gölgelemesine izin vermeyin.
- İkonu banner hissi verecek kadar büyütmeyin.
- Aynı testte ikonu büyütürken rengini veya konumunu da değiştirmeyin.
- Büyütülen ikonu, kullanıcının bulunduğu bölgede veya saatte hizmet vermeyen bir servise ayırmayın.

### EN

Showing all services at equal size creates a neutral experience. Enlarging priority services can raise engagement with them but may overshadow the others.

**What to test**
- Emphasis: Does enlarging the priority service’s icon raise taps?
- Segment: Do users who have used the priority service before and users who never have react differently to the large icon?
- Side effect: Do taps on the other services fall?
- Count: How many services is it best to feature? (1 / 2 / 3)

**KPIs to track**
- Conversion Rate (CR): Does the completion rate of the featured service rise?
- Icon Click-Through Rate (CTR): Is the enlarged icon tapped more?
- Category Entry Rate: Does entry into the service get faster?
- Other Services Usage Rate: The share of assigned users who use the overshadowed services must not drop.
- Navigation Efficiency: Is the target page reached in fewer steps?

**What not to do**
- Don’t differentiate too many services at once; no more than two.
- Don’t let the large icon overshadow access to other categories.
- Don’t enlarge the icon so much that it feels like a banner.
- Don’t change the icon’s color or position in the same test as enlarging it.
- Don’t give the enlarged icon to a service that isn’t available in the user’s area or at that time of day.

---

## Kayıt duvarı sert mi, yumuşak mı olmalı?

Değişken: Kayıt duvarının sertliği · Fark: değiştir

Etiket: id=ma-002 · mercek=Zamanlama · düzey=akış · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Should the sign-up wall be hard or soft?

EN-Variable: Strictness of the sign-up wall

Uygulamayı açar açmaz üye olmayı zorunlu tutmak (sert duvar), kullanıcının değeri görmeden ayrılmasına yol açabilir. Önce denemesine izin vermek (yumuşak duvar) ilk izlenimi artırabilir ama kayıt oranını düşürebilir.

**Test edilmesi gerekenler**
- Zamanlama: Kayıt ekranı açılışta mı, ilk değerden sonra mı gösterilmeli?
- Misafir modu: Sınırlı özellik seti kullanıcıyı ikna edip kaydolmaya yönlendiriyor mu?
- Duvar önü kaybı: Kayıt ekranını görüp hiçbir şey yapmadan uygulamayı kapatan kullanıcı oranı yumuşak duvarda düşüyor mu?
- Segment: Yeni kullanıcıda mı, geri dönende mi etki daha büyük?

**Takip edilecek ana KPI’lar**
- Kayıt Oranı: Toplam üye olma oranı düşüyor mu, artıyor mu?
- Aktivasyon Oranı: Misafir kullanıcı temel aksiyonu tamamlıyor mu?
- Misafirden Üyeye Geçiş: Kaç misafir sonradan kaydoluyor?
- Uygulama Silme Oranı (7 gün): Sert duvar ilk hafta içinde silmeyi artırmamalı.
- 7. Gün Elde Tutma: Hangi model kalıcılığı artırıyor?

**Yapılmaması gerekenler**
- Misafir modunda kritik veriyi kaybettirecek bir akış kurmayın.
- Sosyal giriş seçeneklerini gizlemeyin; kayıt sürtünmesini artırır.
- “Misafir olarak devam et” bağlantısını fark edilmez yapmayın.
- Aynı testte hem duvarı hem misafir modunun kapsamını değiştirmeyin.
- Misafir verisini kayıt sonrası birleştirmeden kaybetmeyin.

### EN

Requiring sign-up as soon as the app opens (a hard wall) can make users leave before they see any value. Letting them try first (a soft wall) can improve the first impression but may lower the sign-up rate.

**What to test**
- Timing: Should the sign-up screen appear at launch or after the first value?
- Guest mode: Does a limited feature set convince the user and lead them to sign up?
- Pre-wall loss: Does the share of users who see the sign-up screen and close the app without doing anything fall with a soft wall?
- Segment: Is the effect larger for new users or for returning ones?

**KPIs to track**
- Sign-up Rate: Does the total sign-up rate fall or rise?
- Activation Rate: Does the guest user complete the core action?
- Guest-to-Member Conversion: How many guests sign up later?
- App Uninstall Rate (7 days): A hard wall must not increase uninstalls in the first week.
- Day-7 Retention: Which model improves stickiness?

**What not to do**
- Don’t build a guest-mode flow that makes users lose critical data.
- Don’t hide the social login options; it adds sign-up friction.
- Don’t make the “Continue as guest” link easy to miss.
- Don’t change the wall and the scope of guest mode in the same test.
- Don’t lose guest data instead of merging it after sign-up.

---

## Push izni hangi anda istenmeli: açılışta mı, ilk değerden sonra mı?

Değişken: Push izninin istendiği an · Fark: değiştir

Etiket: id=ma-003 · mercek=Zamanlama · düzey=onboarding · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: When should push permission be requested: at launch or after the first value?

EN-Variable: Moment push permission is requested

İzin isteğini açılışta göstermek çoğu kullanıcıdan “İzin Verme” yanıtı alır ve o izni bir daha kolay isteyemezsiniz. İlk değeri gördükten sonra sormak kabul oranını yükseltebilir. Bu testte değişen tek şey iznin istendiği andır; akışın geri kalanı iki kolda aynıdır. “İzin istemeden önce nedenini anlatan bir ekran göstermek işe yarar mı?” senaryosundan farkı: orada zamanlama sabit tutulup sistem penceresinden önce açıklama ekranı eklenip eklenmemesi test edilir, burada ise ekran yapısı sabit, yalnızca iznin istendiği an değişir.

**Test edilmesi gerekenler**
- Zamanlama: Açılışta mı, ilk değerden sonra mı kabul oranı daha yüksek?
- Tetikleyici olay: İzni ilk siparişten sonra mı, ilk içerik kaydından sonra mı istemek daha çok izin getiriyor?
- Sonraki test: Kazanan an sabitken izin isteğine somut bir fayda cümlesi (“Antrenman hatırlatması”) eklemek ayrı bir testte kabulü artırıyor mu?
- İzin kalitesi: İlk değerden sonra izin veren kullanıcı, bildirimleri açılışta izin verenden daha uzun süre açık tutuyor mu?
- Platform: iOS ve Android’de kabul oranı farklı mı?

**Takip edilecek ana KPI’lar**
- Net Bildirim İzni Oranı: İzin veren / tüm yeni kullanıcı; iznin istendiği an bu oranı artırıyor mu?
- 7. Gün Elde Tutma: Bildirim alan kullanıcı daha çok mu geri dönüyor?
- Bildirim Tıklama Oranı: Gönderilen bildirimler açılıyor mu?
- İlk Oturum Tamamlama Oranı: İzin isteği akışı kesmemeli.
- Bildirim Kapatma Oranı: Sonradan kapatma artmamalı.

**Yapılmaması gerekenler**
- Sistem izni açılır açılmaz, hiçbir bağlam vermeden sormayın.
- Sistem iznini reddedene pencereyi tekrar göstermeye çalışmayın; iOS pencereyi zaten yalnızca bir kez gösterir, ikinci şans ancak cihaz ayarlarından açılır.
- Ön ekranın metnini gerçek dışı vaatlerle şişirmeyin.
- Aynı testte hem zamanlamayı hem ön açıklama ekranının metnini değiştirmeyin; sistem penceresinin kendi metni zaten değiştirilemez.
- İzin vermeyen kullanıcıyı uygulamadan mahrum bırakmayın.

> **Güncellik notu (2026-11):** Android 13’ten bu yana bildirim izni iOS’taki gibi kullanım sırasında sistem penceresiyle istenir; eski Android sürümlerinde izin varsayılan olarak açıktı. Bu yüzden iki platformun ve eski ile yeni Android sürümlerinin sonucu aynı izin akışını ölçmeyebilir: platform ve işletim sistemi sürümü ayrı okunur. iOS’ta kullanıcıya sormadan sessiz teslimata izin veren geçici izin de mümkündür; bu ayrı bir değişkendir ve iki kolda aynı kalır.

### EN

Showing the permission request at launch gets a “Don’t Allow” from most users, and you can’t easily ask for that permission again. Asking after they have seen the first value can raise the acceptance rate. In this test the only thing that changes is the moment the permission is requested; the rest of the flow is identical in both arms. How it differs from the “Does a screen that explains why, shown before a permission request, pay off?” scenario: there, timing is held fixed and the test is whether an explanation screen is added before the system dialog; here the screen structure is fixed and only the moment of the request changes.

**What to test**
- Timing: Is acceptance higher at launch or after the first value?
- Trigger event: Does asking for the permission after the first order or after the first content save bring more opt-ins?
- Next test: With the winning moment fixed, does adding a concrete benefit sentence (“Workout reminders”) to the permission request raise acceptance in a separate test?
- Permission quality: Do users who grant permission after the first value keep notifications on longer than those who grant at launch?
- Platform: Is the acceptance rate different on iOS and Android?

**KPIs to track**
- Net Push Opt-in Rate: Users who grant permission / all new users; does the moment of the request raise this rate?
- Day-7 Retention: Do users who receive notifications come back more?
- Push Click-Through Rate: Are the notifications sent opened?
- First Session Completion Rate: The permission request must not interrupt the flow.
- Push Opt-out Rate: Later switch-offs must not increase.

**What not to do**
- Don’t ask for the system permission the moment the app opens, with no context.
- Don’t try to show the dialog again to someone who denied the system permission; iOS shows the dialog only once, and a second chance exists only through device settings.
- Don’t inflate the pre-screen text with false promises.
- Don’t change the timing and the pre-explanation screen text in the same test; the system dialog’s own text can’t be changed anyway.
- Don’t shut users who don’t grant permission out of the app.

> **Freshness note (2026-11):** Since Android 13, notification permission is requested with a system dialog during use, as on iOS; on older Android versions the permission was on by default. So the results of the two platforms, and of older and newer Android versions, may not measure the same permission flow: platform and OS version are read separately. On iOS, provisional permission that allows quiet delivery without asking the user is also possible; that is a separate variable and stays the same in both arms.

---

## Yükleme ekranı mesajı satışı etkiler mi?

Değişken: Yükleme ekranındaki kampanya mesajı · Fark: ekle

Etiket: id=ma-004 · mercek=Fiyat · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a message on the loading screen affect sales?

EN-Variable: Campaign message on the loading screen

Yükleme ekranları çoğunlukla boş geçer. Bu anlarda kampanya veya avantaj bilgisi göstermek dikkati çekebilir ve bekleme algısını yumuşatabilir.

**Test edilmesi gerekenler**
- Kampanya: Yükleme ekranında kampanya göstermek isteği artırıyor mu?
- Sabır: Mesaj uzun beklemede terk oranını düşürüyor mu?
- Sonraki test: Mesaj kazanırsa, mesajın içeriği (indirim oranı / ücretsiz kargo) ayrı bir testte devam oranını değiştiriyor mu?
- Platform: iOS ve Android’de yükleme süresi farklıyken mesajın etkisi aynı mı?
- Süre: Kısa yüklemede mesaj algılanıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Kampanya mesajı geliri artırıyor mu?
- Dönüşüm Oranı (CR): Kampanya mesajı satın almayı artırıyor mu?
- Kampanya Etkileşimi: Kampanyalı ürünlere trafik artıyor mu?
- Yükleme Ekranında Terk Oranı: Yükleme bitmeden uygulamadan çıkanların payı artmamalı.
- Sayfa Geçiş Hızı: Kullanıcı yüklemeden sonra daha hızlı mı ilerliyor?

**Yapılmaması gerekenler**
- Yükleme ekranında uzun metin kullanmayın; okunmaz.
- Ağır görsel koymayın; yükleme süresini uzatır.
- Gerçekte olmayan veya süresi bitmiş bir indirimi (“%70’e varan”) yükleme ekranında göstermeyin; gerçek olmayan indirim/teklif göstermeyin.
- Aynı testte indirim, tasarım ve metni birlikte değiştirmeyin.
- Kampanya görseli yükleme animasyonunu gizlemesin.

### EN

Loading screens usually go to waste. Showing a campaign or benefit message in these moments can catch attention and soften the perception of waiting.

**What to test**
- Campaign: Does showing a campaign on the loading screen raise purchase intent?
- Patience: Does the message lower the abandonment rate during long waits?
- Next test: If the message wins, does its content (discount rate / free shipping) change the continue rate in a separate test?
- Platform: When load time differs on iOS and Android, is the message’s effect the same?
- Duration: Is the message noticed on a short load?

**KPIs to track**
- Revenue per Visitor (RPV): Does the campaign message raise revenue?
- Conversion Rate (CR): Does the campaign message raise purchases?
- Campaign Engagement: Does traffic to campaign products increase?
- Loading-Screen Abandonment Rate: The share of users who leave the app before loading finishes must not increase.
- Page Transition Speed: Does the user move faster after loading?

**What not to do**
- Don’t use long text on the loading screen; it won’t be read.
- Don’t add a heavy image; it lengthens the load time.
- Don’t show an expired or nonexistent discount (“up to 70%”) on the loading screen; don’t show a discount or offer that isn’t real.
- Don’t change the discount, the design and the text together in the same test.
- Don’t let the campaign visual hide the loading animation.

---

## İlk kullanımda arayüz ipuçları göstermek işe yarar mı?

Değişken: İlk kullanım arayüz ipuçları · Fark: ekle

Etiket: id=ma-005 · mercek=Netlik · düzey=onboarding · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does showing interface tips on first use pay off?

EN-Variable: First-use interface tips

Uygulamanın üstüne yerleşen kısa baloncuklar, bulunması zor işlevleri ilk kullanımda tanıtır. Riski: kullanıcı henüz ne aradığını bilmeden gösterilen ipucu ezberlenmez, akışı keser ve atlanır; ayrıca ipuçları ilk deneyimi bir eğitim seansına çevirip kullanıcıyı ürünle temas etmeden yorabilir.

**Test edilmesi gerekenler**
- Varlık: İlk kullanım ipuçları özellik kullanımını artırıyor mu?
- Sayı: Kaç ipucu gösterildiğinde atlama başlıyor?
- Sonraki test: İpuçları kazanırsa, gösterim anı (ilk açılış / ilgili ekrana ilk geliş) ayrı bir testte özellik kullanımını değiştiriyor mu?
- Kalıcı etki: İpucunu gören kullanıcı tanıtılan işlevi sonraki oturumlarda da kullanıyor mu, yoksa etki ilk günde mi sönüyor?
- Segment: Yeni kullanıcı ile güncelleme sonrası dönen kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Özellik Deneme Oranı: Teste atanan yeni kullanıcılar içinde ipucunun tanıttığı işlevi kullananların oranı artıyor mu?
- İlk Oturum Tamamlama Oranı: Kullanıcı ilk değerli eyleme ulaşıyor mu?
- İpucu Atlama Oranı: İpuçlarını atlayan kullanıcı oranı ne kadar?
- 7. Gün Elde Tutma: Elde tutma düşmemeli.
- İlk Oturum Terk Oranı: Eğitim yükü çıkışı artırmamalı.

**Yapılmaması gerekenler**
- İpuçlarını atlanamaz hâle getirmeyin.
- Aynı testte ipucu sayısı ile ipucu metinlerini birlikte değiştirmeyin.
- Kullanıcıyı ürünle hiç temas etmeden art arda beş ipucundan geçirmeyin.
- İpucu katmanını ekran okuyucu ile gezilemez bırakmayın.
- İpucunu, tanıttığı işlevin ekranda görünmediği bir anda göstermeyin; baloncuk işaret ettiği öğenin yanında durmalı.

### EN

Short bubbles placed over the app introduce hard-to-find functions on first use. The risk: a tip shown before the user knows what they are looking for isn’t remembered, interrupts the flow and gets skipped; tips can also turn the first experience into a training session and tire the user before they touch the product.

**What to test**
- Presence: Do first-use tips raise feature usage?
- Count: At how many tips does skipping begin?
- Next test: If the tips win, does the moment they are shown (first launch / first arrival at the relevant screen) change feature usage in a separate test?
- Lasting effect: Does a user who saw the tip keep using the introduced function in later sessions, or does the effect fade on day one?
- Segment: Do new users and users returning after an update react differently?

**KPIs to track**
- Feature Trial Rate: Among new users assigned to the test, does the share who use the function the tip introduces rise?
- First Session Completion Rate: Does the user reach the first valuable action?
- Tip Skip Rate: What share of users skip the tips?
- Day-7 Retention: Retention must not drop.
- First-Session Abandonment Rate: The training load must not increase exits.

**What not to do**
- Don’t make the tips impossible to skip.
- Don’t change the number of tips and the tip texts together in the same test.
- Don’t walk the user through five tips in a row without any contact with the product.
- Don’t leave the tip layer unusable with a screen reader.
- Don’t show a tip at a moment when the function it introduces isn’t visible on screen; the bubble should sit next to the element it points to.

---

## İzin istemeden önce nedenini anlatan bir ekran göstermek işe yarar mı?

Değişken: İzin öncesi açıklama ekranı · Fark: ekle

Etiket: id=ma-006 · mercek=Güven · düzey=onboarding · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a screen that explains why, shown before a permission request, pay off?

EN-Variable: Explanation screen before the permission request

Sistem izin penceresi tek seferliktir ve reddedildiğinde geri dönmek zordur. Öncesinde neden gerektiğini anlatan bir ekran göstermek, izni yalnızca ikna olan kullanıcıya sordurur ve sistem penceresini boşa harcamamayı sağlar. Karşı tarafta: fazladan bir adım eklenir ve bazı kullanıcı bu ekranda da düşer. “Push izni hangi anda istenmeli: açılışta mı, ilk değerden sonra mı?” senaryosundan farkı: orada yalnızca iznin istendiği an değişir, burada an sabit tutulup sistem penceresinden önce açıklama ekranının varlığı test edilir.

**Test edilmesi gerekenler**
- Hazırlık ekranı: Ön açıklama izin kabul oranını artırıyor mu?
- Sonraki test: Ekran kazanırsa, anlatım türü (fayda / izin sonrası ne olacağı) ayrı bir testte izin kabulünü değiştiriyor mu?
- Kayıp: Hazırlık ekranında düşen kullanıcı oranı ne kadar?
- Filtre etkisi: Hazırlık ekranı, sistem penceresini ikna olmuş kullanıcıya ulaştırarak kalıcı reddi azaltıyor mu?
- Segment: Yeni kullanıcı ile deneyimli kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Net Bildirim İzni Oranı: İzin veren / tüm yeni kullanıcı; hazırlık ekranı bu oranı artırıyor mu?
- Sistem Penceresi Kabul Oranı: Pencereye ulaşanların kabulü artıyor mu?
- Hazırlık Ekranı Geçiş Oranı: Bu adımdaki kayıp kabul edilemez seviyeye çıkmamalı.
- Kalıcı Reddetme Oranı: Geri dönülemez reddetme azalıyor mu?
- 7. Gün Elde Tutma: Elde tutma düşmemeli.

**Yapılmaması gerekenler**
- Hazırlık ekranını sistem penceresine benzetip kullanıcıyı yanıltmayın.
- İzin vermeden devam etmeyi engelleyen bir akış kurmayın.
- Aynı testte hazırlık ekranı ile iznin istendiği anı birlikte değiştirmeyin.
- Sistem penceresinin kabulünü tek başına başarı sayıp toplam kabule bakmamazlık etmeyin.
- İzin metinlerinin düzenlendiği platformlarda mağaza kurallarını doğrulamadan varyant yayınlamayın.

### EN

The system permission dialog is one-time, and it is hard to come back from once it is denied. Showing a screen first that explains why it is needed means the permission is requested only from users who are convinced, and the system dialog is not wasted. On the other side: an extra step is added, and some users drop at this screen too. How it differs from the “When should push permission be requested: at launch or after the first value?” scenario: there only the moment of the request changes; here the moment is held fixed and the test is whether an explanation screen exists before the system dialog.

**What to test**
- Priming screen: Does a pre-explanation raise the permission acceptance rate?
- Next test: If the screen wins, does the type of explanation (benefit / what happens after granting) change permission acceptance in a separate test?
- Loss: What share of users drop at the priming screen?
- Filter effect: Does the priming screen reduce permanent denials by getting the system dialog to users who are already convinced?
- Segment: Do new users and experienced users react differently?

**KPIs to track**
- Net Push Opt-in Rate: Users who grant permission / all new users; does the priming screen raise this rate?
- System Dialog Acceptance Rate: Does acceptance among those who reach the dialog rise?
- Priming Screen Pass-Through Rate: The loss at this step must not reach an unacceptable level.
- Permanent Denial Rate: Do irreversible denials fall?
- Day-7 Retention: Retention must not drop.

**What not to do**
- Don’t make the priming screen look like the system dialog and mislead the user.
- Don’t build a flow that blocks continuing without granting permission.
- Don’t change the priming screen and the moment of the request in the same test.
- Don’t count acceptance of the system dialog alone as success and fail to look at total acceptance.
- Don’t publish a variant without verifying store rules on platforms where permission texts are regulated.

---

## Sonraki adımı kullanıcının durumuna göre önermek işe yarar mı?

Değişken: Sonraki adım önerisinin kişiselleştirilmesi · Fark: değiştir

Etiket: id=ma-007 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does suggesting the next step based on the user’s status pay off?

EN-Variable: Personalization of the next-step suggestion

Herkese aynı “sonraki adım” yerine kullanıcının nerede kaldığına göre öneri sunmak (profilini tamamla, ilk siparişini ver, uygulamayı indir) ilerlemeyi hızlandırabilir. Riski: durum tespiti yanlışsa alakasız bir öneri gösterilir, öneri mantığı bakım yükü yaratır ve kullanıcı kendi önceliğini seçme imkânını kaybeder.

**Test edilmesi gerekenler**
- Kişiselleştirme: Duruma göre öneri ilerlemeyi artırıyor mu?
- Doğruluk: Durum tespiti ne oranda isabetli?
- Yedek: Durumu belirlenemeyen kullanıcıya ne gösteriliyor?
- Sonraki test: Kişiselleştirme kazanırsa, tek öneri yerine birkaç seçenek sunmak ayrı bir testte ilerlemeyi artırıyor mu?
- Segment: Yeni kullanıcı ile aktif kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Aktivasyon Oranı (ilk değerli eylem): Teste atanan kullanıcıların ilk değerli eyleme (ör. ilk sipariş) ulaşma oranı artıyor mu?
- Önerilen Adımın Tamamlanma Oranı: Tanı metriği; öneri gerçekten yapılıyor mu?
- Alakasız Öneri Oranı: Yanlış öneri gösterimi kabul edilemez seviyeye çıkmamalı.
- 7. Gün Elde Tutma: Elde tutma artıyor mu?
- Uygulama Silme Oranı (30 gün): Öneri baskısı, 30 gün içinde uygulamayı silen kullanıcıyı artırmamalı.

**Yapılmaması gerekenler**
- Durum tespitini kullanıcının paylaşmadığı verilerden türetip bunu ima etmeyin.
- Yedek öneri tanımlamadan kişiselleştirme kurmayın.
- Aynı testte öneri mantığı ile önerinin sunum biçimini birlikte değiştirmeyin.
- Kullanıcının kendi seçtiği yolu öneriyle ezmeyin.
- Kullanıcının az önce tamamladığı veya bilerek atladığı adımı yeniden önermeyin.

### EN

Instead of the same “next step” for everyone, offering a suggestion based on where the user left off (complete your profile, place your first order, download the app) can speed up progress. The risk: if the status detection is wrong, an irrelevant suggestion is shown, the suggestion logic creates a maintenance load, and the user loses the ability to choose their own priority.

**What to test**
- Personalization: Does a status-based suggestion raise progress?
- Accuracy: How accurate is the status detection?
- Fallback: What is shown to a user whose status can’t be determined?
- Next test: If personalization wins, does offering a few options instead of a single suggestion raise progress in a separate test?
- Segment: Do new users and active users react differently?

**KPIs to track**
- Activation Rate (first valuable action): Does the share of users assigned to the test who reach the first valuable action (for example the first order) rise?
- Suggested Step Completion Rate: Diagnostic metric; is the suggestion actually acted on?
- Irrelevant Suggestion Rate: Showing wrong suggestions must not reach an unacceptable level.
- Day-7 Retention: Does retention rise?
- App Uninstall Rate (30 days): Suggestion pressure must not increase the number of users who uninstall within 30 days.

**What not to do**
- Don’t derive status from data the user hasn’t shared and imply that you did.
- Don’t build personalization without defining a fallback suggestion.
- Don’t change the suggestion logic and the way the suggestion is presented together in the same test.
- Don’t override the path the user chose themselves with a suggestion.
- Don’t re-suggest a step the user just completed or deliberately skipped.

---

## Profil tamamlama yüzdesi göstermek eksik alanları doldurtuyor mu?

Değişken: Profil tamamlama göstergesi · Fark: ekle

Etiket: id=ma-008 · mercek=Netlik · düzey=onboarding · sektör=genel · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does showing a profile completion percentage get missing fields filled in?

EN-Variable: Profile completion indicator

Görünürde biten ama tam dolu olmayan bir gösterge (“Profiliniz %70 tamamlandı”) bitmemiş bir işi akılda tutar ve kapatma isteği yaratır; bu, ilk kayıt formunun kendisindeki adım-adım ilerleme çubuğundan (bkz. `cart-checkout.md`) farklı bir mekanizmadır: orada amaç akışta nerede olunduğunu göstermek, burada amaç kayıttan sonra kalan, isteğe bağlı alanlara geri döndürmektir.

**Test edilmesi gerekenler**
- Sonraki test: Gösterge kazanırsa, gösterim biçimi (yüzde / “3 alan kaldı”) ayrı bir testte tamamlamayı değiştiriyor mu?
- Eşik: Tamamlanma oranı belirli bir yüzdenin (ör. %80) üzerine çıkınca “bitirmeye yakın” hissi motivasyonu artırıyor mu?
- Hassas alanlar: Gösterge isteğe bağlı hassas alanlarda da doldurmayı artırıyor mu, yoksa kullanıcı bu alanlarda mı takılıyor?
- Zamanlama: Gösterge ilk oturumda mı, ikinci ziyarette mi daha güçlü çalışıyor?
- Cihaz: Küçük ekranda gösterge ilk bakışta fark ediliyor mu, yoksa mobil kullanıcıda etkisi kayboluyor mu?

**Takip edilecek ana KPI’lar**
- Profil Tamamlama Oranı: Eksik alanları dolduran kullanıcı oranı artıyor mu?
- Tekrar Ziyaret Oranı: Gösterge kullanıcıyı tekrar uygulamaya döndürüyor mu?
- Doldurulan Alan Sayısı (atanan kullanıcı başına ortalama): Bir oturumda tamamlanan alan sayısı artıyor mu?
- Gösterge Kapatma Oranı: Gösterge rahatsız edici bulunup kapatılmamalı.
- Oturum Süresi: Atanan kullanıcıların genel kullanım süresi düşmemeli.

**Yapılmaması gerekenler**
- Kullanıcının doldurmadığı hassas bir alanı yalnızca yüzdeyi yükseltmek için zorunlu göstermeyin; opsiyonel kalmalı.
- Yüzdeyi gerçek doluluktan farklı hesaplayıp yapay biçimde yüksek göstermeyin.
- Aynı testte gösterge biçimi ile hangi alanların “profilde” sayıldığını birlikte değiştirmeyin.
- Göstergeyi kapatılamaz veya ertelenemez hâle getirmeyin; kullanıcı “sonra” diyebilmeli.
- Tamamlama hatırlatmasını e-posta veya push bildirimiyle günde birden fazla tekrarlamayın; sıklık ayrı bir test konusudur.

### EN

An indicator that looks nearly done but not full (“Your profile is 70% complete”) keeps an unfinished task in mind and creates the urge to close it. This is a different mechanism from the step-by-step progress bar in the first sign-up form itself (see `cart-checkout.md`): there the aim is to show where the user is in the flow; here the aim is to bring users back to the optional fields left after sign-up.

**What to test**
- Next test: If the indicator wins, does its display format (percentage / “3 fields left”) change completion in a separate test?
- Threshold: Once the completion rate passes a certain percentage (for example 80%), does the “almost done” feeling raise motivation?
- Sensitive fields: Does the indicator raise filling on optional sensitive fields too, or do users get stuck on those fields?
- Timing: Does the indicator work better in the first session or on the second visit?
- Device: On a small screen, is the indicator noticed at first glance, or does its effect vanish for mobile users?

**KPIs to track**
- Profile Completion Rate: Does the share of users who fill the missing fields rise?
- Return Visit Rate: Does the indicator bring users back to the app?
- Fields Filled (average per assigned user): Does the number of fields completed in a session rise?
- Indicator Dismissal Rate: The indicator must not be found annoying and dismissed.
- Session Duration: Assigned users’ overall usage time must not drop.

**What not to do**
- Don’t present a sensitive field the user hasn’t filled as required just to raise the percentage; it must stay optional.
- Don’t calculate the percentage differently from the real fill level and show it artificially high.
- Don’t change the indicator format and which fields count as part of the “profile” together in the same test.
- Don’t make the indicator impossible to dismiss or snooze; the user must be able to say “later.”
- Don’t repeat the completion reminder by email or push notification more than once a day; frequency is a separate test subject.
