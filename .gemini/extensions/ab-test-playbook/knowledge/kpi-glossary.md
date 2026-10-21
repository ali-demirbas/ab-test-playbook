# KPI sözlüğü

Senaryo arşivinin (`knowledge/scenarios/*.md`) KPI adları bu sözlükteki kanonik adlardır. Her satır bir metriğin tek satırlık tanımını, paydasını ve kabul edilen eş anlamlılarını verir. Eş anlamlı bir ad (ör. kullanıcının planındaki “Checkout Tamamlama”) kanonik metriği olarak okunur; arşive yazılan ad her zaman kanoniktir. Sözlükte olmayan, tek senaryoya özgü bir metrik yazılabilir, ama paydası maddede açıkça söylenir.

Payda kuralı (`knowledge/methodology.md` → KPI denominator): bir oran yalnızca paydası iki kolda da aynı biçimde var olduğunda karşılaştırılabilir. Varsayılan payda teste atanan ziyaretçidir (randomizasyon birimi kullanıcıysa kullanıcı, hesapsa hesap). “Yeni öğeyi gören kullanıcı” payda olamaz, çünkü o kullanıcılar yalnızca B kolunda vardır; daha dar bir payda gerekiyorsa aynı tetikleyici iki kolda da loglanır (tetiklenen analiz). Sayı (“… Sayısı”) birincil metrik olmaz; atanan ziyaretçi başına orana çevrilir. Paydası kollar arasında değişebilen metrikler (sipariş başına, talep başına) birincil olmaz, ikincil veya guardrail olarak yazılır; atanan paydalı bir eşdeğeri varsa guardrail için o seçilir (ör. “Talep Başına Nitelik Oranı” yerine “Nitelikli Talep Oranı”). Her satır tek payda taşır; aynı olayın başka bir paydayla okunması ayrı bir satırdır. Yalnızca B kolunda var olan bir öğenin metriği (“yalnızca B” tanısalı) iki kol arasında karşılaştırılmaz.

`scripts/validate_scenarios.py` bu tabloları okur: ilk sütundaki kalın ad kanonik addır, son sütundaki eş anlamlılar noktalı virgülle ayrılır. Birincil KPI’sı kanonik ad olmayan senaryoların sayısını uyarı olarak basar (`--verbose` ile liste). Sayı ya da “gören” paydalı satırları, birincilin tümleyeni olan guardrail’i ve izolasyon maddesi olmayan senaryoyu da uyarı olarak listeler.

