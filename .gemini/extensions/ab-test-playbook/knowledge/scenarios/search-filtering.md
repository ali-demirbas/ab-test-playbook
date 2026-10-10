# Arama ve Filtreleme

Yolculuk aşaması: kullanıcı ne istediğini biliyor veya keşfediyor; arama kutusu, filtreler, sonuç sayfası ve site içi navigasyon menüleri (sticky/mega menü senaryoları da bu dosyadadır). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Filtreler anında mı, toplu mu uygulanmalı?

Değişken: Filtre uygulama biçimi · Fark: değiştir

Anında filtreleme hızlı geri bildirim verir; toplu filtreleme daha kontrollü bir deneyim sunar. Hangisinin keşif ve dönüşümde daha iyi çalıştığı ölçülmelidir.

**Test edilmesi gerekenler**
- Hız algısı: Anında sonuç göstermek daha akıcı bir deneyim sunuyor mu?
- Kontrol hissi: Toplu filtreleme hatalı seçimleri azaltıyor mu?
- Performans: Sık yenileme sayfa hızını düşürüyor mu?
- Dönüşüm: Hangi model daha yüksek satın alma oranı sağlıyor?
- Cihaz: Filtrenin tam ekran panelde açıldığı mobilde toplu, sonuçların yanda canlı göründüğü masaüstünde ise anında uygulama mı kazanıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Hangi filtre modeli daha çok satış getiriyor?
- Filtre Kullanım Oranı: Hangi modelde daha çok filtre uygulanıyor?
- Keşif Derinliği: Daha fazla ürün görüntüleniyor mu?
- Sayfa Yenileme Süresi: Site hızı bozulmamalı.
- Sıfır Sonuç Oranı: Toplu uygulamada birbirini dışlayan seçimler boş sonuç ekranını artırmamalı.

**Yapılmaması gerekenler**
- Anında filtrelemede her tıklamada sayfayı en üste kaydırıp kullanıcının yerini kaybettirmeyin.
- Filtre sonrası gereksiz animasyon ve geçiş koymayın; performansı düşürür.
- Seçili filtrelerin görünmediği veya kaybolduğu durumlar bırakmayın.
- Aynı testte hem filtre modelini hem filtre setini değiştirmeyin.
- Çok agresif otomatik yenileme kullanmayın; kullanıcıyı yorar.

---

## Arama çubuğu ne kadar görünür olmalı?

Değişken: Arama alanının görünürlük düzeyi · Fark: değiştir

Arama çubuğunun konumu ve görünürlüğü, kullanıcının ürün keşif davranışını değiştirebilir. Bunun dönüşüme yansıyıp yansımadığı ölçülmelidir.

**Test edilmesi gerekenler**
- Konum: Header’da mı, menü içinde mi, yalnızca ikon olarak mı?
- Görünürlük: Açık arama alanı mı, sadece ikon mu daha çok tıklanıyor?
- Sonraki test: Kazanan görünürlük sabitken placeholder metni (“Ürün ara…” / “Favori markanı yaz”) ayrı bir testte arama başlatmayı artırıyor mu?
- Menü etkisi: Arama alanı öne çıkınca kategori menüsüyle gezinme azalıyor mu, yani arama menünün yerini mi alıyor?
- Cihaz: Mobilde ve masaüstünde görünürlük ihtiyacı aynı mı?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Arama yapanların satın alma oranı artıyor mu?
- Arama Kullanım Oranı: Görünürlük arama kullanımını artırıyor mu?
- Arama Sonucu Tıklama Oranı: Doğru ürüne daha hızlı ulaşılıyor mu?
- Arama Başarı Oranı: Düşmemeli; sonuçsuz arama artmamalı.
- Sayfada Kalma Süresi: Keşif derinleşiyor mu?

**Yapılmaması gerekenler**
- Arama kullanımı yüksek bir sitede menü-içi kolu teste hiç sokmayın; o kol ancak arama payı düşükse denenir.
- Aynı testte arama alanının görünürlüğünü değiştirirken placeholder metnini de değiştirmeyin.
- İkon varyantında ikonu etiketsiz ve tanınmayan bir simgeyle göstermeyin.
- Mobilde arama ikonunu tıklanamayacak kadar küçültmeyin.
- Sonuçsuz aramada kullanıcıyı boş ekranda bırakmayın.

