# Sepet ve Ödeme

Yolculuk aşaması: kullanıcı satın almaya karar verdi; sepet, kupon, adres/ödeme formları ve tamamlanma anı. Huninin en pahalı kayıp noktası. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## CTA buton rengi dönüşümü etkiler mi?

Değişken: CTA buton rengi · Fark: değiştir

Buton rengi klasik bir test konusudur ama genelde yanlış kurulur: “kırmızı mı yeşil mi daha iyi” evrensel bir cevabı yoktur, sayfanın geri kalan renk paletiyle kontrastı önemlidir. Marka renginden sapan ama sayfada öne çıkan bir renk genelde kazanır — rengin kendisi değil, göze çarpma derecesi test edilir.

**Test edilmesi gerekenler**
- Kontrast: Sayfanın geri kalanına göre en çok öne çıkan renk hangisi?
- Marka tutarlılığı: Marka renginden sapmak dönüşümü artırsa bile marka algısını bozuyor mu?
- Sonraki test: Kazanan renk sabit tutulduğunda butonun üstte ya da altta durması, ayrı bir testte tıklamayı değiştiriyor mu?
- Cihaz: Mobilde ve masaüstünde kazanan renk aynı mı?
- Erişilebilirlik: Seçilen renk kontrast oranı (WCAG) eşiğini geçiyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Renk değişikliği tamamlanan siparişe yansıyor mu?
- Tıklama Oranı (CTR): Tanı metriği; buton daha çok fark edilip tıklanıyor mu?
- Sepete Ekleme Oranı: İlk aksiyon değişiyor mu?
- Sayfa Terk Oranı: Yükselmemeli.
- Marka Algısı (anket): Ölçülüyorsa düşmemeli.

**Yapılmaması gerekenler**
- Aynı testte renk ile buton metnini birlikte değiştirmeyin.
- Erişilebilirlik kontrastını sağlamayan bir renk seçmeyin (görme engelli kullanıcı dışlanır).
- Marka kılavuzuna aykırı rengi test onayı almadan canlıya almayın.
- Tek bir sayfada kazanan rengi tüm siteye otomatik yaymayın; sayfa bağlamı değişir.
- Rengi diğer CTA’lardan (ikincil butonlar) ayırt edilemez hale getirmeyin.

---

## Sepet ve ödeme adımlarında tekrarlayan CTA’ları azaltmak dönüşümü artırır mı?

Değişken: Tekrarlayan CTA sayısı · Fark: kaldır

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
- Terk Oranı: Yükselmemeli.
- Karar Süresi: Belirgin şekilde uzamamalı.

**Yapılmaması gerekenler**
- Tüm CTA’ları birden kaldırmayın; kullanıcı yönsüz kalır.
- Yalnızca tekrarlayan ve işlevsiz CTA’ları çıkarın.
- Aynı testte CTA sayısı ile kalan CTA’nın metnini birlikte değiştirmeyin.
- Mobilde kritik CTA’nın ekran dışına itilmesine izin vermeyin.
- İkincil aksiyonu birincil CTA ile aynı görsel ağırlıkta yapmayın.

---

## Ücretsiz kargo çubuğu sepet tutarını artırıyor mu?

Değişken: Ücretsiz kargo ilerleme çubuğu · Fark: ekle

Ücretsiz kargoya ne kadar kaldığını göstermek, sepeti büyütme motivasyonunu yükseltebilir. Bu etkinin gerçekte ne kadar olduğu ölçülmelidir.

**Test edilmesi gerekenler**
- Motivasyon: Çubuk “ücretsiz kargoya ulaşmak için ürün ekle” davranışını artırıyor mu?
- Fark edilme: Kullanıcılar çubuğu görüp ücretsiz kargoya kalan tutarı doğru okuyor mu?
- Sonraki test: Çubuğun etkisi kanıtlanırsa yeri (sepet / mini sepet / ürün sayfası) ayrı bir testte sepet tutarını değiştiriyor mu?
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
- Eşiğe kalan tutarı gerçek sepet hesabından farklı göstermeyin (kural 6).
- Mobilde çubuğu görünmeyecek kadar aşağı koymayın.
- Aynı testte renk, eşik ve metni birlikte değiştirmeyin.
- Eşiğe ulaşıldığında geri bildirim vermeyi atlamayın.

> **Pazar notu:** Ücretsiz kargo eşiğinin psikolojik ağırlığı pazara göre değişir: kargo ücretinin sepete oranı, teslimat süresi beklentisi ve rakiplerin eşik seviyesi farklı pazarlarda farklıdır. Eşik tutarını başka bir pazarın rakamından kopyalamayın, kendi sepet dağılımınızdan türetin.

---