## Gelir ve dönüşüm

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Dönüşüm Oranı (CR)** | Hedef satın almayı veya sayfanın tanımlı dönüşümünü tamamlayan ziyaretçilerin payı. | Teste atanan ziyaretçi | Genel Dönüşüm Oranı (CR); Genel Dönüşüm Oranı; Nihai Dönüşüm Oranı (CR); Satın Alma Oranı |
| **Ziyaretçi Başına Gelir (RPV)** | Test süresindeki toplam gelirin atanan ziyaretçiye bölümü; fiyat, taksit, indirim, paket ve abonelik testlerinde birincil metrik. Kupon testinde de iş hedefi belirtilene kadar birincildir. Değişiklik kupon, indirim kodu ya da kampanya gibi bir kullanıcı faydasına dokunuyorsa o faydayı koruyan bir guardrail ister (kuponda Kuponlu Sipariş Veren Ziyaretçi Oranı düşmemeli, yanında invariants); gelir artışı kullanıcı zararını gizlememeli. Gerçekleşmiş gelirdir: abonelikte pencerede fiilen tahsil edilen tutar (Tahsilat satırı); aylığa normalize değer Yeni Abonelik Değeri’dir ve RPV diye sunulmaz. | Teste atanan ziyaretçi | Brüt Gelir / Ziyaretçi; Ziyaretçi Başına Brüt Gelir; Ziyaretçi Başına Gelir |
| **Ziyaretçi Başına Net Gelir** | İade, iptal ve indirim maliyeti düşüldükten sonraki gelirin atanan ziyaretçiye bölümü; gecikmelidir, iade penceresi KPI adında yazılır. | Teste atanan ziyaretçi | Net RPV |
| **Kullanıcı Başına Gelir (ARPU)** | Ödeme yapan kullanıcı başına gelir; plan karışımını gösterir ama toplam gelir düşerken artabilir, bu yüzden ikincildir. | Ödeme yapan kullanıcı (kollar arasında değişebilir) | Kullanıcı Başına Ortalama Gelir |
| **Ortalama Sepet Tutarı (AOV)** | Sipariş başına ortalama tutar; tek başına birincil olmaz, RPV’nin bileşenidir. | Sipariş | Ortalama Sipariş Tutarı; Ortalama Sepet veya Plan Tutarı |
| **Ortalama Plan Değeri** | Plan veya abonelik satın alımı başına ortalama tutar. | Plan satın alımı | Ortalama Seçilen Plan Tutarı |
| **Sepete Ekleme Oranı** | Ürünü sepete ekleyen ziyaretçilerin payı; ara adım metriğidir, birincil yalnızca sipariş olayı izlenmiyorsa olur. | Ürün sayfasına atanan ziyaretçi | Sepete Ekleme |
| **Sipariş Tamamlama Oranı** | Checkout’a ulaşanlardan siparişi tamamlayanların payı; değişken checkout’a ulaşmayı etkiliyorsa bunun yerine Dönüşüm Oranı (CR) yazılır. | Checkout’a ulaşan ziyaretçi (iki kolda aynı tetikleyici) | Checkout Tamamlama; Checkout Tamamlama Oranı |
| **Ödeme Tamamlama Oranı** | Ödeme adımına ulaşanların ödemeyi bitirme payı. | Ödeme adımına ulaşan ziyaretçi (iki kolda aynı tetikleyici) | Ödeme Adımı Tamamlama Oranı |
| **Ödeme Adımına Geçiş Oranı** | Sepetten ödeme adımına geçen ziyaretçilerin payı. | Sepete ulaşan ziyaretçi | Ödeme Adımına Geçiş; Ödeme Adımına Ulaşma Oranı; Ödemeye Geçiş Oranı; Checkout’a Geçiş Oranı |
| **Sepet Terk Oranı** | Sepeti olup siparişi tamamlamadan ayrılanların payı. | Sepete ürün ekleyen ziyaretçi | Sepeti Terk Oranı |
| **Ödeme Adımı Terk Oranı** | Ödeme adımına gelip tamamlamadan ayrılanların payı. | Ödeme adımına ulaşan ziyaretçi | Checkout Terk Oranı |
| **Ek Satın Alma Oranı** | Bir siparişin hemen ardından yeni bir sipariş başlatanların payı. | Teşekkür sayfasına ulaşan alıcı | Sipariş Sonrası Ek Satın Alma |
| **Tekrar Satın Alma Oranı** | KPI adında yazılan pencerede (ör. 30, 60, 90 gün) yeniden sipariş veren alıcıların payı. | Testte siparişini veren alıcı, iki kolda aynı pencere | Tekrar Satın Alma; Yeniden Satın Alma Oranı; İkinci Sipariş Oranı |
| **Brüt Marj** | Gelirden ürün, kargo ve indirim maliyeti düşüldükten sonra kalan pay; fiyat ve indirim testlerinde guardrail. | Gelir | Kâr Marjı |
| **Taksit Seçim Oranı** | Ödemede taksit seçen siparişlerin payı; tanısal. | Sipariş | Taksitli Ödeme Payı |
| **Kupon Kullanım Oranı** | Kod veya kupon kullanılan siparişlerin payı. B sipariş sayısını değiştiriyorsa (kupon alanını gizlemek, ödeme adımını değiştirmek) payda kollar arasında kayar: guardrail Kuponlu Sipariş Veren Ziyaretçi Oranı olarak yazılır. | Sipariş | Kod Kullanım Oranı |
| **Kuponlu Sipariş Veren Ziyaretçi Oranı** | Kupon veya kod uygulanmış sipariş veren ziyaretçilerin atanan ziyaretçiye oranı (eski ad Kuponlu Sipariş Oranı, sipariş paydası sanıldığı için bu ada taşındı); kupon alanını değiştiren testte kupon kullanımının guardrail’i (düşmemeli), yanında invariants’ta işlevsel geçti ölçütü yazılır (geçerli kod iki kolda da girilir, uygulanır, indirim yansır, hatalar aynı ele alınır). Kod sahipleri atamadan önce genelde ayırt edilemez, segment uydurulmaz; atamadan önce ayırt edilebiliyorlarsa (kupon kampanyası bağlantısıyla gelen ya da kendisine kod tanımlanmış giriş yapmış kullanıcı) aynı oran o segmentte de izlenir. | Teste atanan ziyaretçi | Kuponlu Sipariş Oranı; Kodlu Sipariş Oranı |
| **Ödeme Hata Oranı** | Hatayla sonuçlanan ödeme denemelerinin payı; guardrail. | Ödeme denemesi | Ödeme Başarısızlık Oranı |

