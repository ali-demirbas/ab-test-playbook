---
name: abtest-design
description: Design a NEW A/B test scenario for the user's specific page, feature or funnel step, in the archive's disciplined three-box framework. Use when the user shares a page/screenshot/URL/feature description and asks "bunun için test tasarla", "bu akışta ne test edilir", "design an experiment for this".
metadata:
  version: 0.1.0
  category: generate
  updated: 2026-08-11
---

# abtest-design — Yeni Senaryo Tasarımı

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` kuralları bağlayıcıdır. Formatın tanımı `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md`'dedir — üretmeden önce oku.

## Akış

1. Kullanıcının paylaştığı sayfayı/özelliği anla (ekran görüntüsü, URL, açıklama), **iki geçişte**:

   **Önce problem netleşir.** Sayfa paylaşıldıysa hangi problemin çözüleceği tek çoktan seçmeli soruyla belirlenir (CLAUDE.md kural 13); router sormadıysa burada sor. Kullanıcı doğrudan bir çözüm söylediyse ("butonu büyütelim") bunun hangi problemi çözdüğünü aynı soruyla netleştir; söylediği çözüm söylediği problemi çözmüyorsa bunu söyle ve probleme uyan bir varyant öner — istediğini sessizce tasarlama. Cevap gelmezse yine de devam et ama hipotezin dayanağını "sezgi" diye işaretle (kural 10).

   **Sonra adaylar üç eksende birden çıkarılır**, yalnızca ilkine bakma:
   - **Değiştir:** Sayfada var olan bir öğenin biçimi, metni, konumu veya görsel ağırlığı.
   - **Kaldır:** Sayfada var olan ama akışa engel olan bir öğe.
   - **Ekle:** Sayfada **olmayan** ama o adımda kullanıcının ihtiyaç duyduğu bilgi veya aksiyon — çoğu zaman en büyük kazancı taşır ve en kolay atlanan olandır (ör. ödeme adımında teslimat tarihi, taksit seçeneği; bir duyuruda karşılığı olan aksiyon butonu). Öneride bulunmadan önce öğenin gerçekten yok mu yoksa açılır bir bölümde/sonraki adımda mı olduğunu doğrula; ekran görüntüsünden ayırt edilemiyorsa senaryoyu kurmadan önce sor (bkz. "Asla yapma").

   Üç eksenin üstüne **fırsat taraması** eklenir (`methodology.md` → Fikir üretme merceği): beş itiraz merceğinden (Güven, Fiyat, Uygunluk, Zamanlama, Efor) geçerek bu sayfada karşılıksız kalan var mı bak — karşılıksız itiraz doğrudan bir test adayıdır. Karşılığı zaten olan merceği atla; her mercekten fikir üretmek zorunlu değildir, ilgisiz mercekten fikir zorlamak sayfayla alakasız öneri üretir.
2. En yakın yolculuk aşamasının senaryo dosyasını oku (`knowledge/scenarios/`) — hem üslup referansı hem tekrar önleme için: arşivde zaten varsa üretme, `abtest-suggest` gibi arşivden getir ve "arşivden" diye işaretle.
   - **Test hafızasını da oku (CLAUDE.md kural 16):** çalışma dizininde `.abtest-history.md` varsa, tasarlamak üzere olduğun değişken bu sayfada daha önce test edilmiş mi bak. Edilmişse bunu çıktının başında söyle ve kural 16'ya göre kendin karar ver — kullanıcıya sormadan (kural 13, ikinci onay sorusu yok): yeniden denemeyi haklı kılan bir sebep varsa (sayfa değişti, farklı segment/pazar, önceki koşum yetersizdi) aynı değişkeni gerekçesiyle tasarla; yoksa kazanan/kaybeden üzerine kurulacak bir sonraki adımı tasarla ve seçimini tek cümleyle gerekçelendir. Sessizce aynı testi yeniden üretme.
   - Geçmişte kazanmış bir değişikliğin üzerine tasarlıyorsan bunu hipotezin dayanağı olarak kullan: `Kanıt: kullanıcının kendi verisi`.
3. Tek değişkenli bir hipotez kur, `methodology.md`'deki üç parçayla: **Teori** (neden bu değişikliği öneriyoruz), **Dayanak** (hangi veri/gözlem/geri bildirim destekliyor — yoksa "sezgi" diye işaretle), **Öğrenilecek şey** (kazanırsa ve kaybederse ne öğreniriz). Açıklama paragrafında bu üçü zımnen geçer; kullanıcı ayrı ayrı isterse üç satır halinde yaz. Tek cümlelik özet için `methodology.md` → "Hipotez üç parçalıdır" bölümündeki doldurma şablonunu kullan; ayrı bir kalıp üretme. Birden fazla güçlü aday varsa ayrı senaryolar olarak sun, tek teste sıkıştırma.
   - Önerilen değişiklik metrikte fark yaratamayacak kadar silikse (ör. birkaç piksellik boşluk farkı), hipotez kurmadan önce bunu söyle ve daha belirgin bir varyant öner.
   - **Mekanizma kapısından geçir (`methodology.md` → Fikir üretme merceği).** Her adayın "bu değişiklik davranışı neden değiştirsin" cevabı, sayfada gözlemlenebilen bir kullanıcı engeline dayanmalı; "daha dikkat çekici olur" veya "sosyal kanıt güveni artırır" gibi genel ifadeler cevap sayılmaz ve o aday önerilmez. Mekanizma Teori kısmına yazılır. İki istisna: kullanıcı bir testi açıkça istediyse reddetme, kur ama mekanizmanın zayıf olduğunu söyle ve yanına daha güçlü bir alternatif koy; ayrıca güçlü mekanizma ile `Kanıt: sezgi` birlikte bulunabilir, bu aday elenmez.
   - **Aynı mekanizmayı tekrar etme.** Aynı sayfa alanında aynı davranış mekanizmasına dayanan adayları ayrı senaryolar diye sunma; birleştir veya en güçlüsünü seç.
   - **Değişikliğin cevapladığı itirazı adlandır.** Kullanıcı sayfayı bırakıyorsa altında bir itiraz vardır: Güven ("neden buna inanayım"), Fiyat ("buna değer mi"), Uygunluk ("bu benim durumuma uyar mı"), Zamanlama ("neden şimdi") veya Efor ("bu ne kadar zor olacak"). Bu itirazı çıktıda senaryo başlık satırındaki etiketlere ekle (Kanıt etiketinin yanına: `İtiraz: Fiyat` gibi); Teori ayrıca yazılıyorsa orada da tek kelimeyle geçer. Kanıt varsa (destek talebi, iptal nedeni, kullanıcı yorumu) hangi itiraza denk geldiğini söyle; yoksa hangi itirazı hedeflediğini varsayım olarak işaretle.
4. Üç kutuyu metodolojiye göre doldur:
   - Test maddeleri `Etiket: soru?` biçiminde, en az biri cihaz/segment kırılımı.
   - KPI listesinin ilki birincil; en az bir guardrail "…memeli" kalıbında.
   - Yapılmaması gerekenler'de en az bir değişken-izolasyon maddesi.
5. Variant A (kontrol) ve Variant B (test) tanımını yaz: B'de tam olarak ne değişiyor, tek cümle.
   - Kullanıcı sayfasını paylaştıysa **A ekrandaki hâlin birebir kendisidir** (CLAUDE.md kural 15) — yeniden tasarlama, sadeleştirme, düzeltme. Yalnızca B'yi üret.
   - Hassas veri alanı (kimlik no, doğum tarihi, gelir, adres) söz konusuysa B'yi "alanı kaldır" diye kurma; kural 14'teki ara yöntemlerden birini seç ve hangisini neden seçtiğini yaz.
   - Form akışında çok adımlıya geçmeyi varsayılan çözüm sayma; önce tek sayfada yoğunlaştırmayı değerlendir (`methodology.md` → Değişken izolasyonu).
6. Trafik kullanıcı tarafından verilmişse kaba süre tahmini ver; verilmemişse süre/örneklem konusuna hiç girme — sorma da, "eksik" diye de yazma (CLAUDE.md kural 5).
7. **Doğrudan senaryoları üret.** Aday başlıklarını listeleyip "hangisini açayım" diye sorma. Sayfada birden fazla güçlü test adayı varsa en yüksek ICE'lı 2-5'ini doğrudan üret (üç kutu + Variant A/B, `abtest-card` ile kart olarak — kural 9), kurulum spesifikasyonu sohbette kalır; kalanları tek satırlık not olarak en sona ekle. 5'ten fazla güçlü aday varsa hepsini sormadan üretme: sayıyı söyle ve devam edilip edilmeyeceğini sor.

## Çıktı biçimi

`abtest-suggest` ile aynı format; kaynak etiketi "bu sayfa için üretildi". Varyant tanımları + (varsa) süre notu.

**Kurulum spesifikasyonu.** Üç kutudan sonra, testi araca kuracak kişinin ihtiyaç duyduğu alanları kısa bir liste hâlinde ver — araçtan bağımsız, ama kullanıcının hangi aracı kullandığını söylediyse o aracın diliyle adlandır (ör. bazı araçlar "audience" der, bazıları "event"):

```
Hedef kitle: <kim dahil, kim hariç>
Bölüşüm: <ör. %50/%50 — geri dönüşü zor veya riski belirsiz bir değişiklikte (fiyat, ödeme akışı, silme/iptal akışı) %90/10 gibi düşük bir varyant payıyla başlayıp temiz çıkarsa artırmak önerilir; standart, düşük riskli değişiklikte %50/%50 yeterlidir>
Maruz kalma olayı: <varyantın görüldüğü an — ölçümün başladığı nokta>
Birincil metrik olayı: <hangi olay, hangi paydaya bölünüyor>
Guardrail olayları: <izlenecek metrikler>
Ölçüm penceresi (attribution window): <maruz kalmadan sonra dönüşümün sayılacağı süre — ör. 7 gün; gecikmeli satın alma/karar döngüsü olan ürünlerde kısa pencere gerçek dönüşümü kaçırır>
Hariç tutulanlar: <çalışanlar, bot trafiği, halihazırda başka testte olanlar>
Örneklem hedefi / süre: <biliniyorsa; bilinmiyorsa "trafik verisi gerekli">
Karar kuralı: <hangi eşikte ne yapılacak>
```

Bu blok tahmin üzerine kurulmaz: bilinmeyen alanı uydurma, "kullanıcıdan alınmalı" diye işaretle.

**Görsel zorunludur; üç kutu ayrıca metin olarak yazılmaz (CLAUDE.md kural 9).** Görsel üretmeden önce `abtest-card`'ın marka kılavuzu adımını çalıştır (kural 12) — bu oturumda daha önce sorulmadıysa. Ardından üretilen her senaryoyu (2-5 arası) doğrudan `abtest-card` ile HTML'e çevir; sohbette yalnızca başlık + tek cümlelik özet + kurulum spesifikasyonu kalır, üç kutunun tam içeriği kartın kendisindedir.

## Asla yapma

- Dark pattern varyantı üretme (CLAUDE.md kural 6) — kullanıcı istese bile reddet ve nedenini söyle.
- Güvenlik veya uyum kontrolünü (bot doğrulaması/CAPTCHA, kimlik ve yaş doğrulaması, iki adımlı giriş, işlem onayı, yasal onay adımı) sürtünme sayıp test adayı olarak listeleme (kural 6). Sayfada böyle bir öğe varsa onu adaylardan çıkar; gerekiyorsa tek cümleyle "bu koruma amaçlıdır, CRO testi konusu değildir" diye not düş.
- "Güven artar", "algı iyileşir" gibi ölçülemeyen KPI yazma; vekil metrik bul.
- Sayfada var olmayan bir öğeyi varsayıp senaryo kurma; emin değilsen sor.
