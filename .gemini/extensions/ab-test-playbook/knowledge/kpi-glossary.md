# KPI sözlüğü

Senaryo arşivinin (`knowledge/scenarios/*.md`) KPI adları bu sözlükteki kanonik adlardır. Her satır bir metriğin tek satırlık tanımını, paydasını ve kabul edilen eş anlamlılarını verir. Eş anlamlı bir ad (ör. kullanıcının planındaki “Checkout Tamamlama”) kanonik metriği olarak okunur; arşive yazılan ad her zaman kanoniktir. Sözlükte olmayan, tek senaryoya özgü bir metrik yazılabilir, ama paydası maddede açıkça söylenir.

Payda kuralı (`knowledge/methodology.md` → KPI denominator): bir oran yalnızca paydası iki kolda da aynı biçimde var olduğunda karşılaştırılabilir. Varsayılan payda teste atanan ziyaretçidir (randomizasyon birimi kullanıcıysa kullanıcı, hesapsa hesap). “Yeni öğeyi gören kullanıcı” payda olamaz, çünkü o kullanıcılar yalnızca B kolunda vardır; daha dar bir payda gerekiyorsa aynı tetikleyici iki kolda da loglanır (tetiklenen analiz). Sayı (“… Sayısı”) birincil metrik olmaz; atanan ziyaretçi başına orana çevrilir. Paydası kollar arasında değişebilen metrikler (sipariş başına, talep başına) ikincil veya guardrail olarak okunur.

`scripts/validate_scenarios.py` bu tabloları okur: ilk sütundaki kalın ad kanonik addır, son sütundaki eş anlamlılar noktalı virgülle ayrılır. Birincil KPI’sı kanonik ad olmayan senaryoların sayısını uyarı olarak basar (`--verbose` ile liste).

## Gelir ve dönüşüm

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Dönüşüm Oranı (CR)** | Hedef satın almayı veya sayfanın tanımlı dönüşümünü tamamlayan ziyaretçilerin payı. | Teste atanan ziyaretçi | Genel Dönüşüm Oranı (CR); Genel Dönüşüm Oranı; Nihai Dönüşüm Oranı (CR); Satın Alma Oranı |
| **Ziyaretçi Başına Gelir (RPV)** | Test süresindeki toplam gelirin atanan ziyaretçiye bölümü; fiyat, taksit, indirim, paket ve abonelik testlerinde birincil metrik. | Teste atanan ziyaretçi | Brüt Gelir / Ziyaretçi; Ziyaretçi Başına Brüt Gelir; Ziyaretçi Başına Gelir |
| **Ziyaretçi Başına Net Gelir** | İade, iptal ve indirim maliyeti düşüldükten sonraki gelirin atanan ziyaretçiye bölümü; iade penceresi kapanınca okunur. | Teste atanan ziyaretçi | Net RPV |
| **Kullanıcı Başına Gelir (ARPU)** | Ödeme yapan kullanıcı başına gelir; plan karışımını gösterir ama toplam gelir düşerken artabilir, bu yüzden ikincildir. | Ödeme yapan kullanıcı (kollar arasında değişebilir) | Kullanıcı Başına Ortalama Gelir |
| **Ortalama Sepet Tutarı (AOV)** | Sipariş başına ortalama tutar; tek başına birincil olmaz, RPV’nin bileşenidir. | Sipariş | Ortalama Sepet Tutarı; Ortalama Sipariş Tutarı; Ortalama Sepet veya Plan Tutarı |
| **Ortalama Plan Değeri** | Plan veya abonelik satın alımı başına ortalama tutar. | Plan satın alımı | Ortalama Seçilen Plan Tutarı |
| **Sepete Ekleme Oranı** | Ürünü sepete ekleyen ziyaretçilerin payı; ara adım metriğidir, birincil yalnızca trafik siparişi taşımıyorsa olur. | Ürün sayfasına atanan ziyaretçi | Sepete Ekleme |
| **Sipariş Tamamlama Oranı** | Siparişi tamamlayanların payı. | Checkout’a ulaşan ziyaretçi (iki kolda aynı tetikleyici) veya atanan ziyaretçi | Checkout Tamamlama; Checkout Tamamlama Oranı |
| **Ödeme Tamamlama Oranı** | Ödeme adımına ulaşanların ödemeyi bitirme payı. | Ödeme adımına ulaşan ziyaretçi (iki kolda aynı tetikleyici) | Ödeme Adımı Tamamlama Oranı |
| **Ödeme Adımına Geçiş Oranı** | Sepetten ödeme adımına geçen ziyaretçilerin payı. | Sepete ulaşan ziyaretçi | Ödeme Adımına Geçiş; Ödeme Adımına Ulaşma Oranı; Ödemeye Geçiş Oranı; Checkout’a Geçiş Oranı |
| **Sepet Terk Oranı** | Sepeti olup siparişi tamamlamadan ayrılanların payı. | Sepete ürün ekleyen ziyaretçi | Sepeti Terk Oranı |
| **Ödeme Adımı Terk Oranı** | Ödeme adımına gelip tamamlamadan ayrılanların payı. | Ödeme adımına ulaşan ziyaretçi | Checkout Terk Oranı |
| **Ek Satın Alma Oranı** | Bir siparişin hemen ardından yeni bir sipariş başlatanların payı. | Teşekkür sayfasına ulaşan alıcı | Sipariş Sonrası Ek Satın Alma |
| **Tekrar Satın Alma Oranı** | Önceden ilan edilen pencerede (ör. 30, 60, 90 gün) yeniden sipariş veren alıcıların payı. | Testte siparişini veren alıcı, iki kolda aynı pencere | Tekrar Satın Alma; Yeniden Satın Alma Oranı; İkinci Sipariş Oranı |
| **Brüt Marj** | Gelirden ürün, kargo ve indirim maliyeti düşüldükten sonra kalan pay; fiyat ve indirim testlerinde guardrail. | Gelir | Kâr Marjı |
| **Taksit Seçim Oranı** | Ödemede taksit seçen siparişlerin payı; tanısal. | Sipariş | Taksitli Ödeme Payı |
| **Kupon Kullanım Oranı** | Kod veya kupon kullanılan siparişlerin payı. | Sipariş | Kod Kullanım Oranı |
| **Ödeme Hata Oranı** | Hatayla sonuçlanan ödeme denemelerinin payı; guardrail. | Ödeme denemesi | Ödeme Başarısızlık Oranı |

