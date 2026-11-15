#!/usr/bin/env python3
"""User-facing messages of build_card.py (Turkish and English).

Kept in their own module so build_card.py stays under the plugin directory's
per-file size limit. build_card.py imports every *_MSG table from here.
"""

# card.difference no longer overrides the record's difference: the critic
# reviewed the record's, and a card drawn as another type (a move drawn as an
# added or a removed element) shows the user a different test than the one
# reviewed. The hint says how to draw the record's type.
DIFF_MSG = {
    "mismatch": ("card.difference '{card}' differs from the record's difference '{record}': the card would misrepresent "
                 "the variable the record states and the critic reviewed, so it is refused. The card draws the record's "
                 "difference: drop card.difference or set it to '{record}'. {hint}",
                 "card.difference '{card}', kaydın difference değeri '{record}' ile aynı değil: kart, kaydın söylediği ve "
                 "eleştirmenin incelediği değişkeni yanlış gösterir, bu yüzden reddedilir. Kart kaydın farkını çizer: "
                 "card.difference alanını kaldırın ya da '{record}' yapın. {hint}"),
    "move": ("To draw a move: ring the same element in both arms, with identical content and a label that says "
             "where it is in that arm, at its old place in A and its new place in B. A move below the first view or "
             "to a pinned bar: both arms split the screen with <div class=\"r-fold\"></div> at the same place; A "
             "rings the element in the continuation, B rings it in the first view, a pinned element inside "
             "<div class=\"r-sticky\"></div> before the fold. A move to a later screen: both arms split the screen "
             "with <div class=\"r-stage-break\"></div> (card.stage_captions names the two stages), B rings the "
             "element in the second stage.",
             "Taşıma şöyle çizilir: aynı öğeye iki kolda da aynı içerikle halka çizin, etiket öğenin o koldaki yerini "
             "söyler; A'da eski yerinde, B'de yeni yerinde. İlk ekranın altına ya da sabit bara taşıma: iki kol da "
             "ekranı aynı yerde <div class=\"r-fold\"></div> ile böler; A öğeyi devamında, B ilk ekranda halkalar, "
             "sabit öğe kıvrımdan önce <div class=\"r-sticky\"></div> içinde. Sonraki ekrana taşıma: iki kol da "
             "ekranı <div class=\"r-stage-break\"></div> ile böler (card.stage_captions iki aşamayı adlandırır), B "
             "öğeyi ikinci aşamada halkalar."),
    "add": ("To draw an addition: ring the new element in Variant B only; A has no ring.",
            "Ekleme şöyle çizilir: halka yalnızca B'deki yeni öğede; A'da halka yok."),
    "remove": ("To draw a removal: ring the element in Variant A only (labelled); B is genuinely empty in its place.",
               "Kaldırma şöyle çizilir: halka yalnızca A'daki öğede (etiketli); B'de o alan gerçekten boş."),
    "change": ("To draw a change: ring the changed element in Variant B (ringing its old state in A is allowed).",
               "Değiştirme şöyle çizilir: B'de değişen öğeye halka çizin (A'daki eski hâline halka çizmek serbest)."),
}

NO_CARD_MSG = ("the record has no `card` object. It can be a valid record as it is (validate_scenario_json.py "
               "checks it without one), but a card needs card.variant_a and card.variant_b (and a difference, the "
               "card's or the record's): add `card` at render time",
               "kayıtta `card` nesnesi yok. Kayıt bu hâliyle geçerli olabilir (validate_scenario_json.py onu kartsız "
               "da denetler), ama kart için card.variant_a ve card.variant_b (ve kartın ya da kaydın difference "
               "değeri) gerekir: `card` nesnesini çizim aşamasında ekleyin")

