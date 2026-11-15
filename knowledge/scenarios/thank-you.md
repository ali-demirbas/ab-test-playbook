# Teşekkür ve Sipariş Onay Sayfası

Yolculuk aşaması: satın alma veya kayıt tamamlandıktan hemen sonraki an. Kullanıcı zaten dönüştü; bu sayfa yeni bir dönüşüm hunisi değil, ek değer (çapraz satış, hesap oluşturma, referans) için nadir bir dikkat penceresidir. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Sipariş onay sayfasında ilgili ürün önerisi göstermek ek satın alma yaratır mı?

Değişken: Onay sayfasındaki ürün önerisi şeridi · Fark: ekle

Etiket: id=ty-001 · mercek=Zamanlama · düzey=elde-tutma · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing related product recommendations on the order confirmation page create add-on purchases?

EN-Variable: Product recommendation strip on the confirmation page

Kullanıcı zaten ödeme yaptı, kart bilgisi elinde ve satın alma kararı tazeyken tekrar sürtünmeden geçmiş olur; bu, ikinci bir satın almayı önermek için nadir bir andır. Risk, önerinin asıl siparişin teslimat/onay bilgisini gölgelemesi veya kullanıcının “az önce ödedim, şimdi mi” hissiyle rahatsız olmasıdır.

**Test edilmesi gerekenler**
- Gölgeleme: Öneri şeridi eklenince kullanıcı sipariş numarasını ve teslimat tarihini bulmakta zorlanıyor mu?
- Sonraki test: Öneri şeridi kazanırsa, ilişkili ürün ile genel popüler ürün seçim mantığı ayrı bir testte karşılaştırıldığında hangisi daha çok tıklanıyor?
- Sayı: Tek ürün mü, birkaç seçenekli bir şerit mi daha çok satın alma yaratıyor?
- Pişmanlık etkisi: Öneri şeridini gören kullanıcıda asıl sipariş için iptal veya iade talebi artıyor mu?
- Cihaz: Şeridin sipariş bilgisinin altında kaldığı mobilde, şeridi görüp tıklayan kullanıcı oranı masaüstünden ne kadar düşük?

**Takip edilecek ana KPI’lar**
- Ek Satın Alma Oranı: Teşekkür sayfasından yeni bir sipariş başlatan kullanıcı oranı artıyor mu?
- Ek Sipariş Ortalama Tutarı: Yeni siparişlerin ortalama tutarı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Kullanıcı asıl sipariş numarasını ve teslimat bilgisini bulabilmeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Destek Talebi: “Siparişimi nasıl takip ederim” soruları artmamalı.
- İade veya İptal Oranı (30 gün): Öneri şeridi asıl siparişte iptal veya iade talebini artırmamalı.

**Yapılmaması gerekenler**
- Öneriyi, asıl siparişin teslimat tarihi veya sipariş numarasının önüne geçirip gizlemeyin.
- Aynı testte öneri şeridinin varlığı ile ürün seçim mantığını (ilişkili/genel) birlikte değiştirmeyin.
- Kullanıcıyı ikinci bir ödeme adımına yönlendirip asıl siparişin tamamlandığı hissini bulanıklaştırmayın.
- Misafir ödemesi yapan kullanıcıya bu ekranda ayrıca hesap oluşturmayı da aynı anda önermeyin; bu ayrı bir test değişkenidir.
- Öneri şeridini kapatılamaz veya sipariş onayını okumadan geçilemez hâle getirmeyin.

### EN

The user has already paid, has the card at hand and the purchase decision is fresh, so they are past the friction again; this is a rare moment to suggest a second purchase. The risk is that the recommendation overshadows the delivery and confirmation details of the actual order, or that the user is put off by the feeling of “I just paid, and now this?”.

