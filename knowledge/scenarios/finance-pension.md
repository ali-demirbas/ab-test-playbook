# Finans, Sigorta ve Bireysel Emeklilik

Yolculuk aşaması: düzenlemeye tabi finansal ürünlerde (sigorta, hayat, bireysel emeklilik (BES)) web ve mobil uygulama akışları; ürünü tanıma, hesaplama, ön teklif, talep bırakma ve giriş yapmış müşterinin sözleşme işlemleri. Bu dosyadaki her varyant yayından önce uyum onayı ister: zorunlu bilgilendirme metinleri, cayma, onay ve kimlik doğrulama adımları test konusu yapılmaz (CLAUDE.md kural 6 ve 11), kurallar pazara göre değiştiği için bir pazarda onaylanan metin başka pazara taşınmaz. Formun kendi tasarımı `forms-signup.md`, talep formundaki alan sayısı `saas-b2b.md` içindedir; burada tekrar edilmezler. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Akordeondaki uzun ürün açıklamasını etiketli maddelere bölmek talebi artırır mı?

Değişken: Akordeon içindeki ürün açıklamasının biçimi · Fark: değiştir

Etiket: id=fp-001 · mercek=Netlik · düzey=metin · sektör=finans · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does splitting a long product description in an accordion into labelled points raise requests?

EN-Variable: Format of the product description inside the accordion

Bir sigorta ürününün akordeonu açıldığında tek blok hâlinde uzun bir paragraf çıkıyorsa kullanıcı ürünün kimin için olduğunu, neyi kapsadığını ve neyi kapsamadığını satır satır aramak zorunda kalır. Aynı cümleleri “Kimler için”, “Neleri kapsar”, “Neleri kapsamaz” gibi etiketli maddelere bölmek taramayı kolaylaştırır, çünkü karar için aranan bilgi etiketinden bulunur. Riski: maddeleştirirken bir istisna ya da koşul cümlesi kısalır veya düşerse kullanıcı ürünü olduğundan geniş sanar; bu da talepten sonra vazgeçme ve şikâyet olarak geri döner. İki kolda metnin içeriği aynıdır, yalnızca biçimi değişir. “Güvenceleri madde listesi hâlinde vermek ikna ediyor mu?” (`home-landing.md`) senaryosundan farkı: orada pazarlama sayfasındaki güven vaatleri listelenir, burada düzenlemeye tabi bir ürünün kapsam metni bölünür ve metnin anlamı uyum onayıyla sabit tutulur.

**Test edilmesi gerekenler**
- Biçim: Etiketli maddeler, aynı içeriği taşıyan paragrafa göre talep bırakmayı artırıyor mu?
- Kapsam algısı: Maddeli sürümden gelen kullanıcı danışman görüşmesinde ürünün kapsamadığı durumları daha mı az soruyor?
- Okuma: Akordeonu açan kullanıcı maddeli sürümde metnin sonundaki talep butonuna kadar iniyor mu?
- Sonraki test: Maddeler kazanırsa, etiketlerin sırası (önce kapsam / önce kimler için) ayrı bir testte talebi değiştiriyor mu?
- Cihaz: Dar ekranda maddeli sürüm akordeonu uzatıp talep butonunu ekranın altına mı itiyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (ürün sayfasına atanan ziyaretçi başına): Maddeli açıklama talep bırakanların payını artırıyor mu?
- Akordeon Açma Oranı: Tanı metriği; değişiklik akordeonun içinde olduğu için iki kolda aynı çıkması beklenir.
- Talep Butonu Tıklama Oranı: Akordeonu açanlar içinde butona basanların payı yükseliyor mu?
- Başvuru Onay Oranı (90 gün): Maddeli sürümden gelen taleplerin onaylanıp poliçeye dönüşen payı düşmemeli.
- Destek Talebi: Kapsam ve istisnalarla ilgili soru ve şikâyet, atanan ziyaretçi başına artmamalı.

**Yapılmaması gerekenler**
- Aynı testte açıklamanın biçimi ile cümlelerin içeriğini birlikte değiştirmeyin; iki kolda aynı bilgi durmalı.
- Maddeleştirirken istisna, bekleme süresi veya koşul cümlelerini kısaltmayın ya da çıkarmayın; düzenlemeye tabi metin kelimesi kelimesine korunur.
- Maddeli sürümü uyum biriminin yazılı onayı olmadan yayına almayın; kapsam metni hedef pazarın kuralına bağlı bir bilgilendirmedir.
- “Neleri kapsamaz” maddesini katlanmış, soluk veya en sona itilmiş biçimde göstermeyin.
- Etiketleri ikon veya renkle süsleyip aynı testte görsel yoğunluğu da artırmayın.

### EN

When an insurance product’s accordion opens into one long paragraph, the user has to hunt line by line for who the product is for, what it covers and what it does not. Splitting the same sentences into labelled points such as “Who it’s for”, “What it covers” and “What it doesn’t cover” makes scanning easier, because the information needed for the decision can be found from the label. The risk: if an exclusion or condition sentence gets shortened or dropped while the text is turned into bullets, the user assumes the product is broader than it is, and that comes back as post-request drop-out and complaints. The wording is identical in both arms; only the format changes. How it differs from the “Does presenting assurances as a bullet list persuade?” scenario (`home-landing.md`): that one lists trust promises on a marketing page, while this one splits the coverage text of a regulated product and the meaning of the text stays fixed through compliance sign-off.

**What to test**
- Format: Do labelled points raise request submissions compared with a paragraph carrying the same content?
- Coverage perception: Do users arriving from the bulleted version ask advisors fewer questions about what the product does not cover?
- Reading: In the bulleted version, do users who open the accordion scroll down to the request button at the end of the text?
- Next test: If the bullets win, does the order of the labels (coverage first or “Who it’s for” first) change requests in a separate test?
- Device: On a narrow screen, does the bulleted version lengthen the accordion and push the request button below the fold?

**KPIs to track**
- Lead Submission Rate (per visitor assigned to the product page): Does the bulleted description raise the share of visitors who submit a request?
- Accordion Open Rate: Diagnostic metric; since the change sits inside the accordion, it should come out the same in both arms.
- Request Button Click Rate: Among those who open the accordion, does the share who press the button rise?
- Application Approval Rate (90 days): The share of requests from the bulleted version that are approved and become policies must not drop.
- Support Contact Rate: Questions and complaints about coverage and exclusions must not rise per assigned visitor.

**What not to do**
- Don’t change the format of the description and the content of its sentences in the same test; the same information must stand in both arms.
- Don’t shorten or remove exclusion, waiting-period or condition sentences while bulleting; regulated text is preserved word for word.
- Don’t ship the bulleted version without written sign-off from the compliance team; the coverage text is a disclosure tied to the target market’s rules.
- Don’t show the “What it doesn’t cover” point collapsed, faded or pushed to the end.
- Don’t decorate the labels with icons or color and raise visual density in the same test.

---

## Hizmet tanıtımında açıklama cümlelerini ilgili adımın altına taşımak katılımı artırır mı?

Değişken: Tanıtım açıklamasının ekrandaki yeri · Fark: taşı

Etiket: id=fp-002 · mercek=Netlik · düzey=görsel · sektör=finans · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does moving the explanatory sentences of a service introduction under the step they describe raise take-up?

EN-Variable: On-screen position of the introduction’s explanatory text