---

## Arama kutusundaki önceki arama önerilerini kaldırmak dönüşümü etkiliyor mu?

Değişken: Önceki arama önerileri · Fark: kaldır

Arama kutusu açıldığında önceki aramaları varsayılan öneri olarak listelemek aramaya başlamayı hızlandırır ama kullanıcıyı eski aramalarına geri çeker. Bu varsayılan öneri listesini kaldırmak (geçmişe erişim ayrı bir bağlantıda kalır) keşif sürecini ve karar hızını değiştirebilir.

**Test edilmesi gerekenler**
- Hız: Varsayılan öneri varken aramaya daha hızlı başlanıyor mu?
- Keşif: Otomatik doldurmamak yeni içerik keşfini artırıyor mu?
- Boş kutu: Boş arama kutusu popüler kategorilere yönlendiriyor mu?
- Cihaz: Mobilde klavye açıkken öneri listesi ekranın ne kadarını kaplıyor ve kullanımı değiştiriyor mu?
- Geçmiş: Önceki aramalar varsayılan listeden kalkınca geçmişini arayan kullanıcıdan şikâyet geliyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Arama sonrası satın alma nasıl değişiyor?
- Arama Kullanım Oranı: Arama yapmaya başlama artıyor mu?
- İlk Sonuca Ulaşma Süresi: Kullanıcı daha hızlı ulaşıyor mu?
- Sıfır Sonuç Oranı: Artmamalı.
- Keşif Derinliği: Yeni kategori görüntüleme artıyor mu?

**Yapılmaması gerekenler**
- Önceki aramaları tamamen kaldırmayın; kullanıcı geçmişe erişebilmeli.
- Otomatik doldurulan eski aramayı kullanıcı silmeden yeni aramaya eklemeyin.
- Aynı testte önceki arama önerilerini kaldırırken popüler arama veya kategori önerilerini de değiştirmeyin.
- Otomatik önerileri tümden kapatıp kullanıcıyı yönsüz bırakmayın.
- Başka kullanıcıların hassas aramalarını popüler öneri olarak göstermeyin.

---

## Sıfır sonuç sayfası kullanıcıyı elde tutuyor mu?

Değişken: Sıfır sonuç ekranındaki öneri blokları · Fark: ekle

Sonuç bulunamayan arama, terk oranı en yüksek ekranlardan biridir. Boş bir ekran yerine yazım önerisi, popüler kategoriler ve benzer ürünler sunmak bu trafiği kurtarabilir.

**Test edilmesi gerekenler**
- Öneri: Yazım önerisi kurtarma oranını ne kadar artırıyor?
- Sonraki test: Öneri blokları kazanırsa, ürün bloğunda benzer ürün yerine çok satan ürün göstermek ayrı bir testte kurtarma oranını artırıyor mu?
- Yeniden arama: Öneri blokları eklenince kullanıcı yeniden arama yapmak yerine önerilere mi yöneliyor?
- Alaka: Öneri bloğundan tıklanan ürün sayfasında kullanıcı kalıyor mu, yoksa alakasız bulup hemen geri mi dönüyor?
- Cihaz: Mobilde ve masaüstünde davranış farklı mı?

**Takip edilecek ana KPI’lar**
- Sıfır Sonuç Sonrası Satın Alma Oranı: Sıfır sonuçlu aramaya düşen oturumların (iki kolda aynı tetikleyici) satın almayla bitme oranı artıyor mu?
- Sıfır Sonuç Kurtarma Oranı: Tanı metriği; ürün sayfasına geçen kullanıcı oranı.
- Oturum Devam Oranı: Siteden çıkılmıyor mu?
- Arama Dönüşüm Oranı (CR): Toplam performans düşmemeli.
- Sayfa Yüklenme Süresi: Öneri blokları yavaşlatmamalı.

