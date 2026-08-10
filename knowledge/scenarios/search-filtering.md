# Arama ve Filtreleme

Yolculuk aşaması: kullanıcı ne istediğini biliyor veya keşfediyor; arama kutusu, filtreler, sonuç sayfası ve site içi navigasyon menüleri (sticky/mega menü senaryoları da bu dosyadadır). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Filtreler anında mı, toplu mu uygulanmalı?

Anında filtreleme hızlı geri bildirim verir; toplu filtreleme daha kontrollü bir deneyim sunar. Hangisinin keşif ve dönüşümde daha iyi çalıştığı ölçülmelidir.

**Test edilmesi gerekenler**
- Hız algısı: Anında sonuç göstermek daha akıcı bir deneyim sunuyor mu?
- Kontrol hissi: Toplu filtreleme hatalı seçimleri azaltıyor mu?
- Performans: Sık yenileme sayfa hızını düşürüyor mu?
- Dönüşüm: Hangi model daha yüksek satın alma oranı sağlıyor?
- Cihaz: Mobil ve masaüstünde kazanan farklı mı?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Hangi filtre modeli daha çok satış getiriyor?
- Filtre Kullanım Oranı: Hangi modelde daha çok filtre uygulanıyor?
- Keşif Derinliği: Daha fazla ürün görüntüleniyor mu?
- Sayfa Yenileme Süresi: Site hızı bozulmamalı.
- Terk Oranı: Yükselmemeli.

**Yapılmaması gerekenler**
- Test sırasında tasarım, sıralama veya ürün listesini değiştirmeyin.
- Filtre sonrası gereksiz animasyon ve geçiş koymayın; performansı düşürür.
- Seçili filtrelerin görünmediği veya kaybolduğu durumlar bırakmayın.
- Aynı testte hem filtre modelini hem filtre setini değiştirmeyin.
- Çok agresif otomatik yenileme kullanmayın; kullanıcıyı yorar.

---

## Arama çubuğu ne kadar görünür olmalı?

Arama çubuğunun konumu ve görünürlüğü, kullanıcının ürün keşif davranışını değiştirebilir. Bunun dönüşüme yansıyıp yansımadığı ölçülmelidir.

**Test edilmesi gerekenler**
- Konum: Header’da mı, menü içinde mi, yalnızca ikon olarak mı?
- Görünürlük: Açık arama alanı mı, sadece ikon mu daha çok tıklanıyor?
- Placeholder: “Ürün ara…” mı, “Favori markanı yaz” mı daha etkili?
- Öneriler: Otomatik öneri doğru ürüne ulaşmayı hızlandırıyor mu?
- Cihaz: Mobilde ve masaüstünde görünürlük ihtiyacı aynı mı?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Arama yapanların satın alma oranı artıyor mu?
- Arama Kullanım Oranı: Görünürlük arama kullanımını artırıyor mu?
- Arama → Ürün Tıklama: Doğru ürüne daha hızlı ulaşılıyor mu?
- Arama Başarı Oranı: Düşmemeli; sonuçsuz arama artmamalı.
- Sayfada Kalma Süresi: Keşif derinleşiyor mu?

**Yapılmaması gerekenler**
- Arama kullanımı yüksek bir sitede menü-içi kolu teste hiç sokmayın; o kol ancak arama payı düşükse denenir.
- Placeholder metnini uzun yazmayın; okunabilirlik düşer.
- Test sırasında öneri algoritmasını değiştirmeyin.
- Mobilde arama ikonunu tıklanamayacak kadar küçültmeyin.
- Sonuçsuz aramada kullanıcıyı boş ekranda bırakmayın.

---

## Varsayılan arama önerileri dönüşümü etkiliyor mu?

Arama alanının önceki aramaları otomatik doldurup doldurmaması, keşif sürecini ve karar hızını değiştirebilir.

**Test edilmesi gerekenler**
- Hız: Varsayılan öneri varken aramaya daha hızlı başlanıyor mu?
- Keşif: Otomatik doldurmamak yeni içerik keşfini artırıyor mu?
- Boş kutu: Boş arama kutusu popüler kategorilere yönlendiriyor mu?
- Süreç: Otomatik doldurmayı kapatmak süreci hızlandırıyor mu?
- Geçmiş: Geçmişe erişimi kaldırmak şikâyet yaratıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Arama sonrası satın alma nasıl değişiyor?
- Arama Başlatma Oranı: Arama yapmaya başlama artıyor mu?
- İlk Sonuca Ulaşma Süresi: Kullanıcı daha hızlı ulaşıyor mu?
- Sıfır Sonuçlu Arama: Artmamalı.
- Keşif Derinliği: Yeni kategori görüntüleme artıyor mu?