MARKUP_MSG = {
    "not_string": ("must be a string of markup, got {got}",
                   "işaretleme metni olmalı, gelen {got}"),
    "decl": ("comments, declarations and processing instructions (<!-- -->, <!…>, <?…>) are not allowed in a mockup",
             "mockup içinde yoruma, bildirime ve işlem yönergesine (<!-- -->, <!…>, <?…>) izin yok"),
    "control": ("control character {ch} is not allowed in a mockup",
                "mockup içinde {ch} denetim karakterine izin yok"),
    "malformed": ("malformed tag near {near}: write <tag attr=\"value\">, every attribute value in double quotes "
                  "and attributes separated by a space, and close what you open (a literal < in text is &lt;)",
                  "bozuk etiket, {near} yakınında: etiketi <tag attr=\"değer\"> biçiminde, her nitelik değerini çift "
                  "tırnak içinde ve nitelikleri boşlukla ayırarak yazın, açtığınızı kapatın (metindeki < için &lt;)"),
    "tag": ("tag <{tag}> is not allowed in a mockup (allowed: {allowed})",
            "<{tag}> etiketine mockup içinde izin yok (izinli: {allowed})"),
    "attr": ("attribute {attr}= on <{tag}> is not allowed (allowed: {allowed})",
             "<{tag}> üzerindeki {attr}= niteliğine izin yok (izinli: {allowed})"),
    "handler": ("event-handler attribute {attr}= on <{tag}> is not allowed: a card is static HTML",
                "<{tag}> üzerindeki {attr}= olay işleyicisine izin yok: kart durağan HTML’dir"),
    "url_attr": ("attribute {attr}= on <{tag}> is not allowed: a mockup carries no link, source or form target",
                 "<{tag}> üzerindeki {attr}= niteliğine izin yok: mockup bağlantı, kaynak ya da form hedefi taşımaz"),
    "dup_attr": ("attribute {attr}= is written twice on <{tag}>",
                 "{attr}= niteliği <{tag}> üzerinde iki kez yazılmış"),
    "style": ("style on <{tag}> contains a forbidden CSS construct “{what}” (no url(), image-set(), expression(), "
              "@import, javascript:, behavior:, -moz-binding, position:fixed, comments, backslash escapes or < > {{ }})",
              "<{tag}> üzerindeki style yasak bir CSS yapısı içeriyor: “{what}” (url(), image-set(), expression(), "
              "@import, javascript:, behavior:, -moz-binding, position:fixed, yorum, ters eğik çizgi kaçışı ve "
              "< > {{ }} kullanılamaz)"),
    "self_closing": ("<{tag}/> is not a void element; write <{tag}></{tag}>",
                     "<{tag}/> kendiliğinden kapanan bir etiket değil; <{tag}></{tag}> yazın"),
    "void_end": ("</{tag}> closes a void element; write <{tag}> only",
                 "</{tag}> kapanışı olmayan bir etiketi kapatıyor; yalnızca <{tag}> yazın"),
    "unbalanced": ("unbalanced markup: </{tag}> closes <{open}>",
                   "dengesiz işaretleme: </{tag}>, <{open}> etiketini kapatıyor"),
    "stray_end": ("unbalanced markup: </{tag}> has no opening tag (it would close the screen itself)",
                  "dengesiz işaretleme: </{tag}> için açılış etiketi yok (ekranın kendisini kapatır)"),
    "unclosed": ("unbalanced markup: <{tag}> is never closed",
                 "dengesiz işaretleme: <{tag}> hiç kapatılmamış"),
    "p_block": ("<{tag}> inside <p>: a browser closes the paragraph first; use a <div> instead of the <p>",
                "<p> içinde <{tag}>: tarayıcı önce paragrafı kapatır; <p> yerine <div> kullanın"),
    "li_parent": ("<li> must sit directly inside <ul> or <ol>",
                  "<li> doğrudan <ul> ya da <ol> içinde olmalı"),
    "disagree": ("internal check failed: the markup reads differently to two parsers; simplify it",
                 "iç denetim tutmadı: işaretleme iki ayrıştırıcıda farklı okunuyor; sadeleştirin"),
}

RING_MSG = {
    "add_b": ("difference 'add': ring the new element in Variant B (found no .hl in B)",
              "fark 'ekle': B'deki yeni öğeye halka çizin (B'de .hl yok)"),
    "add_a": ("difference 'add': the element does not exist in Variant A, so A carries no ring (found {a} .hl in A)",
              "fark 'ekle': öğe A'da yok, A'da halka olmaz (A'da {a} .hl var)"),
    "remove_a": ("difference 'remove': ring the element in Variant A (found no .hl in A)",
                 "fark 'kaldır': A'daki öğeye halka çizin (A'da .hl yok)"),
    "remove_b": ("difference 'remove': Variant B leaves that area genuinely empty, so B carries no ring (found {b} .hl in B)",
                 "fark 'kaldır': B'de o alan gerçekten boş kalır, B'de halka olmaz (B'de {b} .hl var)"),
    "move": ("difference 'move': ring the element in both variants (found {a} in A, {b} in B)",
             "fark 'taşı': öğeye iki varyantta da halka çizin (A'da {a}, B'de {b} var)"),
    "change": ("difference 'change': ring the changed element in Variant B (found no .hl in B)",
               "fark 'değiştir': B'deki değişen öğeye halka çizin (B'de .hl yok)"),
}

