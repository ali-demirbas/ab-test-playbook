# Finans, Sigorta ve Bireysel Emeklilik

Yolculuk aşaması: düzenlemeye tabi finansal ürünlerde (sigorta, hayat, bireysel emeklilik (BES)) web ve mobil uygulama akışları; ürünü tanıma, hesaplama, ön teklif, talep bırakma ve giriş yapmış müşterinin sözleşme işlemleri. Bu dosyadaki her varyant yayından önce uyum onayı ister: zorunlu bilgilendirme metinleri, cayma, onay ve kimlik doğrulama adımları test konusu yapılmaz (CLAUDE.md kural 6 ve 11), kurallar pazara göre değiştiği için bir pazarda onaylanan metin başka pazara taşınmaz. Formun kendi tasarımı `forms-signup.md`, talep formundaki alan sayısı `saas-b2b.md` içindedir; burada tekrar edilmezler. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Akordeondaki uzun ürün açıklamasını etiketli maddelere bölmek talebi artırır mı?

Değişken: Akordeon içindeki ürün açıklamasının biçimi · Fark: değiştir

Bir sigorta ürününün akordeonu açıldığında tek blok hâlinde uzun bir paragraf çıkıyorsa kullanıcı ürünün kimin için olduğunu, neyi kapsadığını ve neyi kapsamadığını satır satır aramak zorunda kalır. Aynı cümleleri “Kimler için”, “Neleri kapsar”, “Neleri kapsamaz” gibi etiketli maddelere bölmek taramayı kolaylaştırır, çünkü karar için aranan bilgi etiketinden bulunur. Riski: maddeleştirirken bir istisna ya da koşul cümlesi kısalır veya düşerse kullanıcı ürünü olduğundan geniş sanar; bu da talepten sonra vazgeçme ve şikâyet olarak geri döner. İki kolda metnin içeriği aynıdır, yalnızca biçimi değişir. “Güvenceleri madde listesi hâlinde vermek ikna ediyor mu?” (`home-landing.md`) senaryosundan farkı: orada pazarlama sayfasındaki güven vaatleri listelenir, burada düzenlemeye tabi bir ürünün kapsam metni bölünür ve metnin anlamı uyum onayıyla sabit tutulur.

**Test edilmesi gerekenler**
- Biçim: Etiketli maddeler, aynı içeriği taşıyan paragrafa göre talep bırakmayı artırıyor mu?
- Kapsam algısı: Maddeli sürümden gelen kullanıcı danışman görüşmesinde ürünün kapsamadığı durumları daha mı az soruyor?
- Okuma: Akordeonu açan kullanıcı maddeli sürümde metnin sonundaki talep butonuna kadar iniyor mu?
- Sonraki test: Maddeler kazanırsa, etiketlerin sırası (önce kapsam / önce kimler için) ayrı bir testte talebi değiştiriyor mu?
- Cihaz: Dar ekranda maddeli sürüm akordeonu uzatıp talep butonunu ekranın altına mı itiyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (ürün sayfasına atanan ziyaretçi başına): Maddeli açıklama talep bırakanların payını artırıyor mu?
- Akordeon Açma Oranı: Tanı metriği; değişiklik akordeonun içinde olduğu için iki kolda aynı çıkması beklenir.
- Talep Butonu Tıklama Oranı: Akordeonu açanlar içinde butona basanların payı yükseliyor mu?
- Başvuru Onay Oranı (90 gün): Maddeli sürümden gelen taleplerin onaylanıp poliçeye dönüşen payı düşmemeli.
- Destek Talebi: Kapsam ve istisnalarla ilgili soru ve şikâyet, atanan ziyaretçi başına artmamalı.

**Yapılmaması gerekenler**
- Aynı testte açıklamanın biçimi ile cümlelerin içeriğini birlikte değiştirmeyin; iki kolda aynı bilgi durmalı.
- Maddeleştirirken istisna, bekleme süresi veya koşul cümlelerini kısaltmayın ya da çıkarmayın; düzenlemeye tabi metin kelimesi kelimesine korunur.
- Maddeli sürümü uyum biriminin yazılı onayı olmadan yayına almayın; kapsam metni hedef pazarın kuralına bağlı bir bilgilendirmedir (kural 11).
- “Neleri kapsamaz” maddesini katlanmış, soluk veya en sona itilmiş biçimde göstermeyin (kural 6).
- Etiketleri ikon veya renkle süsleyip aynı testte görsel yoğunluğu da artırmayın.

---

## Hizmet tanıtımında açıklama cümlelerini ilgili adımın altına taşımak katılımı artırır mı?

