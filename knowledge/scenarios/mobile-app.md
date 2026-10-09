# Mobil Uygulama

Yolculuk aşaması: uygulamaya özgü akışlar (onboarding, izinler, anasayfa düzeni) ve uygulamaya bitişik mobil web anları (indirme banner’ı, web→uygulama geçişi; bu ikisinde web metrikleri kullanılır). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Servis ikonlarını büyütmek davranışı değiştirir mi?

Değişken: Öncelikli servis ikonunun boyutu · Fark: değiştir

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
- Diğer Servis Tıklaması: Gölgelenen servisler düşmemeli.
- Navigasyon Verimliliği: Hedef sayfaya daha az adımda ulaşılıyor mu?

**Yapılmaması gerekenler**
- Aynı anda çok fazla servisi farklılaştırmayın; ikiyi geçmeyin.
- Büyük ikonun diğer kategorilerin erişimini gölgelemesine izin vermeyin.
- İkonu banner hissi verecek kadar büyütmeyin.
- Aynı testte ikonu büyütürken rengini veya konumunu da değiştirmeyin.
- Sadece tıklamaya bakıp servisin tamamlama oranını atlamayın.

---

## Kayıt duvarı sert mi, yumuşak mı olmalı?

Değişken: Kayıt duvarının sertliği · Fark: değiştir

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
- Uygulama Silme Oranı: Sert duvar ilk gün silmeyi artırmamalı.
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

---

## Yükleme ekranı mesajı satışı etkiler mi?

Değişken: Yükleme ekranındaki kampanya mesajı · Fark: ekle

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
- Terk Oranı: Bekleme sırasında çıkış artmamalı.
- Sayfa Geçiş Hızı: Kullanıcı yüklemeden sonra daha hızlı mı ilerliyor?

**Yapılmaması gerekenler**
- Yükleme ekranında uzun metin kullanmayın; okunmaz.
- Ağır görsel koymayın; yükleme süresini uzatır.
- Gerçekte olmayan veya süresi bitmiş bir indirimi (“%70’e varan”) yükleme ekranında göstermeyin; gerçek olmayan indirim/teklif göstermeyin (kural 6).
- Aynı testte indirim, tasarım ve metni birlikte değiştirmeyin.
- Kampanya görseli yükleme animasyonunu gizlemesin.

---

## Yeni ve dönen kullanıcıya farklı anasayfa göstermek işe yarar mı?

Değişken: Kullanıcı tipine göre anasayfa ayrımı · Fark: değiştir

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

---

## Son gezilen ürünler şeridi geri dönüşü artırır mı?

Değişken: Son gezilen ürünler şeridi · Fark: ekle

Kullanıcının kendi gezinme geçmişi, algoritmik öneriden daha alakalıdır ve hatırlatma maliyeti sıfırdır. Ancak satın alınmış ürünü tekrar göstermek deneyimi bozar.

**Test edilmesi gerekenler**
- Sonraki test: Şerit kazanırsa, şeridin anasayfadaki yeri (ilk ekran / çok satanların altı) ayrı bir testte tıklamayı değiştiriyor mu?
- Sayı: Kaç ürün göstermek optimum? (3 / 6 / 10)
- Varlık: Son gezilen ürünler şeridi, dönen kullanıcının satın almasını artırıyor mu?
- Yamyamlık: Şerit çok satanlar bloğunun performansını yiyor mu?
- Platform: iOS ve Android’de şeridin etkisi aynı mı?

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

---

## Çıkış niyetine bağlı pop-up kaçan mobil kullanıcıyı kurtarır mı?

Değişken: Çıkış niyetine bağlı pop-up · Fark: ekle

Zamana bağlı pop-up herkesi keser; çıkış niyetine bağlı pop-up sadece zaten gitmekte olan kullanıcıyı yakalar. Teorik olarak maliyeti düşüktür ama mobilde çıkış niyeti sinyali güvenilir değildir. “Pop-up ne zaman gösterilmeli?” senaryosundan (`category-listing.md`) farkı: orada pop-up herkese gösterilir ve değişken gösterim anıdır, burada tetik yalnızca ayrılma sinyalidir ve hedef sadece gitmekte olan kullanıcıdır.

