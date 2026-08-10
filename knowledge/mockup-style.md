# Görsel Dil — Senaryo Kartı ve Mockup Kuralları

`abtest-card` skill'i ve `templates/scenario-card.html` bu spec'e uyar. Kaynak: arşivin görsel destesi (repo dışında tutulan dahili tasarım referansı — repoya görsel dosya eklenmez).

## Nötr palet

Marka kılavuzu yokken (kural 12c) kart şu renklerle üretilir: üç kutunun kimlik renkleri teal `#08616b`, amber `#6b3804`, navy `#17086b` (başlık şeritleri); mockup içindeki birincil CTA şablonun varsayılan turuncusu (`#ff6a00`); değişen öğe halkası kırmızı (`#e62d37`). Bu palet kasıtlı olarak markasızdır.

## Kart düzeni

- Yatay kart, iki bölge: **solda mockup çifti**, **sağda metin sütunu**.
- Mockup çifti: solda `Variant A` (kontrol), sağda `Variant B` (test). Her ikisinin üstünde yeşil hap etiket (`Variant A` / `Variant B`).
- Sağ sütun: en üstte soru biçiminde başlık (bold, ~2 satır), altında 2-3 cümlelik açıklama, altında üç kutu.

## Üç kutunun stili

Her kutu: renkli gradient başlık şeridi + beyaz gövde kartı.

| Kutu | Başlık şeridi | Başlık metni rengi |
|---|---|---|
| Test Edilmesi Gerekenler | Camgöbeği/turkuaz gradient | Koyu teal `#08616b` |
| Takip edilecek ana KPI’lar | Sarı/amber gradient | Koyu kahve `#6b3804` |
| Yapılmaması Gerekenler | Mor/lila gradient | Koyu lacivert `#17086b` |

- Başlık: kalın, ~20px eşdeğeri.
- Gövde: madde imli liste, her maddenin `Etiket:` kısmı **bold**, geri kalanı normal; metin rengi siyah ~%60 opaklık.
- Kutular hafif gölgeli, köşeleri yuvarlak (radius ~17), kesikli/yumuşak kenar hissi.

## Gerçekçilik seviyesi

Mockup **tam gerçekçi** üretilir: metin, fiyat, etiket ve düzen gerçek yazılır. Gri yer tutucu kutular yalnızca **fotoğrafın** yerini tutar (ürün görseli, avatar); metnin yerine kullanılmaz. "Başlık", "Lorem ipsum", "Metin alanı" gibi doldurma ifadeleri kabul edilmez.

**Gerçekçi ne demek: kullanıcının kendi sayfası, uydurulmuş bir sayfa değil.** Bu ayrım kartın en kritik kuralıdır.

- **Kullanıcı bir sayfa paylaştıysa (ekran görüntüsü, URL veya akış):** mockup o sayfanın yeniden çizimidir. Ürün adı, fiyat, buton metni, alan etiketleri, bölüm sırası, menü öğeleri — ekranda ne varsa o yazılır. Variant A ekrandaki hâlin birebir kendisidir (CLAUDE.md kural 15): yeniden tasarlanmaz, sadeleştirilmez, "daha iyisi" yapılmaz, eksikleri tamamlanmaz. Variant B yalnızca tek bir öğede A'dan ayrılır. Kendi kafandan bir e-ticaret sayfası kurup üstüne testi oturtmak, gerçekçilik değil uydurmadır ve kural 15'in ihlalidir.
- **Ekran görüntüsünden okunamayan bir ayrıntı varsa** (kesilmiş bir metin, görünmeyen bir bölüm) uydurma: ya o bölümü mockup'a hiç koyma, ya da kullanıcıya sor. Boşluğu makul görünen bir içerikle doldurmak, kullanıcının sayfasını yanlış temsil eder.
- **Ortada paylaşılmış bir sayfa yoksa** (arşivden gelen jenerik senaryo, `abtest-suggest` çıktısı): temsili bir örnek kurulur, ama bu durum kartta belli olur — örnek içerik gerçek bir müşteri sayfasıymış gibi sunulmaz.

Gerekçesi: kart çoğu zaman testi yürütecek veya onaylayacak kişiye gösterilir; ne test edildiği ancak ekran gerçekten göründüğü hâliyle sunulduğunda tartışılabilir. Yarım görünen bir mockup, tartışmayı testin kendisinden mockup'ın eksikliklerine kaydırır.

