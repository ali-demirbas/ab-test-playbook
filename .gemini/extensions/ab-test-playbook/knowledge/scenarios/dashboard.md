# Dashboard (Sürekli Kullanılan Ana Ekran)

Yolculuk aşaması: kullanıcı zaten kayıtlı ve düzenli olarak geri dönüp kullandığı ana ekran; ilk açılış/onboarding (`mobile-app.md`) veya pazarlama ana sayfası (`home-landing.md`) değil, tekrar eden kullanımın kendisi. Boş durum (henüz veri/aktivite yokken ekranın görünümü) burada kritik bir alt konudur. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Boş durumda (henüz veri yokken) yönlendirici bir aksiyon kartı göstermek etkileşimi artırır mı?

Değişken: Boş durumdaki aksiyon kartı · Fark: ekle

Etiket: id=db-001 · mercek=Netlik · düzey=onboarding · sektör=saas · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does an action card that guides the user in the empty state (before any data exists) raise engagement?

EN-Variable: Action card in the empty state

Yeni kaydolan bir kullanıcı dashboard’u ilk açtığında ekran genelde boştur; grafik, liste veya widget’ları dolduracak veri henüz yoktur. Boş bir tablo veya “veri yok” mesajı kullanıcıyı ne yapması gerektiği konusunda yalnız bırakır; somut bir sonraki-aksiyon kartı bu boşluğu bir davete çevirebilir.

**Test edilmesi gerekenler**
- Sonraki test: Kart kazanırsa içeriği (genel “başlayın” mesajı / kurulumda eksik kalan spesifik adım) ayrı bir testte karşılaştırıldığında tıklama değişiyor mu?
- Mekanizma: Kartı gören kullanıcı önerilen aksiyonu karttan mı başlatıyor, yoksa menüden aynı aksiyona mı gidiyor?
- Yan etki: Kart, boş dashboard’daki menü ve ayarlar gibi diğer gezinme öğelerine tıklamayı azaltıyor mu?
- Kalıcılık: Kartla ilk aksiyonu tamamlayan kullanıcı ikinci haftada da veri girmeye devam ediyor mu, yoksa etki ilk oturumla mı sınırlı kalıyor?
- Segment: Kendi başına kaydolan ile davetle eklenen kullanıcıda kartın ilk aksiyon tamamlamaya etkisi aynı yönde mi?

**Takip edilecek ana KPI’lar**
- İlk Aksiyon Tamamlama Oranı: Boş dashboard’u açan yeni kullanıcıların (iki kolda aynı tetikleyici) ilk kurulum aksiyonunu tamamlama oranı artıyor mu?
- Kurulum Tamamlama Süresi: İlk anlamlı veriye ulaşma süresi kısalıyor mu?
- 7. Gün Elde Tutma: Boş durumu geçen kullanıcıların bir hafta sonraki dönüş oranı düşmemeli.
- Destek Talebi: “Nereden başlamalıyım” soruları artmamalı.
- Kartı Kapatma Oranı: Kart rahatsız edici bulunup hemen kapatılmamalı.

**Yapılmaması gerekenler**
- Kullanıcının henüz vermediği bir veriyi varsayıp örnek olarak göstermeyin; gerçek olmayan veriyi gerçekmiş gibi sunmayın.
- Aynı testte boş-durum mesajının içeriğini ve görsel biçimini birlikte değiştirmeyin.
- Kartı kapatılamaz hâle getirmeyin; kullanıcı isterse boş durumu görmezden gelebilmeli.
- Aksiyonu tamamlamadan diğer özelliklere erişimi kısıtlamayın; bu bir yönlendirme kartıdır, bir kilit değil.
- Farklı kullanıcı segmentlerine gösterilen örnek verileri birbirine karıştırmayın.

### EN

When a newly signed-up user first opens the dashboard, the screen is usually empty; there is no data yet to fill the charts, lists or widgets. An empty table or a “no data” message leaves the user alone with the question of what to do next; a concrete next-action card can turn that gap into an invitation.

**What to test**
- Next test: If the card wins, does click behavior change when its content (a generic “get started” message versus the specific step still missing from setup) is compared in a separate test?
- Mechanism: Do users who see the card start the suggested action from the card, or do they reach the same action through the menu?
- Side effect: Does the card reduce clicks on other navigation elements, such as the menu and settings, on the empty dashboard?
- Persistence: Do users who complete their first action through the card keep adding data in the second week, or is the effect limited to the first session?
- Segment: Does the card affect first-action completion in the same direction for self-signed-up users and users added by invitation?

**KPIs to track**
- First Action Completion Rate: Does the share of new users who open the empty dashboard (same trigger in both arms) and complete the first setup action increase?
- Setup Completion Time: Does the time to reach the first meaningful data get shorter?
- Day-7 Retention: The return rate one week later among users who move past the empty state must not drop.
- Support Contact Rate: “Where should I start” questions must not increase.
- Card Dismissal Rate: The card must not feel intrusive and be closed right away.