## Açık kupon kodu alanı sepet terkini artırır mı?

Değişken: Kupon kodu alanının görünürlüğü · Fark: değiştir

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
- Kupon Kullanım Oranı: Kuponu olan kullanıcı alanı bulabilmeli, kullanım çökmemeli.
- Ödeme Adımı Terk Oranı: Doğrudan hedef davranış.
- Kampanya Katılımı: Aktif kampanya performansı çökmemeli.

**Yapılmaması gerekenler**
- Kupon alanını tamamen kaldırmayın; kodu olan kullanıcı öfkelenir.
- Geçersiz kod hatasını belirsiz bırakmayın.
- Kodu olan kullanıcının alanı bulamayıp indirimsiz ödemesini gelir kazancı saymayın.
- Kupon alanını CTA altına gizleyip fark edilmez yapmayın.
- Aynı testte hem konumu hem metni değiştirmeyin.

---

## Üye olmadan ödeme seçeneği işe yarar mı?

Değişken: Misafir ödeme seçeneği · Fark: ekle

Zorunlu üyelik satın alma sürecini uzatır ve terk oranını yükseltebilir. Misafir ödemenin dönüşüme etkisi ölçülmelidir.

**Test edilmesi gerekenler**
- Sonraki test: Misafir seçeneği eklendikten sonra butonunun görsel ağırlığı ayrı bir testte artırılınca tercih oranı yükseliyor mu?
- Kayıt dengesi: Misafir seçeneğinin getirdiği ek sipariş, kaybedilen yeni üye kaydını telafi ediyor mu?
- Cihaz: Mobilde misafir ödeme seçeneği masaüstüne göre daha mı çok tercih ediliyor?
- Kategori: Moda ve hızlı tüketimde misafir ödeme daha mı çok tercih ediliyor?
- Kampanya: Yoğun dönemlerde etki değişiyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Misafir ödeme satın almayı artırıyor mu?
- Sepet Terk Oranı: Üyelik zorunluluğu kalkınca düşüyor mu?
- Checkout Tamamlama Süresi: Süreç kısalıyor mu?
- Kayıt Oranı: Ciddi biçimde düşmemeli.
- Tekrar Satın Alma Oranı: Misafir kullanıcı geri dönmeli.

**Yapılmaması gerekenler**
- Misafir ödemede gereksiz bilgi istemeyin.
- “Üye olmadan devam et” butonunu küçültmeyin veya gizlemeyin.
- Satın alma sonrası kayıt çağrısını agresif tekrar etmeyin.
- Misafir siparişini sonradan hesaba bağlama yolunu kapatmayın.
- Aynı testte hem misafir seçeneğini hem form alanlarını değiştirmeyin.

---

## Tek sayfa checkout mu, çok adımlı checkout mu?

Değişken: Checkout adım yapısı · Fark: değiştir

Tek sayfa akışı toplam tıklamayı azaltır ama ilk bakışta yoğun görünür. Çok adımlı akış daha sindirilebilirdir ama her adım bir kayıp noktasıdır. Sepet tutarına ve cihaza göre kazanan değişebilir.

**Test edilmesi gerekenler**
- Toplam etki: Tek sayfa akışı tamamlama oranını artırıyor mu?
- Cihaz: Tek sayfanın uzun kaydırma gerektirdiği mobilde çok adımlı akış, geniş ekranlı masaüstünde ise tek sayfa akışı mı kazanıyor?
- Sepet tutarı: Yüksek tutarda çok adımlı akış daha mı güven veriyor?
- Sonraki test: Tek sayfa kazanırsa bölümleri katlanabilir yapmak ayrı bir testte yoğunluk algısını azaltıyor mu?
- Segment: Bilgileri kayıtlı dönen kullanıcı tek sayfada, alanları ilk kez dolduran yeni kullanıcı çok adımlı akışta mı daha çok tamamlıyor?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Ödemeye başlayanların bitirme oranı.
- Adım Bazlı Terk Oranı: Hangi alanda kayıp var?
- Checkout Süresi: Toplam süre kısalıyor mu?
- Doğrulama Hatası Oranı: Tek sayfada artmamalı.
- Destek Talebi: Sipariş sorunları yükselmemeli.

**Yapılmaması gerekenler**
- Aynı testte adım yapısı ile ödeme yöntemi setini birlikte değiştirmeyin.
- Tek sayfada tüm alanları aynı anda açıp kullanıcıyı boğmayın.
- Adım göstergesini kaldırıp kullanıcıyı yönsüz bırakmayın.
- Klavye açılınca özet alanı CTA’yı kapatmamalı.
- Kargo ücretini son adıma saklamayın.

---

## Adres formundaki alan sayısını azaltmak tamamlamayı artırır mı?