Fon dağılımını müşteri adına yöneten bir hizmetin tanıtım ekranında açıklama paragrafı üstte, üç adım (risk profilini belirle, öneriyi incele, onayla) altta durduğunda hangi cümlenin hangi adıma ait olduğunu kullanıcı kendi eşleştirir. Aynı cümleleri ait oldukları adımın altına taşımak, her adımda ne olacağını tam o adımın yanında söyler; belirsizlik azaldığı için başlama eşiği düşebilir. Riski: üstteki özet kalkınca hizmetin ne olduğu ilk bakışta anlaşılmayabilir ve adım listesi uzadığı için başlat butonu ekranın altına iner.

**Test edilmesi gerekenler**
- Yer: Açıklama cümleleri adımların altındayken hizmete katılım, cümleler üstte tek paragrafken olduğundan yüksek mi?
- İlk bakış: Üstteki paragraf kalkınca kullanıcı hizmetin ne yaptığını anlamadan tanıtım ekranından çıkıyor mu?
- Adım kaybı: Katılım akışını başlatanların risk profili sorularını bitirme payı iki kolda aynı mı?
- Sonraki test: Taşıma kazanırsa, adım altı cümlelerin açık ya da katlanmış gelmesi ayrı bir testte katılımı değiştiriyor mu?
- Kullanıcı tipi: Fon dağılımını daha önce kendisi değiştirmiş müşteri ile hiç değiştirmemiş müşteri taşınan açıklamaya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Özellik Katılım Oranı (teste atanan giriş yapmış müşteri başına): Hizmeti onaylayıp etkinleştiren müşterilerin payı artıyor mu?
- Akış Başlatma Oranı: Tanıtım ekranından ilk adıma geçenlerin payı; tanı metriği.
- Risk Profili Tamamlama Oranı: Akışı başlatanlar içinde soruları bitirenlerin payı; tanı metriği.
- 30 Gün İçinde Durdurma Oranı (30 gün): Hizmete katılan müşterilerden hizmeti bu pencerede durduranların payı artmamalı.
- Ücret Sorusu Oranı: Hizmetin ücreti ve işleyişi hakkında danışmana gelen sorular artmamalı.

**Yapılmaması gerekenler**
- Aynı testte cümlelerin yeri ile cümlelerin metnini birlikte değiştirmeyin; taşınan cümle kelimesi kelimesine aynı kalır.
- Hizmet ücretini, kesintiyi veya risk uyarısını taşırken küçültmeyin ya da bağlantı arkasına almayın; mevzuatın istediği bilgilendirme iki kolda aynı görünürlükte durur.
- Geçmiş fon getirisini veya beklenen kazancı adım açıklamasına eklemeyin; getiri vaadi yazılmaz, rakam uydurulmaz.
- Onay adımını atlayan ya da risk profili sorularını azaltan bir akışı bu testin parçası yapmayın.
- Adımların sayısını veya sırasını bu testte oynatmayın; üç adım iki kolda da aynıdır.

### EN

On the introduction screen of a service that manages fund allocation on the customer’s behalf, when the explanatory paragraph sits on top and the three steps (set your risk profile, review the recommendation, approve) sit below, users have to match each sentence to its step themselves. Moving the same sentences under the step they belong to says what will happen at each step right next to that step; with less uncertainty, the barrier to starting may drop. The risk: once the summary on top is gone, what the service is may not be clear at first glance, and the longer step list pushes the start button below the fold.

**What to test**
- Position: Is enrolment in the service higher when the explanatory sentences sit under the steps than when they sit on top as a single paragraph?
- First glance: With the top paragraph gone, do users leave the introduction screen without understanding what the service does?
- Step loss: Is the share of those who start the enrolment flow and finish the risk profile questions the same in both arms?
- Next test: If moving wins, does showing the sentences under each step open or collapsed change enrolment in a separate test?
- User type: Do customers who have changed their fund allocation themselves before react differently to the moved text than customers who never have?

**KPIs to track**
- Feature Opt-in Rate (per logged-in customer assigned to the test): Does the share of customers who approve and activate the service rise?
- Flow Start Rate: The share who move from the introduction screen to the first step; diagnostic metric.
- Risk Profile Completion Rate: Among those who start the flow, the share who finish the questions; diagnostic metric.
- 30-Day Stop Rate (30 days): The share of customers who join the service and then stop it within this window must not rise.
- Fee Question Rate: Questions to advisors about the service’s fee and how it works must not rise.

**What not to do**
- Don’t change the position of the sentences and their wording in the same test; the moved sentence stays word for word the same.
- Don’t shrink the service fee, deductions or risk warning when moving them, and don’t put them behind a link; the disclosure the regulation requires keeps the same visibility in both arms.
- Don’t add past fund returns or expected gains to the step descriptions; no return promises are written and no figures are invented.
- Don’t make a flow that skips the approval step or cuts the risk profile questions part of this test.
- Don’t change the number or order of the steps in this test; the three steps are the same in both arms.

---

## Kişisel öneri vaat eden slayta vaadi adlandıran bir buton eklemek işe yarar mı?

Değişken: Öneri slaytındaki eylem butonu · Fark: ekle

Etiket: id=fp-003 · mercek=Netlik · düzey=görsel · sektör=finans · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does adding a button that names the promise to a slide offering a personal recommendation pay off?

EN-Variable: Action button on the recommendation slide

Uygulamanın ana ekranındaki bir slayt “Size özel katkı payı önerimiz hazır” dediği hâlde üzerinde dokunulacak belirgin bir öğe yoksa müşteri vaadin nereden açılacağını bilemez. Slayta vaadi adlandıran bir buton (“Önerimi gör”) eklemek hem dokunulabilirliği işaretler hem dokununca ne çıkacağını söyler. Riski: buton merakla dokunmayı artırır, ama açılan ekran gerçekten kişisel değilse ya da beklenenden yüksek bir tutar öneriyorsa müşteri vazgeçer; dokunma artar, artırım artmaz. Bu yüzden birincil metrik dokunma değil, tamamlanan katkı payı artırımıdır.

**Test edilmesi gerekenler**
- Varlık: Butonlu slayt, butonsuz slayta göre katkı payı artırımını tamamlayan müşteri payını yükseltiyor mu?
- Vaat uyumu: Butona dokunan müşteri açılan ekranda kendi sözleşmesine göre hesaplanmış bir tutar mı buluyor?
- Görünürlük: Öneri slaytı kayan dizide ilk sırada değilken butonun etkisi kayboluyor mu?
- Sonraki test: Buton kazanırsa, buton metni (“Önerimi gör” / “Tutarı incele”) ayrı bir testte artırımı değiştiriyor mu?
- Segment: Son bir yılda katkı payını artırmış müşteri ile hiç artırmamış müşteri butona farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Katkı Payı Artırma Oranı (teste atanan giriş yapmış müşteri başına): Artırımı onaylayıp tamamlayanların payı artıyor mu?
- Slayt Dokunma Oranı: Tanı metriği; öneri ekranını açanların atanan müşteriye oranı.
- Öneriden Onaya Geçiş Oranı: Öneri ekranını açanların kaçı artırım onayına ilerliyor?
- Artırımı Geri Alma Oranı (90 gün): Artırım yapan müşterinin ilan edilen pencerede tutarı eski hâline çekme payı yükselmemeli.
- Diğer Slayt Dokunma Oranı: Butonlu slayt dizideki öbür slaytların dokunulmasını kabul edilemez ölçüde azaltmamalı.

