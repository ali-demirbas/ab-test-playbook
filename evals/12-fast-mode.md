# Eval 12: hızlı kip

Hızlı kip, kural 17’nin tek istisnasıdır: aynı senaryolar yalnızca doğrulayıcıdan geçer, denetçiler çalışmaz, kartlar “Hızlı taslak” etiketli önizleme olarak gelir; kullanıcı “tamamla” deyince iki inceleme yapılır ve nihai kartlar yazılır.

**Girdi A (tetikleyici söz):** Kullanıcı sepet sayfasının ekran görüntüsünü paylaşır ve yazar: “Açık kupon kutusu yüzünden kod aramaya gidiyorlar. Hızlı bir taslak yeter, sonra bakarız.”

**Beklenen davranış:**
1. Yönlendirme `design` olur, hızlı kipte (router: “hızlı”, “taslak”, “quick”, “fast”, “draft” istenen çıktıyı niteliyor). Problem söylendiği için problem sorusu sorulmaz.
2. Senaryo sayısı her zamanki kuraldır (en fazla üç güçlü aday); kayıtlar tek çağrıda `validate_scenario_json.py` ile doğrulanır ve hatasız geçer.
3. scenario-critic ve mockup-reviewer çağrılmaz, `render_check.mjs` çalışmaz. Her kayıt için `build_card.py --quick … --out abtest-card-<slug>.draft.html` tek çağrıyla kurulur; dosyada “Hızlı taslak · incelenmedi” bandı ve `content="quick-draft"` vardır, manifest yazılmaz.
4. Sohbet her zamanki çıktıdır (senaryo başına beş satır, dosya adları `.draft.html`), listeden sonra bir satır: “Hızlı taslak: kartlar ve kayıtlar henüz incelenmedi. “Tamamla” dersen iki incelemeyi yapıp nihai kartları hazırlarım.” Bu satır soru değildir; turun tek sorusu ayrıca sorulabilir. Hiçbir satır taslağa “nihai”, “kontrol edildi” ya da “incelendi” demez.

**Düşme koşulları:**
- Hızlı kipte denetçilerin çağrılması ya da kartların her zamanki incelemeli yoldan kurulması (süre kazancı yok).
- Hızlı taslağın etiketsiz verilmesi, nihai diye anılması ya da `review` alanına damga yazılması.
- Doğrulayıcının atlanması ya da reddettiği kaydın kartının kurulması.

**Girdi B (tamamla):** Girdi A’nın ardından kullanıcı “tamamla” yazar.

**Beklenen davranış:**
1. Aynı kayıtlar tam teslim hattından geçer: scenario-critic tek turda bütün kayıtları inceler; `[fixable]` satırları ana oturum uygular, damga geçerli kalır; ardından `--draft`, `render_check.mjs`, mockup-reviewer ve nihai ya da koşullu kurulum.
2. İncelenen taslak hızlı taslağın yerine aynı yola yazılır; nihai kart `abtest-card-<slug>.html` olur. Problem sorusu yeniden sorulmaz.
3. Sohbet incelenen kartlar için her zamanki çıktıyı verir; eleştirmenin esasen değiştirdiği ya da düşürdüğü bir kayıt tek satırla söylenir.

**Düşme koşulları:**
- Hızlı taslağın `--stamp` ile damgalanmaya çalışılması ya da elle nihai karta çevrilmesi.
- Tamamla sonrası bir kartın denetçilerden geçmeden nihai diye teslim edilmesi.

**Girdi C (tetikleyici olmayan kullanım):** “Taslak test planımı denetler misin?” ve plan yapıştırılmış.

**Beklenen davranış:**
1. Yönlendirme `audit` olur: “taslak” kullanıcının kendi malzemesini niteliyor, istenen çıktıyı değil; hızlı kip açılmaz.

**Düşme koşulları:**
- Denetim isteğinin hızlı kip öneri turuna çevrilmesi.
