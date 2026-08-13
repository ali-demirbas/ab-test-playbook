---
name: abtest-suggest
description: Suggest proven A/B test scenarios for a given page or journey stage, ranked by ICE. Use when the user asks "what should I test", "what should I A/B test on my checkout / cart / product page / pricing page / homepage", "give me A/B test ideas", "experiment ideas", "split test ideas", "CRO ideas", "which tests should I run first", "what tests are worth running", "test öner", "hangi testleri yapmalıyım", "checkout için hangi testler", "anasayfam için test fikirleri", "ne test edeyim". Picks matching scenarios from the curated archive in knowledge/scenarios/ (e-commerce, mobile app, SaaS/B2B, search and filtering, forms, pricing) and delivers each as an HTML card via abtest-card. For a test designed specifically for a page or screenshot you share, see abtest-design. To review a plan you already have, see abtest-audit.
metadata:
  version: 0.1.0
  category: recommend
  updated: 2026-08-11
---

# abtest-suggest — Arşivden Test Önerisi

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` kuralları bağlayıcıdır.

## Akış

1. Router'dan gelen bağlamı al (sektör, sayfa). **Trafik, test aracı ve kurulum bilgisi sorulmaz** (CLAUDE.md kural 5 ve 13): senaryo üretmek için gerekli değildir, eksik diye çıktının önüne konmaz. Bunlar yalnızca kullanıcı süre, örneklem veya anlamlılık sorduğunda istenir. Sektör veya sayfa da belirsizse en yakın aşamayı seç ve varsayımını tek cümleyle söyle, soru sorup akışı durdurma.
   - **Test hafızasını oku (CLAUDE.md kural 16).** Kullanıcının çalışma dizininde `.abtest-history.md` var mı bak. Varsa oku ve hedef sayfaya ait kayıtları çıkar. Yoksa arama yaptığını anlatma, sessizce devam et; çıktının sonunda bir kez öner: "Test geçmişini `.abtest-history.md` olarak tutarsan önerileri geçmiş sonuçlarına göre süzebilirim."
2. Sayfa/akışı yolculuk aşamasına eşle ve ilgili dosyayı oku:
   - Anasayfa, landing, kampanya sayfası → `knowledge/scenarios/home-landing.md`
   - Arama, filtre, sonuç sayfası → `knowledge/scenarios/search-filtering.md`
   - Menü ve site içi navigasyon → `knowledge/scenarios/search-filtering.md`
   - Kategori/liste sayfası → `knowledge/scenarios/category-listing.md`
   - Ürün detay → `knowledge/scenarios/product-detail.md`
   - Sepet, kupon, ödeme, adres → `knowledge/scenarios/cart-checkout.md`
   - Form, kayıt, giriş → `knowledge/scenarios/forms-signup.md`
   - Fiyat sayfası, fiyat gösterimi, plan karşılaştırma → `knowledge/scenarios/pricing.md`
   - Uygulama onboarding/izin/anasayfa → `knowledge/scenarios/mobile-app.md`
   - SaaS ticari kararları (plan varsayılanı, deneme süresi, paywall) → `knowledge/scenarios/saas-b2b.md`
   - Buton, bağlantı, ikon gibi sayfadan bağımsız öğeler → `knowledge/scenarios/ui-elements.md` (alt kademedir: daha yüksek kademeden güçlü aday varken birinci sıraya konmaz, ama sayfada gözlemlenebilir bir engele dayanan güçlü mekanizması olan senaryo önerilir — `methodology.md` → etki sıralaması. Trafiğin düşük olduğu biliniyorsa bu dosyadan öneri yapma; bilinmiyorsa sormadan varsayma)
   - Birden fazla aşama isteniyorsa ilgili dosyaların hepsini oku. **Form içeren her sayfada `forms-signup.md`'yi de oku**: checkout adres formu, lead formu ve kayıt ekranı bağlam dosyasında yer alır, ama formun kendi tasarımına (etiket konumu, alan sırası, giriş yöntemi) dair senaryolar yalnızca o dosyadadır.
   - **Huniyi teşhis et.** Kullanıcı hangi adımda kayıp yaşandığını söylediyse (kural 13'teki problem sorusu buna cevap verir) önce iki şeyi ayır: **tıkalı damar** — trafiği yüksek ama dönüşümü düşük bir adım (buradaki küçük bir iyileştirme bile çok kullanıcıyı etkiler, öncelik burada) ve **eksik halka** — huninin olması gereken bir adımı hiç içermemesi (ör. sepette teslimat tarihi hiç yok). İkisi farklı öncelik taşır: tıkalı damarda mevcut adımı iyileştir, eksik halkada yeni bir öğe ekle (methodology.md → Değişken izolasyonu, "ekleme" ekseni).
3. Kullanıcının bağlamına uyan 2-5 senaryo seç. Uymayanı eleme gerekçesiyle birlikte at (ör. düşük trafikli sayfaya iade-oranı-birincil test önerme). 5'ten fazla güçlü aday varsa hepsini sormadan seçme — adım 6'daki kural geçerlidir.
   - **Geçmişle karşılaştır.** Bir senaryo aynı sayfada aynı değişkeni daha önce test etmişse:
     - **kazandı** → tekrar önerme; onun yerine kazanan değişikliğin üzerine kurulacak bir sonraki adımı öner.
     - **kaybetti / fark yok** → otomatik eleme yok (kural 16: geçmiş veto değildir). Önce yeniden denemeyi haklı kılan bir sebep ara: sayfa o testten sonra değişti mi, farklı segment/pazar mı soruluyor, aradan uzun süre geçti mi, önceki koşum yetersiz miydi. Sebep varsa gerekçesiyle öner: "Mart'ta kaybetmişti, ama o testten sonra kart tasarımı değişti." Sebep yoksa bu turda listeye almamayı seç ve bunu tek cümleyle söyle — sessizce eleme.
     - **yetersiz / geçersiz** → bu bir sonuç değildir; senaryoyu normal şekilde öner ve "daha önce denendi ama ölçülemedi" diye not düş.
   - Aynı sayfada art arda "fark yok" kaydı varsa küçük varyasyon önermeyi bırak; daha yapısal bir değişiklik öner ve nedenini söyle (methodology.md → yerel tepe riski).
   - Geçmiş kayıt bir senaryonun güven düzeyini de değiştirir: kullanıcının kendi ürününde kazanmış bir desen `Kanıt: kullanıcının kendi verisi` olur.
   - **"Genellenebilir örüntü" sütununu farklı sayfalar için de kullan.** Bir satırda dolu bir örüntü varsa (ör. "ilerleme göstergesi harcama davranışını güçlendiriyor") ve önerdiğin sayfa aynı mekanizmaya uyuyorsa, bunu ayrı bir senaryo olarak öner ve gerekçesini söyle: "[X sayfasında] aynı mekanizma kazanmıştı, burada da işe yarayabilir." Otomatik varsayma — hâlâ ayrı, tek değişkenli bir test olarak kurulur.
4. **Mercekten geçir, sonra ICE ile sırala (`methodology.md` → Fikir üretme merceği).** Arşivden seçilen adaylar ICE'a girmeden önce iki elemeden geçer: (a) **mekanizma tekrarı** — aynı sayfa alanında aynı davranış mekanizmasına dayanan iki senaryoyu ayrı öneri diye sunma, birleştir veya en güçlüsünü seç; (b) **etki sıralaması** — kapıdan geçen adaylar arasında teklif/akış/karar anındaki bilgi/bilgi mimarisi önce, hiyerarşi ve itiraz cevaplayan metin sonra, renk ve jenerik CTA kelimesi en sonda gelir. Bu bir yasak değildir: üçüncü kademeden bir aday güçlü bir mekanizmaya sahipse önerilir. Test hafızası bu sıralamayı yalnızca **aynı bileşen veya aynı mekanizma** için ezer, tüm kademeyi değil.
5. ICE ile sırala: Etki × Güven × Kolaylık. Puanlama skalası ve eşitlik bozma sırası `knowledge/methodology.md` → Önceliklendirme (ICE) bölümündedir; aynı girdiye aynı sıralamayı üret. Her önerinin yanına tek cümlelik ICE gerekçesi yaz.
6. **Denetle (CLAUDE.md kural 17).** Seçilen senaryoları karta basmadan önce `agents/scenario-critic`'e ver. `FIX` dönen maddeyi düzelt ve denetimi tekrarla; `RET` dönen senaryoyu üretme, elenme gerekçesini kullanıcıya tek cümleyle söyle. Denetim raporunu sohbete dökme (kural 9). Arşivden gelen senaryo da denetlenir — arşivde durması bu sayfa için geçerli olduğunu göstermez (pazar bağımlılığı, bayatlama, test hafızası).
7. Marka kılavuzu sorusu bu oturumda sorulmadıysa önce onu sor (kural 12). Ardından denetimden geçen her senaryoyu (2-5 arası) doğrudan `abtest-card` ile HTML'e çevir (CLAUDE.md kural 9) — üç kutunun tam içeriği yalnızca kartta bulunur, sohbete ayrıca metin olarak yazılmaz.

## Çıktı biçimi

Sohbette senaryo başına yalnızca kısa bir üst bilgi kalır (üç kutu değil — o kartın içindedir):

```
## <Soru biçiminde başlık>  (arşivden · ICE: Yüksek — <tek cümle gerekçe> · Kanıt: <kullanıcının kendi verisi / arşiv emsali / sektör gözlemi / sezgi>)
<tek cümlelik mekanizma> → `abtest-card-<slug>.html`
```

5'ten fazla güçlü aday varsa hepsini sormadan üretme: kaç aday olduğunu söyle ve devam edilip edilmeyeceğini sor — bu kural 13'ün tek istisnasıdır (CLAUDE.md kural 9).

Liste sonunda, öneri kümesinin güveni zayıfsa bunu tek cümleyle söyle — sessizce güçlü gibi sunma. Zayıflık kaynakları: kullanıcı hiç veri paylaşmadı, arşivde bu bağlama yakın emsal yok, sektör/sayfa bilgisi kaba kaldı, trafik bilinmiyor. Örnek: "Bu öneriler yalnızca sayfa tipine dayanıyor; kendi huni verini paylaşırsan sıralama değişebilir."

## Asla yapma

- Pazara bağlı bir senaryoyu (altında "Pazar notu" olanlar) o notu iletmeden önerme; kullanıcının hedef pazarı bilinmiyorsa önce sor (CLAUDE.md kural 11).
- Geçerliliği düşmüş senaryoyu sessizce önerme: platform kuralı, mevzuat veya standartlaşma senaryonun zeminini kaydırdıysa bunu söyle veya hiç önerme (`knowledge/methodology.md` → Arşiv bayatlar).
- Arşivdeki metni kullanıcının bağlamına uyarlamadan kopyalama — sektöre/ürüne göre örnekleri yerelleştir (ör. moda sitesiyse "Kablosuz Kulaklık" değil giyim örneği).
- Beş senaryodan fazlasını sormadan üretme; sayıyı söyle ve kullanıcıya sor (kural 9).
- Üç kutunun tam içeriğini kartın yanında ayrıca sohbete metin olarak yazma (kural 9) — yalnızca kullanıcı açıkça metin hâlini isterse ayrıca yaz.
- Senaryo başlıklarını listeleyip "hangisini açayım" diye sorma (CLAUDE.md kural 13); seçilenleri doğrudan kart olarak ver.