**Yapılmaması gerekenler**
- Önceki aramaları tamamen kaldırmayın; kullanıcı geçmişe erişebilmeli.
- Test boyunca placeholder metnini değiştirmeyin.
- Aynı testte kategori ve filtre isimlerini değiştirmeyin.
- Otomatik önerileri tümden kapatıp kullanıcıyı yönsüz bırakmayın.
- Öneri kaynağını (algoritma veya elle liste) test ortasında değiştirmeyin.

---

## Sıfır sonuç sayfası kullanıcıyı elde tutuyor mu?

Sonuç bulunamayan arama, terk oranı en yüksek ekranlardan biridir. Boş bir ekran yerine yazım önerisi, popüler kategoriler ve benzer ürünler sunmak bu trafiği kurtarabilir.

**Test edilmesi gerekenler**
- Öneri: Yazım önerisi kurtarma oranını ne kadar artırıyor?
- İçerik: Popüler kategori mi, çok satan ürün mü daha çok tıklanıyor?
- Arama kutusu: Ekranda tutmak yeniden arama oranını artırıyor mu?
- Blok sırası: Hangi öneri bloğu en etkili?
- Cihaz: Mobilde ve masaüstünde davranış farklı mı?

**Takip edilecek ana KPI’lar**
- Sıfır Sonuç Kurtarma Oranı: Ürün sayfasına geçen kullanıcı oranı.
- Yeniden Arama Oranı: İkinci bir arama yapılıyor mu?
- Oturum Devam Oranı: Siteden çıkılmıyor mu?
- Genel Arama Dönüşümü: Toplam performans düşmemeli.
- Sayfa Yüklenme Süresi: Öneri blokları yavaşlatmamalı.

**Yapılmaması gerekenler**
- Alakasız ürün önerip kullanıcıyı yanıltmayın.
- Arama kutusunu ekrandan kaldırmayın.
- Sıfır sonuç sayfasını sadece kampanya alanına çevirmeyin.
- Test sırasında arama eşleştirme kurallarını değiştirmeyin.
- Yazım önerisini otomatik uygulayıp kullanıcıyı şaşırtmayın.

---

## Arama sonuçlarında varsayılan sıralama ne olmalı?

Varsayılan sıralama, kullanıcıların büyük çoğunluğunun gördüğü tek sıralamadır. İlgi düzeyi, çok satan ve fiyat sıralamaları farklı kullanıcı gruplarına hizmet eder ve marj üzerinde farklı etki yaratır.

**Test edilmesi gerekenler**
- Dönüşüm: Hangi varsayılan sıralama daha yüksek dönüşüm getiriyor?
- Sepet: Çok satan sıralaması ortalama sepet tutarını düşürüyor mu?
- Kontrol: Kullanıcılar sıralamayı ne sıklıkla manuel değiştiriyor?
- Uzun kuyruk: Nadir aramalarda ilgi düzeyi daha mı iyi çalışıyor?
- Segment: Yeni ve dönen kullanıcıda kazanan farklı mı?

**Takip edilecek ana KPI’lar**
- Arama Dönüşüm Oranı (CR): Arama yapanların satın alma oranı.
- İlk Sonuca Tıklama Oranı: İlk 4 sonucun isabeti.
- Sıralama Değiştirme Oranı: Varsayılan yeterli mi?
- Ortalama Sepet Tutarı: Ucuza kayarsa AOV düşebilir.
- Sıfır Etkileşimli Arama: Artmamalı.

**Yapılmaması gerekenler**
- Sıralama seçeneklerini test sırasında gizlemeyin.
- Stokta olmayan ürünleri üst sıraya taşımayın.
- Aynı testte hem sıralamayı hem filtre setini değiştirmeyin.
- Sponsorlu ürünleri organik sonuç gibi göstermeyin.
- Sadece dönüşüme bakıp marj etkisini atlamayın.

---

## Sticky menü deneyimi iyileştiriyor mu?

Menünün sabit kalması sayfa içi gezinme hızını artırabilir, ancak ekran alanı kaplayarak rahatsız da edebilir.

