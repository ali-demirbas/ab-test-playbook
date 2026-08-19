# Form ve kayıt akışı

Yolculuk aşaması: bir formun doldurulmaya başlanmasından gönderilmesine kadar geçen her şey. Alan sayısı, adım sayısı ve zorunlu/isteğe bağlı işaretlemesi bu dosyada değil, ilgili bağlam dosyalarındadır (checkout için `cart-checkout.md`, lead formu için `saas-b2b.md`); burada formun kendi tasarımı ve giriş/kayıt yöntemi ele alınır. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Etiketler alanın üstünde mi, solunda mı durmalı?

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

---

## Yüzen etiket doldurmayı kolaylaştırıyor mu?

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
- Alan Terk Oranı: Belirli bir alanda bırakma artıyor mu?
- Erişilebilirlik: Etiket kontrastı ve ekran okuyucu okuması bozulmamalı.

**Yapılmaması gerekenler**
- Etiketi tamamen placeholder’a çevirip kaldırmayın; bu ayrı ve daha riskli bir değişikliktir.
- Yüzen etiketi hem etiket hem yardım metni yerine kullanmayın.
- Animasyon süresini testin ortasında değiştirmeyin.
- Otomatik doldurma davranışını test aracıyla bastırmayın; gerçek kullanımda çalışan hâli ölçülmelidir.
- Hareket azaltma tercihini yok sayan bir geçiş animasyonu koymayın.

---

## Form alanlarını tek sütuna almak tamamlamayı artırır mı?

İki sütunlu form ekranda kısa görünür ama gözün zikzak çizmesini gerektirir ve bir sütunu tamamen atlama riski yaratır. Tek sütun daha uzun görünür, buna karşılık sıra belirsizliği ortadan kalkar. Birlikte anlam taşıyan alanlarda (il/ilçe, ad/soyad) yan yana dizilim savunulabilir.

**Test edilmesi gerekenler**
- Düzen: Tek sütun mu iki sütun mu daha yüksek tamamlama veriyor?
- Atlama: İki sütunda sağdaki alanlar daha sık boş mu kalıyor?
- İstisna: Ad/soyad gibi ilişkili alanlar yan yana kalırsa sonuç değişiyor mu?
- Algılanan uzunluk: Tek sütunun uzunluğu başlamayı caydırıyor mu?
- Cihaz: Masaüstündeki kazanç mobilde de geçerli mi?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Düzen gönderimi artırıyor mu?
- Boş Bırakılan Alan Sayısı: Atlanan alan sayısı artmamalı.
- Ortalama Doldurma Süresi: Tek sütun doldurmayı yavaşlatıyor mu?
- Form Başlama Oranı: Uzayan form ilk dokunuşu azaltıyor mu?
- Doğrulama Hatası Oranı: Gönderimde geri dönen hata sayısı artmamalı.

**Yapılmaması gerekenler**
- Aynı testte düzen ile alan sırasını birlikte değiştirmeyin.
- Mobilde zaten tek sütuna düşen bir formu iki sütunlu varyantla test etmeye çalışmayın; orada değişiklik yoktur.
- Sütun sayısını değiştirirken alan genişliğini de değiştirmeyin.
- İlişkili alanları bölerken sekme sırasını bozmayın.
- Sonucu farklı uzunluktaki formlara genellemeyin; üç alanlı formla on iki alanlı form aynı davranmaz.

---

## En kolay alanı başa koymak formu tamamlatır mı?

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
- Terk azaldı diye erken karar vermeyin; terkin sona kayıp kaymadığını alan bazında kontrol edin.
- Yasal olarak belirli bir sırada sunulması gereken alanları (onay metinleri) taşımayın.
- Sıralamayı kullanıcıya mantıksız gelecek şekilde bozmayın (şehirden önce mahalle sormak gibi).
- Tek bir form tipinde ölçüp sonucu tüm formlara kural diye yazmayın.

---

## Alanları baştan göstermek mi, kademeli açmak mı daha çok tamamlatıyor?

Tüm alanları baştan göstermek beklentiyi netleştirir ama form uzun görünür. Kademeli açma (bir alan doldurulunca sonrakinin belirmesi, ya da isteğe bağlı bir bölümün bir bağlantıyla açılması) algılanan uzunluğu düşürür. Riski: kullanıcı formun ne kadar süreceğini bilemez ve gizlenen alan sürpriz gibi gelir.

**Test edilmesi gerekenler**
- Görünürlük: Alanlar baştan mı görünmeli, doldurdukça mı açılmalı?
- İsteğe bağlı bölüm: Zorunlu olmayan alanları katlanmış bir bölümde sunmak tamamlamayı artırıyor mu?
- Beklenti: Kaç adım kaldığı belirsizleşince terk artıyor mu?
- Doluluk: Kademeli açmada isteğe bağlı alanların doldurulma oranı ne kadar düşüyor?
- Cihaz: Küçük ekranda kademeli açma daha mı çok fayda veriyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Kademeli açma gönderimi artırıyor mu?
- Form Başlama Oranı: Kısalan form ilk dokunuşu artırıyor mu?
- İsteğe Bağlı Alan Doldurma Oranı: Toplanan veri kalitesi kabul edilemez seviyeye düşmemeli.
- Ortalama Doldurma Süresi: Açılıp kapanan bölümler süreyi uzatmamalı.
- Alan Terk Oranı: Beliren alanda ani bırakma olmamalı.