**What not to do**
- Don’t assume data the user hasn’t provided and show it as an example; don’t present non-real data as if it were real.
- Don’t change the content and the visual form of the empty-state message in the same test.
- Don’t make the card impossible to dismiss; users must be able to ignore the empty state if they wish.
- Don’t restrict access to other features until the action is completed; this is a guidance card, not a lock.
- Don’t mix up the sample data shown to different user segments.

---

## Dashboard’da en son kullanılan widget’ı öne almak etkileşimi artırır mı?

Değişken: Widget sıralama mantığı · Fark: değiştir

Etiket: id=db-002 · mercek=Çaba · düzey=kişiselleştirme · sektör=saas · pazar=global · emek=yüksek · durum=güncel · tarih=2026-11

EN: Does moving the most recently used widget to the front of the dashboard raise engagement?

EN-Variable: Widget ordering logic

Sabit bir widget sırası her kullanıcıya aynı düzeni sunar ve öngörülebilirdir, ama çoğu kullanıcının asıl ilgilendiği widget sayfanın altında kalabilir. Kullanım geçmişine göre sıralamak ilgiyi öne çıkarır, ama düzenin sürekli değişmesi kullanıcının “her şeyin yerini bildiği” hissini bozabilir.

**Test edilmesi gerekenler**
- Sonraki test: Kişisel sıralama kazanırsa, en son kullanılan yerine en sık kullanılan widget’ı öne almak ayrı bir testte etkileşimi daha çok artırıyor mu?
- İlk etkileşim: Öne alınan widget, kullanıcının oturumdaki ilk tıklaması oluyor mu?
- Farkındalık: Kullanıcı sıranın değiştiğini fark edip kafası mı karışıyor?
- Az kullanılan widget: Sıranın sonuna düşen widget’lara ihtiyaç duyulduğunda onlara ulaşma süresi uzuyor mu?
- Cihaz: Mobilde dar ekranda kişiselleştirilmiş sıralama masaüstünden farklı mı çalışıyor?

**Takip edilecek ana KPI’lar**
- Widget Etkileşim Oranı: Dashboard oturumlarında en az bir widget’la etkileşilen oturumların payı artıyor mu?
- Görev Tamamlama Süresi (ana görev): Kullanıcı asıl aradığı bilgiye daha hızlı ulaşıyor mu?
- Kayıp Widget Şikâyeti: “Şu widget nereye gitti” destek talebi artmamalı.
- Ayarları Sıfırlama Oranı: Kullanıcı sabit sıraya dönmeyi seçmemeli.
- Sayfa Yüklenme Süresi: Kişiselleştirme mantığı sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Aynı testte sıralama mantığını (en son/en sık) ve güncelleme sıklığını birlikte değiştirmeyin.
- Kullanıcının manuel olarak sabitlediği bir widget’ı algoritmik sıralamayla yeniden taşımayın.
- Az kullanılan ama kritik bir widget’ı (ör. faturalandırma uyarısı) sırf düşük etkileşimli diye tamamen gizlemeyin; kritik bilgi guardrail’dir.
- Sıralamayı kullanıcının paylaşmadığı verilerden türetmeyin, yalnızca gözlemlenen kullanım verisini kullanın.
- Kişiselleştirmeyi kapatma seçeneği sunmadan zorunlu hâle getirmeyin.

### EN

A fixed widget order gives every user the same, predictable layout, but the widget most users actually care about may sit at the bottom of the page. Ordering by usage history brings relevance forward, but a layout that keeps changing can break the user’s sense of knowing where everything is.

**What to test**
- Next test: If the personalized order wins, does moving the most frequently used widget to the front, instead of the most recently used one, raise engagement more in a separate test?
- First interaction: Does the widget moved to the front become the user’s first click in the session?
- Awareness: Do users notice that the order has changed and get confused?
- Rarely used widgets: Does it take longer to reach widgets that drop to the end of the order when they are needed?
- Device: Does personalized ordering work differently on a narrow mobile screen than on desktop?

**KPIs to track**
- Widget Engagement Rate: Does the share of dashboard sessions with at least one widget interaction increase?
- Task Completion Time (primary task): Do users reach the information they actually came for faster?
- Lost-Widget Complaints: “Where did that widget go” support requests must not increase.
- Settings Reset Rate: Users must not choose to return to the fixed order.
- Page Load Time: The personalization logic must not slow the page down.

**What not to do**
- Don’t change the ordering logic (most recent versus most frequent) and the update frequency in the same test.
- Don’t move a widget the user has manually pinned through the algorithmic order.
- Don’t hide a rarely used but critical widget (for example a billing alert) completely just because its engagement is low; critical information is a guardrail.
- Don’t derive the order from data the user hasn’t shared; use only observed usage data.
- Don’t make personalization mandatory without an option to turn it off.