CARD_MSG = {
    "ring_label": ("ring in {v} has no data-note label (two to four words saying what changed)",
                   "{v} varyantındaki halkanın data-note etiketi yok (neyin değiştiğini söyleyen iki ila dört kelime)"),
    "ring_box": ("ring in {v} carries inline {prop}: a ring must not push content; give the spacing to the "
                 "children, and if the label collides use data-pos=\"below\" or card.note_pos",
                 "{v} varyantındaki halka satır içi {prop} taşıyor: halka içeriği itmemeli; boşluğu çocuk öğelere "
                 "verin, etiket çakışıyorsa data-pos=\"below\" ya da card.note_pos kullanın"),
    "class": ("variant_{vl}: class \"{cls}\" is not a template component; it would render unstyled "
              "(components are listed in the template's comment)",
              "variant_{vl}: \"{cls}\" sınıfı şablonda tanımlı bir bileşen değil; biçimsiz çizilir "
              "(bileşenler şablonun yorumunda listeli)"),
    "ring_style": ("ring in {v} carries inline {prop}: the ring wrapper adds no styling of its own "
                   "(mockup-style.md); put it on the element inside",
                   "{v} varyantındaki halka satır içi {prop} taşıyor: halka sarmalayıcısı kendi biçimini eklemez "
                   "(mockup-style.md); içteki öğeye yazın"),
    "label_long": ("ring label in {v} is {n} words (“{note}”); keep it to two to four",
                   "{v} varyantındaki halka etiketi {n} kelime (“{note}”); iki ila dört kelimede tutun"),
    "label_case": ("ring label in {v} starts with a lowercase letter (“{note}”); a Turkish label starts with a "
                   "capital letter",
                   "{v} varyantındaki halka etiketi küçük harfle başlıyor (“{note}”); Türkçe etiket büyük harfle "
                   "başlar"),
    "move_content": ("difference 'move': the ringed element's content differs between A and B ({what}); only its "
                     "position may change, a changed copy, size or style is a second variable",
                     "fark 'taşı': halkalı öğenin içeriği A ile B arasında farklı ({what}); yalnızca yeri "
                     "değişebilir, değişen metin, boyut ya da biçim ikinci bir değişkendir"),
    "outside": ("A and B differ outside any ring ({where}: {na} node(s) in A, {nb} in B), e.g. {what}; a second "
                "variable is refused, and a linked consequence of the variable belongs inside the ring (one ring "
                "around the group, its label naming the consequence). Drawn from one card.screen with one "
                "card.change, the arms can't differ elsewhere: {{\"op\": \"edit\", \"target\": \"<id>\", "
                "\"set\": {{\"cta\": \"<B's text>\"}}, \"label\": \"<two to four words>\"}}; a consequence "
                "goes in card.soft",
                "A ile B halkanın dışında da farklı ({where}: A'da {na}, B'de {nb} düğüm), ör. {what}; ikinci bir "
                "değişken reddedilir, değişkenin bağlı bir sonucu halkanın içine alınır (grubun etrafında tek halka, "
                "etiketi sonucu adlandırır). Tek card.screen ve tek card.change ile çizilen kollar başka yerde "
                "farklılaşamaz: {{\"op\": \"edit\", \"target\": \"<kimlik>\", \"set\": {{\"cta\": "
                "\"<B'nin metni>\"}}, \"label\": \"<iki ila dört kelime>\"}}; bir sonuç card.soft'a yazılır"),
    "colour_b": ("inline colour only in Variant B, inside the ring: {vals}; a colour that exists only in B is a "
                 "second variable unless colour is what the test changes (the manifest lists it for the reviewer)",
                 "yalnızca B varyantında, halkanın içinde geçen satır içi renk: {vals}; yalnızca B'de olan renk, "
                 "test rengi değiştirmiyorsa ikinci bir değişkendir (manifest gözden geçiren için listeler)"),
    "hide": ("variant_{vl}: inline “{decl}” on <{tag}> can hide, clip, displace or reorder what a reader sees; "
             "{why}. Positioning, clipping and stacking belong to the template's components, never to a mockup's "
             "inline style: draw the element where it is, as it looks",
             "variant_{vl}: <{tag}> üzerindeki satır içi “{decl}”, okurun gördüğünü gizleyebilir, kırpabilir, "
             "kaydırabilir ya da yeniden sıralayabilir; {why_tr}. Konumlandırma, kırpma ve katmanlama şablonun "
             "bileşenlerine aittir, mockup'ın satır içi stiline asla: öğeyi olduğu yerde, göründüğü gibi çizin"),
    "ring_empty": ("ring “{note}” in {v} contains nothing visible (no text with a visible character and no drawn "
                   "component): a ring around nothing shows no variable",
                   "{v} varyantındaki “{note}” halkası görünür hiçbir şey içermiyor (görünür karakterli metin ya da "
                   "çizilmiş bileşen yok): hiçbir şeyin etrafındaki halka bir değişken göstermez"),
    "no_change": ("A and B render the same (only the ring and its label differ): the card would claim a difference "
                  "that doesn't exist. Draw the change itself in B (a move: the element at another place)",
                  "A ile B aynı çiziliyor (yalnızca halka ve etiketi farklı): kart olmayan bir farkı göstermiş olur. "
                  "Değişikliğin kendisini B'de çizin (taşımada öğe başka bir yerde)"),
    "rings_many": ("{n} rings in {v}: one change applied to {n} elements gets one ring around the group; {n} "
                   "independent rings read as {n} variables, and a linked consequence takes .hl-soft",
                   "{v} varyantında {n} halka var: {n} öğeye uygulanan tek değişiklik grubun etrafında tek halka "
                   "alır; {n} bağımsız halka {n} değişken gibi okunur, bağlı sonuç .hl-soft alır"),
    "ring_whole": ("the ring in {v} wraps {pct}% of the screen's text: a ring around (almost) the whole screen rings a "
                   "region, not the variable; ring the element that changes",
                   "{v} varyantındaki halka ekran metninin %{pct} kadarını sarıyor: ekranın (neredeyse) tamamını "
                   "saran halka değişkeni değil bir bölgeyi gösterir; değişen öğeyi halkalayın"),
    "soft_far": ("{v}: the .hl-soft “{note}” is not next to the ring: a linked consequence sits beside the variable "
                 "(a sibling of the ring or of the block that holds it), not elsewhere on the screen",
                 "{v}: “{note}” .hl-soft halkası halkanın yanında değil: bağlı sonuç değişkenin yanında durur "
                 "(halkanın ya da onu taşıyan bloğun kardeşi), ekranın başka bir yerinde değil"),
    "colour_b_outside": ("inline colour only in Variant B on an element outside the ring: {vals}; a colour change "
                         "outside the ring is a second variable, whatever the test changes",
                         "yalnızca B varyantında, halkanın dışındaki bir öğede geçen satır içi renk: {vals}; "
                         "halkanın dışındaki renk değişikliği, test neyi değiştirirse değiştirsin ikinci bir "
                         "değişkendir"),
}