**Yapılmaması gerekenler**
- Aynı testte butonu eklerken slaytın başlığını, görselini veya dizideki sırasını birlikte değiştirmeyin.
- Buton “Önerimi gör” diyorsa arkasında herkese aynı tutarı sunan genel bir ekran açmayın; vaat edilen kişisel öneri gerçek sözleşme verisinden hesaplanır.
- Butona veya slayta “Son gün”, “Kaçırmayın” gibi aciliyet ifadesi ya da gerçek olmayan bir süre sınırı koymayın.
- Devlet katkısını, getiriyi veya birikim tutarını slayta rakamla yazmayın; uyum onayından geçmemiş hiçbir oran ya da tutar gösterilmez.
- Artırım onayındaki bilgilendirmeyi kısaltmayın; buton yalnızca öneri ekranını açar, onayın yerine geçmez.

### EN

When a slide on the app’s home screen says “Your personal contribution recommendation is ready” but has no clear element to tap, the customer does not know where the promise opens. Adding a button that names the promise (“See my recommendation”) both signals tappability and says what will appear on tap. The risk: a button raises taps out of curiosity, but if the screen it opens is not truly personal or recommends a higher amount than expected, the customer backs out; taps rise and increases do not. That is why the primary metric is not taps but completed contribution increases.

**What to test**
- Presence: Does the slide with a button raise the share of customers who complete a contribution increase compared with the slide without one?
- Promise match: Does the customer who taps the button find an amount calculated from their own contract on the screen that opens?
- Visibility: When the recommendation slide is not first in the carousel, does the button’s effect disappear?
- Next test: If the button wins, does the button text (“See my recommendation” / “Review the amount”) change increases in a separate test?
- Segment: Do customers who raised their contribution in the past year react to the button differently from customers who never have?

**KPIs to track**
- Contribution Increase Rate (per logged-in customer assigned to the test): Does the share of those who approve and complete an increase rise?
- Slide Tap Rate: Diagnostic metric; the ratio of customers who open the recommendation screen to assigned customers.
- Recommendation-to-Approval Rate: Of those who open the recommendation screen, how many move on to approve the increase?
- Increase Reversal Rate (90 days): The share of customers who raise their contribution and then return the amount to its old level within the stated window must not rise.
- Other Slide Tap Rate: The slide with the button must not reduce taps on the other slides in the carousel to an unacceptable degree.

**What not to do**
- Don’t change the slide’s title, image or position in the carousel in the same test as adding the button.
- If the button says “See my recommendation”, don’t open a generic screen that offers everyone the same amount; the promised personal recommendation is calculated from real contract data.
- Don’t put urgency wording such as “Last day” or “Don’t miss out”, or a fake time limit, on the button or the slide.
- Don’t write government contribution, returns or savings amounts as figures on the slide; no rate or amount that has not passed compliance sign-off is shown.
- Don’t shorten the disclosure on the increase approval; the button only opens the recommendation screen and does not replace the approval.

---

## Yalnızca ürün adlarından oluşan listenin başına “Hangisi bana uygun?” yönlendirmesi eklemek talebi artırır mı?

Değişken: Liste başındaki ürün seçme yönlendirmesi · Fark: ekle

Etiket: id=fp-004 · mercek=Uygunluk · düzey=bilgi · sektör=finans · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does adding a “Which one suits me?” guide at the top of a list of bare product names raise requests?

EN-Variable: Product-selection guide at the top of the list

Sigorta ürünleri yalnızca adlarıyla sıralandığında (“Ferdi Kaza”, “Yıllık Hayat”, “Kritik Hastalıklar”) ürünleri tanımayan ziyaretçi hangisine bakacağını bilemez; her birini tek tek açıp karşılaştırmak zorunda kalır. Listenin başına ihtiyaçtan ürüne götüren kısa bir yönlendirme (“Hangisi bana uygun?” başlığı altında “Ailemi korumak istiyorum”, “Borcumu güvenceye almak istiyorum” gibi birkaç seçenek) eklemek seçim yükünü azaltır, çünkü ziyaretçi ürün adını değil kendi ihtiyacını tanır. Riski: yönlendirme kişiye özel tavsiye gibi algılanırsa yanlış ürüne talep gelir; ayrıca liste aşağı itilir ve ne aradığını bilen ziyaretçi yavaşlar.

**Test edilmesi gerekenler**
- Varlık: Yönlendirme eklenen listede herhangi bir ürün için talep bırakanların payı artıyor mu?
- Eşleşme: Bir ihtiyaç seçen ziyaretçi yönlendirildiği ürünün sayfasında mı kalıyor, yoksa listeye geri mi dönüyor?
- Bilen ziyaretçi: Aradığı ürünü doğrudan açan ziyaretçinin ürüne ulaşma süresi uzuyor mu?
- Sonraki test: Yönlendirme kazanırsa, ihtiyaç seçeneklerinin sayısı (3 / 5) ayrı bir testte talebi değiştiriyor mu?
- Kategori: Hayat, sağlık ve kaza ürünlerinde yönlendirmenin etkisi aynı mı, yoksa tek bir ürün grubunda mı toplanıyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (liste ekranına atanan ziyaretçi başına): Herhangi bir üründe talep bırakanların payı artıyor mu?
- Liste → Ürün Tıklama Oranı: Listeden bir ürün sayfasına geçenlerin payı; tanı metriği.
- Listeye Geri Dönüş Oranı: Ürün sayfasından listeye dönenlerin payı; eşleşme tutmuyorsa yükselir.
- Başvuru Onay Oranı (90 gün): Gönderilen taleplerden onaylananların payı gerilememeli; yanlış ürüne yönlenen talep burada görünür.
- Cayma Süresi İçinde İptal Oranı (yasal cayma süresi): Yönlendirmeyle alınan poliçelerde cayma çoğalmamalı.

**Yapılmaması gerekenler**
- Aynı testte yönlendirmeyi eklerken ürünlerin sırasını, adlarını veya kart tasarımını birlikte değiştirmeyin.
- Yönlendirmeyi kişiye özel tavsiye gibi sunmayın (“Sizin için en doğru ürün”); genel bilgilendirme ile tavsiye arasındaki sınırı hedef pazarın kuralına göre uyum birimiyle doğrulayın.
- İhtiyaç seçeneklerinin hepsini aynı ürüne ya da komisyonu yüksek ürüne bağlamayın; eşleşme ürünün gerçek kapsamına dayanır.
- Yönlendirmeyi kapatılamayan bir katman olarak açmayın; ürün listesi onun altında her zaman erişilebilir kalır.
- Yönlendirmede sağlık durumu veya gelir gibi hassas bilgileri sormayın; seçenekler ihtiyaç düzeyinde kalır.

### EN

When insurance products are listed by name only (“Personal Accident”, “Annual Life”, “Critical Illness”), a visitor who does not know the products cannot tell which one to look at and has to open and compare each one. Adding a short guide at the top that leads from need to product (a “Which one suits me?” heading with a few options such as “I want to protect my family” and “I want to secure my debt”) reduces the choice load, because the visitor recognises their own need rather than a product name. The risk: if the guide reads as personal advice, requests arrive for the wrong product; it also pushes the list down and slows visitors who know what they are looking for.

**What to test**
- Presence: In the list with the guide added, does the share of visitors who submit a request for any product rise?
- Match: Does a visitor who picks a need stay on the product page they are sent to, or go back to the list?
- Visitors who know: Does it take longer for a visitor who opens the product they are looking for directly to reach it?
- Next test: If the guide wins, does the number of need options (3 / 5) change requests in a separate test?
- Category: Is the guide’s effect the same across life, health and accident products, or concentrated in one product group?

