# Kurulum, güncelleme ve sorun giderme

**Dil:** [English](install.md) · [Türkçe](install.tr.md)

Kısa hali [README](../README.tr.md) içinde: Claude Code’da iki komut ve görsel kontrol için isteğe bağlı tek komut. Bu sayfa geri kalan her şeyi taşır: diğer kurulum yolları, görsel kontrolün nasıl çalıştığı, güncelleme ve bir şey ters göründüğünde ne yapılacağı.

A/B Test Builder görünen addır. Plugin `ab-test-playbook` adıyla kurulur.

## Gerekenler

| Ne | Ne için gerekir | Kontrol komutu |
|---|---|---|
| Claude Code | Her şey | `claude --version` |
| Python 3.9 veya üstü | Her şey (yalnızca standart kütüphane, `pip install` gerektiren bir şey yok) | `python3 --version` |
| Node.js 18 veya üstü, Playwright ve Chromium | Yalnızca kartın son görsel kontrolü. O olmadan da her kartı alırsınız, ama görsel olarak kontrol edilmemiş bir önizleme olarak | `node --version` |

**Gereksinimler:** Claude Code ve PATH üzerinde `python3` 3.9 veya üstü. Script’ler yalnızca Python standart kütüphanesini kullanır; `pip install` gerektiren bir şey yok. Nihai kart için görsel kontrol de gerekir: `scripts/render_check.mjs`, Node ile Chromium’lu Playwright üzerinde çalışır (aşağıda Görsel kontrol). O olmadan yalnızca doğrulanmamış bir önizleme alırsınız, nihai kart asla.

## Claude Code (önerilen)

```
/plugin marketplace add ali-demirbas/ab-test-playbook
/plugin install ab-test-playbook@ab-test-playbook
```

A/B Test Builder görünen addır; plugin `ab-test-playbook` adıyla kurulur ve bütün komutlar bu adı kullanır.

Ya da klonlayıp yerel bir plugin olarak ekleyin:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git
claude --plugin-dir ./ab-test-playbook
```

## Diğer kurulum yolları

**Yalnızca skill’ler, sınırlı.** Skills CLI beş skill talimatını tek başına kopyalayabilir:

```bash
npx skills add ali-demirbas/ab-test-playbook --all
```

Bu yol her skill’in yalnızca `SKILL.md` dosyasını getirir. Bağlayıcı kurallar (`CLAUDE.md`), senaryo arşivi, script’ler ve denetim agent’ları gelmez. Her skill bunlara plugin kökü üzerinden ulaştığı için arşivden öneri, senaryo doğrulama ve kart üretimi çalışmaz. Motorun tamamı için yukarıdaki plugin kurulumunu kullanın.

[Gemini CLI](https://github.com/google-gemini/gemini-cli) mi kullanıyorsunuz? `.gemini/extensions/ab-test-playbook/` aynı skill’leri, kuralları ve denetim agent’larını taşır; aynı kaynak dosyalardan `scripts/build_gemini.py` ile üretilir:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git
cd ab-test-playbook/.gemini/extensions/ab-test-playbook && gemini extensions link .
```

**Codex.** Repoda bir Codex plugin manifesti (`.codex-plugin/plugin.json`) ve marketplace dosyası (`.agents/plugins/marketplace.json`) da var:

```bash
codex plugin marketplace add ali-demirbas/ab-test-playbook
```

Ardından bir Codex oturumunda `/plugins` açıp **ab-test-playbook**’u kurun. Codex beş skill’i kurallar, arşiv ve script’lerle birlikte kurar; iki denetim agent’ı Claude Code alt agent’larıdır ve bu yol Claude Code plugin’i kadar kapsamlı test edilmedi.

