# Dashboard (Sürekli Kullanılan Ana Ekran)

Yolculuk aşaması: kullanıcı zaten kayıtlı ve düzenli olarak geri dönüp kullandığı ana ekran — ilk açılış/onboarding (`mobile-app.md`) veya pazarlama ana sayfası (`home-landing.md`) değil, tekrar eden kullanımın kendisi. Boş durum (henüz veri/aktivite yokken ekranın görünümü) burada kritik bir alt konudur. Her KPI listesinin ilk maddesi birincil metriktir; listede en az bir madde bozulmaması gereken guardrail’dir.

---

## Boş durumda (henüz veri yokken) yönlendirici bir aksiyon kartı göstermek etkileşimi artırır mı?

Yeni kaydolan bir kullanıcı dashboard’u ilk açtığında ekran genelde boştur — grafik, liste veya widget’ları dolduracak veri henüz yoktur. Boş bir tablo veya “veri yok” mesajı kullanıcıyı ne yapması gerektiği konusunda yalnız bırakır; somut bir sonraki-aksiyon kartı bu boşluğu bir davete çevirebilir.

**Test edilmesi gerekenler**
- İçerik: Genel “başlayın” mesajı mı, kullanıcının kurulumunda eksik kalan spesifik adım mı daha çok tıklanıyor?
- Sayı: Tek bir öncelikli aksiyon mu, sıralı bir kontrol listesi mi daha çok tamamlanıyor?
- Görsel: Boş durumda illüstrasyon kullanmak mesajın okunma oranını değiştiriyor mu?
- Israrcılık: Kart ilk veri geldikten sonra ne zaman kaybolmalı?
- Segment: Kendi başına kaydolan ile davetle eklenen kullanıcıya farklı bir boş-durum mesajı mı gerekiyor?

**Takip edilecek ana KPI’lar**
- İlk Aksiyon Tamamlama Oranı: Boş durumdaki öneriyi takip eden kullanıcı oranı artıyor mu?
- Kurulum Tamamlama Süresi: İlk anlamlı veriye ulaşma süresi kısalıyor mu?
- 7 Günlük Aktif Kullanım: Boş durumu geçen kullanıcıların bir hafta sonraki dönüş oranı düşmemeli.
- Destek Talebi: “Nereden başlamalıyım” soruları artmamalı.
- Kartı Kapatma Oranı: Kart rahatsız edici bulunup hemen kapatılmamalı.

**Yapılmaması gerekenler**
- Kullanıcının henüz vermediği bir veriyi varsayıp örnek olarak göstermeyin; gerçek olmayan veriyi gerçekmiş gibi sunmayın.
- Aynı testte boş-durum mesajının içeriğini ve görsel biçimini birlikte değiştirmeyin.
- Kartı kapatılamaz hâle getirmeyin; kullanıcı isterse boş durumu görmezden gelebilmeli.
- Aksiyonu tamamlamadan diğer özelliklere erişimi kısıtlamayın — bu bir yönlendirme kartıdır, bir kilit değil.
- Farklı kullanıcı segmentlerine gösterilen örnek verileri birbirine karıştırmayın.

---

## Dashboard’da en son kullanılan widget’ı öne almak etkileşimi artırır mı?

Sabit bir widget sırası her kullanıcıya aynı düzeni sunar ve öngörülebilirdir, ama çoğu kullanıcının asıl ilgilendiği widget sayfanın altında kalabilir. Kullanım geçmişine göre sıralamak ilgiyi öne çıkarır, ama düzenin sürekli değişmesi kullanıcının “her şeyin yerini bildiği” hissini bozabilir.

**Test edilmesi gerekenler**
- Sıralama mantığı: En son kullanılan mı, en sık kullanılan mı daha iyi bir sıralama üretiyor?
- Kararlılık: Sıra her oturumda mı, haftada bir mi güncellenmeli?
- Farkındalık: Kullanıcı sıranın değiştiğini fark edip kafası mı karışıyor?
- Az kullanılan widget: Hiç etkileşim almayan widget’lar tamamen kaybolduğunda bu fark ediliyor mu?
- Cihaz: Mobilde dar ekranda kişiselleştirilmiş sıralama masaüstünden farklı mı çalışıyor?

