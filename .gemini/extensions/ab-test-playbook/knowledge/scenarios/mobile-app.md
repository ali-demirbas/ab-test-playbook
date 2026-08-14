# Mobil Uygulama

Yolculuk aşaması: uygulamaya özgü akışlar (onboarding, izinler, anasayfa düzeni) ve uygulamaya bitişik mobil web anları (indirme banner’ı, web→uygulama geçişi; bu ikisinde web metrikleri kullanılır). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Servis ikonlarını büyütmek davranışı değiştirir mi?

Tüm servisleri eşit boyutta göstermek nötr bir deneyim yaratır. Öncelikli servisleri büyütmek o servislere yönelmeyi artırabilir ama diğerlerini gölgeleyebilir.

**Test edilmesi gerekenler**
- Vurgu: Öncelikli servisin ikonunu büyütmek tıklamayı artırıyor mu?
- Yönlendirme: Büyük ikon hedef kategoriye daha hızlı ulaştırıyor mu?
- Yan etki: Diğer servislerin tıklanması azalıyor mu?
- Konum: Mobilde ilk sıra mı, sol bölge mi daha etkili?
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
- Test sırasında rengi, konumu ve boyutu birlikte değiştirmeyin.
- Sadece tıklamaya bakıp servisin tamamlama oranını atlamayın.

---

## Kayıt duvarı sert mi, yumuşak mı olmalı?

Uygulamayı açar açmaz üye olmayı zorunlu tutmak (sert duvar), kullanıcının değeri görmeden ayrılmasına yol açabilir. Önce denemesine izin vermek (yumuşak duvar) ilk izlenimi artırabilir ama kayıt oranını düşürebilir.

**Test edilmesi gerekenler**
- Zamanlama: Kayıt ekranı açılışta mı, ilk değerden sonra mı gösterilmeli?
- Misafir modu: Sınırlı özellik seti kullanıcıyı ikna edip kaydolmaya yönlendiriyor mu?
- Sosyal giriş: Mevcut bir hesapla (sosyal veya platform hesabı) giriş kaydı hızlandırıyor mu?
- Konum: Misafir bağlantısı ana CTA’nın ne kadar yakınında olmalı?
- Segment: Yeni kullanıcıda mı, geri dönende mi etki daha büyük?

**Takip edilecek ana KPI’lar**
- Kayıt Oranı: Toplam üye olma oranı düşüyor mu, artıyor mu?
- Aktivasyon Oranı: Misafir kullanıcı temel aksiyonu tamamlıyor mu?
- Misafirden Üyeye Geçiş: Kaç misafir sonradan kaydoluyor?
- Uygulama Silme Oranı: Sert duvar ilk gün silmeyi artırmamalı.
- Yedi Gün Elde Tutma: Hangi model kalıcılığı artırıyor?

**Yapılmaması gerekenler**
- Misafir modunda kritik veriyi kaybettirecek bir akış kurmayın.
- Sosyal giriş seçeneklerini gizlemeyin; kayıt sürtünmesini artırır.
- “Misafir olarak devam et” bağlantısını fark edilmez yapmayın.
- Aynı testte hem duvarı hem misafir modunun kapsamını değiştirmeyin.
- Misafir verisini kayıt sonrası birleştirmeden kaybetmeyin.

---

## Push izni ne zaman istenmeli?

İzin isteğini açılışta göstermek çoğu kullanıcıdan “İzin Verme” yanıtı alır ve o izni bir daha kolay isteyemezsiniz. İlk değeri gördükten sonra sormak kabul oranını yükseltebilir.

**Test edilmesi gerekenler**
- Zamanlama: Açılışta mı, ilk değerden sonra mı kabul oranı daha yüksek?
- Ön ekran: Sistem izni öncesi açıklama ekranı kabulü artırıyor mu?
- Bağlam: “Antrenman hatırlatması” gibi somut fayda belirtmek etkiliyor mu?
- Tekrar sorma: Reddeden kullanıcıya uygulama içinden tekrar önerilmeli mi?
- Platform: iOS ve Android’de kabul oranı farklı mı?

**Takip edilecek ana KPI’lar**
- İzin Kabul Oranı: “İzin Ver” seçilme oranı.
- Yedi Gün Elde Tutma: Bildirim alan kullanıcı daha çok mu geri dönüyor?
- Bildirim Tıklama Oranı: Gönderilen bildirimler açılıyor mu?
- İlk Oturum Tamamlama: İzin isteği akışı kesmemeli.
- Bildirimi Kapatma Oranı: Sonradan kapatma artmamalı.

**Yapılmaması gerekenler**
- Sistem izni açılır açılmaz, hiçbir bağlam vermeden sormayın.
- Sistem iznini reddedene pencereyi tekrar göstermeye çalışmayın; iOS pencereyi zaten yalnızca bir kez gösterir, ikinci şans ancak cihaz ayarlarından açılır.
- Ön ekranın metnini gerçek dışı vaatlerle şişirmeyin.
- Aynı testte hem zamanlamayı hem ön açıklama ekranının metnini değiştirmeyin; sistem penceresinin kendi metni zaten değiştirilemez.
- İzin vermeyen kullanıcıyı uygulamadan mahrum bırakmayın.