Değişken: Adres formundaki alan sayısı · Fark: kaldır

Her ek form alanı bir sürtünme noktasıdır. Posta koduyla otomatik il/ilçe doldurma veya adres önerisi kullanmak, mobilde yazma yükünü ciddi biçimde azaltabilir.

**Test edilmesi gerekenler**
- Alan sayısı: Azaltmak tamamlama oranını artırıyor mu?
- Sonraki test: Alan sayısı sabitken adres önerisi ile posta kodundan doldurma ayrı bir testte karşılaştırıldığında hangisi daha hızlı tamamlatıyor?
- Birleştirme: Ad ve soyadı tek alanda toplamak hata oranını artırıyor mu?
- Cihaz: Mobilde etki masaüstünden daha mı yüksek?
- Segment: Kayıtlı adresi olan kullanıcıda fark kalıyor mu?

**Takip edilecek ana KPI’lar**
- Adres Adımı Tamamlama Oranı: Adres adımına ulaşan kullanıcıların (iki kolda aynı tetikleyici) adımı bitirme oranı artıyor mu?
- Ortalama Doldurma Süresi: Kısalıyor mu?
- Sipariş Tamamlama Oranı: Zincirin sonuna yansıyor mu?
- Hatalı Adres / Teslimat Hatası: Artmamalı; en kritik guardrail.
- Destek Talebi: Adres düzeltme talepleri yükselmemeli.

**Yapılmaması gerekenler**
- Otomatik doldurmayı düzenlenemez yapmayın.
- Kargo için gerçekten gereken alanı kaldırmayın; hassas alanlarda önce kural 14’teki ara yöntemleri değerlendirin.
- Aynı testte hem alan sayısını hem validasyon kurallarını değiştirmeyin.
- Hata mesajlarını alan altından kaldırmayın.
- Posta kodundan doldurulan il/ilçeyi kullanıcıya göstermeden siparişe yazmayın.

---

## Adet seçiminin görünürlüğü davranışı etkiliyor mu?

Değişken: Adet seçicinin görünürlüğü · Fark: değiştir

Sepette adet seçimini daha net sunmak, kullanıcıların adedi artırma davranışını ve sepet değerini etkileyebilir.

**Test edilmesi gerekenler**
- Cihaz: Mobilde ve masaüstünde adet artırma davranışı aynı mı?
- Görünürlük: Görünürlük artınca adet artırma davranışı değişiyor mu?
- Buton: “+ / −” butonlarını belirginleştirmek ekleme hızını artırıyor mu?
- Sonraki test: Belirgin adet seçici sabitken alanın satır ortasına alınması ayrı bir testte sepet tutarını yükseltiyor mu?
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

---

## Sepetteki ürün önerileri satın almayı artırır mı?

Değişken: Sepetteki tamamlayıcı ürün önerileri · Fark: ekle

Sepet adımında tamamlayıcı ürün göstermek ortalama sepet tutarını yükseltebilir ama asıl akıştan uzaklaştırma riski taşır.

**Test edilmesi gerekenler**
- Cihaz: Mobil dar ekranda öneri alanı sipariş özetini ve CTA’yı aşağı itiyor mu?
- Etkileşim: Kullanıcılar öneri alanına tıklayıp inceliyor mu?
- Akıştan sapma: Öneri kartına tıklayan kullanıcılar ürün sayfasına gidip sepete geri dönmeden ayrılıyor mu?
- Sayı: Öneri sayısı kaç olmalı? (2 / 4 / 6)
- Sonraki test: Öneri alanı kazanırsa sipariş özetinin üstünde mi altında mı durduğu ayrı bir testte tamamlamayı değiştiriyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Öneriler dönüşümü düşürmeden toplam geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Öneriler sepet değerini yükseltiyor mu?
- Öneriden Sepete Ekleme Oranı: Önerilerden ekleme yapılıyor mu?
- Sipariş Tamamlama Oranı: Öneri alanı akışı bozup tamamlamayı düşürmemeli.
- Öneri Tıklama Oranı: Tanı metriği; kullanıcılar önerilere tıklıyor mu?

**Yapılmaması gerekenler**
- Sepet alanını kalabalıklaştırmayın; asıl akıştan uzaklaştırır.
- Alakasız veya stokta olmayan ürün önermeyin.
- Fiyat ve indirim tutarsızlığı bırakmayın.
- Öneri kartında, eklenince değişecek toplam tutarı veya kargo ücretini gizlemeyin.
- Önerileri “Siparişi Tamamla” butonunun üstüne koymayın.

---

## Kargo eşiğini yükseltmek sepet ortalamasını artırır mı?

Değişken: Ücretsiz kargo eşik tutarı · Fark: değiştir