**Yapılmaması gerekenler**
- Zorunlu bir alanı kademeli açmanın arkasına gizlemeyin; kullanıcı ne isteneceğini bilmeden başlamamalı.
- Açılan alanı sayfayı zıplatarak göstermeyin; içerik kayması ayrı bir değişkendir.
- Aynı testte hem kademeli açma hem alan sayısı azaltma yapmayın.
- İsteğe bağlı alanların doldurulma oranı düştü diye testi hemen kesmeyin; tamamlama artışıyla birlikte değerlendirin.
- Kademeli açmayı hassas alanı gizlemek için kullanmayın; hassas alan için kural 14’teki yöntemler geçerlidir.

---

## Sayfa açılır açılmaz imleci ilk alana koymak işe yarar mı?

Sayfa açılır açılmaz ilk alana odaklanmak bir adımı ortadan kaldırır ve masaüstünde yazmaya doğrudan başlatır. Mobilde ise klavyeyi zorla açar, sayfayı yukarı iter ve kullanıcının önce içeriği okumasını engelleyebilir. Formun sayfa içindeki konumu da sonucu değiştirir.

**Test edilmesi gerekenler**
- Odak: İlk alana otomatik odaklanmak doldurmayı başlatıyor mu?
- Kaydırma: Otomatik odak sayfayı forma kaydırıp üstteki içeriği atlatıyor mu?
- Klavye: Mobilde açılan klavye ekranın ne kadarını kapatıyor?
- Konum: Form ekranın altındaysa otomatik odak faydalı mı, rahatsız edici mi?
- Cihaz: Masaüstünde kazanan davranış mobilde de kazanıyor mu?

**Takip edilecek ana KPI’lar**
- Form Başlama Oranı: İlk alana giriş artıyor mu?
- Form Tamamlama Oranı: Başlama artışı gönderime dönüşüyor mu?
- Sayfa Terk Oranı: Otomatik odak nedeniyle sayfadan çıkış artmamalı.
- Üst İçerik Görüntülenme Oranı: Formun üstündeki açıklamanın okunması düşmemeli.
- Erişilebilirlik: Klavye ve ekran okuyucu ile gezinme sırası bozulmamalı.

**Yapılmaması gerekenler**
- Sayfa ortasındaki veya altındaki bir forma otomatik odak verip kullanıcıyı zorla oraya kaydırmayın.
- Mobilde otomatik odağı sınamadan masaüstü sonucuna göre açmayın.
- Aynı testte odak ile alan boyutunu birlikte değiştirmeyin.
- Modal içindeki forma odak verirken modalın kapatma düğmesini odak sırasından çıkarmayın.
- Otomatik odağı sayfa yüklenmesi tamamlanmadan tetikleyip odağın kaymasına izin vermeyin.

---

## Alan yüksekliğini büyütmek doldurmayı etkiler mi?

Daha büyük giriş alanı dokunma hedefini büyütür, mobilde yanlış dokunmayı azaltır ve alanın tıklanabilir olduğunu görsel olarak netleştirir. Karşı tarafta: büyüyen alanlar formu uzatır, ekranda aynı anda daha az alan görünür ve form daha ağır hissettirebilir.

**Test edilmesi gerekenler**
- Boyut: Alan yüksekliğini artırmak tamamlamayı değiştiriyor mu?
- Dokunma: Mobilde yanlış alana dokunma azalıyor mu?
- Algı: Büyüyen alanlar formu daha mı uzun gösteriyor?
- Görünen alan sayısı: Ekranda aynı anda daha az alan görünmesi terk yaratıyor mu?
- Cihaz: Kazanç mobile mi özgü, masaüstünde de var mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Büyük alan gönderimi artırıyor mu?
- Yanlış Dokunma Oranı: Hedef dışına dokunma azalıyor mu?
- Form Başlama Oranı: İlk dokunuş artıyor mu?
- Ortalama Doldurma Süresi: Süre uzamamalı.
- Erişilebilirlik: Dokunma hedefi erişilebilirlik alt sınırının altına inmemeli.

**Yapılmaması gerekenler**
- Aynı testte alan yüksekliği ile yazı tipi boyutunu birlikte değiştirmeyin.
- Alanı büyütürken aradaki boşluğu da değiştirmeyin; ikisi ayrı değişkendir.
- Dokunma hedefini küçülten bir varyantı erişilebilirlik alt sınırının altına indirmeyin; bu test edilecek bir seçenek değildir.
- Masaüstünde ölçüp mobil dokunma davranışı hakkında sonuç çıkarmayın.
- Alanı büyütüp aynı anda ekranda görünen alan sayısını düşürürken bunu yalnızca tamamlama ile değerlendirmeyin, başlama oranına da bakın.