## İade ve iptal

İade ve iptal gecikmeli sonuçtur: takip penceresi (ör. teslimattan sonra 30 gün) metriğin tanımının parçasıdır, KPI adında yazılır (“İade Oranı (30 gün)”) ve iki kolda her siparişin kendi tarihinden itibaren uygulanır.

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **İade Oranı** | Takip penceresinde iade edilen siparişlerin payı. | Sipariş | Genel İade Oranı |
| **Beden Kaynaklı İade Oranı** | İade nedeni beden uyumsuzluğu olan siparişlerin payı; beden yardımı testlerinde genel iade oranından daha duyarlıdır. | Sipariş | Yanlış Beden Kaynaklı İade |
| **Ölçü Kaynaklı İade Oranı** | İade nedeni ürünün boyutunun beklenenden farklı çıkması olan siparişlerin payı. | Sipariş | Boyut Kaynaklı İade Oranı |
| **İade veya İptal Oranı** | Takip penceresinde iade edilen ya da iptal edilen sipariş veya aboneliklerin payı. | Sipariş | İptal / İade Oranı; İptal veya İade Oranı |
| **İade veya İtiraz Oranı** | Belirli bir nedenle (beklenti, tutar şaşkınlığı) iade, itiraz veya şikâyete dönen siparişlerin payı; sayı olarak yazılmışsa sipariş başına bu orana çevrilerek okunur. | Sipariş | İade veya İtiraz Sayısı |
| **İptal Oranı** | Takip penceresinde iptal edilen aboneliklerin payı. | Testte başlayan abonelik | Aboneliği İptal Etme Oranı; Abonelik İptal Oranı |
| **Sipariş İptal Oranı** | Takip penceresinde iptal edilen siparişlerin payı. | Sipariş | Sipariş Sonrası İptal; Sipariş Sonrası İptal Oranı |

## Form ve kayıt

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Form Başlama Oranı** | Forma ilk girişi yapan ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi | Form Başlatma Oranı |
| **Form Tamamlama Oranı** | Formu gönderen ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi (başlatanlar değil, çünkü başlatma B’de değişebilir) | Form Gönderim Oranı; Form Dönüşüm Oranı; Talep Formu Dönüşümü |
| **Ortalama Doldurma Süresi** | Forma ilk girişten gönderime kadar geçen medyan süre. | Formu gönderen | Form Doldurma Süresi |
| **Doğrulama Hatası Oranı** | En az bir doğrulama hatası alan gönderim denemelerinin payı. | Gönderim denemesi | Form Hata Oranı |
| **Alan Bazlı Terk Oranı** | Formu bırakanların son dokunduğu alana göre dağılımı; tanısal. | Formu başlatan | Alan Terk Oranı; Alan Başına Terk |
| **Alan Bazlı Hata Oranı** | Her alanda hata alan girişlerin payı; tanısal. | Alana veri giren | Alan Hata Oranı |
| **Adım Bazlı Terk Oranı** | Çok adımlı akışta her adımda ayrılanların payı; tanısal. | O adıma ulaşan | Adım Bazlı Terk; Adım Terk Oranı; Adım Terk |
| **Kayıt Oranı** | Hesap oluşturan ziyaretçilerin payı. | Teste atanan ziyaretçi | Ücretsiz Kayıt Oranı; Yeni Kullanıcı Kaydı; Hesap Oluşturma Oranı |
| **Kayıt Tamamlama Oranı** | Kayıt akışını başlatanların bitirme payı. | Kayıt akışını başlatan (iki kolda aynı tetikleyici) | Kayıt Bitirme Oranı |
| **Aktivasyon Oranı** | Ürünün temel aksiyonunu belirli sürede yapan kullanıcıların payı. | Teste atanan ziyaretçi (kaydolanlar değil, çünkü kayıt B’de değişebilir) | Atanan Ziyaretçi Başına Aktivasyon |
| **Kayıt Başına Aktivasyon Oranı** | Kaydolanlar içinde temel aksiyonu belirli sürede yapanların payı; kayıt kalitesi tanısıdır. | Kaydolan kullanıcı (kollar arasında değişebilir) | Kayıt Sonrası Aktivasyon Oranı |
| **Profil Tamamlama Oranı** | Eksik profil alanlarını dolduran kullanıcıların payı. | Teste atanan kullanıcı | Profil Doldurma Oranı |
| **Alan Doldurma Oranı** | Belirli bir alanı (isteğe bağlı alan, serbest metin) dolduran ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi (gönderenler değil, çünkü gönderim B’de değişebilir) | İsteğe Bağlı Alan Doldurma Oranı |

