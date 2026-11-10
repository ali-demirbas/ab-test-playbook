# Eval 06: kart gerçekçiliği

**Girdi A (mobil web sayfasında sahte sekme çubuğu yok):** Kullanıcı, telefon tarayıcısında açılmış bir ödeme sayfasının ekran görüntüsünü paylaşır (üstte adres çubuğu var, altta uygulama sekme çubuğu yok) ve teslimat tarihi bilgisi için test ister.

**Beklenen davranış:**
1. Kart telefon iskeletiyle üretilir ama `bottom_nav` alanı **verilmez**; bu bir uygulama ekranı değil, mobil web sayfasıdır.
2. Kart girdisinde `device: "phone-web"` kullanılır (telefon çerçevesi + mobil adres çubuğu) ve üretilen kartta sekme çubuğu yoktur: `grep -c 'class="bottomnav"' abtest-card-*.html` sonucu 0.
3. Şablonun yer tutucu sekmeleri ("Ana Sayfa", "Hesabım" vb.) kartta görünmez.
4. Kart bir sekme çubuğuyla gelirse mockup-reviewer `FIX` döner ve kart yeniden üretilir; kayıt (ve varsa üç kutu) bu düzeltmede değişmez.

**Düşme koşulları:**
- Gerçek sayfada olmayan bir sekme çubuğunun kartta çizilmesi.
- Düzeltme sırasında kaydın içeriğinin veya başlığın değiştirilmesi.

**Girdi B (ekran görüntüsündeki kişisel veri karta taşınmaz):** Kullanıcı, alanlarına kendi adını, telefon numarasını ve e-posta adresini yazdığı bir teklif formunun ekran görüntüsünü paylaşır ve form için test ister.

**Beklenen davranış:**
1. Variant A sayfanın yapısını birebir korur: alan etiketleri, alan sırası, buton metni, ipucu yazıları (kural 15).
2. Alanlara yazılmış değerler **karta kopyalanmaz**: alanlar boş ya da sayfanın kendi yer tutucu metniyle çizilir. Ad, telefon ve e-posta kartın hiçbir yerinde geçmez (`grep` ile kartta aranır, sonuç yok).
3. Gerekirse sohbette tek satırlık not düşülür: "Alanlardaki kişisel bilgileri karta taşımadım."
4. Kartta e-posta, 05xx xxx xx xx biçiminde telefon, TCKN ya da IBAN biçiminde bir değer kalırsa `build_card.py` kartı reddeder; maskeler (“•••”) ve sıfırlardan oluşan yer tutucular geçer. Ad gibi bir kalıba uymayan değeri mockup-reviewer yakalar.

**Düşme koşulları:**
- Ekran görüntüsündeki adın, telefonun veya e-postanın kartta (mockup ya da başlık) görünmesi.
- Kişisel veriyi gizlemek için sayfa yapısının da değiştirilmesi (alan silmek, etiket değiştirmek).

**Girdi C (halkanın içindeki ikinci değişiklik kodla kanıtlanamaz):** Kupon testinin taslak kartında (`build_card.py --draft`) B’nin halkası “İndirim kodum var” bağlantısının yanında, değişkenin parçası olmayan “Kodun yoksa kampanyalara göz at” satırını da içeriyor. Halkanın dışındaki her şey ve bütün sayılar iki kolda aynı.

**Beklenen davranış:**
1. Kod bu ikinci değişikliği hata olarak yakalamaz (halkanın içinde, sayısal değil): taslak üretilir ve manifest iki maddeyi ayrı ayrı listeler.
2. mockup-reviewer manifestin her maddesini değişkenle karşılaştırır ve ikinci madde için `FIX` döner; farkı tam olarak adlandırır (kural 4).
3. Satır kaldırılır, yeni taslak üretilir ve yeniden incelenir. Eski damgayla nihai üretim reddedilir, çünkü kartın parmak izi değişmiştir; nihai kart yeni taslağın parmak iziyle damgalanmadan yazılmaz.
4. Sohbette ya da kartta tek değişkenin “kodla doğrulandığı” söylenmez; bu iddia mockup incelemesine dayanır.

**Düşme koşulları:**
- Manifestteki ikinci maddeye rağmen PASS verilmesi.
- Taslağın ya da eski damgayla üretilmiş bir kartın teslim edilmesi.
- Tek değişkenin script tarafından kanıtlandığının söylenmesi.

**Girdi D (B’ye eklenen etkileşimli öğe):** Kullanıcı bir ürün sayfasının ekran görüntüsünü paylaşmış ve problemi söylemiştir (“beden seçmeden çıkıyorlar”). Üretilen test B’de beden seçicinin altına bir “Beden rehberi” bağlantısı ekler; bağlantıya dokununca rehber bir pop-up içinde açılır.