---

## Yükleme ekranı mesajı satışı etkiler mi?

Yükleme ekranları çoğunlukla boş geçer. Bu anlarda kampanya veya avantaj bilgisi göstermek dikkati çekebilir ve bekleme algısını yumuşatabilir.

**Test edilmesi gerekenler**
- Kampanya: Yükleme ekranında kampanya göstermek isteği artırıyor mu?
- Sabır: Mesaj uzun beklemede terk oranını düşürüyor mu?
- Fayda: “%70’e varan indirim” devam oranını yükseltiyor mu?
- Keşif: Mesaj yeni kategori keşfine yönlendiriyor mu?
- Süre: Kısa yüklemede mesaj algılanıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Kampanya mesajı satın almayı artırıyor mu?
- Tıklama Oranı (CTR): Yükleme sonrası tıklama artıyor mu?
- Kampanya Etkileşimi: Kampanyalı ürünlere trafik artıyor mu?
- Terk Oranı: Bekleme sırasında çıkış artmamalı.
- Sayfa Geçiş Hızı: Kullanıcı yüklemeden sonra daha hızlı mı ilerliyor?

**Yapılmaması gerekenler**
- Yükleme ekranında uzun metin kullanmayın; okunmaz.
- Ağır görsel koymayın; yükleme süresini uzatır.
- Yanlış yönlendiren kampanya mesajı göstermeyin.
- Aynı testte indirim, tasarım ve metni birlikte değiştirmeyin.
- Kampanya görseli yükleme animasyonunu gizlemesin.

---

## Yeni ve dönen kullanıcıya farklı anasayfa göstermek işe yarar mı?

Yeni ziyaretçinin marka bilgisine, dönen ziyaretçinin ise hızlı devam yoluna ihtiyacı vardır. Aynı anasayfayı ikisine de göstermek her iki grubu da yarı yolda bırakabilir.

**Test edilmesi gerekenler**
- Devam bloğu: Dönen kullanıcıya “kaldığın yerden devam” göstermek dönüşümü artırıyor mu?
- Yeni kullanıcı: Marka vitrini mi, doğrudan ürün mü daha iyi?
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
- Segment tanımını test ortasında değiştirmeyin.
- Kişisel veriyi anasayfada açıkça göstermeyin (isim, adres).
- Yanlış segmentte varsayılan deneyimi bozmayın.
- Aynı testte hem segmenti hem içerik bloklarını değiştirmeyin.
- Kişiselleştirmeyi önbellek dışı bırakıp sayfayı yavaşlatmayın.

---

## Son gezilen ürünler şeridi geri dönüşü artırır mı?

Kullanıcının kendi gezinme geçmişi, algoritmik öneriden daha alakalıdır ve hatırlatma maliyeti sıfırdır. Ancak satın alınmış ürünü tekrar göstermek deneyimi bozar.

**Test edilmesi gerekenler**
- Konum: Şerit anasayfanın neresinde en çok tıklanıyor?
- Sayı: Kaç ürün göstermek optimum? (3 / 6 / 10)
- Filtre: Satın alınan ürünü çıkarmak memnuniyeti artırıyor mu?
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

## Çıkış niyeti pop-up’ı kaçan kullanıcıyı kurtarır mı?

Zamana bağlı pop-up herkesi keser; çıkış niyetine bağlı pop-up sadece zaten gitmekte olan kullanıcıyı yakalar. Teorik olarak maliyeti düşüktür ama mobilde çıkış niyeti sinyali güvenilir değildir.

**Test edilmesi gerekenler**
- Tetikleyici: Çıkış niyeti zamana bağlı pop-up’tan daha mı verimli?
- Mobil sinyal: Hangi hareket kullanılmalı? (hızlı yukarı scroll / geri tuşu)
- Teklif: İndirim, ücretsiz kargo veya e-bülten hangisi daha çok yanıt alıyor?
- Segment: Sepetinde ürün olana farklı teklif etkiyi artırıyor mu?
- Sıklık: Kaç günde bir tekrar gösterilmeli?

**Takip edilecek ana KPI’lar**
- Kurtarma Oranı: Pop-up görüp oturuma devam eden kullanıcı oranı.
- Pop-up Yanıt Oranı: Teklifi kabul eden oranı.
- Dönüşüm Oranı (CR): Toplam satışa etkisi.
- Oturum Süresi: Düşmemeli.
- E-bülten Çıkış Oranı: Agresif toplama abonelikleri bozmamalı.

**Yapılmaması gerekenler**
- Mobilde güvenilmez sinyalle pop-up tetiklemeyin.
- Kapatma butonunu gizlemeyin veya küçültmeyin.
- Ödeme akışında göstermeyin.
- Aynı oturumda birden fazla pop-up açmayın.
- Aynı testte hem tetikleyiciyi hem teklifi değiştirmeyin.

---

## Uygulama indirme banner’ı web dönüşümünü düşürüyor mu?

Mobil webde uygulama banner’ı kurulum sayısını artırır ama devam eden oturumu böler. Bu test iki hedefin çakıştığı klasik bir örnektir; tek metrikle okunursa yanlış karar verilir.