---

## Kullanılmayan bir özelliği dashboard’da tek seferlik bir ipucu kartıyla tanıtmak kullanımını artırır mı?

Değişken: Özelliği tanıtan tek seferlik ipucu kartı · Fark: ekle

Etiket: id=db-003 · mercek=Netlik · düzey=onboarding · sektör=saas · pazar=global · emek=orta · durum=güncel · tarih=2026-11

EN: Does introducing an unused feature with a one-off tip card on the dashboard raise its use?

EN-Variable: One-off tip card introducing a feature

Bir ürünün değerli ama az bilinen bir özelliği, arayüzde durduğu hâlde kullanıcı tarafından hiç keşfedilmeyebilir. Tek seferlik, kapatılabilir bir ipucu kartı bu özelliği görünür kılabilir, ama sık tekrarlanan veya çok sayıda ipucu “bildirim yorgunluğu” yaratıp asıl işe odaklanmayı bozar.

**Test edilmesi gerekenler**
- Sonraki test: İpucu kartı kazanırsa içeriği (özelliğin ne işe yaradığı / nasıl kullanıldığı) ayrı bir testte karşılaştırıldığında deneme oranı değişiyor mu?
- Mekanizma: Özelliği ilk kez deneyenler ipucu kartındaki bağlantıdan mı geliyor, yoksa kartı gördükten sonra özelliği menüden mi buluyor?
- Ek kazanım: Kontrol grubu özelliği zamanla kendi keşfedip ipucu grubuna yetişiyor mu, yoksa fark kalıcı mı?
- Yan etki: İpucu kartının göründüğü oturumda dashboard’daki diğer widget’larla etkileşim azalıyor mu?
- Segment: İpucunun deneme oranına etkisi yeni kullanıcıda mı, uzun süredir aktif olup özelliği hiç kullanmamış kullanıcıda mı daha büyük?

**Takip edilecek ana KPI’lar**
- Özellik Deneme Oranı: Teste atanan kullanıcılardan özelliği ilk kez deneyenlerin oranı artıyor mu? Payda, ipucunun gösterildiği kullanıcılar değil, iki koldaki tüm kullanıcılardır.
- Özelliği Tekrar Kullanma Oranı: Bir kez deneyen kullanıcı özelliği tekrar kullanıyor mu?
- Görev Tamamlama Süresi (ana görev): İpucu, kullanıcının o an yapmaya çalıştığı asıl işi yavaşlatmamalı.
- İpucu Kapatma Oranı: İpucu rahatsız edici bulunup anında kapatılmamalı.
- Destek Talebi: İpucu kaynaklı kafa karışıklığı destek talebini artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte ipucunun içeriğini ve gösterim zamanlamasını birlikte değiştirmeyin.
- Kullanıcı ipucunu kapattıktan sonra aynı oturumda tekrar göstermeyin.
- İpucunu, kullanıcının o an yapmakta olduğu asıl görevi engelleyecek şekilde kurmayın.
- İpucunda özelliğin gerçekte sağlamadığı bir sonucu vaat etmeyin.
- Kullanım verisine dayanmayan bir varsayımla ipucu hedefleme mantığı kurmayın; gerçek kullanım geçmişine dayanmalı.

### EN

A valuable but little-known feature of a product may never be discovered by users even though it sits in the interface. A one-off, dismissible tip card can make the feature visible, but frequently repeated or numerous tips cause “notification fatigue” and disrupt focus on the actual task.

**What to test**
- Next test: If the tip card wins, does the trial rate change when its content (what the feature is for versus how to use it) is compared in a separate test?
- Mechanism: Do users who try the feature for the first time arrive through the link in the tip card, or do they find the feature in the menu after seeing the card?
- Catch-up: Does the control group discover the feature on its own over time and catch up with the tip group, or does the gap persist?
- Side effect: Does interaction with the other dashboard widgets drop in sessions where the tip card appears?
- Segment: Is the tip’s effect on the trial rate larger for new users or for long-time active users who have never used the feature?

**KPIs to track**
- Feature Trial Rate: Does the share of users assigned to the test who try the feature for the first time increase? The denominator is all users in both arms, not the users shown the tip.
- Feature Repeat Usage Rate: Do users who try the feature once use it again?
- Task Completion Time (primary task): The tip must not slow down the main job the user is trying to do at that moment.
- Tip Dismissal Rate: The tip must not feel intrusive and be closed immediately.
- Support Contact Rate: Confusion caused by the tip must not increase support requests.

**What not to do**
- Don’t change the tip’s content and its display timing in the same test.
- Don’t show the tip again in the same session after the user has dismissed it.
- Don’t place the tip so that it blocks the main task the user is doing at that moment.
- Don’t promise in the tip an outcome the feature doesn’t actually deliver.
- Don’t build the tip-targeting logic on an assumption that isn’t based on usage data; it must rest on real usage history.