LAYOUT_MSG = {
    "marker_bare": ("{v}: write the {what} exactly as {tag} (a bare marker: no other class, attribute, spacing or "
                    "content)",
                    "{v}: {what} tam olarak {tag} biçiminde yazılır (yalın işaret: başka sınıf, nitelik, boşluk ya da "
                    "içerik yok)"),
    "marker_top": ("{v}: .{cls} must be a direct child of the screen, not inside another element or a ring",
                   "{v}: .{cls} doğrudan ekranın çocuğu olmalı, başka bir öğenin ya da halkanın içinde değil"),
    "marker_many": ("{v}: {n} .{cls} in one screen; at most {most}",
                    "{v}: bir ekranda {n} .{cls} var; en fazla {most}"),
    "fold_one_arm": ("only Variant {has} has a .r-fold: the fold is drawn in both arms or in neither (both show a first "
                     "view and its continuation, split at the same place)",
                     "yalnızca {has} varyantında .r-fold var: kıvrım iki kolda da çizilir ya da hiçbirinde (ikisi de "
                     "ilk ekranı ve devamını aynı yerden bölünmüş gösterir)"),
    "fold_empty": ("{v}: nothing {side} the .r-fold; the first view and the continuation both show content",
                   "{v}: .r-fold {side_tr} hiçbir şey yok; ilk ekran da devamı da içerik gösterir"),
    "breaks": ("Variant A has {a} .r-stage-break, Variant B {b}: both arms show the same number of stages",
               "A varyantında {a}, B varyantında {b} .r-stage-break var: iki kol da aynı sayıda aşama gösterir"),
    "stage_empty": ("{v}: stage {n} is empty; every stage shows its screen",
                    "{v}: {n}. aşama boş; her aşama kendi ekranını gösterir"),
    "fold_stages": ("{v}: .r-fold and .r-stage-break don't mix: a screen either continues below its first view or is "
                    "split into stages",
                    "{v}: .r-fold ile .r-stage-break birlikte kullanılmaz: ekran ya ilk görünümün altında devam eder "
                    "ya da aşamalara bölünür"),
    "sticky_attrs": ("{v}: .r-sticky takes class=\"r-sticky\" only (no other class, style or attribute; the ring goes "
                     "on the element inside)",
                     "{v}: .r-sticky yalnızca class=\"r-sticky\" taşır (başka sınıf, style ya da nitelik yok; halka "
                     "içteki öğeye çizilir)"),
    "sticky_content": ("{v}: .r-sticky holds exactly one element (the pinned element, ringed when it is the variable) "
                       "and no loose text",
                       "{v}: .r-sticky tam olarak bir öğe taşır (sabit öğe; değişken oysa halkalı), çıplak metin "
                       "taşımaz"),
    "sticky_fold": ("{v}: .r-sticky is the bar at the bottom of the first view: the screen needs a .r-fold and the "
                    "bar comes before it; in card.screen: [{{\"h\": \"..\"}}, {{\"sticky\": {{\"cta\": "
                    "\"Checkout\", \"id\": \"cta\"}}}}, {{\"fold\": true}}, {{\"text\": \"..\"}}]",
                    "{v}: .r-sticky ilk ekranın altındaki bardır: ekranda bir .r-fold olmalı ve bar ondan önce gelir; "
                    "card.screen içinde: [{{\"h\": \"..\"}}, {{\"sticky\": {{\"cta\": \"Ödemeye geç\", "
                    "\"id\": \"cta\"}}}}, {{\"fold\": true}}, {{\"text\": \"..\"}}]"),
    "pinned": ("difference 'move': {where} says the element is pinned (“{word}”) but Variant B has no .r-sticky: a "
               "pinned element is drawn as a bar at the bottom of the first view (.r-sticky with .r-fold), not inside "
               "the page flow",
               "fark 'taşı': {where_tr} öğenin sabit olduğunu söylüyor (“{word}”) ama B varyantında .r-sticky yok: "
               "sabit öğe sayfa akışının içinde değil, ilk ekranın altında bir bar olarak çizilir (.r-sticky ve "
               ".r-fold)"),
    "soft_alone": (".hl-soft marks a linked consequence of the variable: the card also needs a .hl around the "
                   "variable itself",
                   ".hl-soft değişkenin bağlı bir sonucunu işaretler: kartta değişkenin kendisinin etrafında da bir "
                   ".hl olmalı"),
    "soft_many": ("{v}: {n} .hl-soft rings; at most {most} per arm (more read as more variables)",
                  "{v}: {n} .hl-soft halka var; kol başına en fazla {most} (fazlası fazla değişken gibi okunur)"),
    "soft_nested": ("{v}: a .hl-soft sits next to the ring, never inside or around a ring (.hl or .hl-soft)",
                    "{v}: .hl-soft halkanın yanında durur, hiçbir halkanın (.hl ya da .hl-soft) içinde ya da "
                    "etrafında değil"),
    "soft_both": ("{v}: an element is either the variable (.hl) or a linked consequence (.hl-soft), not both",
                  "{v}: bir öğe ya değişkendir (.hl) ya bağlı sonuçtur (.hl-soft), ikisi birden değil"),
    "soft_box": ("soft ring in {v} carries inline {prop}: a ring must not push content; give the spacing to the "
                 "children",
                 "{v} varyantındaki yumuşak halka satır içi {prop} taşıyor: halka içeriği itmemeli; boşluğu çocuk "
                 "öğelere verin"),
    "soft_case": ("soft ring label in {v} starts with a lowercase letter (“{note}”); a Turkish label starts with a "
                  "capital letter",
                  "{v} varyantındaki yumuşak halka etiketi küçük harfle başlıyor (“{note}”); Türkçe etiket büyük "
                  "harfle başlar"),
    "device": ("{what} draws a phone screen: only valid with device phone or phone-web, not '{device}'",
               "{what} telefon ekranı çizer: yalnızca device phone ya da phone-web ile kullanılır, '{device}' ile "
               "değil"),
    "captions_missing": ("the screens have {n} stages: card.stage_captions needs {n} short captions, one per stage, "
                         "the same in both arms",
                         "ekranlarda {n} aşama var: card.stage_captions her aşama için bir tane olmak üzere {n} kısa "
                         "başlık ister, iki kolda aynı"),
    "captions_count": ("card.stage_captions has {got} caption(s) for {n} stage(s); give one per stage",
                       "card.stage_captions {n} aşama için {got} başlık taşıyor; her aşamaya bir başlık yazın"),
    "captions_unused": ("card.stage_captions is given but the screens have no .r-stage-break",
                        "card.stage_captions verilmiş ama ekranlarda .r-stage-break yok"),
    "captions_item": ("card.stage_captions: every caption is a short non-empty text, got {got!r}",
                      "card.stage_captions: her başlık kısa ve boş olmayan bir metindir, gelen {got!r}"),
    "captions_case": ("card.stage_captions: “{text}” starts with a lowercase letter; a Turkish caption starts with a "
                      "capital letter",
                      "card.stage_captions: “{text}” küçük harfle başlıyor; Türkçe başlık büyük harfle başlar"),
    "toolbar": ("card.mobile_toolbar draws a mobile browser's bottom toolbar: only valid with device 'phone-web', "
                "not '{device}'",
                "card.mobile_toolbar mobil tarayıcının alt araç çubuğunu çizer: yalnızca device 'phone-web' ile "
                "kullanılır, '{device}' ile değil"),
    "toolbar_type": ("card.mobile_toolbar must be true or false, got {got!r}",
                     "card.mobile_toolbar true ya da false olmalı, gelen {got!r}"),
}

