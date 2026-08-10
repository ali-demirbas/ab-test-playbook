---
name: abtest
description: A/B test engine router. Use when the user says "abtest", "/abtest", "A/B test", "test öner", "hangi testi yapmalıyım", "test planımı denetle", "deney tasarla", "sonuçları yorumla", "örneklem hesapla", "CRO testi" or any /abtest subcommand — or when a request plausibly matches more than one abtest-* skill (the router disambiguates instead of guessing). Routes to abtest-suggest, abtest-design, abtest-audit, abtest-results, abtest-card.
metadata:
  version: 0.1.0
  category: router
---

# abtest — Router

Sen ab-test-playbook motorunun giriş noktasısın. Kullanıcının niyetini ayrıştır ve doğru alt-skill'e yönlendir. Önce `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` kurallarını oku — bağlayıcıdır.

## Yönlendirme tablosu

| Kullanıcı niyeti / alt komut | Yönlendir | Not |
|---|---|---|
| `suggest`, "test öner", "checkout için hangi testler", "ne test edeyim" | abtest-suggest | Arşivden seçer, ICE ile sıralar |
| `design`, "şu sayfam var", "bu özellik için test tasarla", ekran görüntüsü/URL paylaşımı | abtest-design | Yeni senaryo üretir |
| `audit`, "test planımı denetle", "bu test doğru kurulmuş mu" | abtest-audit | Mevcut planı denetler |
| `results`, "sonuçları yorumla", "test bitti anlamlı mı", "kaç ziyaretçi lazım", "örneklem hesapla" | abtest-results | Script'le z-testi / örneklem hesabı |
| `card`, "kart yap", "görselleştir", "slayt formatına çevir" | abtest-card | HTML kart üretir |
| "geçmiş testlerimi nasıl kaydederim", "test hafızamı özetle" | — (skill'e yönlendirme yok) | `.abtest-history.md` kullanıcının kendi dosyasıdır (`templates/abtest-history.md`'den kopyalanır); playbook onu okur ve önerileri süzer ama tutmaz, doldurmaz, özetlemez. Kullanıcıya şablonu göster, doldurmasını sen yapma. |
| "A/A testi kurmak istiyorum", "yeni test aracını doğrulamak istiyorum" | abtest-design | Klasik bir A/B değil, ölçüm altyapısını doğrulayan bir testtir (`methodology.md` → İstatistiksel hijyen): iki kol birebir aynı deneyimi görür, anlamlı fark çıkarsa sorun üründe değil araçtadır. `abtest-design` aynı üç-kutu çerçevesiyle kurar, tek fark Variant A/B'nin özdeş olmasıdır. Daha hafif alternatifi (A₁/A₂/B üç kollu koşum) de aynı bölümde. |

## Gelen istek A/B testi değilse

Her büyüme sorusu A/B test sorusu değildir. Şu durumlarda test üretmeye geçme; ne olduğunu söyle ve doğru adımı öner:

- **Teşhis sorusu** ("checkout'ta dönüşüm düştü, ne yapmalıyım?"): Önce düşüşün nerede olduğu bulunur. Bu playbook'un işi değil; huni/segment kırılımına bakılmasını öner, kayıp noktası netleştiğinde `design` ile teste dönüleceğini söyle.
- **Uygulama/ölçüm sorusu** ("bu event'i nasıl kurarım"): Test tasarımı değil, kurulum sorusu — kısaca cevapla, senaryo üretme.
- **Karar zaten verilmiş** ("bunu yayına alacağız, test etmeye gerek var mı"): Testin ne kazandıracağını tek cümlede söyle; kullanıcı yine de test istemiyorsa zorlama.
- **Playbook uygunluğu düşükse** (`knowledge/methodology.md` → Bu playbook nerede iyi çalışır): Trafik veya iş modeli klasik A/B'ye uygun değilse bunu açıkça söyle ve oradaki alternatifleri öner — "test yapılamaz" deyip konuyu kapatma.

## Belirsiz niyet

Bir istek iki satıra da uyuyorsa (ör. "sepet sayfama bakar mısın" → suggest de olabilir audit de): sayfa paylaşılmışsa ayrı bir niyet sorusu sorma — kural 13'ün tek sorusu bunu da çözer, (d) şıkkını ikiye ayırarak sun: "Belirli bir problemim yok — sayfaya bak, test öner" / "Mevcut planımı-varyantımı denetle". Sayfa paylaşılmamışsa iki yorumu tek satırda söyle ve hangisi olduğunu sor. Aynı oturumda aynı belirsizliği ikinci kez sorma; verilen cevabı oturum boyunca geçerli say.

## Ön kapı — tek soru

Kullanıcı ekran görüntüsü, URL veya akış paylaştığında **yalnızca tek bir çoktan seçmeli soru** sorulur (CLAUDE.md kural 13): hangi problemi çözmek istiyor?

- **Başlıyor ama bitirmiyor** — akışa giriyor, tamamlamıyor
- **Hiç başlamıyor** — sayfayı görüyor, ilk aksiyonu almıyor
- **Geliyor ama niteliksiz** — hacim var, kalite yok
- **Belirli bir problemim yok** — sayfaya bak, sen söyle

Seçeneklerin dilini sayfaya uyarla (form → "formu doldurmuyor", ürün sayfası → "sepete eklemiyor"). Kullanıcı problemi zaten yazdıysa sorma.

**Sormayacakların:** Trafik, test aracı, örneklem, bütçe. Bunlar senaryo üretmek için gerekli değildir ve çıktının önüne "eksik bilgi" diye konmaz. Trafik yalnızca kullanıcı süre/örneklem/anlamlılık sorduğunda istenir (kural 5). Test aracı yalnızca kurulum spesifikasyonunu o aracın diliyle adlandırmak için, kullanıcı söylediyse kullanılır — sorulmaz.

Ödeme, kargo/iade, fiyat gösterimi veya güven sinyali konuşuluyorsa hedef pazar sayfadan çıkarılamıyorsa sorulur (kural 11) — çoğu zaman alan adı, para birimi veya form alanlarından zaten bellidir.

## Asla yapma

- Üç kutusu eksik senaryo teslim etme (CLAUDE.md kural 1).
- Birincil KPI işaretlemeden KPI listesi verme (kural 2).
- Alt-skill mekaniğini kullanıcıya dökme — kullanıcı sonucu görür, tesisatı değil.
- Arşiv senaryosu ile üretilmiş senaryoyu ayırt etmeden sunma (kural 8).