## Etkileşim ve gezinme

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Ana Aksiyon Tamamlama Oranı** | Sayfanın tanımlı ana işini (sipariş, talep, kayıt, işlem) tamamlayan ziyaretçilerin payı; sayfa türü belli olmayan senaryolarda kullanılan genel ad. | Teste atanan ziyaretçi | Aksiyon Tamamlama Oranı; Toplam Aksiyon Tamamlama Oranı; Asıl Akış Tamamlama Oranı |
| **Tıklama Oranı (CTR)** | Maddede adı geçen öğeye tıklayan ziyaretçilerin payı; ara adım metriğidir. Öğe adı belirtilmemiş “Tıklama Oranı” bu satıra, sayfanın ana CTA’sı kastediliyorsa CTA Tıklama Oranı’na okunur. | Teste atanan ziyaretçi (öğe iki kolda da varsa öğe gösterimi) | Tıklama Oranı |
| **CTA Tıklama Oranı** | Sayfanın ana CTA’sına tıklayan ziyaretçilerin payı; tanısal. | Teste atanan ziyaretçi | Buton Tıklama Oranı; Birincil Buton Tıklama Oranı; Tıklama Oranı (CTA) |
| **Kategori Tıklama Oranı** | Bir kategori bağlantısına veya kartına tıklayan ziyaretçilerin payı; tanısal. | Teste atanan ziyaretçi | Kategoriye Geçiş Oranı |
| **Aksiyon Sonrası Dökülme Oranı** | Aksiyona tıklayıp bir sonraki adımı tamamlamayanların payı; ara adım kazancının gerçek olup olmadığını gösterir. | Tıklayan ziyaretçi (kollar arasında değişebilir) | Tıklama Sonrası Dökülme Oranı |
| **Aksiyon Sonrası Tamamlama Oranı** | Aksiyona tıklayanlardan bir sonraki adımı tamamlayanların payı; Aksiyon Sonrası Dökülme Oranı’nın tümleyenidir, aynı kutuda ikisi birlikte yazılmaz. | Tıklayan ziyaretçi (kollar arasında değişebilir) | Tıklama Sonrası Tamamlama Oranı |
| **Liste → Ürün Tıklama Oranı** | Liste veya kategori sayfasından bir ürün detayına geçen ziyaretçilerin payı. | Liste sayfasına atanan ziyaretçi | Ürün Detayına Tıklama Oranı; Listeden Ürüne Geçiş Oranı |
| **Arama Kullanım Oranı** | Site içi aramayı kullanan ziyaretçilerin payı. | Teste atanan ziyaretçi | Arama Kullanımı; Site İçi Arama Kullanımı; Arama Başlatma Oranı |
| **Arama Dönüşüm Oranı (CR)** | Arama yapan oturumların satın almayla bitme payı. | Arama yapan oturum (aramaya ulaşma iki kolda aynıysa) | Genel Arama Dönüşümü |
| **Arama Sonucu Tıklama Oranı** | Bir sonuca tıklanan aramaların payı. | Arama | Arama → Ürün Tıklama |
| **Sıfır Sonuç Oranı** | Sonuç döndürmeyen aramaların payı. | Arama | Sıfır Sonuçlu Arama |
| **Filtre Kullanım Oranı** | En az bir filtre uygulayan liste ziyaretçilerinin payı; tanısal. | Liste sayfasına atanan ziyaretçi | Filtre Kullanımı |
| **Görülen Ürün Sayısı** | Ziyaretçi başına görüntülenen ortalama ürün sayısı; keşif tanısı. | Teste atanan ziyaretçi (ortalama) | Ürün Görüntüleme Sayısı; Benzersiz Ürün Görüntüleme |
| **Galeri Etkileşim Oranı** | Ürün görselleriyle etkileşen ziyaretçilerin payı; tanısal. | Ürün sayfasına atanan ziyaretçi | Görsel Etkileşim Oranı |
| **Karşılaştırma Etkileşim Oranı** | Karşılaştırma tablosu veya aracıyla etkileşen ziyaretçilerin payı; tanısal. | Teste atanan ziyaretçi | Karşılaştırma Etkileşimi |
| **Referans Etkileşim Oranı** | Referans veya müşteri hikâyesi bloğuyla etkileşen ziyaretçilerin payı; tanısal. | Teste atanan ziyaretçi | Referans Tıklama Oranı |
| **Sohbet Başlatma Oranı** | Canlı destek veya sohbet başlatan ziyaretçilerin payı. | Teste atanan ziyaretçi | Sohbet Açma Oranı |
| **Pop-up Yanıt Oranı** | Pop-up’a yanıt verenlerin payı; yalnızca B kolu içi tanısaldır: iki kol arasında karşılaştırılmaz, birincil veya guardrail olamaz, KPI kutusuna “İkincil (yalnızca B)” diye yazılır. İki kolda karşılaştırılacak karşılığı Oturum Devam Oranı’dır. | Pop-up gösterilen ziyaretçi (yalnızca B kolunda vardır) | Pop-up Etkileşim Oranı |
| **Özellik Deneme Oranı** | Tanıtılan özelliği ilk kez kullanan kullanıcıların payı. | Teste atanan kullanıcı (ipucunu görenler değil) | Tanıtılan Özellik Kullanım Oranı |
| **Duyurulan Aksiyonun Tamamlanma Oranı** | Duyuru veya kampanya şeridinin çağırdığı aksiyonu (kampanya ürünü alımı, kayıt) tamamlayan ziyaretçilerin payı. | Teste atanan ziyaretçi (şeridi tıklayanlar değil) | Kampanya Aksiyonu Tamamlama Oranı |