GATE_MSG = {
    "numbers": ("numbers differ between A and B (only in A: {a}; only in B: {b}): a price, amount, percentage, count "
                "or rating that changes between the arms is a second variable, unless the record says why in "
                "`numeric_change`",
                "sayılar A ile B arasında farklı (yalnızca A'da: {a}; yalnızca B'de: {b}): kollar arasında değişen "
                "bir fiyat, tutar, yüzde, adet ya da puan ikinci bir değişkendir; kayıt nedenini `numeric_change` "
                "alanında söylemedikçe"),
    "a11y_none": ("B adds an interactive element ({what}) and the record has no accessibility warning (rule 3): add a "
                  "warnings item of type accessibility whose pass/fail criteria fit the element ({need})",
                  "B etkileşimli bir öğe ekliyor ({what}) ve kayıtta erişilebilirlik uyarısı yok (kural 3): öğeye "
                  "uyan geçti/kaldı ölçütleriyle accessibility türünde bir warnings maddesi ekleyin ({need})"),
    "a11y_missing": ("B adds an interactive element ({what}); the accessibility warning lacks: {missing} (rule 3; "
                     "criteria for this element: {need})",
                     "B etkileşimli bir öğe ekliyor ({what}); erişilebilirlik uyarısında eksik: {missing} (kural 3; "
                     "bu öğenin ölçütleri: {need})"),
    "legal": ("rule 11: legal or mandatory text in A is missing or changed in B (“{text}”); a variant that changes a "
              "regulated display is held until the market's rule is verified, it isn't rendered",
              "kural 11: A'daki yasal ya da zorunlu metin B'de yok ya da değişmiş (“{text}”); düzenlemeye tabi bir "
              "gösterimi değiştiren varyant, pazarın kuralı doğrulanana dek bekletilir, çizilmez"),
    "auth": ("rule 6: B drops security or verification text that A shows (“{term}”: {na} in A, {nb} in B); security "
             "and compliance controls aren't test subjects",
             "kural 6: B, A'nın gösterdiği güvenlik ya da doğrulama metnini düşürüyor (“{term}”: A'da {na}, B'de "
             "{nb}); güvenlik ve uyum denetimleri test konusu yapılmaz"),
    "consent": ("rule 6: a consent box that A leaves unticked is ticked in B (“{text}”); a pre-ticked consent is a "
                "dark pattern and is refused",
                "kural 6: A'da işaretsiz duran onay kutusu B'de işaretli (“{text}”); önceden işaretlenmiş onay "
                "karanlık bir örüntüdür ve reddedilir"),
    "consent_removed": ("rule 6: B removes a consent box that A shows (“{text}”); legal consent is a compliance "
                        "control, never a test subject: the scenario is not produced, and improving the consent step "
                        "is the compliance team's work",
                        "kural 6: B, A'nın gösterdiği onay kutusunu kaldırıyor (“{text}”); yasal onay bir uyum "
                        "denetimidir, test konusu yapılmaz: senaryo üretilmez, onay adımını iyileştirmek uyum "
                        "ekibinin işidir"),
    "metadata": ("{field}: the mockup shows the record's own metadata (“{text}”); the card shows only the title, the "
                 "two mockups and the ring labels, and a KPI, guardrail, evidence or priority line is never drawn into "
                 "a mockup (rule 9)",
                 "{field}: mockup kaydın kendi bilgisini gösteriyor (“{text}”); kart yalnızca başlığı, iki mockup'ı ve "
                 "halka etiketlerini gösterir, KPI, guardrail, kanıt ya da öncelik satırı mockup'a çizilmez (kural 9)"),
    "pii": ("{field}: a value shaped like personal data ({kind}: “{masked}”); rule 15: personal data never reaches a "
            "card. Draw the field empty with its label, mask the value (“•••”) or use an all-zero placeholder",
            "{field}: kişisel veri biçiminde bir değer ({kind}: “{masked}”); kural 15: kişisel veri karta asla "
            "taşınmaz. Alanı etiketiyle boş çizin, değeri maskeleyin (“•••”) ya da sıfırlı bir yer tutucu kullanın"),
}