---

## Otomatik tamamlama form doldurmayı hızlandırır mı?

Adres, şehir, şirket gibi alanlarda öneri listesi yazma yükünü azaltır ve yazım hatasını düşürür. Riski: öneri listesi yanlış eşleşme sunarsa kullanıcı hatalı veriyi onaylar, ya da liste klavyenin üstünü kapatıp kullanıcıyı kilitler. Veri kalitesi kazancı ile tamamlama kazancı aynı yönde olmayabilir.

**Test edilmesi gerekenler**
- Öneri: Otomatik tamamlama tamamlamayı artırıyor mu?
- Doğruluk: Seçilen öneriler gerçekten doğru veri mi üretiyor?
- Serbest giriş: Listede olmayan değeri yazabilme kapalıysa terk artıyor mu?
- Liste uzunluğu: Kaç öneri gösterildiğinde seçim hızlanıyor?
- Cihaz: Mobilde öneri listesi klavyeyle çakışıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Öneri gönderimi artırıyor mu?
- Adres/Alan Doğruluk Oranı: Hatalı veri oranı artmamalı.
- Ortalama Doldurma Süresi: Alan doldurma süresi kısalıyor mu?
- Alan Terk Oranı: Öneri listesi olan alanda bırakma artmamalı.
- Operasyonel Yük: Yanlış veriden doğan düzeltme/iletişim maliyeti artmamalı.

**Yapılmaması gerekenler**
- Serbest metin girişini tamamen kapatıp kullanıcıyı listeye hapsetmeyin.
- Öneri kaynağının kapsamı düşükken testi başlatmayın; eksik veri kaynağı öneriyi değil altyapıyı ölçer.
- Aynı testte otomatik tamamlama ile alan sayısını birlikte değiştirmeyin.
- Tamamlama arttı diye veri doğruluğuna bakmadan kazandı demeyin.
- Öneri listesini klavye ile gezilemez hâlde bırakmayın.

---

## Alan altına açıklama eklemek hata oranını düşürür mü?

Kısa bir yardım metni (“Fatura adresinizle aynı olmalı”, “Örnek: 5xx xxx xx xx”) hatalı girişi azaltabilir ve tereddüdü giderebilir. Karşı tarafta: her alana açıklama eklemek formu görsel olarak ağırlaştırır, önemli uyarının fark edilmesini zorlaştırır ve gerçek sorunun yanlış alan tasarımı olduğunu gizler.

**Test edilmesi gerekenler**
- Açıklama: Alan altı yardım metni hata oranını düşürüyor mu?
- Kapsam: Tüm alanlara mı, yalnızca hata alan alanlara mı eklenmeli?
- Zamanlama: Açıklama sürekli mi görünmeli, yoksa odaklanınca mı belirmeli?
- Ton: Örnek format vermek mi, gerekçe açıklamak mı daha etkili?
- Segment: Yeni ziyaretçi ile kayıtlı kullanıcı açıklamaya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Doğrulama Hatası Oranı: Hatalı gönderim azalıyor mu?
- Form Tamamlama Oranı: Tamamlama düşmemeli.
- Alan Bazlı Terk Oranı: Açıklama eklenen alanda bırakma azalıyor mu?
- Ortalama Doldurma Süresi: Okuma yükü süreyi belirgin uzatmamalı.
- Destek Talebi Sayısı: Aynı konudaki soru sayısı azalıyor mu?

**Yapılmaması gerekenler**
- Her alana açıklama ekleyip hangisinin işe yaradığını ölçemez hâle gelmeyin.
- Açıklamayı hata mesajının yerine koymayın; ikisi farklı işlev görür.
- Yardım metnini tıklanınca açılan bir ipucunun arkasına gizleyip “açıklama ekledik” demeyin; görünürlük ayrı bir değişkendir.
- Açıklama metnini kontrastı düşük gri ile yazıp okunmaz hâle getirmeyin.
- Hatalı alan tasarımını açıklama ile yamamayın; asıl çözüm alanın kendisi olabilir.

---

## Sosyal hesapla giriş seçeneği kaydı artırır mı?

Sosyal giriş şifre oluşturma yükünü kaldırır ve kaydı hızlandırır. Buna karşılık kullanıcı hangi verinin paylaşılacağından çekinebilir, kurumsal kullanıcı kişisel hesabıyla giriş yapmak istemeyebilir ve sonradan “hangi yöntemle giriş yapmıştım” karışıklığı destek yüküne dönüşebilir.