## Sayfa davranışı ve kalite

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Kaydırma Derinliği** | Sayfanın görülen yüzdesi; tanısal, tek başına başarı değildir. | Sayfa görüntüleme | Scroll Derinliği |
| **Sayfada Kalma Süresi** | Sayfada geçirilen medyan süre; artışı iyi de kötü de olabilir. | Sayfa görüntüleme | Sayfada Geçirilen Süre; Liste Sayfasında Süre; Listede Kalma Süresi |
| **Oturum Süresi** | Oturumun medyan süresi; tanısal. | Oturum | Genel Oturum Süresi |
| **Oturum Devam Oranı** | Belirli bir andan (ör. çıkış niyeti sinyali) sonra oturumu sürdüren kullanıcıların payı. | O ana ulaşan kullanıcı (aynı tetikleyici iki kolda da loglanır) | Oturuma Devam Oranı |
| **Hemen Çıkma Oranı** | Tek sayfa görüntüleyip etkileşim olmadan biten oturumların payı. | Sayfayla başlayan oturum | Bounce Oranı |
| **Sayfa Terk Oranı** | Sayfaya gelip hedef aksiyonu yapmadan siteden ayrılan ziyaretçilerin payı; birincil aynı sayfanın dönüşümüyse onun tümleyenidir ve guardrail olarak yazılmaz. | Teste atanan ziyaretçi | Sayfayı Terk Oranı |
| **Terk Oranı** | Hangi adımın terk edildiği yazılmadan kullanılan genel ad; tek başına bir metrik değildir. Maddede adımıyla yazılır: Sepet Terk Oranı, Ödeme Adımı Terk Oranı, Adım Bazlı Terk Oranı veya Sayfa Terk Oranı. Birincilin ölçtüğü adımın terki guardrail olamaz. | Maddede adı yazılan adıma ulaşan ziyaretçi (iki kolda aynı tetikleyici) | Bırakma Oranı |
| **Çıkış Oranı** | Sayfa görüntülemelerinden oturumun son görüntülemesi olanların payı. | Sayfa görüntüleme | Sayfadan Çıkış Oranı |
| **Geri Dönüş Oranı** | Bir sonraki sayfadan veya adımdan geri tuşuyla öncekine dönenlerin payı (gidip gelme); siteye yeniden gelmek için Tekrar Ziyaret Oranı kullanılır. | Sonraki sayfaya geçen ziyaretçi | Geri Tuşu Kullanımı |
| **Tekrar Ziyaret Oranı** | KPI adında yazılan pencerede siteye veya uygulamaya yeniden gelen kullanıcıların payı. | Teste atanan kullanıcı | Tekrar Ziyaret |
| **7. Gün Elde Tutma** | İlk açılış veya kayıttan 7 gün sonra yeniden aktif olan kullanıcıların payı. | Testte ilk açılışı yapan kullanıcı | Yedi Gün Elde Tutma; Uygulama 7 Gün Retention; 7 Günlük Aktif Kullanım |
| **Karar Süresi** | Sayfaya gelişten seçime veya aksiyona kadar geçen medyan süre. | Aksiyonu yapan ziyaretçi | Sayfada Karar Süresi |
| **Yanlış Tıklama Oranı** | Amaçlanmayan öğeye tıklayıp hemen geri dönen ziyaretçilerin payı; guardrail. | Etkileşen ziyaretçi | Yanlış Dokunma Oranı |
| **Sayfa Yüklenme Süresi** | Ana içeriğin yüklenme süresi (LCP, yüzdelik olarak, ör. p75); guardrail. | Sayfa görüntüleme | Sayfa Performansı |
| **Erişilebilirlik** | Klavye ve ekran okuyucuyla görevin tamamlanabilmesi, kontrast, dokunma hedefi ve hareket uyumu; guardrail. Geçti/kaldı denetimidir: KPI kutusuna “Erişilebilirlik Kontrolü (yayın öncesi, geçti/kaldı)” adıyla ve “Geçmeli: …” ölçütüyle yazılır (ör. “Geçmeli: B’nin klavye ve ekran okuyucu incelemesinde kritik sorun yok”), test trafik almadan önce B üzerinde bakılır. | Denetim ölçütü (oran değil) | Erişilebilirlik Uyumu; Erişilebilirlik Kontrolü |
| **Destek Talebi** | Testin konusuyla ilgili açılan destek talepleri; sayı olarak yazılmışsa atanan ziyaretçi başına orana çevrilerek okunur (ör. 1.000 ziyaretçi başına). | Teste atanan ziyaretçi | Destek Talebi Sayısı; İlgili Destek Talebi; Destek Temas Oranı; Müşteri Hizmetleri Talebi; Destek Yükü; Destek Çağrı Hacmi |
| **Ürün Sorusu Oranı** | Ürünle ilgili sorulan soruların (soru alanı, sohbet, destek) atanan ziyaretçiye oranı; sayı olarak yazılmışsa bu orana çevrilerek okunur. | Ürün sayfasına atanan ziyaretçi | Ürün Sorusu Sayısı |
| **Marka Algısı (anket)** | Kısa anketle ölçülen marka algısı; yalnızca yanıtlayanları kapsayan tanısal sinyal. | Anketi yanıtlayan | Marka Algısı Anketi (varsa); Marka Güven Skoru |
| **Güven Algısı (anket)** | Kısa anketle ölçülen güven algısı; yalnızca yanıtlayanları kapsayan tanısal sinyal. | Anketi yanıtlayan | Güven Anketi |