**Test edilmesi gerekenler**
- Varlık: Çıkış niyetinde gösterilen pop-up, gösterilmeyen kola göre oturuma devam eden kullanıcıyı artırıyor mu?
- Mobil sinyal: Seçilen ayrılma hareketini yapan kullanıcıların kaçı, pop-up gösterilmeyen kolda gerçekten oturumu bitiriyor?
- Sonraki test: Pop-up kazanırsa, teklif türü (indirim / ücretsiz kargo / e-bülten) ayrı bir testte yanıt oranını değiştiriyor mu?
- Segment: Sepetinde ürün olan kullanıcı ile boş sepetle ayrılan kullanıcı aynı pop-up’a farklı mı tepki veriyor?
- Sıklık: Kaç günde bir tekrar gösterilmeli?

**Takip edilecek ana KPI’lar**
- Oturum Devam Oranı: Çıkış niyeti sinyali iki kolda da loglanır (A’da pop-up çıkmaz); sinyal veren kullanıcılar içinde oturuma devam edenlerin oranı artıyor mu?
- Pop-up Yanıt Oranı: Teklifi kabul eden oranı.
- Dönüşüm Oranı (CR): Toplam satışa etkisi.
- Oturum Süresi: Düşmemeli.
- E-bülten Çıkış Oranı: Agresif toplama abonelikleri bozmamalı.

**Yapılmaması gerekenler**
- Mobilde güvenilmez sinyalle pop-up tetiklemeyin.
- Kapatma butonunu gizlemeyin veya küçültmeyin.
- Pop-up’taki indirim teklifini, sepette gerçekten uygulanmayan bir oran veya süreyle yazmayın (kural 6).
- Aynı oturumda birden fazla pop-up açmayın.
- Aynı testte hem tetikleyiciyi hem teklifi değiştirmeyin.

---

## Uygulama indirme banner’ı web dönüşümünü düşürüyor mu?

Değişken: Uygulama indirme banner’ı · Fark: ekle

Mobil webde uygulama banner’ı kurulum sayısını artırır ama devam eden oturumu böler. Bu test iki hedefin çakıştığı klasik bir örnektir; tek metrikle okunursa yanlış karar verilir.

**Test edilmesi gerekenler**
- Kazanç: Banner uygulama kurulumunu ne kadar artırıyor?
- Kayıp: Aynı oturumdaki web dönüşümü ne kadar düşüyor?
- Sonraki test: Banner kazanırsa, yerleşimi (üstte sabit / içerik arasında) ayrı bir testte kurulum ile web dönüşümü arasındaki dengeyi değiştiriyor mu?
- Segment: Sadece yeni ziyaretçiye göstermek dengeyi kuruyor mu?
- Kurulum sonrası: Banner’dan uygulamayı kuran kullanıcı, webde yarım kalan işlemini uygulamada tamamlıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İki kanalı birlikte okuyan metrik.
- Uygulama Kurulum Oranı: Banner’ın ana amacı.
- Web Dönüşüm Oranı (CR): Kayıp tarafı.
- Oturum Devam Oranı: Kullanıcı akıştan kopmamalı.
- 7. Gün Elde Tutma: Kurulum kalıcı mı?

**Yapılmaması gerekenler**
- Sadece kurulum sayısına bakıp web kaybını görmezden gelmeyin.
- Banner’ı kapatılamaz yapmayın.
- Ödeme akışının içinde göstermeyin.
- Her sayfada tekrar tekrar açmayın.
- Aynı testte teklif tutarını da değiştirmeyin.

---

## İlk kullanımda arayüz ipuçları göstermek işe yarar mı?

Değişken: İlk kullanım arayüz ipuçları · Fark: ekle

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
- Özellik kullanımı arttı diye elde tutmaya bakmadan kazandı demeyin.

---

## İzin istemeden önce nedenini anlatan bir ekran göstermek işe yarar mı?

Değişken: İzin öncesi açıklama ekranı · Fark: ekle

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

Herkese aynı “sonraki adım” yerine kullanıcının nerede kaldığına göre öneri sunmak (profilini tamamla, ilk siparişini ver, uygulamayı indir) ilerlemeyi hızlandırabilir. Riski: durum tespiti yanlışsa alakasız bir öneri gösterilir, öneri mantığı bakım yükü yaratır ve kullanıcı kendi önceliğini seçme imkânını kaybeder.

