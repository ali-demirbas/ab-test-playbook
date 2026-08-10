# Evals

Elle koşulan kabul testleri. Her dosya bir akışı tarif eder: girdi, beklenen davranış, geçme kriterleri. Bir değişiklikten sonra dördü de elle koşulur; kriterlerden biri düşerse değişiklik gönderilmez.

| Eval | Akış |
|---|---|
| `01-suggest.md` | Arşivden öneri + ICE sıralama + ön kapı soruları |
| `02-design.md` | Yeni senaryo üretimi + tek değişken + guardrail zorunluluğu |
| `03-audit.md` | Confound'lu varyant çiftini yakalama |
| `04-results.md` | Sonuç yorumlama + örneklem hesabı + hatalı girdi davranışı |

İstatistik motoru ayrıca otomatik test edilir: `python3 tests/test_analyze_results.py` — sınır durumları (sıfır ziyaretçi, dönüşüm > ziyaretçi, geçersiz MDE vb.) script seviyesinde bu dosyayla doğrulanır.
