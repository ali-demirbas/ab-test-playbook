# Arama ve Filtreleme

Yolculuk aşaması: kullanıcı ne istediğini biliyor veya keşfediyor; arama kutusu, filtreler, sonuç sayfası ve site içi navigasyon menüleri (sticky/mega menü senaryoları da bu dosyadadır). Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Filtreler anında mı, toplu mu uygulanmalı?

Değişken: Filtre uygulama biçimi · Fark: değiştir

Etiket: id=sf-001 · mercek=Çaba · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should filters apply instantly or all at once?

EN-Variable: How filters are applied

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

### EN

Instant filtering gives fast feedback; batch filtering offers a more controlled experience. Which one works better for discovery and conversion has to be measured.

**What to test**
- Perceived speed: Does showing results instantly feel smoother?
- Sense of control: Does batch filtering reduce mistaken selections?
- Performance: Does frequent refreshing slow the page down?
- Conversion: Which model gives a higher purchase rate?
- Device: Does batch application win on mobile, where filters open in a full-screen panel, and instant application on desktop, where results stay live beside the filters?

**KPIs to track**
- Conversion Rate (CR): Which filter model brings more sales?
- Filter Usage Rate: In which model are more filters applied?
- Discovery Depth: Are more products viewed?
- Page Refresh Time: Site speed must not degrade.
- Zero-Result Rate: With batch application, mutually exclusive selections must not increase empty result screens.

**What not to do**
- With instant filtering, don’t scroll the page to the top on every click and make the user lose their place.
- Don’t add needless animations and transitions after filtering; they hurt performance.
- Don’t leave cases where the selected filters are not visible or disappear.
- Don’t change both the filter model and the filter set in the same test.
- Don’t use overly aggressive auto-refresh; it tires the user.

---
## Arama çubuğu ne kadar görünür olmalı?

Değişken: Arama alanının görünürlük düzeyi · Fark: değiştir

Etiket: id=sf-002 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: How visible should the search bar be?

EN-Variable: Visibility level of the search field

Arama çubuğunun konumu ve görünürlüğü, kullanıcının ürün keşif davranışını değiştirebilir. Bunun dönüşüme yansıyıp yansımadığı ölçülmelidir.

**Test edilmesi gerekenler**
- Konum: Header’da mı, menü içinde mi, yalnızca ikon olarak mı?
- Görünürlük: Açık arama alanı mı, sadece ikon mu daha çok tıklanıyor?
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

### EN

The position and visibility of the search bar can change how users discover products. Whether this shows up in conversion has to be measured.

**What to test**
- Position: In the header, inside the menu, or as an icon only?
- Visibility: Is an open search field or just an icon clicked more?
- Menu effect: When the search field stands out, does browsing through the category menu drop, that is, does search take the menu’s place?
- Device: Is the visibility need the same on mobile and desktop?

**KPIs to track**
- Conversion Rate (CR): Does the purchase rate of those who search go up?
- Search Usage Rate: Does visibility raise search usage?
- Search Result Click Rate: Do users reach the right product faster?
- Search Success Rate: Must not drop; searches with no results must not increase.
- Time on Page: Does discovery get deeper?

**What not to do**
- On a site with high search usage, don’t put the in-menu arm in the test at all; that arm is tried only when the search share is low.
- Don’t change the placeholder text while changing the visibility of the search field in the same test.
- In the icon variant, don’t show the icon unlabeled or as an unrecognized symbol.
- Don’t shrink the search icon on mobile until it can’t be tapped.
- Don’t leave the user on an empty screen after a search with no results.

---
## Arama kutusundaki önceki arama önerilerini kaldırmak dönüşümü etkiliyor mu?

Değişken: Önceki arama önerileri · Fark: kaldır

Etiket: id=sf-003 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does removing past-search suggestions from the search box affect conversion?

EN-Variable: Past-search suggestions

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

### EN