**claude.ai (skill yükleme).** Her skill, kuralların, senaryo arşivinin, şablonların ve script’lerin kendi kopyasını taşıyan bir ZIP olarak paketlenebilir:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git && cd ab-test-playbook
python3 scripts/build_skill_zips.py --out dist
```

Her `dist/<skill>.zip` dosyasını Özelleştir (Customize) > Skill’ler (Skills) > + > Skill oluştur (Create skill) > Skill yükle (Upload a skill) yoluyla yükleyin; kod çalıştırma Ayarlar (Settings) > Yetenekler (Capabilities) altında açık olmalı. `ab-test` diğer dördüne yönlendirdiği için beşini de yükleyin. claude.ai bir skill açıklamasını 200 karakterle sınırlar, bu yüzden ZIP’ler daha kısa, gözden geçirilmiş bir açıklama kullanır; talimatlar aynıdır. Orada headless Chromium olmadığı için kartlar, Görsel kontrol bölümünde anlatıldığı gibi UNVERIFIED etiketli önizleme olarak çıkar.

## Görsel kontrol (nihai kart için gerekli)

Bir kart ancak `scripts/render_check.mjs` onu Chromium’da çizdikten ve görsel incelemeci görüntüye baktıktan sonra nihai olur. Rehberin geri kalanı Python standart kütüphanesiyle çalışır; bu kısım Node.js 18 veya üstü ister. Playwright’ı bir kez, reponun dışına kurun:

```bash
npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright install chromium
```

`render_check.mjs`, `~/.abtest-visual/node_modules` klasörünü kendisi bulur. Linux’ta sistem kütüphaneleri için `install` sözcüğünden sonra `--with-deps` ekleyin. `NODE_PATH` yalnızca Playwright başka bir yerdeyse, `CHROMIUM_PATH=/yol/chrome-headless-shell` yalnızca kendi tarayıcı dosyanızı kullanacaksanız gerekir. Denemek için önce klonunuza geçin:

```bash
cd ab-test-playbook
node scripts/render_check.mjs --strict docs/demo/scenario-card.html
```

Son stderr satırı sonucu söyler:

| Çıkış | Sonuç | Anlamı |
|---|---|---|
| 0 | `VERIFIED` | Çizildi, hata yok |
| 1 | `VISUAL_CHECK_FAILED` | Çizildi, kartta düzeltilecek bir yerleşim hatası var |
| 2 | kullanım hatası | Bilinmeyen seçenek, kart yok ya da dosya bulunamadı |
| 3 | `VISUAL_CHECK_UNAVAILABLE` | Playwright veya Chromium yok, hiçbir şey ölçülmedi |

Çıkış 3’te incelemecinin kararı `UNVERIFIED` olur, hiçbir kart nihai olmaz: taslak, açıkça UNVERIFIED diye etiketlenmiş bir önizleme olarak gelir. Kontrol kurulunca aynı taslak kontrol edilip tamamlanır. `--shot` ve `--half`, kartın yanına `card-<ad>.png` ve `card-<ad>-800.png` yazar. Nihai üretim de kartın yanına `card-<ad>.png` yazar (`--no-png` bunu atlar).

## Güncelleme

```
/plugin marketplace update ab-test-playbook
/plugin update ab-test-playbook@ab-test-playbook
```

Güncellemeler yalnızca plugin’in sürüm numarası değişince gelir. `/plugin` kurulu sürümü gösterir; [CHANGELOG](../CHANGELOG.md)’dakinden geride kalıyorsa iki komutu da çalıştırıp Claude Code’u yeniden başlatın. Yerel bir klon `git pull` ile güncellenir.

**Eski bir Claude Code’da `claude plugin validate`.** Plugin önerisi (relevance) özelliğinden önceki sürümler (ör. 2.1.117), `.claude-plugin/marketplace.json` için `Unrecognized key: "relevance"` bildirir. Zararsızdır: bu anahtar yalnızca Claude Code’un plugin’i önermesini sağlar; ekleme, kurma ve güncelleme o sürümlerde de çalışır, güncel sürümler anahtarı doğrular.

## Sorun giderme

| Ne görüyorsunuz | Ne anlama geliyor | Ne yapmalı |
|---|---|---|
| Kart UNVERIFIED etiketli bir önizleme olarak geliyor | Görsel kontrol kurulu değil, yani hiçbir şey ölçülmedi. Senaryo ve incelemesi tamam; eksik olan yalnızca son görsel kontrol | [Görsel kontrol](#görsel-kontrol-nihai-kart-için-gerekli) başlığındaki tek seferlik Playwright komutunu çalıştırın. Aynı taslak sonra kontrol edilip tamamlanır |
| `render_check.mjs` çıktısında `VISUAL_CHECK_UNAVAILABLE` (çıkış 3) | Playwright ya da Chromium yok veya başlamadı | Aynı komut. Linux’ta `install` sözcüğünden sonra `--with-deps` ekleyin |
| `npx skills add` sonrası öneri, doğrulama ya da kart çalışmıyor | Bu yol yalnızca skill talimatlarını kopyalar | Bu sayfanın başındaki plugin kurulumunu kullanın |
| `/plugin update` yeni bir şey getirmiyor | Güncellemeler yalnızca sürüm numarası değişince gelir | İki güncelleme komutunu da çalıştırıp Claude Code’u yeniden başlatın |
| `claude plugin validate` çıktısında `Unrecognized key: "relevance"` | Eski bir Claude Code sürümü | Zararsız, [Güncelleme](#güncelleme) altındaki nota bakın |
| `python3: command not found` ya da bir script başlarken duruyor | PATH üzerinde Python 3.9 veya üstü yok | Güncel bir Python 3 kurup terminali yeniden açın |

Hâlâ takıldınız mı? [Bir issue açın](https://github.com/ali-demirbas/ab-test-playbook/issues) ve komutun yazdığı son satırı ekleyin.
