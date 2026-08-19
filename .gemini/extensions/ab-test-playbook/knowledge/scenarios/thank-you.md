# Teşekkür ve Sipariş Onay Sayfası

Yolculuk aşaması: satın alma veya kayıt tamamlandıktan hemen sonraki an. Kullanıcı zaten dönüştü — bu sayfa yeni bir dönüşüm hunisi değil, ek değer (çapraz satış, hesap oluşturma, referans) için nadir bir dikkat penceresidir. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Sipariş onay sayfasında ilgili ürün önerisi göstermek ek satın alma yaratır mı?

Kullanıcı zaten ödeme yaptı, kart bilgisi elinde ve satın alma kararı tazeyken tekrar sürtünmeden geçmiş olur — bu, ikinci bir satın almayı önermek için nadir bir andır. Risk, önerinin asıl siparişin teslimat/onay bilgisini gölgelemesi veya kullanıcının “az önce ödedim, şimdi mi” hissiyle rahatsız olmasıdır.

**Test edilmesi gerekenler**
- Zamanlama: Öneri sipariş özetinden önce mi, sonra mı gösterilmeli?
- İlgi düzeyi: Az önce alınan ürünle ilişkili öneri mi, genel popüler ürün mü daha çok tıklanıyor?
- Sayı: Tek ürün mü, birkaç seçenekli bir şerit mi daha çok satın alma yaratıyor?
- Fiyat aralığı: Ana siparişten daha düşük fiyatlı öneri daha mı çok kabul görüyor?
- Cihaz: Mobilde öneri şeridi sipariş onay bilgisinin altına mı, kaydırmadan görünür bir yere mi konmalı?

**Takip edilecek ana KPI’lar**
- Ek Satın Alma Oranı: Teşekkür sayfasından yeni bir sipariş başlatan kullanıcı oranı artıyor mu?
- Ek Sipariş Ortalama Tutarı: Yeni siparişlerin ortalama tutarı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Kullanıcı asıl sipariş numarasını ve teslimat bilgisini bulabilmeli.
- Destek Talebi: “Siparişimi nasıl takip ederim” soruları artmamalı.
- Sayfa Terk Oranı: Öneri şeridi sayfadan hızlı çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Öneriyi, asıl siparişin teslimat tarihi veya sipariş numarasının önüne geçirip gizlemeyin.
- Aynı testte öneri şeridinin varlığı ile ürün seçim mantığını (ilişkili/genel) birlikte değiştirmeyin.
- Kullanıcıyı ikinci bir ödeme adımına yönlendirip asıl siparişin tamamlandığı hissini bulanıklaştırmayın.
- Misafir ödemesi yapan kullanıcıya bu ekranda ayrıca hesap oluşturmayı da aynı anda önermeyin — bu ayrı bir test değişkenidir.
- Öneri şeridini kapatılamaz veya sipariş onayını okumadan geçilemez hâle getirmeyin.

---

## Misafir olarak ödeme yapana teşekkür sayfasında hesap oluşturma daveti göstermek kayıt oranını artırır mı?

Misafir ödemesi checkout sürtünmesini azaltır ama işletmeyi tekrar iletişim kurabileceği bir hesaptan mahrum bırakır. Sipariş tamamlandıktan hemen sonra, bilgiler zaten girilmişken hesap oluşturmayı önermek, checkout öncesinde zorunlu kayıt istemekten farklı bir sürtünme profiline sahiptir — kullanıcı artık kaybedecek bir dönüşümü riske atmıyor.

**Test edilmesi gerekenler**
- Teklif: “Şifre belirle, hesabını tamamla” ifadesi mi, “siparişlerini takip et” faydası mı daha çok kabul görüyor?
- Ön doldurma: E-posta ve adres bilgisi otomatik dolu gelince kayıt oranı artıyor mu?
- Zorunluluk: Daveti reddetmek gelecekteki alışverişi zorlaştırıyor mu, yoksa nötr mü?
- Konum: Davet sipariş özetinin üstünde mi, altında mı daha çok kabul görüyor?
- Segment: İlk kez alışveriş yapan ile daha önce misafir olarak alışveriş yapmış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Hesap Oluşturma Oranı: Misafir ödemesi yapıp hesap oluşturan kullanıcı oranı artıyor mu?
- Tekrar Satın Alma Oranı: Hesap oluşturan kullanıcılar 30/60/90 gün içinde gerçekten geri dönüyor mu?
- Sipariş Netliği (anket): Davet, siparişin tamamlandığı algısını bulanıklaştırmamalı.
- E-posta Onay Oranı: Hesap oluşturma sürecinde bırakma artmamalı.
- Destek Talebi: “Siparişim nereye gitti, hesabım var mı” karışıklığı artmamalı.

**Yapılmaması gerekenler**
- Hesap oluşturmayı, sipariş onayını görmenin ön koşulu hâline getirmeyin — sipariş bilgisi davetten bağımsız her zaman görünür olmalı.
- Aynı testte davet metnini ve ön doldurma davranışını birlikte değiştirmeyin.
- Kullanıcı reddettiğinde bir daha aynı oturumda tekrar sormayın.
- Misafir ödemesini bu test yüzünden zorlaştırmayın; checkout akışının kendisine dokunmayın.
- Kullanıcının açıkça vermediği bir bilgiyle hesabı önceden doldurmayın.

---

## Teşekkür sayfasında arkadaşını davet et teklifini göstermek paylaşım oranını artırır mı?

Kullanıcı memnuniyetinin tepe noktası satın alma anının hemen sonrasıdır — referans isteği için davranışsal olarak en uygun an burasıdır. Riski, teklifin asıl sipariş bilgisini gölgelemesi veya ödül teklifi gerçek değilse güven kaybı yaratmasıdır.

**Test edilmesi gerekenler**
- Teşvik: Ödüllü davet mi, ödülsüz basit paylaşım mı daha çok tıklanıyor?
- Kanal: Mesajlaşma uygulaması, e-posta veya link kopyalama seçeneklerinden hangisi en çok kullanılıyor?
- Zamanlama: Davet sipariş özetiyle aynı ekranda mı, kısa bir gecikmeyle mi daha etkili?
- Görünürlük: Davet kalıcı bir kart mı, kapatılabilir bir öneri mi daha az rahatsız ediyor?
- Cihaz: Mobilde paylaşım linki native paylaşım menüsünü mü açmalı, kopyala butonu mu yeterli?

**Takip edilecek ana KPI’lar**
- Paylaşım Başlatma Oranı: Daveti kullanan kullanıcı oranı artıyor mu?
- Referans Dönüşüm Oranı: Paylaşılan linkten gelen yeni müşteri sayısı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Davet, sipariş bilgisini gölgelememeli.
- Ödül Talep Oranı: Vaat edilen ödül gerçekten talep edilip kullanılabiliyor mu — edilmiyorsa bu bir bulgudur.
- Sayfa Terk Oranı: Davet kartı sayfadan hızlı çıkışı artırmamalı.

**Yapılmaması gerekenler**
- Vaat edilen ödülü gerçekte vermeyin ya da koşullarını sayfada belirtmeden bırakmayın (kural 6).
- Aynı testte teşvik türü ile paylaşım kanallarının sırasını birlikte değiştirmeyin.
- Daveti kapatılamaz hâle getirmeyin; kullanıcı sipariş bilgisine daveti görmeden de ulaşabilmeli.
- Kullanıcının rızası olmadan davet linkini otomatik olarak sosyal medyada paylaşmayın.
- Ödül tutarını gerçek maliyeti karşılamayacak kadar düşük tutup büyük vaat gibi sunmayın.