Listing past searches as default suggestions when the search box opens speeds up starting a search but pulls the user back to their old searches. Removing this default suggestion list (access to history stays on a separate link) can change the discovery process and decision speed.

**What to test**
- Speed: Do searches start faster when there is a default suggestion?
- Discovery: Does not auto-filling raise discovery of new content?
- Empty box: Does an empty search box steer users toward popular categories?
- Device: On mobile, how much of the screen does the suggestion list take while the keyboard is open, and does it change usage?
- History: When past searches are taken off the default list, do users who look for their history complain?

**KPIs to track**
- Conversion Rate (CR): How does purchase after search change?
- Search Usage Rate: Does starting a search go up?
- Time to First Result: Do users get there faster?
- Zero-Result Rate: Must not increase.
- Discovery Depth: Does viewing of new categories go up?

**What not to do**
- Don’t remove past searches entirely; the user must be able to reach their history.
- Don’t add an auto-filled old search to a new search without the user deleting it.
- Don’t change popular search or category suggestions in the same test while removing past-search suggestions.
- Don’t switch off all automatic suggestions and leave the user without direction.
- Don’t show other users’ sensitive searches as popular suggestions.

---
## Sıfır sonuç sayfası kullanıcıyı elde tutuyor mu?

Değişken: Sıfır sonuç ekranındaki öneri blokları · Fark: ekle

Etiket: id=sf-004 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does the zero-results page keep users from leaving?

EN-Variable: Suggestion blocks on the zero-results screen

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

### EN

A search that returns no results is one of the screens with the highest abandonment. Offering a spelling suggestion, popular categories and similar products instead of an empty screen can rescue this traffic.

**What to test**
- Suggestion: How much does a spelling suggestion raise the recovery rate?
- Next test: If the suggestion blocks win, does showing best sellers instead of similar products in the product block raise the recovery rate in a separate test?
- Re-search: Once the suggestion blocks are added, do users turn to the suggestions instead of searching again?
- Relevance: Do users stay on the product page they clicked from the suggestion block, or do they find it irrelevant and go straight back?
- Device: Is behavior different on mobile and desktop?

**KPIs to track**
- Zero-Result Search Purchase Rate: Does the share of sessions that land on a zero-result search (same trigger in both arms) and end in a purchase go up?
- Zero-Result Recovery Rate: Diagnostic metric; the share of users who move on to a product page.
- Session Continuation Rate: Are users not leaving the site?
- Search Conversion Rate (CR): Overall performance must not drop.
- Page Load Time: The suggestion blocks must not slow it down.

**What not to do**
- Don’t suggest irrelevant products and mislead the user.
- Don’t change the position of the search box or the zero-result message in the same test while adding the suggestion blocks.
- Don’t turn the zero-results page into just a campaign area.
- Don’t place the suggestion blocks above the search box and make re-searching harder.
- Don’t apply the spelling suggestion automatically and surprise the user.

---
## Arama sonuçlarında varsayılan sıralama ne olmalı?

Değişken: Arama sonuçlarının varsayılan sıralaması · Fark: değiştir

Etiket: id=sf-005 · mercek=Uygunluk · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: What should the default sort order of search results be?

EN-Variable: Default sort order of search results

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

### EN

The default sort order is the only order the vast majority of users see. Relevance, best-seller and price sorting serve different user groups and affect margin differently.

**What to test**
- Conversion: Which default sort order brings higher conversion?
- Cart: Does best-seller sorting lower average order value?
- Control: How often do users change the sort order manually?
- Long tail: Does relevance work better for rare searches?
- Segment: Is the winner different for new and returning users?

**KPIs to track**
- Search Conversion Rate (CR): The purchase rate of those who search.
- First-Result Click Rate: Hit rate of the top 4 results.
- Sort Change Rate: Is the default enough?
- Average Order Value (AOV): AOV can drop if it drifts toward cheaper items.
- Zero-Interaction Searches: Must not increase.