Ücretsiz kargo sınırı sepeti büyütmek için güçlü bir teşviktir, ancak eşik fazla yükselirse kullanıcıyı kaçırır. Dengenin nerede olduğu ölçülmelidir.

**Test edilmesi gerekenler**
- Eşik: 500, 750 ve 1.000 TL’de davranış nasıl değişiyor?
- Sonraki test: Yeni eşik sabitken eşik bilgisinin ürün sayfasında mı sepette mi duyurulduğu ayrı bir testte sepet tutarını değiştiriyor mu?
- Kampanya: İndirim döneminde eşiğe yaklaşma isteği artıyor mu?
- Segment: Sadık müşteri ile yeni kullanıcı aynı tepkiyi mi veriyor?
- Eşik altı davranış: Sepeti yeni eşiğin hemen altında kalan kullanıcılar ürün ekliyor mu, yoksa siparişi bırakıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Eşik artışı AOV'yi şişirirken toplam geliri düşürmüyor mu?
- Ortalama Sepet Tutarı (AOV): Kullanıcılar eşiğe ulaşmak için daha çok ekliyor mu?
- Dönüşüm Oranı (CR): Eşik değişimi satın almayı düşürüyor mu?
- Ödeme Adımına Geçiş Oranı: Sepetten ödeme adımına geçiş artıyor mu?
- Kargo Maliyeti: Birim başına kargo gideri marjı eritmemeli.

**Yapılmaması gerekenler**
- Eşik yükselişini, sepetteki ürünlerin kargo durumunu habersizce değiştirecek şekilde uygulamayın.
- “Ücretsiz kargo” mesajını yanlış beklenti yaratacak şekilde kurmayın.
- Eşiği aşırı yükseltmeyin; kullanıcıyı kaçırır.
- Aynı testte eşik tutarı ile kalan tutar mesajını birlikte değiştirmeyin.
- Sadece sepet tutarına bakıp kargo maliyetini atlamayın.

> Not: Bu senaryo, “Ücretsiz kargo çubuğu sepet tutarını artırıyor mu?” senaryosuyla ilişkilidir — o çubuğun varlığını, bu ise doğru eşik değerini test eder. İkisini aynı anda değiştirmeyin.

> **Pazar notu:** Kargo maliyetinin sepete oranı ve tüketicinin ücretsiz kargo beklentisi pazara göre değişir; bir pazarda kabul gören eşik artışı, başka bir pazarda doğrudan terke dönüşebilir.

---

## Microcopy kullanıcı davranışını nasıl etkiliyor?

Değişken: Buton altı microcopy metni · Fark: değiştir

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
- Çıkış Oranı: Yanlış microcopy kullanıcıyı kaçırmamalı.
- Adımda Geçirilen Süre: Uzamamalı.

**Yapılmaması gerekenler**
- Yanıltıcı, aşırı iddialı veya baskıcı ifadeler kullanmayın.
- Çok uzun microcopy yazmayın; okunabilirliği düşürür.
- Aynı testte microcopy, fiyat ve görseli birlikte değiştirmeyin.
- Microcopy’i ürünle alakasız kampanya mesajlarıyla doldurmayın.
- Mobilde microcopy alanını ekranı sıkıştıracak şekilde konumlandırmayın.

---

## Kayıtlı kartla hızlı ödeme dönüşümü artırıyor mu?

Değişken: Kayıtlı kartla hızlı ödeme seçeneği · Fark: ekle

Kayıtlı kartla tek tıkla ödeme, veri girişini ortadan kaldırarak süreci hızlandırır ve sürtünmeyi azaltır. Bu kolaylığın dönüşüme ne kadar yansıdığı ölçülmelidir.

**Test edilmesi gerekenler**
- Otomatik gösterim: Kayıtlı kartın otomatik gelmesi tamamlamayı artırıyor mu?
- Benimsenme: Kayıtlı kartı olan kullanıcıların ne kadarı hızlı ödemeyi seçiyor, ne kadarı kartı yine elle giriyor?
- Sonraki test: Hızlı ödeme kazanırsa seçeneğin ödeme adımındaki yeri ayrı bir testte fark edilme oranını değiştiriyor mu?
- Cihaz: Mobilde hızlı ödemenin etkisi masaüstünden daha mı yüksek?
- Sağlayıcı: Kayıtlı-kart cüzdan çözümlerinde etki değişiyor mu?

**Takip edilecek ana KPI’lar**
- Ödeme Tamamlama Oranı: Hızlı ödeme satın almayı artırıyor mu?
- Ödeme Yöntemi Seçim Oranı: Hangi yöntem seçiliyor?
- Adım Tamamlama Süresi: Ödeme adımı kısalıyor mu?
- Hata / Reddedilme Oranı: Artmamalı.
- Sipariş Sonrası İptal: Yükselmemeli.

