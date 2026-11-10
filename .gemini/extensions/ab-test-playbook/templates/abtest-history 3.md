# A/B Test Geçmişi

Bu dosya projenin test hafızasıdır. `ab-test-playbook` skill’leri öneri üretmeden, yeni senaryo tasarlamadan ve bir test planını denetlemeden önce burayı okur; aynı değişkenin daha önce test edilip edilmediğini ve test aracınızın ne sonuç bildirdiğini görür, böylece aynı testi yeniden önermez.

**Nereye konur:** Projenin kök dizininde `.abtest-history.md` adıyla. (Bu dosya o şablonun kendisidir; kopyalayıp adını değiştirin.)

**Kim doldurur:** Siz. Bir test bittiğinde sonucu kendi test aracınızın raporundan alıp buraya bir satır olarak yazarsınız. Playbook bu dosyayı yalnızca okur: satır eklemez, değiştirmez, sonucu kendisi hesaplamaz ve yeniden yorumlamaz.

**Gizlilik:** Bu dosya sizin iş verinizi içerir. Public bir depoda tutuyorsanız `.gitignore`’a ekleyin.

## Kayıtlar

Yeni kayıt en üste eklenir (en yeni önce).

> **Aşağıdaki dört satır örnektir, gerçek veri değildir.** Biçimi göstermek için konmuştur ve her biri “(örnek)” diye işaretlidir; kendi ilk kaydınızı eklerken bu satırları silin. Silmezseniz `ab-test-suggest`, `ab-test-design` ve `ab-test-audit` bunları sizin geçmiş testleriniz sanır ve önerileri buna göre süzer.

| Tarih | Sayfa/Akış | Test edilen tek değişken | Sonuç | Genellenebilir örüntü | Not |
|---|---|---|---|---|---|
| 2026-07 (örnek) | Ürün detay | CTA buton rengi (turuncu → yeşil) | fark yok | | Test aracı iki varyant arasında fark bildirmedi |
| 2026-05 (örnek) | Sepet | Ücretsiz kargo ilerleme çubuğu (yok → var) | kazandı | İlerleme göstergesi (ne kadar kaldığını görmek) harcama davranışını güçlendiriyor; teslimat, puan ve ödül eşiklerinde de denenebilir | Varyant tüm kullanıcılara açıldı |
| 2026-03 (örnek) | Ürün detay | Taksit rozeti konumu (kart içi → görsel üstü) | kaybetti | | Rozet fiyat alanını gölgeledi |
| 2026-02 (örnek) | Ödeme | Misafir ödeme butonu görünürlüğü | geçersiz | | Ölçüm hatası: iki varyantta farklı event tetiklenmiş |

## Sonuç değerleri

Yalnızca şunlardan biri yazılır; açıklama “Not” sütununa gider. Değer, kendi test aracınızın bildirdiği sonuçtur; playbook onu hesaplamaz ve yeniden yorumlamaz.

- **kazandı** (won): Test aracınız varyantı kazanan olarak bildirdi.
- **kaybetti** (lost): Test aracınız varyantın kontrolden kötü sonuç verdiğini bildirdi.
- **fark yok** (no difference): Test aracınız iki varyant arasında fark bildirmedi.
- **belirsiz** (inconclusive): Test bir sonuca varmadan kapandı; tekrar denenebilir.
- **geçersiz** (invalid): Ölçüm ya da kurulum hatası (yanlış event, kirlenmiş trafik, bozuk atama); sonuç okunamaz, tekrar denenebilir.

Bir dosyada tek dil kullanılır: Türkçe değerlerle başlayan dosya Türkçe, İngilizce değerlerle başlayan dosya İngilizce sürer.

## Genellenebilir örüntü sütunu

Yalnızca **kazandı** sonucunda doldurulur. Buraya yazılan şey testin kendisi değil, testin ardındaki soyut fikirdir; “kargo çubuğu kazandı” değil, “ilerleme göstergesi harcama davranışını güçlendiriyor” gibi. Amaç, bir sayfada işe yarayan bir mekanizmanın başka sayfalarda da denenebilir olduğunu görmek. `ab-test-suggest` bu sütunu okur ve benzer bir mekanizma başka bir sayfaya uyuyorsa “burada da denenebilir, çünkü [X sayfasında] aynı mekanizma kazanmıştı” diye önerebilir; ama bunu otomatik varsaymaz, hâlâ ayrı bir test olarak kurar.

## Neden “kaybetti” kaydı fikri öldürmez

Skill’ler bu dosyayı okurken geçmiş sonucu **bilgi** olarak kullanır, otomatik veto olarak değil. Aynı fikir şu durumlarda yeniden önerilebilir ve gerekçesi çıktıda yazılır:

- Sayfanın veya akışın kendisi o testten sonra değişti
- Test farklı bir segmentte, cihazda veya pazarda koşulmuştu
- Sonuç “belirsiz” veya “geçersiz” idi; yani aslında hiç okunamadı

Aynı değişken aynı sayfada art arda “fark yok” veriyorsa, skill daha küçük bir varyasyon değil, daha yapısal bir değişiklik önerir (yerel tepe riski; bkz. `knowledge/methodology.md`).