**What to test**
- Overshadowing: Once the recommendation strip is added, do users struggle to find their order number and delivery date?
- Next test: If the recommendation strip wins, which one gets more clicks when the related-product and general popular-product selection logic are compared in a separate test?
- Count: Does a single product or a strip with several options create more purchases?
- Regret effect: Do cancellation or return requests for the original order increase among users who see the recommendation strip?
- Device: On mobile, where the strip sits below the order details, how much lower is the share of users who see and click the strip than on desktop?

**KPIs to track**
- Post-Purchase Add-on Rate: Does the share of users who start a new order from the thank-you page increase?
- Average Add-on Order Value: What is the average value of the new orders?
- Order Information Visibility (survey): Users must be able to find the original order number and delivery information. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Support Contact Rate: “How do I track my order” questions must not increase.
- Return or Cancellation Rate (30 days): The recommendation strip must not increase cancellation or return requests on the original order.

**What not to do**
- Don’t let the recommendation push ahead of and hide the delivery date or order number of the original order.
- Don’t change the presence of the recommendation strip and the product selection logic (related versus general) in the same test.
- Don’t send the user into a second payment step and blur the sense that the original order is complete.
- Don’t also invite guest checkout users to create an account on this screen at the same time; that is a separate test variable.
- Don’t make the recommendation strip impossible to dismiss, or make the screen impossible to pass without reading the order confirmation.

---

## Misafir olarak ödeme yapana teşekkür sayfasında hesap oluşturma daveti göstermek kayıt oranını artırır mı?

Değişken: Teşekkür sayfasındaki hesap oluşturma daveti · Fark: ekle

Etiket: id=ty-002 · mercek=Zamanlama · düzey=elde-tutma · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does inviting guest buyers to create an account on the thank-you page raise sign-ups?

EN-Variable: Account-creation invitation on the thank-you page

Misafir ödemesi checkout sürtünmesini azaltır ama işletmeyi tekrar iletişim kurabileceği bir hesaptan mahrum bırakır. Sipariş tamamlandıktan hemen sonra, bilgiler zaten girilmişken hesap oluşturmayı önermek, checkout öncesinde zorunlu kayıt istemekten farklı bir sürtünme profiline sahiptir; kullanıcı artık kaybedecek bir dönüşümü riske atmıyor.

**Test edilmesi gerekenler**
- Hesap kullanımı: Davetle açılan hesaplara ilk ay içinde tekrar giriş yapılıyor mu, yoksa hesaplar açılıp unutuluyor mu?
- Sonraki test: Davet kazanırsa, siparişte verilen e-posta bilgisinin davet formunda hazır gelmesi ayrı bir testte kayıt oranını artırıyor mu?
- Zorunluluk: Daveti reddetmek gelecekteki alışverişi zorlaştırıyor mu, yoksa nötr mü?
- Sipariş algısı: Daveti gören kullanıcı siparişin tamamlandığından emin oluyor mu, yoksa hesap açmazsa siparişin geçersiz kalacağını mı düşünüyor?
- Segment: İlk kez alışveriş yapan ile daha önce misafir olarak alışveriş yapmış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Kayıt Oranı: Misafir ödemesi yapıp hesap oluşturan kullanıcı oranı artıyor mu?
- Tekrar Satın Alma Oranı (60 gün): Misafir alıcıların ilan edilen pencerede (ör. 60 gün) yeniden sipariş verme oranı artıyor mu?
- Sipariş Netliği (anket): Davet, siparişin tamamlandığı algısını bulanıklaştırmamalı. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- E-posta Onay Oranı: Hesap oluşturma sürecinde bırakma artmamalı.
- Destek Talebi: “Siparişim nereye gitti, hesabım var mı” karışıklığı artmamalı.