**Test edilmesi gerekenler**
- Seçenek: Sosyal giriş eklemek kayıt oranını artırıyor mu?
- Sağlayıcı sayısı: Tek sağlayıcı mı, birkaç sağlayıcı mı daha iyi çalışıyor?
- Hiyerarşi: Sosyal giriş birincil mi olmalı, e-posta ile kaydın altında mı durmalı?
- Geri dönüş: Kullanıcılar sonraki girişte aynı yöntemi bulabiliyor mu?
- Segment: Bireysel ve kurumsal kullanıcı farklı yönteme mi yöneliyor?

**Takip edilecek ana KPI’lar**
- Kayıt Tamamlama Oranı: Sosyal giriş kaydı artırıyor mu?
- İkinci Oturum Giriş Oranı: Kullanıcı geri dönüp giriş yapabilmeli, düşmemeli.
- Kayıt Sonrası Aktivasyon Oranı: Hızlı kayıt niteliksiz kullanıcı getirmemeli.
- Giriş Kaynaklı Destek Talebi: “Giriş yapamıyorum” talepleri artmamalı.
- E-posta Erişilebilirlik Oranı: Ulaşılabilir e-posta adresi toplama oranı düşmemeli.

**Yapılmaması gerekenler**
- Sosyal girişi tek seçenek yapıp e-posta ile kaydı kaldırmayın.
- Hangi verilerin alındığını gizleyen bir buton metni kullanmayın.
- Aynı testte hem sosyal giriş eklemeyi hem form alanı azaltmayı yapmayın.
- Kayıt arttı diye aktivasyona bakmadan kazandı demeyin.
- Kimlik doğrulama akışının güvenlik adımlarını sürtünme diye testin konusu yapmayın (kural 6).

---

## Şifre yerine tek kullanımlık kod göndermek girişi artırır mı?

Şifresiz giriş (e-postaya veya telefona gönderilen tek kullanımlık kod) unutulan şifre kaynaklı kayıpları ortadan kaldırır. Bedeli: kullanıcı e-posta veya SMS’e geçmek zorunda kalır, kod gecikirse akış kopar ve kanal teslim oranı doğrudan dönüşüme yansır.

**Test edilmesi gerekenler**
- Yöntem: Tek kullanımlık kod ile şifreli giriş arasında tamamlama farkı var mı?
- Kanal geçişi: Kullanıcı e-postaya gidip geri dönebiliyor mu, akış kopuyor mu?
- Teslim süresi: Kodun ulaşma süresi tamamlamayı ne kadar etkiliyor?
- Alternatif: Şifreli giriş ikinci seçenek olarak kalırsa sonuç değişiyor mu?
- Cihaz: Mobilde kod otomatik doldurulduğunda fark büyüyor mu?

**Takip edilecek ana KPI’lar**
- Giriş Tamamlama Oranı: Yöntem girişi tamamlatıyor mu?
- Kod Teslim ve Kullanım Oranı: Gönderilen kodun kullanılma oranı düşmemeli.
- İlk Deneme Başarı Oranı: Tek seferde giriş yapabilme artıyor mu?
- Şifre Sıfırlama Talebi: Sıfırlama yükü azalıyor mu?
- Destek Talebi Sayısı: Giriş kaynaklı talepler artmamalı.

**Yapılmaması gerekenler**
- İki adımlı doğrulamayı veya kimlik doğrulamayı bu testin kapsamına almayın; bunlar koruma amaçlıdır (kural 6).
- Kod teslim altyapısı kararsızken testi başlatmayın; altyapıyı ölçmüş olursunuz.
- Şifreli girişi aynı anda kaldırıp geri dönüşü olmayan bir varyant kurmayın.
- Kod geçerlilik süresini test ortasında değiştirmeyin.
- Yalnızca yeni kullanıcıda ölçüp sonucu mevcut kullanıcı tabanına genellemeyin.

---

## Kaydı aksiyondan sonraya ertelemek tamamlamayı artırır mı?

Kayıt ekranını aksiyonun önüne koymak niyeti test eder ama hazır olmayan kullanıcıyı kaybeder. Kaydı sonraya bırakmak (önce işlemi yaptırmak, sonra kaydetmeyi teklif etmek) tamamlamayı artırabilir, buna karşılık kayıtsız tamamlanan işlemlerin geri dönüşü ve iletişimi zorlaşır.

**Test edilmesi gerekenler**
- Zamanlama: Kayıt aksiyondan önce mi, sonra mı istenmeli?
- Değer anı: Kullanıcı faydayı gördükten sonra kayıt oranı artıyor mu?
- Kayıp: Kayıtsız tamamlayanların ne kadarı sonradan kaydoluyor?
- Çerçeveleme: Kaydı “ilerlemeni kaydet” diye sunmak farkı büyütüyor mu?
- Segment: Yeni ziyaretçi ile geri dönen kullanıcı farklı zamanlamaya mı uyuyor?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: Asıl işlemi bitirenler artıyor mu?
- Kayıt Oranı: Toplam kayıt sayısı kabul edilemez seviyeye düşmemeli.
- Kayıt Sonrası Geri Dönüş Oranı: İkinci ziyaret oranı düşmemeli.
- İletişim İzni Oranı: Ulaşılabilir kullanıcı oranı düşmemeli.
- Destek Talebi Sayısı: “İşlemimi bulamıyorum” talepleri artmamalı.

