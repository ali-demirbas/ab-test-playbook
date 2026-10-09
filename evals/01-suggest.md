# Eval 01 — suggest akışı

**Girdi A:** "Moda e-ticaret sitem var, sepet sayfam için test öner." (Trafik verilmemiş, sayfa paylaşılmamış.)

**Beklenen davranış:**
1. Ön kapı: trafik, test aracı veya kurulum bilgisi **sorulmaz** (trafik: kural 5; araç/kurulum: senaryo üretimi için gerekli değildir, `ab-test-suggest` adım 1). Sayfa paylaşılmadığı için kural 13'ün problem sorusu da zorunlu değildir; senaryo doğrudan üretilir.
2. `cart-checkout.md` baştan sona okunmaz. Önce `grep -nE '^## |Değişken:'` ile başlıklar listelenir, yalnızca seçilen senaryo blokları okunur. Form tasarımına dair aday çıkarsa `forms-signup.md` için de aynı yol izlenir.
3. 1-5 **güçlü aday** gelir (mekanizma kapısını geçen ve ICE bandı en az Orta olan), ICE gerekçeli ve sıralı. Sayıyı tamamlamak için zayıf aday eklenmez; tek güçlü senaryo da tam bir yanıttır (kural 9).
4. Sayfa paylaşılmadığı için her mekanizma, sepet sayfası tipinde tipik olan engeli adlandırır ve bunu "kendi sayfanızda doğrulayın" diye varsayım olarak belirtir.
5. Her senaryo doğrudan `ab-test-card` ile HTML kart olarak üretilir ("arşivden" etiketiyle). Sohbette yalnızca başlık ve tek cümlelik özet kalır; üç kutulu tam metin ayrıca yazılmaz (kural 9).
6. Marka kılavuzu **sorulmaz**: nötr palet kullanılır, kartın altına tek satırlık yeniden renklendirme teklifi eklenir (kural 12).
7. Her kartın KPI kutusunda ilk madde birincil diye işaretli, en az bir guardrail "…memeli" kalıbında.
8. Örnekler moda bağlamına yerelleştirilmiş (kulaklık örneği geçmiyor).
9. `agents/mockup-reviewer` kart başına ayrı ayrı değil, turun bütün kartları için bir kez çalışır.
10. Tur en fazla bir soru sorar: backlog teklifi ya da "N güçlü aday daha var" teklifi, ikisi birden değil (kural 19).

**Düşme koşulları:**
- Ön kapıda trafik, test aracı, kurulum veya marka kılavuzu sorusu sorulması.
- Trafik verilmediği hâlde "2 haftada sonuç alırsın" tarzı süre/örneklem vaadi.
- Eksik bilginin çıktının önüne "önce şunu öğrenmem lazım" diye konması.
- Üç kutudan biri eksik senaryo.
- Herhangi bir senaryonun üç kutulu tam içeriğinin kart dışında ayrıca sohbete metin olarak yazılması (kural 9 ihlali).
- 5'ten fazla senaryonun sorulmadan üretilmesi ya da sayıyı doldurmak için zayıf aday eklenmesi (kural 9).
- Aynı turda birden fazla soru (kural 19).

**Girdi B (gönüllü verilen trafik):** "Sepet sayfam ayda ~40 bin ziyaretçi alıyor, dönüşüm %3. Test öner."

**Beklenen davranış:**
1. Senaryolar Girdi A'daki gibi gelir; trafik **sorulmadan** verildiği için listenin altına tek satırlık bir fizibilite notu eklenir.
2. Not script ile hesaplanır, tahmin edilmez: `analyze_results.py samplesize --baseline-rate 0.03 --mde 0.10 --daily-visitors 1333` → kol başına 53.211 ziyaretçi, toplam 106.422, 84 gün (12 hafta).
3. Not bir sonuç da söyler: bu trafikte küçük bir değişikliğin %10'luk etkisini görmek yaklaşık üç ay sürer; daha cesur bir değişiklik ya da değişikliğe daha yakın bir metrik önerilir.

**Düşme koşulları:**
- Fizibilite notunun hiç verilmemesi ya da elle kestirilmesi.
- Notun senaryoların önüne "önce bunu çözelim" diye konması.

**Girdi C (pazara bağlı aday, pazar bilinmiyor):** "Ödeme sayfamda taksit seçeneğini öne çıkaran testler öner." (Pazar belirtilmemiş, sayfa yok.)

**Beklenen davranış:**
1. Taksit senaryosu bekletilmez: kart üretilir ve altına tek satırlık pazar bağımlılığı notu eklenir ("taksitin yaygın olduğu bir pazar varsayıldı").
2. Pazar sorusu turun **tek** sorusu olarak sorulur (kural 11, kural 19 önceliğiyle).

**Düşme koşulları:**
- Pazar cevabı gelene kadar hiçbir senaryonun üretilmemesi.
- Pazar notunun hiç düşülmemesi.