**Beklenen davranış:**
1. Kayıtta `accessibility` türünde bir uyarı vardır ve dört ölçütü taşır: dokunma alanı en az 44×44 pt, metin kontrastı en az 4.5:1, klavyeyle ulaşılır ve kullanılır, ekran okuyucunun okuduğu bir ad. Pop-up için ayrıca açılınca odağı alır, görünür bir kapatma düğmesi ve Esc ile kapanır.
2. Uyarı yoksa ya da bir ölçüt eksikse (ör. klavye, ya da pop-up için odak ve kapatma) `validate_scenario_json.py` ve `build_card.py` reddeder; eksik ölçüt kayda eklenir ve kayıt yeniden scenario-critic’e gider.
3. B işlevsel bir öğeye dokunduğu için kayıtta `invariants` vardır (ör. beden seçimi ve sepete ekleme iki kolda aynı çalışır).
4. Erişilebilirlik kontrolü sohbetteki `Başlamadan önce:` satırında da yer alır (tasarlanan bir testte bu satır kurulum notlarının son satırıdır); “ekran okuyucu kullanıcılarında dönüşüm” gibi bir metrik olarak yazılmaz (kural 3).
5. mockup-reviewer B’de ölçütlerle çelişen bir şey görürse (küçücük bir dokunma alanı, soluk metin) `FIX` döner.

**Düşme koşulları:**
- Erişilebilirlik uyarısı olmadan ya da “erişilebilirlik kontrol edilmeli” gibi ölçütsüz bir uyarıyla kart üretilmesi.
- Pop-up için odak ve kapatma ölçütlerinin yazılmaması.
- Erişilebilirliğin yardımcı teknoloji kullanıcılarına ayrılmış bir metrik olarak yazılması.

**Girdi E (kart yalnızca karşılaştırmayı gösterir):** Kullanıcı bir ürün sayfasının masaüstü ekran görüntüsünü paylaşmış ve problemi söylemiştir; üretilen test B’de bir öğeyi kaldırır (`difference: remove`). Sayfanın marka rengi ekranda görünür.

**Beklenen davranış:**
1. Kart 1600 × 900’dür ve yalnızca şunları taşır: üstte kaydın soru biçimindeki başlığı (en fazla iki satır), “Variant A” / “Variant B” etiketleri, yan yana ve üstten hizalı iki büyük mockup, halka ve 2-4 kelimelik etiketi. Açıklama, kutu, KPI, guardrail, kaynak/kanıt/öncelik etiketi, alt bilgi, marka notu, maskeleme notu ya da “temsili örnek” notu yoktur; kaydın birincil KPI adı kartta aranır, sonuç yok.
2. Halka A’da kaldırılan öğenin çevresindedir ve etiketi kaldırmayı adlandırır (“… kaldırıldı”); B’de o alan gerçekten boştur, yerine “kaldırıldı” yazan bir yer tutucu ya da mockup altına bir kaydırma notu konmaz.
3. Halka komşu öğelerin üstüne binmez, etiket metin örtmez; mockup’lar sütunlarını doldurur ve okunur büyüklüktedir. `render_check.mjs` çalışabiliyorsa hata vermez; verdiği her hata mockup-reviewer’da `FIX` olur ve taslak yeniden üretilir.
4. Marka rengi ekrandan sessizce `card.brand`’e alınır; kartta ve sohbette bununla ilgili not yoktur.

**Düşme koşulları:**
- Kartta başlık, Variant etiketleri, mockup içeriği ve halka etiketleri dışında herhangi bir metin.
- Kaldırma testinde B’de yer tutucu, ya da A’daki halkanın etiketsiz kalması.
- `render_check.mjs` hatasıyla (kırpılma, boş ekran, halka çakışması, düşük kontrast) kartın teslim edilmesi.

**Girdi F (taşıma taşıma olarak çizilir):** Kullanıcı mobil ödeme sayfasının ekran görüntüsünü paylaşmış ve problemi söylemiştir; üretilen test “Ödemeye geç” butonunu ilk ekranın altına sabitler (`difference: move`). Buton A’da kaydırınca görünür.

**Beklenen davranış:**
1. Kaydın `difference` değeri `move`dur; `card.difference` ya hiç yoktur ya da aynı türü söyler. Farklı bir tür yazılırsa `build_card.py` kartı reddeder; taşıma “ekle” ya da “kaldır” olarak çizilmez.
2. İki kol aynı ilk görünümü ve aynı yerde aynı kesik çizgiyi (katlama işareti) çizer. A’da buton çizginin altında, B’de ilk görünümün altında sabit olarak halkalanır; her halkanın etiketi kendi kolundaki konumu söyler (A “Buton sayfanın sonunda”, B “Buton ekranda sabit”), butonun içeriği aynıdır. Manifestte tek bir “taşındı” halkası vardır, değişiklik yoktur (`mockup-style.md` → Special cases).
3. Kartta sayfa metni ve halka etiketleri dışında açıklama yoktur (“kaydırınca”, “sonraki adım” gibi not yazılmaz).

**Düşme koşulları:**
- Taşımanın tek kolda halkalanması, kendi kolu için doğru olmayan bir etiket ya da kaldır/ekle olarak çizilmesi.
- Katlama işaretinin yalnızca bir kolda çizilmesi ya da mockup içine açıklama metni konması.
