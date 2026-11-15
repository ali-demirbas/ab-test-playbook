# Archive format

Each stage file (`cart-checkout.md`, …) holds scenario blocks: a `## ` title, a fixed head of one-line fields, the Turkish body, and, once translated, an English body. A block ends at its `---` line. `scripts/validate_scenarios.py` checks everything below; this file holds no scenarios and the validator skips it.

### Head

Four lines in this order under the title (the title is a question), a blank line between each:

    Değişken: <one variable, at most 80 characters> · Fark: <değiştir | ekle | taşı | kaldır>
    Etiket: id=<id> · mercek=<lens> · düzey=<level> · sektör=<sector> · pazar=<market> · emek=<effort> · durum=<status> · tarih=<YYYY-MM>
    EN: <the English title, a question>
    EN-Variable: <the English variable>

`EN-Variable:` arrives with the full translation; every other line is required. The tag keys keep this order and every key is present.

| Key | Values | Meaning |
|---|---|---|
| `id` | `cc-001`, … | Permanent. The prefix names the file the block was first filed in and never changes, not even when the block moves. The next free id: `python3 scripts/validate_scenarios.py --next-id cart-checkout.md` |
| `mercek` | `Güven`, `Fiyat`, `Uygunluk`, `Zamanlama`, `Çaba`, `Netlik` | The objection the change answers (methodology: Trust, Price, Fit, Timing, Effort, Clarity) |
| `düzey` | element: `görsel`, `gezinme`, `bilgi`, `form`, `metin`, `güven`, `sosyal-kanıt`, `sürtünme`; structural: `teklif`, `fiyat`, `kişiselleştirme`, `akış`, `elde-tutma`, `onboarding` | What kind of change it is (below) |
| `sektör` | `genel`, `e-ticaret`, `moda`, `saas`, `b2b`, `finans`, `ilan`; one or two, comma-separated | Where the pattern applies; `genel` is any site or app |
| `pazar` | `TR`, `global` | `TR`: rests on a Turkey-specific practice or rule (card installments, the national ID number); `global`: no single-market assumption, a market note may still apply |
| `emek` | `düşük`, `orta`, `yüksek` | The record's `priority.inputs.effort`: copy, style or order; front-end work; backend, a native app release or an operational or commercial change |
| `durum` | `güncel`, `klasik` | `klasik`: a dated pattern kept for reference; suggested only when the user names it |
| `tarih` | `2026-11` | The month the block was last reviewed |

Levels. Element level changes how one thing on the page looks or reads: `görsel` visual weight, position, format; `gezinme` search, navigation, listing and discovery; `bilgi` information added or shown at the decision point (price and offer display included); `form` form and field design; `metin` copy and microcopy; `güven` trust and assurance signals; `sosyal-kanıt` reviews, testimonials, logos; `sürtünme` removing effort inside the same flow (defaults, saved data, shortcuts). Structural level changes the thing itself: `teklif` what is offered (threshold, trial length, a new offer); `fiyat` price point or package and plan structure; `kişiselleştirme` content that differs by visitor or segment; `akış` the steps, their order or a new path; `elde-tutma` what happens after the purchase or sign-up; `onboarding` first use and activation.

### Body

An intro paragraph (the concrete obstacle, the risk on each side, what stays equal in both arms, how the block differs from a sibling), then `**Test edilmesi gerekenler**`, `**Takip edilecek ana KPI’lar**` and `**Yapılmaması gerekenler**`, 3 to 6 items each; the validator's docstring lists the box rules. A `Sonraki test:` item, at most one, builds on this scenario's winning variant; asking where the winner should sit is not a follow-up. Block text never cites an internal rule number (“kural 6”); it states the rule.

### Notes under a block

`> **Pazar notu:** …` names a market dependency. `> **Güncellik notu (YYYY-MM):** …` records that the ground under a scenario shifted (a platform rule, a regulation, a pattern turned standard, the technology): what changed, then what to test instead. A stale block keeps its place with its note; it is not deleted (methodology: When the archive goes stale). The month is when the note was written.

### Deliberately out of scope

- **Cookie consent and other consent requests** (cookie banners, marketing permission, data-sharing consent). Their wording, button order, colors and defaults are never a test subject: raising acceptance is a dark pattern and the flow is regulated. The archive has no consent scenario on purpose; a scenario that sits next to a consent step leaves it identical in both arms.

### English

The archive is one source in two languages. The `EN:` title is the stable English name of the scenario: English searches, history and backlog rows match it, and it is never re-translated per turn. Tag values and `Fark` stay Turkish data; English output renders them through the tables above (`değiştir` change, `ekle` add, `taşı` move, `kaldır` remove).

The full translation adds `EN-Variable:` to the head and an English body at the end of the block, after a line holding only `### EN`:

- the intro paragraph, then `**What to test**`, `**KPIs to track**` and `**What not to do**`, each with as many items as its Turkish box, in the same order;
- test items keep the `Label: question?` shape, `Sonraki test:` becomes `Next test:`;
- the primary KPI is the glossary's English name (`kpi-glossary.md`, last column) and a guardrail says “must not”;
- notes are translated (`Pazar notu` → `Market note`, `Ölçüm notu` → `Measurement note`, `Güncellik notu` → `Freshness note`), and a reference to another scenario quotes its `EN:` title followed by “scenario”.

