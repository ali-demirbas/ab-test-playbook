# A/B Test Backlog

Bu dosya henüz koşulmamış test adaylarının sıralı listesidir. `ab-test-suggest` ve `ab-test-design` öneri üretmeden önce burayı okur (varsa); aynı sayfa için zaten sırada bekleyen bir aday yeniymiş gibi tekrar önerilmez.

**Nereye konur:** Projenin kök dizininde `.abtest-backlog.md` adıyla. (Bu dosya o şablonun kendisidir; kopyalayıp adını değiştirin.) İsteğe bağlıdır.

**Kim doldurur:** `ab-test-suggest` bir turdaki güçlü adayları (mekanizma kapısından geçen ve önceliği Yüksek ya da Orta olanlar) buraya eklemeyi önerir; yalnızca siz sohbette onaylarsanız ekler. Elle de yazabilirsiniz. Bir aday koşulunca satırı silin ve sonucu, test aracınızın bildirdiği şekliyle, `.abtest-history.md` dosyasına kendiniz yazın.

**Gizlilik:** Bu dosya sizin iş planınızı içerir. Public bir depoda tutuyorsanız `.gitignore`’a ekleyin.

## Adaylar

Önceliği Yüksek olanlar en üstte.

> **Aşağıdaki satır örnektir, gerçek veri değildir.** “(örnek)” diye işaretlidir; kendi ilk adayınızı eklerken silin.

| Eklenme | Sayfa/Akış | Soru biçiminde başlık | Tek değişken | Mekanizma (bir cümle) | Öncelik | Kanıt | Kaynak | Durum |
|---|---|---|---|---|---|---|---|---|
| 2026-09 (örnek) | Sepet | Teslimat tarihini sepette göstermek ödeme başlatmayı artırır mı? | Tahmini teslimat tarihi (yok → var) | Ödeme öncesi “ne zaman gelir” sorusunu yanıtlayarak zamanlama itirazını kaldırır | Yüksek | arşiv örüntüsü | arşivden | sırada |

## Değerler

- **Öncelik:** Yüksek / Orta (önceliği Düşük adaylar buraya eklenmez)
- **Kanıt:** kendi verin / arşiv örüntüsü (derlenmiş bir fikir, test sonucu değil) / sektör gözlemi / sezgi
- **Kaynak:** arşivden / arşivden uyarlandı / bu sayfa için üretildi
- **Durum:** sırada / tasarlanıyor / koşuyor (koşan test bitince satırı silin ve sonucu `.abtest-history.md` dosyasına kendiniz yazın)