**Yapılmaması gerekenler**
- Hızlı ödemeyi zorunlu kılmayın; manuel giriş seçeneği kalmalı.
- Görünürlüğü bozacak büyük uyarı kutuları eklemeyin.
- Aynı testte hızlı ödeme ile kart giriş alanlarının tasarımını birlikte değiştirmeyin.
- Mobilde hızlı ödeme kutusunu ekranı sıkıştıracak kadar büyütmeyin.
- Kayıtlı kartı kullanıcı onayı olmadan varsayılan yapmayın.

---

## İlerleme çubuğu tamamlama oranını artırıyor mu?

Değişken: Checkout ilerleme çubuğu · Fark: ekle

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
- Adım Süresi: Adımlar daha hızlı mı tamamlanıyor?
- Geri Dönüş Oranı: Önceki adıma dönüş artmamalı.
- Sayfa Yüklenme Süresi: Çubuk yavaşlatmamalı.

**Yapılmaması gerekenler**
- Gereğinden fazla adım göstermeyin; süreç uzun hissettirir.
- Adım isimlerini teknik veya anlaşılmaz yazmayın.
- Mobilde çubuğa çok fazla ekran alanı ayırmayın.
- Aynı testte çubuğu eklerken funnel adımlarının sayısını birlikte değiştirmeyin.
- Aşırı animasyonlu veya yavaş yüklenen çubuk kullanmayın.

> **Ölçüm notu:** Bu senaryoda ilk adımın tamamlanma oranı neredeyse her zaman yükselir; asıl soru yükselen adımın siparişe dönüp dönmediğidir. Adım metriği testin fotoğrafını çeker, sonucunu değil — birincil metrik huninin sonunda kalır.
---

## Otomatik indirim kodu davranışı nasıl etkiler?

Değişken: İndirim kodunun otomatik uygulanması · Fark: değiştir

İndirim kodunun otomatik uygulanması ödeme sürecini kısaltarak dönüşümü artırabilir. Gerçek karşılığı ölçülmelidir.

**Test edilmesi gerekenler**
- Hız: Otomatik kod ödeme adımına geçişi hızlandırıyor mu?
- Farkındalık: Kampanya farkındalığı tamamlama ile ilişkili mi?
- Cihaz: Kodu kopyalayıp yapıştırmanın zahmetli olduğu mobilde otomatik uygulama, masaüstüne göre tamamlamayı daha çok mu artırıyor?
- Güven: Otomatik uygulandı mesajı güven veriyor mu?
- Kod çakışması: Otomatik kod uygulanmışken kullanıcılar manuel alana ikinci bir kod girmeye çalışıp hata alıyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Otomatik kod, indirim maliyetine rağmen atanan ziyaretçi başına geliri artırıyor mu? Birincil metrik bu; CR tek başına kazanan seçmez.
- Dönüşüm Oranı (CR): Otomatik kod satın almayı artırıyor mu? — RPV ile birlikte okunur.
- Kupon Kullanım Oranı: Otomatik uygulama kullanımı artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Sepet değeri değişiyor mu?
- Brüt Marj: Otomatik indirim marjı eritmemeli.

**Yapılmaması gerekenler**
- Kafa karıştırıcı indirim mesajı göstererek kullanıcıyı şüphelendirmeyin.
- Aynı ekranda birden fazla indirim kodu alanı göstermeyin.
- Kod uygulandı mesajını geciktirmeyin; güveni azaltır.
- Otomatik uygulandı denen indirimi gerçek tutarından farklı göstermeyin veya ödemede sessizce düşürmeyin (kural 6).
- Manuel kod girme yolunu tamamen kapatmayın.

---

## Ödeme adımındaki güven rozetleri tamamlamayı artırır mı?

Değişken: Ödeme adımındaki güven rozeti şeridi · Fark: ekle

Kart bilgisi girilen ekran, terk oranının en yüksek olduğu andır. Güvenli ödeme, iade garantisi ve 3D Secure gibi görsel sinyaller tereddüdü azaltabilir; fazlası ise şüphe uyandırabilir.

**Test edilmesi gerekenler**
- Sonraki test: Rozet şeridi kazanırsa kart alanının üstünde mi altında mı durduğu ayrı bir testte ödeme tamamlamayı değiştiriyor mu?
- Sayı: Kaç rozet optimum? (1 / 3 / 5)
- Fark edilme: Kart bilgisini giren kullanıcılar rozet şeridini fark ediyor mu, oturum kayıtları bunu doğruluyor mu?
- Tereddüt anı: Rozet şeridi, kart numarası alanında duraksayıp sayfadan çıkan kullanıcı oranını azaltıyor mu?
- Segment: İlk kez kart bilgisi giren yeni kullanıcıda rozet şeridi, önceden ödeme yapmış dönen kullanıcıya göre terki daha çok mu azaltıyor?

