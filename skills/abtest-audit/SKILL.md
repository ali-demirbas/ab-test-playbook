---
name: abtest-audit
description: Audit an existing A/B test plan, running experiment or mockup pair for methodological flaws. Use when the user says "test planımı denetle", "bu test doğru mu kurulmuş", "review my experiment", or shares variant designs asking what's wrong.
metadata:
  version: 0.1.0
  category: audit
---

# abtest-audit — Test Planı Denetimi

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` ve `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` bağlayıcıdır.

## Denetim listesi

Paylaşılan planı/varyantları şu sırayla denetle; her bulguyu kanıtıyla raporla:

1. **Değişken izolasyonu (en kritik):** A ile B arasında test edilen öğe DIŞINDA fark var mı? Fiyat, ürün, puan, rozet, metin, sıralama — herhangi bir ikinci fark confound'dur. Varyant görselleri paylaşıldıysa ikisini öğe öğe karşılaştır.
2. **Birincil metrik:** Tek ve net mi? Birden çok metrik eşit ağırlıkta okunuyorsa p-hacking riski olarak işaretle.
3. **Guardrail:** Dönüşüm artarken bozulabilecek metrik (marj, iade, hız, destek, terk) izleniyor mu? Yoksa senaryoya uygun guardrail öner.
4. **Ölçülebilirlik:** Metrikler araçla gerçekten ölçülebilir mi? Vekilsiz "algı" metriklerini işaretle. Varyant istemci tarafında (sayfa yüklendikten sonra JS ile) mi uygulanıyor, sunucu tarafında mı? İstemci tarafı uygulamada kullanıcı bir an için kontrol varyantını görüp sonra değişikliğe geçebilir (flicker/FOUC) — bu hem deneyimi bozar hem de o kullanıcının hangi varyanta sayılacağını belirsizleştirir. Bilinmiyorsa doğrulanması gereken bir varsayım olarak işaretle.
5. **Örneklem/süre:** Trafik hacmine göre test süresi gerçekçi mi? İki tam haftadan kısa plan varsa uyar. Trafik bilinmiyorsa bunu bulgu olarak yaz, tahmin uydurma.
6. **Hipotez-kurgu tutarlılığı:** Başlık/hipotez ile varyantların gerçekte değiştirdiği şey aynı mı? (Başlık "arka plan rengi" derken varyant menü sırasını değiştiriyorsa uyumsuzluktur.)
7. **Etik/yasal:** Sahte referans fiyat, gizlenen toplam tutar, kapatılamayan modal, yanıltıcı stok — varsa engelleyici bulgu olarak işaretle.
8. **Kurgu hijyeni:** Test sırasında planlanan kampanya/fiyat/algoritma değişikliği var mı? A/A doğrulaması gerekli mi (yeni araç / yeni segmentasyon)?
9. **Yenilik etkisi riski:** Test kısa süre (bir haftadan az) koşup kapatıldıysa veya kapatma planlanıyorsa, ölçülen liftin kalıcı davranış değişikliği mi yoksa değişikliğin "yeni" olmasından kaynaklanan geçici ilgi mi olduğunu ayırt edilemez diye işaretle.
10. **Segment kontrolü:** Sonuç "genel olarak fark yok" ise, orada durma. En az cihaz (mobil/masaüstü) ve kullanıcı tipi (yeni/dönen) kırılımı soruldu mu? Sorulmadıysa, iki segmentin birbirini götürüp yanlış "fark yok" sonucu vermiş olabileceğini bulgu olarak yaz. Ama bunu kazanan bir alt grup arayana kadar veri dilimlemeye çevirme — genel sonuç zaten net çıktıysa segment taraması önerme (p-hacking riski).
11. **"Fark yok" teşhisi:** Sonuç "anlamlı fark yok" ise, sebebi ayır: örneklem hedefine ulaşılmadı mı (trafik/süre yetersiz), yoksa hedefe ulaşıldı ama değişiklik davranışı etkileyecek kadar belirgin değil miydi? İkisi farklı düzeltme gerektirir (daha fazla bekle / daha iddialı bir varyant tasarla).
12. **Örneklem oranı uyuşmazlığı (SRM):** Gerçekleşen trafik bölüşümü planlanan orana (ör. 50/50) uyuyor mu? Sapmanın anlamlı olup olmadığı sabit bir yüzdeyle değil örneklem büyüklüğüyle belirlenir: 200 kişilik bir testte 52/48 tamamen normalken 200 binlik bir testte aynı oran ciddi bir sinyaldir. `analyze_results.py srm --control-visitors <N> --variant-visitors <N> --expected-split <ör. 0.5>` ile çalıştırın — ki-kare uyum testiyle sınar, iki-oranlı z-testinden farklıdır (iki kolun sayıları bağımsız örneklem değil aynı toplamın parçalarıdır, `significance` komutu bu soruya uygulanamaz). `srm_detected: true` çıkarsa randomizasyon veya araç hatasıdır; sonuçlar güvenilmez, engelleyici bulgu olarak işaretle. Sık sebep: varyant ataması ile sonuç ölçümü aynı olayla karışmış (ör. "gösterildi" ile "tıklandı" tek event'te loglanmış) — bu iki olay ayrı loglanmalı, aksi halde SRM'nin kaynağı bulunamaz.
13. **Çoklu karşılaştırma / peeking:** Burada sayılan şey **karar metrikleridir**, izlenen metriklerin tamamı değil. Bu playbook her testte bir birincil metrik + dört ikincil/guardrail metrik ister; guardrail'ler "bozulmadı mı" diye izlenir, kazananı belirlemek için kullanılmaz, dolayısıyla çoklu karşılaştırma sayısına girmezler. Bulgu şu üç durumda yazılır: (a) kazanan kararı birden fazla metriğe bağlanmışsa ("CR veya AOV'den biri artarsa uygularız"), (b) önceden tanımlanmamış segmentlerde kazanan aranmışsa, (c) sonuca defalarca bakılıp anlamlılık görülünce test durdurulmuşsa. Üç veya daha fazla varyant kolu varsa bunu ayrıca not et. Guardrail sayısının fazla olmasını tek başına bulgu sayma.
14. **Geçmiş tekrarı:** Çalışma dizininde `.abtest-history.md` varsa oku (CLAUDE.md kural 16). Denetlenen test bu sayfada daha önce koşulmuş mu? Koşulmuş ve sonuç "kaybetti/fark yok" ise, aradan ne değiştiğini sor — değişen bir şey yoksa aynı sonucu almanın maliyeti bir bulgudur. Sonuç "geçersiz/yetersiz" idiyse tekrar koşmak doğrudur, bunu da yaz. Aynı değişken art arda fark yok veriyorsa daha yapısal bir varyant öner (yerel tepe riski).
15. **Deney kirliliği (contamination):** Üç soru sırayla:
    - Varyant ataması hangi kimliğe (user ID, cihaz ID, anonim cookie) bağlı üretiliyor — bu kimlik login/cihaz değişiminde aynı kalıyor mu, yoksa oturum başına yeniden mi türetiliyor (sticky bucketing)?
    - "Gösterildi" (exposure) olayı sonuç olayından (satın alma, tıklama) ayrı mı loglanıyor — atandı ama hiç gösterilmedi farkı sorgulanabiliyor mu?
    - Test süresince segment/dağılım kuralları (yeni segment, değişen rollout yüzdesi) güncellendi mi — güncellendiyse kullanıcının farklı bir varyanta kayma ihtimali değerlendirildi mi?
    Bilinmiyorsa doğrulanması gereken bir varsayım olarak işaretle.
16. **Seçici kayıp (selective attrition):** Kontrol ve varyant arasında ölçüm/veri kaybı oranı eşit mi? Bir varyant teknik nedenle (ağır sayfa, geç yüklenen script, tarayıcı uyumsuzluğu) bazı kullanıcılardan sistematik olarak daha az veri topluyorsa sonuç geçersizdir — bu SRM'den farklıdır (SRM örnekleme oranını, bu ölçüm tamlığını sorgular). Kanıt yoksa "kontrol edilmeli" diye işaretle.

## Çıktı biçimi

- Bulgular önem sırasıyla: `[Engelleyici] / [Ciddi] / [İyileştirme]` etiketiyle, her biri tek cümle sorun + tek cümle düzeltme.
- Emin olamadığını "doğrulanmalı" diye işaretle; kesinmiş gibi sunma.
- Sonda tek paragraf karar: "Bu test bu haliyle koşulabilir mi?" — evet/hayır + koşul.

## Asla yapma

- Genel geçer laf ("iyileştirilebilir") yazma; her bulguda somut değişiklik öner.
- Sorun bulamadıysan sorun uydurma; "değişken izolasyonu temiz" demek de bir bulgudur.
