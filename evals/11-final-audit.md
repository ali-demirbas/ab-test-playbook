# Eval 11: son denetim, yeniden koşulan dokuz senaryo

3.0.0 öncesi son denetimde yeniden koşulan dokuz senaryonun beklenen ana davranışları. Her girdide genel ölçütler de geçerlidir: sohbette senaryo başına dört satır (başlık, etiket satırı, en fazla 140 karakterlik `Neden:` satırı, kart dosyası), listeden sonra yalnızca geçerli satırlar (scenario-critic planlanan sohbetin tamamını görür), en fazla bir soru ve tek cümle, Türkçe metinde uzun tire yok, iki damga olmadan kart yok.

**Girdi A (kupon bağlantı arkasında):** Sepet sayfası, açık kupon kutusu; problem: kod aramaya gidiyorlar.
- `difference: change`; B’de kutu “İndirim kodum var” bağlantısının arkasındadır, halka B’dedir.
- Birincil “Ziyaretçi Başına Gelir (RPV)” (iş hedefi netleşene kadar); guardrail “Kuponlu Sipariş Veren Ziyaretçi Oranı” atanan ziyaretçi başına, sipariş başına değil. Kod sahibi segmenti uydurulmaz.
- Üç `invariants` maddesi (kod aynı adımla uygulanır, indirim ve toplamlar aynı, hata mesajı aynı); bağlantı için ölçütlü erişilebilirlik uyarısı (odak alana geçer) ve `Başlamadan önce:` satırı.

**Girdi B (sabit ödeme butonu):** Mobil ödeme sayfası; buton kaydırınca görünüyor, B’de ilk ekranın altına sabitleniyor.
- `difference: move`, `card.difference` yok ya da aynı. İki kol aynı ilk görünümü ve aynı katlama çizgisini çizer; A butonu çizginin altında, B ilk görünümün altında halkalar; etiket ve içerik aynı, manifestte tek “taşındı” halkası.
- Ekle/kaldır olarak çizilmez; mockup içinde açıklama metni yoktur.

**Girdi C (ücretsiz kargo çubuğu):** Sepette “X TL kaldı” çubuğu ekleniyor; eşik sayfada yazıyor.
- `difference: add`, halka yalnızca B’de. Kalan tutar sayfadaki eşikten hesaplanır: `numeric_change` nedenini söyler, nasıl hesaplandığı sohbette tek satırdır. Eşik bilinmiyorsa uydurulmaz, sorulur.
- Kargo beklentisi pazara bağlıdır: `market` uyarısı. Sayfadaki eşik bir iddia sayılmaz; “sepet tutarı yüzde 15 artar” gibi bir tahmin yazılmaz.

**Girdi D (SaaS’ta yıllık plan varsayılanı):** Fiyat sayfasında aylık seçili; B yıllığı varsayılan yapıyor; yıllık fiyatın kartta nasıl göründüğü bilinmiyor.
- Koşullu öneri: soru taşıyan `critical` varsayım, öncelik en fazla Orta, nihai kartta “KOŞULLU · doğrulanacak” bandı; sohbette doğrulanacak olguyu adlandıran “Koşullu (1): 1 için yıllık planın kartta görünen fiyatı.” satırı ve turun tek sorusu olarak en kritik olgu (“Yıllık plan kartta hangi fiyatla görünüyor?”). Birincil KPI satırı yazılırsa bu değeri gelir ya da tahsilat diye anmaz.
- “Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)” ile “Tahsilat (gözlem penceresi, atanan ziyaretçi başına)” ayrı tutulur; aylığa normalize değer gerçekleşmiş ziyaretçi başına gelir gibi sunulmaz.
- Kullanıcı fiyatı doğrulayınca varsayım kaldırılır, kayıt yeniden incelenir, kart bantsız yazılır.

**Girdi E (onboarding’de “Atla”):** Uygulama tanıtım slaytlarına “Atla” metin butonu ekleniyor.
- Buton ekranın kendi metin renginde bir metin olarak çizilir (`Special cases` → Text buttons); erişilebilirlik uyarısı dokunma alanını, ekran okuyucu adını ve klavyeyi sayar.
- Birincil tamamlanan kayıt; guardrail daha sonraki bir adım (ör. 7 günlük aktivasyon). Yerel uygulama sürümü gerektiği için kolaylık düşük, gerekçe bunu söyler.

**Girdi F (yumuşak kayıt duvarı korunur):** B kayıt duvarını kapatılabilir yumuşak bir pencereye çeviriyor; ilk kayıtta odak ve Esc ölçütleri eksik.
- scenario-critic eksikleri ilk turda birlikte, `[fixable]` olarak bildirir; üretici tarif edilen ölçütleri ekler, sonraki incelemede PASS gelir. Öneri düşürülmez, `[blocking]` sayılmaz.
- Pencere görünür bir kapatma düğmesi ve Esc ile kapanır, açılınca odağı alır.

**Girdi G (sigorta adım adları):** Teklif akışına adım göstergesi ekleniyor; gerçek adım adları ekranda yok.
- Adım adları uydurulmaz: soru taşıyan `critical` varsayım (“Akıştaki adımların gerçek adları neler?”), en fazla Orta, koşullu kart.
- Düzenlenen akış, düzenlenen gösterime dokunmayan B: `regulation` uyarısı ve `Başlamadan önce:` satırında uyum onayı.

**Girdi H (TC kimlik alanına gerekçe satırı):** Teklif formunda TC kimlik numarası alanı sürtünme yaratıyor.
- Alan kaldırılmaz; tek değişken “neden istendiğini yazmak” (kural 14). Satır yalnızca aydınlatma metnindeki amacı tekrar ettiği için durum (b): `regulation` uyarısı ve uyum onayı.
- Aydınlatma metnindeki amaç bilinmiyorsa öneri koşulludur (“Aydınlatma metni TC kimlik numarasının amacını nasıl yazıyor?”); amaç uydurulmaz.

**Girdi I (telefon teklif sonrasına taşınır):** Telefon alanı ilk adımdan teklif sonrasına alınıyor.
- `difference: move`; iki kol aynı iki aşamayı ayrı ekranlar olarak çizer (`.r-stage-break`, `card.stage_captions`: ilk adım ve “Teklifiniz hazır” ekranı); A alanı ilk adımda, B teklif ekranında halkalar. Her etiket kendi kolundaki gerçek konumu söyler (A “Telefon ilk adımda”, B “Telefon teklif sonrasında”).
- Telefonun teklif ya da SMS doğrulaması için teklif öncesinde gerekip gerekmediği bilinmiyorsa öneri koşulludur (soru taşıyan `critical` varsayım, en fazla Orta). Alan boş çizilir, kişisel değer taşınmaz.

**Düşme koşulları:**
- Taşımanın ekle/kaldır olarak ya da tek kolda çizilmesi; `card.difference` ile kaydın farkının ayrışması.
- Doğrulanmamış bir bilginin (fiyat gösterimi, adım adı, yasal amaç, telefon ihtiyacı) uydurulması ya da güçlü önerinin koşullu öneri yerine düşürülmesi; koşullu bir kaydın Yüksek önceliği.
- Aylığa normalize abonelik değerinin tahsilat ya da gerçekleşmiş gelir gibi sunulması.
- Düzeltilebilir bir erişilebilirlik eksiği yüzünden önerinin düşürülmesi ya da eksiklerin turlara bölünmesi.
- Sohbette senaryo başına dört satırdan fazlası, iki soru ya da kanıtsız artış iddiası.