**Takip edilecek ana KPI’lar**
- Ödeme Tamamlama Oranı: Kart ekranına ulaşanların (iki kolda aynı tetikleyici) ödemeyi bitirme oranı artıyor mu?
- Ödeme Adımı Terk Oranı: Düşüyor mu?
- Adımda Geçirilen Süre: Tereddüt kısalıyor mu?
- Hata / Reddedilme Oranı: Değişmemeli.
- Sipariş Sonrası İptal: Yükselmemeli.

**Yapılmaması gerekenler**
- Gerçekte sahip olmadığınız sertifika rozetlerini göstermeyin.
- Rozetleri CTA’nın önüne geçecek boyutta kullanmayın.
- Çok fazla rozet koyup “fazla ısrarcı” algısı yaratmayın.
- Aynı testte rozetlerin konumu ile sayısını birlikte değiştirmeyin.
- Klavye açılınca rozet şeridi CTA’yı kapatmamalı.

> **Pazar notu:** Hangi sinyalin güven verdiği pazara bağlıdır: bazı pazarlarda banka ve kart doğrulama logoları tanıdık ve rahatlatıcıyken, bazılarında ödeme sağlayıcısı veya bağımsız güvenlik mührü daha güçlü sinyaldir. Rozet setini kendi pazarınızın tanıdığı kurumlardan seçin.

---

## Zorunlu ve isteğe bağlı alanları açıkça işaretlemek doldurma oranını artırır mı?

Değişken: Alanların zorunluluk etiketi · Fark: ekle

Formdaki hangi alanın zorunlu, hangisinin isteğe bağlı olduğu genelde belirsizdir; kullanıcı emin olmadığı alanı da doldurur ya da doldurmayıp hata mesajıyla karşılaşır. İkisini de açıkça işaretlemek bu belirsizliği kaldırabilir.

**Test edilmesi gerekenler**
- Etiket: “(isteğe bağlı)” etiketi eklemek tamamlama süresini/hata oranını düşürüyor mu?
- Kapsam: Sadece isteğe bağlı alanları mı, yoksa zorunlu alanları da yıldızla mı işaretlemeli?
- Sonraki test: Etiket eklemek kazanırsa etiketin alan adının yanında mı, alan içinde mi durduğu ayrı bir testte fark edilmeyi değiştiriyor mu?
- Cihaz: Mobilde dar ekranda etiket yer kaplaması okunabilirliği bozuyor mu?
- Tutarlılık: Formun tamamında aynı işaretleme kuralı uygulandığında etki büyüyor mu?

**Takip edilecek ana KPI’lar**
- Form Tamamlama Oranı: Form adımına atanan kullanıcıların formu gönderme oranı artıyor mu? Birincil metrik.
- Doğrulama Hatası Oranı: Yükselmemeli; yanlış doldurulan/boş bırakılan zorunlu alan azalmalı.
- Ortalama Doldurma Süresi: Kısalıyor mu?
- Alan Bazlı Terk Oranı: Hangi alanda kayıp azalıyor?
- Destek Talebi: Form doldurmayla ilgili talepler artmamalı.

**Yapılmaması gerekenler**
- Etiketleri form doğrulama kurallarıyla aynı testte değiştirmeyin.
- İsteğe bağlı bir alanı arka planda zorunlu tutup öyle işaretlemeyin.
- Etiketi form tasarımının geri kalanıyla tutarsız bir stilde göstermeyin.
- Mobilde etiketi alan metnini kesecek kadar uzun yazmayın.
- Zorunlu bir alanı “isteğe bağlı” diye etiketleyip gönderimde hata vermeyin.

> **Not:** Büyük ölçekli bağımsız checkout kullanılabilirliği araştırmaları, bu işaretlemenin sitelerin yalnızca küçük bir kısmında (ve mobilde daha da az) uygulandığını, buna rağmen düşük maliyetli ve uzun süredir çözülmemiş bir sorun olduğunu gösteriyor.

---

## Ödeme yöntemini adres bilgisinden önce sormak işe yarar mı?

Değişken: Ödeme yöntemi adımının sırası · Fark: taşı

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
- Toplam tutarı ödeme bilgisi alındıktan sonra göstermeyin; gizlenen fiyat kabul edilemez (kural 6).
- Aynı testte adım sırası ile adım sayısını birlikte değiştirmeyin.
- Ödeme güvenlik doğrulamalarını sıralama testinin kapsamına almayın (kural 6).
- Adrese bağlı yöntemleri test öncesi teknik olarak doğrulamadan varyantı açmayın.
- Tamamlama arttı diye ödeme hata oranına bakmadan kazandı demeyin.