**What not to do**
- Don’t hide the sort options during the test.
- Don’t move out-of-stock products up the order.
- Don’t change both the sort order and the filter set in the same test.
- Don’t show sponsored products as organic results.
- Don’t arrange the default sort by a rule different from the criterion in its label (“Recommended”, “Best sellers”).

---
## Sticky menü deneyimi iyileştiriyor mu?

Değişken: Menünün kaydırmada sabit kalması · Fark: değiştir

Etiket: id=sf-006 · mercek=Çaba · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does a sticky menu improve the experience?

EN-Variable: Menu staying fixed on scroll

Menünün sabit kalması sayfa içi gezinme hızını artırabilir, ancak ekran alanı kaplayarak rahatsız da edebilir.

**Test edilmesi gerekenler**
- Gezinme: Sticky menü sayfa içi gezinmeyi kolaylaştırıyor mu?
- Kaydırma: Yukarı çıkma zorunluluğunu ortadan kaldırıyor mu?
- Mobil: Uzun sayfalarda gezinme performansını artırıyor mu?
- Alan: Ekran alanını kaplaması rahatsız ediyor mu?

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

### EN

A menu that stays fixed can speed up in-page navigation, but it can also annoy by taking up screen space.

**What to test**
- Navigation: Does a sticky menu make in-page navigation easier?
- Scrolling: Does it remove the need to scroll back up?
- Mobile: Does it improve navigation on long pages?
- Space: Does the space it takes up annoy users?

**KPIs to track**
- Conversion Rate (CR): Does the sticky menu raise purchases?
- Menu Click Rate: Is the menu used more?
- Pages per Session: Are more pages browsed in a session?
- Scroll Depth: Is reading the content hindered?
- Exit Rate: Must not rise; the menu must not drive users away.

**What not to do**
- Don’t make the sticky menu so tall that it covers most of the screen.
- Don’t let the menu cover the CTA and filters on mobile.
- Don’t change the menu items or their order in the same test while fixing the menu.
- Don’t keep hiding and showing the sticky menu by scroll direction and cause flicker.
- Don’t cause page shift when the menu is fixed.

---
## Mega menü mü, yatay menü mü?

Değişken: Ana menünün yapısı · Fark: değiştir

Etiket: id=sf-007 · mercek=Netlik · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Mega menu or horizontal menu?

EN-Variable: Structure of the main menu

Geniş kataloglu bir sitede ziyaretçi aradığı alt kategoriye ana menüden ulaşır. Mega menü, üzerine gelindiğinde ya da tıklandığında bütün alt kategorileri sütunlar hâlinde tek panelde açar: ziyaretçi “erkek ayakkabı → koşu” gibi derin bir kategoriye tek adımda iner; ama çok bağlantılı panel taranamaz hâle gelebilir ve fare panelden kayınca kapanması sinir bozar. Sade yatay menü yalnızca ana kategorileri gösterir ve ziyaretçiyi önce kategori sayfasına götürür: seçim kolaylaşır, ama aranan alt kategori bir sayfa daha uzaktadır. Hangisinin kazanacağı katalog derinliğine ve ziyaretçinin ne aradığını bilip bilmediğine bağlıdır. Mobilde iki yapı da çoğu zaman açılır bir menüye dönüşür; bu senaryo masaüstündeki menü yapısını test eder, mobil menü iki kolda aynı kalır. Kategori adları, sırası ve sayısı iki kolda aynıdır; değişen yalnızca alt kategorilerin menüde mi, kategori sayfasında mı sunulduğudur.