**KPIs to track**
- Lead Submission Rate (per visitor assigned to the list screen): Does the share of visitors who submit a request for any product rise?
- List-to-Product Click Rate: The share who move from the list to a product page; diagnostic metric.
- Return-to-List Rate: The share who go back from a product page to the list; it rises if the match is not holding.
- Application Approval Rate (90 days): The share of submitted requests that are approved must not decline; requests steered to the wrong product show up here.
- Cooling-off Cancellation Rate (statutory cooling-off period): Cancellations within the cooling-off period must not rise on policies bought through the guide.

**What not to do**
- Don’t change the order, names or card design of the products in the same test as adding the guide.
- Don’t present the guide as personal advice (“The right product for you”); check the line between general information and advice with the compliance team under the target market’s rules.
- Don’t tie all need options to the same product or to the product with the higher commission; the match rests on what the product actually covers.
- Don’t open the guide as a layer that cannot be dismissed; the product list stays reachable beneath it at all times.
- Don’t ask for sensitive information such as health status or income in the guide; the options stay at the level of needs.

---

## Sözleşme seçimi adımına ne yapılacağını söyleyen bir yönerge satırı eklemek ilerlemeyi artırır mı?

Değişken: Sözleşme seçimi adımındaki yönerge satırı · Fark: ekle

Etiket: id=fp-005 · mercek=Netlik · düzey=metin · sektör=finans · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does adding an instruction line to the contract selection step raise progress?

EN-Variable: Instruction line on the contract selection step

Birden fazla sözleşmesi olan müşteri bir işlem akışına girdiğinde (katkı payı değişikliği, fon dağılımı, ödeme aracı güncelleme) ilk ekranda sözleşmelerin listesini ve pasif bir “Devam” butonunu bulur; ne yapması gerektiği yazmıyorsa butonun neden çalışmadığını anlamaz ve çıkar. Listenin üstüne tek satırlık bir yönerge (“İşlem yapmak istediğiniz sözleşmeyi seçin”) eklemek beklenen eylemi söyler. Riski: satır fark edilmezse hiçbir şey değişmez. “Daha hızlı olsun” diye sözleşmeyi önceden işaretlemek cazip görünür, ama işlemin kapsamını müşteri yerine seçmek olur; o yüzden bu senaryonun dışındadır ve aşağıda yasak olarak yazılıdır.

**Test edilmesi gerekenler**
- Varlık: Yönerge satırı eklenince seçim adımına gelen müşterilerin işlemi tamamlama payı artıyor mu?
- Takılma: Hiçbir sözleşme seçmeden pasif “Devam” butonuna dokunma denemeleri azalıyor mu?
- Yanlış seçim: İşlemi bitiren müşterinin sonradan düzeltme isteme payı iki kolda aynı mı?
- Sonraki test: Yönerge kazanırsa, pasif butona dokunulduğunda satırın vurgulanması ayrı bir testte ilerlemeyi artırıyor mu?
- Segment: Tek sözleşmeli müşteri ile birden fazla sözleşmesi olan müşteri yönergeye farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ana Aksiyon Tamamlama Oranı (seçim adımına ulaşan müşteri başına, iki kolda aynı tetikleyici): Akışın işini (ör. katkı payı değişikliği) bitirenlerin payı artıyor mu?
- Sözleşme Seçim Oranı: Adıma gelenlerin en az bir sözleşme işaretleme payı; tanı metriği.
- Pasif Butona Dokunma Oranı: Seçim yapmadan “Devam”a dokunan müşteri payı azalıyor mu?
- İşlem Düzeltme Oranı (30 gün): Biten işlemin ilan edilen pencerede geri alınma ya da düzeltilme payı artmamalı.
- Yanlış Sözleşme Şikâyeti Oranı: İstenmeyen sözleşmede işlem yapıldığı gerekçesiyle açılan kayıtlar çoğalmamalı.

**Yapılmaması gerekenler**
- Sözleşme kutusunu önceden işaretli getirmeyin; işlemin hangi sözleşmeyi kapsayacağını müşteri yerine seçmek reddedilen bir varyanttır.
- Aynı testte yönerge satırını eklerken sözleşme kartlarının içeriğini veya “Devam” butonunun metnini birlikte değiştirmeyin.
- Yönergeyi “Tümünü seç” kısayoluna çevirmeyin; kapsamı genişleten bir varsayılan bu testin konusu olamaz.
- Seçimden sonraki bilgilendirme ve işlem onayı ekranını atlamayın ya da daraltmayın; mevzuatın istediği onay adımı iki kolda aynen durur.
- Yönerge satırına sözleşmenin birikimi, getirisi veya kesintisi hakkında yeni bir rakam ya da vaat yazmayın; satır yalnızca yapılacak eylemi söyler.

### EN

When a customer with several contracts enters a transaction flow (changing a contribution, fund allocation, updating a payment method), the first screen shows a list of contracts and an inactive “Continue” button; if nothing says what to do, the customer does not understand why the button does not work and leaves. Adding a one-line instruction above the list (“Select the contract you want to act on”) states the expected action. The risk: if the line goes unnoticed, nothing changes. Preselecting the contract to make it “faster” is tempting, but it means choosing the scope of the transaction for the customer; that is why it falls outside this scenario and is written below as a prohibition.

**What to test**
- Presence: With the instruction line added, does the share of customers reaching the selection step who complete the transaction rise?
- Getting stuck: Do attempts to tap the inactive “Continue” button without selecting a contract decrease?
- Wrong selection: Is the share of customers who ask for a correction after finishing the transaction the same in both arms?
- Next test: If the instruction wins, does highlighting the line when the inactive button is tapped increase progress in a separate test?
- Segment: Do customers with a single contract react to the instruction differently from customers with several contracts?

**KPIs to track**
- Primary Action Completion Rate (per customer reaching the selection step, same trigger in both arms): Does the share of those who finish the flow’s job (e.g. a contribution change) rise?
- Contract Selection Rate: The share of those who arrive at the step and select at least one contract; diagnostic metric.
- Inactive Button Tap Rate: Does the share of customers who tap “Continue” without selecting decrease?
- Transaction Correction Rate (30 days): The share of completed transactions reversed or corrected within the stated window must not rise.
- Wrong Contract Complaint Rate: Cases opened because a transaction was made on an unintended contract must not rise.

**What not to do**
- Don’t ship the contract checkbox preselected; choosing which contract a transaction covers on the customer’s behalf is a rejected variant.
- Don’t change the content of the contract cards or the text of the “Continue” button in the same test as adding the instruction line.
- Don’t turn the instruction into a “Select all” shortcut; a default that widens the scope cannot be the subject of this test.
- Don’t skip or shrink the disclosure and transaction confirmation screen after selection; the confirmation step the regulation requires stays as it is in both arms.
- Don’t put a new figure or promise about the contract’s savings, returns or deductions into the instruction line; the line only says what action to take.

---

## Hesaplama sonuç ekranına sonucu talebe bağlayan bir buton eklemek talep oluşturmayı artırır mı?

Değişken: Hesaplama sonuç ekranındaki talep butonu · Fark: ekle

Etiket: id=fp-006 · mercek=Netlik · düzey=görsel · sektör=finans · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does a button on the calculator result screen that carries the result into a request raise request creation?

EN-Variable: Request button on the calculator result screen