---

## Ödeme akışında menü ve bağlantıları kaldırmak tamamlamayı artırır mı?

Değişken: Checkout’taki gezinme bağlantıları · Fark: kaldır

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
- Kullanıcının akıştan çıkmasını tamamen engelleyen bir tasarım kurmayın (kural 6).
- Yasal olarak bulunması gereken bağlantıları (mesafeli satış, iade, gizlilik) kaldırmayın.
- Aynı testte bağlantı temizliği ile adım sayısını birlikte değiştirmeyin.
- Güven rozetlerini ve iletişim bilgisini dikkat dağıtıcı sayıp birlikte kaldırmayın.
- Sepeti düzenleme yolunu kapatıp tamamlama artışını kazanç saymayın.

---

## Seçimi onaylayan geri bildirim vermek hatayı azaltır mı?

Değişken: Seçim onayı geri bildirimi · Fark: ekle

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
- İade Oranı: Yanlış seçim kaynaklı iade artmamalı.
- Erişilebilirlik: Onay yalnızca renkle verilmemeli, ekran okuyucuya duyurusuz kalmamalı.

**Yapılmaması gerekenler**
- Onayı yalnızca renk değişimiyle verip başka bir işaret bırakmayın.
- Beliren onayın sayfayı zıplatmasına izin vermeyin.
- Aynı testte onay biçimi ile seçim öğesinin tasarımını birlikte değiştirmeyin.
- Onay mesajını, seçim gerçekte kaydedilmeden göstermeyin.
- Hata azaldı diye tamamlama oranına bakmadan kazandı demeyin.

---

## Varsayılan olarak işaretli gelen seçenekler kabul edilebilir mi?

Değişken: Tarafsız seçeneğin varsayılan seçimi · Fark: değiştir

Bir kutunun önceden işaretli gelmesi kullanıcıyı hızlandırabilir, ama bu tekniğin sınırı nettir: pazarlama izni, veri paylaşımı ve ek ücretli hizmetler önceden işaretlenemez; birçok pazarda bu yasaktır ve kullanıcının açık iradesi gerekir. Test edilebilir olan yalnızca tarafsız tercihlerdir (teslimat günü, kargo yöntemi, adet).

**Test edilmesi gerekenler**
- Varsayılan: Tarafsız bir seçeneğin önceden seçili gelmesi tamamlamayı artırıyor mu?
- Doğruluk: Varsayılan çoğu kullanıcı için gerçekten doğru mu?
- Farkındalık: Kullanıcı varsayılanı fark edip değiştirebiliyor mu?
- Değiştirme oranı: Varsayılanı değiştirenlerin oranı ne kadar?
- Segment: Farklı kullanıcı tipleri için farklı varsayılan mı doğru?

**Takip edilecek ana KPI’lar**
- Sipariş Tamamlama Oranı: Varsayılan tamamlamayı artırıyor mu?
- Varsayılan Değiştirme Oranı: Yüksek değiştirme oranı yanlış varsayılana işarettir.
- İade veya İptal Oranı: İstenmeyen seçim kaynaklı iptal artmamalı.
- Destek Talebi: “Bunu ben seçmedim” türü talepler artmamalı.
- Ziyaretçi Başına Gelir (RPV): Gelir düşmemeli.

**Yapılmaması gerekenler**
- Pazarlama izni, veri paylaşımı veya ek ücretli hizmeti önceden işaretli getirmeyin; bu bir test değişkeni değildir (kural 6).
- Kullanıcının ödeyeceği tutarı artıran bir seçeneği varsayılan yapmayın.
- Varsayılanı fark edilmeyecek kadar silik göstermeyin.
- Aynı testte varsayılan ile seçeneklerin sırasını birlikte değiştirmeyin.
- Hedef pazarın izin kurallarını doğrulamadan varyant kurmayın (kural 11).

---

## Ödeme işlenirken adımları gösteren bir yükleme ekranı güveni artırıyor mu?

Değişken: Ödeme yükleme ekranının biçimi · Fark: değiştir

Tek bir dönen ikon, arka planda ne olduğu hakkında hiçbir şey söylemez ve bekleme süresini belirsiz hissettirir. “Kart doğrulanıyor”, “banka onayı bekleniyor”, “sipariş oluşturuluyor” gibi gerçek adımları sırayla göstermek, işlemin özenle yapıldığını hissettirip aynı bekleme süresini daha kısa algılatabilir — görünür emek, güven inşa eder. Risk, adımların gerçek işlem sırasını yansıtmaması veya süreyi yapay olarak uzatmak için kullanılmasıdır.

