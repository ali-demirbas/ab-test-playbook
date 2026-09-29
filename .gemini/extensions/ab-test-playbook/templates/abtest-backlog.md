# A/B Test Backlog

Bu dosya henüz koşulmamış test adaylarının sıralı listesidir. `ab-test-suggest` ve `ab-test-design` öneri üretmeden önce burayı okur (varsa); aynı sayfa için zaten sırada bekleyen bir aday yeniymiş gibi tekrar önerilmez.

**Nereye konur:** Projenin kök dizininde `.abtest-backlog.md` adıyla. (Bu dosya o şablonun kendisidir — kopyalayıp adını değiştirin.) İsteğe bağlıdır.

**Kim doldurur:** `ab-test-suggest` bir turdaki güçlü adayları (mekanizma kapısından geçen ve ICE ≥ Orta olanlar) buraya eklemeyi önerir; yalnızca siz sohbette onaylarsanız ekler. Elle de yazabilirsiniz. Bir aday koşulunca satırı silin ve sonucu `.abtest-history.md`'ye yazın.

**Gizlilik:** Bu dosya sizin iş planınızı içerir. Public bir depoda tutuyorsanız `.gitignore`'a ekleyin.

## Adaylar

En yüksek ICE en üstte.

> **Aşağıdaki satır örnektir, gerçek veri değildir.** Kendi ilk adayınızı eklerken silin.

| Eklenme | Sayfa/Akış | Soru biçiminde başlık | Tek değişken | Mekanizma (bir cümle) | ICE | Kanıt | Kaynak | Durum |
|---|---|---|---|---|---|---|---|---|
| 2026-09 | Sepet | Teslimat tarihini sepette göstermek ödeme başlatmayı artırır mı? | Tahmini teslimat tarihi (yok → var) | Ödeme öncesi "ne zaman gelir" sorusunu yanıtlayarak zamanlama itirazını kaldırır | Yüksek | arşiv emsali | arşivden | sırada |

## Değerler

- **ICE:** Yüksek / Orta (Düşük adaylar buraya eklenmez)
- **Kanıt:** kendi verisi / arşiv emsali / sektör gözlemi / sezgi
- **Kaynak:** arşivden / bu sayfa için üretildi
- **Durum:** sırada / tasarlanıyor / koşuyor (koşan test bitince satır geçmiş dosyasına taşınır)
