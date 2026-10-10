# Teşekkür ve Sipariş Onay Sayfası

Yolculuk aşaması: satın alma veya kayıt tamamlandıktan hemen sonraki an. Kullanıcı zaten dönüştü; bu sayfa yeni bir dönüşüm hunisi değil, ek değer (çapraz satış, hesap oluşturma, referans) için nadir bir dikkat penceresidir. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Sipariş onay sayfasında ilgili ürün önerisi göstermek ek satın alma yaratır mı?

Değişken: Onay sayfasındaki ürün önerisi şeridi · Fark: ekle

Kullanıcı zaten ödeme yaptı, kart bilgisi elinde ve satın alma kararı tazeyken tekrar sürtünmeden geçmiş olur; bu, ikinci bir satın almayı önermek için nadir bir andır. Risk, önerinin asıl siparişin teslimat/onay bilgisini gölgelemesi veya kullanıcının “az önce ödedim, şimdi mi” hissiyle rahatsız olmasıdır.

**Test edilmesi gerekenler**
- Gölgeleme: Öneri şeridi eklenince kullanıcı sipariş numarasını ve teslimat tarihini bulmakta zorlanıyor mu?
- Sonraki test: Öneri şeridi kazanırsa, ilişkili ürün ile genel popüler ürün seçim mantığı ayrı bir testte karşılaştırıldığında hangisi daha çok tıklanıyor?
- Sayı: Tek ürün mü, birkaç seçenekli bir şerit mi daha çok satın alma yaratıyor?
- Pişmanlık etkisi: Öneri şeridini gören kullanıcıda asıl sipariş için iptal veya iade talebi artıyor mu?
- Cihaz: Şeridin sipariş bilgisinin altında kaldığı mobilde, şeridi görüp tıklayan kullanıcı oranı masaüstünden ne kadar düşük?

**Takip edilecek ana KPI’lar**
- Ek Satın Alma Oranı: Teşekkür sayfasından yeni bir sipariş başlatan kullanıcı oranı artıyor mu?
- Ek Sipariş Ortalama Tutarı: Yeni siparişlerin ortalama tutarı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Kullanıcı asıl sipariş numarasını ve teslimat bilgisini bulabilmeli.
- Destek Talebi: “Siparişimi nasıl takip ederim” soruları artmamalı.
- İade veya İptal Oranı: Öneri şeridi asıl siparişte iptal veya iade talebini artırmamalı.

**Yapılmaması gerekenler**
- Öneriyi, asıl siparişin teslimat tarihi veya sipariş numarasının önüne geçirip gizlemeyin.
- Aynı testte öneri şeridinin varlığı ile ürün seçim mantığını (ilişkili/genel) birlikte değiştirmeyin.
- Kullanıcıyı ikinci bir ödeme adımına yönlendirip asıl siparişin tamamlandığı hissini bulanıklaştırmayın.
- Misafir ödemesi yapan kullanıcıya bu ekranda ayrıca hesap oluşturmayı da aynı anda önermeyin; bu ayrı bir test değişkenidir.
- Öneri şeridini kapatılamaz veya sipariş onayını okumadan geçilemez hâle getirmeyin.

---

## Misafir olarak ödeme yapana teşekkür sayfasında hesap oluşturma daveti göstermek kayıt oranını artırır mı?

Değişken: Teşekkür sayfasındaki hesap oluşturma daveti · Fark: ekle

Misafir ödemesi checkout sürtünmesini azaltır ama işletmeyi tekrar iletişim kurabileceği bir hesaptan mahrum bırakır. Sipariş tamamlandıktan hemen sonra, bilgiler zaten girilmişken hesap oluşturmayı önermek, checkout öncesinde zorunlu kayıt istemekten farklı bir sürtünme profiline sahiptir; kullanıcı artık kaybedecek bir dönüşümü riske atmıyor.

**Test edilmesi gerekenler**
- Hesap kullanımı: Davetle açılan hesaplara ilk ay içinde tekrar giriş yapılıyor mu, yoksa hesaplar açılıp unutuluyor mu?
- Sonraki test: Davet kazanırsa, siparişte verilen e-posta bilgisinin davet formunda hazır gelmesi ayrı bir testte kayıt oranını artırıyor mu?
- Zorunluluk: Daveti reddetmek gelecekteki alışverişi zorlaştırıyor mu, yoksa nötr mü?
- Sipariş algısı: Daveti gören kullanıcı siparişin tamamlandığından emin oluyor mu, yoksa hesap açmazsa siparişin geçersiz kalacağını mı düşünüyor?
- Segment: İlk kez alışveriş yapan ile daha önce misafir olarak alışveriş yapmış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Kayıt Oranı: Misafir ödemesi yapıp hesap oluşturan kullanıcı oranı artıyor mu?
- Tekrar Satın Alma Oranı: Misafir alıcıların ilan edilen pencerede (ör. 60 gün) yeniden sipariş verme oranı artıyor mu?
- Sipariş Netliği (anket): Davet, siparişin tamamlandığı algısını bulanıklaştırmamalı.
- E-posta Onay Oranı: Hesap oluşturma sürecinde bırakma artmamalı.
- Destek Talebi: “Siparişim nereye gitti, hesabım var mı” karışıklığı artmamalı.

**Yapılmaması gerekenler**
- Hesap oluşturmayı, sipariş onayını görmenin ön koşulu hâline getirmeyin; sipariş bilgisi davetten bağımsız her zaman görünür olmalı.
- Aynı testte davet metnini ve ön doldurma davranışını birlikte değiştirmeyin.
- Kullanıcı reddettiğinde bir daha aynı oturumda tekrar sormayın.
- Misafir ödemesini bu test yüzünden zorlaştırmayın; checkout akışının kendisine dokunmayın.
- Kullanıcının açıkça vermediği bir bilgiyle hesabı önceden doldurmayın.