Değişken: Tanıtım açıklamasının ekrandaki yeri · Fark: taşı

Fon dağılımını müşteri adına yöneten bir hizmetin tanıtım ekranında açıklama paragrafı üstte, üç adım (risk profilini belirle, öneriyi incele, onayla) altta durduğunda hangi cümlenin hangi adıma ait olduğunu kullanıcı kendi eşleştirir. Aynı cümleleri ait oldukları adımın altına taşımak, her adımda ne olacağını tam o adımın yanında söyler; belirsizlik azaldığı için başlama eşiği düşebilir. Riski: üstteki özet kalkınca hizmetin ne olduğu ilk bakışta anlaşılmayabilir ve adım listesi uzadığı için başlat butonu ekranın altına iner.

**Test edilmesi gerekenler**
- Yer: Açıklama cümleleri adımların altındayken hizmete katılım, cümleler üstte tek paragrafken olduğundan yüksek mi?
- İlk bakış: Üstteki paragraf kalkınca kullanıcı hizmetin ne yaptığını anlamadan tanıtım ekranından çıkıyor mu?
- Adım kaybı: Katılım akışını başlatanların risk profili sorularını bitirme payı iki kolda aynı mı?
- Sonraki test: Taşıma kazanırsa, adım altı cümlelerin açık ya da katlanmış gelmesi ayrı bir testte katılımı değiştiriyor mu?
- Kullanıcı tipi: Fon dağılımını daha önce kendisi değiştirmiş müşteri ile hiç değiştirmemiş müşteri taşınan açıklamaya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Özellik Katılım Oranı (teste atanan giriş yapmış müşteri başına): Hizmeti onaylayıp etkinleştiren müşterilerin payı artıyor mu?
- Akış Başlatma Oranı: Tanıtım ekranından ilk adıma geçenlerin payı; tanı metriği.
- Risk Profili Tamamlama Oranı: Akışı başlatanlar içinde soruları bitirenlerin payı; tanı metriği.
- 30 Gün İçinde Durdurma Oranı (30 gün): Hizmete katılan müşterilerden hizmeti bu pencerede durduranların payı artmamalı.
- Ücret Sorusu Oranı: Hizmetin ücreti ve işleyişi hakkında danışmana gelen sorular artmamalı.

**Yapılmaması gerekenler**
- Aynı testte cümlelerin yeri ile cümlelerin metnini birlikte değiştirmeyin; taşınan cümle kelimesi kelimesine aynı kalır.
- Hizmet ücretini, kesintiyi veya risk uyarısını taşırken küçültmeyin ya da bağlantı arkasına almayın; mevzuatın istediği bilgilendirme iki kolda aynı görünürlükte durur (kural 11).
- Geçmiş fon getirisini veya beklenen kazancı adım açıklamasına eklemeyin; getiri vaadi yazılmaz, rakam uydurulmaz.
- Onay adımını atlayan ya da risk profili sorularını azaltan bir akışı bu testin parçası yapmayın (kural 6).
- Adımların sayısını veya sırasını bu testte oynatmayın; üç adım iki kolda da aynıdır.

---

## Kişisel öneri vaat eden slayta vaadi adlandıran bir buton eklemek işe yarar mı?

Değişken: Öneri slaytındaki eylem butonu · Fark: ekle

Uygulamanın ana ekranındaki bir slayt “Size özel katkı payı önerimiz hazır” dediği hâlde üzerinde dokunulacak belirgin bir öğe yoksa müşteri vaadin nereden açılacağını bilemez. Slayta vaadi adlandıran bir buton (“Önerimi gör”) eklemek hem dokunulabilirliği işaretler hem dokununca ne çıkacağını söyler. Riski: buton merakla dokunmayı artırır, ama açılan ekran gerçekten kişisel değilse ya da beklenenden yüksek bir tutar öneriyorsa müşteri vazgeçer; dokunma artar, artırım artmaz. Bu yüzden birincil metrik dokunma değil, tamamlanan katkı payı artırımıdır.