Emeklilik birikimi ya da prim hesaplama aracı sonucu gösterip orada bitiyorsa ziyaretçi en ilgili olduğu anda çıkmaza girer: sonucu almıştır ama devam etmek için menüden başka bir sayfa bulması gerekir. Sonuç ekranına talep formunu açan bir buton (“Bu hesapla teklif iste”) eklemek ilgiyi eyleme bağlar. Riski: araç yalnızca merak eden ziyaretçiden düşük niyetli talep toplar ve danışman ekibinin yükü artar; ayrıca hesaplanan tutar bir taahhüt gibi okunursa teklif aşamasında hayal kırıklığı doğar.

**Test edilmesi gerekenler**
- Varlık: Sonuç ekranına buton eklemek, hesaplamayı bitirenlerin talep bırakma payını artırıyor mu?
- Talep niteliği: Butondan gelen talep, menüden gelen talebe göre danışman görüşmesine daha mı az dönüşüyor?
- Erken ayrılma: Buton eklenince ziyaretçi farklı değerlerle tekrar hesaplamayı bırakıp sonuç ekranından erken mi çıkıyor?
- Sonraki test: Buton kazanırsa, hesaplamada girilen değerleri talep formuna hazır taşımak ayrı bir testte form tamamlamayı artırıyor mu?
- Cihaz: Mobil web ve masaüstünde buton sonuç tablosunun üstünde mi kalıyor, yoksa kaydırmadan görünmüyor mu?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (hesaplamayı tamamlayan ziyaretçi başına, iki kolda aynı tetikleyici): Sonuç ekranına ulaşanlar içinde talep bırakanların payı artıyor mu?
- Hesaplama Tamamlama Oranı: Değişiklik sonuç ekranında olduğu için iki kolda eşit çıkması beklenir; fark atama ya da ölçüm hatasına işaret eder.
- Yeniden Hesaplama Oranı: Sonuç ekranında değerleri değiştirip tekrar hesaplayanların payı; tanı metriği.
- Başvuru Onay Oranı (90 gün): Sonuç ekranından gelen başvurularda onaylananların payı düşmemeli.
- Ulaşılamayan Talep Oranı: Danışmanın aradığında ulaşamadığı ya da ilgisiz çıkan taleplerin payı artmamalı.

**Yapılmaması gerekenler**
- Aynı testte butonu eklerken sonuç tablosunun içeriğini, varsayımlarını veya hesaplama formülünü birlikte değiştirmeyin.
- Sonucu garanti edilmiş getiri ya da kesin prim gibi sunan bir buton metni yazmayın (“Bu birikimi garantile”); hesap bir tahmindir ve varsayım notu iki kolda yerinde kalır.
- Butonu, sonucu görmek için iletişim bilgisi isteyen bir kapıya çevirmeyin; sonuç iki kolda da talepsiz görünür.
- Butona dokunmayı talep saymayın; iletişim izni ve aydınlatma metni formda aynen durur, buton onların yerine geçmez.
- “Bu teklif yalnızca bugün geçerli” gibi süre baskısı kuran ifadeleri butonun yanına koymayın.

### EN

When a retirement savings or premium calculator shows its result and ends there, the visitor hits a dead end at the moment of highest interest: they have the result, but to continue they must find another page through the menu. Adding a button to the result screen that opens the request form (“Request a quote with this calculation”) links interest to action. The risk: the tool collects low-intent requests from merely curious visitors and the advisory team’s load rises; and if the calculated amount reads as a commitment, disappointment follows at the quote stage.

**What to test**
- Presence: Does adding the button to the result screen raise the share of visitors who finish the calculation and then submit a request?
- Request quality: Do requests from the button convert to an advisor call less often than requests from the menu?
- Early exit: Once the button is there, do visitors stop recalculating with different values and leave the result screen early?
- Next test: If the button wins, does carrying the values entered in the calculator into the request form, ready-filled, raise form completion in a separate test?
- Device: On mobile web and desktop, does the button stay above the result table, or is it invisible without scrolling?

**KPIs to track**
- Lead Submission Rate (per visitor who completes the calculation, same trigger in both arms): Among those who reach the result screen, does the share who submit a request rise?
- Calculator Completion Rate: Since the change sits on the result screen, it should come out equal in both arms; a gap points to an assignment or measurement error.
- Recalculation Rate: The share who change values on the result screen and recalculate; diagnostic metric.
- Application Approval Rate (90 days): The share of applications from the result screen that are approved must not drop.
- Unreachable Lead Rate: The share of requests the advisor cannot reach on calling, or that turn out irrelevant, must not rise.

**What not to do**
- Don’t change the content, assumptions or formula of the result table in the same test as adding the button.
- Don’t write button text that presents the result as a guaranteed return or a fixed premium (“Lock in these savings”); the calculation is an estimate and the assumptions note stays in place in both arms.
- Don’t turn the button into a gate that asks for contact details before the result is shown; the result is visible without a request in both arms.
- Don’t count a button tap as a request; the contact consent and the privacy notice stay on the form as they are, and the button does not replace them.
- Don’t put pressure wording such as “This quote is valid only today” next to the button.

---

## Ön teklif formunda kimlik numarası alanının yanına neden istendiğini yazmak teklif almayı artırır mı?

Değişken: Kimlik numarası alanının yanındaki gerekçe satırı · Fark: ekle

Etiket: id=fp-007 · mercek=Güven · düzey=güven · sektör=finans · pazar=TR · emek=düşük · durum=güncel · tarih=2026-11

EN: Does writing why the ID number is needed next to its field on a pre-quote form raise quotes?

EN-Variable: Rationale line next to the ID number field

Sigorta ya da emeklilik ön teklif formunda kimlik numarası veya doğum tarihi alanı, henüz fiyat bile almamış ziyaretçiye ağır gelir: “neden şimdi istiyorlar” sorusu yanıtsız kalınca form orada bırakılır. Alanı kaldırmak çoğu zaman mümkün değildir, çünkü teklif bu bilgiyle hesaplanır; alanı kaldırmak yerine denenen ara yöntemlerden biri olan gerekçe vermek, alanın yanına bilginin ne için kullanılacağını yazar (“Primi yaşınıza göre hesaplayabilmemiz için gerekir”). Riski: gerekçe yayımlanan aydınlatma metniyle birebir örtüşmezse yanıltıcı olur; ayrıca gerekçe, ziyaretçinin aklına gelmemiş bir kaygıyı uyandırabilir. “Alanın yanına “neden soruyoruz” açıklaması eklemek, amacı belirsiz görünen bir alanı doldurtur mu?” (`saas-b2b.md`) senaryosundan farkı: orada alan hassas olmayan bir niteleme sorusudur ve ölçülen o alanın doldurulmasıdır; burada alan zorunlu ve hassastır, gerekçenin metni kişisel veri kurallarına bağlıdır ve ölçülen teklifin alınmasıdır.

**Test edilmesi gerekenler**
- Varlık: Gerekçe satırı eklenince ön teklif formunu gönderip teklif isteyenlerin payı artıyor mu?
- Alan düzeyi: Kimlik numarası alanına gelip formu orada bırakanların payı azalıyor mu?
- Ters etki: Gerekçe, alanı sorgulamadan dolduran ziyaretçide tereddüt uyandırıp doldurma süresini uzatıyor mu?
- Segment: Reklamdan ilk kez gelen ziyaretçi ile mevcut müşteri gerekçeye farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (ön teklif formuna atanan ziyaretçi başına): Formu gönderip teklif isteyenlerin payı artıyor mu?
- Alan Bazlı Terk Oranı: Kimlik numarası alanında formu bırakanların payı; tanı metriği.
- Doğrulama Hatası Oranı: Geçersiz ya da doğrulanamayan numara girişleri artmamalı.
- Sözleşme Oranı (90 gün): Ön teklif formuna atanan ziyaretçilerden pencerede sözleşmeyi ya da poliçeyi tamamlayanların payı düşmemeli; gerekçe teklif isteyenleri artırıp sözleşmeye dönmeyen talep getiriyorsa burada görünür.
- Teklif → Sözleşme Dönüşüm Oranı (90 gün): Tanı metriği; teklif alan ziyaretçi sayısı B’de değişebildiği için kazanan seçmez ve guardrail yerine geçmez.
- Veri Şikâyeti Oranı: Kişisel verinin kullanımıyla ilgili başvuru ve şikâyetler çoğalmamalı.

