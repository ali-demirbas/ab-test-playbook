# Metodoloji — Her Senaryonun Uyması Gereken Çerçeve

Bu playbook'taki her senaryo (arşivden gelen veya yeni üretilen) aynı çerçeveyle yazılır. Bu dosya bağlayıcıdır: `abtest-design` yeni senaryo üretirken, `abtest-audit` mevcut bir planı denetlerken buradaki kuralları uygular.

## Üç kutu çerçevesi

Her senaryo üç bloktan oluşur, üçü de zorunludur ve her biri tam 5 maddeden oluşur (`validate_scenarios.py` bunu şart koşar):

1. **Test edilmesi gerekenler** — hipotezi hangi soruların doğrulayacağı. Her madde `Etiket: soru?` biçimindedir (ör. `Konum: Header'da mı, menü içinde mi?`). Maddelerden en az biri cihaz/segment kırılımı sorar.
2. **Takip edilecek ana KPI’lar** — ölçüm seti. Kurallar aşağıda. (Kutu adındaki kesme işareti kıvrıktır — U+2019; düz kesme ile yazılan başlığı doğrulayıcı tanımaz.)
3. **Yapılmaması gerekenler** — testi geçersiz kılan veya kullanıcıya zarar veren hatalar. En az bir madde "aynı testte X ile Y'yi birlikte değiştirmeyin" biçiminde değişken izolasyonunu korur.

## KPI kuralları

- İlk sıradaki metrik **birincil metriktir** — testin kazananını tek başına o belirler. Beş metriği eşit ağırlıkta okumak p-hacking'e davetiyedir.
- Listede en az bir **guardrail** bulunur: dönüşüm artarken bozulabilecek şey. Tipik guardrail'ler: brüt marj, iade oranı, sayfa hızı (LCP), destek talebi, terk oranı, RPV. Guardrail maddeleri "Düşmemeli / Yükselmemeli / Artmamalı" kalıbıyla yazılır. Guardrail'i olmayan kazanç, ertelenmiş bir kayıptır: testte ölçmediğiniz maliyet iptal edilmez, yalnızca sonraki çeyreğin iade oranına veya destek yüküne taşınır.
- Metrik, aracın gerçekten ölçebileceği bir şey olmalı. "Güven algısı" bir KPI değildir; onun vekili (proxy) yazılır.
- **Ara adım metriği tamamlamayı gizleyebilir.** Bir değişiklik huninin ortasındaki bir adımı (sepete ekleme, ödeme başlatma, formu açma, hızlı ödeme seçme) kolayca artırabilir ve bu ilk bakışta kazanç gibi görünür — ama o adımı daha kolay geçen kullanıcı bir sonrakinde takılıyorsa toplam sipariş değişmez, hatta düşer. Özellikle bir akışı hızlandıran, atlayan veya öne çıkaran varyantlarda risk yüksektir: kullanıcı henüz vermediği bir kararın sonucuna fırlatılır ve geri döner. Bu yüzden birincil metrik daima huninin sonundaki gerçek sonuçtur (tamamlanan sipariş, gönderilen form); ara adım metriği tanı metriği olarak ikinci sırada izlenir. İkisi ters yönde hareket ediyorsa bulgu budur.
- **Dönüşüm oranı geliri gizleyebilir.** Fiyat, taksit, indirim veya paket testlerinde birincil metrik olarak salt "Dönüşüm Oranı (CR)" yeterli değildir — fiyat düşürmek CR'yi neredeyse her zaman artırır ama geliri düşürebilir. Bu tür senaryolarda birincil metrik gelir bazlı olmalı: Ziyaretçi Başına Gelir (RPV) veya Ortalama Sepet Tutarı (AOV) × CR. `knowledge/scenarios/product-detail.md` ve `cart-checkout.md`'deki fiyat senaryoları bu ayrımı zaten uygular; yeni fiyat/paket senaryosu üretilirken aynı kural geçerlidir.

## Hipotez üç parçalıdır

Tek cümlelik hipotez ("X'i Y yapmak Z'yi artırır") yetmez, üç ayrı soruya cevap vermelidir:

1. **Teori:** Bu değişikliği neden öneriyoruz? Hangi gözlem, veri veya kullanıcı geri bildirimi bu hipotezi doğurdu?
2. **Dayanak:** Bu teoriyi destekleyen somut kanıt ne? (Bir metrik, bir kullanıcı yorumu, bir davranış deseni.) Kanıt yoksa "sezgi" olarak işaretlenir, güven düzeyi buna göre düşük tutulur. Dayanak dört seviyeden biriyle etiketlenir ve çıktıda görünür:
   - **Kullanıcının kendi verisi** — bu üründe/sayfada ölçülmüş bir sinyal (en güçlü).
   - **Arşiv emsali** — benzer bağlamda daha önce test edilmiş bir desen.
   - **Sektör gözlemi** — yaygın pratik, ama bu ürüne özel doğrulaması yok.
   - **Sezgi** — hiçbiri yok; öneri verilebilir ama düşük güvenli olduğu söylenir.
3. **Öğrenilecek şey:** Test kazanırsa ne öğreniriz, kaybederse ne öğreniriz? İkisi de bilgi üretmiyorsa test zaten kurgusu zayıf demektir.