COLOR_MSG = {
    "syntax": ("brand.{key} must be a plain colour (#hex, rgb(), hsl() or a CSS colour name), got {val!r}",
               "brand.{key} düz bir renk olmalı (#hex, rgb(), hsl() ya da bir CSS renk adı), gelen {val!r}"),
    "name": ("brand.{key}: {val!r} is not a colour name a browser knows, so the button would render transparent; "
             "give the colour as #hex (e.g. #0b4dc2), rgb()/hsl() or a CSS colour name such as navy",
             "brand.{key}: {val!r} tarayıcının tanıdığı bir renk adı değil, buton saydam çizilir; rengi #hex "
             "(ör. #0b4dc2), rgb()/hsl() ya da navy gibi bir CSS renk adı olarak yazın"),
}

LABEL_MSG = {
    "too_wide": ("variant {v}: the ring label “{note}” is about {w}px wide and the screen {screen}px: it fits at no "
                 "position; shorten it to two to four words",
                 "varyant {v}: “{note}” halka etiketi yaklaşık {w}px, ekran {screen}px genişliğinde: hiçbir konuma "
                 "sığmıyor; iki ila dört kelimeye kısaltın"),
    "crowded": ("variant {v}: no position keeps the ring label “{note}” clear of {what}; it was placed {pos} with the "
                "least overlap: check the render, or shorten the label",
                "varyant {v}: “{note}” halka etiketi hiçbir konumda {what} öğesinden uzak kalmıyor; en az örten konuma "
                "({pos}) kondu: görüntüyü kontrol edin ya da etiketi kısaltın"),
}

FRAME_MSG = {
    "nav_device": ("card.bottom_nav: only valid with device 'phone' (native app); a '{device}' frame draws no tab bar",
                   "card.bottom_nav: yalnızca device 'phone' (yerel uygulama) ile kullanılır; '{device}' çerçevesinde "
                   "sekme çubuğu çizilmez"),
    "url": ("card.url: device '{device}' draws an address bar; give the domain (if it was not visible, use a "
            "representative one)",
            "card.url: device '{device}' adres çubuğu çizer; alan adını yazın (görünmüyorsa temsilî bir adres "
            "yazın)"),
    "nav_active": ("card.bottom_nav_active: {val!r} names no tab in bottom_nav; give a tab's label or its 0-based index",
                   "card.bottom_nav_active: {val!r} bottom_nav'daki hiçbir sekmeyle eşleşmiyor; sekmenin adını ya da "
                   "0 tabanlı sırasını yazın"),
}