**Yapılmaması gerekenler**
- Hesap oluşturmayı, sipariş onayını görmenin ön koşulu hâline getirmeyin; sipariş bilgisi davetten bağımsız her zaman görünür olmalı.
- Aynı testte davet metnini ve ön doldurma davranışını birlikte değiştirmeyin.
- Kullanıcı reddettiğinde bir daha aynı oturumda tekrar sormayın.
- Misafir ödemesini bu test yüzünden zorlaştırmayın; checkout akışının kendisine dokunmayın.
- Kullanıcının açıkça vermediği bir bilgiyle hesabı önceden doldurmayın.

### EN

Guest checkout reduces checkout friction but leaves the business without an account it can contact again. Offering account creation right after the order is complete, with the details already entered, has a different friction profile from demanding registration before checkout; the user is no longer risking a conversion they could lose.

**What to test**
- Account usage: Do accounts opened through the invitation log in again within the first month, or are they opened and forgotten?
- Next test: If the invitation wins, does pre-filling the email given in the order into the invitation form raise the sign-up rate in a separate test?
- Obligation: Does declining the invitation make future purchases harder, or is it neutral?
- Order perception: Do users who see the invitation feel sure the order is complete, or do they think the order will be invalid if they don’t open an account?
- Segment: Do first-time shoppers and users who have shopped as a guest before react differently?

**KPIs to track**
- Sign-up Rate: Does the share of guest checkout users who create an account increase?
- Repeat Purchase Rate (60 days): Does the share of guest buyers who place another order within the stated window (for example 60 days) increase?
- Order Clarity (survey): The invitation must not blur the sense that the order is complete. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Email Verification Rate: Drop-off in the account creation process must not increase.
- Support Contact Rate: Confusion such as “where did my order go, do I have an account” must not increase.

**What not to do**
- Don’t make account creation a precondition for seeing the order confirmation; the order information must always be visible regardless of the invitation.
- Don’t change the invitation text and the pre-fill behavior in the same test.
- Don’t ask again in the same session once the user has declined.
- Don’t make guest checkout harder because of this test; don’t touch the checkout flow itself.
- Don’t pre-fill the account with information the user hasn’t explicitly provided.

---

## Teşekkür sayfasında arkadaşını davet et teklifini göstermek paylaşım oranını artırır mı?

Değişken: Arkadaşını davet et kartı · Fark: ekle

Etiket: id=ty-003 · mercek=Zamanlama · düzey=elde-tutma · sektör=e-ticaret · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does showing a refer-a-friend offer on the thank-you page raise sharing?

EN-Variable: Refer-a-friend card

Kullanıcı memnuniyetinin tepe noktası satın alma anının hemen sonrasıdır; referans isteği için davranışsal olarak en uygun an burasıdır. Riski, teklifin asıl sipariş bilgisini gölgelemesi veya ödül teklifi gerçek değilse güven kaybı yaratmasıdır.

**Test edilmesi gerekenler**
- Sonraki test: Davet kartı kazanırsa, ödüllü davet ile ödülsüz basit paylaşım ayrı bir testte karşılaştırıldığında hangisi daha çok tıklanıyor?
- Kanal: Mesajlaşma uygulaması, e-posta veya link kopyalama seçeneklerinden hangisi en çok kullanılıyor?
- Tekrar görme: Daveti önceki siparişlerinde de görmüş müşteride paylaşım oranı, daveti ilk kez görene göre düşüyor mu?
- Davet edilen niteliği: Paylaşılan linkten gelen yeni müşteriler ilk siparişten sonra geri dönüyor mu, yoksa yalnızca ödül için mi geliyor?
- Cihaz: Mesajlaşma uygulamalarının elde olduğu mobilde davet kartı, masaüstüne göre daha mı çok paylaşım başlatıyor?

