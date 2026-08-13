---
name: abtest-results
description: Interpret A/B test results and run the statistics on real numbers. Use when the user pastes visitor and conversion counts per variant, or asks "is this significant", "interpret these results", "did my test win", "which variant won", "calculate statistical significance", "what is the p-value", "confidence interval", "how many visitors do I need", "what sample size do I need", "how long should I run this test", "minimum detectable effect", "is my traffic split off", "sample ratio mismatch", "SRM", "sonuçları yorumla", "test bitti ne çıktı", "anlamlı mı", "kaç ziyaretçi lazım", "örneklem hesapla". Runs a real two-proportion z-test, confidence interval, required sample size, revenue and margin check, and an SRM check through scripts/analyze_results.py — the math is computed, never estimated — then states the decision and what happens next. To check whether the test was set up correctly in the first place, see abtest-audit.
metadata:
  version: 0.1.0
  category: analyze
  updated: 2026-08-11
---

# abtest-results — Sonuç Yorumlama ve Örneklem Hesabı

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` ve `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` bağlayıcıdır. Hesaplamalar `${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py` ile yapılır — anlamlılık ve p-değeri asla elle/tahminle hesaplanmaz, script çalıştırılır.

## İki mod

### A) Sonuç yorumlama (test bitti veya koşuyor)

1. Kontrol ve varyantın ziyaretçi + dönüşüm sayılarını al. Eksikse sor; oran verilip ziyaretçi sayısı verilmemişse ("kontrolde %5, varyantta %6 dönüşüm" gibi) mutlak sayıları da iste — oranla güven aralığı hesaplanamaz.
2. Çalıştır:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py significance \
     --control-visitors <n> --control-conversions <n> \
     --variant-visitors <n> --variant-conversions <n>
   ```
3. Çıktıyı ham JSON olarak gösterme; `methodology.md` merceğinden yorumla:
   - `normal_approx_valid: false` çıktıysa **başka hiçbir yorumu yapma**: bu testte z-testi geçerli değil (nadir olay), p-değeri ve güven aralığı güvenilmez. Kazanan/kaybeden ilan etme; daha fazla veri toplanmasını veya nadir olaylara uygun bir yöntem kullanılmasını söyle. Bu, örneklem büyük olsa bile geçerlidir.
   - `is_significant: false` çıktıysa **tek başına "kaybetti" deme**. `low_sample_warning` var mı bak, testin kaç gündür/haftadır koştuğunu sor. Örneklem yetmemiş mi yoksa değişiklik zaten zayıf mı — ikisini ayır (methodology.md → "Fark yok" teşhisi).
   - `is_significant: true` çıktıysa, testin **en az iki tam hafta** koştuğunu doğrula. Koşmadıysa "istatistiksel olarak anlamlı ama süre kuralına uymuyor, ortalamaya dönüş riski var" diye uyar — sonucu kesin kazanan ilan etme.
   - Kullanıcı guardrail rakamı da verdiyse (iade, marj, hata oranı) onu ayrıca değerlendir; guardrail kötüleşmişse birincil metrik anlamlı olsa bile "guardrail nedeniyle durdurulmalı" diye işaretle (methodology.md → guardrail erken durdurma istisnası).
   - Kullanıcı segment kırılımı (mobil/masaüstü, yeni/dönen) da verdiyse ayrı ayrı çalıştır, genel sonuçla karşılaştır; vermemişse ve genel sonuç "fark yok" ise segment kırılımını sor.
4. Sonuç cümlesi net olmalı: "anlamlı, uygulanabilir" / "anlamlı ama süre/örneklem riski var, bekle" / "anlamlı değil, X nedenle" — ortada bırakma. Karar şu tabloya göre verilir (satır çakışırsa üsttekini önceliklendir):

   **Önce "örneklem yeterli mi" sorusunu doğru sor.** Tabloda "Yeterli", `low_sample_warning`'in yokluğu **değildir**. O uyarı 250 dönüşümlük kaba bir alt sınıra bakar ve script'in kendisi bunun formal bir yeterlilik kriteri olmadığını söyler. Gerçek yeterlilik tek şeydir: **önceden belirlenmiş baz oran ve MDE için hesaplanan örneklem hedefine ulaşılmış olması.** Bunu `samplesize` komutuyla hesapla:

   - Kullanıcı testten önce bir MDE belirlediyse onu kullan.
   - Belirlemediyse, gözlenen baz oranla birlikte kullanıcıya sor: "bu sayfada kaç puanlık bir fark senin için uygulamaya değer?" Cevap gelmeden "yeterli" deme.
   - Hedefe ulaşılmadıysa örneklem **yetersizdir** — dönüşüm sayısı 250'yi kat kat aşsa bile. Bu durumda "fark yok" kararı verilmez; "bu testin bu farkı yakalayacak gücü yoktu" denir ve gereken örneklem yazılır.

   | Anlamlı mı | Örneklem (MDE hedefine göre) | Süre | Guardrail | Karar |
   |---|---|---|---|---|
   | — | — | — | Kötüleşti | **Durdur** — birincil metrik ne çıkarsa çıksın |
   | Hayır | Hedefe ulaşılmadı | — | Temiz | **Devam et veya güçsüz ilan et** — hedefe ne kadar kaldığını yaz; ulaşılamayacaksa testi "sonuçsuz" kapat, "fark yok" deme |
   | Hayır | Hedefe ulaşıldı | < 2 hafta | Temiz | **Bekle** — örneklem doldu ama süre kuralı dolmadı; iş döngüsü tamamlanmadan "fark yok" ilan etme |
   | Hayır | Hedefe ulaşıldı | ≥ 2 hafta | Temiz | **Anlamlı fark yok** — hedeflenen büyüklükte bir etki yok; daha küçük bir etki hâlâ mümkün olabilir, bunu söyle |
   | Evet | Hedefe ulaşılmadı | ≥ 2 hafta | Temiz | **Doğrulanmalı** — anlamlı çıktı ama güç yetersizdi, etki büyüklüğü abartılı olabilir; kırılgan işaretle |
   | Evet | Hedefe ulaşılmadı | < 2 hafta | Temiz | **Bekle** — ne güç ne süre koşulu sağlandı; peeking riskinin en yüksek olduğu durum, karar verme |
   | Evet | Hedefe ulaşıldı | < 2 hafta | Temiz | **Bekle** — istatistiksel olarak anlamlı ama süre kuralı dolmadı, ortalamaya dönüş riski var |
   | Evet | Hedefe ulaşıldı | ≥ 2 hafta | Temiz | **Uygulanabilir** — kazanan ilan edilebilir |

   `low_sample_warning` bu tabloda karar girdisi değildir; yalnızca "bu sayıların altında hiçbir yorum güvenilir değil" diyen bir alt bariyerdir. Uyarı varsa hedefe bakmaya bile gerek yok, örneklem kesin yetersizdir.
5. **Karardan sonra durma — testin devamını da yaz.** Sonuç yorumu tek başına teslim değildir; kararın karşılığı olan adımı da ver:
   - **Uygulanabilir çıktıysa:** aşağıdaki kademeli yayma tablosunu doldurup sun; kontrol varyantının ne zaman kaldırılacağını ve testin öğreniminin bir sonraki hipoteze nasıl bağlandığını da yaz (methodology.md → yerel tepe riski).

     | Aşama | Trafik payı | Kontrol sıklığı | Otomatik DUR koşulu | Devam koşulu |
     |---|---|---|---|---|
     | 1 | %25 | Günde 1 guardrail kontrolü | Guardrail 2 ardışık kontrolde referans dışına çıkarsa → tam geri al | 2 ardışık temiz kontrol → 2. aşama |
     | 2 | %50 | Günde 1 kontrol | Aynı kural | Aynı kural → 3. aşama |
     | 3 | %75 | Günde 1 kontrol | Aynı kural | Aynı kural → %100'e geç |
     | 4 | %100 | — | — | Buradan itibaren 7 günlük tam guardrail gözlemi |

     Aşama sayısı ve trafik payları sabit değil — düşük trafikli sayfada aşama başına süre uzatılır, yüksek riskli değişiklikte (fiyat, ödeme akışı) aşama sayısı artırılabilir; tabloyu bağlama göre uyarla, kopyala-yapıştır yapma.

     **"Temiz kontrol" ve "referans dışı" tanımsız bırakılmaz.** Tabloyu doldururken üçünü de yaz, yoksa tablo uygulanamaz:
     - **Referans aralığı:** Her guardrail için testten önceki normal dalgalanma bandı (ör. son 4 haftanın günlük en düşük ve en yüksek değeri). Bu bant yoksa kademeli yayma başlatılmaz — neyin bozulma olduğunu bilmeden neyin temiz olduğu bilinemez.
     - **Asgari gözlem:** Bir kontrolün "temiz" sayılması için o aşamada en az kaç kullanıcının varyantı görmüş olması gerektiği. Günlük hacim düşükse kontrol sıklığı günlük değil, bu sayıya ulaşıldığında yapılır; aksi halde her gün gürültü ölçülür.
     - **Bozulma eşiği:** Referans bandının ne kadar dışına çıkmanın DUR sayılacağı. Tek bir günlük sapma normal varyasyon olabilir; tablodaki "2 ardışık kontrol" kuralı tam da bunun içindir, ama bandın çok dışına tek seferlik büyük bir sapma (ör. hata oranının katlanması) beklenmeden geri alınır.
   - **Anlamlı fark yok çıktıysa:** öğrenim ne? Değişiklik zayıf mıydı (daha iddialı varyant), yoksa problem başka yerde mi (aynı sayfada farklı bir değişken)? Bir sonraki testi öner.
   - **Kaybettiyse:** mevcut deneyimin neden daha iyi çalıştığına dair tek cümlelik öğrenim yaz — kaybeden test de bilgidir, sessizce kapatma.
   - **Guardrail nedeniyle durdurulduysa:** geri alma adımı + guardrail'in neden bozulduğuna dair hipotez.
6. **Kaydı test hafızasına yaz (CLAUDE.md kural 16).** Sonuç yorumu ve devam adımı verildikten sonra, bu testin `.abtest-history.md` satırını üret ve kullanıcıya sun:

   ```
   | <YYYY-AA> | <sayfa/akış> | <test edilen tek değişken> | <kazandı/kaybetti/fark yok/yetersiz/durduruldu/geçersiz> | <birincil metrik etkisi> | <guardrail durumu> | <genellenebilir örüntü — yalnızca kazandıysa doldur, yoksa "—"> | <tek cümle not> |
   ```

   - Çalışma dizininde `.abtest-history.md` varsa satırı tablonun en üstüne eklemeyi öner; kullanıcı onaylarsa ekle.
   - Dosya yoksa `${CLAUDE_PLUGIN_ROOT}/templates/abtest-history.md` şablonundan oluşturmayı öner — bir kez öner, ısrar etme.
   - Sonuç değerini karar matrisiyle tutarlı seç: örneklem/süre dolmadan kapatıldıysa "kaybetti" değil **yetersiz**; SRM veya ölçüm hatası varsa **geçersiz**; guardrail nedeniyle durdurulduysa **durduruldu**.
   - **Genellenebilir örüntü** yalnızca "kazandı" sonucunda doldurulur — testin kendisini değil (ör. "kargo çubuğu kazandı"), ardındaki soyut mekanizmayı yaz (ör. "ilerleme göstergesi harcama davranışını güçlendiriyor"). Bu, aynı mekanizmanın başka sayfalarda da denenebilir olduğunu görünür kılar (`templates/abtest-history.md` → Genellenebilir örüntü sütunu).
   - Kullanıcı istemezse yazma. Bu dosya onun verisidir; public bir depoda çalışıyorsa `.gitignore`'a eklemesini hatırlat.
7. **Yüzde karışıklığına düşme:** Script hem `absolute_diff` (yüzde puan farkı) hem `relative_lift_pct` (göreli değişim) döndürür — ikisi farklı sayılardır ve karıştırılırsa yanlış anlaşılır (ör. %5'ten %6'ya çıkmak "1 puan artış" ile "%20 göreli artış" aynı şeyi anlatır, ama "%1 artış" demek yanlıştır). Çıktıda ikisini de ayrı ayrı ve etiketli ver: "kontrol %5,0 → varyant %6,0 (1,0 yüzde puan / göreli %20 artış)".

### A2) Fiyat/indirim/paket testinde gelir kontrolü

Test edilen şey fiyat, indirim, taksit, kargo eşiği veya paket ise dönüşüm oranı tek başına yanıltır (methodology.md → Dönüşüm oranı geliri gizleyebilir). Kullanıcıdan iki kolun ortalama sipariş tutarını da iste ve çalıştır:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py revenue \
  --control-visitors <n> --control-conversions <n> --control-aov <tutar> \
  --variant-visitors <n> --variant-conversions <n> --variant-aov <tutar> \
  [--margin-rate 0.35]
```

- `warning` alanı doluysa bunu çıktının en üstüne taşı: dönüşüm artarken gelirin düşmesi (veya tersi) bu testin asıl bulgusudur.
- Marj oranı biliniyorsa `--margin-rate` ile ziyaretçi başına brüt kârı da hesapla; indirim testlerinde gelir korunurken marj erimiş olabilir.
- Bu komut anlamlılık testi değildir — sipariş tutarı dağılımı çarpıktır. Yön göstergesi olarak sun ve dönüşüm oranının anlamlılığını ayrıca `significance` ile kontrol et. "RPV %5 arttı, anlamlı" deme.

### B) Örneklem büyüklüğü / süre planlama (test başlamadan önce)

1. Baz dönüşüm oranını ve hedeflenen göreli lift'i al (yoksa tipik aralık için %10-20 öner ve netleştirmesini iste).
2. Çalıştır:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py samplesize \
     --baseline-rate <ondalık> --mde <ondalık>
   ```
3. `required_n_per_variant` çıktığında, kullanıcının verdiği günlük/haftalık trafikle kaç gün süreceğini hesapla (`required_n_total / günlük_trafik`). İki tam haftadan kısa çıkıyorsa bile en az iki hafta öner (methodology.md kuralı, kısa süre örneklem yeterli olsa da dış geçerlilik riski taşır).
4. Trafik hiç verilmediyse süre hesaplama, sadece gereken örneklemi ver ve trafiği sor.

## Asla yapma

- p-değerini veya anlamlılığı script çalıştırmadan tahmin etme.
- Testin süresini sormadan "anlamlı, bitir" deme — süre kuralı KPI kadar bağlayıcı.
- Ham JSON'u yorumsuz kullanıcıya atma; her sayı bir cümleyle Türkçeleştirilir.
- Test hafızası dosyasına kullanıcının onayı olmadan yazma; kaydı üret, eklemeyi öner, kararı ona bırak.
- Örneklem hesaplarken kullanıcı MDE (hedef lift) vermediyse rastgele bir sayı uydurma; sor.