**Yapılmaması gerekenler**
- Kaydı erteleyip sonra kullanıcıyı kapatılamayan bir ekranla kayda zorlamayın (kural 6).
- İşlemi tamamlatıp ardından sonucu kayıt arkasına kilitlemeyin.
- Aynı testte hem zamanlamayı hem kayıt formunun alanlarını değiştirmeyin.
- Aksiyon tamamlama arttı diye kayıt kaybını ölçmeden kazandı demeyin.
- Yasal olarak kimlik veya izin gerektiren bir işlemde kaydı ertelemeyi test konusu yapmayın.

---

## Formu modal içinde mi, sayfa akışında mı göstermeli?

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
- Sayfa Terk Oranı: Modal nedeniyle sayfadan çıkış artmamalı.
- Erişilebilirlik: Modal açıkken odak dışarı kaçmamalı, klavyeyle kapatma bozulmamalı.

**Yapılmaması gerekenler**
- Kapatılamayan veya kapatma düğmesi gizlenmiş modal önermeyin (kural 6).
- Modalın arka planını karartma yoğunluğunu aynı testte değiştirmeyin; bu ayrı bir değişkendir.
- Veri girilmiş bir modalı dışına tıklayınca uyarısız kapatan varyantı kazanan ilan etmeyin.
- Mobilde modalı ekranın yarısına sıkıştırıp masaüstü sonucuyla karşılaştırmayın.
- Modalı açılış anında değil kullanıcı davranışına göre tetikliyorsanız tetikleme kuralını test ortasında değiştirmeyin.

---

## Çok adımlı formda geri dönüş imkânı tamamlamayı etkiler mi?

Görünür bir geri düğmesi hata düzeltmeyi kolaylaştırır ve kullanıcıya kontrol hissi verir. Karşı argüman: geri dönüş imkânı ilerlemeyi yavaşlatır, kullanıcı adımlar arasında gidip gelir ve girilen veri kaybolursa güven zedelenir. Asıl belirleyici, geri dönüldüğünde verinin korunup korunmadığıdır.

**Test edilmesi gerekenler**
- Görünürlük: Geri düğmesi görünür olduğunda tamamlama değişiyor mu?
- Veri koruma: Geri dönünce girilen veri korunuyor mu?
- Özet: Son adımda düzenleme bağlantısı vermek geri dönüş ihtiyacını karşılıyor mu?
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
- Geri dönüş az kullanıldı diye faydasız saymayın; nadir ama kritik bir kurtarma yolu olabilir.
- Ödeme adımında geri dönüşü test ederken işlem güvenliği kontrollerini zayıflatmayın (kural 6).

---

## Formu cümle hâline getirmek doldurmayı artırır mı?

Alanları bir cümlenin içine yerleştirmek (“Ben [ad], [şehir]’de [hizmet] arıyorum”) formu ankete değil sohbete benzetir ve kısa formlarda samimi durur. Riski: uzun formlarda cümle yapısı dağılır, alanların sırası dilbilgisine esir olur, hata mesajlarını yerleştirmek zorlaşır ve ekran okuyucu deneyimi bozulabilir.

**Test edilmesi gerekenler**
- Biçim: Cümle formu klasik alan listesinden daha mı çok dolduruluyor?
- Uzunluk: Kaç alandan sonra cümle yapısı bozuluyor?
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

---

## Formu sayfanın ortasına almak mı, sola hizalamak mı?

Ortalanmış form dikkati toplar ve tek amaçlı sayfalarda doğal durur. Sola hizalı form ise okuma yönüyle uyumludur ve yanına açıklama, güvence veya özet yerleştirmeye izin verir. Ortalama, formun yanındaki destekleyici içeriği de ortadan kaldırır.

**Test edilmesi gerekenler**
- Hizalama: Ortalanmış form tamamlamayı artırıyor mu?
- Destek içeriği: Formun yanındaki güvence veya özet kaybolunca ne oluyor?
- Odak: Ortalama dikkat dağıtıcıları gerçekten azaltıyor mu?
- Genişlik: Form genişliği hizalamadan bağımsız olarak etkiliyor mu?
- Cihaz: Mobilde zaten tek sütuna düşen düzende fark kalıyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Hizalama gönderimi artırıyor mu?
- Form Başlama Oranı: İlk dokunuş artıyor mu?
- Destek İçerik Görülme Oranı: Yandaki güvencelerin görülmesi kabul edilemez ölçüde düşmemeli.
- Ortalama Doldurma Süresi: Süre uzamamalı.
- Sayfa Terk Oranı: Çıkış artmamalı.

