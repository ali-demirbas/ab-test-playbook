# Evals

Elle koşulan kabul testleri. Her dosya bir veya birkaç girdiyi tarif eder: girdi, beklenen davranış, düşme koşulları. Bir değişiklikten sonra hepsi elle koşulur; kriterlerden biri düşerse değişiklik gönderilmez.

| Eval | Akış |
|---|---|
| `01-suggest.md` | Arşivden öneri, 1-5 güçlü aday, ICE sıralama, ön kapı soruları; gönüllü trafikte fizibilite notu; pazara bağlı adayda tek soru |
| `02-design.md` | Yeni senaryo, tek değişken, sayısal eşikli guardrail, doğrulanmış ön kayıt bloğu; A/A dalı; kaybın yeri belli değilken kırılım maddesi |
| `03-audit.md` | Confound'lu varyant çifti; dosyadan gelen kusurlu plan (vekil metrik, farklı payda, eşiksiz ve ters yönlü guardrail, segment seçme); korumayı ve düzenlenen gösterimi test konusu yapan plan |
| `04-results.md` | Anlamlılık, örneklem ve süre, hatalı girdi; SRM'de durma; nadir olayda Fisher; sürekli metrik ve CUPED; belirsiz MDE; A/A sonucu |
| `05-cross-cutting.md` | Tur başına tek soru ve turu tutan problem sorusu, dark pattern reddi, prompt injection'ın alıntılanması |
| `06-card.md` | Mobil web sayfasında sahte sekme çubuğu yok; ekran görüntüsündeki kişisel veri karta taşınmaz |
| `07-regulated-flow.md` | Sigorta ve emeklilik ekranları: turu tutan problem sorusu, iki durumlu düzenleme kapısı, `Pre-start gates` satırı, tutar/sözleşme numarası/grafik maskeleme, `read_after_days` ile geciken guardrail, geçti/kaldı erişilebilirlik kontrolü |
| `08-insisted-weak.md` | Kullanıcının ısrarla istediği zayıf test: reddedilmez, zayıflık yazılır, “Stronger alternative:” notu eklenir |
| `09-results-prereg.md` | Ön kayıt bloğuyla sonuç okuma (alfa, yön, geciken pencere, kontrol teyidi, geçici kazanan); anlamlı kaybeden; belirsiz guardrail ve gereken örneklem |
| `10-english.md` | İngilizce konuşma: çıktı ve kart dili, `--lang en` yolu, pazarın dilden ayrı okunması |

İstatistik motoru, validator'lar ve kart üreticisi ayrıca otomatik test edilir: `python3 -m unittest discover -s tests` (veya `python3 -m pytest tests -q`). Script seviyesindeki sınır durumları (sıfır ziyaretçi, dönüşüm > ziyaretçi, geçersiz MDE vb.) orada doğrulanır; bu evaller skill'lerin davranışını sınar.

## Koşu kaydı

Evaller elle koşulur; her sürümden önce koşulur ve sonucu buraya yazılır. Kayıt yoksa o sürüm için evallerin koşulduğu varsayılmaz.

| Sürüm | Tarih | Koşan | Geçen / toplam girdi | Not |
|---|---|---|---|---|
| 2.2.0 | (bekliyor) | (bekliyor) | (bekliyor) | 07-10 bu sürümde eklendi; yayından önce bütün dosyalar koşulur |
