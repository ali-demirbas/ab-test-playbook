# Evals

Elle koşulan kabul testleri. Her dosya bir veya birkaç girdiyi tarif eder: girdi, beklenen davranış, düşme koşulları. Bir değişiklikten sonra hepsi elle koşulur; kriterlerden biri düşerse değişiklik gönderilmez.

| Eval | Akış |
|---|---|
| `01-suggest.md` | Arşivden öneri, 1-5 güçlü aday, ICE sıralama, ön kapı soruları; gönüllü trafikte fizibilite notu; pazara bağlı adayda tek soru |
| `02-design.md` | Yeni senaryo, tek değişken, sayısal eşikli guardrail, doğrulanmış ön kayıt bloğu; A/A dalı; kaybın yeri belli değilken kırılım maddesi |
| `03-audit.md` | Confound'lu varyant çifti; dosyadan gelen kusurlu plan (vekil metrik, farklı payda, eşiksiz guardrail, segment seçme) |
| `04-results.md` | Anlamlılık, örneklem ve süre, hatalı girdi; SRM'de durma; nadir olayda Fisher; sürekli metrik ve CUPED |
| `05-cross-cutting.md` | Tur başına tek soru, dark pattern reddi, prompt injection'ın alıntılanması |
| `06-card.md` | Mobil web sayfasında sahte sekme çubuğu yok; ekran görüntüsündeki kişisel veri karta taşınmaz |

İstatistik motoru, validator'lar ve kart üreticisi ayrıca otomatik test edilir: `python3 -m unittest discover -s tests` (veya `python3 -m pytest tests -q`). Script seviyesindeki sınır durumları (sıfır ziyaretçi, dönüşüm > ziyaretçi, geçersiz MDE vb.) orada doğrulanır; bu evaller skill'lerin davranışını sınar.