**Test edilmesi gerekenler**
- Varlık: Butonlu slayt, butonsuz slayta göre katkı payı artırımını tamamlayan müşteri payını yükseltiyor mu?
- Vaat uyumu: Butona dokunan müşteri açılan ekranda kendi sözleşmesine göre hesaplanmış bir tutar mı buluyor?
- Görünürlük: Öneri slaytı kayan dizide ilk sırada değilken butonun etkisi kayboluyor mu?
- Sonraki test: Buton kazanırsa, buton metni (“Önerimi gör” / “Tutarı incele”) ayrı bir testte artırımı değiştiriyor mu?
- Segment: Son bir yılda katkı payını artırmış müşteri ile hiç artırmamış müşteri butona farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Katkı Payı Artırma Oranı (teste atanan giriş yapmış müşteri başına): Artırımı onaylayıp tamamlayanların payı artıyor mu?
- Slayt Dokunma Oranı: Tanı metriği; öneri ekranını açanların atanan müşteriye oranı.
- Öneriden Onaya Geçiş Oranı: Öneri ekranını açanların kaçı artırım onayına ilerliyor?
- Artırımı Geri Alma Oranı (90 gün): Artırım yapan müşterinin ilan edilen pencerede tutarı eski hâline çekme payı yükselmemeli.
- Diğer Slayt Dokunma Oranı: Butonlu slayt dizideki öbür slaytların dokunulmasını kabul edilemez ölçüde azaltmamalı.

**Yapılmaması gerekenler**
- Aynı testte butonu eklerken slaytın başlığını, görselini veya dizideki sırasını birlikte değiştirmeyin.
- Buton “Önerimi gör” diyorsa arkasında herkese aynı tutarı sunan genel bir ekran açmayın; vaat edilen kişisel öneri gerçek sözleşme verisinden hesaplanır (kural 6).
- Butona veya slayta “Son gün”, “Kaçırmayın” gibi aciliyet ifadesi ya da gerçek olmayan bir süre sınırı koymayın.
- Devlet katkısını, getiriyi veya birikim tutarını slayta rakamla yazmayın; uyum onayından geçmemiş hiçbir oran ya da tutar gösterilmez (kural 11).
- Artırım onayındaki bilgilendirmeyi kısaltmayın; buton yalnızca öneri ekranını açar, onayın yerine geçmez.

---

## Yalnızca ürün adlarından oluşan listenin başına “Hangisi bana uygun?” yönlendirmesi eklemek talebi artırır mı?

Değişken: Liste başındaki ürün seçme yönlendirmesi · Fark: ekle

Sigorta ürünleri yalnızca adlarıyla sıralandığında (“Ferdi Kaza”, “Yıllık Hayat”, “Kritik Hastalıklar”) ürünleri tanımayan ziyaretçi hangisine bakacağını bilemez; her birini tek tek açıp karşılaştırmak zorunda kalır. Listenin başına ihtiyaçtan ürüne götüren kısa bir yönlendirme (“Hangisi bana uygun?” başlığı altında “Ailemi korumak istiyorum”, “Borcumu güvenceye almak istiyorum” gibi birkaç seçenek) eklemek seçim yükünü azaltır, çünkü ziyaretçi ürün adını değil kendi ihtiyacını tanır. Riski: yönlendirme kişiye özel tavsiye gibi algılanırsa yanlış ürüne talep gelir; ayrıca liste aşağı itilir ve ne aradığını bilen ziyaretçi yavaşlar.

**Test edilmesi gerekenler**
- Varlık: Yönlendirme eklenen listede herhangi bir ürün için talep bırakanların payı artıyor mu?
- Eşleşme: Bir ihtiyaç seçen ziyaretçi yönlendirildiği ürünün sayfasında mı kalıyor, yoksa listeye geri mi dönüyor?
- Bilen ziyaretçi: Aradığı ürünü doğrudan açan ziyaretçinin ürüne ulaşma süresi uzuyor mu?
- Sonraki test: Yönlendirme kazanırsa, ihtiyaç seçeneklerinin sayısı (3 / 5) ayrı bir testte talebi değiştiriyor mu?
- Kategori: Hayat, sağlık ve kaza ürünlerinde yönlendirmenin etkisi aynı mı, yoksa tek bir ürün grubunda mı toplanıyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (liste ekranına atanan ziyaretçi başına): Herhangi bir üründe talep bırakanların payı artıyor mu?
- Liste → Ürün Tıklama Oranı: Listeden bir ürün sayfasına geçenlerin payı; tanı metriği.
- Listeye Geri Dönüş Oranı: Ürün sayfasından listeye dönenlerin payı; eşleşme tutmuyorsa yükselir.
- Başvuru Onay Oranı (90 gün): Gönderilen taleplerden onaylananların payı gerilememeli; yanlış ürüne yönlenen talep burada görünür.
- Cayma Süresi İçinde İptal Oranı (yasal cayma süresi): Yönlendirmeyle alınan poliçelerde cayma çoğalmamalı.