`abtest-design` her senaryonun açıklama paragrafında bu üçünü zımnen taşır; kullanıcı açıkça isterse üçü ayrı ayrı yazılır. Tek cümlelik doldurma şablonu:

> "[Gözlem/veri]'ye dayanarak, [değişiklik] yaparsak [hedef kitle] için [beklenen sonuç] olacağını düşünüyoruz. Bunu [metrik]'te göreceğiz."

Zayıf örnek: "Buton rengini değiştirmek tıklamayı artırabilir." (Dayanaksız, sonuç ölçülemez netlikte.)
Güçlü örnek: "Mobil kullanıcıların CTA'yı geç fark ettiğini ısı haritalarından biliyoruz; butonu büyütüp kontrastı artırırsak yeni ziyaretçilerde tıklama oranı en az %15 artar. Bunu sayfa görüntülemeden kayda geçiş oranında göreceğiz."

Değişiklik metrikte fark yaratamayacak kadar silikse (ör. 2px kenarlık kalınlığı) hipotez kurmayın; "bu değişiklik fark edilecek kadar belirgin mi?" sorusu her senaryo tasarımının ilk filtresidir.

**Hangi itirazı çözüyoruz?** Bir kullanıcı bir adımı tamamlamıyorsa altında çoğu zaman adı konmamış bir itiraz vardır. Beş kalıp tekrar eder:

| İtiraz | Kullanıcının sorusu | Tipik karşılık |
|---|---|---|
| Güven | "Neden buna inanayım?" | İsimli referans, somut kanıt, güvenlik sinyali |
| Fiyat | "Buna değer mi?" | Değer karşılaştırması, taksit, ROI gösterimi |
| Uygunluk | "Bu benim durumuma uyar mı?" | Benzer kullanıcı örneği, segment bazlı içerik |
| Zamanlama | "Neden şimdi?" | Gerçek (uydurma olmayan) aciliyet, fırsat maliyeti |
| Efor | "Bu ne kadar zor olacak?" | "5 dakikada kurulum", adım adım gösterim |

Hipotez kurarken hangi itirazın hedeflendiğini bir kelimeyle adlandırmak, testin neden işe yarayacağını (veya yaramayacağını) daha net gösterir. Kanıt varsa (destek talebi, iptal nedeni, anket yanıtı) hangi itiraza denk geldiği söylenir; yoksa varsayım olarak işaretlenir. İtiraz kapatan mesaj örtük de kurulabilir — "Tembel olduğunuzdan mı endişeleniyorsunuz?" gibi itirazı doğrudan söylemek yerine "Bu işi sizin yerinize hallediyoruz" gibi doğrudan çözüme geçmek genelde daha iyi çalışır; itirazı yüksek sesle söylemek onu güçlendirebilir.

**İstatistiksel anlamlılık ≠ pratik anlamlılık.** `p < 0.05` çıkması tek başına "uygula" demek değildir. %0,1'lik istatistiksel olarak anlamlı bir lift, uygulama/bakım maliyetine değmeyebilir. Sonuç yorumlanırken iki soru ayrı sorulur: (1) İstatistiksel olarak gerçek mi? (2) Mutlak büyüklüğü, değişikliği kalıcı hale getirmenin mühendislik/tasarım/operasyon maliyetini karşılıyor mu? İkinci soru bir sayı değil, bir karardır — `abtest-results` bunu "uygulanabilir" kararının bir parçası olarak sorar.

## Fikir üretme merceği

Fikirler sayfaya bakılıp akla gelenin yazılmasıyla üretilmez. Dört filtre sırayla uygulanır.

**1. Fırsat taraması.** Yukarıdaki beş itiraz merceği (Güven, Fiyat, Uygunluk, Zamanlama, Efor) fırsat taraması için kullanılır: her itiraz için bu sayfada gerçek bir karşılıksızlık veya kullanıcı engeli var mı diye bakılır. Karşılığı zaten varsa o mercek atlanır. **Her mercekten fikir üretmek zorunlu değildir**; ilgisiz bir mercekten fikir zorlamak sayfayla alakası olmayan öneri üretir (checkout adımında "uzman görüşü ekleyelim" gibi). Tarama, ekranda olana ek olarak olması gerekip olmayanı da görünür kılar (bkz. Değişken izolasyonu → ekleme ekseni).

**2. Mekanizma kapısı.** Her aday "bu değişiklik kullanıcı davranışını neden değiştirsin?" sorusuna somut cevap vermek zorundadır. "Daha dikkat çekici olur", "daha modern görünür", "daha temiz olur" cevap değildir; bu adaylar önerilmez. Mekanizma **sayfada gözlemlenebilen bir kullanıcı engeline** dayanmalıdır, genel bir psikoloji iddiasına değil:

- Mekanizma değil: "Sosyal kanıt güveni artırır."
- Mekanizma: "Bu sayfada kullanıcı ürünün kalitesini değerlendirecek bir kanıt göremiyor; doğrulanabilir kullanıcı değerlendirmesini karar noktasına taşımak bu belirsizliği azaltır."

Mekanizma hipotezin **Teori** kısmına yazılır; yeni bir çıktı alanı açılmaz. İki sınırı vardır:

- **Kapı yalnızca playbook'un kendiliğinden ürettiği adaylara uygulanır.** Kullanıcı açıkça bir testi istiyorsa (ör. "butonu kırmızı yapalım") test reddedilmez: kurulur, ama mekanizmasının zayıf olduğu açıkça söylenir ve daha güçlü mekanizmalı bir alternatif yanına konur. Reddedilen tek şey dark pattern'dir (kural 6).
- **Mekanizma ile dayanak farklı eksenlerdir.** Dayanak "bu problem gerçekten var mı" sorusudur (kanıt seviyesi, kural 10); mekanizma "varsa bu değişiklik neden çözer" sorusudur. Güçlü mekanizma ile `Kanıt: sezgi` birlikte bulunabilir ve bu aday elenmez — yalnızca güven düzeyi düşük olarak işaretlenir.

**3. Mekanizma tekrarı kontrolü.** Aynı sayfa alanında aynı davranış mekanizmasına dayanan fikirler farklı kelimelerle ayrı öneri olarak sunulmaz; birleştirilir veya en güçlüsü seçilir. "Sosyal kanıt ekle", "yorumları görünür yap", "popüler ürünleri öne çıkar" üç fikir değil, tek mekanizmanın üç ifadesidir.

**4. Etki sıralaması — yasak değil, sıra.** Kapıdan geçen birden fazla aday varsa şu sırayla önceliklendirilir:

1. Teklifin kendisi, akıştan bir adımın kalkması, karar anında eksik bilginin eklenmesi, bilgi mimarisi ve karar yapısı.
2. Hiyerarşi ve görsel ağırlık, bir itiraza cevap veren metin, sürtünme noktasındaki güven sinyali.
3. Renk, köşe yuvarlaklığı, yazı tipi, jenerik CTA kelimesi, mikro boşluk.

Üçüncü kademeden bir aday güçlü bir mekanizmaya sahipse önerilir; bu bir yasak değil, eşit koşulda sıralama ölçütüdür. Sıralama sezgisel bir önceliktir, ölçülmüş bir sonuç değildir. Kullanıcının test hafızası (kural 16) bu sıralamayı **yalnızca aynı bileşen veya aynı mekanizma için** ezer: geçmişte bir CTA rengi testinin kazanmış olması, tüm kozmetik adayların yapısal adayların önüne geçmesi anlamına gelmez.

Bu dört filtre önceliklendirmenin yerine geçmez, öncesinde çalışır: mercek "bu fikir öneriye değer mi" sorusunu, ICE "kalanlardan hangisi önce" sorusunu cevaplar. Etki sıralaması ICE'ı ezmez: kapıdan geçen adaylar ICE ile sıralanır; kademe, aday seçiminde ve ICE puanları eşitken devreye girer.

## Değişken izolasyonu

- Bir testte **tek değişken** değişir. Variant B'de fiyat, ürün, puan sayısı, rozet gibi ikinci bir fark varsa test kirlenmiştir (confound) ve sonucu yorumlanamaz. Aynı ekranda iki fark, iki ayrı testtir; tek raporda birleşmeleri onları tek test yapmaz.
- Variant A her zaman kontroldür (mevcut durum), Variant B testtir. Rolleri ters kurmayın.
- **Test yalnızca var olanı değiştirmek değildir.** Bir sayfada üç tür fırsat vardır: mevcut öğeyi değiştirmek, mevcut öğeyi kaldırmak ve **olmayan bir öğeyi eklemek**. Üçüncüsü genelde en yüksek etkilidir ama en az akla gelendir, çünkü ekrana bakıldığında görünen şey hep "orada olan"dır. Sayfayı değerlendirirken şu soru ayrıca sorulur: kullanıcı bu adımda hangi soruyu soruyor ve cevabı ekranda var mı? Eksik bilgi veya eksik aksiyon, bir varyantın konusu olabilir.
- **Kullanıcı sayfasını paylaştıysa A o sayfadır.** Kontrolü yeniden tasarlamak, sadeleştirmek veya "temsili" hâle getirmek testi geçersiz kılar — ölçtüğünüz şey artık önerinizin etkisi değil, iki ayrı tasarımın farkı olur. Ekranda ne varsa A odur; üretilecek tek şey B'dir.
- **Form akışında çok adımlıya geçmek varsayılan çözüm değildir.** Adım eklemek her adımda yeni bir terk noktası açar; pratikte tek sayfa kalıp ekrana sığacak şekilde yoğunlaştırılan form çoğu zaman daha iyi çalışır (ilişkili alanları yan yana almak, gereksiz alanı çıkarmak, dikey boşluğu azaltmak). Çok adımlı form yalnızca alanlar gerçekten tek ekrana sığmıyorsa veya alanlar doğal olarak ayrı aşamalara ait olduğunda önerilir — ve önerildiğinde bunun bir varsayım olduğu söylenir. **Alan sayısı, adım sayısından önce gelir:** bir formu test ederken önce alan sayısını azaltma/gereksiz alanı kaldırma senaryosu, sonra tek-sayfa-vs-çok-adım senaryosu önerilir — checkout kullanılabilirliği üzerine büyük ölçekli bağımsız araştırmalar, akışı kaç adıma böldüğünüzden çok kaç alan doldurttuğunuzun deneyimi belirlediğini tekrar tekrar gösteriyor.
- İki varyantta aynı ürün, aynı fiyat, aynı içerik kullanılır; yalnızca test edilen öğe farklıdır.

