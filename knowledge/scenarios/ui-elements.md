# Buton, bağlantı ve arayüz öğeleri

Yolculuk aşaması: sayfaya değil öğeye bağlı kararlar. Bir butonun ne dediği, bir bağlantının nasıl davrandığı, bir ikonun etiketli olup olmadığı her sayfada karşınıza çıkar; bu yüzden ayrı bir dosyada toplanmıştır. Buton rengi ve CTA sayısı `cart-checkout.md`, CTA tekrarı `home-landing.md`, ürün sayfasındaki satın alma butonu `product-detail.md` içindedir.

**Bir uyarı.** Bu dosyadaki değişikliklerin çoğu etki sıralamasının alt kademesindedir (`knowledge/methodology.md` → Fikir üretme merceği): daha yüksek kademeden bir aday varken bunlar birinci sıraya konmaz. Yasak değildir — buradaki bir senaryo, sayfada gözlemlenebilen bir kullanıcı engeline dayanan güçlü bir mekanizmaya sahipse önerilir (ör. kontrastı yetersiz olduğu için gerçekten görülmeyen bir buton). Mekanizması “daha dikkat çekici olur” seviyesinde kalıyorsa önerilmez. Düşük trafikli sayfada bu testler ölçülemeyecek kadar küçük fark arar; orada daha yapısal bir değişiklik tercih edilir (`methodology.md` → Uygunluk tablosu). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Buton metni eylemi mi, kazanılan şeyi mi söylemeli?

“Gönder” butonun ne yaptığını söyler, “Fiyat teklifimi al” tıklandığında ne kazanılacağını söyler. Kazanç ifadesi motive edebilir ama uzar, butonu şişirir ve bazı bağlamlarda abartılı durur. Eylem ifadesi kısadır ve beklentiyi tam karşılar; buna karşılık ilerlemek için bir sebep sunmaz.

**Test edilmesi gerekenler**
- İfade: Kazanç ifadesi tıklamayı artırıyor mu?
- Uzunluk: Uzayan metin butonun tanınmasını zorlaştırıyor mu?
- Beklenti: Kazanç ifadesi tıklandıktan sonra gerçekten karşılanıyor mu?
- Kişi eki: Birinci tekil ifade (“teklifimi al”) fark yaratıyor mu?
- Segment: Yeni ziyaretçi ile geri dönen kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: Buton metni sonraki adımın tamamlanmasını artırıyor mu?
- Buton Tıklama Oranı: Tıklama artıyor mu?
- Tıklama Sonrası Dökülme Oranı: Beklentisi karşılanmayan kullanıcı sonraki adımda kaybedilmemeli.
- Geri Dönüş Oranı: Butona tıklayıp geri dönme artmamalı.
- Erişilebilirlik: Ekran okuyucuda tek başına anlamsız kalan buton metni bırakılmamalı.

**Yapılmaması gerekenler**
- Butonda tıklandığında gerçekleşmeyecek bir sonucu vaat etmeyin.
- Aynı testte buton metni ile buton biçimini birlikte değiştirmeyin.
- Metni butona sığmayacak kadar uzatıp iki satıra bölmeyin.
- Aynı sayfadaki iki butonu farklı yaklaşımla yazıp hangisinin etkilediğini karıştırmayın.
- Tıklama arttı diye sonraki adıma bakmadan kazandı demeyin.


> **Not:** SaaS deneme CTA'sının metni `saas-b2b.md`'de kendi senaryosudur (huni-sonu birincil metrikleriyle); deneme akışı için onu kullanın.
---

## Dolu buton mu, çerçeveli buton mu daha çok tıklanıyor?

Dolu buton görsel ağırlığıyla öne çıkar ve birincil aksiyonu işaret eder. Çerçeveli (içi boş) buton sayfayı sakinleştirir ve ikincil aksiyonlar için doğal görünür. İkisini de dolu yapmak hiyerarşiyi yok eder; ikisini de çerçeveli yapmak hiçbirini öne çıkarmaz.

**Test edilmesi gerekenler**
- Biçim: Dolu buton tıklamayı artırıyor mu?
- Hiyerarşi: Birincil ve ikincil aksiyon arasındaki fark yeterince belirgin mi?
- Rekabet: İki dolu buton birbirinin tıklamasını mı yiyor?
- Bağlam: Yoğun bir sayfada çerçeveli buton kayboluyor mu?
- Cihaz: Mobilde biçim farkı hâlâ ayırt ediliyor mu?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: Birincil aksiyon artıyor mu?
- Birincil Buton Tıklama Oranı: Asıl istenen aksiyon artıyor mu?
- İkincil Buton Tıklama Oranı: İkincil aksiyon tamamen kaybolmamalı.
- Sayfa Terk Oranı: Belirsiz hiyerarşi çıkışı artırmamalı.
- Erişilebilirlik: Buton kenar ve metin kontrastı eşiğin altına inmemeli.