## SaaS, B2B ve abonelik

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Nitelikli Fırsat Oranı** | Satış ekibinin nitelikli kabul ettiği fırsatların (SQL) atanan ziyaretçiye oranı; birincil olarak sayı değil bu oran yazılır. | Teste atanan ziyaretçi | Nitelikli Fırsat Sayısı (SQL); Nitelikli Fırsat Sayısı; SQL Oranı |
| **Nitelikli Talep Oranı** | Hedef profile uyan taleplerin atanan ziyaretçiye oranı; birincil olarak sayı değil bu oran yazılır. | Teste atanan ziyaretçi | Nitelikli Talep Sayısı |
| **Talep Başına Nitelik Oranı** | Gelen talepler içinde hedef profile uyanların payı; yalnızca B talep sayısını değiştirmiyorsa talep kalitesi guardrail’i olur. B talep sayısını değiştiriyorsa (alan kaldırmak, buton eklemek) payda kollar arasında kayar: guardrail Hedef Profil Dışı Talep Oranı olarak yazılır. | Gelen talep (kollar arasında değişebilir) | Kayıt Başına Nitelik Oranı; Talep Kalitesi; Talep Niteliği |
| **Hedef Profil Dışı Talep Oranı** | Hedef profile uymayan taleplerin atanan ziyaretçiye oranı; B talep sayısını değiştirdiğinde talep kalitesi guardrail’i bu orandır (artmamalı). | Teste atanan ziyaretçi | Niteliksiz Talep Oranı |
| **Fırsat Kapanış Oranı** | Nitelikli fırsatlardan satışa dönenlerin payı; gecikmelidir, satış döngüsü boyunca oluşur. | Nitelikli fırsat | Kazanma Oranı |
| **Ücretliye Geçiş Oranı** | Deneme veya ücretsiz kullanımdan ücretli plana geçen kullanıcıların payı. | Teste atanan kullanıcı (denemeyi başlatanlar değil, çünkü deneme başlatma B’de değişebilir) | Ücretli Plana Geçiş Oranı |
| **Deneme Başına Ücretliye Geçiş Oranı** | Denemeyi başlatanlardan ücretli plana geçenlerin payı; değişken deneme başlatmayı etkiliyorsa kullanılmaz. | Denemeyi başlatan kullanıcı (iki kolda aynı tetikleyici) | Deneme → Ücretli Geçiş Oranı |
| **Yükseltme Oranı** | Mevcut plandan daha üst bir plana geçen kullanıcıların payı. | Teste atanan mevcut kullanıcı (limit ekranını görenler değil) | Plan Yükseltme Oranı |
| **Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)** | Test penceresinde başlayan yeni aboneliklerin aylık karşılık fiyatları toplamının (yıllık plan 12’ye bölünür) atanan ziyaretçiye bölümü; yıllık ve aylık varsayılan testlerinde seçilen plan değerini karşılaştırır. Gerçekleşmiş gelir değildir, Ziyaretçi Başına Gelir (RPV) diye sunulmaz; taahhüt süresi boyunca sözleşilen toplam değer ayrı bir metriktir ve penceresi adında yazılır. | Teste atanan ziyaretçi | Yeni Abonelik Değeri; Aylığa Normalize Abonelik Değeri |
| **Tahsilat (gözlem penceresi, atanan ziyaretçi başına)** | KPI adındaki gözlem penceresinde fiilen tahsil edilen tutarın atanan ziyaretçiye bölümü; yıllık peşin ödeme pencerede tamamıyla, aylık ödeme yalnızca gerçekleşen ödemeleriyle sayılır. Abonelikte Ziyaretçi Başına Gelir (RPV) bu tanımla okunur. | Teste atanan ziyaretçi | Tahsilat; Gerçekleşen Tahsilat |
| **Dönem Kaynaklı İade veya Şikâyet Talebi Oranı (ilk ödemeden sonra 30 gün)** | Faturalanan dönemin istenmediğini gerekçe gösteren iade veya şikâyet taleplerinin (ör. “yıllık değil aylık istemiştim”) atanan ziyaretçiye oranı; pencere her aboneliğin ilk ödemesinden başlar. Varsayılan fatura dönemini (aylık ya da yıllık) değiştiren testin guardrail’idir (artmamalı): yanlışlıkla seçilen dönemi yakalar, genel iade oranı bunu seyreltir. Payda abonelik başlatanlar değildir, çünkü başlatma B’de değişebilir. | Teste atanan ziyaretçi | Dönem Kaynaklı İade Talebi Oranı; Yanlış Dönem İade veya Şikâyet Oranı |
| **Plan Seçim Dağılımı** | Satın alınan planların planlara göre dağılımı; tanısal. | Plan satın alan | Plan Seçim Oranı |

