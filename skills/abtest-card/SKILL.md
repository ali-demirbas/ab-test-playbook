---
name: abtest-card
description: Render an A/B test scenario as a single-file HTML card in the archive's visual style (Variant A/B mockup pair + three colored boxes). Use when the user says "kart yap", "görselleştir", "slayt formatına çevir", "make a card for this test".
metadata:
  version: 0.1.0
  category: render
---

# abtest-card — Senaryo Kartı Üretimi

Görsel dilin tanımı `${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md`'dedir — üretmeden önce oku. Şablon: `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html`.

Bu skill, `abtest-design` metin çıktısı verildikten hemen sonra otomatik çalışır (CLAUDE.md kural 9) — kullanıcının ayrıca istemesi gerekmez. `abtest-suggest` çoklu öneri listesinde ise **liste aşamasında kart üretilmez** (kural 9'un tek istisnası): kullanıcı bir senaryo seçtikten sonra o senaryonun kartı üretilir. Kullanıcı doğrudan "kart yap" derse de aynı akış işler.

## Akış

0. **Marka kaynağı (oturumda bir kez).**
   - **Kullanıcı ekran görüntüsü/sayfa paylaştıysa sorma:** marka rengini, logo metnini ve buton stilini doğrudan görüntüden çıkar ve kullan. Kartın altına tek satır not düş: "Renkleri ekran görüntüsünden aldım; resmi marka kılavuzunu paylaşırsan güncellerim." Akışı durdurup cevap bekleme.
   - **Görsel kaynak yoksa sor:** "Kartı senin marka kılavuzuna (logo, renk paleti) göre mi hazırlayayım, yoksa nötr bir stil mi kullanayım?" Cevap gelene kadar bu adımda bekle. Kullanıcı bir URL verdiyse bu da sayfa paylaşımıdır (kural 12a): tarayıcı aracı varsa siteye gidip renkleri sormadan oradan çıkar; araç yoksa yukarıdaki soruya düş.
   - **Kılavuz verilirse:** Renkleri (birincil/ikincil, CTA rengi), logo/marka adını ve varsa tipografi tercihini çıkar; `mockup-style.md`'deki nötr paletin yerine bunları kullan. Logoyu gerçek dosya olarak gömmek yerine, kılavuzdaki marka adını/kısaltmasını metin olarak header'a yaz (dış görsel bağlantısı yok kuralı bozulmasın).
   - **Verilmezse/"hayır" derse:** `mockup-style.md`'deki nötr palet (teal/amber/navy) kullanılır.
   - Karar oturum boyunca hatırlanır (CLAUDE.md kural 12), sonraki kartlarda tekrar sorulmaz — kullanıcı değiştirmek istemedikçe.
1. Karta basılacak senaryoyu al: bu oturumda `abtest-suggest`/`abtest-design` çıktısı, ya da kullanıcının verdiği metin. Üç kutu eksikse önce tamamlat (`abtest-design`'a yönlendir). Metindeki içeriği birebir kullan; karta basarken maddeleri yeniden yazma veya kısaltma.
2. `templates/scenario-card.html` şablonunu oku ve doldur:
   - Başlık, açıklama, üç kutunun maddeleri (etiketler bold).
   - Mockup bölgesi: senaryo mobil bağlamlıysa `.phone` iskeletini (durum çubuğu + alt nav) kullan; masaüstü/web bağlamlıysa şablondaki `.browser`/`.browser-bar`/`.browser-url`/`.browser-screen` iskeletini kullan (üç nokta + adres çubuğu + beyaz gövde, statusbar/bottomnav yok). Marka kılavuzu verildiyse header/CTA rengi ve marka adı ona göre; verilmediyse nötr palet.
   - **İçerik tam gerçekçi yazılır** (`mockup-style.md` → Gerçekçilik seviyesi): metin, fiyat, etiket ve düzen gerçek; "Başlık", "Lorem ipsum" gibi doldurma yok. Şablondaki `.r-*` bileşenlerini kullan (`.r-item` ürün satırı, `.r-field` form alanı, `.r-line` fiyat satırı, `.r-cta`, `.r-badge`, `.r-stars`) — markup'ı sıfırdan uydurma. Gri `.ph` blokları yalnızca fotoğrafın yerini tutar (ürün görseli, avatar), metnin yerine kullanılmaz.
   - **Kullanıcı bir sayfa paylaştıysa mockup O SAYFANIN yeniden çizimidir, uydurulmuş bir sayfa değil.** Ürün adı, fiyat, buton metni, alan etiketleri, bölüm sırası — ekranda ne varsa o yazılır. Variant A ekrandaki hâlin birebir kendisidir (kural 15): yeniden tasarlama, sadeleştirme, eksiğini tamamlama. Kendi kafandan örnek bir sayfa kurup testi ona oturtma. Ekran görüntüsünde okunamayan bir ayrıntıyı uydurma: ya mockup'a koyma ya da sor. Paylaşılmış sayfa yoksa (arşiv senaryosu) temsili örnek kurulur ama gerçek müşteri sayfasıymış gibi sunulmaz.
   - Test edilen fark kırmızı çerçeveyle vurgulanır ve **çerçeveye ne değiştiğini söyleyen kısa bir etiket konur**: `<div class="hl" data-note="kupon alanı katlandı">`. Etiket iki üç kelimeyi geçmez. Kaldırma testinde çerçeve A'daki öğeye çizilir.
   - İki varyantta test edilen öğe dışında HER ŞEY aynı olmalı (mockup-style.md kuralı).
3. Tek dosyalık, bağımsız HTML üret (inline CSS, dış kaynak yok). Kullanıcının çalışma dizinine `abtest-card-<slug>.html` olarak yaz.
4. Kullanıcıya doğrudan gönder (dosya teslimi). Görüntüleme imkânın varsa (tarayıcı aracı) açıp doğrula: metin taşması, Türkçe karakter, kutu hizası, marka renklerinin doğru uygulandığı.

## Asla yapma

- Üç kutusu eksik senaryoyu karta basma.
- Dark pattern içeren senaryoyu karta basma — kullanıcı doğrudan "kart yap" dese de CLAUDE.md kural 6 geçerlidir; reddet ve nedenini söyle.
- Karta `<script>` veya etkileşimli kod koyma; kart salt statik HTML/CSS'tir.
- **Metni şablona koymadan önce HTML olarak kaçır.** Senaryo başlığı, açıklama ve üç kutunun maddeleri `{{TITLE}}`, `{{DESC}}`, `{{TEST_ITEMS}}` gibi yer tutuculara doğrudan gömülür; içinde `<`, `>` veya `&` geçen bir metin (ör. "CTA < 3 kelime olmalı mı?", "kargo & iade") kartı bozar ya da beklenmeyen etiket üretir. Bu karakterleri sırasıyla `&lt;`, `&gt;`, `&amp;` yaz. Kaçırma işlemi, madde metnindeki kasıtlı `<b>` vurgusundan **sonra** değil önce yapılır: önce içerik kaçırılır, sonra biçimlendirme etiketleri eklenir. Kullanıcının yapıştırdığı bir metni doğrudan karta aktarıyorsan bu kural özellikle geçerlidir.
- Mockup'ta iki varyant arasına ikinci bir fark koyma.
- Kaldırılan bir öğenin yerine "gösterilmez / kaldırıldı" yazan yer tutucu koyma (`mockup-style.md`); B'de o bloğu hiç yazma, altındaki içerik doğal olarak yukarı kaysın. Kaymayı görünür kılmak için mockup'ın **altına** tek satır not düş: `<div class="shift-note">…</div>` — bu not ekranın içine girmez.
- Dış font/CDN bağlantısı ekleme; kart çevrimdışı açılabilmeli (sistem fontu: Inter yoksa -apple-system/Segoe UI düşüşü).
- Kartı kullanıcının dilinden farklı bir dilde üretme (kural 7); tırnaklar kıvrık, Türkçe kartta Türkçe karakterler tam.
- Ekran görüntüsü varken marka kılavuzu sorusu sorup akışı durdurma; renkleri görüntüden al. Hiçbir görsel kaynak yokken de nötr paleti sessizce varsayma — o durumda sor.
- Marka logosunu dış bir URL'den çekmeye çalışma; sadece kullanıcının verdiği bilgiyi (renk kodu, marka adı) kullan.