**Yapılmaması gerekenler**
- Aynı testte yönlendirmeyi eklerken ürünlerin sırasını, adlarını veya kart tasarımını birlikte değiştirmeyin.
- Yönlendirmeyi kişiye özel tavsiye gibi sunmayın (“Sizin için en doğru ürün”); genel bilgilendirme ile tavsiye arasındaki sınırı hedef pazarın kuralına göre uyum birimiyle doğrulayın (kural 11).
- İhtiyaç seçeneklerinin hepsini aynı ürüne ya da komisyonu yüksek ürüne bağlamayın; eşleşme ürünün gerçek kapsamına dayanır (kural 6).
- Yönlendirmeyi kapatılamayan bir katman olarak açmayın; ürün listesi onun altında her zaman erişilebilir kalır.
- Yönlendirmede sağlık durumu veya gelir gibi hassas bilgileri sormayın; seçenekler ihtiyaç düzeyinde kalır (kural 14).

---

## Sözleşme seçimi adımına ne yapılacağını söyleyen bir yönerge satırı eklemek ilerlemeyi artırır mı?

Değişken: Sözleşme seçimi adımındaki yönerge satırı · Fark: ekle

Birden fazla sözleşmesi olan müşteri bir işlem akışına girdiğinde (katkı payı değişikliği, fon dağılımı, ödeme aracı güncelleme) ilk ekranda sözleşmelerin listesini ve pasif bir “Devam” butonunu bulur; ne yapması gerektiği yazmıyorsa butonun neden çalışmadığını anlamaz ve çıkar. Listenin üstüne tek satırlık bir yönerge (“İşlem yapmak istediğiniz sözleşmeyi seçin”) eklemek beklenen eylemi söyler. Riski: satır fark edilmezse hiçbir şey değişmez. “Daha hızlı olsun” diye sözleşmeyi önceden işaretlemek cazip görünür, ama işlemin kapsamını müşteri yerine seçmek olur; o yüzden bu senaryonun dışındadır ve aşağıda yasak olarak yazılıdır.

**Test edilmesi gerekenler**
- Varlık: Yönerge satırı eklenince seçim adımına gelen müşterilerin işlemi tamamlama payı artıyor mu?
- Takılma: Hiçbir sözleşme seçmeden pasif “Devam” butonuna dokunma denemeleri azalıyor mu?
- Yanlış seçim: İşlemi bitiren müşterinin sonradan düzeltme isteme payı iki kolda aynı mı?
- Sonraki test: Yönerge kazanırsa, pasif butona dokunulduğunda satırın vurgulanması ayrı bir testte ilerlemeyi artırıyor mu?
- Segment: Tek sözleşmeli müşteri ile birden fazla sözleşmesi olan müşteri yönergeye farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı (seçim adımına ulaşan müşteri başına, iki kolda aynı tetikleyici): Akışın işini (ör. katkı payı değişikliği) bitirenlerin payı artıyor mu?
- Sözleşme Seçim Oranı: Adıma gelenlerin en az bir sözleşme işaretleme payı; tanı metriği.
- Pasif Butona Dokunma Oranı: Seçim yapmadan “Devam”a dokunan müşteri payı azalıyor mu?
- İşlem Düzeltme Oranı (30 gün): Biten işlemin ilan edilen pencerede geri alınma ya da düzeltilme payı artmamalı.
- Yanlış Sözleşme Şikâyeti Oranı: İstenmeyen sözleşmede işlem yapıldığı gerekçesiyle açılan kayıtlar çoğalmamalı.

**Yapılmaması gerekenler**
- Sözleşme kutusunu önceden işaretli getirmeyin; işlemin hangi sözleşmeyi kapsayacağını müşteri yerine seçmek reddedilen bir varyanttır (kural 6).
- Aynı testte yönerge satırını eklerken sözleşme kartlarının içeriğini veya “Devam” butonunun metnini birlikte değiştirmeyin.
- Yönergeyi “Tümünü seç” kısayoluna çevirmeyin; kapsamı genişleten bir varsayılan bu testin konusu olamaz.
- Seçimden sonraki bilgilendirme ve işlem onayı ekranını atlamayın ya da daraltmayın; mevzuatın istediği onay adımı iki kolda aynen durur (kural 11).
- Yönerge satırına sözleşmenin birikimi, getirisi veya kesintisi hakkında yeni bir rakam ya da vaat yazmayın; satır yalnızca yapılacak eylemi söyler.

---

## Hesaplama sonuç ekranına sonucu talebe bağlayan bir buton eklemek talep oluşturmayı artırır mı?