STAMP_MSG = {
    "missing_critic": ("missing review stamp: review.scenario_critic. Run scenario-critic on the record; on PASS "
                       "write the JSON line `build_card.py --critic-stamp <record>` prints",
                       "inceleme damgası eksik: review.scenario_critic. Kaydı scenario-critic'e inceletin; PASS "
                       "gelirse `build_card.py --critic-stamp <kayıt>` çıktısındaki JSON satırını yazın"),
    "missing_mockup": ("missing review stamp: review.mockup_reviewer. Build the draft (--draft) and have "
                       "mockup-reviewer review the draft and its manifest; on PASS the reviewer runs --stamp on that "
                       "draft and its output is the stamp",
                       "inceleme damgası eksik: review.mockup_reviewer. Taslağı kurun (--draft) ve taslağı "
                       "manifestiyle mockup-reviewer'a inceletin; PASS gelirse gözden geçiren o taslakta --stamp "
                       "çalıştırır, çıktısı damgadır"),
    "verdict": ("review.{key}.verdict is {val!r}: only a PASS is ever stamped (FIX and RET go back to {name})",
                "review.{key}.verdict değeri {val!r}: yalnızca PASS damgalanır (FIX ve RET {name} adımına geri döner)"),
    "format": ("review.{key}.fingerprint must be a sha256 hex string (64 lowercase characters), got {val!r}",
               "review.{key}.fingerprint bir sha256 onaltılık dizesi olmalı (64 küçük harf karakter), gelen {val!r}"),
    "stale_critic": ("review.scenario_critic.fingerprint ({val}…) doesn't match the record: the record changed after "
                     "scenario-critic reviewed it, outside the small-fix fields (title, problem, mechanism, the "
                     "denominators, notes, rationale, objection, exposure, warnings, invariants, assumption wording, "
                     "must_be_true), so it goes back to scenario-critic",
                     "review.scenario_critic.fingerprint ({val}…) kayıtla eşleşmiyor: kayıt scenario-critic "
                     "incelemesinden sonra küçük düzeltme alanlarının (başlık, problem, mekanizma, paydalar, notlar, "
                     "gerekçe, itiraz, maruz kalma, uyarılar, değişmezler, varsayım metni, must_be_true) dışında "
                     "değişmiş, yeniden scenario-critic'e gider"),
    "critic_whole": ("review.scenario_critic.fingerprint ({val}…) doesn't match the record: the record changed after "
                     "scenario-critic reviewed it, and this stamp has no safeguards, so it approves only the exact "
                     "record it was printed for (a small fix keeps only the whole JSON line `build_card.py "
                     "--critic-stamp <record>` prints, safeguards included); the record goes back to scenario-critic",
                     "review.scenario_critic.fingerprint ({val}…) kayıtla eşleşmiyor: kayıt scenario-critic "
                     "incelemesinden sonra değişmiş ve bu damgada safeguards yok, yani yalnızca basıldığı kaydın "
                     "birebir aynısını onaylar (küçük düzeltmeyi yalnızca `build_card.py --critic-stamp <kayıt>` "
                     "çıktısındaki JSON satırının safeguards dahil tamamı taşır); kayıt yeniden scenario-critic'e "
                     "gider"),
    "removed_safeguard": ("A small fix removed or weakened what scenario-critic reviewed: {what}. A small fix may add "
                          "or reword a warning, an accessibility criterion, an invariant or the exposure, never remove "
                          "one: restore it, or send the record back to scenario-critic (review.scenario_critic)",
                          "Küçük bir düzeltme scenario-critic'in incelediği bir güvenceyi kaldırmış ya da "
                          "zayıflatmış: {what}. Küçük düzeltme uyarı, erişilebilirlik ölçütü, değişmez ya da maruz "
                          "kalma ekleyebilir veya yeniden yazabilir, hiçbirini kaldıramaz: geri koyun ya da kaydı "
                          "yeniden scenario-critic'e gönderin (review.scenario_critic)"),
    "critic_refused": ("no critic stamp: {n} validator error(s); fix the record first",
                       "eleştirmen damgası yok: {n} doğrulayıcı hatası; önce kaydı düzeltin"),
    "quick_stamp": ("--stamp {path} is a quick draft (fast mode): it is never stamped; after scenario-critic's PASS "
                    "build the reviewed draft with --draft and have that one reviewed",
                    "--stamp {path} hızlı taslak (hızlı kip): hiç damgalanmaz; scenario-critic PASS verince "
                    "incelenecek taslağı --draft ile kurun ve onu inceletin"),
    "stale_mockup": ("review.mockup_reviewer.fingerprint ({val}…) doesn't match the card this build would write: the "
                     "record's card, its text or the template changed after mockup-reviewer reviewed the draft; build "
                     "a new draft and have it reviewed",
                     "review.mockup_reviewer.fingerprint ({val}…) bu kurulumun yazacağı kartla eşleşmiyor: "
                     "mockup-reviewer taslağı inceledikten sonra kaydın kartı, metni ya da şablon değişmiş; yeni bir "
                     "taslak kurup inceletin"),
}