## İstatistiksel hijyen

- Kazananı ilk anlamlı sonuçta ilan etmeyin. Bunun iki ayrı gerekçesi var, birbirine karıştırılmaz:
  - **İstatistiksel (peeking riski):** Bir testi sonuçlar akarken tekrar tekrar kontrol edip ilk anlamlı ana çıktığınızda durdurmak (peeking), yanlış pozitif oranını nominal eşiğin (%5) çok üzerine çıkarır — iki özdeş deneyimi karşılaştıran bir A/A testinde bile, süreç boyunca birden fazla kez bakılırsa en az bir noktada geçici olarak "anlamlı" görünme ihtimali yüksektir. Çözüm: önceden belirlenen örneklem/süre dolmadan karar vermeyin, sonuca yalnızca planlanan noktada bakın. Bu bir istatistiksel zorunluluktur, ama "hiç bakmayın" demek değildir — sıralı test (sequential testing) yöntemleri, testin başında planlanan her ara-bakış için önceden bir karar sınırı hesaplayarak erken bakmayı geçerli kılabilir. `analyze_results.py` bu tür bir sınır hesaplamıyor; kural bu yüzden bağlayıcıdır. Hazırlıksız, tekrarlanan ham anlamlılık kontrolü (sıralı sınır olmadan) her durumda geçersizdir.
  - **Dış geçerlilik (iş döngüsü kapsama):** En az iki tam hafta koşturma kuralı istatistiksel güç şartı değildir — haftanın günlerini (hafta içi/hafta sonu davranış farkı), maaş günü etkisini ve operasyonel döngüleri kapsamak için bir deney hijyeni kuralıdır. Örneklem hedefine 3 günde ulaşılsa bile, test en az iki hafta açık tutulur.
- **Ortalamaya dönüş:** Testin ilk günlerinde bir varyant büyük farkla önde görünüp üçüncü haftada sonuç tersine dönebilir. İlk haftanın "kazananı" ilan edilmez; eğri düzleşene kadar beklenir.
- **Yenilik etkisi:** Yeni görünen bir değişiklik salt yeni olduğu için ilk günlerde fazladan dikkat çeker; bu fazlalık zamanla söner. Kısa süre koşup kapatılan bir testin lifti büyük olasılıkla yenilik etkisidir, kalıcı davranış değişikliği değil. `abtest-audit` bunu ayrı bir bulgu olarak işaretler (bkz. `skills/abtest-audit/SKILL.md` → denetim listesi, yenilik etkisi maddesi).
- Test süresince kampanya, fiyat, algoritma veya tasarım değişikliği yapmayın; veri kirlenir. Test sırasında bir teknik hata (script hatası, ölçüm kopması, yanlış segment ataması) fark edilirse testi düzeltip sıfırdan başlatın — SRM'nin en sık nedeni budur, kirli veriyle devam etmeyin.
- **Aynı kullanıcı aynı anda birden fazla teste dahil olmamalı.** İki test aynı sayfayı veya akışı etkiliyorsa (ör. biri fiyat kartını, diğeri ödeme butonunu test ediyor) varyasyonlar birbirine karışır ve hangi testin sonucu neyi ürettiği ayırt edilemez. Testler ya sıraya alınır ya da kullanıcı havuzu tamamen ayrılır (mutually exclusive traffic). Kurulum spesifikasyonundaki "Hariç tutulanlar" alanı bunun içindir.
- **Seçici kayıp (selective attrition) kontrolü.** Kontrol ve varyant arasında ölçüm/veri kaybı oranı asimetrikse (ör. bir varyant teknik nedenle bazı kullanıcılardan veri toplayamıyor — yavaş bağlantılı kullanıcı ağır bir görsel varyantta daha çok "kaybolur" gibi) sonuç geçersiz sayılır. Bu, SRM'den farklıdır: SRM örnekleme oranı sapmasını yakalar, seçici kayıp her iki kolda eşit örneklenmiş ama farklı oranda veri kaybedilmiş olmasını yakalar. `abtest-audit` bunu ayrı bir kontrol olarak sorar.
- **İstisna — guardrail erken durdurma:** "Erken bakmayın" kuralı birincil metrik içindir. Bir guardrail metriği (marj, hata oranı, destek talebi) test sırasında anlamlı biçimde kötüleşiyorsa, testi örneklem dolmadan durdurmak doğrudur — burada karar "kazanan kim" değil "zarar var mı" sorusuna dayanır, farklı bir eşiktir.
- Yeni bir test aracına geçerken veya trafik segmentasyonu değiştiğinde önce **A/A testi** koşun: iki grup birebir aynı deneyimi görür; anlamlı fark çıkarsa sorun üründe değil ölçüm altyapısındadır.
  - A/A'da bakılacaklar: %50/%50 bölünme gerçekten rastgele mi, p-değeri dağılımı düzgün mü, örneklem dengeli mi, yanlış pozitif oranı %5 anlamlılıkta beklenenin üstünde mi.
  - Tek bir A/A'ya bakıp aracı güvenilir ilan etmeyin; birkaç kez tekrarlayın.
  - **Daha hafif alternatif:** Ayrı bir A/A testi kurmak zaman maliyetlidir. Kontrolü ikiye bölüp gerçek varyantla birlikte üç kollu koşmak (A₁ / A₂ / B) da aynı doğrulamayı yapar — A₁ ile A₂ arasında anlamlı fark çıkarsa araç/segmentasyon şüphelidir, ayrıca test kurmaya gerek kalmaz.
