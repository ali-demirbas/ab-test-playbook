# Evals

Elle koşulan kabul testleri. Her dosya bir veya birkaç girdiyi tarif eder: girdi, beklenen davranış, düşme koşulları. Bir değişiklikten sonra hepsi elle koşulur; kriterlerden biri düşerse değişiklik gönderilmez.

| Eval | Akış |
|---|---|
| `01-suggest.md` | Arşivden öneri, en fazla 3 güçlü aday, gerekçeli öncelik sıralaması, ön kapı soruları; gönüllü verilen trafiğin hesaba çevrilmemesi; pazara bağlı adayda tek soru; kısa kayıt: arşivin `grep` ve kısa listeli bloklarla okunması, sohbette öneri başına dört satır (başlık, etiket, `Neden:`, kart dosyası); açık isteklerin istendiği sırayla önce gelmesi ve doğrudan çağrının tarif edilen sayfayla `suggest`’te kalması |
| `02-design.md` | Yeni senaryo kaydı, tek değişken, paydalı ve bağımsız guardrail, doğrulanmış senaryo JSON’u, yalnızca istenince yazılan kurulum notları ve `Başlamadan önce:` satırı; kapsam dışı araç doğrulama isteği; kaybın yeri belli değilken kırılım maddesi; kupon örneğinde gelir kazancının kullanıcı zararını gizlememesi (kupon guardrail’i, değişmezler, erişilebilirlik ölçütleri) |
| `03-audit.md` | Confound’lu varyant çifti; dosyadan gelen kusurlu plan (vekil metrik, farklı payda, ters yönlü ve tümleyen guardrail, önceden adlandırılmamış segmentler); korumayı ve düzenlenen gösterimi test konusu yapan plan |
| `05-cross-cutting.md` | Tur başına tek soru ve turu tutan problem sorusu, dark pattern reddi, prompt injection’ın alıntılanması, istek üzerine ayrıntı (üç kutu yalnızca istenince ve yalnızca sohbette; `detail` kartta gösterilmez); arşiv kanıtının test edilmiş gibi sunulmaması; kartın yalnızca iki incelemeden ve iki damgadan sonra teslim edilmesi |
| `06-card.md` | Mobil web sayfasında sahte sekme çubuğu yok; ekran görüntüsündeki kişisel veri karta taşınmaz; halkanın içindeki ikinci değişikliği kod değil mockup-reviewer yakalar; B’ye eklenen etkileşimli öğe ölçütlü erişilebilirlik uyarısı taşır; kartta başlık, iki mockup ve halka dışında bir şey olmaz |
| `07-regulated-flow.md` | Sigorta ve emeklilik ekranları: turu tutan problem sorusu, iki durumlu düzenleme kapısı, `Pre-start gates` satırı, tutar/sözleşme numarası/grafik maskeleme, takip penceresi KPI adında olan geciken guardrail, geçti/kaldı erişilebilirlik kontrolü |
| `08-insisted-weak.md` | Kullanıcının ısrarla istediği zayıf test: reddedilmez, zayıflık yazılır, sohbette “Daha güçlü alternatif:” satırı eklenir |
| `10-english.md` | İngilizce konuşma: çıktı ve kart dili, pazarın dilden ayrı okunması, sonuç sorusuna İngilizce kapsam dışı cümlesi |
| `11-final-audit.md` | Son denetimde yeniden koşulan dokuz senaryo: bağlantı arkasında kupon, taşıma olarak çizilen sabit buton, ücretsiz kargo çubuğu, koşullu yıllık plan varsayılanı (normalize değer ile tahsilat ayrı), “Atla” butonu, düzeltilebilir ölçütlerle korunan yumuşak kayıt duvarı, koşullu sigorta adım adları, koşullu TC gerekçe satırı, koşullu ve taşıma olarak çizilen telefon alanı |

Numaralar korunmuştur: 3.0.0’da sonuç analizi kapsamdan çıktığı için 04 ve 09 silindi, diğer dosyaların adı değişmedi.

Validator’lar, kart üreticisi, render kontrolü ve giriş taraması ayrıca otomatik test edilir: `python3 -m unittest discover -s tests` (veya `python3 -m pytest tests -q`). Script seviyesindeki sınır durumları orada doğrulanır; bu evaller skill’lerin davranışını sınar.

## Koşu kaydı

Evaller elle koşulur; her sürümden önce koşulur ve sonucu buraya yazılır. Kayıt yoksa o sürüm için evallerin koşulduğu varsayılmaz.

| Sürüm | Tarih | Koşan | Geçen / toplam girdi | Not |
|---|---|---|---|---|
| 2.2.0 | (bekliyor) | (bekliyor) | (bekliyor) | 07-10 bu sürümde eklendi; yayından önce bütün dosyalar koşulur |
| 3.0.0 | (bekliyor) | (bekliyor) | (bekliyor) | 04 ve 09 silindi; 01, 02, 03, 07, 08, 10 kapsam daralmasına göre, bütün dosyalar kısa senaryo kaydına göre güncellendi; 01’e kısa kayıt, 05’e istek üzerine ayrıntı girdisi eklendi; kalite kapıları için 02’ye D, 05’e E ve F, 06’ya C ve D girdileri eklendi; son denetimde sohbet biçimi (`Neden:` satırı, `Başlamadan önce:`, `Koşullu (<n>):`), koşullu öneriler, taşıma çizimi ve iddia kuralı için 01, 02, 05, 06, 07, 08, 10 güncellendi, 06’ya F girdisi ve 11 eklendi |