**Yapılmaması gerekenler**
- Aynı testte hizalama ile form genişliğini birlikte değiştirmeyin.
- Ortalarken yandaki güvence içeriğini sessizce kaldırmayın; kaldırıyorsanız bu ayrı bir testtir.
- Mobilde fark olmayan bir değişikliği mobil kazancı gibi raporlamayın.
- Ortalanmış formu ekranın dikey ortasına sabitleyip kaydırmayı engellemeyin.
- Tek sayfada ölçüp sonucu farklı amaçlı formlara genellemeyin.

---

## Modal formda arka planı soldurmak dikkati topluyor mu?

Arka planı karartmak veya bulanıklaştırmak modalı öne çıkarır ve form dışındaki her şeyi görsel olarak susturur. Karşı tarafta: karartma kullanıcının bağlamını kaybetmesine yol açar, hangi sayfadan geldiğini hatırlamasını zorlaştırır ve yoğun karartma kapana kısılma hissi verebilir.

**Test edilmesi gerekenler**
- Yoğunluk: Arka plan karartması tamamlamayı artırıyor mu?
- Bağlam: Arkadaki bilginin görünmesi karar için gerekli mi?
- Biçim: Karartma mı, bulanıklaştırma mı daha iyi çalışıyor?
- Kapatma: Karartılmış alana tıklayınca ne olmalı?
- Cihaz: Mobilde tam ekran forma geçmek karartmadan daha mı iyi?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Karartma gönderimi artırıyor mu?
- Yanlışlıkla Kapatma Oranı: Veri girildikten sonra kapatma artmamalı.
- Form Başlama Oranı: Formun fark edilmesi artıyor mu?
- Sayfa Terk Oranı: Kapana kısılma hissi çıkışı artırmamalı.
- Erişilebilirlik: Odak modaldan kaçmamalı, klavyeyle kapatma yolu kaybolmamalı.

**Yapılmaması gerekenler**
- Kapatma yolu bırakmayan bir karartma kurmayın (kural 6).
- Aynı testte karartma yoğunluğu ile modal içeriğini birlikte değiştirmeyin.
- Karar için gereken bilgiyi arkada karartılmış hâlde bırakmayın.
- Veri girilmiş formu dışına tıklayınca uyarısız kapatmayın.
- Hareket azaltma tercihini yok sayan bir bulanıklaştırma animasyonu kullanmayın.

---

## Hazır şablon metin sunmak serbest metin alanını doldurtuyor mu?

Boş bir metin kutusu, ne yazacağını bilmeyen kullanıcıyı durdurur. Hazır bir örnek metin sunmak (düzenlenebilir bir taslak) bu engeli kaldırır ve alanın doldurulma oranını artırabilir. Riski: gönderilen metinlerin çoğu birbirinin aynısı olur, kişisel olmaktan çıkar ve alıcı tarafında değeri düşer.

**Test edilmesi gerekenler**
- Şablon: Hazır metin sunmak alanın doldurulmasını artırıyor mu?
- Kişiselleştirme: Kullanıcılar şablonu düzenliyor mu, olduğu gibi mi gönderiyor?
- Seçenek: Birden fazla şablon sunmak çeşitliliği artırıyor mu?
- Sunum: Şablon alana yazılı mı gelmeli, bir düğmeyle mi eklenmeli?
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
- Doldurma oranı arttı diye metinlerin özgünlüğüne bakmadan kazandı demeyin.

---

## Tutar seçiminde hazır butonlar mı, serbest giriş mi sunmalı?

Hazır tutar butonları karar yükünü kaldırır, bir aralık önerir ve yazma zahmetini sıfırlar. Serbest giriş kutusu ise kullanıcıyı kendi tutarını belirlemekte özgür bırakır ama boş kutu ne yazılacağı konusunda bir işaret vermez. Sunulan butonların hangi tutarları içerdiği, seçilen ortalama tutarı doğrudan belirler.

**Test edilmesi gerekenler**
- Biçim: Hazır butonlar mı, serbest giriş mi daha çok tamamlatıyor?
- Aralık: Buton tutarları ortalama seçimi hangi yöne çekiyor?
- Birlikte sunum: Butonların yanında serbest giriş de bulunmalı mı?
- Varsayılan: Butonlardan biri önceden seçili gelmeli mi?
- Segment: İlk kez ödeme yapan ile tekrar edenler farklı mı davranıyor?

**Takip edilecek ana KPI’lar**
- Kullanıcı Başına Toplam Tutar: Biçim toplam tutarı artırıyor mu?
- Tamamlama Oranı: İşlemi bitiren kullanıcı oranı artıyor mu?
- Ortalama Seçilen Tutar: Ortalama tutar düşmemeli.
- Serbest Giriş Kullanım Oranı: Kendi tutarını girenlerin oranı ne kadar?
- İptal veya Düzeltme Oranı: Yanlış tutar kaynaklı düzeltme artmamalı.