- Trafiğin düşük olduğu **biliniyorsa** (kullanıcı söylediyse ya da sayfanın doğası gereği belliyse, ör. iade formu) klasik A/B önermek yerine Uygunluk tablosundaki alternatiflere geçin. Trafiği öğrenmek için ön kapıda soru sormayın (kural 5): senaryo üretmek trafiğe bağlı değildir, yalnızca süre ve örneklem hesabı bağlıdır.

## Sonuç yorumlama — genel farksızlık segment farksızlığı demek değildir

Toplamda A ile B arasında anlamlı fark çıkmaması testin "kazananı yok" demek olduğu anlamına gelmez. Bir segmentte (mobil, yeni kullanıcı, belirli bir trafik kaynağı) B kazanırken başka bir segmentte (masaüstü, dönen kullanıcı) A kazanıyorsa, ikisi toplamda birbirini götürüp yanlışlıkla "fark yok" görüntüsü yaratır. `abtest-audit`, genel sonuç "fark yok" olarak raporlandığında en az iki temel kırılımı (cihaz, yeni/dönen kullanıcı) ayrıca sormadan denetimi kapatmaz — segment başına örneklem yeterli değilse bunu bulgu olarak yazar, tahmin uydurmaz.

**Tuzak — segment taraması p-hacking'e dönüşmesin:** Bu kontrol, sonucu anlamak içindir, kazanan bir alt grup arayana kadar veriyi dilimlemek için değil. Segmentlere yalnızca genel sonuç belirsiz/farksızken bakılır; genel sonuç zaten netse "acaba şu segmentte daha iyi çıkar mı" diye tarama yapılmaz. ~250-350 dönüşüm, segment örnekleminin "muhtemelen çok küçük" olduğunu gösteren kaba bir uyarı eşiğidir — formal bir güç hesabı yerine geçmez; segment başına gerçek yeterlilik o segmentin kendi baz oranı ve hedeflenen MDE'siyle `analyze_results.py samplesize` üzerinden hesaplanır. Eşiğin altındaki segment farkı güvenilir sayılmaz, bulgu olarak "doğrulanmalı" diye işaretlenir.

**"Fark yok" sonucunun iki farklı nedeni olabilir:** Ya trafik/süre yetersiz kaldı (istatistiksel güç düşük), ya da değişiklik kullanıcının davranışını etkileyecek kadar belirgin değildi. `abtest-audit` "fark yok" bulgusunu raporlarken ikisini ayırt eder — örneklem hedefine ulaşılmış mı, ulaşılmışsa değişikliğin kendisi zayıf mıydı.

**Segmentasyonun üç merceği:** Cihaz/kullanıcı tipi tek kırılım değildir. Anlamlı segment üç kaynaktan gelir:
- **Kaynağa göre:** Trafiğin geldiği kanal (organik arama, sosyal, e-posta, ücretli). Bir kanaldan gelen kullanıcı değişikliğe farklı tepki verebilir.
- **Davranışa göre:** Kullanım sıklığı veya derinliği (ilk kez gelen vs. sık ziyaret eden, az sayfa gezen vs. çok gezen).
- **Sonuca göre:** Ne satın aldığı, sepete ne kadar harcadığı, hangi plana kaydolduğu.
Bir segmentte kazanan, başka bir segmentte kaybediyor olabilir; bu üç mercekten en az biri, "fark yok" veya sınırda çıkan sonuçlarda mutlaka sorulur.

## Önceliklendirme (ICE)

Birden fazla senaryo önerirken ICE ile sıralayın: Etki (Impact) × Güven (Confidence) × Kolaylık (Ease). Yüksek trafikli sayfadaki düşük eforlu test, düşük trafikli sayfadaki iddialı testten önce gelir.

Aynı girdiyle aynı sıralamanın çıkması için skala sabittir (her boyut 1-10, toplam = üç puanın çarpımı):

| Boyut | 1-3 | 4-7 | 8-10 |
|---|---|---|---|
| Etki | Kozmetik fark, birincil KPI'a dolaylı etki | Birincil KPI'ı etkilemesi makul | Huninin pahalı noktasında doğrudan etki |
| Güven | Sezgi / sektör gözlemi | Arşiv emsali veya kendi verinde dolaylı gözlem (ısı haritası, oturum kaydı, anket) | Kendi ürününde doğrudan sinyal veya kendi ürününde tekrarlanmış geçmiş test |
| Kolaylık | Yeni akış / backend işi | Orta ölçekli cephe işi | Metin/stil/sıralama düzeyinde değişiklik |

Eşitlikte sıra: hedef sayfanın trafiği yüksek olan → ölçümü basit olan (tek net olay) → guardrail riski düşük olan önce gelir. Trafik bilinmiyorsa ilk eşitlik bozucu atlanır — kural 5 gereği sorulmaz, kural 10 gereği tahmin edilmez; sıralama kalan iki ölçütle yapılır. Güven puanının dayanağı tek cümleyle yazılır ("Güven 8: aynı sayfada geçen çeyrekteki benzer test kazandı" gibi); dayanaksız yüksek güven puanı verilmez.