## İade ve iptal

İade ve iptal gecikmeli sonuçtur: takip penceresi (ör. teslimattan sonra 30 gün) test başlamadan ilan edilir, iki kolda her siparişin kendi tarihinden itibaren uygulanır ve son kohortun penceresi kapanmadan sonuç okunmaz.

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **İade Oranı** | Takip penceresinde iade edilen siparişlerin payı. | Sipariş | Genel İade Oranı |
| **Beden Kaynaklı İade Oranı** | İade nedeni beden uyumsuzluğu olan siparişlerin payı; beden yardımı testlerinde genel iade oranından daha duyarlıdır. | Sipariş | Yanlış Beden Kaynaklı İade |
| **Ölçü Kaynaklı İade Oranı** | İade nedeni ürünün boyutunun beklenenden farklı çıkması olan siparişlerin payı. | Sipariş | Boyut Kaynaklı İade Oranı |
| **İade veya İptal Oranı** | Takip penceresinde iade edilen ya da iptal edilen sipariş veya aboneliklerin payı. | Sipariş | İptal / İade Oranı; İptal veya İade Oranı |
| **İade veya İtiraz Oranı** | Belirli bir nedenle (beklenti, tutar şaşkınlığı) iade, itiraz veya şikâyete dönen siparişlerin payı. | Sipariş | İade veya İtiraz Sayısı |
| **İptal Oranı** | Takip penceresinde iptal edilen abonelik veya siparişlerin payı. | Abonelik veya sipariş | Aboneliği İptal Etme Oranı |