**Yapılmaması gerekenler**
- Serbest giriş imkânını tamamen kaldırıp kullanıcıyı hazır tutarlara hapsetmeyin.
- Yüksek bir tutarı önceden seçili getirip kullanıcıyı fark etmeden ona yönlendirmeyin; ödenecek tutarı artıran varsayılan kural 6 sınırındadır (bkz. cart-checkout → varsayılan işaretli seçenekler).
- Aynı testte butonların varlığı ile buton tutarlarını birlikte değiştirmeyin.
- Tamamlama arttı diye ortalama tutara bakmadan kazandı demeyin.
- Tutarları görünmez küçüklükte yazıp seçim yapmayı zorlaştırmayın.

---

## Formun başına uygunluk açıklaması koymak talebin niteliğini artırır mı?

Formun üstüne kimin için uygun olduğunu yazmak (asgari bütçe, hizmet bölgesi, gerekli koşul) uymayan kullanıcıyı baştan eler ve satış ekibinin yükünü azaltır. Bedeli: toplam talep sayısı düşer, sınırda kalan bazı uygun kullanıcılar da kendini dışarıda görüp vazgeçer.

**Test edilmesi gerekenler**
- Açıklama: Uygunluk bilgisi nitelikli talebi artırıyor mu?
- Hacim kaybı: Toplam talep ne kadar düşüyor?
- Ton: Koşulu net söylemek mi, yumuşak ifade etmek mi daha iyi çalışıyor?
- Yanlış eleme: Aslında uygun olan kullanıcılar da eleniyor mu?
- Segment: Farklı kullanıcı tipleri açıklamaya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Nitelikli Talep Sayısı: Satışa uygun talep artıyor mu?
- Toplam Form Gönderimi: Hacim kabul edilemez ölçüde düşmemeli.
- Talep Başına Nitelik Oranı: Uygun talep oranı artıyor mu?
- Satış Ekibi Eleme Süresi: Eleme yükü azalıyor mu?
- Fırsat Kapanış Oranı: Gelen taleplerin satışa dönüşü artıyor mu?

**Yapılmaması gerekenler**
- Uygunluk açıklamasını caydırıcı veya küçümseyici bir dille yazmayın.
- Aynı testte açıklama ile form alanlarını birlikte değiştirmeyin.
- Gerçekte esnek olan bir koşulu kesin kuralmış gibi yazmayın.
- Hacim düştü diye niteliğe bakmadan kaybetti demeyin; birincil metrik nitelikli taleptir.
- Ayrımcılık doğuracak bir eleme kriterini uygunluk açıklaması olarak kullanmayın.

---

## Asıl formdan önce küçük bir ısındırma sorusu sormak tamamlama oranını artırır mı?

Kullanıcıyı doğrudan çok alanlı bir formla karşılaştırmak yerine, önce tek ve kolay bir soruyla (“Hangisi size en yakın?”) başlamak küçük bir taahhüt yaratır — bu taahhüdün ardından gelen asıl formu tamamlama isteği güçlenebilir. Bu, alanları kademeli açmaktan farklıdır: orada aynı formun alanları sırayla açılır, burada asıl formdan önce ayrı, ilgisiz görünmeyen bir soru sorulur.

**Test edilmesi gerekenler**
- Soru türü: Kategori seçimi mi, evet/hayır sorusu mu daha çok ilerletiyor?
- İlgi: Isındırma sorusu asıl formun konusuyla doğrudan ilişkili mi olmalı?
- Görsel geçiş: Isındırma sorusundan asıl forma geçiş tek ekranda mı, ayrı bir adımda mı daha akıcı?
- Atlanabilirlik: Soruyu atlama seçeneği sunmak tamamlama oranını düşürüyor mu?
- Segment: Mobil ve masaüstünde ısındırma adımının etkisi farklı mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Isındırma sorusuyla başlayan akış, doğrudan forma göre daha çok tamamlanıyor mu?
- Isındırma Sorusu Yanıtlama Oranı: Soruyu yanıtlayıp devam eden ziyaretçi oranı nedir?
- Toplam Süre: Isındırma adımı toplam tamamlama süresini kabul edilemez ölçüde uzatmamalı.
- Talep Niteliği: Isındırma sorusu talebin niteliğini düşürmemeli.
- Terk Oranı: Isındırma adımının kendisinde terk artmamalı.

**Yapılmaması gerekenler**
- Isındırma sorusunu asıl formla ilgisiz, dikkat dağıtıcı bir konu yapmayın.
- Aynı testte ısındırma sorusunun içeriğini ve asıl formun alan sayısını birlikte değiştirmeyin.
- Soruyu zorunlu hâle getirip atlama seçeneği sunmadan ilerlemeyi engellemeyin.
- Isındırma sorusunun cevabını, kullanıcıya söylemeden başka bir amaç (ör. segmentleme) için kullanmayın.
- Isındırma adımını, asıl formun alan sayısını azaltmanın yerine geçen bir çözüm gibi sunmayın — ikisi ayrı testtir.

---

## Form alanının yanına veri gizliliği güvencesi eklemek kayıt oranını artırır mı?