**Yapılmaması gerekenler**
- Aynı testte buton biçimi ile buton rengini birlikte değiştirmeyin.
- Çerçeveli butonu arka planla aynı tona getirip görünmez hâle sokmayın.
- Birincil butonu belirginleştirirken ikincil aksiyonu erişilemez yapmayın.
- Biçim değişikliğini yalnızca bir butonda yapıp sayfadaki diğerlerini eski hâlinde bırakmayın.
- Kontrast eşiğini karşılamayan bir varyantı kazanan ilan etmeyin.

---

## İkincil aksiyonu bağlantı mı, buton mu yapmalı?

Butona benzeyen bir öğe tıklanabilirliğini açıkça duyurur; bağlantı ise daha hafif durur ve birincil aksiyonla rekabet etmez. İkincil aksiyonu buton yapmak onu görünür kılar ama asıl istenen aksiyonun payını azaltabilir. Bağlantı yapmak ise onu tamamen görünmez kılabilir.

**Test edilmesi gerekenler**
- Biçim: İkincil aksiyon buton olduğunda toplam ilerleme artıyor mu?
- Yamyamlık: İkincil aksiyon birincilin tıklamasını mı alıyor?
- Görünürlük: Bağlantı hâlinde kaç kullanıcı öğeyi fark ediyor?
- Konum: İkincil aksiyon birincilin yanında mı, altında mı durmalı?
- Cihaz: Mobilde bağlantının dokunma hedefi yeterli mi?

**Takip edilecek ana KPI’lar**
- Toplam Aksiyon Tamamlama Oranı: İki yolun toplamı artıyor mu?
- Birincil Aksiyon Oranı: Asıl istenen aksiyon kabul edilemez ölçüde düşmemeli.
- İkincil Aksiyon Oranı: İkincil yolun kullanımı ne kadar?
- Sayfa Terk Oranı: Seçenek karmaşası çıkışı artırmamalı.
- Erişilebilirlik: Dokunma hedefi küçülmemeli, odak görünürlüğü bozulmamalı.

**Yapılmaması gerekenler**
- Gezinme amaçlı bir bağlantıyı buton, işlem yapan bir butonu bağlantı olarak işaretlemeyin; semantik doğru kalmalıdır.
- Aynı testte biçim ile konumu birlikte değiştirmeyin.
- İkincil aksiyonu birincil kadar belirgin yapıp hiyerarşiyi silmeyin.
- Bağlantıyı yalnızca renkle ayırt edilebilir bırakmayın.
- Birincil aksiyon düştü diye toplam ilerlemeye bakmadan karar vermeyin.

---

## Buton stillerini tüm sayfada tutarlı tutmak fark yaratır mı?

Tutarlı buton stili neyin tıklanabilir olduğunu öğretir ve kullanıcı bir kez öğrendiğinde her yerde uygular. Bölümden bölüme değişen stiller dikkat çekebilir ama tıklanabilirlik işaretini bulanıklaştırır. Tutarlılık aynı zamanda tek tek bölümlerin öne çıkma imkânını azaltır.

**Test edilmesi gerekenler**
- Tutarlılık: Tüm butonları tek stile getirmek toplam aksiyonu artırıyor mu?
- Tanınırlık: Kullanıcı neyin tıklanabilir olduğunu daha hızlı anlıyor mu?
- Vurgu kaybı: Farklılaşan bir bölüm tutarlılık uğruna görünürlük kaybediyor mu?
- Kapsam: Tutarlılık sayfa içinde mi, tüm site genelinde mi kurulmalı?
- Cihaz: Mobilde stil farkları zaten ayırt edilebiliyor mu?

**Takip edilecek ana KPI’lar**
- Toplam Aksiyon Tamamlama Oranı: Tutarlılık ilerlemeyi artırıyor mu?
- Tıklanabilir Öğe Etkileşim Oranı: Etkileşim artıyor mu?
- Yanlış Tıklama Oranı: Tıklanabilir sanılan öğelere tıklama azalıyor mu?
- Bölüm Bazlı Etkileşim: Belirli bir bölümün etkileşimi kabul edilemez ölçüde düşmemeli.
- Erişilebilirlik: Odak göstergesi hiçbir butonda görünmez hâle gelmemeli.

**Yapılmaması gerekenler**
- Aynı testte stil tutarlılığı ile buton metinlerini birlikte değiştirmeyin.
- Tutarlılık adına birincil ve ikincil ayrımını da silmeyin.
- Site genelinde değişiklik yaparken yalnızca tek sayfada ölçüm kurmayın.
- Eski stili kullanmaya devam eden bölümleri test dışında bırakıp sonucu genellemeyin.
- Tutarlılığı, aslında farklı işlev gören öğeleri aynı göstermek için kullanmayın.

---

## Büyük taahhüt butonu mu, küçük adım butonu mu daha çok ilerletiyor?