**Takip edilecek ana KPI’lar**
- Paylaşım Başlatma Oranı: Teşekkür sayfasına ulaşan alıcılar içinde davet paylaşımı başlatanların oranı (A’da diğer yüzeylerden yapılanlar dahil) artıyor mu?
- Referans Dönüşüm Oranı: Paylaşılan linkten gelen yeni müşteri sayısı nedir?
- Sipariş Bilgisi Görünürlüğü (anket): Davet, sipariş bilgisini gölgelememeli. Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Ödül Talep Oranı: Vaat edilen ödül gerçekten talep edilip kullanılabiliyor mu; edilmiyorsa bu bir bulgudur.
- Brüt Marj: Ödül maliyeti, davetle gelen siparişlerin marjını eritmemeli.

**Yapılmaması gerekenler**
- Vaat edilen ödülü gerçekte vermeyin ya da koşullarını sayfada belirtmeden bırakmayın.
- Aynı testte teşvik türü ile paylaşım kanallarının sırasını birlikte değiştirmeyin.
- Daveti kapatılamaz hâle getirmeyin; kullanıcı sipariş bilgisine daveti görmeden de ulaşabilmeli.
- Kullanıcının rızası olmadan davet linkini otomatik olarak sosyal medyada paylaşmayın.
- Ödül tutarını gerçek maliyeti karşılamayacak kadar düşük tutup büyük vaat gibi sunmayın.

### EN

The peak of customer satisfaction comes right after the purchase, which makes this the behaviorally best moment to ask for a referral. The risk is that the offer overshadows the actual order information, or that it costs trust if the reward on offer isn’t real.

**What to test**
- Next test: If the invitation card wins, which one gets more clicks when an incentivized invitation and a plain, no-reward share are compared in a separate test?
- Channel: Which is used most: the messaging app, email or copy-link option?
- Repeat exposure: Does the sharing rate drop among customers who also saw the invitation on previous orders, compared with those seeing it for the first time?
- Quality of invitees: Do new customers who arrive through the shared link come back after the first order, or do they come only for the reward?
- Device: On mobile, where messaging apps are at hand, does the invitation card start more shares than on desktop?

**KPIs to track**
- Share Start Rate: Does the share of buyers reaching the thank-you page who start an invitation share (in A, including those from other surfaces) increase?
- Referral Conversion Rate: How many new customers arrive through the shared link?
- Order Information Visibility (survey): The invitation must not overshadow the order information. The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Reward Claim Rate: Can the promised reward actually be claimed and used? If it can’t, that is a finding.
- Gross Margin: The reward cost must not erode the margin of orders that come through invitations.

**What not to do**
- Don’t fail to deliver the promised reward, or leave its terms unstated on the page.
- Don’t change the type of incentive and the order of the sharing channels in the same test.
- Don’t make the invitation impossible to dismiss; the user must be able to reach the order information without seeing the invitation.
- Don’t automatically share the invitation link on social media without the user’s consent.
- Don’t set the reward amount too low to cover the real cost and present it as a big promise.

---

## Sipariş onayını rutin bir bilgi ekranı yerine akılda kalıcı bir an olarak tasarlamak sadakati artırır mı?

Değişken: Onay ekranındaki kutlama anı · Fark: ekle

Etiket: id=ty-004 · mercek=Güven · düzey=elde-tutma · sektör=e-ticaret · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does designing the order confirmation as a memorable moment, instead of a routine information screen, raise loyalty?

EN-Variable: Celebration moment on the confirmation screen

Bir deneyim büyük ölçüde en yoğun anına ve nasıl bittiğine göre hatırlanır; sürecin geri kalanı ortalama olsa bile güçlü bir bitiş, deneyimin genel algısını yükseltebilir. Standart bir “siparişiniz alındı” ekranı yerine kısa bir kutlama animasyonu, kişiselleştirilmiş bir teşekkür mesajı veya beklenmedik küçük bir jest, satın alma sürecinin son izlenimini güçlendirebilir.