**Yapılmaması gerekenler**
- Aynı testte gerekçe satırını eklerken alanın zorunluluğunu, sırasını veya etiketini birlikte değiştirmeyin.
- Alanı tümden kaldırmayı ya da kimlik doğrulamasını gevşetmeyi bu senaryonun varyantı yapmayın; doğrulama bir koruma adımıdır, alanın kaldırılıp kaldırılamayacağı ayrıca sorulur.
- Gerekçeyi yayımlanan aydınlatma metninde yer almayan bir amaçla yazmayın; cümle hukuk ve uyum onayından geçmeden yayına girmez.
- “Bilginiz kimseyle paylaşılmaz” gibi doğrulanmamış bir güvenceyi gerekçe satırına katmayın; güvence ayrı bir değişkendir ve gerçek veri akışına uymak zorundadır.
- Gerekçe satırını açık rıza ya da ticari ileti izni kutusunun yanına koyup izni vermeye yönlendiren bir metne dönüştürmeyin.

### EN

On an insurance or pension pre-quote form, an ID number or date of birth field weighs heavily on a visitor who has not even seen a price yet: with the question “why do they want this now?” unanswered, the form is abandoned there. Removing the field is often not possible because the quote is calculated from this information; one of the middle-ground approaches tried instead of removing it is giving a rationale, writing next to the field what the information will be used for (“We need this to calculate your premium by age”). The risk: if the rationale does not match the published privacy notice exactly, it becomes misleading; it can also raise a concern the visitor had not thought of. How it differs from the “Does adding a “why we ask” note next to a field get a field with an unclear purpose filled in?” scenario (`saas-b2b.md`): there the field is a non-sensitive qualifying question and what is measured is whether that field gets filled; here the field is mandatory and sensitive, the wording of the rationale is bound by personal data rules, and what is measured is getting a quote.

**What to test**
- Presence: With the rationale line added, does the share of visitors who submit the pre-quote form and ask for a quote rise?
- Field level: Does the share of those who reach the ID number field and abandon the form there decrease?
- Backfire: Does the rationale raise hesitation in visitors who would have filled the field without questioning it, and lengthen fill time?
- Segment: Do first-time visitors from ads react to the rationale differently from existing customers?

**KPIs to track**
- Lead Submission Rate (per visitor assigned to the pre-quote form): Does the share of visitors who submit the form and ask for a quote rise?
- Field-Level Abandonment Rate: The share who leave the form at the ID number field; diagnostic metric.
- Validation Error Rate: Invalid or unverifiable number entries must not rise.
- Contract Rate (90 days): The share of visitors assigned to the pre-quote form who complete a contract or policy within the window must not drop; if the rationale increases quote requests but brings requests that do not turn into contracts, it shows up here.
- Quote-to-Contract Rate (90 days): Diagnostic metric; because the number of visitors who get a quote can differ in B, it does not pick the winner and does not replace the guardrail.
- Data Complaint Rate: Requests and complaints about the use of personal data must not rise.

**What not to do**
- Don’t change the field’s requirement, order or label in the same test as adding the rationale line.
- Don’t make removing the field or loosening identity verification a variant of this scenario; verification is a protection step, and whether the field can be removed is a separate question.
- Don’t write the rationale for a purpose that does not appear in the published privacy notice; the sentence does not go live without legal and compliance sign-off.
- Don’t add an unverified assurance such as “Your information is never shared” to the rationale line; assurance is a separate variable and must match the real data flow.
- Don’t place the rationale line next to an explicit consent or commercial-message permission box or turn it into wording that steers people toward giving consent.

---

## Teklif akışındaki adım göstergesinde numaraların yanına adım adlarını yazmak sözleşmeye ulaşmayı artırır mı?

Değişken: Adım göstergesindeki adım etiketleri · Fark: değiştir

Etiket: id=fp-008 · mercek=Netlik · düzey=bilgi · sektör=finans · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does writing step names next to the numbers in a quote flow’s step indicator raise contract completion?

EN-Variable: Step labels in the step indicator

Teklif akışında yalnızca numara gösteren bir gösterge (“2 / 4”) kullanıcıya kaçıncı adımda olduğunu söyler ama sırada ne olduğunu söylemez: fiyatı hangi adımda alacağını, ödemenin ne zaman isteneceğini bilmeyen kullanıcı kişisel bilgi vermeye isteksiz davranır. Numaraların yanına adımların adını yazmak (“1 Bilgiler, 2 Teminat, 3 Teklif, 4 Onay”) yolu önceden gösterir; fiyatın üçüncü adımda geleceğini bilen kullanıcı ilk iki adımı bitirmeye daha yatkın olabilir. Riski: adlar akışı olduğundan uzun gösterebilir ve dar ekranda sığmayıp kırpılır. “İlerleme çubuğu tamamlama oranını artırıyor mu?” (`cart-checkout.md`) senaryosundan farkı: orada göstergenin kendisi eklenir, burada gösterge iki kolda da vardır ve yalnızca adımların adlandırılması değişir.

**Test edilmesi gerekenler**
- Adlandırma: Adım adları yazan gösterge, yalnızca numara gösteren göstergeye göre akışı sözleşmeyle bitirenlerin payını artırıyor mu?
- Fiyat beklentisi: Fiyatın hangi adımda geleceğini adından öğrenen kullanıcı ilk adımdaki kişisel bilgileri daha mı çok tamamlıyor?
- Geri dönüş: Adlı göstergede önceki adıma dönüp bilgi düzeltme sıklığı değişiyor mu?
- Sonraki test: Adlandırma kazanırsa, biten adımların göstergeden tıklanabilir olması ayrı bir testte tamamlamayı artırıyor mu?
- Cihaz: Dar ekranda dört adım adı tek satıra sığıyor mu, yoksa mobilde kırpılan adlar etkiyi siliyor mu?

**Takip edilecek ana KPI’lar**
- Sözleşme Oranı (30 gün): Teklif akışına atanan ziyaretçilerden pencerede sözleşmeyi ya da poliçeyi tamamlayanların payı artıyor mu? Gösterge teklif ekranından önceki adımlarda da durduğu için payda teklif alanlar değil, atanan ziyaretçidir.
- Teklif Görüntüleme Oranı: Fiyatın gösterildiği adıma ulaşanların payı; tanı metriği.
- Adım Bazlı Terk Oranı: Hangi adımda bırakıldığını gösteren tanı metriği.
- Cayma Süresi İçinde İptal Oranı (yasal cayma süresi): Adlı göstergeyle biten sözleşmelerde cayma artmamalı.
- Erişilebilirlik: Adım adları ekran okuyucuda sırayla okunmalı; etkin adımın yalnızca renkle ayrılması kabul edilmemeli.

