# Before the test starts

Given only when the user asks for a reusable pre-start list (`ab-test-audit` → Output format, On request only), in the user's language, as written; never unasked and never appended to an audit. It holds no statistic, sample size, duration or decision rule (CLAUDE.md rule 5).

## Test başlamadan önce

1. B’de tek fark var ve A ile B arasındaki fark tek cümleyle yazılı; geri kalan her şey iki kolda aynı.
2. Hipotez yazılı: bu adımda gözlenen engel, B’nin onu neden değiştireceği, iki sonuçta ne öğrenileceği.
3. Birincil KPI tek ve önceden seçili; adı, paydası ve geciken bir sonuçsa penceresi yazılı, payda iki kolda aynı noktadan sayılıyor.
4. Gösterim noktası belli: akordeon, sekme, modal ya da ekran altındaki bir değişiklikte kullanıcı öğe gerçekten göründüğünde sayılıyor, iki kolda aynı yerde kaydediliyor.
5. Hedefleme ile ölçüm kapsamı aynı: B yalnız bir cihazda, segmentte ya da ülkede değişiyorsa KPI’lar yalnız o kullanıcıları sayıyor.
6. Guardrail bağımsız bir zararı ölçüyor (birincilin tümleyeni değil); paydası, yönü ve geciken sonuçta penceresi adında yazılı.
7. B yeni bir dokunma hedefi, alan, modal ya da hareketli öğe ekliyorsa erişilebilirlik kontrolü trafikten önce geçti: dokunma hedefi en az 44×44 pt, kontrast en az 4,5:1, klavyeyle kullanım, ekran okuyucu adı.
8. Uyum ve etik: düzenlenen bir akışta B’nin tam metni onaylı; dark pattern, gerçek veriye dayanmayan aciliyet ya da zayıflatılmış koruma yok.
9. Atama bir kimliğe bağlı ve girişte ya da cihaz değişiminde kol değişmiyor; atama ve sonuç ayrı kaydediliyor, iki kol her olayı aynı biçimde kaydediyor.
10. Aynı ekranda başka test yok ya da trafik karşılıklı dışlanmış; test boyunca sayfada fiyat, kampanya ya da metin değişikliği yok; kırılımlar (en az cihaz ve yeni / dönen kullanıcı) önceden yazılı.

## Before the test starts (English)

1. B has one difference, stated in one sentence; everything else is the same in both arms.
2. A hypothesis is written: the obstacle observed at this step, why B changes it, what each outcome would teach.
3. One primary KPI, chosen in advance, with its name, its denominator and, for a lagging outcome, its window; the denominator counts from the same point in both arms.
4. The exposure point is set: for a change in an accordion, tab, modal or below the first view, users are counted when the element is actually shown, logged at the same point in both arms.
5. Targeting and measurement match: when B changes only on one device, segment or country, the KPIs count only those users.
6. The guardrail measures an independent harm (never the primary's complement), with its denominator, its direction and, for a lagging outcome, its window in its name.
7. When B adds a tap target, a field, a modal or a moving element, the accessibility check has passed before traffic: a target of at least 44×44 pt, contrast of at least 4.5:1, keyboard operation, a screen-reader name.
8. Compliance and ethics: inside a regulated flow, B's exact copy is signed off; no dark pattern, no urgency without real data, no weakened protection.
9. Assignment is keyed on one identity and doesn't switch arms at login or on another device; assignment and outcome are logged separately, and both arms log every event the same way.
10. No other test runs on the same screen, or traffic is mutually exclusive; no price, campaign or copy change on the page during the test; the breakdowns (at least device and new versus returning) are named in advance.