**Test edilmesi gerekenler**
- Gezinme: Sticky menü sayfa içi gezinmeyi kolaylaştırıyor mu?
- Kaydırma: Yukarı çıkma zorunluluğunu ortadan kaldırıyor mu?
- Mobil: Uzun sayfalarda gezinme performansını artırıyor mu?
- Alan: Ekran alanını kaplaması rahatsız ediyor mu?
- Konum: Üstte mi, altta mı daha iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sticky menü satın almayı artırıyor mu?
- Menü Tıklama Oranı: Menü daha çok kullanılıyor mu?
- Sayfa Başına Görüntüleme: Oturumda daha çok sayfa geziliyor mu?
- Kaydırma Derinliği: İçerik okuma engelleniyor mu?
- Çıkış Oranı: Yükselmemeli; menü kullanıcıyı kaçırmamalı.

**Yapılmaması gerekenler**
- Sticky menüyü ekranın büyük bölümünü kaplayacak kadar yüksek yapmayın.
- Mobilde menünün CTA ve filtreleri kapatmasına izin vermeyin.
- Sayfa hızını düşüren animasyon ve gölge kullanmayın.
- Test süresince menü yapısını ve içeriğini değiştirmeyin.
- Menü sabitlenirken sayfa kaymasına yol açmayın.

---

## Mega menü mü, yatay menü mü?

Mega menü mü, sade yatay menü mü daha iyi gezinme sunuyor? Yapıdaki fark, içerik keşif davranışını ciddi biçimde değiştirebilir.

**Test edilmesi gerekenler**
- Hız: Hangi menü aranan içeriğe daha hızlı ulaştırıyor?
- Çıkış: Menü türü hemen çıkma oranını değiştiriyor mu?
- Süre: Menüde geçirilen süre artıyor mu, azalıyor mu?
- Yönlendirme: Menü kritik içeriğe yönlendirmeyi etkiliyor mu?
- Mobil: İki yapı arasındaki fark mobilde büyüyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sade menü satın almayı artırıyor mu?
- İlk Tıklama Süresi: Doğru kategoriye ulaşma süresi kısalıyor mu?
- Menü Tıklama Derinliği: Daha az adımda hedefe ulaşılıyor mu?
- Hemen Çıkma Oranı: Yükselmemeli; karmaşık menü kullanıcıyı kaçırmamalı.
- Kategori Sayfası Girişi: Kategoriye geçiş artıyor mu?

**Yapılmaması gerekenler**
- Test sırasında menü başlıklarının sırasını veya adını değiştirmeyin.
- Mega menüde çok fazla kategori sunmayın; bilgi yükü yaratır.
- Mobilde yatay menüde kaydırma sorununa izin vermeyin.
- Mega menüde kolon sayısını taranamayacak kadar artırmayın.
- Menü açılma hızını yavaşlatan animasyon eklemeyin.

---

## Menü sadeleştirmesi deneyimi etkiler mi?

Menüyü sadeleştirmek navigasyon hızını ve kategori keşfini etkileyebilir. Daha az karmaşık menü odaklanmayı kolaylaştırabilir.

**Test edilmesi gerekenler**
- Sadelik: Alt başlık sayısını azaltmak odaklanmayı kolaylaştırıyor mu?
- Hız: Sade menü aranan kategoriye daha hızlı ulaştırıyor mu?
- Tıklama: Kullanıcılar daha az tıklamayla ilerliyor mu?
- Süre: Navigasyon süresi anlamlı kısalıyor mu?
- Keşif: Sadeleşince keşfedilen kategori sayısı düşüyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sade menü satın almayı artırıyor mu?
- İlk Tıklama Süresi: Doğru kategoriye ulaşma kısalıyor mu?
- Menü Tıklama Derinliği: Daha az adımda hedefe varılıyor mu?
- Kategori Kapsama Oranı: Düşmemeli; keşfedilen kategori sayısı daralmamalı.
- Arama Kullanımı: Menü yetersiz kalıp aramaya mı itiyor?

**Yapılmaması gerekenler**
- Ana kategorileri tamamen kaldırmayın; bilgi kaybı hissi yaratır.
- Alt başlıkları aşırı azaltıp keşfi kısıtlamayın.
- Test sırasında ikon ve tasarım dilini değiştirmeyin.
- Mobilde sticky menünün kritik alanları kapatmasına izin vermeyin.
- Menü değişikliğiyle birlikte sayfa hızını etkileyen eklemeler yapmayın.

---

## İndirim filtresi davranışı nasıl etkiler?

İndirim yüzdesine göre filtreleme sunmak ürün keşfini hızlandırabilir ve fiyat hassas kullanıcıyı hedefe daha çabuk ulaştırabilir.