Değişken: Hesaplama sonuç ekranındaki talep butonu · Fark: ekle

Emeklilik birikimi ya da prim hesaplama aracı sonucu gösterip orada bitiyorsa ziyaretçi en ilgili olduğu anda çıkmaza girer: sonucu almıştır ama devam etmek için menüden başka bir sayfa bulması gerekir. Sonuç ekranına talep formunu açan bir buton (“Bu hesapla teklif iste”) eklemek ilgiyi eyleme bağlar. Riski: araç yalnızca merak eden ziyaretçiden düşük niyetli talep toplar ve danışman ekibinin yükü artar; ayrıca hesaplanan tutar bir taahhüt gibi okunursa teklif aşamasında hayal kırıklığı doğar.

**Test edilmesi gerekenler**
- Varlık: Sonuç ekranına buton eklemek, hesaplamayı bitirenlerin talep bırakma payını artırıyor mu?
- Talep niteliği: Butondan gelen talep, menüden gelen talebe göre danışman görüşmesine daha mı az dönüşüyor?
- Erken ayrılma: Buton eklenince ziyaretçi farklı değerlerle tekrar hesaplamayı bırakıp sonuç ekranından erken mi çıkıyor?
- Sonraki test: Buton kazanırsa, hesaplamada girilen değerleri talep formuna hazır taşımak ayrı bir testte form tamamlamayı artırıyor mu?
- Cihaz: Mobil web ve masaüstünde buton sonuç tablosunun üstünde mi kalıyor, yoksa kaydırmadan görünmüyor mu?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (hesaplamayı tamamlayan ziyaretçi başına, iki kolda aynı tetikleyici): Sonuç ekranına ulaşanlar içinde talep bırakanların payı artıyor mu?
- Hesaplama Tamamlama Oranı: Değişiklik sonuç ekranında olduğu için iki kolda eşit çıkması beklenir; fark atama ya da ölçüm hatasına işaret eder.
- Yeniden Hesaplama Oranı: Sonuç ekranında değerleri değiştirip tekrar hesaplayanların payı; tanı metriği.
- Başvuru Onay Oranı (90 gün): Sonuç ekranından gelen başvurularda onaylananların payı düşmemeli.
- Ulaşılamayan Talep Oranı: Danışmanın aradığında ulaşamadığı ya da ilgisiz çıkan taleplerin payı artmamalı.

**Yapılmaması gerekenler**
- Aynı testte butonu eklerken sonuç tablosunun içeriğini, varsayımlarını veya hesaplama formülünü birlikte değiştirmeyin.
- Sonucu garanti edilmiş getiri ya da kesin prim gibi sunan bir buton metni yazmayın (“Bu birikimi garantile”); hesap bir tahmindir ve varsayım notu iki kolda yerinde kalır (kural 11).
- Butonu, sonucu görmek için iletişim bilgisi isteyen bir kapıya çevirmeyin; sonuç iki kolda da talepsiz görünür (kural 6).
- Butona dokunmayı talep saymayın; iletişim izni ve aydınlatma metni formda aynen durur, buton onların yerine geçmez.
- “Bu teklif yalnızca bugün geçerli” gibi süre baskısı kuran ifadeleri butonun yanına koymayın.

---

## Ön teklif formunda kimlik numarası alanının yanına neden istendiğini yazmak teklif almayı artırır mı?

Değişken: Kimlik numarası alanının yanındaki gerekçe satırı · Fark: ekle

Sigorta ya da emeklilik ön teklif formunda kimlik numarası veya doğum tarihi alanı, henüz fiyat bile almamış ziyaretçiye ağır gelir: “neden şimdi istiyorlar” sorusu yanıtsız kalınca form orada bırakılır. Alanı kaldırmak çoğu zaman mümkün değildir, çünkü teklif bu bilgiyle hesaplanır; kural 14’teki ara yöntemlerden biri olan gerekçe vermek, alanın yanına bilginin ne için kullanılacağını yazar (“Primi yaşınıza göre hesaplayabilmemiz için gerekir”). Riski: gerekçe yayımlanan aydınlatma metniyle birebir örtüşmezse yanıltıcı olur; ayrıca gerekçe, ziyaretçinin aklına gelmemiş bir kaygıyı uyandırabilir. “Alanın yanına “neden soruyoruz” açıklaması eklemek, amacı belirsiz görünen bir alanı doldurtur mu?” (`saas-b2b.md`) senaryosundan farkı: orada alan hassas olmayan bir niteleme sorusudur ve ölçülen o alanın doldurulmasıdır; burada alan zorunlu ve hassastır, gerekçenin metni kişisel veri kurallarına bağlıdır ve ölçülen teklifin alınmasıdır.

