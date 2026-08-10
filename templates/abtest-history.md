# A/B Test Geçmişi

Bu dosya projenin test hafızasıdır. `ab-test-playbook` skill'leri öneri üretmeden, yeni senaryo tasarlamadan ve bir test planını denetlemeden önce burayı okur; aynı değişkenin daha önce test edilip edilmediğini, ne sonuç verdiğini bilir.

**Nereye konur:** Projenin kök dizininde `.abtest-history.md` adıyla. (Bu dosya o şablonun kendisidir — kopyalayıp adını değiştirin.)

**Kim doldurur:** Bir test bittiğinde `/abtest results` çalıştırdığınızda, sonucu yorumladıktan sonra kaydın satır hâlini size verir; onu buraya yapıştırırsınız. Elle de yazabilirsiniz.

**Gizlilik:** Bu dosya sizin iş verinizi içerir. Public bir depoda tutuyorsanız `.gitignore`'a ekleyin.

## Kayıtlar

Yeni kayıt en üste eklenir (en yeni önce).

> **Aşağıdaki dört satır örnektir, gerçek veri değildir.** Biçimi göstermek için konmuştur; kendi ilk kaydınızı eklerken bu satırları silin. Silmezseniz `abtest-suggest` ve `abtest-design` bunları sizin geçmiş testleriniz sanır ve önerileri buna göre süzer.

| Tarih | Sayfa/Akış | Test edilen tek değişken | Sonuç | Birincil metrik etkisi | Guardrail | Genellenebilir örüntü | Not |
|---|---|---|---|---|---|---|---|
| 2026-07 | Ürün detay | CTA buton rengi (turuncu → yeşil) | fark yok | CR %3,2 → %3,3 (anlamsız) | temiz | — | Örneklem hedefe ulaştı; değişiklik davranışı etkilemedi |
| 2026-05 | Sepet | Ücretsiz kargo ilerleme çubuğu (yok → var) | kazandı | AOV +%7,1 | marj sabit | İlerleme göstergesi (ne kadar kaldığını görmek) harcama davranışını güçlendiriyor — teslimat/puan/ödül eşiklerinde de denenebilir | 3 hafta koştu, %100 yayıldı |
| 2026-03 | Ürün detay | Taksit rozeti konumu (kart içi → görsel üstü) | kaybetti | CR −%2,4 | temiz | — | Rozet fiyat alanını gölgeledi |
| 2026-02 | Ödeme | Misafir ödeme butonu görünürlüğü | geçersiz | — | — | — | Ölçüm hatası: iki varyantta farklı event tetiklenmiş |

## Sonuç değerleri

Yalnızca şunlardan biri yazılır — yorum "Not" sütununa gider:

- **kazandı** — birincil metrikte anlamlı iyileşme, guardrail temiz, süre kuralı sağlandı
- **kaybetti** — birincil metrikte anlamlı kötüleşme
- **fark yok** — örneklem hedefine ulaşıldı ama anlamlı fark çıkmadı
- **yetersiz** — örneklem/süre dolmadan kapatıldı; sonuç bilgi taşımaz, tekrar denenebilir
- **durduruldu** — guardrail bozulduğu için erken kapatıldı
- **geçersiz** — ölçüm/kurulum hatası (SRM, yanlış event, kirlenmiş trafik); sonuç okunamaz

## Genellenebilir örüntü sütunu

Yalnızca **kazandı** sonucunda doldurulur. Buraya yazılan şey testin kendisi değil, testin ardındaki soyut fikirdir — "kargo çubuğu kazandı" değil, "ilerleme göstergesi harcama davranışını güçlendiriyor" gibi. Amaç: bir sayfada işe yarayan bir mekanizmanın başka sayfalarda da denenebilir olduğunu görmek. `abtest-suggest` bu sütunu okur ve benzer bir mekanizma başka bir sayfaya uyuyorsa "burada da denenebilir, çünkü [X sayfasında] aynı mekanizma kazanmıştı" diye önerebilir — ama bunu otomatik varsaymaz, hâlâ ayrı bir test olarak kurar.

## Neden "kaybetti" kaydı fikri öldürmez

Skill'ler bu dosyayı okurken geçmiş sonucu **bilgi** olarak kullanır, otomatik veto olarak değil. Aynı fikir şu durumlarda yeniden test edilebilir ve bunun gerekçesi çıktıda yazılır:

- Sayfanın veya akışın kendisi o testten sonra değişti
- Sonuç "yetersiz" veya "geçersiz" idi — yani aslında hiç ölçülmedi
- Test farklı bir segmentte/cihazda/pazarda koşulmuştu
- Aradan uzun süre geçti ve kullanıcı davranışı ya da rekabet değişti

Aynı değişken aynı sayfada art arda "fark yok" veriyorsa, skill daha küçük bir varyasyon değil, daha yapısal bir değişiklik önerir (yerel tepe riski — bkz. `knowledge/methodology.md`).