**Test edilmesi gerekenler**
- Derinlik: Mega menü, ziyaretçinin alt kategori sayfasına ulaşmasını kısaltıp satın almaya giden gezinmeyi artırıyor mu?
- Taranabilirlik: Mega menüyü açıp hiçbir bağlantıya tıklamadan kapatan ziyaretçilerin payı, yatay menüde kategori sayfasından geri dönenlerin payından yüksek mi?
- Kayan panel: Fare panelden kayınca menünün istemeden kapanması, mega menü kolunda menüyü tekrar açma denemelerini artırıyor mu?
- Arama kaçışı: Yatay menü kolunda aradığı alt kategoriyi bulamayan ziyaretçi arama kutusuna mı yöneliyor?
- Segment: Ne aradığını bilen dönen ziyaretçi ile göz atan yeni ziyaretçi iki menü yapısına farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Dönüşüm Oranı (CR): Menü yapısı, masaüstünde teste atanan ziyaretçilerin satın alma oranını değiştiriyor mu?
- Alt Kategoriye Doğrudan İniş Oranı: Menüden tek adımda alt kategoriye geçenlerin payı değişiyor mu?
- Menüden Kategoriye Geçiş Oranı: Menüyü açanların kaçı bir kategoriye iniyor?
- Seçimsiz Kapatılan Menü Oranı: Artmamalı; kullanıcı menüde kaybolmamalı.
- Hemen Çıkma Oranı: Yükselmemeli; menü yapısı kullanıcıyı kaçırmamalı.

**Yapılmaması gerekenler**
- Aynı testte menü yapısını değiştirirken kategori adlarını veya sırasını da değiştirmeyin.
- Yatay menü kolunda mega menüdeki alt kategorileri erişilemez bırakmayın; ikinci seviyeye kategori sayfasından bir yol kalmalı.
- Mega menü panelini taranamayacak kadar çok bağlantıyla doldurmayın; sütunlar katalogun gerçek yapısını izler.
- Paneli yalnızca fareyle açılıp fare kayınca hemen kapanan biçimde kurmayın; klavyeyle ve dokunarak da açılıp kapanabilmeli.
- Mobil menüyü bu testte değiştirmeyin; iki kolda aynı kalır.

### EN

On a site with a wide catalog, the visitor reaches the subcategory they want through the main menu. A mega menu opens all subcategories in columns in a single panel on hover or click: the visitor drops to a deep category such as “men’s shoes → running” in one step; but a panel with many links can become unscannable, and it is annoying when it closes as the mouse slips off the panel. A plain horizontal menu shows only the main categories and takes the visitor to a category page first: choosing is easier, but the subcategory they want is one page further away. Which one wins depends on the depth of the catalog and on whether the visitor knows what they are looking for. On mobile both structures often turn into an expandable menu; this scenario tests the desktop menu structure, and the mobile menu stays the same in both arms. Category names, their order and their number are the same in both arms; the only thing that changes is whether subcategories are presented in the menu or on the category page.

**What to test**
- Depth: Does the mega menu shorten the visitor’s path to a subcategory page and increase navigation that leads to purchase?
- Scannability: Is the share of visitors who open the mega menu and close it without clicking any link higher than the share who come back from the category page in the horizontal menu?
- Slipping panel: Does the menu closing unintentionally when the mouse slips off the panel increase attempts to reopen the menu in the mega menu arm?
- Search escape: In the horizontal menu arm, do visitors who can’t find the subcategory they want turn to the search box?
- Segment: Do returning visitors who know what they want and new visitors who browse react differently to the two menu structures?

**KPIs to track**
- Conversion Rate (CR): Does the menu structure change the purchase rate of visitors assigned to the test on desktop?
- Direct Subcategory Landing Rate: Does the share who go from the menu to a subcategory in one step change?
- Menu-to-Category Click Rate: What share of those who open the menu land on a category?
- Menu Closed Without Selection Rate: Must not increase; the user must not get lost in the menu.
- Bounce Rate: Must not rise; the menu structure must not drive users away.

**What not to do**
- Don’t change the category names or their order in the same test while changing the menu structure.
- In the horizontal menu arm, don’t leave the mega menu’s subcategories unreachable; a path to the second level must remain from the category page.
- Don’t fill the mega menu panel with so many links that it can’t be scanned; the columns follow the real structure of the catalog.
- Don’t build the panel so that it opens only with the mouse and closes the instant the mouse slips; it must open and close by keyboard and touch too.
- Don’t change the mobile menu in this test; it stays the same in both arms.