“Satın al” doğrudan sonuca gider ama hazır olmayan ziyaretçiyi durdurur. “Önce dene”, “Fiyatı gör” gibi küçük bir adım daha çok tıklanır ama ilerleyen kullanıcıların bir kısmı sonuca hiç ulaşmaz. Doğru cevap, ziyaretçinin karar aşamasına ve ürünün fiyat seviyesine bağlıdır.

**Test edilmesi gerekenler**
- Taahhüt: Küçük adım butonu toplam dönüşümü artırıyor mu?
- Zincir: Küçük adımı atanların kaçı sonuca ulaşıyor?
- Birlikte sunum: İki butonu birlikte sunmak toplamı büyütüyor mu?
- Metin: Küçük adımın ne kadar küçük olduğu ifadeden anlaşılıyor mu?
- Segment: Yeni ziyaretçi ile karar aşamasındaki ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Nihai Dönüşüm Oranı (CR): Huninin sonundaki tamamlama artıyor mu?
- Buton Tıklama Oranı: İlk aksiyon artıyor mu?
- Ara Adım → Sonuç Geçiş Oranı: Küçük adımı atanların sonuca ulaşma oranı düşmemeli.
- Karar Süresi: Toplam satın alma süresi kabul edilemez ölçüde uzamamalı.
- Aksiyon Kalitesi: Kolaylaşan ilk adım niteliksiz talep getirmemeli.

**Yapılmaması gerekenler**
- Ara adımın tıklamasını nihai dönüşüm gibi raporlamayın; birincil metrik daima huninin sonudur.
- Aynı testte buton taahhüdü ile fiyat gösterimini birlikte değiştirmeyin.
- Küçük adımı, aslında büyük bir taahhüde götüren bir kapı gibi kurmayın.
- İki butonu eşit görsel ağırlıkta verip hiyerarşiyi silmeyin.
- Tıklama arttı diye zincirin sonuna bakmadan kazandı demeyin.

---

## İkonların yanına yazılı etiket eklemek işe yarar mı?

İkon yer kazandırır ve dili aşar ama anlamı çoğu zaman öğrenilmiş bir konvansiyona dayanır; tanınmayan bir ikon boş bir kutudur. Etiket eklemek anlamı netleştirir, buna karşılık yer kaplar ve arayüzü kalabalıklaştırır. Özellikle az kullanılan işlevlerde etiketin değeri yükselir.

**Test edilmesi gerekenler**
- Etiket: İkona metin eklemek kullanımı artırıyor mu?
- Tanınırlık: Hangi ikonlar etiketsiz zaten anlaşılıyor?
- Yer: Etiket ikonun altında mı, yanında mı durmalı?
- Kalabalık: Etiketler diğer öğelerin alanını daraltıyor mu?
- Cihaz: Mobilde etiket için yer kalıyor mu?

**Takip edilecek ana KPI’lar**
- İlgili İşlev Kullanım Oranı: İkonun temsil ettiği işlevin kullanımı artıyor mu?
- Aksiyon Tamamlama Oranı: Genel ilerleme düşmemeli.
- Yanlış Tıklama Oranı: Beklenmeyen işleve tıklama azalıyor mu?
- Destek Talebi Sayısı: “Bunu nerede yapıyorum” soruları azalıyor mu?
- Erişilebilirlik: Etiketsiz ikon erişilebilir adsız kalmamalı.

**Yapılmaması gerekenler**
- Etiketi eklerken ikonu da değiştirmeyin.
- Etiketi yalnızca üzerine gelince görünen bir ipucuna dönüştürüp “etiket eklendi” saymayın.
- Etiket eklerken dokunma hedeflerini küçültmeyin.
- Ekran okuyucu için tanımlı erişilebilir adı görsel etikete bağımlı hâle getirmeyin.
- Tek dilde ölçüp sonucu etiketleri çok daha uzun olan dillere genellemeyin.

---

## Bağlantıları yeni sekmede açmak işe yarar mı?

Yeni sekmede açmak kullanıcının bulunduğu sayfayı kaybetmemesini sağlar; ödeme veya form akışında yarım kalan işin korunması değerlidir. Karşı tarafta: kullanıcı denetimini elinden alır, geri tuşunu işlevsiz kılar, mobilde sekme yönetimi zordur ve beklenmedik davranış rahatsız eder.

**Test edilmesi gerekenler**
- Davranış: Yeni sekmede açmak asıl akışın tamamlanmasını artırıyor mu?
- Kapsam: Hangi bağlantılar (yasal metin, yardım, dış kaynak) yeni sekmede açılmalı?
- Beklenti: Kullanıcı davranışı önceden anlıyor mu, sürpriz mi oluyor?
- Geri dönüş: Yeni sekmeden asıl akışa dönüş gerçekleşiyor mu?
- Cihaz: Mobilde sekme değişimi kullanıcıyı kaybettiriyor mu?