**Test edilmesi gerekenler**
- Ekleme: İndirim filtresi sepete ekleme davranışını artırıyor mu?
- Hız: Fiyat hassas kullanıcılar ürünü daha hızlı buluyor mu?
- Konum: Filtrenin sayfa üstünde olması diğer filtreleri etkiliyor mu?
- Cihaz: Mobil ve masaüstünde kullanım nasıl farklılaşıyor?
- Karar: Filtre kullanımı artınca karar süresi kısalıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): İndirim filtresi satın almayı artırıyor mu?
- Filtre Kullanım Oranı: Filtre ne kadar kullanılıyor?
- Sepete Ekleme Oranı: Filtreleyenler daha çok ekliyor mu?
- Ortalama Sepet Tutarı: İndirime yönelim sepeti küçültüyor mu?
- Brüt Marj: Düşmemeli; indirimli ürüne kayış kârı eritmemeli.

**Yapılmaması gerekenler**
- Çok fazla filtre ekleyip kullanıcıyı kararsız bırakmayın.
- Tutarsız sonuç veren indirim aralığı tasarlamayın.
- Test süresince filtreyi değiştirmeyin; veri güvenilmez olur.
- Mobilde filtre alanını ekranı kaplayacak kadar büyütmeyin.
- Yalnızca dönüşüme bakıp marj etkisini atlamayın.

---

## Filtreler kaydırma boyunca görünür kalmalı mı?

Filtre panelinin sayfa kaydırılırken ekranda kalması, listenin ortasında fikir değiştiren kullanıcının yukarı dönmesini gerektirmez. Bedeli: panel sürekli yer kaplar, ürünlere kalan alan daralır ve mobilde ekranın önemli bir kısmını yiyebilir.

**Test edilmesi gerekenler**
- Kalıcılık: Filtreler görünür kaldığında filtre kullanımı artıyor mu?
- Alan: Daralan ürün alanı görülen ürün sayısını düşürüyor mu?
- Biçim: Tam panel mi, sadece bir filtre düğmesi mi görünür kalmalı?
- Zamanlama: Panel baştan mı sabit olmalı, kaydırma başlayınca mı belirmeli?
- Cihaz: Mobilde sabit filtre yerine alta yerleşen bir düğme daha mı iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Filtre erişimi satışa dönüyor mu?
- Filtre Kullanım Oranı: Filtre uygulayan kullanıcı oranı artıyor mu?
- Görülen Ürün Sayısı: Daralan alan görülen ürün sayısını kabul edilemez ölçüde düşürmemeli.
- Liste → Ürün Tıklama Oranı: Ürüne geçiş düşmemeli.
- Sıfır Sonuç Oranı: Kolaylaşan filtreleme boş sonuç sayısını artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte filtrenin kalıcılığı ile filtre seçeneklerini birlikte değiştirmeyin.
- Sabit paneli ekranın yarısını kaplayacak boyutta kurmayın.
- Filtre kullanımı arttı diye dönüşüme bakmadan kazandı demeyin.
- Sabit panelin altında kalan içeriği erişilemez bırakmayın.
- Klavye ile gezinirken sabit panelin odak sırasını bozmayın.

---

## Filtreleri açıkta göstermek mi, düğme arkasına almak mı daha iyi çalışıyor?

Filtreleri doğrudan görünür kılmak varlıklarını hatırlatır ve kullanımı artırır. Düğme arkasına almak ise ürünlere daha çok yer bırakır ve sayfayı sadeleştirir; buna karşılık filtrenin varlığından habersiz kullanıcı hiç filtrelemeden gezinir ve doğru ürünü bulamaz.

**Test edilmesi gerekenler**
- Görünürlük: Açıktaki filtreler kullanımı artırıyor mu?
- Farkındalık: Düğme arkasındaki filtreyi kaç kullanıcı açıyor?
- Seçim: Hangi filtreler açıkta durmalı, hangileri gizlenebilir?
- Alan: Açıktaki filtreler ürün alanını ne kadar daraltıyor?
- Cihaz: Masaüstünde açık, mobilde düğme arkası bir düzen daha mı iyi?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Filtre görünürlüğü satışa dönüyor mu?
- Filtre Kullanım Oranı: Filtre uygulayan kullanıcı oranı artıyor mu?
- Aranan Ürüne Ulaşma Süresi: Doğru ürüne ulaşma hızlanıyor mu?
- Görülen Ürün Sayısı: Daralan alan görülen ürün sayısını düşürmemeli.
- Liste Terk Oranı: Kalabalıklaşan sayfa çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte filtre görünürlüğü ile filtre sayısını birlikte değiştirmeyin.
- Açıkta gösterdiğiniz filtreleri kategoriye göre değiştirip testi karıştırmayın.
- Filtre kullanımı arttı diye dönüşüme bakmadan kazandı demeyin.
- Düğme arkasındaki filtreye kaç filtre uygulandığını gösteren işareti kaldırmayın.
- Tek kategoride ölçüp sonucu filtre yapısı çok farklı kategorilere taşımayın.