---
## Menü sadeleştirmesi deneyimi etkiler mi?

Değişken: Menüdeki alt başlık sayısı · Fark: kaldır

Etiket: id=sf-008 · mercek=Netlik · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does simplifying the menu affect the experience?

EN-Variable: Number of sub-items in the menu

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

### EN

Simplifying the menu can affect navigation speed and category discovery. A less complex menu can make it easier to focus.

**What to test**
- Simplicity: Does reducing the number of sub-items make it easier to focus?
- Speed: Does the simpler menu get users to the category they want faster?
- Device: Is the effect of simplification bigger in the mobile menu than on desktop?
- Time: Does navigation time get meaningfully shorter?
- Discovery: Does the number of categories discovered drop once the menu is simplified?

**KPIs to track**
- Conversion Rate (CR): Does the simpler menu raise purchases?
- Time to First Click: Does reaching the right category get shorter?
- Menu Click Depth: Is the goal reached in fewer steps?
- Category Coverage Rate: Must not drop; the number of categories discovered must not narrow.
- Search Usage Rate: Does the menu fall short and push users to search?

**What not to do**
- Don’t remove the main categories entirely; it creates a sense of lost information.
- Don’t cut sub-items so far that discovery is restricted.
- Don’t leave old links to the removed sub-items without redirects.
- On mobile, don’t let the sticky menu cover critical areas.
- Don’t change the names or order of the remaining items in the same test while reducing sub-items.

---
## İndirim filtresi davranışı nasıl etkiler?

Değişken: İndirim oranı filtresi · Fark: ekle

Etiket: id=sf-009 · mercek=Fiyat · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: How does a discount filter affect behavior?

EN-Variable: Discount-rate filter

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
- Uydurma referans fiyattan hesaplanan indirim oranını filtreye dahil etmeyin; filtre yalnızca gerçek indirimi göstermeli.
- Mobilde filtre alanını ekranı kaplayacak kadar büyütmeyin.
- Aynı testte indirim filtresini eklerken varsayılan sıralamayı veya diğer filtrelerin sırasını da değiştirmeyin.

### EN

Offering filtering by discount percentage can speed up product discovery and get price-sensitive users to their goal more quickly.

**What to test**
- Adding: Does the discount filter raise add-to-cart behavior?
- Speed: Do price-sensitive users find a product faster?
- Neighboring filters: Once the discount filter is added, does use of the price range filter drop, that is, does one replace the other?
- Device: How does usage differ on mobile and desktop?
- Decision: As filter usage rises, does decision time get shorter?

**KPIs to track**
- Revenue per Visitor (RPV): Does the discount filter raise revenue? The primary decision is made on this metric.
- Conversion Rate (CR): Does the discount filter raise purchases?
- Add-to-Cart Rate: Do those who filter add more?
- Average Order Value (AOV): Does leaning toward discounts shrink the cart?
- Gross Margin: Must not drop; the shift toward discounted products must not erode profit.

**What not to do**
- Don’t add too many filters and leave the user undecided.
- Don’t design discount ranges that give inconsistent results.
- Don’t include in the filter a discount rate calculated from a made-up reference price; the filter must show only real discounts.
- Don’t enlarge the filter area on mobile until it covers the screen.
- Don’t change the default sort order or the order of the other filters in the same test while adding the discount filter.

---
## Filtreler kaydırma boyunca görünür kalmalı mı?

Değişken: Filtre panelinin kaydırmada sabit kalması · Fark: değiştir

Etiket: id=sf-010 · mercek=Çaba · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Should filters stay visible while scrolling?

EN-Variable: Filter panel staying fixed on scroll

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

### EN

Keeping the filter panel on screen while the page scrolls means a user who changes their mind in the middle of the list doesn’t have to go back up. The cost: the panel takes space constantly, the area left for products narrows and on mobile it can eat a large part of the screen.