**Yerel tepe (local maximum) riski:** Sadece küçük, tek-değişkenli iyileştirmeler biriktirmek (buton rengi, satır aralığı, madde sırası) belirli bir noktadan sonra platoya oturur — küçük artışlar tükenir ama daha büyük bir kazanç için sayfanın kendisi yeniden tasarlanmalı. Bir ürün/sayfa için art arda birkaç küçük test "fark yok" veya "ihmal edilebilir" çıkıyorsa, `abtest-suggest` bir sonraki öneride daha cesur/yapısal bir varyant önerir (ör. tek alan değil tüm akışın yeniden kurgulanması) ve bunu neden önerdiğini söyler. Somut kaçış taktiği: değişkeni tek bir küçük elemandan sayfanın/akışın tamamına genişletin (radikal redesign testi); anlamlı bir kazanan bulununca tekrar mikro-optimizasyona dönülür.

**Kantitatif KPI'lara kalitatif geri bildirim eklenir.** Sadece sayılara bakmak yanıltıcı olabilir — KPI'nın *neden* değiştiğini kullanıcı yorumu açıklar. Test sayfasının altına kısa bir anket linki eklemek ucuz bir ek sinyaldir; zorunlu değildir ama özellikle "fark yok" veya sınırda çıkan sonuçlarda önerilir. Tek soruluk anketler en yüksek yanıt oranını verir — örnek sorular: "Bugün [aksiyon]'u tamamlamanızı ne engelliyor?" (tamamlamayanlara), "Satın almanızı ne az kalsın engelliyordu?" (satın alanlara, satın almadan hemen sonra sorulursa en dürüst cevabı verir). Destek talebi ve iptal nedeni kayıtları da aynı sinyali ücretsiz taşır — "ama", "endişe", "emin değilim" gibi ifadeler aranır.

## Arşiv bayatlar — ne zaman güvenilmeyeceğini bilin

Bu senaryolar zamansız değildir. Bir senaryonun geçerliliği şu durumlarda düşer; `abtest-suggest` bunlardan birini fark ederse senaryoyu önerirken uyarır veya hiç önermez:

- **Platform kuralı değişti:** İzin akışları, bildirim politikaları, tarayıcı çerez/izleme kısıtları, uygulama mağazası kuralları. Ölçüm veya uygulama artık mümkün olmayabilir.
- **Mevzuat değişti:** İndirim ve referans fiyat gösterimi, veri toplama, abonelik iptali, erişilebilirlik zorunlulukları.
- **Desen standartlaştı:** Bir zamanlar ayrıştırıcı olan şey (misafir ödeme, mobil uyum, arama önerisi) artık asgari beklentiyse, testin sorusu "eklemeli miyiz" değil "nasıl yapmalıyız"a döner.
- **Teknoloji değişti:** Sayfa hızı, arayüz kalıbı veya cihaz kullanımı senaryonun varsaydığı zemini kaydırdıysa.
- **Kendi verinizde tükendi:** Aynı desen sizin ürününüzde art arda "fark yok" verdiyse, arşivde durması onu sizin için geçerli kılmaz (bkz. yerel tepe riski).

Arşiv bir vaat değil, bir emsaldir: bir senaryonun burada durması onun sizin ürününüzde kazanacağını değil, benzer bir bağlamda daha önce sorulmaya değer bulunduğunu gösterir.

Bir senaryo bu nedenlerden biriyle geçersizleştiğinde arşivden sessizce silinmez: senaryonun kendi altına neyin değiştiği ve yerine ne önerildiği yazılır, böylece gerekçe senaryoyla birlikte kalır. Senaryonun altındaki "Pazar notu" satırları da bu amaca hizmet eder — bağımlılık görünür olur, kullanıcı kendi bağlamında geçerli olup olmadığına karar verebilir.

## Bu kuralların dayanağı

Buradaki disiplinin çoğu bu arşivin kendi saha pratiğinden gelir. Bir kısmı ise deney metodolojisinde yaygın kabul görmüş, tekrar tekrar doğrulanmış sonuçlardır — kullanıcı "bunu ekibime nasıl savunurum" diye sorduğunda bunların yerleşik pratik olduğu söylenebilir, ama tek bir kuruma/yayına atıfla değil:

- **Erken bakma (peeking) ve tekrarlı kontrolün yanlış pozitifi artırması** — çevrimiçi kontrollü deneylerde standart bir bulgu; sıralı test (sequential testing) yöntemleri tam da bu sorunu çözmek için vardır.
- **A/A testiyle ölçüm altyapısını doğrulama** — deney platformu güvenilirliği kontrollerinin klasik parçasıdır.
- **Örneklem oranı uyuşmazlığı (SRM)** — büyük ölçekli deney sistemlerinde en sık raporlanan veri kalitesi hatalarından biridir; sapma varsa sonuç okunmaz.
- **Yenilik etkisi ve ortalamaya dönüş** — deney sonuçlarının zaman içinde sönmesinin bilinen iki nedenidir.
- **Dönüşüm oranının geliri gizlemesi** — fiyat ve indirim deneylerinde gelir bazlı metrik (RPV) kullanma gerekçesi buradan gelir.
- **Normal yaklaşımın nadir olaylarda geçersizleşmesi** — iki oran karşılaştırmasının temel varsayımıdır (bkz. `scripts/analyze_results.py` içindeki beklenen sayı kontrolü).
- **Seçici kayıp ve eşzamanlı test kirlenmesi** — ölçekli deney altyapılarının ve açık kaynak A/B test araçlarının ortak pratiğidir; bu playbook'un istatistiksel hijyen bölümünde ayrı maddeler olarak yer alır.
- **Checkout/form kullanılabilirliği** — bağımsız, uzun soluklu kullanılabilirlik araştırmalarının tekrar eden bulgusu; alan sayısının adım sayısından önce geldiği bulgusu buradan gelir.

