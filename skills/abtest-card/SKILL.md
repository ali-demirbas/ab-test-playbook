---
name: abtest-card
description: Render an A/B test scenario as a single-file HTML card in the archive's visual style — a Variant A/B mockup pair with the tested element boxed, plus the three coloured boxes. Use when the user says "make a card for this test", "turn this into a card", "visualise this test", "render this scenario", "make a slide out of this", "show me the two variants side by side", "kart yap", "görselleştir", "slayt formatına çevir", "bunu karta bas". Runs automatically for every scenario produced by abtest-suggest and abtest-design (CLAUDE.md rule 9), so it rarely needs to be invoked directly. Output is self-contained HTML with no external assets, built deterministically by scripts/build_card.py.
metadata:
  version: 0.1.0
  category: render
  updated: 2026-08-13
---

# abtest-card — Senaryo Kartı Üretimi

> **Türkçe/English:** Çıktı dili kullanıcının yazdığı dildir (CLAUDE.md kural 7). / Output always matches the language you write in.

Görsel dilin tanımı `${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md`'dedir — üretmeden önce oku. Şablon: `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html`.

Bu skill, `abtest-suggest` veya `abtest-design`'ın bir turda ürettiği HER senaryo için otomatik çalışır (CLAUDE.md kural 9) — kullanıcının ayrıca istemesi gerekmez. Üç kutunun ("Test edilmesi gerekenler" / "Takip edilecek ana KPI'lar" / "Yapılmaması gerekenler") tam içeriği yalnızca bu kartta bulunur; aynı içerik sohbete ayrıca metin olarak yazılmaz — sohbette yalnızca başlık, kaynak etiketi ve tek cümlelik özet kalır. Bir turda 2-5 senaryo doğrudan kart olur; 5'ten fazla güçlü aday varsa hepsi sormadan üretilmez (kural 9). Kullanıcı doğrudan "kart yap" derse de aynı akış işler.

## Akış

0. **Marka kaynağı (oturumda bir kez).**
   - **Kullanıcı ekran görüntüsü/sayfa paylaştıysa sorma:** marka rengini, logo metnini ve buton stilini doğrudan görüntüden çıkar ve kullan. Kartın altına tek satır not düş: "Renkleri ekran görüntüsünden aldım; resmi marka kılavuzunu paylaşırsan güncellerim." Akışı durdurup cevap bekleme.
   - **Görsel kaynak yoksa sor:** "Kartı senin marka kılavuzuna (logo, renk paleti) göre mi hazırlayayım, yoksa nötr bir stil mi kullanayım?" Cevap gelene kadar bu adımda bekle. Kullanıcı bir URL verdiyse bu da sayfa paylaşımıdır (kural 12a): tarayıcı aracı varsa siteye gidip renkleri sormadan oradan çıkar; araç yoksa yukarıdaki soruya düş.
   - **Kılavuz verilirse:** Renkleri (birincil/ikincil, CTA rengi), logo/marka adını ve varsa tipografi tercihini çıkar; `mockup-style.md`'deki nötr paletin yerine bunları kullan. Logoyu gerçek dosya olarak gömmek yerine, kılavuzdaki marka adını/kısaltmasını metin olarak header'a yaz (dış görsel bağlantısı yok kuralı bozulmasın).
   - **Verilmezse/"hayır" derse:** `mockup-style.md`'deki nötr palet (teal/amber/navy) kullanılır.
   - Karar oturum boyunca hatırlanır (CLAUDE.md kural 12), sonraki kartlarda tekrar sorulmaz — kullanıcı değiştirmek istemedikçe.