**Takip edilecek ana KPI’lar**
- Widget Etkileşim Oranı: Bir oturumda etkileşime giren widget sayısı artıyor mu?
- Ana Görev Tamamlama Süresi: Kullanıcı asıl aradığı bilgiye daha hızlı ulaşıyor mu?
- Kayıp Widget Şikâyeti: “Şu widget nereye gitti” destek talebi artmamalı.
- Ayarları Sıfırlama Oranı: Kullanıcı sabit sıraya dönmeyi seçmemeli.
- Sayfa Yüklenme Süresi: Kişiselleştirme mantığı sayfayı yavaşlatmamalı.

**Yapılmaması gerekenler**
- Aynı testte sıralama mantığını (en son/en sık) ve güncelleme sıklığını birlikte değiştirmeyin.
- Kullanıcının manuel olarak sabitlediği bir widget’ı algoritmik sıralamayla yeniden taşımayın.
- Az kullanılan ama kritik bir widget’ı (ör. faturalandırma uyarısı) sırf düşük etkileşimli diye tamamen gizlemeyin — kritik bilgi guardrail’dir.
- Sıralamayı kullanıcının paylaşmadığı verilerden türetmeyin, yalnızca gözlemlenen kullanım verisini kullanın.
- Kişiselleştirmeyi kapatma seçeneği sunmadan zorunlu hâle getirmeyin.

---

## Kullanılmayan bir özelliği dashboard’da tek seferlik bir ipucu kartıyla tanıtmak kullanımını artırır mı?

Bir ürünün değerli ama az bilinen bir özelliği, arayüzde durduğu hâlde kullanıcı tarafından hiç keşfedilmeyebilir. Tek seferlik, kapatılabilir bir ipucu kartı bu özelliği görünür kılabilir, ama sık tekrarlanan veya çok sayıda ipucu “bildirim yorgunluğu” yaratıp asıl işe odaklanmayı bozar.

**Test edilmesi gerekenler**
- İçerik: Özelliğin ne işe yaradığını mı, nasıl kullanılacağını mı anlatmak daha çok denenmeye yol açıyor?
- Zamanlama: İpucu ilk oturumda mı, kullanıcı belirli bir eşiğe ulaştıktan sonra mı daha etkili?
- Sayı: Aynı anda birden fazla ipucu göstermek mi, sırayla tek tek göstermek mi daha çok denenmeye yol açıyor?
- Kalıcılık: Kapatılan ipucu bir daha hiç mi çıkmamalı, yoksa belirli bir süre sonra mı tekrar sorulmalı?
- Segment: Yeni kullanıcı ile uzun süredir aktif olan kullanıcıya aynı ipucu mu gösterilmeli?

**Takip edilecek ana KPI’lar**
- Özellik Deneme Oranı: İpucunu görüp özelliği ilk kez deneyen kullanıcı oranı artıyor mu?
- Özelliği Tekrar Kullanma Oranı: Bir kez deneyen kullanıcı özelliği tekrar kullanıyor mu?
- Ana Görev Tamamlama Süresi: İpucu, kullanıcının o an yapmaya çalıştığı asıl işi yavaşlatmamalı.
- İpucu Kapatma Oranı: İpucu rahatsız edici bulunup anında kapatılmamalı.
- Destek Talebi: İpucu kaynaklı kafa karışıklığı destek talebini artırmamalı.

**Yapılmaması gerekenler**
- Aynı testte ipucunun içeriğini ve gösterim zamanlamasını birlikte değiştirmeyin.
- Kullanıcı ipucunu kapattıktan sonra aynı oturumda tekrar göstermeyin.
- İpucunu, kullanıcının o an yapmakta olduğu asıl görevi engelleyecek şekilde kurmayın.
- Birden fazla ipucunu aynı anda üst üste yığmayın; sırayla ve tek tek gösterin.
- Kullanım verisine dayanmayan bir varsayımla ipucu hedefleme mantığı kurmayın; gerçek kullanım geçmişine dayanmalı.