---

## Arama kelimesini sonuçlarda vurgulamak işe yarar mı?

Aranan kelimenin sonuç başlıklarında işaretlenmesi eşleşmenin nerede olduğunu gösterir ve doğru sonuca ulaşmayı hızlandırır. Riski: vurgu görsel gürültü yaratır, çok sayıda eşleşme olduğunda başlık okunmaz hâle gelir ve alakasız bir eşleşme vurgulandığında arama kalitesizmiş gibi görünür.

**Test edilmesi gerekenler**
- Vurgu: Anahtar kelimeyi işaretlemek sonuç tıklamasını artırıyor mu?
- Yoğunluk: Çok sayıda vurgu okunabilirliği bozuyor mu?
- Kapsam: Vurgu başlıkta mı, açıklamada da mı olmalı?
- Kalite algısı: Zayıf eşleşmenin vurgulanması arama güvenini düşürüyor mu?
- Cihaz: Mobilde kısalan başlıklarda vurgu hâlâ anlamlı mı?

**Takip edilecek ana KPI’lar**
- Arama Sonucu Tıklama Oranı: Sonuçlara tıklama artıyor mu?
- Dönüşüm Oranı (CR): Aramadan satışa giden oran artıyor mu?
- Arama Tekrarı Oranı: Aynı kullanıcının yeniden arama yapması artmamalı.
- Sonuç Terk Oranı: Sonuç sayfasından çıkış artmamalı.
- Erişilebilirlik: Vurgu yalnızca renge dayanmamalı, kontrast korunmalıdır.

**Yapılmaması gerekenler**
- Vurguyu yalnızca renkle yapıp kontrast ve biçim farkını atlamayın.
- Aynı testte vurgu ile sonuç sıralamasını birlikte değiştirmeyin.
- Başlığın yarısını vurgulayacak kadar geniş eşleşme kurmayın.
- Vurguyu arama kalitesini düzeltmenin yerine koymayın; asıl sorun sıralama olabilir.
- Tek kelimelik aramalarda ölçüp sonucu uzun sorgulara genellemeyin.

---

## Filtreleri seçenek listesi yerine cümle hâlinde sormak işe yarar mı?

Filtreleri “kimin için, hangi bütçeyle” gibi bir soru akışına çevirmek, ne aradığını tam bilmeyen kullanıcıyı yönlendirir. Karşı tarafta: ne aradığını bilen kullanıcı için bu fazladan adımdır, akış onu yavaşlatır ve klasik filtreye göre daha az hassas sonuç verir.

**Test edilmesi gerekenler**
- Biçim: Soru akışı klasik filtreden daha çok mu kullanılıyor?
- Kullanıcı tipi: Ne aradığını bilen kullanıcı akışı atlayabiliyor mu?
- Uzunluk: Kaç soru sorulduğunda terk başlıyor?
- Hassasiyet: Akışın ürettiği sonuç kümesi yeterince isabetli mi?
- Segment: Yeni ziyaretçi ile geri dönen kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Soru akışı satışa dönüyor mu?
- Akış Tamamlama Oranı: Soruları bitiren kullanıcı oranı ne kadar?
- Klasik Filtre Kullanımı: Deneyimli kullanıcının filtre erişimi kaybolmamalı.
- Sıfır Sonuç Oranı: Akış sonunda boş sonuç artmamalı.
- Aranan Ürüne Ulaşma Süresi: Toplam süre uzamamalı.

**Yapılmaması gerekenler**
- Soru akışını atlanamaz hâle getirip klasik filtreyi kaldırmayın.
- Aynı testte soru sayısı ile soru içeriğini birlikte değiştirmeyin.
- Akışın sonunda boş sonuç veren kombinasyonları çıkışsız bırakmayın.
- Cevapları sonraki ziyarette kullanıcıya sormadan kalıcı hâle getirmeyin.
- Akış tamamlama arttı diye dönüşüme bakmadan kazandı demeyin.