**Yapılmaması gerekenler**
- Aynı testte adım adlarını yazarken adımların sayısını, sırasını veya adımlardaki alanları birlikte değiştirmeyin.
- Bilgilendirme formu, onay veya kimlik doğrulama adımını göstergede gizlemeyin ya da başka bir adın altına saklamayın; zorunlu adımlar adıyla görünür ve akışta aynen kalır.
- Göstergede yazmayan bir adımı (ör. ödeme) akışın sonunda sürpriz olarak çıkarmayın; adlar gerçek akışla birebir örtüşür.
- Adım adına “Ücretsiz teklif” ya da “Anında onay” gibi doğrulanmamış bir vaat yazmayın; ad yalnızca adımın işini söyler ve uyum onayından geçer.
- Adım adlarını dar ekranda okunmayacak kadar küçültmeyin veya üç noktayla kırpılmış bırakmayın.

### EN

An indicator that shows only numbers in a quote flow (“2 / 4”) tells the user which step they are on but not what comes next: a user who does not know at which step they will see the price, or when payment will be asked for, is reluctant to give personal information. Writing step names next to the numbers (“1 Details, 2 Coverage, 3 Quote, 4 Confirmation”) shows the path in advance; a user who knows the price arrives at step three may be more inclined to finish the first two. The risk: names can make the flow look longer than it is and get truncated when they do not fit on a narrow screen. How it differs from the “Does a progress bar raise completion?” scenario (`cart-checkout.md`): there the indicator itself is added, while here the indicator is present in both arms and only the naming of the steps changes.

**What to test**
- Naming: Does the indicator with step names raise the share who finish the flow with a contract compared with the numbers-only indicator?
- Price expectation: Does a user who learns from the names at which step the price comes complete more of the personal information in the first step?
- Going back: Does how often users go back to a previous step to correct information change with the named indicator?
- Next test: If naming wins, does making completed steps clickable in the indicator raise completion in a separate test?
- Device: On a narrow screen, do four step names fit on one line, or do names truncated on mobile erase the effect?

**KPIs to track**
- Contract Rate (30 days): Does the share of visitors assigned to the quote flow who complete a contract or policy within the window rise? Because the indicator also appears in the steps before the quote screen, the denominator is assigned visitors, not those who get a quote.
- Quote View Rate: The share who reach the step where the price is shown; diagnostic metric.
- Step-Level Abandonment Rate: Diagnostic metric showing at which step people leave.
- Cooling-off Cancellation Rate (statutory cooling-off period): Cancellations must not rise on contracts completed with the named indicator.
- Accessibility Check: Step names must be read in order by a screen reader; marking the active step by color alone is not acceptable.

**What not to do**
- Don’t change the number, order or fields of the steps in the same test as writing the step names.
- Don’t hide the disclosure form, confirmation or identity verification step in the indicator or tuck it under another name; mandatory steps appear by name and stay in the flow as they are.
- Don’t spring a step that the indicator does not list (e.g. payment) on the user at the end of the flow; the names match the real flow exactly.
- Don’t put an unverified promise such as “Free quote” or “Instant approval” in a step name; a name only says the step’s job and goes through compliance sign-off.
- Don’t shrink step names to unreadable size on a narrow screen or leave them truncated with an ellipsis.

---

## Hesaplama aracını müşterinin mevcut sözleşme verisiyle dolu açmak hesaplamayı tamamlatır mı?

Değişken: Hesaplama aracındaki alanların başlangıç değeri · Fark: değiştir

Etiket: id=fp-009 · mercek=Çaba · düzey=sürtünme · sektör=finans · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does opening the calculator prefilled with the customer’s existing contract data get the calculation finished?

EN-Variable: Initial values of the fields in the calculator

Giriş yapmış müşteri uygulamadaki birikim hesaplama aracını açtığında yaş, aylık katkı payı ve mevcut birikim alanları boş geliyorsa, şirketin zaten bildiği bilgiyi yeniden yazması istenir; çoğu müşteri katkı payı tutarını ezbere bilmez ve araç yarıda kalır. Alanları müşterinin kendi sözleşme verisiyle dolu açmak yazma yükünü kaldırır ve sonucu ilk dokunuşta kişisel kılar. Riski: veri eski ya da yanlış sözleşmeden gelirse sonuç yanlış olur ve müşteri bunu fark etmeyebilir; birden fazla sözleşmesi olan müşteride hangisinin kullanıldığı açık değilse güven zedelenir. Dolu gelen her alan düzenlenebilir kalır; değişen yalnızca başlangıç değeridir. Bu bir benzetim aracıdır: bir işlemin kapsamını önceden seçmekle aynı şey değildir ve hiçbir işlemi başlatmaz.

**Test edilmesi gerekenler**
- Başlangıç değeri: Alanlar sözleşme verisiyle dolu açıldığında hesaplamayı sonuca ulaştıran müşteri payı, boş açılana göre yüksek mi?
- Düzenleme: Dolu gelen değerleri değiştirip farklı bir katkı payıyla yeniden hesaplayan müşteri payı ne kadar?
- Doğruluk: Dolu gelen değerlerin güncel kayıtlarla uyuşmadığı müşteriler aracı yarıda mı bırakıyor?
- Platform: iOS ve Android uygulamasında verinin yüklenme süresi farklıyken dolu başlangıcın etkisi aynı mı?

**Takip edilecek ana KPI’lar**
- Hesaplama Tamamlama Oranı (aracı açan giriş yapmış müşteri başına, iki kolda aynı tetikleyici): Sonuç ekranına ulaşanların payı artıyor mu?
- Katkı Payı Artırma Oranı (30 gün): Hesaplama bir ara adım olduğu için asıl sonuç burada izlenir; artırım yapan müşteri payı düşmemeli, trafik yetiyorsa birincil metrik bu olur.
- Değer Düzenleme Oranı: Dolu gelen alanlardan en az birini değiştirenlerin payı; tanı metriği, B kolunda okunur.
- Hatalı Veri Bildirimi Oranı: Yanlış ya da eski bilgi gösterildiği gerekçesiyle açılan kayıtlar artmamalı.
- Araç Açılış Süresi: Sözleşme verisini çekmek ekranın açılmasını kabul edilemez ölçüde geciktirmemeli.

**Yapılmaması gerekenler**
- Aynı testte alanları dolu açarken alanların sayısını, sırasını veya sonuç ekranının tasarımını birlikte değiştirmeyin.
- Dolu gelen alanları kilitlemeyin; müşteri her değeri değiştirebilir ve değerin hangi sözleşmeden, hangi tarihte alındığı alanın altında yazar.
- Getiri oranı, enflasyon veya devlet katkısı varsayımını müşteri verisi gibi sessizce doldurmayın; varsayımlar uyum onaylı metniyle ayrı gösterilir, yeni oran uydurulmaz.
- Aracı, aydınlatma metninde bildirilmeyen bir amaçla işlenen veriyle doldurmayın (ör. başka şirketteki birikim, tahmini gelir).
- Dolu açılan hesaplamayı müşteri adına başlatılmış bir artırım talebi gibi kaydetmeyin; hesaplama hiçbir işlemi kendiliğinden başlatmaz.

### EN

When a logged-in customer opens the in-app savings calculator and the age, monthly contribution and existing savings fields come up empty, they are asked to retype what the company already knows; most customers do not remember their contribution amount by heart and the tool is abandoned midway. Opening the fields prefilled with the customer’s own contract data removes the typing load and makes the result personal at the first tap. The risk: if the data comes from an old or wrong contract, the result is wrong and the customer may not notice; for a customer with several contracts, trust suffers if it is unclear which one was used. Every prefilled field stays editable; only the initial value changes. This is a simulation tool: it is not the same as preselecting the scope of a transaction, and it starts no transaction.

