# Denetim örneği: kusurlu bir plan, denetlenmiş hâli

`/ab-test audit` komutunun Türkçe bir plana verdiği cevap. Plan kurgusaldır.
Denetim planın kendisine bakar (UX, CRO, yöntem, etik, gizlilik, düzenleme,
erişilebilirlik ve uygulanabilirlik); planın rakamlarını okumaz. İngilizce
örnek: [`audit-example.md`](audit-example.md).

## Kullanıcının getirdiği plan

Dosya olarak verildi, `plan.md`:

> **Sayfa:** Ürün detay sayfası (ev ve yaşam e-ticareti, web ve mobil web).
> **Hipotez:** “Teslimat” sekmesini açan ziyaretçi yalnızca kargoya veriliş
> süresini görüyor, ürünün ne zaman elinde olacağını bilmeden karar vermiyor.
> Teslim süresini yazarsak daha çok ziyaretçi sipariş verir.
> **A:** “Teslimat” sekmesi kapalı; açılınca “Kargoya veriliş: 1-3 iş günü.” yazar.
> **B:** Yalnızca mobil webde: sekmenin metni “Tahmini teslim: 2-4 iş günü.”
> olur, sekmenin başlığı da “Hızlı teslimat” olur.
> **Birincil KPI:** Sepete ekleme oranı, sayfayı açan kullanıcı başına, tüm cihazlar.
> **Guardrail:** İptal oranı artmamalı.
> **Kurulum:** %50 / %50, kullanıcı kimliğine göre, sunucu tarafında.
> **Süre ve karar:** 3 hafta koşar, B %95 anlamlıysa yayına alırız.

Dosya okunmadan önce taranır (CLAUDE.md kural 18):

```bash
python3 scripts/validate_input.py --lang tr plan.md
```

Talimat benzeri bir satır yok, plan veri olarak denetlenir.

## Denetimin cevabı

Önce tablo gelir, en ağır bulgu en üstte; her satır kontrol listesindeki
maddesinin sabit etiketini taşır (`[Kritik]`, `[Ciddi]`, `[Orta]`, `[Not]`).
Ayrıntı yalnızca kritik satır için yazılır, denetim düzeltilmiş planla kapanır.

| Önem | Bulgu | Düzeltme |
|---|---|---|
| [Kritik] | B’de sekme başlığı da değişiyor | Başlık iki kolda “Teslimat” kalsın |
| [Ciddi] | Birincil bir ara adım: sepete ekleme | Dönüşüm Oranı (CR) birincil, sepete ekleme ikincil |
| [Ciddi] | B yalnız mobil webde, KPI tüm cihazlarda | Yalnız mobil web kullanıcıları sayılsın |
| [Ciddi] | Değişiklik kapalı sekmede, gösterim sayfa yüklemede sayılıyor | Sekme açıldığında, iki kolda aynı noktada sayılsın |
| [Orta] | Guardrail’in paydası ve penceresi yok | Sipariş başına, pencere adında |
| [Orta] | Kırılımlar önceden yazılmamış | İşletim sistemi ve yeni / dönen kullanıcı |
| [Orta] | Testi neyin geçersiz kılacağı yazılmamış | Düzeltilmiş plandaki “Sabit kalanlar” satırı |

**Karar: bu hâliyle başlayamaz; düzeltilmiş planla başlayabilir.**

**B’de sekme başlığı da değişiyor.** “Hızlı teslimat” başlığı sekmeyi kimin
açacağını da değiştirir; fark metinden mi başlıktan mı geldi, söylenemez.

Doğrulanacaklar: 2-4 iş günü teslim süresi operasyonca tutulabiliyor mu;
girişsiz ziyaretçi hangi kimlikle atanıyor; aynı sayfada başka test var mı.

Bakılan 20 başlıktan temiz olanlar: Mekanizma, UX ve CRO uyumu, Erişilebilirlik,
Etik, koruma ve düzenleme, Gizlilik, Kurulum düzeni, Çok değişkenli plan,
Seçici veri kaybı, Geçmiş.

Kontrol edilmedi: “3 hafta”, %50 / %50 bölünme ve “%95 anlamlıysa yayına
alırız” kuralı. Bu playbook A/B test önerir, tasarlar, denetler ve
görselleştirir. Sonuç analizi yapmaz; örneklem, süre, anlamlılık veya kazanan
hesaplamaz. Bunun için test aracınızın kendi raporunu kullanın. Mevcut dönüşüm
oranınızı ve uygun ziyaretçi sayınızı yazarsanız kaba bir ölçülebilirlik
aralığı gösterebilirim.

**Düzeltilmiş plan**
- Değişken: “Teslimat” sekmesindeki süre metni.
- A: Sekme “Teslimat” başlığıyla kapalı; açılınca “Kargoya veriliş: 1-3 iş günü.”
- B: Aynı sekme, aynı başlık; açılınca “Tahmini teslim: 2-4 iş günü.” (yalnız mobil web).
- Hipotez: Sekmeyi açan ziyaretçi ürünün ne zaman elinde olacağını bilmediği için karar vermiyor; teslim süresini yazarsak zamanlama itirazı yanıtlanır, daha çok ziyaretçi sipariş verir; teslim belirsizliğinin bu adımda engel olup olmadığını öğreniriz.
- Birincil KPI: Dönüşüm Oranı (CR), mobil webde “Teslimat” sekmesini açan kullanıcı başına; açılış iki kolda aynı noktada kaydedilir.
- Guardrail: İptal Oranı (pencere doğrulanmalı), sipariş başına, artmamalı.
- Sabit kalanlar: Sekmenin başlığı, yeri ve kapalı durumu, fiyat ve buton; ikinci bir değişiklik ya da aynı sayfada başka bir test testi geçersiz kılar.
- Başlamadan önce: Yukarıdaki üç madde doğrulanır; kırılımlar işletim sistemi ve yeni / dönen kullanıcı.

İsterseniz düzeltilmiş planı karta çevireyim.