**Takip edilecek ana KPI’lar**
- Asıl Akış Tamamlama Oranı: Form veya ödeme tamamlanması artıyor mu?
- Bağlantı Tıklama Oranı: Bağlantıya erişim düşmemeli.
- Akışa Geri Dönüş Oranı: Ayrılan kullanıcının dönüşü artıyor mu?
- Veri Kaybı Oranı: Yarım kalan formdaki veri kaybolmamalı.
- Erişilebilirlik: Yeni sekme davranışı bildirimsiz bırakılmamalı.

**Yapılmaması gerekenler**
- Sitedeki tüm bağlantıları ayrım yapmadan yeni sekmede açmayın.
- Yeni sekme davranışını kullanıcıya bildirmeden uygulamayın.
- Aynı testte sekme davranışı ile bağlantı metnini birlikte değiştirmeyin.
- Yeni sekmeyi, kullanıcının çıkmasını engellemek için kullanmayın.
- Form verisinin korunmasını çözmek yerine yeni sekmeyi yama olarak kullanmayın.

---

## Metin içine yerleştirilen bağlantı tıklanıyor mu?

Açıklama metninin içine gömülü bir bağlantı, tam ilgili düşünce oluştuğu anda yol sunar ve ayrı bir buton kadar rahatsız etmez. Riski: metin içinde gözden kaçar, tıklanabilirliği butona göre zayıf işaretlenir ve okuma akışını bölerek kullanıcıyı erken uzaklaştırabilir.

**Test edilmesi gerekenler**
- Yerleşim: Metin içi bağlantı ayrı bir butondan daha mı çok tıklanıyor?
- Konum: Bağlantı paragrafın başında mı, sonunda mı daha etkili?
- Görünürlük: Bağlantı yeterince ayırt edilebiliyor mu?
- Erken ayrılma: Bağlantı okuma akışını bölüp asıl mesajı yarıda mı bırakıyor?
- Segment: Okuyan ve tarayan kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: Bağlantı asıl hedefe götürüyor mu?
- Bağlantı Tıklama Oranı: Tıklama artıyor mu?
- Kaydırma Derinliği: Metnin okunması kabul edilemez ölçüde düşmemeli.
- Sayfa Terk Oranı: Erken ayrılma artmamalı.
- Erişilebilirlik: Bağlantı yalnızca renkle işaretlenmemeli.

**Yapılmaması gerekenler**
- Bağlantıyı çevresindeki metinden ayırt edilemeyecek biçimde biçimlendirmeyin.
- Aynı testte bağlantı yerleşimi ile paragraf metnini birlikte değiştirmeyin.
- Bağlantı metnini “buraya tıklayın” gibi bağlamsız bir ifadeye indirgemeyin.
- Aynı paragrafa birden çok bağlantı koyup hangisinin çalıştığını ölçemez hâle gelmeyin.
- Tıklama arttı diye asıl hedefe ulaşmayı ölçmeden kazandı demeyin.

---

## Sık yapılan işlemler için kısayol sunmak işe yarar mı?

Tekrarlanan bir işlemi tek dokunuşa indirmek (tekrar sipariş, son aramayı yükle, kayıtlı adresle devam) deneyimli kullanıcıyı hızlandırır. Riski: kısayol arayüzde yer kaplar, yeni kullanıcı için anlamsızdır ve yanlış varsayımla hazırlanmış bir kısayol hatalı işleme yol açabilir.

**Test edilmesi gerekenler**
- Varlık: Kısayol sunmak tamamlamayı artırıyor mu?
- Hedef kitle: Kısayolu kimler kullanıyor, yeni kullanıcıya faydası var mı?
- Doğruluk: Kısayolun getirdiği varsayılan gerçekten doğru mu?
- Görünürlük: Kısayol yalnızca ilgili kullanıcıya mı gösterilmeli?
- Segment: İlk kez gelen ile tekrar eden kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: İşlem tamamlanması artıyor mu?
- Kısayol Kullanım Oranı: Kısayol gerçekten kullanılıyor mu?
- Hatalı İşlem Oranı: Yanlış varsayılanla yapılan işlem artmamalı.
- İşlem Süresi: Tamamlama süresi kısalıyor mu?
- İptal veya Düzeltme Oranı: Sonradan düzeltme talebi artmamalı.

**Yapılmaması gerekenler**
- Kısayolu geri alınamaz bir işlemi tek dokunuşa indirmek için kullanmayın.
- Aynı testte kısayol ile ana akışın adımlarını birlikte değiştirmeyin.
- Kısayolun getirdiği varsayılanı kullanıcıya göstermeden uygulamayın.
- Yeni kullanıcıya anlamsız gelen bir kısayolu ana akışın önüne koymayın.
- Kullanım oranı düşük diye hemen kaldırmayın; küçük ama sadık bir grup için kritik olabilir.

---