1. Karta basılacak senaryoyu al: bu oturumda `abtest-suggest`/`abtest-design` çıktısı, ya da kullanıcının verdiği metin. Üç kutu eksikse önce tamamlat (`abtest-design`'a yönlendir). Metindeki içeriği birebir kullan; karta basarken maddeleri yeniden yazma veya kısaltma.
2. Senaryoyu bir JSON dosyasına yaz; şablonu elle doldurma (CLAUDE.md kural 9 → Mekanizma). Alanlar:
   - `title`, `desc` ve üç kutunun maddeleri (`test_items`, `kpi_items`, `dont_items`): **düz metin ver, kaçırma yapma** — script `html.escape` uygular. Bold etiket isteyen madde `{"label": "Birincil KPI", "text": "sepet → ödeme"}` biçiminde verilir; elle `<b>` yazma, sıra bozulur.
   - `device`: mobil bağlamda `"phone"`, masaüstü/web bağlamda `"web"` (+ adres çubuğu için `url`). Browser iskeletine geçişi script yapar; yorumdaki iskeleti elle kopyalama.
   - `variant_a` / `variant_b`: mockup markup'ı, **ham HTML** olarak. Aşağıdaki kurallar bu iki alan içindir.
   - Mockup bölgesi: senaryo mobil bağlamlıysa `.phone` iskeletini (durum çubuğu + alt nav) kullan; masaüstü/web bağlamlıysa şablondaki `.browser`/`.browser-bar`/`.browser-url`/`.browser-screen` iskeletini kullan (üç nokta + adres çubuğu + beyaz gövde, statusbar/bottomnav yok). Marka kılavuzu verildiyse header/CTA rengi ve marka adı ona göre; verilmediyse nötr palet.
   - **İçerik tam gerçekçi yazılır** (`mockup-style.md` → Gerçekçilik seviyesi): metin, fiyat, etiket ve düzen gerçek; "Başlık", "Lorem ipsum" gibi doldurma yok. Şablondaki `.r-*` bileşenlerini kullan (`.r-item` ürün satırı, `.r-field` form alanı, `.r-line` fiyat satırı, `.r-cta`, `.r-badge`, `.r-stars`) — markup'ı sıfırdan uydurma. Gri `.ph` blokları yalnızca fotoğrafın yerini tutar (ürün görseli, avatar), metnin yerine kullanılmaz.
   - **Kullanıcı bir sayfa paylaştıysa mockup O SAYFANIN yeniden çizimidir, uydurulmuş bir sayfa değil.** Ürün adı, fiyat, buton metni, alan etiketleri, bölüm sırası — ekranda ne varsa o yazılır. Variant A ekrandaki hâlin birebir kendisidir (kural 15): yeniden tasarlama, sadeleştirme, eksiğini tamamlama. Kendi kafandan örnek bir sayfa kurup testi ona oturtma. Ekran görüntüsünde okunamayan bir ayrıntıyı uydurma: ya mockup'a koyma ya da sor. Paylaşılmış sayfa yoksa (arşiv senaryosu) temsili örnek kurulur ama gerçek müşteri sayfasıymış gibi sunulmaz.
   - Test edilen fark kırmızı çerçeveyle vurgulanır ve **çerçeveye ne değiştiğini söyleyen kısa bir etiket konur**: `<div class="hl" data-note="kupon alanı katlandı">`. Etiket iki üç kelimeyi geçmez. Kaldırma testinde çerçeve A'daki öğeye çizilir.
   - İki varyantta test edilen öğe dışında HER ŞEY aynı olmalı (mockup-style.md kuralı).
3. Kartı üret:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py \
     --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html \
     --scenario senaryo.json \
     --out abtest-card-<slug>.html
   ```

   Script tek dosyalık bağımsız HTML üretir (inline CSS, dış kaynak yok) ve yazdıktan sonra sabit iskeletin sürüklenmediğini doğrular. Hata verirse dosya yazılmaz: hatayı düzelt, kartı elle üretmeye kaçma. Çıktı kullanıcının çalışma dizinine yazılır.
4. **Denetle (CLAUDE.md kural 17).** Kart üretildikten sonra `agents/mockup-reviewer`'ı çalıştır: iki mockup arasında test edilen öğe dışında ikinci bir fark olup olmadığını arar. `FIX` dönerse düzelt ve kartı yeniden üret. Denetim raporunu sohbete yazma; yalnızca kullanıcının bilmesi gereken bir kısıt varsa tek cümleyle söyle.
5. Kullanıcıya doğrudan gönder (dosya teslimi). Görüntüleme imkânın varsa (tarayıcı aracı) açıp doğrula: metin taşması, Türkçe karakter, kutu hizası, marka renklerinin doğru uygulandığı.

## Asla yapma

- Üç kutusu eksik senaryoyu karta basma.
- Dark pattern içeren senaryoyu karta basma — kullanıcı doğrudan "kart yap" dese de CLAUDE.md kural 6 geçerlidir; reddet ve nedenini söyle.
- Karta `<script>` veya etkileşimli kod koyma; kart salt statik HTML/CSS'tir.
- **Metin alanlarını elle kaçırma, kaçırılmış metin de verme.** `title`, `desc` ve üç kutunun maddeleri script tarafından kaçırılır; JSON'a `&lt;` yazarsan kartta `&amp;lt;` görünür. Düz metin ver. (Kaçırmanın neden koda alındığı: "CTA < 3 kelime olmalı mı?" veya "kargo & iade" gibi bir metin elle gömüldüğünde kartı sessizce bozar, ve bold etiket kaçırmadan önce uygulanırsa etiket içeriği tag olarak sızar. Bu iki hata da tek tek hatırlanmaya bırakılamaz.)
- **`variant_a`/`variant_b` markup'ında kullanıcı metnini ham gömme.** Bu iki alan ham HTML olarak geçer — mockup'a ürün adı, buton metni veya kullanıcının paylaştığı bir metin yazarken `<`, `>`, `&` karakterlerini sen kaçır. Kaçırma yalnızca metin alanlarında otomatiktir.
- Mockup'ta iki varyant arasına ikinci bir fark koyma.
- Kaldırılan bir öğenin yerine "gösterilmez / kaldırıldı" yazan yer tutucu koyma (`mockup-style.md`); B'de o bloğu hiç yazma, altındaki içerik doğal olarak yukarı kaysın. Kaymayı görünür kılmak için mockup'ın **altına** tek satır not düş: `<div class="shift-note">…</div>` — bu not ekranın içine girmez.
- Dış font/CDN bağlantısı ekleme; kart çevrimdışı açılabilmeli (sistem fontu: Inter yoksa -apple-system/Segoe UI düşüşü).
- Kartı kullanıcının dilinden farklı bir dilde üretme (kural 7); tırnaklar kıvrık, Türkçe kartta Türkçe karakterler tam.
- Ekran görüntüsü varken marka kılavuzu sorusu sorup akışı durdurma; renkleri görüntüden al. Hiçbir görsel kaynak yokken de nötr paleti sessizce varsayma — o durumda sor.
- Marka logosunu dış bir URL'den çekmeye çalışma; sadece kullanıcının verdiği bilgiyi (renk kodu, marka adı) kullan.