**What to test**
- Initial value: When the fields open prefilled with contract data, is the share of customers who reach a result higher than when they open empty?
- Editing: What share of customers change the prefilled values and recalculate with a different contribution?
- Accuracy: Do customers whose prefilled values do not match current records abandon the tool midway?
- Platform: Is the effect of the prefilled start the same on iOS and Android, where the data load time differs?

**KPIs to track**
- Calculator Completion Rate (per logged-in customer who opens the tool, same trigger in both arms): Does the share who reach the result screen rise?
- Contribution Increase Rate (30 days): Since the calculation is an intermediate step, the real outcome is tracked here; the share of customers who make an increase must not drop, and with enough traffic this becomes the primary metric.
- Value Edit Rate: The share who change at least one of the prefilled fields; diagnostic metric, read in arm B.
- Incorrect Data Report Rate: Cases opened because wrong or outdated information was shown must not rise.
- Tool Open Time: Fetching the contract data must not delay the screen opening to an unacceptable degree.

**What not to do**
- Don’t change the number or order of the fields or the design of the result screen in the same test as prefilling them.
- Don’t lock the prefilled fields; the customer can change every value, and which contract and what date the value came from is written under the field.
- Don’t silently fill a return rate, inflation or government contribution assumption as if it were customer data; assumptions are shown separately with the compliance-approved text, and no new rate is invented.
- Don’t fill the tool with data processed for a purpose not stated in the privacy notice (e.g. savings at another company, estimated income).
- Don’t record the prefilled calculation as an increase request started on the customer’s behalf; the calculation starts no transaction on its own.

---

## “Sizi arayalım” formuna talepten sonra kimin, hangi kanaldan döneceğini yazmak talebi artırır mı?

Değişken: Talep formundaki sonraki adım satırı · Fark: ekle

Etiket: id=fp-010 · mercek=Netlik · düzey=bilgi · sektör=finans · pazar=global · emek=düşük · durum=güncel · tarih=2026-11

EN: Does stating on a “Call me back” form who will get back to you, and through which channel, raise requests?

EN-Variable: Next-step line on the request form

“Sizi arayalım” formu ad ve telefon ister ama gönderdikten sonra ne olacağını söylemez: kim arayacak, hangi kanaldan, ne için? Belirsizlik iki yerde kayıp yaratır: bilinmeyen bir satış aramasından çekinen ziyaretçi formu göndermez, gönderen ise tanımadığı numarayı açmaz. Butonun üstüne sürecin gerçekte nasıl işlediğini söyleyen tek satır (“Müşteri danışmanımız sizi telefonla arar ve sorularınızı yanıtlar”) eklemek beklentiyi kurar. Riski: satır şirketin gerçekten yürütmediği bir süreci anlatırsa vaat tutulmaz ve şikâyete dönüşür; arama fikri netleşince bazı ziyaretçiler de vazgeçebilir.

**Test edilmesi gerekenler**
- Varlık: Sonraki adımı söyleyen satır eklenince formu gönderenlerin payı artıyor mu?
- Ulaşılabilirlik: Satırlı formdan talep bırakan ziyaretçi danışmanın ilk aramasını daha mı çok açıyor?
- Caydırma: Aranacağını açıkça öğrenen ziyaretçilerin bir kısmı formu göndermekten vazgeçiyor mu?
- Sonraki test: Satır kazanırsa, aranmak istenen zaman dilimini seçtirmek ayrı bir testte ulaşılan talebi artırıyor mu?
- Mobil: Uygulamadaki form ile mobil web formunda satırın etkisi aynı mı?

**Takip edilecek ana KPI’lar**
- Talep Oluşturma Oranı (form ekranına atanan ziyaretçi başına): Formu gönderenlerin payı artıyor mu?
- Talebe Ulaşma Oranı: Danışmanın ilan edilen deneme sayısı içinde ulaşabildiği taleplerin payı düşmemeli.
- Görüşmeden Teklife Geçiş Oranı: Ulaşılan taleplerin kaçı teklif aşamasına ilerliyor?
- Arama Şikâyeti Oranı: “Aranmadım” ya da “istemediğim hâlde arandım” şikâyetleri artmamalı.
- İleti İzni Geri Çekme Oranı (90 gün): Talep bırakanların iletişim iznini geri çekme payı yükselmemeli.

**Yapılmaması gerekenler**
- Ölçülmemiş bir geri dönüş süresi vaat etmeyin (“10 dakika içinde arıyoruz”); süre ancak çağrı kayıtlarıyla doğrulanmış ve her talepte tutulabiliyorsa yazılır.
- Satırda şirketin gerçekte yürütmediği bir süreci anlatmayın; arayan dış arama ekibiyse ya da ilk temas SMS ise satır bunu söyler ve uyum onayından geçer.
- Aynı testte sonraki adım satırını eklerken form alanlarını veya buton metnini birlikte değiştirmeyin.
- Satırı iletişim izni ve aydınlatma metninin yerine koymayın, izin kutusunu önceden işaretlemeyin; izin metni onaylı hâliyle aynen kalır.
- “Danışmanlarımız şu an müsait” gibi gerçek zamanlı veriye dayanmayan bir doluluk ya da aciliyet sinyali eklemeyin.

### EN

A “Call me back” form asks for a name and phone number but does not say what happens after sending: who will call, through which channel, and about what? The uncertainty loses people in two places: a visitor wary of an unknown sales call does not submit the form, and one who does submit does not pick up a number they do not recognise. Adding a single line above the button that says how the process really works (“Our customer advisor will call you by phone and answer your questions”) sets the expectation. The risk: if the line describes a process the company does not actually run, the promise is not kept and turns into complaints; and once the idea of being called becomes clear, some visitors may back out.

**What to test**
- Presence: With the line stating the next step added, does the share of visitors who submit the form rise?
- Reachability: Do visitors who leave a request through the form with the line pick up the advisor’s first call more often?
- Deterrence: Do some visitors who learn plainly that they will be called give up on submitting the form?
- Next test: If the line wins, does letting people choose the time slot they want to be called in raise the number of requests reached in a separate test?
- Mobile: Is the line’s effect the same on the in-app form and the mobile web form?

**KPIs to track**
- Lead Submission Rate (per visitor assigned to the form screen): Does the share of visitors who submit the form rise?
- Lead Contact Rate: The share of requests the advisor can reach within the stated number of attempts must not drop.
- Call-to-Quote Rate: Of the requests reached, how many move on to the quote stage?
- Call Complaint Rate: Complaints of “I was not called” or “I was called although I did not want it” must not rise.
- Consent Withdrawal Rate (90 days): The share of people who leave a request and then withdraw their contact consent must not rise.

**What not to do**
- Don’t promise a callback time that has not been measured (“We call within 10 minutes”); a time is written only if it is verified with call logs and can be kept on every request.
- Don’t describe in the line a process the company does not actually run; if the caller is an outside calling team or the first contact is an SMS, the line says so and goes through compliance sign-off.
- Don’t change the form fields or the button text in the same test as adding the next-step line.
- Don’t use the line in place of the contact consent and privacy notice, and don’t preselect the consent box; the consent text stays exactly as approved.
- Don’t add an availability or urgency signal that is not based on real-time data, such as “Our advisors are available right now”.