**Test edilmesi gerekenler**
- Varlık: Gerekçe satırı eklenince ön teklif formunu gönderip teklif isteyenlerin payı artıyor mu?
- Alan düzeyi: Kimlik numarası alanına gelip formu orada bırakanların payı azalıyor mu?
- Ters etki: Gerekçe, alanı sorgulamadan dolduran ziyaretçide tereddüt uyandırıp doldurma süresini uzatıyor mu?
- Sonraki test: Gerekçe kazanırsa, bilginin nasıl korunduğunu söyleyen bir güvence satırı ayrı bir testte teklif almayı artırıyor mu?
- Segment: Reklamdan ilk kez gelen ziyaretçi ile mevcut müşteri gerekçeye farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (ön teklif formuna atanan ziyaretçi başına): Formu gönderip teklif isteyenlerin payı artıyor mu?
- Alan Bazlı Terk Oranı: Kimlik numarası alanında formu bırakanların payı; tanı metriği.
- Doğrulama Hatası Oranı: Geçersiz ya da doğrulanamayan numara girişleri artmamalı.
- Teklif → Sözleşme Dönüşüm Oranı (90 gün): Gerekçeli formdan gelen tekliflerin sözleşmeye dönüşen payı düşmemeli.
- Veri Şikâyeti Oranı: Kişisel verinin kullanımıyla ilgili başvuru ve şikâyetler çoğalmamalı.

**Yapılmaması gerekenler**
- Aynı testte gerekçe satırını eklerken alanın zorunluluğunu, sırasını veya etiketini birlikte değiştirmeyin.
- Alanı tümden kaldırmayı ya da kimlik doğrulamasını gevşetmeyi bu senaryonun varyantı yapmayın; doğrulama bir koruma adımıdır (kural 6), alanın kaldırılıp kaldırılamayacağı ayrıca sorulur (kural 14).
- Gerekçeyi yayımlanan aydınlatma metninde yer almayan bir amaçla yazmayın; cümle hukuk ve uyum onayından geçmeden yayına girmez (kural 11).
- “Bilginiz kimseyle paylaşılmaz” gibi doğrulanmamış bir güvenceyi gerekçe satırına katmayın; güvence ayrı bir değişkendir ve gerçek veri akışına uymak zorundadır.
- Gerekçe satırını açık rıza ya da ticari ileti izni kutusunun yanına koyup izni vermeye yönlendiren bir metne dönüştürmeyin.

---

## Teklif akışındaki adım göstergesinde numaraların yanına adım adlarını yazmak sözleşmeye ulaşmayı artırır mı?

Değişken: Adım göstergesindeki adım etiketleri · Fark: değiştir

Teklif akışında yalnızca numara gösteren bir gösterge (“2 / 4”) kullanıcıya kaçıncı adımda olduğunu söyler ama sırada ne olduğunu söylemez: fiyatı hangi adımda alacağını, ödemenin ne zaman isteneceğini bilmeyen kullanıcı kişisel bilgi vermeye isteksiz davranır. Numaraların yanına adımların adını yazmak (“1 Bilgiler, 2 Teminat, 3 Teklif, 4 Onay”) yolu önceden gösterir; fiyatın üçüncü adımda geleceğini bilen kullanıcı ilk iki adımı bitirmeye daha yatkın olabilir. Riski: adlar akışı olduğundan uzun gösterebilir ve dar ekranda sığmayıp kırpılır. “İlerleme çubuğu tamamlama oranını artırıyor mu?” (`cart-checkout.md`) senaryosundan farkı: orada göstergenin kendisi eklenir, burada gösterge iki kolda da vardır ve yalnızca adımların adlandırılması değişir.

**Test edilmesi gerekenler**
- Adlandırma: Adım adları yazan gösterge, yalnızca numara gösteren göstergeye göre akışı sözleşmeyle bitirenlerin payını artırıyor mu?
- Fiyat beklentisi: Fiyatın hangi adımda geleceğini adından öğrenen kullanıcı ilk adımdaki kişisel bilgileri daha mı çok tamamlıyor?
- Geri dönüş: Adlı göstergede önceki adıma dönüp bilgi düzeltme sıklığı değişiyor mu?
- Sonraki test: Adlandırma kazanırsa, biten adımların göstergeden tıklanabilir olması ayrı bir testte tamamlamayı artırıyor mu?
- Cihaz: Dar ekranda dört adım adı tek satıra sığıyor mu, yoksa mobilde kırpılan adlar etkiyi siliyor mu?