**Yapılmaması gerekenler**
- Alakasız ürün önerip kullanıcıyı yanıltmayın.
- Aynı testte öneri bloklarını eklerken arama kutusunun yerini veya sıfır sonuç mesajını da değiştirmeyin.
- Sıfır sonuç sayfasını sadece kampanya alanına çevirmeyin.
- Öneri bloklarını arama kutusunun üstüne yerleştirip yeniden aramayı zorlaştırmayın.
- Yazım önerisini otomatik uygulayıp kullanıcıyı şaşırtmayın.

---

## Arama sonuçlarında varsayılan sıralama ne olmalı?

Değişken: Arama sonuçlarının varsayılan sıralaması · Fark: değiştir

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
- Ortalama Sepet Tutarı (AOV): Ucuza kayarsa AOV düşebilir.
- Sıfır Etkileşimli Arama: Artmamalı.

**Yapılmaması gerekenler**
- Sıralama seçeneklerini test sırasında gizlemeyin.
- Stokta olmayan ürünleri üst sıraya taşımayın.
- Aynı testte hem sıralamayı hem filtre setini değiştirmeyin.
- Sponsorlu ürünleri organik sonuç gibi göstermeyin.
- Varsayılan sıralamayı, etiketinde yazan ölçütten (“Önerilen”, “Çok satan”) farklı bir kurala göre dizmeyin.

---

## Sticky menü deneyimi iyileştiriyor mu?

Değişken: Menünün kaydırmada sabit kalması · Fark: değiştir

Menünün sabit kalması sayfa içi gezinme hızını artırabilir, ancak ekran alanı kaplayarak rahatsız da edebilir.

**Test edilmesi gerekenler**
- Gezinme: Sticky menü sayfa içi gezinmeyi kolaylaştırıyor mu?
- Kaydırma: Yukarı çıkma zorunluluğunu ortadan kaldırıyor mu?
- Mobil: Uzun sayfalarda gezinme performansını artırıyor mu?
- Alan: Ekran alanını kaplaması rahatsız ediyor mu?
- Sonraki test: Sabit menü kazanırsa, mobilde ekranın üstüne mi altına mı sabitlendiği ayrı bir testte menü kullanımını değiştiriyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sticky menü satın almayı artırıyor mu?
- Menü Tıklama Oranı: Menü daha çok kullanılıyor mu?
- Sayfa Başına Görüntüleme: Oturumda daha çok sayfa geziliyor mu?
- Kaydırma Derinliği: İçerik okuma engelleniyor mu?
- Çıkış Oranı: Yükselmemeli; menü kullanıcıyı kaçırmamalı.

**Yapılmaması gerekenler**
- Sticky menüyü ekranın büyük bölümünü kaplayacak kadar yüksek yapmayın.
- Mobilde menünün CTA ve filtreleri kapatmasına izin vermeyin.
- Aynı testte menüyü sabitlerken menü öğelerini veya sırasını da değiştirmeyin.
- Sticky menüyü kaydırma yönüne göre sürekli gizleyip gösterip titremeye yol açmayın.
- Menü sabitlenirken sayfa kaymasına yol açmayın.

---

## Mega menü mü, yatay menü mü?

Değişken: Ana menünün yapısı · Fark: değiştir

Mega menü mü, sade yatay menü mü daha iyi gezinme sunuyor? Yapıdaki fark, içerik keşif davranışını ciddi biçimde değiştirebilir.

**Test edilmesi gerekenler**
- Hız: Hangi menü aranan içeriğe daha hızlı ulaştırıyor?
- Çıkış: Menü türü hemen çıkma oranını değiştiriyor mu?
- Süre: Menüde geçirilen süre artıyor mu, azalıyor mu?
- Yönlendirme: Menü kritik içeriğe yönlendirmeyi etkiliyor mu?
- Mobil: İki yapı arasındaki fark mobilde büyüyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Menü yapısı satın almaya giden gezinmeyi değiştiriyor mu?
- Alt Kategoriye Doğrudan İniş Oranı: Menüden tek adımda alt kategoriye geçenlerin payı değişiyor mu?
- Menüden Kategoriye Geçiş Oranı: Menüyü açanların kaçı bir kategoriye iniyor?
- Seçimsiz Kapatılan Menü Oranı: Artmamalı; kullanıcı menüde kaybolmamalı.
- Hemen Çıkma Oranı: Yükselmemeli; menü yapısı kullanıcıyı kaçırmamalı.