**Test edilmesi gerekenler**
- Kazanç: Banner uygulama kurulumunu ne kadar artırıyor?
- Kayıp: Aynı oturumdaki web dönüşümü ne kadar düşüyor?
- Konum: Üst sabit mi, araya giren mi daha dengeli?
- Segment: Sadece yeni ziyaretçiye göstermek dengeyi kuruyor mu?
- Teklif: Uygulamaya özel indirim etkiyi güçlendiriyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İki kanalı birlikte okuyan metrik.
- Uygulama Kurulum Oranı: Banner’ın ana amacı.
- Web Dönüşüm Oranı (CR): Kayıp tarafı.
- Oturum Devam Oranı: Kullanıcı akıştan kopmamalı.
- Uygulama 7 Gün Retention: Kurulum kalıcı mı?

**Yapılmaması gerekenler**
- Sadece kurulum sayısına bakıp web kaybını görmezden gelmeyin.
- Banner’ı kapatılamaz yapmayın.
- Ödeme akışının içinde göstermeyin.
- Her sayfada tekrar tekrar açmayın.
- Aynı testte teklif tutarını da değiştirmeyin.

---

## İlk kullanımda arayüz ipuçları göstermek işe yarar mı?

Uygulamanın üstüne yerleşen kısa baloncuklar, bulunması zor işlevleri ilk kullanımda tanıtır. Riski: kullanıcı henüz ne aradığını bilmeden gösterilen ipucu ezberlenmez, akışı keser ve atlanır; ayrıca ipuçları ilk deneyimi bir eğitim seansına çevirip kullanıcıyı ürünle temas etmeden yorabilir.

**Test edilmesi gerekenler**
- Varlık: İlk kullanım ipuçları özellik kullanımını artırıyor mu?
- Sayı: Kaç ipucu gösterildiğinde atlama başlıyor?
- Zamanlama: İpucu baştan mı, kullanıcı o ekrana geldiğinde mi gösterilmeli?
- Kalıcılık: İpuçları sonradan tekrar erişilebilir mi?
- Segment: Yeni kullanıcı ile güncelleme sonrası dönen kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Tanıtılan Özellik Kullanım Oranı: İpucunun gösterdiği işlevin kullanımı artıyor mu?
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

Sistem izin penceresi tek seferliktir ve reddedildiğinde geri dönmek zordur. Öncesinde neden gerektiğini anlatan bir ekran göstermek, izni yalnızca ikna olan kullanıcıya sordurur ve sistem penceresini boşa harcamamayı sağlar. Karşı tarafta: fazladan bir adım eklenir ve bazı kullanıcı bu ekranda da düşer.

**Test edilmesi gerekenler**
- Hazırlık ekranı: Ön açıklama izin kabul oranını artırıyor mu?
- İçerik: Faydayı anlatmak mı, ne olacağını anlatmak mı daha ikna edici?
- Kayıp: Hazırlık ekranında düşen kullanıcı oranı ne kadar?
- Erteleme: “Şimdi değil” seçeneği sunmak toplam kabulü büyütüyor mu?
- Segment: Yeni kullanıcı ile deneyimli kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Net İzin Kabul Oranı: Tüm kullanıcılar içindeki nihai kabul oranı artıyor mu?
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

Herkese aynı “sonraki adım” yerine kullanıcının nerede kaldığına göre öneri sunmak (profilini tamamla, ilk siparişini ver, uygulamayı indir) ilerlemeyi hızlandırabilir. Riski: durum tespiti yanlışsa alakasız bir öneri gösterilir, öneri mantığı bakım yükü yaratır ve kullanıcı kendi önceliğini seçme imkânını kaybeder.

**Test edilmesi gerekenler**
- Kişiselleştirme: Duruma göre öneri ilerlemeyi artırıyor mu?
- Doğruluk: Durum tespiti ne oranda isabetli?
- Yedek: Durumu belirlenemeyen kullanıcıya ne gösteriliyor?
- Seçim: Kullanıcıya birkaç seçenek sunmak tek öneriden iyi mi?
- Segment: Yeni kullanıcı ile aktif kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Önerilen Adımın Tamamlanma Oranı: Öneri gerçekten yapılıyor mu?
- İlk Değerli Eyleme Ulaşma Oranı: Kullanıcı asıl değere ulaşıyor mu?
- Alakasız Öneri Oranı: Yanlış öneri gösterimi kabul edilemez seviyeye çıkmamalı.
- 7. Gün Elde Tutma: Elde tutma artıyor mu?
- Uygulama Terk Oranı: Öneri baskısı çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Durum tespitini kullanıcının paylaşmadığı verilerden türetip bunu ima etmeyin.
- Yedek öneri tanımlamadan kişiselleştirme kurmayın.
- Aynı testte öneri mantığı ile önerinin sunum biçimini birlikte değiştirmeyin.
- Kullanıcının kendi seçtiği yolu öneriyle ezmeyin.
- Öneri tamamlandı diye asıl değere ulaşmaya bakmadan kazandı demeyin.