**Takip edilecek ana KPI’lar**
- Teklif → Sözleşme Dönüşüm Oranı (teklif akışına atanan ziyaretçi başına): Akışı sözleşmeyle bitirenlerin payı artıyor mu? Gösterge teklif ekranından önceki adımlarda da durduğu için payda atanan ziyaretçidir.
- Teklif Görüntüleme Oranı: Fiyatın gösterildiği adıma ulaşanların payı; tanı metriği.
- Adım Bazlı Terk Oranı: Hangi adımda bırakıldığını gösteren tanı metriği.
- Cayma Süresi İçinde İptal Oranı (yasal cayma süresi): Adlı göstergeyle biten sözleşmelerde cayma artmamalı.
- Erişilebilirlik: Adım adları ekran okuyucuda sırayla okunmalı; etkin adımın yalnızca renkle ayrılması kabul edilmemeli.

**Yapılmaması gerekenler**
- Aynı testte adım adlarını yazarken adımların sayısını, sırasını veya adımlardaki alanları birlikte değiştirmeyin.
- Bilgilendirme formu, onay veya kimlik doğrulama adımını göstergede gizlemeyin ya da başka bir adın altına saklamayın; zorunlu adımlar adıyla görünür ve akışta aynen kalır (kural 6 ve 11).
- Göstergede yazmayan bir adımı (ör. ödeme) akışın sonunda sürpriz olarak çıkarmayın; adlar gerçek akışla birebir örtüşür.
- Adım adına “Ücretsiz teklif” ya da “Anında onay” gibi doğrulanmamış bir vaat yazmayın; ad yalnızca adımın işini söyler ve uyum onayından geçer.
- Adım adlarını dar ekranda okunmayacak kadar küçültmeyin veya üç noktayla kırpılmış bırakmayın.

---

## Hesaplama aracını müşterinin mevcut sözleşme verisiyle dolu açmak hesaplamayı tamamlatır mı?

Değişken: Hesaplama aracındaki alanların başlangıç değeri · Fark: değiştir

Giriş yapmış müşteri uygulamadaki birikim hesaplama aracını açtığında yaş, aylık katkı payı ve mevcut birikim alanları boş geliyorsa, şirketin zaten bildiği bilgiyi yeniden yazması istenir; çoğu müşteri katkı payı tutarını ezbere bilmez ve araç yarıda kalır. Alanları müşterinin kendi sözleşme verisiyle dolu açmak yazma yükünü kaldırır ve sonucu ilk dokunuşta kişisel kılar. Riski: veri eski ya da yanlış sözleşmeden gelirse sonuç yanlış olur ve müşteri bunu fark etmeyebilir; birden fazla sözleşmesi olan müşteride hangisinin kullanıldığı açık değilse güven zedelenir. Dolu gelen her alan düzenlenebilir kalır; değişen yalnızca başlangıç değeridir. Bu bir benzetim aracıdır: bir işlemin kapsamını önceden seçmekle aynı şey değildir ve hiçbir işlemi başlatmaz.

**Test edilmesi gerekenler**
- Başlangıç değeri: Alanlar sözleşme verisiyle dolu açıldığında hesaplamayı sonuca ulaştıran müşteri payı, boş açılana göre yüksek mi?
- Düzenleme: Dolu gelen değerleri değiştirip farklı bir katkı payıyla yeniden hesaplayan müşteri payı ne kadar?
- Doğruluk: Dolu gelen değerlerin güncel kayıtlarla uyuşmadığı müşteriler aracı yarıda mı bırakıyor?
- Sonraki test: Dolu başlangıç kazanırsa, sonuç ekranına katkı payı artırma butonu eklemek ayrı bir testte artırımı yükseltiyor mu?
- Platform: iOS ve Android uygulamasında verinin yüklenme süresi farklıyken dolu başlangıcın etkisi aynı mı?

**Takip edilecek ana KPI’lar**
- Hesaplama Tamamlama Oranı (aracı açan giriş yapmış müşteri başına, iki kolda aynı tetikleyici): Sonuç ekranına ulaşanların payı artıyor mu?
- Katkı Payı Artırma Oranı (30 gün): Hesaplama bir ara adım olduğu için asıl sonuç burada izlenir; artırım yapan müşteri payı düşmemeli, trafik yetiyorsa birincil metrik bu olur.
- Değer Düzenleme Oranı: Dolu gelen alanlardan en az birini değiştirenlerin payı; tanı metriği, B kolunda okunur.
- Hatalı Veri Bildirimi Oranı: Yanlış ya da eski bilgi gösterildiği gerekçesiyle açılan kayıtlar artmamalı.
- Araç Açılış Süresi: Sözleşme verisini çekmek ekranın açılmasını kabul edilemez ölçüde geciktirmemeli.