Kullanıcı bir kuralın gerekçesini sorduğunda "kural böyle" demek yeterli değildir — nedeni tek cümleyle açıklanır. Bu playbook'a özgü, literatürde karşılığı olmayan tercihler (üç kutu formatı, ICE skalası, arşiv seçimi) böyle olduğu belirtilir; dış otorite gibi sunulmaz. Hiçbir kural belirli bir şirket, ürün veya yayına atıfla savunulmaz — dayanağın kendisi (istatistiksel mantık, tekrarlanmış gözlem) yeterlidir.

## Pazar bağlamı — dil ile pazar aynı şey değil

Kullanıcının dili Türkçe olması, hedef pazarının Türkiye olduğu anlamına gelmez; İngilizce sorması da pazarının ABD olduğu anlamına gelmez. Bu arşiv Türkiye e-ticaret pratiğinden doğdu ve senaryoların çoğu evrenseldir (buton, görsel, sıralama, arama, form) — ama bir bölümü doğrudan pazara bağlıdır ve başka pazara taşınırken kırılır.

**Pazara bağlı davranış sınıfları:**
- **Ödeme kültürü:** Kredi kartı taksiti Türkiye, MENA ve Latin Amerika'da satın alma kararının merkezindedir; ABD ve Kuzey Avrupa'da bu mekanizma yoktur, oradaki karşılığı olan "sonra öde" (BNPL) çözümlerinin hedef kitlesi ve güven algısı farklıdır. Taksit senaryolarının sonucu bu pazarlar arasında taşınamaz.
- **Güven sinyalinin kaynağı:** Hangi logonun güven verdiği pazara bağlıdır — bir pazarda banka/kart doğrulama işareti tanıdıkken, başka pazarda ödeme sağlayıcısı veya bağımsız güvenlik mührü daha güçlü sinyaldir.
- **Kargo ve iade beklentisi:** Ücretsiz ve sorusuz iadenin standart sayıldığı pazarlarda "kolay iade" vurgusu ayrıştırıcı değil asgari şarttır; iade kültürünün zayıf olduğu pazarlarda ise güçlü bir güven sinyalidir. Ücretsiz kargo eşiğinin psikolojik ağırlığı da kargo maliyetinin sepete oranıyla birlikte değişir.
- **Fiyat algısı:** Fiyat sonu etkisi (9 ile bitmek) evrensel bir yasa değil, kültürel bir alışkanlıktır; bazı pazarlarda belirli rakamların ayrı çağrışımları vardır.
- **Destek kanalı beklentisi:** Mesajlaşma uygulaması veya telefon üzerinden satış desteği bazı pazarlarda güven artırırken, bazılarında kurumsallık algısını zayıflatabilir.
- **Kurumsal satın alma:** Fiyat şeffaflığının beklenti olduğu pazarlar ile teklif/pazarlık kültürünün baskın olduğu pazarlar farklı davranır.

**Mevzuat, pazardan ayrı bir kısıttır.** İndirim ve referans fiyat gösterimi, çerez/izin akışları, veri toplama ve abonelik iptali bazı bölgelerde yasal olarak bağlıdır — orada "hangi varyant daha çok satar" sorusu ancak izin verilen varyantlar arasında sorulabilir. Testi kurmadan önce hedef pazarın kuralını doğrulayın; playbook bunu bilmez ve tahmin etmez.

**Uygulama:** Pazara bağlı bir senaryo önerilirken bu bağımlılık çıktıda söylenir (senaryoların altındaki "Pazar notu" satırları). Kullanıcının hedef pazarı bilinmiyorsa ve pazara bağlı bir senaryo öneriliyorsa, önce hangi pazar için çalıştığı sorulur.

## Bu playbook nerede iyi çalışır, nerede çalışmaz

Klasik %50/%50 A/B testi her iş modeli için doğru araç değildir. Öneri üretmeden önce uygunluğu değerlendirin ve düşükse bunu açıkça söyleyin.

| Uygunluk | Bağlam |
|---|---|
| Yüksek | B2C e-ticaret, tüketici mobil uygulaması, self-servis SaaS — haftalık binlerce oturum, hızlı ve tekrarlanan dönüşüm olayı |
| Orta | Pazaryeri (arz/talep yan etkisi olabilir), abonelik, B2B lead formu — test edilebilir ama örneklem ve gecikmeli dönüşüm dikkat ister |
| Düşük | Düşük trafikli kurumsal satış sayfaları, uzun satış döngüsü (aylarca), ağır regülasyonlu akışlar (sigorta/finans/sağlık teklif ve sözleşme adımları), fiziksel mağaza etkisi baskın işler |