**Test edilmesi gerekenler**
- Sonraki test: Kutlama anı kazanırsa, kısa bir animasyon ile kişiselleştirilmiş metin ayrı bir testte karşılaştırıldığında hangisi daha akılda kalıcı bulunuyor?
- Fark edilme: Kullanıcılar kutlama anını izliyor mu, yoksa sipariş bilgisine ulaşmak için hemen geçiyor mu?
- Süre: Anın uzunluğu bir noktadan sonra sıkıcı mı geliyor?
- Destek etkisi: Kutlama anı eklenen ekranda “siparişim alındı mı” sorusuyla gelen destek talebi artıyor mu?
- Segment: İlk kez alışveriş yapan ile sadık müşteriye aynı an mı sunulmalı?

**Takip edilecek ana KPI’lar**
- Tekrar Satın Alma Oranı (60 gün): Onay ekranına ulaşan alıcıların ilan edilen pencerede (ör. 60 gün) yeniden sipariş verme oranı artıyor mu?
- Marka Algısı (anket): İkincil sinyal; deneyimin genel algısı standart ekrana göre daha olumlu mu? Payda anketi yanıtlayan ziyaretçidir; yanıt oranı (yanıt veren / atanan ziyaretçi) iki kolda da izlenir, tanısal sinyaldir.
- Sosyal Paylaşım Oranı: Kullanıcı deneyimi kendiliğinden paylaşıyor mu?
- Sipariş Bilgisi Görünürlüğü: Kutlama anı asıl sipariş veya teslimat bilgisinin görünürlüğünü azaltmamalı.
- Sayfa Yüklenme Süresi: Animasyon veya ek görsel sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Kutlama anını, asıl sipariş bilgisini bulmayı zorlaştıracak şekilde tasarlamayın.
- Aynı testte anın biçimini (animasyon/metin) ve kişiselleştirme derecesini birlikte değiştirmeyin.
- Erişilebilirlik araçlarıyla uyumsuz, durdurulamayan bir animasyon kurmayın; hareket azaltma tercihini yok saymayın.
- Her siparişte aynı sürpriz jesti tekrarlayıp sürprizi öngörülebilir hâle getirmeyin.
- Kutlama anını, gerçekleşmemiş bir başarıyı (ör. sahte bir rozet veya ödül) ima edecek şekilde kurmayın.

### EN

An experience is remembered largely by its peak and by how it ends; even if the rest of the process is average, a strong ending can lift the overall impression of the experience. Instead of a standard “your order has been received” screen, a short celebration animation, a personalized thank-you message or an unexpected small gesture can strengthen the final impression of the purchase.

**What to test**
- Next test: If the celebration moment wins, which one is found more memorable when a short animation and personalized text are compared in a separate test?
- Noticing: Do users watch the celebration moment, or do they move on immediately to get to the order information?
- Duration: Beyond what length does the moment start to feel tedious?
- Support effect: Do support requests with the question “was my order received” increase on the screen where the celebration moment is added?
- Segment: Should first-time shoppers and loyal customers be given the same moment?

**KPIs to track**
- Repeat Purchase Rate (60 days): Does the share of buyers reaching the confirmation screen who place another order within the stated window (for example 60 days) increase?
- Brand Perception (survey): A secondary signal; is the overall impression of the experience more positive than with the standard screen? The denominator is the visitors who answer the survey; the response rate (respondents / assigned visitors) is tracked in both arms as a diagnostic signal.
- Social Share Rate: Do users share the experience spontaneously?
- Order Information Visibility: The celebration moment must not reduce the visibility of the actual order or delivery information.
- Page Load Time: The animation or extra visuals must not slow the page down.

**What not to do**
- Don’t design the celebration moment in a way that makes the order information harder to find.
- Don’t change the form of the moment (animation versus text) and the degree of personalization in the same test.
- Don’t build an animation that is incompatible with accessibility tools or can’t be stopped; don’t ignore the reduced-motion preference.
- Don’t repeat the same surprise gesture on every order and make the surprise predictable.
- Don’t build the celebration moment so that it implies an achievement that hasn’t happened (for example a fake badge or reward).