**Test edilmesi gerekenler**
- Biçim: Adım adım ilerleyen bir yükleme ekranı tek bir dönen ikona göre terk oranını düşürüyor mu?
- Süre algısı: Adımlı ekran, gerçek süre değişmeden bekleme süresini daha kısa hissettiriyor mu?
- Doğruluk: Gösterilen adımlar gerçek işlem sırasına mı uyuyor?
- Hata anı: İşlem başarısız olursa adımlı ekran hatayı daha mı anlaşılır kılıyor?
- Cihaz: Mobilde yavaş bağlantıda adımlı ekranın etkisi masaüstünden farklı mı?

**Takip edilecek ana KPI’lar**
- Ödeme Adımı Terk Oranı: Adımlı ekran bekleme sırasında ayrılan kullanıcı oranını düşürüyor mu?
- Algılanan Süre (anket): Kullanıcı bekleme süresini kısa mı buluyor?
- Gerçek İşlem Süresi: Adımlı ekran gerçek işlem süresini uzatmamalı.
- Hata Sonrası Destek Talebi: Başarısız işlemlerde destek talebi artmamalı.
- Ödeme Başarı Oranı: Genel ödeme tamamlama oranı düşmemeli.

**Yapılmaması gerekenler**
- Gerçek işlemi yapay olarak yavaşlatıp adımları uzatmayın — gösterilen süre gerçek işlem süresini aşarsa bu manipülasyondur (kural 6).
- Gerçekleşmeyen bir adımı (ör. çalışmayan bir “dolandırıcılık taraması”) ekrana koymayın.
- Aynı testte yükleme ekranı biçimi ile ödeme akışının adım sayısını birlikte değiştirmeyin.
- Hata durumunda kullanıcıyı adımlı ekranda takılı bırakmayın; başarısızlık anında net bir hata mesajına geçin.
- Yükleme ekranını güvenlik doğrulamasını (3D Secure, OTP vb.) atlatma veya gizleme amacıyla kullanmayın.

---

## Ödeme yöntemi ikonlarını checkout’tan önce görünür yapmak güveni artırır mı?

Değişken: Checkout öncesi ödeme yöntemi ikonları · Fark: ekle

Kullanıcı ödeme adımına gelmeden önce hangi kartların veya yöntemlerin kabul edildiğini bilmek ister; bu bilgi genelde yalnızca ödeme sayfasında ortaya çıkar. İkonları daha erken (ürün sayfası veya sepette) göstermek, desteklenmeyen bir yöntemi kullanan ziyaretçinin akışı erkenden terk etmesini önleyebilir — ama fazla ikon görsel gürültü yaratabilir.

**Test edilmesi gerekenler**
- Sonraki test: İkonların erken gösterimi kazanırsa ürün sayfası ile sepet ayrı bir testte karşılaştırıldığında hangisi ödeme adımına ulaşmayı daha çok artırıyor?
- Sayı: Tüm yöntemler mi, yalnızca en çok kullanılan 3-4’ü mü daha iyi çalışıyor?
- Terkin yer değiştirmesi: Desteklenmeyen yöntemi kullanan ziyaretçi artık sepette mi ayrılıyor, yani terk yalnızca öne mi kayıyor?
- Sepet tutarı: Yüksek tutarlı sepetlerde kabul edilen kartları erken görmek ödeme adımına geçişi daha çok artırıyor mu?
- Cihaz: Mobilde ikon şeridi ekran alanını gereğinden fazla mı kaplıyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Ürün sayfası veya sepete atanan ziyaretçilerin siparişi tamamlama oranı artıyor mu?
- Ödeme Adımına Geçiş Oranı: Tanı metriği; sepete ulaşan ziyaretçilerin (ikonları görenler değil) ödeme adımına geçme oranı artıyor mu?
- Ödeme Adımı Terk Oranı: Desteklenmeyen yöntem yüzünden son adımda terk azalıyor mu?
- Sepete Ekleme Oranı: İkonlar erken adımı olumsuz etkilememeli.
- Sayfa Yüklenme Süresi: Ek görsel sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Gerçekte kabul etmediğiniz bir ödeme yöntemini ikon olarak göstermeyin.
- Aynı testte ikonların konumunu ve sayısını birlikte değiştirmeyin.
- İkon şeridini asıl ürün bilgisi veya CTA’nın önüne geçirip hiyerarşiyi bozmayın.
- Ödeme sağlayıcı marka kurallarına uymayan boyutta veya biçimde logo kullanmayın.
- Mobilde ikonları okunmaz derecede küçültüp yalnızca dekoratif hâle getirmeyin.