**Test edilmesi gerekenler**
- Kişiselleştirme: Duruma göre öneri ilerlemeyi artırıyor mu?
- Doğruluk: Durum tespiti ne oranda isabetli?
- Yedek: Durumu belirlenemeyen kullanıcıya ne gösteriliyor?
- Sonraki test: Kişiselleştirme kazanırsa, tek öneri yerine birkaç seçenek sunmak ayrı bir testte ilerlemeyi artırıyor mu?
- Segment: Yeni kullanıcı ile aktif kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- İlk Değerli Eyleme Ulaşma Oranı: Teste atanan kullanıcıların ilk değerli eyleme (ör. ilk sipariş) ulaşma oranı artıyor mu?
- Önerilen Adımın Tamamlanma Oranı: Tanı metriği; öneri gerçekten yapılıyor mu?
- Alakasız Öneri Oranı: Yanlış öneri gösterimi kabul edilemez seviyeye çıkmamalı.
- 7. Gün Elde Tutma: Elde tutma artıyor mu?
- Uygulama Terk Oranı: Öneri baskısı çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Durum tespitini kullanıcının paylaşmadığı verilerden türetip bunu ima etmeyin.
- Yedek öneri tanımlamadan kişiselleştirme kurmayın.
- Aynı testte öneri mantığı ile önerinin sunum biçimini birlikte değiştirmeyin.
- Kullanıcının kendi seçtiği yolu öneriyle ezmeyin.
- Öneri tamamlandı diye asıl değere ulaşmaya bakmadan kazandı demeyin.

---

## Profil tamamlama yüzdesi göstermek eksik alanları doldurtuyor mu?

Değişken: Profil tamamlama göstergesi · Fark: ekle

Görünürde biten ama tam dolu olmayan bir gösterge (“Profiliniz %70 tamamlandı”) bitmemiş bir işi akılda tutar ve kapatma isteği yaratır — bu, ilk kayıt formunun kendisindeki adım-adım ilerleme çubuğundan (bkz. `cart-checkout.md`) farklı bir mekanizmadır: orada amaç akışta nerede olunduğunu göstermek, burada amaç kayıttan sonra kalan, isteğe bağlı alanlara geri döndürmektir.

**Test edilmesi gerekenler**
- Sonraki test: Gösterge kazanırsa, gösterim biçimi (yüzde / “3 alan kaldı”) ayrı bir testte tamamlamayı değiştiriyor mu?
- Eşik: Tamamlanma oranı belirli bir yüzdenin (ör. %80) üzerine çıkınca “bitirmeye yakın” hissi motivasyonu artırıyor mu?
- Hassas alanlar: Gösterge isteğe bağlı hassas alanlarda da doldurmayı artırıyor mu, yoksa kullanıcı bu alanlarda mı takılıyor?
- Zamanlama: Gösterge ilk oturumda mı, ikinci ziyarette mi daha güçlü çalışıyor?
- Cihaz: Küçük ekranda gösterge ilk bakışta fark ediliyor mu, yoksa mobil kullanıcıda etkisi kayboluyor mu?

**Takip edilecek ana KPI’lar**
- Profil Tamamlama Oranı: Eksik alanları dolduran kullanıcı oranı artıyor mu?
- Tekrar Ziyaret Oranı: Gösterge kullanıcıyı tekrar uygulamaya döndürüyor mu?
- Doldurulan Ortalama Alan Sayısı: Bir oturumda tamamlanan alan sayısı artıyor mu?
- Gösterge Kapatma Oranı: Gösterge rahatsız edici bulunup kapatılmamalı.
- Oturum Süresi: Atanan kullanıcıların genel kullanım süresi düşmemeli.

**Yapılmaması gerekenler**
- Kullanıcının doldurmadığı hassas bir alanı (kural 14) yalnızca yüzdeyi yükseltmek için zorunlu göstermeyin; opsiyonel kalmalı.
- Yüzdeyi gerçek doluluktan farklı hesaplayıp yapay biçimde yüksek göstermeyin.
- Aynı testte gösterge biçimi ile hangi alanların “profilde” sayıldığını birlikte değiştirmeyin.
- Göstergeyi kapatılamaz veya ertelenemez hâle getirmeyin; kullanıcı “sonra” diyebilmeli.
- Tamamlama hatırlatmasını e-posta veya push bildirimiyle günde birden fazla tekrarlamayın; sıklık ayrı bir test konusudur.