OUT_MSG = {
    "suffix": ("--out must name an .html card file, got {path}",
               "--out bir .html kart dosyası olmalı, gelen {path}"),
    "input": ("--out {path} is the {what}: a build never overwrites its own input",
              "--out {path} {what_tr} dosyasının kendisi: kurulum kendi girdisinin üzerine asla yazmaz"),
    "source": ("--out {path} lies in the repository's {dir}/ directory: cards are never written among the "
               "playbook's source files; write it to your working directory",
               "--out {path} deponun {dir}/ dizininde: kartlar oyun kitabının kaynak dosyalarının arasına asla "
               "yazılmaz; çalışma dizininize yazın"),
    "not_card": ("--out {path} already exists and is not a card this tool built (no provenance line): refusing to "
                 "overwrite it; choose another file name",
                 "--out {path} zaten var ve bu aracın kurduğu bir kart değil (köken satırı yok): üzerine yazılmıyor; "
                 "başka bir dosya adı seçin"),
}

RUN_MSG = {
    "draft_review": ("review: mockup-reviewer reviews this draft and its manifest; on PASS it runs\n"
                     "  build_card.py --template {template} --scenario {scenario} --stamp {draft}\n"
                     "  and writes the JSON it prints into review.mockup_reviewer",
                     "inceleme: mockup-reviewer bu taslağı ve manifestini inceler; PASS ise şunu çalıştırır\n"
                     "  build_card.py --template {template} --scenario {scenario} --stamp {draft}\n"
                     "  ve yazdığı JSON'u review.mockup_reviewer alanına koyar"),
    "stale_draft": ("--stamp {path}: {what} is not what this record builds now (it changed, or the draft is "
                    "stale): rebuild the draft with --draft and review that one",
                    "--stamp {path}: {what_tr} bu kaydın şu an kurduğuyla aynı değil (değişmiş ya da taslak eski): "
                    "taslağı --draft ile yeniden kurun ve onu inceleyin"),
    "quick_next": ("not reviewed (fast mode): on finish, scenario-critic reviews the record, then the reviewed "
                   "draft (--draft) replaces this file",
                   "incelenmedi (hızlı kip): tamamla denince scenario-critic kaydı inceler, sonra incelenen taslak "
                   "(--draft) bu dosyanın yerini alır"),
    "no_draft": ("--stamp {path}: no such draft; build it with --draft first",
                 "--stamp {path}: böyle bir taslak yok; önce --draft ile kurun"),
    "delivered": ("{path} does not match the reviewed card (sha256 {got}…, the record builds {want}…): the delivered "
                  "file was edited or is stale; rebuild it with the final build",
                  "{path} incelenen kartla eşleşmiyor (sha256 {got}…, kayıt {want}… kuruyor): teslim edilen dosya "
                  "elle değişmiş ya da eski; nihai kurulumla yeniden kurun"),
    "delivered_ok": ("{path} matches the reviewed card (both stamps match)",
                     "{path} incelenen kartla eşleşiyor (iki damga da eşleşiyor)"),
}

PNG_MSG = {
    "written": ("png: {path}", "png: {path}"),
    "failed_check": ("png: {path} (render_check reported a visual problem on this card: run it with --strict and read "
                     "the errors)",
                     "png: {path} (render_check bu kartta görsel bir sorun bildirdi: --strict ile çalıştırıp hataları "
                     "okuyun)"),
    "no_node": ("png: not written (Node.js was not found; the card itself is complete)",
                "png: yazılmadı (Node.js bulunamadı; kartın kendisi tamam)"),
    "unavailable": ("png: not written (Playwright or Chromium is not installed; the card itself is complete)",
                    "png: yazılmadı (Playwright ya da Chromium kurulu değil; kartın kendisi tamam)"),
    "error": ("png: not written (the screenshot step did not finish; the card itself is complete)",
              "png: yazılmadı (ekran görüntüsü adımı tamamlanmadı; kartın kendisi tamam)"),
}

SHARE_MSG = {
    "written": ("share: {path} (1200 × 630)", "paylaşım: {path} (1200 × 630)"),
}

OVERVIEW_MSG = {
    "not_card": ("{path} is not a card this tool built (no provenance line)",
                 "{path} bu aracın kurduğu bir kart değil (köken satırı yok)"),
    "draft": ("{path} is a draft (not visually checked): the overview shows delivered cards; build the final card",
              "{path} bir taslak (görsel kontrol yapılmadı): özet teslim edilen kartları gösterir; nihai kartı kurun"),
    "missing": ("no such card: {path}", "böyle bir kart yok: {path}"),
    "none": ("--overview needs at least one card", "--overview en az bir kart ister"),
    "written": ("overview: {path} ({n} card(s))", "özet: {path} ({n} kart)"),
}