**Yapılmaması gerekenler**
- Yatay menü varyantında mega menüdeki alt kategorileri erişilemez bırakmayın; ikinci seviyeye bir yol kalmalı.
- Mega menüde çok fazla kategori sunmayın; bilgi yükü yaratır.
- Mobilde yatay menüde kaydırma sorununa izin vermeyin.
- Mega menüde kolon sayısını taranamayacak kadar artırmayın.
- Aynı testte menü yapısını değiştirirken kategori adlarını veya sırasını da değiştirmeyin.

---

## Menü sadeleştirmesi deneyimi etkiler mi?

Değişken: Menüdeki alt başlık sayısı · Fark: kaldır

Menüyü sadeleştirmek navigasyon hızını ve kategori keşfini etkileyebilir. Daha az karmaşık menü odaklanmayı kolaylaştırabilir.

**Test edilmesi gerekenler**
- Sadelik: Alt başlık sayısını azaltmak odaklanmayı kolaylaştırıyor mu?
- Hız: Sade menü aranan kategoriye daha hızlı ulaştırıyor mu?
- Cihaz: Mobil menüde sadeleştirmenin etkisi masaüstündekinden büyük mü?
- Süre: Navigasyon süresi anlamlı kısalıyor mu?
- Keşif: Sadeleşince keşfedilen kategori sayısı düşüyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Sade menü satın almayı artırıyor mu?
- İlk Tıklama Süresi: Doğru kategoriye ulaşma kısalıyor mu?
- Menü Tıklama Derinliği: Daha az adımda hedefe varılıyor mu?
- Kategori Kapsama Oranı: Düşmemeli; keşfedilen kategori sayısı daralmamalı.
- Arama Kullanım Oranı: Menü yetersiz kalıp aramaya mı itiyor?

**Yapılmaması gerekenler**
- Ana kategorileri tamamen kaldırmayın; bilgi kaybı hissi yaratır.
- Alt başlıkları aşırı azaltıp keşfi kısıtlamayın.
- Kaldırılan alt başlıklara giden eski bağlantıları yönlendirmesiz bırakmayın.
- Mobilde sticky menünün kritik alanları kapatmasına izin vermeyin.
- Aynı testte alt başlıkları azaltırken kalan başlıkların adını veya sırasını da değiştirmeyin.

---

## İndirim filtresi davranışı nasıl etkiler?

Değişken: İndirim oranı filtresi · Fark: ekle

İndirim yüzdesine göre filtreleme sunmak ürün keşfini hızlandırabilir ve fiyat hassas kullanıcıyı hedefe daha çabuk ulaştırabilir.

**Test edilmesi gerekenler**
- Ekleme: İndirim filtresi sepete ekleme davranışını artırıyor mu?
- Hız: Fiyat hassas kullanıcılar ürünü daha hızlı buluyor mu?
- Komşu filtreler: İndirim filtresi eklenince fiyat aralığı filtresinin kullanımı azalıyor mu, biri diğerinin yerini mi alıyor?
- Cihaz: Mobil ve masaüstünde kullanım nasıl farklılaşıyor?
- Karar: Filtre kullanımı artınca karar süresi kısalıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İndirim filtresi geliri artırıyor mu? Birincil karar bu metrikle verilir.
- Dönüşüm Oranı (CR): İndirim filtresi satın almayı artırıyor mu?
- Sepete Ekleme Oranı: Filtreleyenler daha çok ekliyor mu?
- Ortalama Sepet Tutarı (AOV): İndirime yönelim sepeti küçültüyor mu?
- Brüt Marj: Düşmemeli; indirimli ürüne kayış kârı eritmemeli.

