# Dashboard (Sürekli Kullanılan Ana Ekran)

Yolculuk aşaması: kullanıcı zaten kayıtlı ve düzenli olarak geri dönüp kullandığı ana ekran; ilk açılış/onboarding (`mobile-app.md`) veya pazarlama ana sayfası (`home-landing.md`) değil, tekrar eden kullanımın kendisi. Boş durum (henüz veri/aktivite yokken ekranın görünümü) burada kritik bir alt konudur. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Boş durumda (henüz veri yokken) yönlendirici bir aksiyon kartı göstermek etkileşimi artırır mı?

Değişken: Boş durumdaki aksiyon kartı · Fark: ekle

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

---

## Dashboard’da en son kullanılan widget’ı öne almak etkileşimi artırır mı?

Değişken: Widget sıralama mantığı · Fark: değiştir

Sabit bir widget sırası her kullanıcıya aynı düzeni sunar ve öngörülebilirdir, ama çoğu kullanıcının asıl ilgilendiği widget sayfanın altında kalabilir. Kullanım geçmişine göre sıralamak ilgiyi öne çıkarır, ama düzenin sürekli değişmesi kullanıcının “her şeyin yerini bildiği” hissini bozabilir.

**Test edilmesi gerekenler**
- Sonraki test: Kişisel sıralama kazanırsa, en son kullanılan yerine en sık kullanılan widget’ı öne almak ayrı bir testte etkileşimi daha çok artırıyor mu?
- İlk etkileşim: Öne alınan widget, kullanıcının oturumdaki ilk tıklaması oluyor mu?
- Farkındalık: Kullanıcı sıranın değiştiğini fark edip kafası mı karışıyor?
- Az kullanılan widget: Sıranın sonuna düşen widget’lara ihtiyaç duyulduğunda onlara ulaşma süresi uzuyor mu?
- Cihaz: Mobilde dar ekranda kişiselleştirilmiş sıralama masaüstünden farklı mı çalışıyor?

**Takip edilecek ana KPI’lar**
- Widget Etkileşim Oranı: Dashboard oturumlarında en az bir widget’la etkileşilen oturumların payı artıyor mu?
- Ana Görev Tamamlama Süresi: Kullanıcı asıl aradığı bilgiye daha hızlı ulaşıyor mu?
- Kayıp Widget Şikâyeti: “Şu widget nereye gitti” destek talebi artmamalı.
- Ayarları Sıfırlama Oranı: Kullanıcı sabit sıraya dönmeyi seçmemeli.
- Sayfa Yüklenme Süresi: Kişiselleştirme mantığı sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Aynı testte sıralama mantığını (en son/en sık) ve güncelleme sıklığını birlikte değiştirmeyin.
- Kullanıcının manuel olarak sabitlediği bir widget’ı algoritmik sıralamayla yeniden taşımayın.
- Az kullanılan ama kritik bir widget’ı (ör. faturalandırma uyarısı) sırf düşük etkileşimli diye tamamen gizlemeyin; kritik bilgi guardrail’dir.
- Sıralamayı kullanıcının paylaşmadığı verilerden türetmeyin, yalnızca gözlemlenen kullanım verisini kullanın.
- Kişiselleştirmeyi kapatma seçeneği sunmadan zorunlu hâle getirmeyin.

---

## Kullanılmayan bir özelliği dashboard’da tek seferlik bir ipucu kartıyla tanıtmak kullanımını artırır mı?

Değişken: Özelliği tanıtan tek seferlik ipucu kartı · Fark: ekle

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
- Ana Görev Tamamlama Süresi: İpucu, kullanıcının o an yapmaya çalıştığı asıl işi yavaşlatmamalı.
- İpucu Kapatma Oranı: İpucu rahatsız edici bulunup anında kapatılmamalı.
- Destek Talebi: İpucu kaynaklı kafa karışıklığı destek talebini artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte ipucunun içeriğini ve gösterim zamanlamasını birlikte değiştirmeyin.
- Kullanıcı ipucunu kapattıktan sonra aynı oturumda tekrar göstermeyin.
- İpucunu, kullanıcının o an yapmakta olduğu asıl görevi engelleyecek şekilde kurmayın.
- İpucunda özelliğin gerçekte sağlamadığı bir sonucu vaat etmeyin.
- Kullanım verisine dayanmayan bir varsayımla ipucu hedefleme mantığı kurmayın; gerçek kullanım geçmişine dayanmalı.