**Yapılmaması gerekenler**
- Aynı testte alanları dolu açarken alanların sayısını, sırasını veya sonuç ekranının tasarımını birlikte değiştirmeyin.
- Dolu gelen alanları kilitlemeyin; müşteri her değeri değiştirebilir ve değerin hangi sözleşmeden, hangi tarihte alındığı alanın altında yazar.
- Getiri oranı, enflasyon veya devlet katkısı varsayımını müşteri verisi gibi sessizce doldurmayın; varsayımlar uyum onaylı metniyle ayrı gösterilir, yeni oran uydurulmaz (kural 11).
- Aracı, aydınlatma metninde bildirilmeyen bir amaçla işlenen veriyle doldurmayın (ör. başka şirketteki birikim, tahmini gelir).
- Dolu açılan hesaplamayı müşteri adına başlatılmış bir artırım talebi gibi kaydetmeyin; hesaplama hiçbir işlemi kendiliğinden başlatmaz (kural 6).

---

## “Sizi arayalım” formuna talepten sonra kimin, hangi kanaldan döneceğini yazmak talebi artırır mı?

Değişken: Talep formundaki sonraki adım satırı · Fark: ekle

“Sizi arayalım” formu ad ve telefon ister ama gönderdikten sonra ne olacağını söylemez: kim arayacak, hangi kanaldan, ne için? Belirsizlik iki yerde kayıp yaratır: bilinmeyen bir satış aramasından çekinen ziyaretçi formu göndermez, gönderen ise tanımadığı numarayı açmaz. Butonun üstüne sürecin gerçekte nasıl işlediğini söyleyen tek satır (“Müşteri danışmanımız sizi telefonla arar ve sorularınızı yanıtlar”) eklemek beklentiyi kurar. Riski: satır şirketin gerçekten yürütmediği bir süreci anlatırsa vaat tutulmaz ve şikâyete dönüşür; arama fikri netleşince bazı ziyaretçiler de vazgeçebilir.

**Test edilmesi gerekenler**
- Varlık: Sonraki adımı söyleyen satır eklenince formu gönderenlerin payı artıyor mu?
- Ulaşılabilirlik: Satırlı formdan talep bırakan ziyaretçi danışmanın ilk aramasını daha mı çok açıyor?
- Caydırma: Aranacağını açıkça öğrenen ziyaretçilerin bir kısmı formu göndermekten vazgeçiyor mu?
- Sonraki test: Satır kazanırsa, aranmak istenen zaman dilimini seçtirmek ayrı bir testte ulaşılan talebi artırıyor mu?
- Mobil: Uygulamadaki form ile mobil web formunda satırın etkisi aynı mı?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (form ekranına atanan ziyaretçi başına): Formu gönderenlerin payı artıyor mu?
- Talebe Ulaşma Oranı: Danışmanın ilan edilen deneme sayısı içinde ulaşabildiği taleplerin payı düşmemeli.
- Görüşmeden Teklife Geçiş Oranı: Ulaşılan taleplerin kaçı teklif aşamasına ilerliyor?
- Arama Şikâyeti Oranı: “Aranmadım” ya da “istemediğim hâlde arandım” şikâyetleri artmamalı.
- İleti İzni Geri Çekme Oranı (90 gün): Talep bırakanların iletişim iznini geri çekme payı yükselmemeli.

**Yapılmaması gerekenler**
- Ölçülmemiş bir geri dönüş süresi vaat etmeyin (“10 dakika içinde arıyoruz”); süre ancak çağrı kayıtlarıyla doğrulanmış ve her talepte tutulabiliyorsa yazılır.
- Satırda şirketin gerçekte yürütmediği bir süreci anlatmayın; arayan dış arama ekibiyse ya da ilk temas SMS ise satır bunu söyler ve uyum onayından geçer.
- Aynı testte sonraki adım satırını eklerken form alanlarını veya buton metnini birlikte değiştirmeyin.
- Satırı iletişim izni ve aydınlatma metninin yerine koymayın, izin kutusunu önceden işaretlemeyin; izin metni onaylı hâliyle aynen kalır (kural 6 ve 11).
- “Danışmanlarımız şu an müsait” gibi gerçek zamanlı veriye dayanmayan bir doluluk ya da aciliyet sinyali eklemeyin.