**What to test**
- Persistence: Does filter usage go up when the filters stay visible?
- Space: Does the narrower product area lower the number of products viewed?
- Next test: If staying fixed wins, does keeping only a filter button fixed instead of the full panel win back the product area in a separate test?
- Mid-list: Does the share of users who change a filter in the middle of the list go up with a fixed panel?
- Device: Is the fixed panel’s effect on filter usage bigger on desktop or on mobile?

**KPIs to track**
- Conversion Rate (CR): Does filter access turn into sales?
- Filter Usage Rate: Does the share of users who apply a filter go up?
- Products Viewed per Visitor: The narrower area must not lower the number of products viewed unacceptably.
- List-to-Product Click Rate: Moving on to a product must not drop.
- Zero-Result Rate: Easier filtering must not increase the number of empty results.

**What not to do**
- Don’t change the filter persistence and the filter options in the same test.
- Don’t build the fixed panel so large that it covers half the screen.
- On mobile, don’t leave the fixed panel as a block that can’t be collapsed with one tap.
- Don’t leave the content that falls under the fixed panel unreachable.
- Don’t break the focus order of the fixed panel when navigating by keyboard.

---
## Filtreleri açıkta göstermek mi, düğme arkasına almak mı daha iyi çalışıyor?

Değişken: Filtrelerin görünürlüğü · Fark: değiştir

Etiket: id=sf-011 · mercek=Netlik · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Show filters openly or behind a button: which works better?

EN-Variable: Visibility of the filters

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
- Görev Tamamlama Süresi (aranan ürüne ulaşma): Doğru ürüne ulaşma hızlanıyor mu?
- Görülen Ürün Sayısı: Daralan alan görülen ürün sayısını düşürmemeli.
- Sayfa Yüklenme Süresi: Açıktaki filtre paneli ve seçenek sayıları listenin yüklenmesini (LCP) geciktirmemeli.

**Yapılmaması gerekenler**
- Aynı testte filtre görünürlüğü ile filtre sayısını birlikte değiştirmeyin.
- Açıkta gösterdiğiniz filtreleri kategoriye göre değiştirip testi karıştırmayın.
- Açık düzende filtre panelini, ilk ürün satırını ilk ekranın dışına itecek kadar uzatmayın.
- Düğme arkasındaki filtreye kaç filtre uygulandığını gösteren işareti kaldırmayın.
- Tek kategoride ölçüp sonucu filtre yapısı çok farklı kategorilere taşımayın.

### EN

Making filters directly visible reminds users that they exist and raises usage. Putting them behind a button leaves more room for products and simplifies the page; on the other hand, a user who doesn’t know a filter exists browses without ever filtering and can’t find the right product.

**What to test**
- Visibility: Do open filters raise usage?
- Awareness: How many users open the filter behind a button?
- Next test: If the open layout wins, does leaving only the most used filters open and putting the rest behind a button reduce list abandonment in a separate test?
- Space: How much do open filters narrow the product area?
- Device: Is a layout that is open on desktop and behind a button on mobile better?

**KPIs to track**
- Conversion Rate (CR): Does filter visibility turn into sales?
- Filter Usage Rate: Does the share of users who apply a filter go up?
- Task Completion Time (reaching the searched product): Does reaching the right product get faster?
- Products Viewed per Visitor: The narrower area must not lower the number of products viewed.
- Page Load Time: The open filter panel and the number of options must not delay loading of the list (LCP).

**What not to do**
- Don’t change filter visibility and the number of filters in the same test.
- Don’t vary the filters you show openly by category and muddy the test.
- In the open layout, don’t make the filter panel so long that it pushes the first row of products out of the first screen.
- Don’t remove the indicator on the button-hidden filter that shows how many filters are applied.
- Don’t measure in a single category and carry the result over to categories with very different filter structures.

