# Mobil Uygulama

Yolculuk aşaması: yüklü uygulamanın içindeki akışlar (onboarding, izinler, uygulama anasayfasının düzeni). Mobil web anları (uygulama indirme banner’ı, çıkış niyeti pop-up’ı, son gezilen ürünler şeridi, yeni ve dönen ziyaretçiye ayrı anasayfa) web dosyalarındadır: `home-landing.md` ve `category-listing.md`. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Servis ikonlarını büyütmek davranışı değiştirir mi?

Değişken: Öncelikli servis ikonunun boyutu · Fark: değiştir

Etiket: id=ma-001 · mercek=Netlik · düzey=görsel · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does enlarging service icons change behavior?

Tüm servisleri eşit boyutta göstermek nötr bir deneyim yaratır. Öncelikli servisleri büyütmek o servislere yönelmeyi artırabilir ama diğerlerini gölgeleyebilir.

**Test edilmesi gerekenler**
- Vurgu: Öncelikli servisin ikonunu büyütmek tıklamayı artırıyor mu?
- Segment: Öncelikli servisi daha önce kullanmış kullanıcı ile hiç kullanmamış kullanıcı büyük ikona farklı mı tepki veriyor?
- Yan etki: Diğer servislerin tıklanması azalıyor mu?
- Sonraki test: Büyütme kazanırsa, büyük ikonun yeri (ilk sıra / sol bölge) ayrı bir testte tıklamayı değiştiriyor mu?
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

---

## Kayıt duvarı sert mi, yumuşak mı olmalı?

Değişken: Kayıt duvarının sertliği · Fark: değiştir

Etiket: id=ma-002 · mercek=Zamanlama · düzey=akış · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Should the sign-up wall be hard or soft?

Uygulamayı açar açmaz üye olmayı zorunlu tutmak (sert duvar), kullanıcının değeri görmeden ayrılmasına yol açabilir. Önce denemesine izin vermek (yumuşak duvar) ilk izlenimi artırabilir ama kayıt oranını düşürebilir.

**Test edilmesi gerekenler**
- Zamanlama: Kayıt ekranı açılışta mı, ilk değerden sonra mı gösterilmeli?
- Misafir modu: Sınırlı özellik seti kullanıcıyı ikna edip kaydolmaya yönlendiriyor mu?
- Sonraki test: Kazanan duvar sabitken mevcut bir hesapla giriş seçeneği ayrı bir testte kaydı hızlandırıyor mu?
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

---

## Push izni hangi anda istenmeli: açılışta mı, ilk değerden sonra mı?

Değişken: Push izninin istendiği an · Fark: değiştir

Etiket: id=ma-003 · mercek=Zamanlama · düzey=onboarding · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: When should push permission be requested: at launch or after the first value?

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

---

## Yükleme ekranı mesajı satışı etkiler mi?

Değişken: Yükleme ekranındaki kampanya mesajı · Fark: ekle

Etiket: id=ma-004 · mercek=Fiyat · düzey=bilgi · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does a message on the loading screen affect sales?

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
- Gerçekte olmayan veya süresi bitmiş bir indirimi (“%70’e varan”) yükleme ekranında göstermeyin; gerçek olmayan indirim/teklif göstermeyin (kural 6).
- Aynı testte indirim, tasarım ve metni birlikte değiştirmeyin.
- Kampanya görseli yükleme animasyonunu gizlemesin.

---

## İlk kullanımda arayüz ipuçları göstermek işe yarar mı?

Değişken: İlk kullanım arayüz ipuçları · Fark: ekle

Etiket: id=ma-005 · mercek=Netlik · düzey=onboarding · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing interface tips on first use pay off?

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

---

## İzin istemeden önce nedenini anlatan bir ekran göstermek işe yarar mı?

Değişken: İzin öncesi açıklama ekranı · Fark: ekle

Etiket: id=ma-006 · mercek=Güven · düzey=onboarding · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does a screen that explains why, shown before a permission request, pay off?

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
- İzin vermeden devam etmeyi engelleyen bir akış kurmayın (kural 6).
- Aynı testte hazırlık ekranı ile iznin istendiği anı birlikte değiştirmeyin.
- Sistem penceresinin kabulünü tek başına başarı sayıp toplam kabule bakmamazlık etmeyin.
- İzin metinlerinin düzenlendiği platformlarda mağaza kurallarını doğrulamadan varyant yayınlamayın.

---

## Sonraki adımı kullanıcının durumuna göre önermek işe yarar mı?

Değişken: Sonraki adım önerisinin kişiselleştirilmesi · Fark: değiştir

Etiket: id=ma-007 · mercek=Uygunluk · düzey=kişiselleştirme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does suggesting the next step based on the user’s status pay off?

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

---

## Profil tamamlama yüzdesi göstermek eksik alanları doldurtuyor mu?

Değişken: Profil tamamlama göstergesi · Fark: ekle

Etiket: id=ma-008 · mercek=Netlik · düzey=onboarding · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing a profile completion percentage get missing fields filled in?

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
- Kullanıcının doldurmadığı hassas bir alanı (kural 14) yalnızca yüzdeyi yükseltmek için zorunlu göstermeyin; opsiyonel kalmalı.
- Yüzdeyi gerçek doluluktan farklı hesaplayıp yapay biçimde yüksek göstermeyin.
- Aynı testte gösterge biçimi ile hangi alanların “profilde” sayıldığını birlikte değiştirmeyin.
- Göstergeyi kapatılamaz veya ertelenemez hâle getirmeyin; kullanıcı “sonra” diyebilmeli.
- Tamamlama hatırlatmasını e-posta veya push bildirimiyle günde birden fazla tekrarlamayın; sıklık ayrı bir test konusudur.
