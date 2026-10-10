# Eval 09: ön kayıtlı sonuç, anlamlı kaybeden, çözülemeyen guardrail

**Girdi A (ön kayıt bloğuyla gelen sonuç):** Kullanıcı aşağıdaki bloğu ve sayıları yapıştırır; test 28 gün koşmuş ve bugün bitmiştir.

```json
{"preregistration": {
  "hypothesis": "Katkı payı ekranına adım yönergesi eklemek ilerlemeyi artırır",
  "variable": "Adım yönergesi satırı",
  "primary_kpi": {"name": "Katkı payı artışını tamamlama oranı (atanan kullanıcı başına)", "direction": "increase"},
  "guardrails": [
    {"name": "Destek talebi oranı (atanan kullanıcı başına)", "direction": "must_not_increase", "margin_relative": 0.10},
    {"name": "30 gün içinde geri alma oranı (atanan kullanıcı başına)", "direction": "must_not_increase", "margin_relative": 0.05, "read_after_days": 30},
    {"name": "Erişilebilirlik kontrolü", "type": "check", "criterion": "Klavye ve ekran okuyucu incelemesi B'de kritik sorun bulmaz"}
  ],
  "mde": 0.10, "alpha": 0.10, "power": 0.8, "alternative": "two-sided",
  "allocation": {"A": 0.5, "B": 0.5},
  "planned_n_per_arm": 20000, "duration_days": 28,
  "decision_rule": "Uyum B metnini onayladıktan sonra başlar; birincil metrik beyan edilen yönde anlamlıysa ve bütün guardrail'ler temizse yayına alınır",
  "segments": ["device"]
}}
```

“A: 20.000 kullanıcı, 2.000 tamamlama, 600 destek talebi. B: 20.000 kullanıcı, 2.110 tamamlama, 610 destek talebi. Kazandı mı?”

**Beklenen davranış:**
1. SRM önce çalışır, `allocation` alanından `--expected-split 0.5` ile: temiz.
2. Birincil metrik blok alanlarıyla koşulur: `significance … --confidence 0.90 --expected-direction increase --planned-n 20000` (alfa 0,10 → güven 0,90; varsayılan 0,95 kullanılmaz). Çıktı: `p_value` 0,07008, `decision_code: significant_improvement`. Aynı sayılar varsayılan 0,95 ile `not_significant` çıkar; kararı beyan edilen alfa verir.
3. Destek talebi guardrail'i blokta yazan yön ve marjla koşulur: `--ni-margin 0.10 --guardrail-direction must_not_increase --confidence 0.90` → `status: clean` (p 0,0824; varsayılan 0,95 ile aynı sayılar `inconclusive` olurdu). Yön bloktan kopyalanır, tahmin edilmez.
4. Geciken guardrail **henüz okunamaz**: test bugün bitti, son kohort için pencere 30 gün sonra kapanır. Skill bu guardrail için sayı istemez, okumaz ve erken “temiz” demez; pencerenin kapanacağı tarihi verir.
5. Erişilebilirlik kontrolü hesaplanmaz: skill kullanıcıdan ölçüte göre geçti/kaldı teyidi ister. Teyit yoksa geçmiş sayılmaz.
6. Karar **geçici kazanan**dır, “yayına al” değildir: birincil metrik beyan edilen yönde anlamlı ve ölçülen guardrail temiz, ama geciken pencere kapanmadı ve kontrol teyit edilmedi. Skill “yayına al” için dört koşulu sayar (beyan edilen yönde anlamlı birincil, bütün marjlı guardrail'ler temiz, bütün kontroller geçti, bütün geciken pencereler kapandı) ve hangilerinin açık olduğunu söyler.
7. `decision_rule` cümlesi alıntılanır ve uyum onayının test başlamadan alınıp alınmadığı (yayın öncesi kapı) tek soruyla teyit edilir ya da açık varsayım olarak yazılır. Tur en fazla bir soru sorar (kural 19).
8. Segment yorumu yalnızca önceden beyan edilen `device` için ve `interaction` ile yapılır.

**Düşme koşulları:**
- Varsayılan %95 güvenle koşulup sonucun “anlamlı değil” ya da farklı bir p eşiğiyle sunulması.
- Geciken guardrail'in pencere kapanmadan okunması ya da “temiz” sayılması.
- Erişilebilirlik kontrolünün teyitsiz geçmiş kabul edilmesi.
- “Kazandı, yayına al” denmesi.
- Guardrail yönünün bloktan okunmayıp varsayılması.

**Girdi B (anlamlı kaybeden):** “Kontrol 10.000 ziyaretçi 600 dönüşüm, varyant 10.000 ziyaretçi 500 dönüşüm. Üç haftadır koşuyor, örneklem hedefi doldu. Anlamlı çıktı, yayına alalım mı?”

**Beklenen davranış:**
1. `significance` çıktısı: `p_value` 0,00192, `is_significant: true`, `effect_direction: variant_lower`, `relative_lift_pct` −16,67, `decision_code: significant_degradation`.
2. Karar **Kaybetti, yayına alınmaz**. “Anlamlı” kelimesi tek başına kazanan anlamına gelmez; skill varyantın anlamlı biçimde **kötü** olduğunu açıkça söyler.
3. Devamı yazılır: mevcut deneyimin neden daha iyi çalıştığına dair tek cümlelik öğrenim ve bir sonraki test önerisi. Test-hafızası satırı `kaybetti` olarak önerilir, `fark yok` olarak değil.
4. Aynı sayılar `--alternative greater` ile koşulsaydı: `is_significant: false` ama `opposite_direction_significant: true` ve yine `decision_code: significant_degradation`; skill bunu “fark yok” diye kapatmaz.

**Düşme koşulları:**
- “Anlamlı, yayına al” denmesi ya da kademeli yayılım tablosunun sunulması.
- Sonucun “fark yok” ya da “yetersiz” diye kaydedilmesi.

**Girdi C (guardrail belirsiz):** “Birincil metrik kazandı, iki hafta doldu, örneklem hedefi tamam. İade oranı guardrail'i: kontrol 20.000 siparişte 800 iade, varyant 20.000 siparişte 800 iade. Marjımız göreli %2 idi. Yayına alabilir miyiz?”

**Beklenen davranış:**
1. Guardrail `--ni-margin 0.02 --guardrail-direction must_not_increase` ile koşulur → `status: inconclusive`, `inconclusive_reason: underpowered`, `sample_needed.n_control` 756.894, `margin_too_tight_for_current_n: true`.
2. Skill bunu kendi durumu olarak raporlar: “temiz” demez, “kötüleşti” de demez. Açıkça söyler: oran hiç değişmemiş olsa bile %2'lik marjı göstermek için kol başına yaklaşık 757 bin sipariş gerekir; marj bu trafik için dardır.
3. Karar **guardrail çözülmedi, henüz yayın yok**; iki dürüst seçenek sunulur: o örnekleme kadar devam etmek ya da bu guardrail'i otomatik durdurma koşulu yapan kademeli yayılım (kullanıcının kabul ettiği risk olarak, “temiz” diye değil). Marj sonuç görüldükten sonra genişletilmez; daha geniş marj ancak bir sonraki test için beyan edilir.
4. Yön verilmeden koşulursa script hata döner; skill yönü varsaymaz.

**Düşme koşulları:**
- Belirsiz guardrail'in “temiz” sayılıp “yayına al” denmesi.
- Gereken örneklemin ya da “marj dar” tespitinin söylenmemesi.
- Marjın sonuç görüldükten sonra %10'a çekilip “temiz” denmesi.