---
## Arama kelimesini sonuçlarda vurgulamak işe yarar mı?

Değişken: Aranan kelimenin sonuçlarda vurgulanması · Fark: ekle

Etiket: id=sf-012 · mercek=Netlik · düzey=gezinme · sektör=genel · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does highlighting the search term in the results pay off?

EN-Variable: Highlighting the search term in results

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

### EN

Marking the search term in result titles shows where the match is and speeds up reaching the right result. The risk: the highlight creates visual noise, with many matches the title becomes unreadable and when an irrelevant match is highlighted the search looks poor in quality.

**What to test**
- Highlight: Does marking the keyword raise result clicks?
- Density: Do many highlights hurt readability?
- Scope: Should the highlight be in the title only or in the description too?
- Perceived quality: Does highlighting a weak match lower trust in search?
- Device: Is the highlight still meaningful in titles that get shortened on mobile?

**KPIs to track**
- Conversion Rate (CR): Does the rate from search to sale go up?
- Search Result Click Rate: Diagnostic metric; do clicks on results go up?
- Repeat Search Rate: The same user searching again must not increase.
- Back-Navigation Rate: Users who click a highlighted weak match and go straight back from the product page to the results must not increase.
- Accessibility Check: The highlight must not rely on color alone and contrast must be kept.

**What not to do**
- Don’t do the highlight by color alone and skip a contrast and format difference.
- Don’t change the highlight and the result order in the same test.
- Don’t set up matching so broad that half the title is highlighted.
- Don’t use the highlight as a substitute for fixing search quality; the real problem may be the ranking.
- Don’t measure on one-word searches and generalize the result to long queries.

---
## Filtreleri seçenek listesi yerine cümle hâlinde sormak işe yarar mı?

Değişken: Filtrelerin sorulma biçimi · Fark: değiştir

Etiket: id=sf-013 · mercek=Uygunluk · düzey=gezinme · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does asking filters as a sentence instead of option lists pay off?

EN-Variable: How filters are asked

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
- Görev Tamamlama Süresi (aranan ürüne ulaşma): Toplam süre uzamamalı.

**Yapılmaması gerekenler**
- Soru akışını atlanamaz hâle getirip klasik filtreyi kaldırmayın.
- Aynı testte soru sayısı ile soru içeriğini birlikte değiştirmeyin.
- Akışın sonunda boş sonuç veren kombinasyonları çıkışsız bırakmayın.
- Cevapları sonraki ziyarette kullanıcıya sormadan kalıcı hâle getirmeyin.
- Akışın getirdiği sonuç kümesinde hangi cevapların uygulandığını gizlemeyin; kullanıcı her birini tek tek geri alabilmeli.

### EN

Turning filters into a question flow such as “who is it for, what budget” guides a user who doesn’t quite know what they are looking for. On the other side: for a user who knows what they want it is an extra step, the flow slows them down and it gives less precise results than a classic filter.

**What to test**
- Format: Is the question flow used more than the classic filter?
- User type: Can a user who knows what they want skip the flow?
- Length: At how many questions does abandonment start?
- Precision: Is the result set the flow produces accurate enough?
- Segment: Does a new visitor seeing the catalog for the first time find more accurate results through the question flow than a returning user who knows the products?

**KPIs to track**
- Conversion Rate (CR): Does the question flow turn into sales?
- Flow Completion Rate: What share of users finish the questions?
- Classic Filter Usage: Access to the filter for experienced users must not be lost.
- Zero-Result Rate: Empty results at the end of the flow must not increase.
- Task Completion Time (reaching the searched product): Total time must not lengthen.

**What not to do**
- Don’t make the question flow impossible to skip and remove the classic filter.
- Don’t change the number of questions and their content in the same test.
- Don’t leave combinations that end in an empty result at the end of the flow with no way out.
- Don’t make answers persistent on the next visit without asking the user.
- Don’t hide which answers were applied in the result set the flow produces; the user must be able to undo each one individually.