Bunun bilinen bir bedeli vardır ve kartı sunan kişi bunu bilmelidir: **bitmiş görünen bir tasarım, karşıdakinin yapısal itirazını bastırır.** İnsanlar tamamlanmış görünen bir ekrana "buradaki akış yanlış kurulmuş" demek yerine renk ve kelime düzeyinde yorum yapmaya eğilimlidir. Bu risk mockup'ı basitleştirerek değil, iki şeyle karşılanır:

- Değişen öğe halkayla işaretlenir ve halkanın etiketi ne değiştiğini yazar; böylece dikkat kozmetik ayrıntıya değil test edilen değişkene gider.
- Kartın metin sütunu (üç kutu) her zaman mockup'la birlikte sunulur; tartışılacak şey mockup değil, oradaki sorulardır.

`templates/scenario-card.html` içindeki `.r-*` bileşenleri (ürün satırı, form alanı, fiyat satırı, CTA, rozet, yıldız) bu seviyeyi üretmek için hazırdır; her kartta markup sıfırdan uydurulmaz.

## Mockup kuralları

- İki varyant arasında **yalnızca test edilen öğe** farklıdır. Ürün adı, fiyat, puan, rozet — hepsi birebir aynı kalır.
- Test edilen fark **kırmızı yuvarlak köşeli çerçeveyle** (kalınlık ~3px, radius ~12, hafif glow) vurgulanır. Çerçeve sadece değişen öğenin etrafına çizilir, tüm ekranı kaplamaz.
- **Çerçevenin etiketi olur.** Halkanın üstünde ne değiştiğini söyleyen kısa bir etiket bulunur (`.hl[data-note]`, ör. “kupon alanı katlandı”, “teslimat tarihi eklendi”). Etiketsiz halka okuyucuyu iki ekranı karşılaştırıp farkı kendi bulmaya zorlar; kartın işi bu farkı söylemektir. Etiket iki üç kelimeyi geçmez.
- Yeni bir öğe ekleniyorsa (B'de var, A'da yok) çerçeve B'deki yeni öğeye çizilir; A'ya çerçeve konmaz.
- **Bir öğe kaldırılıyorsa (A'da var, B'de yok) çerçeve A'daki öğeye çizilir ve B'de o alan gerçekten boş bırakılır.** "Bu öğe gösterilmez", "kaldırıldı" yazan kesikli bir yer tutucu konmaz — yer tutucu hem kalıcı bir kuralmış gibi okunur hem de varyantı yanlış gösterir: gerçek B'de o alan yoktur, altındaki içerik yukarı kayar. Bu kayma mockup'ta korunur, çünkü çoğu zaman testin faydasının bir parçasıdır (asıl içerik ekranın üst kısmına çıkar). Kaymanın fark edilmesi için mockup'ın **altına** tek satırlık bir not düşülür (`.shift-note`, ör. “kupon alanı kaldırıldı, alttaki içerik yukarı kaydı”); bu not ekranın içine yazılmaz.
- Mobil mockup: telefon çerçevesi içinde, durum çubuğu (saat + pil) ve alt navigasyon (Anasayfa/Keşfet/Favoriler/Sepet/Profil) ile.
- Web/masaüstü mockup: tarayıcı çerçevesi içinde — üst barda üç nokta ve adres çubuğu (şablondaki `.browser`/`.browser-bar`/`.browser-url`), beyaz gövde. Durum çubuğu ve alt navigasyon yalnızca mobil çerçeveye aittir, web kartında kullanılmaz.
- Metin dili ve para birimi kullanıcının sayfasını izler (kural 7 ve 15): İngilizce/USD bir sayfa Türkçe+TL'ye çevrilmez. Paylaşılmış sayfa yoksa (temsili örnek) Türkçe ve TL varsayılır. Tutarlar iki varyantta her durumda aynıdır.

## Tipografi

- Ana font: Inter (başlıklar Bold/Semi Bold, gövde Regular).
- Türkçe karakterler tam desteklenmeli; "Baslık", "İndrim" gibi karakter düşmeleri kabul edilmez.
- Tırnaklar kıvrık ("…" ve '), düz tırnak kullanılmaz.