**Yapılmaması gerekenler**
- Çok fazla filtre ekleyip kullanıcıyı kararsız bırakmayın.
- Tutarsız sonuç veren indirim aralığı tasarlamayın.
- Uydurma referans fiyattan hesaplanan indirim oranını filtreye dahil etmeyin; filtre yalnızca gerçek indirimi göstermeli (kural 6).
- Mobilde filtre alanını ekranı kaplayacak kadar büyütmeyin.
- Aynı testte indirim filtresini eklerken varsayılan sıralamayı veya diğer filtrelerin sırasını da değiştirmeyin.

---

## Filtreler kaydırma boyunca görünür kalmalı mı?

Değişken: Filtre panelinin kaydırmada sabit kalması · Fark: değiştir

Filtre panelinin sayfa kaydırılırken ekranda kalması, listenin ortasında fikir değiştiren kullanıcının yukarı dönmesini gerektirmez. Bedeli: panel sürekli yer kaplar, ürünlere kalan alan daralır ve mobilde ekranın önemli bir kısmını yiyebilir.

**Test edilmesi gerekenler**
- Kalıcılık: Filtreler görünür kaldığında filtre kullanımı artıyor mu?
- Alan: Daralan ürün alanı görülen ürün sayısını düşürüyor mu?
- Sonraki test: Sabit kalma kazanırsa, tam panel yerine yalnızca bir filtre düğmesinin sabit kalması ayrı bir testte ürün alanını geri kazandırıyor mu?
- Liste ortası: Listenin ortasında filtre değiştiren kullanıcı oranı sabit panelde artıyor mu?
- Cihaz: Sabit panelin filtre kullanımına etkisi masaüstünde mi, mobilde mi daha büyük?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Filtre erişimi satışa dönüyor mu?
- Filtre Kullanım Oranı: Filtre uygulayan kullanıcı oranı artıyor mu?
- Görülen Ürün Sayısı: Daralan alan görülen ürün sayısını kabul edilemez ölçüde düşürmemeli.
- Liste → Ürün Tıklama Oranı: Ürüne geçiş düşmemeli.
- Sıfır Sonuç Oranı: Kolaylaşan filtreleme boş sonuç sayısını artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte filtrenin kalıcılığı ile filtre seçeneklerini birlikte değiştirmeyin.
- Sabit paneli ekranın yarısını kaplayacak boyutta kurmayın.
- Mobilde sabit paneli, tek dokunuşla daraltılamayan bir blok olarak bırakmayın.
- Sabit panelin altında kalan içeriği erişilemez bırakmayın.
- Klavye ile gezinirken sabit panelin odak sırasını bozmayın.

---

## Filtreleri açıkta göstermek mi, düğme arkasına almak mı daha iyi çalışıyor?

Değişken: Filtrelerin görünürlüğü · Fark: değiştir

Filtreleri doğrudan görünür kılmak varlıklarını hatırlatır ve kullanımı artırır. Düğme arkasına almak ise ürünlere daha çok yer bırakır ve sayfayı sadeleştirir; buna karşılık filtrenin varlığından habersiz kullanıcı hiç filtrelemeden gezinir ve doğru ürünü bulamaz.

**Test edilmesi gerekenler**
- Görünürlük: Açıktaki filtreler kullanımı artırıyor mu?
- Farkındalık: Düğme arkasındaki filtreyi kaç kullanıcı açıyor?
- Sonraki test: Açık düzen kazanırsa, yalnızca en çok kullanılan filtreleri açıkta bırakıp gerisini düğme arkasına almak ayrı bir testte liste terkini azaltıyor mu?
- Alan: Açıktaki filtreler ürün alanını ne kadar daraltıyor?
- Cihaz: Masaüstünde açık, mobilde düğme arkası bir düzen daha mı iyi?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Filtre görünürlüğü satışa dönüyor mu?
- Filtre Kullanım Oranı: Filtre uygulayan kullanıcı oranı artıyor mu?
- Aranan Ürüne Ulaşma Süresi: Doğru ürüne ulaşma hızlanıyor mu?
- Görülen Ürün Sayısı: Daralan alan görülen ürün sayısını düşürmemeli.
- Sayfa Yüklenme Süresi: Açıktaki filtre paneli ve seçenek sayıları listenin yüklenmesini (LCP) geciktirmemeli.