## Bir adım bittiğinde otomatik olarak sonrakine geçmek işe yarar mı?

Seçim yapılır yapılmaz sonraki adıma geçmek bir tıklamayı ortadan kaldırır ve akışı hızlandırır. Bedeli: kullanıcı seçimini gözden geçiremez, yanlış dokunuş geri alınamaz bir ilerlemeye dönüşür ve kontrol hissi kaybolur. Geri dönüşün ne kadar kolay olduğu belirleyicidir.

**Test edilmesi gerekenler**
- Otomatik geçiş: Seçimden sonra otomatik ilerleme tamamlamayı artırıyor mu?
- Hata: Yanlış seçimle ilerleme ne sıklıkla oluyor?
- Geri dönüş: Geri dönmek ne kadar kolay, veri korunuyor mu?
- Gecikme: Kısa bir bekleme eklemek hatayı azaltıyor mu?
- Cihaz: Mobilde yanlış dokunma kaynaklı geçiş daha mı sık?

**Takip edilecek ana KPI’lar**
- Akış Tamamlama Oranı: Otomatik geçiş tamamlamayı artırıyor mu?
- Geri Dönüş Oranı: Bir önceki adıma dönme artmamalı.
- Hatalı Seçim Oranı: Yanlış seçimle ilerleme artmamalı.
- Ortalama Tamamlama Süresi: Akış hızlanıyor mu?
- Erişilebilirlik: Otomatik geçişte odak eski adımda kalmamalı, geçiş duyurusuz olmamalı.

**Yapılmaması gerekenler**
- Geri dönüşü olmayan bir adımda otomatik geçiş kurmayın.
- Ödeme veya onay adımını otomatik geçişe bağlamayın.
- Aynı testte otomatik geçiş ile adım sayısını birlikte değiştirmeyin.
- Otomatik geçişte girilen veriyi korumayan bir uygulama bırakmayın.
- Süre kısaldı diye hata oranına bakmadan kazandı demeyin.

---

## Süreli kampanya duyurusunu site genelinde göstermek işe yarar mı?

Belirli bir süre boyunca tüm sayfalarda görünen bir duyuru şeridi kampanyayı kaçırılmaz kılar. Riski: kullanıcılar reklam bandına benzeyen öğeleri görmezden gelmeyi öğrenmiştir, şerit her sayfada dikey alan yer ve süreklileşen bir duyuru bir süre sonra görünmez hâle gelir. (Kalıcı hizmet vaatlerini — kargo, iade, teslimat — sayfa üstünde göstermek ayrı bir senaryodur: `home-landing.md` → fayda çubuğu.)

**Test edilmesi gerekenler**
- Varlık: Site geneli duyuru kampanya aksiyonunu artırıyor mu?
- Kapsam: Tüm sayfalarda mı, yalnızca ilgili kategorilerde mi görünmeli?
- Kapatma: Kapatılabilir olması kullanımı nasıl değiştiriyor?
- Körlük: Çubuk birkaç ziyaretten sonra fark edilmemeye mi başlıyor?
- Cihaz: Mobilde çubuk ekranın değerli kısmını yiyor mu?

**Takip edilecek ana KPI’lar**
- Duyurulan Aksiyonun Tamamlanma Oranı: Çubuğun işaret ettiği eylem artıyor mu?
- Genel Dönüşüm Oranı (CR): Sitenin ana dönüşümü düşmemeli.
- Çubuk Tıklama Oranı: Çubuk gerçekten tıklanıyor mu?
- Kapatma Oranı: Rahatsızlık sinyali olarak kapatma artmamalı.
- Sayfa Terk Oranı: Ek öğe çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Kapatılamayan bir çubuk kurmayın (kural 6).
- Aynı testte çubuğun varlığı ile içeriğini birlikte değiştirmeyin.
- Süresi dolunca gerçekten kalkmayan “süreli” kampanya duyurmayın; sayaç ve tarih gerçek olmalı (kural 6).
- Çubuğu sabitleyip ekranın önemli bir kısmını kalıcı olarak kaplamayın.
- Çubuk tıklaması arttı diye sitenin ana dönüşümüne bakmadan kazandı demeyin.

---

## Kampanya duyurusu hemen mi, bir süre sonra mı görünmeli?

Çubuğun sayfa açılır açılmaz görünmesi mesajı herkese ulaştırır ama içerikle rekabet eder. Kaydırma sonrası veya birkaç saniye gecikmeyle belirmesi ise ziyaretçi bağlamı kurduktan sonra devreye girer; buna karşılık geç beliren bir öğe içeriği kaydırarak yanlış tıklamaya yol açabilir.

**Test edilmesi gerekenler**
- Zamanlama: Hemen mi, gecikmeli mi gösterim daha çok aksiyon getiriyor?
- Tetikleyici: Süre mi, kaydırma derinliği mi daha iyi bir tetikleyici?
- Sayfa hareketi: Sonradan beliren çubuk içeriği kaydırıyor mu?
- Tekrar: Aynı oturumda tekrar gösterilmeli mi?
- Cihaz: Mobilde gecikmeli gösterim daha mı az rahatsız edici?