**Uygunluk düşükse ne önerilir (çıkmaz sokak bırakmayın):**
- **Nitel yöntemler:** 5-8 kişilik kullanılabilirlik testi, oturum kaydı incelemesi, çıkış anketi — küçük örneklemde bile problem tespitinde işe yarar, "hangi varyant kazandı" sorusuna değil "sorun ne" sorusuna cevap verir.
- **Öncesi/sonrası ölçüm (quasi-experiment):** Rastgele bölme mümkün değilse, değişiklik öncesi ve sonrası dönemleri mevsimsellik/kampanya etkisini not ederek karşılaştırın — nedensellik iddiası zayıftır, bunu açıkça yazın.
- **Daha kaba ama daha büyük değişiklik:** Küçük farkı ölçecek trafik yoksa, ölçülebilir büyüklükte bir fark yaratacak yapısal değişiklik test edin (küçük MDE devasa örneklem ister).
- **Yukarı taşıma:** Testi düşük trafikli alt sayfada değil, aynı problemi barındıran üst huni adımında koşun.
- **Regülasyonlu akışlarda:** Varyantlardan biri yasal metni, zorunlu bilgilendirmeyi veya fiyat şeffaflığını değiştiriyorsa test edilmez; önce hukuk/uyum onayı alınır.

## Kapsam: tek değişkenli A/B, çok değişkenli (MVT) değil

Bu playbook yalnızca **tek değişkenli A/B testleri** üretir ve denetler — aynı anda birden fazla öğenin (başlık + görsel + buton rengi) farklı kombinasyonlarıyla test edildiği multivariate testing (MVT) kapsam dışıdır. Sebep: MVT anlamlı sonuç için çok yüksek trafik gerektirir ve kombinasyon sayısı arttıkça hangi öğenin etkili olduğunu ayırt etmek zorlaşır — bizim tüm çerçevemiz (tek değişken, üç kutu, confound denetimi) buna göre kurulu. Uygunluğu sabit bir trafik sayısıyla değil hesapla belirleyin: MVT'de örneklem her **kombinasyona** ayrı ayrı bölünür, dolayısıyla gereken toplam trafik yaklaşık olarak kombinasyon sayısı × tek bir A/B testinin gereksinimidir. Kombinasyon başına düşen trafiği `analyze_results.py samplesize` ile kendi baz oranınız ve MDE'niz üzerinden hesaplayın; çıkan sayı elinizdeki trafiğe uymuyorsa MVT'ye girişmeyin. Kullanıcı birden fazla öğeyi birden test etmek isterse, `abtest-design` bunu ayrı tek-değişkenli testlere böler (methodology.md → Değişken izolasyonu) ve gerçekten MVT gerekiyorsa (çok yüksek trafik + öğeler arası etkileşim sorusu) bunun playbook'un kapsamı dışında olduğunu açıkça söyler.

## Etik ve yasal sınırlar

- Hiç uygulanmamış bir fiyatı "eski fiyat" diye göstermek yasal risktir (referans fiyat düzenlemeleri).
- Aylık taksit tutarını öne çıkarırken toplam tutarı gizlemek şeffaflık ihlalidir.
- Dark pattern üreten varyant önermeyin: kapatılamayan modal, gizlenen iptal koşulu, yanlış stok bilgisi.

**Kanıt/güven sinyali sıralaması.** Bir varyant güven artırmayı hedefliyorsa (referans, rozet, istatistik, vaka örneği) hepsi eşit ağırlıkta değildir — bağlam ve gerçek sayı içeren kanıt, jenerik olandan daha güçlüdür (ör. isimli/somut sonuçlu bir referans, sade bir logo şeridinden daha ikna edicidir). Somut sayı yuvarlanmış sayıdan daha güvenilir görünür ve genelde gerçektir de ("2.500 kullanıcı" yerine elde varsa "2.487 kullanıcı"). Kanıt, en çok tereddüt edilen noktaya (ör. ödeme formunun yanına) yerleştirilir — SSS'ye gömülmez. Kural 6 zaten geçerlidir: sahip olunmayan sertifika, uydurma istatistik veya sahte referans önerilmez; bu madde yalnızca gerçek kanıtın nasıl sıralanacağını anlatır.

**Manipülatif varyant kontrolü.** Bir varyantın dark pattern olup olmadığından şüphe varsa 5 soru sırayla sorulur: (1) Kullanıcıya sunulan seçenekler arasında bilerek eşitsiz bir yük mü koyuyor (asymmetric)? (2) Etkisi kullanıcıdan gizli mi (covert)? (3) Yanlış bir inanç mı üretiyor — abartılı iddia, eksik bilgi ya da yanıltıcı ifade yoluyla (deceptive)? (4) Gerekli bilgiyi geciktiriyor ya da gizliyor mu (hides information)? (5) Kullanıcının seçim kümesini daraltıyor mu (restrictive)? İkisi ya da fazlası "evet" ise varyant revize edilmeden önerilmez. Bağımsız araştırmalar, countdown timer'ların ve "az stok kaldı" mesajlarının önemli bir kısmının gerçek veriye değil zamanlanmış/rastgele üretime dayandığını gösteriyor — bkz. CLAUDE.md kural 6.