---

## Teşekkür sayfasında arkadaşını davet et teklifini göstermek paylaşım oranını artırır mı?

Değişken: Arkadaşını davet et kartı · Fark: ekle

Kullanıcı memnuniyetinin tepe noktası satın alma anının hemen sonrasıdır; referans isteği için davranışsal olarak en uygun an burasıdır. Riski, teklifin asıl sipariş bilgisini gölgelemesi veya ödül teklifi gerçek değilse güven kaybı yaratmasıdır.

**Test edilmesi gerekenler**
- Sonraki test: Davet kartı kazanırsa, ödüllü davet ile ödülsüz basit paylaşım ayrı bir testte karşılaştırıldığında hangisi daha çok tıklanıyor?
- Kanal: Mesajlaşma uygulaması, e-posta veya link kopyalama seçeneklerinden hangisi en çok kullanılıyor?
- Tekrar görme: Daveti önceki siparişlerinde de görmüş müşteride paylaşım oranı, daveti ilk kez görene göre düşüyor mu?
- Davet edilen niteliği: Paylaşılan linkten gelen yeni müşteriler ilk siparişten sonra geri dönüyor mu, yoksa yalnızca ödül için mi geliyor?
- Cihaz: Mesajlaşma uygulamalarının elde olduğu mobilde davet kartı, masaüstüne göre daha mı çok paylaşım başlatıyor?

**Takip edilecek ana KPI’lar**
- Paylaşım Başlatma Oranı: Teşekkür sayfasına ulaşan alıcılar içinde davet paylaşımı başlatanların oranı (A’da diğer yüzeylerden yapılanlar dahil) artıyor mu?
- Referans Dönüşüm Oranı: Paylaşılan linkten gelen yeni müşteri sayısı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Davet, sipariş bilgisini gölgelememeli.
- Ödül Talep Oranı: Vaat edilen ödül gerçekten talep edilip kullanılabiliyor mu; edilmiyorsa bu bir bulgudur.
- Brüt Marj: Ödül maliyeti, davetle gelen siparişlerin marjını eritmemeli.

**Yapılmaması gerekenler**
- Vaat edilen ödülü gerçekte vermeyin ya da koşullarını sayfada belirtmeden bırakmayın (kural 6).
- Aynı testte teşvik türü ile paylaşım kanallarının sırasını birlikte değiştirmeyin.
- Daveti kapatılamaz hâle getirmeyin; kullanıcı sipariş bilgisine daveti görmeden de ulaşabilmeli.
- Kullanıcının rızası olmadan davet linkini otomatik olarak sosyal medyada paylaşmayın.
- Ödül tutarını gerçek maliyeti karşılamayacak kadar düşük tutup büyük vaat gibi sunmayın.

---

## Sipariş onayını rutin bir bilgi ekranı yerine akılda kalıcı bir an olarak tasarlamak sadakati artırır mı?

Değişken: Onay ekranındaki kutlama anı · Fark: ekle

Bir deneyim büyük ölçüde en yoğun anına ve nasıl bittiğine göre hatırlanır; sürecin geri kalanı ortalama olsa bile güçlü bir bitiş, deneyimin genel algısını yükseltebilir. Standart bir “siparişiniz alındı” ekranı yerine kısa bir kutlama animasyonu, kişiselleştirilmiş bir teşekkür mesajı veya beklenmedik küçük bir jest, satın alma sürecinin son izlenimini güçlendirebilir.

**Test edilmesi gerekenler**
- Sonraki test: Kutlama anı kazanırsa, kısa bir animasyon ile kişiselleştirilmiş metin ayrı bir testte karşılaştırıldığında hangisi daha akılda kalıcı bulunuyor?
- Fark edilme: Kullanıcılar kutlama anını izliyor mu, yoksa sipariş bilgisine ulaşmak için hemen geçiyor mu?
- Süre: Anın uzunluğu bir noktadan sonra sıkıcı mı geliyor?
- Destek etkisi: Kutlama anı eklenen ekranda “siparişim alındı mı” sorusuyla gelen destek talebi artıyor mu?
- Segment: İlk kez alışveriş yapan ile sadık müşteriye aynı an mı sunulmalı?

**Takip edilecek ana KPI’lar**
- Tekrar Satın Alma Oranı: Onay ekranına ulaşan alıcıların ilan edilen pencerede (ör. 60 gün) yeniden sipariş verme oranı artıyor mu?
- Marka Algısı (anket): İkincil sinyal; deneyimin genel algısı standart ekrana göre daha olumlu mu?
- Sosyal Paylaşım Oranı: Kullanıcı deneyimi kendiliğinden paylaşıyor mu?
- Sipariş Bilgisi Görünürlüğü: Kutlama anı asıl sipariş veya teslimat bilgisinin görünürlüğünü azaltmamalı.
- Sayfa Yüklenme Süresi: Animasyon veya ek görsel sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Kutlama anını, asıl sipariş bilgisini bulmayı zorlaştıracak şekilde tasarlamayın.
- Aynı testte anın biçimini (animasyon/metin) ve kişiselleştirme derecesini birlikte değiştirmeyin.
- Erişilebilirlik araçlarıyla uyumsuz, durdurulamayan bir animasyon kurmayın; hareket azaltma tercihini yok saymayın.
- Her siparişte aynı sürpriz jesti tekrarlayıp sürprizi öngörülebilir hâle getirmeyin.
- Kutlama anını, gerçekleşmemiş bir başarıyı (ör. sahte bir rozet veya ödül) ima edecek şekilde kurmayın.