**Takip edilecek ana KPI’lar**
- Duyurulan Aksiyonun Tamamlanma Oranı: Zamanlama aksiyonu artırıyor mu?
- Çubuk Görülme Oranı: Çubuğu gören ziyaretçi oranı ne kadar?
- Yanlış Tıklama Oranı: Kayan içerik kaynaklı yanlış tıklama artmamalı.
- Genel Dönüşüm Oranı (CR): Ana dönüşüm düşmemeli.
- Sayfa Terk Oranı: Çıkış artmamalı.

**Yapılmaması gerekenler**
- Beliren çubuğun sayfa içeriğini kaydırmasına izin vermeyin; yer önceden ayrılmalıdır.
- Aynı testte zamanlama ile çubuk içeriğini birlikte değiştirmeyin.
- Aynı oturumda kapatılan çubuğu tekrar tekrar göstermeyin.
- Gecikmeli gösterimi kullanıcı bir aksiyona başladığı anda tetiklemeyin.
- Görülme oranı arttı diye aksiyona bakmadan kazandı demeyin.

---

## Bildirim işaretini sayı olarak mı, nokta olarak mı göstermeli?

Sayılı rozet ne kadar bekleyen iş olduğunu söyler ve aciliyeti ölçeklendirir. Sade bir nokta ise yalnızca “yeni bir şey var” der; daha az baskı yaratır ama bilgi vermez. Yüksek sayılar motive etmek yerine bunaltabilir, sıfırlanamayan bir rozet ise kalıcı bir rahatsızlığa dönüşür.

**Test edilmesi gerekenler**
- Biçim: Sayılı rozet mi, sade nokta mı daha çok tıklanıyor?
- Büyüklük: Yüksek sayılar caydırıcı hâle geliyor mu?
- Sıfırlama: Rozet ne zaman temizlenmeli?
- Konum: Rozet hangi öğede daha etkili?
- Cihaz: Mobilde küçük rozet fark ediliyor mu?

**Takip edilecek ana KPI’lar**
- İlgili Bölüm Ziyaret Oranı: Rozetin işaret ettiği bölüme giriş artıyor mu?
- Aksiyon Tamamlama Oranı: Girenler işi bitiriyor mu?
- Rozet Yoksayma Oranı: Sürekli görülüp tıklanmayan rozet oranı artmamalı.
- Uygulama veya Site Terk Oranı: Rahatsızlık çıkışı artırmamalı.
- Erişilebilirlik: Rozet yalnızca renkle anlatılmamalı, ekran okuyucuya duyurusuz kalmamalı.

**Yapılmaması gerekenler**
- Karşılığı olmayan bir rozet göstermeyin; sahte bekleyen iş üretmeyin (kural 6).
- Aynı testte rozet biçimi ile rozetin konumunu birlikte değiştirmeyin.
- Sıfırlanamayan, kullanıcının kapatamadığı bir rozet kurmayın.
- Rozeti yalnızca kırmızı renkle ayırt edilebilir bırakmayın.
- Tıklama arttı diye ilgili bölümdeki tamamlamaya bakmadan kazandı demeyin.

---

## Canlı destek düğmesi eklemek dönüşümü artırır mı?

Erişilebilir bir destek düğmesi tereddüt eden kullanıcıya çıkış yolu verir ve cevapsız kalan soruyu terke dönüşmeden yakalar. Bedeli: düğme ekranda yer kaplar, mobilde içeriği kapatabilir ve destek yükünü artırır. Ayrıca canlı destek gerçekten canlı değilse (yanıt gecikmesi) güveni düşürür.

**Test edilmesi gerekenler**
- Varlık: Destek düğmesi dönüşümü artırıyor mu?
- Yanıt süresi: Gelen taleplere yanıt süresi vaadi karşılıyor mu?
- Konum: Düğme sağ altta mı, akışın içinde belirli bir noktada mı?
- Kapsam: Her sayfada mı, yalnızca tereddüt noktalarında mı görünmeli?
- Cihaz: Mobilde düğme içeriği veya ana butonu kapatıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Destek erişimi satışa dönüyor mu?
- Sohbet Başlatma Oranı: Düğme kullanılıyor mu?
- Destek Yanıt Süresi: Yanıt süresi vaat edilen seviyenin altına düşmemeli.
- Terk Oranı: Tereddüt kaynaklı bırakma azalıyor mu?
- Ana Buton Görünürlüğü: Destek düğmesi asıl aksiyonu kapatmamalı.