## Form ve kayıt

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Form Başlama Oranı** | Forma ilk girişi yapan ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi | Form Başlatma Oranı |
| **Form Tamamlama Oranı** | Formu gönderen ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi (başlatanlar değil, çünkü başlatma B’de değişebilir) | Form Gönderim Oranı; Form Dönüşüm Oranı (CR); Talep Formu Dönüşümü |
| **Ortalama Doldurma Süresi** | Forma ilk girişten gönderime kadar geçen medyan süre. | Formu gönderen | Form Doldurma Süresi |
| **Doğrulama Hatası Oranı** | En az bir doğrulama hatası alan gönderim denemelerinin payı. | Gönderim denemesi | Form Hata Oranı |
| **Alan Bazlı Terk Oranı** | Formu bırakanların son dokunduğu alana göre dağılımı; tanısal. | Formu başlatan | Alan Terk Oranı; Alan Başına Terk |
| **Alan Bazlı Hata Oranı** | Her alanda hata alan girişlerin payı; tanısal. | Alana veri giren | Alan Hata Oranı |
| **Adım Bazlı Terk Oranı** | Çok adımlı akışta her adımda ayrılanların payı; tanısal. | O adıma ulaşan | Adım Bazlı Terk; Adım Terk Oranı; Adım Terk |
| **Kayıt Oranı** | Hesap oluşturan ziyaretçilerin payı. | Teste atanan ziyaretçi | Ücretsiz Kayıt Oranı; Yeni Kullanıcı Kaydı; Hesap Oluşturma Oranı |
| **Kayıt Tamamlama Oranı** | Kayıt akışını başlatanların bitirme payı. | Kayıt akışını başlatan (iki kolda aynı tetikleyici) | Kayıt Bitirme Oranı |
| **Aktivasyon Oranı** | Kayıttan sonra ürünün temel aksiyonunu belirli sürede yapan kullanıcıların payı. | Kaydolan kullanıcı veya atanan ziyaretçi | Kayıt Sonrası Aktivasyon Oranı |
| **Profil Tamamlama Oranı** | Eksik profil alanlarını dolduran kullanıcıların payı. | Teste atanan kullanıcı | Profil Doldurma Oranı |
| **Alan Doldurma Oranı** | Belirli bir alanı (isteğe bağlı alan, serbest metin) dolduran ziyaretçilerin payı. | Form sayfasına atanan ziyaretçi (gönderenler değil, çünkü gönderim B’de değişebilir) | İsteğe Bağlı Alan Doldurma Oranı |

## Etkileşim ve gezinme

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Ana Aksiyon Tamamlama Oranı** | Sayfanın tanımlı ana işini (sipariş, talep, kayıt, işlem) tamamlayan ziyaretçilerin payı; sayfa türü belli olmayan senaryolarda kullanılan genel ad. | Teste atanan ziyaretçi | Aksiyon Tamamlama Oranı; Toplam Aksiyon Tamamlama Oranı; Asıl Akış Tamamlama Oranı |
| **Tıklama Oranı (CTR)** | Öğeye tıklayan ziyaretçilerin payı; ara adım metriğidir. | Teste atanan ziyaretçi (öğe iki kolda da varsa öğe gösterimi) | Tıklama Oranı |
| **CTA Tıklama Oranı** | Sayfanın ana CTA’sına tıklayan ziyaretçilerin payı; tanısal. | Teste atanan ziyaretçi | Buton Tıklama Oranı; Birincil Buton Tıklama Oranı |
| **Aksiyon Sonrası Dökülme Oranı** | Aksiyona tıklayıp bir sonraki adımı tamamlamayanların payı; ara adım kazancının gerçek olup olmadığını gösterir. | Tıklayan ziyaretçi | Tıklama Sonrası Dökülme Oranı |
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
| **Pop-up Yanıt Oranı** | Pop-up’a yanıt verenlerin payı; yalnızca pop-up gösterilen kolda tanımlıdır, birincil olamaz. | Pop-up gösterilen ziyaretçi | Pop-up Etkileşim Oranı |
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
| **Sayfa Terk Oranı** | Sayfaya gelip hedef aksiyonu yapmadan siteden ayrılan ziyaretçilerin payı. | Teste atanan ziyaretçi | Sayfayı Terk Oranı |
| **Çıkış Oranı** | Sayfa görüntülemelerinden oturumun son görüntülemesi olanların payı. | Sayfa görüntüleme | Sayfadan Çıkış Oranı |
| **Geri Dönüş Oranı** | Bir sonraki sayfadan veya adımdan geri tuşuyla öncekine dönenlerin payı (gidip gelme); siteye yeniden gelmek için Tekrar Ziyaret Oranı kullanılır. | Sonraki sayfaya geçen ziyaretçi | Geri Tuşu Kullanımı |
| **Tekrar Ziyaret Oranı** | Önceden ilan edilen pencerede siteye veya uygulamaya yeniden gelen kullanıcıların payı. | Teste atanan kullanıcı | Tekrar Ziyaret |
| **7. Gün Elde Tutma** | İlk açılış veya kayıttan 7 gün sonra yeniden aktif olan kullanıcıların payı. | Testte ilk açılışı yapan kullanıcı | Yedi Gün Elde Tutma; Uygulama 7 Gün Retention; 7 Günlük Aktif Kullanım |
| **Karar Süresi** | Sayfaya gelişten seçime veya aksiyona kadar geçen medyan süre. | Aksiyonu yapan ziyaretçi | Sayfada Karar Süresi |
| **Yanlış Tıklama Oranı** | Amaçlanmayan öğeye tıklayıp hemen geri dönen ziyaretçilerin payı; guardrail. | Etkileşen ziyaretçi | Yanlış Dokunma Oranı |
| **Sayfa Yüklenme Süresi** | Ana içeriğin yüklenme süresi (LCP, yüzdelik olarak, ör. p75); guardrail. | Sayfa görüntüleme | Sayfa Performansı |
| **Erişilebilirlik** | Klavye ve ekran okuyucuyla görevin tamamlanabilmesi, kontrast, dokunma hedefi ve hareket uyumu; guardrail. | Denetim ölçütü (oran değil) | Erişilebilirlik Uyumu |
| **Destek Talebi** | Testin konusuyla ilgili açılan destek talepleri; atanan ziyaretçi başına oran olarak okunur (ör. 1.000 ziyaretçi başına). | Teste atanan ziyaretçi | Destek Talebi Sayısı; Destek Temas Oranı; Müşteri Hizmetleri Talebi; Destek Yükü; Destek Çağrı Hacmi |
| **Marka Algısı (anket)** | Kısa anketle ölçülen marka algısı; küçük örneklemli tanısal sinyal. | Anketi yanıtlayan | Marka Algısı Anketi (varsa); Marka Güven Skoru |
| **Güven Algısı (anket)** | Kısa anketle ölçülen güven algısı; küçük örneklemli tanısal sinyal. | Anketi yanıtlayan | Güven Anketi |