A Turkish turn reads a block up to `### EN`; an English turn reads the head and everything after it. Blocks with and without an English body are both valid. A translator works on one file, leaves the Turkish text untouched, writes curly quotes and apostrophes (’ “ ”), and runs `python3 scripts/validate_scenarios.py <file>` before handing back.

### Example

A complete block with its English body (shown indented; in a stage file it starts at the margin):

    ## Kargo eşiğini yükseltmek sepet ortalamasını artırır mı?

    Değişken: Ücretsiz kargo eşik tutarı · Fark: değiştir

    Etiket: id=cc-010 · mercek=Fiyat · düzey=teklif · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

    EN: Does raising the free-shipping threshold raise average order value?

    EN-Variable: Free-shipping threshold amount

    Ücretsiz kargo sınırı sepeti büyütmek için güçlü bir teşviktir, ancak eşik fazla yükselirse kullanıcıyı kaçırır. Dengenin nerede olduğu ölçülmelidir.

    **Test edilmesi gerekenler**
    - Eşik: 500, 750 ve 1.000 TL’de davranış nasıl değişiyor?
    - Sonraki test: Yeni eşik sabitken eşik bilgisinin ürün sayfasında mı sepette mi duyurulduğu ayrı bir testte sepet tutarını değiştiriyor mu?
    - Kampanya: İndirim döneminde eşiğe yaklaşma isteği artıyor mu?
    - Segment: Sadık müşteri ile yeni kullanıcı aynı tepkiyi mi veriyor?
    - Eşik altı davranış: Sepeti yeni eşiğin hemen altında kalan kullanıcılar ürün ekliyor mu, yoksa siparişi bırakıyor mu?

    **Takip edilecek ana KPI’lar**
    - Ziyaretçi Başına Gelir (RPV): Eşik artışı AOV’yi şişirirken toplam geliri düşürmüyor mu?
    - Ortalama Sepet Tutarı (AOV): Kullanıcılar eşiğe ulaşmak için daha çok ekliyor mu?
    - Dönüşüm Oranı (CR): Eşik değişimi satın almayı düşürüyor mu?
    - Ödeme Adımına Geçiş Oranı: Sepetten ödeme adımına geçiş artıyor mu?
    - Kargo Maliyeti: Birim başına kargo gideri marjı eritmemeli.

    **Yapılmaması gerekenler**
    - Eşik yükselişini, sepetteki ürünlerin kargo durumunu habersizce değiştirecek şekilde uygulamayın.
    - “Ücretsiz kargo” mesajını yanlış beklenti yaratacak şekilde kurmayın.
    - Eşiği aşırı yükseltmeyin; kullanıcıyı kaçırır.
    - Aynı testte eşik tutarı ile kalan tutar mesajını birlikte değiştirmeyin.
    - Aynı kullanıcıya farklı oturumda veya cihazda farklı eşik göstermeyin; tutarsız eşik güveni bozar.

    > Not: Bu senaryo, “Ücretsiz kargo çubuğu sepet tutarını artırıyor mu?” senaryosuyla ilişkilidir; o çubuğun varlığını, bu ise doğru eşik değerini test eder. İkisini aynı anda değiştirmeyin.

    > **Pazar notu:** Kargo maliyetinin sepete oranı ve tüketicinin ücretsiz kargo beklentisi pazara göre değişir; bir pazarda kabul gören eşik artışı, başka bir pazarda doğrudan terke dönüşebilir.

    ### EN

    A free-shipping threshold is a strong incentive to grow the cart, but set too high it drives the user away. Where the balance lies has to be measured.

    **What to test**
    - Threshold: How does behavior change at 500, 750 and 1,000 TL?
    - Next test: With the new threshold fixed, does announcing it on the product page rather than in the cart change cart value in a separate test?
    - Campaign: Does the urge to reach the threshold grow during a sale?
    - Segment: Do loyal customers and new users react the same way?
    - Below the threshold: Do users whose cart sits just under the new threshold add items, or abandon the order?

    **KPIs to track**
    - Revenue per Visitor (RPV): Does total revenue hold up while the higher threshold inflates AOV?
    - Average Order Value (AOV): Do users add more to reach the threshold?
    - Conversion Rate (CR): Does the threshold change lower purchases?
    - Proceed-to-Payment Rate: Does the move from cart to the payment step increase?
    - Shipping Cost: Shipping cost per unit must not erode the margin.

    **What not to do**
    - Don’t roll out the higher threshold in a way that silently changes the shipping status of items already in the cart.
    - Don’t word the “Free shipping” message so that it sets a false expectation.
    - Don’t raise the threshold too far; it drives users away.
    - Don’t change the threshold amount and the remaining-amount message in the same test.
    - Don’t show the same user a different threshold in another session or on another device; an inconsistent threshold breaks trust.

    > Note: This scenario is related to the “Does a free-shipping progress bar raise cart value?” scenario; that one tests whether the bar exists, this one tests the right threshold value. Don’t change both at once.

    > **Market note:** The ratio of shipping cost to cart value and shoppers’ free-shipping expectations vary by market; a threshold increase accepted in one market can turn straight into abandonment in another.