E-posta veya telefon isteyen bir form, kullanıcıda “bu bilgi spam’e mi dönüşecek” tereddüdü yaratabilir. Alanın hemen yanına kısa bir güvence metni (“E-postanızı kimseyle paylaşmayız”) koymak bu tereddüdü giderebilir, ama gereksiz yere hatırlatma da tam tersi bir etki yaratıp “neden bunu söylemeleri gerekti” şüphesi doğurabilir.

**Test edilmesi gerekenler**
- Varlık: Güvence metni eklemek kayıt oranını artırıyor mu, yoksa şüphe mi uyandırıyor?
- Konum: Metin alanın hemen altında mı, gönder butonunun yanında mı daha etkili?
- İkon: Kilit veya kalkan ikonu eklemek metnin etkisini güçlendiriyor mu?
- Somutluk: Genel bir ifade mi (“gizliliğinize önem veriyoruz”), spesifik bir taahhüt mü (“asla üçüncü taraflarla paylaşmayız”) daha ikna edici?
- Segment: Hassas sayılabilecek bir bilgi (ör. telefon) istenen formlarda etki, yalnızca e-posta isteyen formdan farklı mı?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Güvence metni kayıt oranını artırıyor mu?
- Alan Terk Oranı: Kullanıcı ilgili alanı doldurmadan formu bırakmıyor mu?
- Güven Algısı (anket): Metin güveni artırdığını hissettiriyor mu, yoksa şüphe mi uyandırıyor?
- Sayfada Kalma Süresi: Ek metin okuma süresini kabul edilemez ölçüde uzatmamalı.
- Kayıt Sonrası Şikâyet: Verilen sözle kayıt sonrası gönderim davranışı tutarsızsa bu artmamalı — artıyorsa ayrı, engelleyici bir bulgudur (kural 6).

**Yapılmaması gerekenler**
- Vermediğiniz bir sözü yazmayın — “asla paylaşmayız” derken üçüncü taraf pazarlama ortaklarıyla paylaşıyorsanız bu kural 6 ihlalidir.
- Aynı testte güvence metnini ve form alan sayısını birlikte değiştirmeyin.
- Metni, gerçek bir gizlilik politikası bağlantısının yerine geçecek şekilde sunmayın — ayrıntılı politika hâlâ erişilebilir olmalı.
- Güvence metnini o kadar büyük veya göze batan yapmayın ki asıl formu gölgelesin.
- Hedef pazarın veri koruma mevzuatının gerektirdiği açık rıza metnini bu güvence cümlesiyle karıştırıp eksik bırakmayın (kural 11).

---

## Tek seçimlik bir alanda radio button mu, açılır liste (dropdown) mu daha çok tamamlatıyor?

Radio button tüm seçenekleri aynı anda görünür kılar, kullanıcı tıklamadan karşılaştırma yapabilir ama seçenek sayısı arttıkça dikey yer kaplar. Dropdown yer kazandırır ve çok seçenekli durumlarda formu kısa gösterir, buna karşılık seçenekleri görmek için bir ek tıklama gerektirir ve mobilde platformun kendi bileşenine bağlı bir davranışa geçer — kullanıcı neyle karşılaşacağını göremeden tıklar.

**Test edilmesi gerekenler**
- Biçim: Radio button mu, dropdown mu ilgili alanın doldurulma oranını artırıyor?
- Seçenek sayısı: Kaç seçenekten sonra dropdown radio button’dan daha avantajlı hâle geliyor?
- Varsayılan: Dropdown’da hiçbir seçeneğin önceden seçili gelmemesi doğru seçime mi yönlendiriyor, yoksa atlanmasına mı yol açıyor?
- Hata: Yanlış seçim oranı biçime göre değişiyor mu?
- Cihaz: Mobilde platformun kendi dropdown bileşeni radio button’a göre nasıl bir fark yaratıyor?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Biçim gönderimi artırıyor mu?
- Alan Bazlı Hata Oranı: Yanlış veya eksik seçim artmamalı.
- Ortalama Doldurma Süresi: İlgili alanı doldurma süresi uzamamalı.
- Alan Terk Oranı: İlgili alanda bırakma artmamalı.
- Erişilebilirlik: Klavye ile gezinme ve ekran okuyucu davranışı biçime göre bozulmamalı.

**Yapılmaması gerekenler**
- Aynı testte biçimle birlikte seçenek sayısını veya sırasını değiştirmeyin.
- Dropdown’da bir seçeneği önceden seçili getirip kullanıcının fark etmeden onu onaylamasına yol açmayın.
- Çok az seçenek için dropdown, çok fazla seçenek için radio button önermeyin; ikisi de yanlış bağlamda dezavantajlıdır.
- Mobil platformun kendi dropdown bileşenini özel bir bileşenle değiştirip erişilebilirlik davranışını bozmayın.
- Tek bir alan tipinde ölçüp sonucu tüm tek seçimlik alanlara genellemeyin.