## SaaS, B2B ve abonelik

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Nitelikli Fırsat Oranı** | Satış ekibinin nitelikli kabul ettiği fırsatların (SQL) atanan ziyaretçiye oranı; birincil olarak sayı değil bu oran yazılır. | Teste atanan ziyaretçi | Nitelikli Fırsat Sayısı (SQL); Nitelikli Fırsat Sayısı; SQL Oranı |
| **Nitelikli Talep Oranı** | Hedef profile uyan taleplerin atanan ziyaretçiye oranı; birincil olarak sayı değil bu oran yazılır. | Teste atanan ziyaretçi | Nitelikli Talep Sayısı |
| **Talep Başına Nitelik Oranı** | Gelen talepler içinde hedef profile uyanların payı; talep kalitesi guardrail’i. | Gelen talep (kollar arasında değişebilir) | Kayıt Başına Nitelik Oranı; Talep Kalitesi; Talep Niteliği |
| **Fırsat Kapanış Oranı** | Nitelikli fırsatlardan satışa dönenlerin payı; gecikmeli, satış döngüsü kadar beklenir. | Nitelikli fırsat | Kazanma Oranı |
| **Ücretliye Geçiş Oranı** | Deneme veya ücretsiz kullanımdan ücretli plana geçen kullanıcıların payı. | Denemeyi başlatan kullanıcı (iki kolda aynı tetikleyici) veya atanan ziyaretçi | Deneme → Ücretli Geçiş Oranı |
| **Yükseltme Oranı** | Mevcut plandan daha üst bir plana geçen kullanıcıların payı. | Teste atanan mevcut kullanıcı (limit ekranını görenler değil) | Plan Yükseltme Oranı |
| **Plan Seçim Dağılımı** | Satın alınan planların planlara göre dağılımı; tanısal. | Plan satın alan | Plan Seçim Oranı |

## Mobil uygulama ve bildirim

| Kanonik ad | Tanım | Payda | Kabul edilen eş anlamlılar |
|---|---|---|---|
| **Net Bildirim İzni Oranı** | Bildirim iznini veren kullanıcıların tüm yeni kullanıcılara oranı; izin istenenlere değil. | Teste atanan yeni kullanıcı | Bildirim İzni Oranı |
| **İlk Oturum Tamamlama Oranı** | İlk oturumda karşılama akışını bitiren yeni kullanıcıların payı. | Teste atanan yeni kullanıcı | İlk Oturum Tamamlama |
| **Uygulama Silme Oranı** | Önceden ilan edilen pencerede uygulamayı silen kullanıcıların payı; guardrail. | Teste atanan kullanıcı | Kaldırma Oranı |
| **Bildirim Kapatma Oranı** | Bildirim iznini sonradan kapatan kullanıcıların payı; guardrail. | İzin veren kullanıcı | Bildirimi Kapatma Oranı |
| **Haber Ver Kayıt Oranı** | Stokta olmayan üründe “haber ver” kaydı bırakan ziyaretçilerin payı. | Tükenen ürün sayfasına atanan ziyaretçi | Stok Bildirimi Kayıt Oranı |