## Mobil uygulama ve bildirim

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Net Bildirim İzni Oranı** | Bildirim iznini veren kullanıcıların tüm yeni kullanıcılara oranı; izin istenenlere değil. | Teste atanan yeni kullanıcı | Bildirim İzni Oranı |
| **İlk Oturum Tamamlama Oranı** | İlk oturumda karşılama akışını bitiren yeni kullanıcıların payı. | Teste atanan yeni kullanıcı | İlk Oturum Tamamlama |
| **Uygulama Silme Oranı** | KPI adında yazılan pencerede uygulamayı silen kullanıcıların payı; guardrail. | Teste atanan kullanıcı | Kaldırma Oranı |
| **Bildirim Kapatma Oranı** | Bildirim iznini sonradan kapatan kullanıcıların payı; guardrail. | İzin veren kullanıcı | Bildirimi Kapatma Oranı |
| **Haber Ver Kayıt Oranı** | Stokta olmayan üründe “haber ver” kaydı bırakan ziyaretçilerin payı. | Tükenen ürün sayfasına atanan ziyaretçi | Stok Bildirimi Kayıt Oranı |

## Finans, sigorta ve bireysel emeklilik

Bu bölümün gecikmeli satırlarında (cayma, durdurma, teklif sonrası sözleşme) “İade ve iptal” bölümündeki pencere kuralı aynen geçerlidir: pencere KPI adında yazılır; yasal ya da ürüne özgü bir süreyse (cayma süresi) ürün şartlarından alınır, tahmin edilmez. Mevzuata bağlı metin, oran ve tutar gösterimi bu akışlarda test konusu olmaz; B’nin metni için uyum onayı test trafik almadan önce alınır.

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Talep Oluşturma Oranı** | Teklif, başvuru veya talep formunu gönderen ziyaretçilerin payı. | Teste atanan ziyaretçi (formu başlatanlar değil) | Teklif Talebi Oranı; Başvuru Oranı; Teklif Al Oranı |
| **Hesaplama Tamamlama Oranı** | Hesaplayıcıda sonuç ekranına ulaşan ziyaretçilerin payı; ara adım metriğidir, birincil yalnızca talep olayı izlenmiyorsa olur. | Hesaplayıcı sayfasına atanan ziyaretçi | Hesaplayıcı Tamamlama; Sonuç Ekranına Ulaşma Oranı |
| **Sözleşme Oranı (30 gün)** | KPI adındaki pencerede (ör. 30 gün) sözleşmeyi veya poliçeyi tamamlayan ziyaretçilerin atanan ziyaretçiye oranı; teklif akışı testlerinde iki kolda karşılaştırılan sözleşme metriği ve guardrail’i, gecikmelidir. | Teste atanan ziyaretçi | Sözleşme Oranı; Poliçe Oranı |
| **Teklif → Sözleşme Dönüşüm Oranı** | Teklif alanlardan KPI adındaki pencerede sözleşmeyi veya poliçeyi tamamlayanların payı; teklif sayısı B’de değişebildiği için yalnızca tanısaldır (detayda ikincil), birincil olmaz ve guardrail için atanan paydalı karşılığı Sözleşme Oranı (30 gün) seçilir. | Teklif alan ziyaretçi (kollar arasında değişebilir) | Poliçeleşme Oranı; Teklif → Poliçe |
| **Özellik Katılım Oranı** | Sunulan bir özelliğe veya programa (ör. otomatik fon yönetimi) katılım onayı veren kullanıcıların payı. | Teste atanan kullanıcı (tanıtım ekranını görenler değil) | Katılım Oranı; Opt-in Oranı |
| **Katkı Payı Artırma Oranı** | KPI adında yazılan pencerede katkı payını veya primini artırma talimatı veren müşterilerin payı. | Teste atanan müşteri | Prim Artırma Oranı; Artırım Oranı |
| **Ortalama Artış Tutarı** | Artıranlarda ortalama artış; ikincil metriktir. | Artıran müşteri (kollar arasında değişebilir) | Ortalama Katkı Artışı |
| **Cayma Süresi İçinde İptal Oranı** | Yasal cayma penceresinde sözleşmeyi iptal edenlerin payı; gecikmeli guardrail, penceresi ürün şartlarındaki cayma süresidir ve tahmin edilmez. | Testte sözleşme yapan müşteri | Cayma Oranı |
| **30 Gün İçinde Durdurma Oranı** | Sözleşmeyi veya ödemeyi ilk 30 günde durduran ya da ödemeye ara verenlerin payı; gecikmeli guardrail. | Testte sözleşme yapan müşteri, iki kolda aynı pencere | Erken Churn Oranı; Ödeme Durdurma Oranı |
| **Başvuru Onay Oranı** | Gönderilen başvurulardan onaylananların payı; talep kalitesi guardrail’i. | Gönderilen başvuru (kollar arasında değişebilir) | Onay Oranı; Kabul Oranı |
