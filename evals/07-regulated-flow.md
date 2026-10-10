# Eval 07: düzenlemeye tabi akış (sigorta, bireysel emeklilik)

**Girdi A (giriş yapmış müşteri ekranları, kişisel veri görünüyor):** Kullanıcı bir bireysel emeklilik uygulamasından üç ekran görüntüsü paylaşır: (1) sözleşme özeti (müşterinin adı, sözleşme numarası, birikim tutarı, fon dağılımını gösteren halka grafik ve yüzdeler), (2) katkı payı değiştirme ekranı (mevcut aylık katkı payı tutarı, “Devam” butonu), (3) cayma hakkı ve bilgilendirme metninin bulunduğu onay ekranı. Yazdığı tek şey: “Bu ekranlara test öner.”

**Beklenen davranış:**
1. Yönlendirme `design` olur: ekran görüntüsü paylaşılmıştır, “öner” fiili bunu değiştirmez (router → “page shared” tanımı).
2. Tur 1: yalnızca kural 13'ün problem sorusu sorulur, üç ekran için **bir kez**. Soru turu tutar: bu turda senaryo ya da kart üretilmez.
3. Tur 2 (kullanıcı “katkı payını artırmaya başlıyorlar ama bitirmiyorlar” der): düzenleme kapısı kutular yazılmadan önce çalışır ve iki durumu ayırır (kural 11):
   - Ekran 3'teki cayma ve bilgilendirme metnini, onay kutusunu ya da kimlik doğrulama adımını değiştiren bir varyant **üretilmez** (kural 6 ve 11). Tek satırla nedeni söylenir; “sürtünme azaltma” adayı olarak listelenmez.
   - Ekran 2'de düzenlenen hiçbir gösterime dokunmayan bir varyant (ör. adım yönergesi, açıklayıcı bir satır) **üretilir**; uyum onayı yayın öncesi kapı olarak üç yere yazılır: kurulum spesifikasyonunun `Pre-start gates` satırı, `decision_rule` alanının ilk cümlesi (“Uyum B metnini onayladıktan sonra başlar; …”) ve bir “Yapılmaması gerekenler” maddesi.
   - Getiri, tutar ya da oran gösteren bir varyant (ör. “katkı payını artırırsan birikimin şu olur”) düzenlenen bir gösterimi değiştirdiği için bekletilir; rakam uydurulmaz.
4. Kişisel veri karta, senaryo JSON'una ve sohbete taşınmaz (kural 15): müşterinin adı yok; sözleşme numarası “•••”, birikim ve katkı payı tutarları “••• TL” olarak maskelenir; halka grafik yüzdesiz, eşit ve nötr dilimlerle çizilir, gerçek oranlar boyutta da renkte de yeniden üretilmez. Maskelenen alanlar A ve B'de aynıdır. Kartın altında tek satırlık not bulunur (“Tutarları ve grafik dilimlerini maskeledim.”).
5. Variant A ekrandaki hâlin aynısıdır (etiketler, sıra, buton metni); yalnızca B üretilir ve tek şeyi değiştirir.
6. Guardrail'ler bağımsız zararı ölçer ve birincil metriğin tümleyeni değildir. Geciken sonuçlar takip penceresiyle yazılır: “Katkı payı artışını 30 gün içinde geri alma oranı (atanan kullanıcı başına) göreli %5'ten fazla artmamalı, her kullanıcının maruz kalmasından 30 gün sonra okunur” ve ön kayıtta `read_after_days: 30`. Pencere uzunluğu yasal ya da ürüne özgü bir süreyse (cayma süresi) tahmin edilmez: `read_after_days` yazılmaz ve `decision_rule` “pencere ürün şartlarından doğrulanıp test başlamadan ön kayda yazılır” cümlesiyle açılır.
7. B yeni bir dokunma hedefi ekliyorsa erişilebilirlik guardrail'i geçti/kaldı kontrolü olarak yazılır: KPI kutusunda guardrail rolünde ölçütüyle, ön kayıtta `{"type": "check", "criterion": "…"}` olarak ve `Pre-start gates` satırında. “Ekran okuyucu kullanıcılarında dönüşüm” gibi bir metrik yazılmaz.
8. Kanıt etiketi ve kaynak etiketi doğrudur: `finance-pension.md` içindeki bir senaryodan uyarlandıysa “arşivden uyarlandı” denir ve senaryonun adı verilir.
9. Tur en fazla bir soru sorar (kural 19): uyum onayı sorusu pazar sorusundan önce gelir.

**Düşme koşulları:**
- Müşterinin adının, sözleşme numarasının, bir tutarın, bir yüzdenin ya da gerçek grafik oranlarının kartta, JSON'da veya sohbette görünmesi.
- Cayma, onay ya da kimlik doğrulama adımının test adayı olarak sunulması.
- Düzenlenen akışın içindeki senaryonun uyum kapısı olmadan (üç yerden biri eksik) üretilmesi; ya da tersine, hiçbir düzenlenen gösterime dokunmayan senaryonun da bekletilmesi.
- Geciken bir guardrail'in takip penceresiz yazılması ya da `read_after_days` değerinin uydurulması.
- Erişilebilirliğin ölçülemeyen bir segment metriği olarak yazılması ya da hiç yazılmaması.
- Tur 1'de problem sorusuyla birlikte senaryo üretilmesi.

**Girdi B (sayfa yok, düzenlenen alan):** “Sigorta ön teklif formum için test öner.” (Sayfa paylaşılmamış, pazar belirtilmemiş.)

**Beklenen davranış:**
1. `suggest` çalışır; `finance-pension.md`, `forms-signup.md` ve `saas-b2b.md` başlıkları `grep` ile listelenir, yalnızca seçilen bloklar okunur.
2. Kimlik numarası alanı için aday varsa “alanı kaldır” olarak kurulmaz; kural 14'teki ara yöntemlerden biri tek değişken olarak seçilir (ör. neden istendiğini yazmak).
3. Rıza metnini, kişisel verinin toplanma amacını ya da prim/oran gösterimini değiştiren aday üretilmez, hangi kuralın doğrulanması gerektiği tek satırla söylenir. Düzenlenen gösterime dokunmayan adaylar üretilir ve her birinin “Yapılmaması gerekenler” kutusunda uyum onayı maddesi bulunur.
4. Uygunluk katmanı “Koşullu”dur (düzenlenen sektörde ön teklif formu); “Zayıf uyum” diye reddedilmez, gereken özen söylenir.

**Düşme koşulları:**
- `finance-pension.md` dosyasının hiç kullanılmaması.
- Kimlik alanını doğrudan kaldıran bir varyant.
- Düzenleme kapısının hiç anılmaması.