**Yapılmaması gerekenler**
- Destek ekibi hazır değilken canlı destek düğmesi açmayın; yanıtsız sohbet zarar verir.
- Aynı testte düğmenin varlığı ile konumunu birlikte değiştirmeyin.
- Düğmeyi ana aksiyon butonunun üzerine bindirmeyin.
- Sohbet başlatmadan kişisel bilgi zorunluluğu koymayın.
- Sohbet sayısı arttı diye dönüşüme ve yanıt süresine bakmadan kazandı demeyin.

---

## Sohbet penceresini kendiliğinden açmak işe yarar mı?

Kendiliğinden açılan sohbet penceresi yardımın varlığını duyurur ve pasif düğmeye göre çok daha fazla sohbet başlatır. Riski: davetsiz açılan bir pencere içeriği kapatır, kullanıcıyı böler ve rahatsızlık yaratır; gelen sohbetlerin niteliği de düşebilir çünkü kullanıcı yardım istemek yerine tepki vermiştir.

**Test edilmesi gerekenler**
- Açılma: Kendiliğinden açılma dönüşümü artırıyor mu?
- Tetikleyici: Süre mi, belirli bir sayfa mı, duraksama mı tetiklemeli?
- Nitelik: Gelen sohbetlerin niteliği düşüyor mu?
- Kapatma: Kapatan kullanıcı sonradan tekrar açıyor mu?
- Cihaz: Mobilde açılan pencere ekranın tamamını kapatıyor mu?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Kendiliğinden açılma satışa dönüyor mu?
- Sohbet Başlatma Oranı: Sohbet sayısı artıyor mu?
- Nitelikli Sohbet Oranı: Anlamsız veya boş sohbet oranı artmamalı.
- Sayfa Terk Oranı: Rahatsızlık çıkışı artırmamalı.
- Destek Yükü: Ekibin taşıyabileceği talep seviyesi aşılmamalı.

**Yapılmaması gerekenler**
- Kapatılamayan veya kapatma düğmesi gizlenmiş bir pencere kurmayın (kural 6).
- Kullanıcı bir form doldururken veya ödeme yaparken pencereyi açmayın.
- Aynı testte açılma davranışı ile karşılama mesajını birlikte değiştirmeyin.
- Kapatılan pencereyi aynı oturumda tekrar açmayın.
- Sohbet sayısı arttı diye niteliğe ve destek yüküne bakmadan kazandı demeyin.

---

## Bilgiyi tablo olarak mı, kutular hâlinde mi sunmalı?

Tablo satır ve sütun mantığıyla doğrudan karşılaştırma kurar; çok sayıda özelliği yan yana koymak gerektiğinde en verimli biçimdir. Kutular her seçeneği bağımsız bir teklif gibi gösterir ve tarama kolaylığı sağlar ama farkların bulunmasını zorlaştırır. Yatay ve dikey yönelim de aynı içeriği farklı okutur.

**Test edilmesi gerekenler**
- Biçim: Tablo mu, kutu mu, madde listesi mi daha çok aksiyon getiriyor?
- Yönelim: Yatay mı, dikey mi düzen daha kolay okunuyor?
- Satır sayısı: Kaç karşılaştırma satırı faydalıyken kaçında yoruluyor?
- Farkların bulunması: Kullanıcı seçenekler arası farkı bulabiliyor mu?
- Cihaz: Mobilde tablo yatay kaydırmaya düşüyor mu?

**Takip edilecek ana KPI’lar**
- Aksiyon Tamamlama Oranı: Sunum biçimi seçim yapmayı artırıyor mu?
- Karşılaştırma Etkileşim Oranı: İçerik gerçekten inceleniyor mu?
- Karar Süresi: Seçim süresi kabul edilemez ölçüde uzamamalı.
- Sayfa Terk Oranı: Karmaşa çıkışı artırmamalı.
- Erişilebilirlik: Tablo yapısı ekran okuyucuda anlamsız hâle gelmemeli.

**Yapılmaması gerekenler**
- Aynı testte sunum biçimi ile karşılaştırılan içeriği birlikte değiştirmeyin.
- Düzen amaçlı tabloyu semantik tablo olarak işaretlemeyin veya tersini yapmayın.
- Mobilde tabloyu okunmaz derecede küçültüp kutu düzeniyle karşılaştırmayın.
- Kutu düzeninde farkları yalnızca sıralamayla ima edip yazılı olarak vermemezlik etmeyin.
- Tek bir içerik türünde ölçüp sonucu tüm karşılaştırmalara genellemeyin.

> **Not:** Fiyat planlarının tablo/kart karşılaştırması `pricing.md` → “Planları karşılaştırma tablosunda mı, ayrı kartlarda mı sunmalı?” senaryosunun konusudur; fiyat sayfası için bu senaryoyu değil onu kullanın.

---

## Dış bağlantıları yeni sekmede açmak sayfada kalma oranını artırır mı?

