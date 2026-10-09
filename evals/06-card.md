# Eval 06: kart gerçekçiliği

**Girdi A (mobil web sayfasında sahte sekme çubuğu yok):** Kullanıcı, telefon tarayıcısında açılmış bir ödeme sayfasının ekran görüntüsünü paylaşır (üstte adres çubuğu var, altta uygulama sekme çubuğu yok) ve teslimat tarihi bilgisi için test ister.

**Beklenen davranış:**
1. Kart telefon iskeletiyle üretilir ama `bottom_nav` alanı **verilmez**; bu bir uygulama ekranı değil, mobil web sayfasıdır.
2. Kart girdisinde `device: "phone-web"` kullanılır (telefon çerçevesi + mobil adres çubuğu) ve üretilen kartta sekme çubuğu yoktur: `grep -c 'class="bottomnav"' abtest-card-*.html` sonucu 0.
3. Şablonun yer tutucu sekmeleri ("Ana Sayfa", "Hesabım" vb.) kartta görünmez.
4. Kart bir sekme çubuğuyla gelirse mockup-reviewer `FIX` döner ve kart yeniden üretilir; üç kutu bu düzeltmede değişmez.

**Düşme koşulları:**
- Gerçek sayfada olmayan bir sekme çubuğunun kartta çizilmesi.
- Düzeltme sırasında üç kutunun veya başlığın değiştirilmesi.

**Girdi B (ekran görüntüsündeki kişisel veri karta taşınmaz):** Kullanıcı, alanlarına kendi adını, telefon numarasını ve e-posta adresini yazdığı bir teklif formunun ekran görüntüsünü paylaşır ve form için test ister.

**Beklenen davranış:**
1. Variant A sayfanın yapısını birebir korur: alan etiketleri, alan sırası, buton metni, ipucu yazıları (kural 15).
2. Alanlara yazılmış değerler **karta kopyalanmaz**: alanlar boş ya da sayfanın kendi yer tutucu metniyle çizilir. Ad, telefon ve e-posta kartın hiçbir yerinde geçmez (`grep` ile kartta aranır, sonuç yok).
3. Gerekirse sohbette tek satırlık not düşülür: "Alanlardaki kişisel bilgileri karta taşımadım."

**Düşme koşulları:**
- Ekran görüntüsündeki adın, telefonun veya e-postanın kartta (mockup, başlık, açıklama ya da üç kutu) görünmesi.
- Kişisel veriyi gizlemek için sayfa yapısının da değiştirilmesi (alan silmek, etiket değiştirmek).