**Yapılmaması gerekenler**
- Aynı testte filtre görünürlüğü ile filtre sayısını birlikte değiştirmeyin.
- Açıkta gösterdiğiniz filtreleri kategoriye göre değiştirip testi karıştırmayın.
- Açık düzende filtre panelini, ilk ürün satırını ilk ekranın dışına itecek kadar uzatmayın.
- Düğme arkasındaki filtreye kaç filtre uygulandığını gösteren işareti kaldırmayın.
- Tek kategoride ölçüp sonucu filtre yapısı çok farklı kategorilere taşımayın.

---

## Arama kelimesini sonuçlarda vurgulamak işe yarar mı?

Değişken: Aranan kelimenin sonuçlarda vurgulanması · Fark: ekle

Aranan kelimenin sonuç başlıklarında işaretlenmesi eşleşmenin nerede olduğunu gösterir ve doğru sonuca ulaşmayı hızlandırır. Riski: vurgu görsel gürültü yaratır, çok sayıda eşleşme olduğunda başlık okunmaz hâle gelir ve alakasız bir eşleşme vurgulandığında arama kalitesizmiş gibi görünür.

**Test edilmesi gerekenler**
- Vurgu: Anahtar kelimeyi işaretlemek sonuç tıklamasını artırıyor mu?
- Yoğunluk: Çok sayıda vurgu okunabilirliği bozuyor mu?
- Kapsam: Vurgu başlıkta mı, açıklamada da mı olmalı?
- Kalite algısı: Zayıf eşleşmenin vurgulanması arama güvenini düşürüyor mu?
- Cihaz: Mobilde kısalan başlıklarda vurgu hâlâ anlamlı mı?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Aramadan satışa giden oran artıyor mu?
- Arama Sonucu Tıklama Oranı: Tanı metriği; sonuçlara tıklama artıyor mu?
- Arama Tekrarı Oranı: Aynı kullanıcının yeniden arama yapması artmamalı.
- Geri Dönüş Oranı: Vurgulanan zayıf eşleşmeye tıklayıp ürün sayfasından hemen sonuçlara dönenler artmamalı.
- Erişilebilirlik: Vurgu yalnızca renge dayanmamalı, kontrast korunmalıdır.

**Yapılmaması gerekenler**
- Vurguyu yalnızca renkle yapıp kontrast ve biçim farkını atlamayın.
- Aynı testte vurgu ile sonuç sıralamasını birlikte değiştirmeyin.
- Başlığın yarısını vurgulayacak kadar geniş eşleşme kurmayın.
- Vurguyu arama kalitesini düzeltmenin yerine koymayın; asıl sorun sıralama olabilir.
- Tek kelimelik aramalarda ölçüp sonucu uzun sorgulara genellemeyin.

---

## Filtreleri seçenek listesi yerine cümle hâlinde sormak işe yarar mı?

Değişken: Filtrelerin sorulma biçimi · Fark: değiştir

Filtreleri “kimin için, hangi bütçeyle” gibi bir soru akışına çevirmek, ne aradığını tam bilmeyen kullanıcıyı yönlendirir. Karşı tarafta: ne aradığını bilen kullanıcı için bu fazladan adımdır, akış onu yavaşlatır ve klasik filtreye göre daha az hassas sonuç verir.

**Test edilmesi gerekenler**
- Biçim: Soru akışı klasik filtreden daha çok mu kullanılıyor?
- Kullanıcı tipi: Ne aradığını bilen kullanıcı akışı atlayabiliyor mu?
- Uzunluk: Kaç soru sorulduğunda terk başlıyor?
- Hassasiyet: Akışın ürettiği sonuç kümesi yeterince isabetli mi?
- Segment: Kataloğu ilk kez gören yeni ziyaretçi, ürünleri tanıyan dönen kullanıcıya göre soru akışından daha mı isabetli sonuç buluyor?

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
- Akışın getirdiği sonuç kümesinde hangi cevapların uygulandığını gizlemeyin; kullanıcı her birini tek tek geri alabilmeli.