Bir sayfadaki dış bağlantı (ör. blog yazısındaki kaynak, ortak site linki) aynı sekmede açılırsa kullanıcı asıl siteden tamamen ayrılır; yeni sekmede açılırsa asıl sekme açık kalır. Riski, beklenmedik bir yeni sekmenin bazı kullanıcılarda kafa karışıklığı yaratması ve erişilebilirlik araçlarıyla kullanımı zorlaştırmasıdır.

**Test edilmesi gerekenler**
- Davranış: Yeni sekmede açmak sayfaya geri dönüş oranını artırıyor mu?
- Bağlantı türü: İç bağlantılarda da aynı davranış mı uygulanmalı, yoksa yalnızca dış bağlantılarda mı?
- Farkındalık: Kullanıcı yeni sekme açıldığını fark edip kafası mı karışıyor?
- Cihaz: Mobilde yeni sekme davranışı masaüstünden farklı bir deneyim mi yaratıyor?
- Erişilebilirlik: Ekran okuyucu kullanıcısı yeni sekme açılacağını önceden anlayabiliyor mu?

**Takip edilecek ana KPI’lar**
- Sayfada Kalma/Geri Dönüş Oranı: Yeni sekme davranışı asıl siteye dönüşü artırıyor mu?
- Dış Bağlantı Tıklama Oranı: Davranış değişikliği tıklama oranını etkiliyor mu?
- Oturum Süresi: Toplam site kullanım süresi düşmemeli.
- Kafa Karışıklığı (anket): Kullanıcı beklenmedik bir sekme açıldığını fark edip rahatsız olmamalı.
- Geri Tuşu Kullanımı: Tarayıcı geri tuşuna basma sıklığı artmamalı — artıyorsa davranış kafa karıştırıyordur.

**Yapılmaması gerekenler**
- Ekran okuyucu kullanıcısını önceden uyarmadan yeni sekme açan bağlantı kurmayın (erişilebilirlik guardrail’i, kural 3).
- Aynı testte iç ve dış bağlantıların davranışını birlikte değiştirmeyin.
- Ödeme veya form gönderimi gibi kritik bir aksiyonu yeni sekmede açıp kullanıcıyı akıştan koparmayın.
- Yeni sekme davranışını yalnızca bazı tarayıcılarda tutarsız çalışacak şekilde kurmayın.
- Kullanıcının linke sağ tıklayıp kendi tercihiyle sekme açma imkânını elinden almayın.

---

## Buton metnini komut kipiyle mi (“Başlat”), birinci şahıs bildirimiyle mi (“Başlıyorum”) yazmalı?

Bir CTA’nın emir kipiyle mi (“Başlat”), yoksa kullanıcının kendi ağzından söylediği birinci şahıs bildirimiyle mi (“Başlıyorum”) yazıldığı, kararı kimin verdiği hissini değiştirebilir — emir kipi siteden gelen bir talimat gibi okunurken, birinci şahıs ifade kullanıcının kendi kararını onayladığı bir cümle gibi okunur. Etkisi küçük ama tutarlı bir mikro-copy farkıdır; markanın genel ses tonuyla uyumlu olmayan bir kalıp tuhaf durabilir.

**Test edilmesi gerekenler**
- Kip: Emir kipi mi, birinci şahıs bildirimi mi tıklama oranını artırıyor?
- Bağlam: Etki ücretsiz/düşük riskli aksiyonlarda mı, ücretli/yüksek riskli aksiyonlarda mı daha güçlü?
- Ton tutarlılığı: Marka sesi resmi olduğunda birinci şahıs ifade garip mi duruyor?
- Uzunluk: Birinci şahıs ifade buton genişliğini büyütüp mobilde sıkışıklık mı yaratıyor?
- Segment: Yeni ziyaretçi ile daha önce siteyi kullanmış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Tıklama Oranı (CTR): Buton metni tıklamayı artırıyor mu?
- Dönüşüm Oranı (CR): Tıklamadan sonraki tamamlama oranı düşmemeli.
- Marka Algısı (anket): İfade markayı samimiyetsiz veya tuhaf hissettirmemeli.
- Sayfa Terk Oranı: Değişiklik terk oranını artırmamalı.
- Tekrar Ziyaret Oranı: Kısa vadeli tıklama artışı uğruna marka algısı zedelenmemeli.

**Yapılmaması gerekenler**
- Aynı testte buton metninin kipini ve rengini veya boyutunu birlikte değiştirmeyin.
- Birinci şahıs ifadeyi, kullanıcının henüz vermediği bir kararı vermiş gibi göstermek için kullanmayın — ücretli bir işlemde onay adımı hâlâ ayrıca gösterilmeli.
- Marka sesi ile tutarsız bir kip seçip sayfanın geri kalanıyla çelişen bir ton yaratmayın.
- Farklı butonlarda farklı kipler kullanıp sayfa içi tutarlılığı bozmayın.
- Sonucu tek bir CTA’dan genelleyip sitedeki tüm butonları aynı anda değiştirmeyin; kademeli uygulayın.
