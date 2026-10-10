# Fiyatlandırma ve fiyat sunumu

Yolculuk aşaması: fiyatın görüldüğü an. Hem abonelik fiyat sayfası hem e-ticarette fiyat gösterimi bu dosyadadır. Ticari strateji kararları (plan varsayılanı, kurumsal fiyatın gizlenmesi, deneme süresi) `saas-b2b.md`, indirim ve taksit sunumu `product-detail.md` içindedir; burada fiyatın kendisinin nasıl çerçevelendiği ele alınır.

**Bu dosyadaki tüm senaryolarda birincil metrik gelir bazlıdır.** Fiyatı ucuz göstermek veya seçenek azaltmak dönüşüm oranını neredeyse her zaman artırır ama geliri düşürebilir; bu yüzden Ziyaretçi Başına Gelir (RPV) birincil, dönüşüm oranı ikincil metriktir (`knowledge/methodology.md` → Dönüşüm oranı geliri gizleyebilir). Her KPI listesinde en az bir madde bozulmaması gereken guardrail’dir.

---

## Gösterilen fiyat planı sayısını azaltmak geliri artırır mı?

Değişken: Gösterilen fiyat planı sayısı · Fark: kaldır

Çok sayıda plan farklı ihtiyaçları karşılar ama seçim felcine yol açabilir ve ziyaretçiyi hiçbirini seçmemeye itebilir. Mevcut çok planlı sayfadan (A) en az seçilen planı kaldırmak (B) kararı hızlandırır ve karşılaştırma yükünü azaltır. Plan sayısını değiştirmek aynı zamanda hangi planın ortada kaldığını da değiştirir; bu, seçim dağılımını fiyattan bağımsız olarak kaydırır.

**Test edilmesi gerekenler**
- Sayı: Plan sayısını azaltmak toplam geliri artırıyor mu?
- Dağılım: Hangi plan ne oranda seçiliyor, ortadaki plan avantaj sağlıyor mu?
- Kaybedilen ihtiyaç: Kaldırılan planı seçenler başka plana mı geçiyor, yoksa kayboluyor mu?
- Aşağı kayma: Az seçenek ziyaretçiyi daha ucuz plana mı yönlendiriyor?
- Segment: Bireysel ve kurumsal ziyaretçi farklı sayıda seçeneğe mi ihtiyaç duyuyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Plan sayısı geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Dağılımı: Herhangi bir planı seçen ziyaretçi oranı artıyor mu?
- İptal veya Plan Düşürme Oranı: Yanlış plana yönlenen kullanıcı sonradan düşmemeli.
- Destek Talebi: “Hangi planı almalıyım” soruları artmamalı.

**Yapılmaması gerekenler**
- Aynı testte plan sayısı ile plan fiyatlarını birlikte değiştirmeyin.
- Kaldırdığınız planı fiyat sayfasından çıkarıp ödeme adımında veya doğrudan bağlantıyla satılabilir bırakmayın; kol kirlenir.
- Kaldırdığınız planın mevcut abonelerini test kapsamına almayın.
- Plan sayısını değiştirirken plan içeriklerini de yeniden paketlemeyin.
- Seçenek azaltmayı, aslında satmak istediğiniz planı tek çıkış yolu hâline getirmek için kullanmayın.

---

## Planları karşılaştırma tablosunda mı, ayrı kartlarda mı sunmalı?

Değişken: Plan sunum biçimi · Fark: değiştir

Karşılaştırma tablosu farkları satır satır görünür kılar ve ayrıntılı değerlendirme yapan ziyaretçiye hitap eder. Ayrı kartlar her planı kendi başına bir teklif gibi sunar, hızlı karar verdirir ama farkları gizler. Tablo aynı zamanda ucuz planda eksik olan her şeyi de görünür kılar; bu hem ikna edici hem caydırıcı olabilir.

**Test edilmesi gerekenler**
- Biçim: Tablo mu, kart mı daha yüksek gelir getiriyor?
- Sonraki test: Tablo kazanırsa karşılaştırma satırlarının sayısı ayrı bir testte azaltıldığında plan seçimi artıyor mu?
- Eksiklik vurgusu: Ucuz planda eksik olanları göstermek yukarı mı itiyor, caydırıyor mu?
- Plan dağılımı: Kart biçimi ziyaretçiyi ilk karta mı yığıyor, tablo seçimi daha pahalı planlara mı yayıyor?
- Cihaz: Mobilde tablo yatay kaydırmaya düşüyor mu, kart daha mı iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sunum biçimi geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Dağılımı: Karar veren ziyaretçi oranı artıyor mu?
- Karşılaştırma Etkileşim Oranı: Tablo gerçekten inceleniyor mu?
- Sayfada Kalma Süresi: Karar süresi kabul edilemez ölçüde uzamamalı.

**Yapılmaması gerekenler**
- Aynı testte sunum biçimi ile karşılaştırılan özellik listesini birlikte değiştirmeyin.
- Tabloda ucuz planın eksiklerini abartılı işaretlerle vurgulayıp korku yaratmayın.
- Mobilde tabloyu okunmaz derecede küçültüp kartla karşılaştırmayın.
- Özellik adlarını tabloda ve kartta farklı yazmayın; karşılaştırma bozulur.
- Tabloda gerçekte sunulmayan bir özelliği yer tutucu olarak bırakmayın.

---

## Fiyatı öne çıkarmak mı, faydadan sonra göstermek mi daha iyi çalışıyor?

Değişken: Fiyatın sayfadaki sırası · Fark: taşı

Fiyatı erken göstermek beklentiyi netleştirir ve bütçesi uymayan ziyaretçinin vaktini almaz. Faydayı önce anlatmak, fiyat görüldüğünde algılanan değeri yükseltir. Erken fiyat pahalı algılanan üründe kayıp yaratabilir; geç fiyat ise güvensizlik ve “fiyatı gizliyorlar” hissi doğurabilir.

**Test edilmesi gerekenler**
- Sıra: Fiyat faydadan önce mi, sonra mı gösterilmeli?
- Sonraki test: Kazanan sıra sabitken fiyat puntosunu büyütmek ayrı bir testte algılanan pahalılığı değiştiriyor mu?
- Nitelik: Erken fiyat gelen talebin niteliğini yükseltiyor mu?
- Güven: Fiyatı geciktirmek gizleme algısı yaratıyor mu?
- Segment: Fiyata duyarlı ve değere duyarlı ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sıralama geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Ortalama tutar düşmemeli.
- Dönüşüm Oranı (CR): Satın alan ziyaretçi oranı ne yönde değişiyor?
- Hemen Çıkma Oranı: Erken fiyat çıkışı kabul edilemez ölçüde artırmamalı.
- Talep Başına Nitelik Oranı: Geç fiyat, ödeme gücü olmayan talebi çoğaltmamalı.

**Yapılmaması gerekenler**
- Fiyatı geciktirmeyi, kullanıcı taahhüde girene kadar saklamak için kullanmayın.
- Aynı testte fiyat konumu ile fiyat rakamını birlikte değiştirmeyin.
- Toplam fiyatın bir kısmını (kargo, vergi, kurulum) sonraya bırakıp “fiyat öne alındı” demeyin.
- Yasal olarak fiyatın belirli bir aşamada gösterilmesi gereken pazarlarda kuralı doğrulamadan sıralama değiştirmeyin.
- Fiyat büyütülürken para birimi veya vergi ifadesini küçültmeyin.

---

## Abonelik fiyatını aylık birime bölerek göstermek işe yarar mı?

Değişken: Abonelik fiyatının gösterim birimi · Fark: değiştir

Yıllık bir tutarı aylık karşılığıyla göstermek rakamı küçültür ve giriş engelini düşürür. Buna karşılık toplam taahhüdü belirsizleştirir, kullanıcı ödeme anında beklemediği bir tutarla karşılaşabilir ve bu iptal ile itiraza dönüşebilir. Belirleyici olan, toplam tutarın aynı ekranda ne kadar net durduğudur.

**Test edilmesi gerekenler**
- Çerçeve: Aylık birim gösterimi geliri artırıyor mu?
- Sonraki test: Aylık çerçeve sabitken yıllık toplamın punto büyüklüğü ayrı bir testte ilk dönem iptalini azaltıyor mu?
- Beklenti: Ödeme adımında sürpriz tutar itirazı artıyor mu?
- Ayrıntı düzeyi: Aylık yerine daha küçük birime bölmek inandırıcılığı düşürüyor mu?
- Segment: Bireysel ve kurumsal alıcı aynı çerçeveye mi tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çerçeveleme geliri artırıyor mu?
- İlk Dönem İptal Oranı: Beklenti uyumsuzluğundan doğan iptal artmamalı.
- Ödeme Adımı Terk Oranı: Toplam tutarı görünce bırakma artmamalı.
- Yıllık Plan Seçim Oranı: Uzun taahhüde geçiş artıyor mu?
- Ödeme İtirazı veya İade Talebi: Tutar şaşkınlığı kaynaklı talepler artmamalı.

**Yapılmaması gerekenler**
- Toplam tutarı okunmaz derecede küçük yazıp aylık rakamı tek görünen fiyat hâline getirmeyin.
- Aylık gösterip aylık ödeme seçeneği sunmuyorsanız bunu belirtmeden bırakmayın.
- Aynı testte çerçeveleme ile fiyat seviyesini birlikte değiştirmeyin.
- Fiyat gösterimi yasal olarak düzenlenen pazarlarda kuralı doğrulamadan çerçeve değiştirmeyin.
- Aylık birime bölünen tutarı aşağı yuvarlayıp on iki katı gerçek yıllık tutardan düşük çıkan bir rakam göstermeyin.

---

## Birim fiyat göstermek karşılaştırmayı kolaylaştırıp geliri artırır mı?

Değişken: Paket kartındaki birim fiyat · Fark: ekle

Birim başına fiyat (kilogram, adet, kullanıcı, ay) farklı boyuttaki paketleri karşılaştırılabilir kılar ve büyük paketin avantajını görünür yapar. Riski: birim fiyat küçük paketi pahalı gösterir ve ziyaretçiyi bütçesini aşan bir pakete iter; ayrıca fiyat alanını kalabalıklaştırıp asıl tutarın okunmasını zorlaştırabilir.

**Test edilmesi gerekenler**
- Varlık: Birim fiyat göstermek geliri artırıyor mu?
- Yönlenme: Ziyaretçi daha büyük pakete mi kayıyor?
- Okunabilirlik: İki fiyatın yan yana durması asıl tutarı gölgeliyor mu?
- Sonraki test: Birim fiyat kazanırsa farklı birimler (adet / ağırlık / kullanıcı) ayrı bir testte denendiğinde hangisi paket seçimini daha çok kolaylaştırıyor?
- Cihaz: Mobilde birim fiyat satırı asıl fiyatın altına kaydığında etkisi değişiyor mu?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Birim fiyat geliri artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Büyük pakete kayma tutarı artırıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı düşmemeli.
- İade veya İptal Oranı: Bütçesini aşan alım sonradan geri dönmemeli.
- Fiyat Alanı Etkileşimi: Asıl fiyatın okunması zorlaşmamalı.

**Yapılmaması gerekenler**
- Birim fiyatı asıl fiyattan daha büyük puntoyla göstermeyin.
- Birim hesabını yuvarlayarak gerçek orandan sapan bir rakam üretmeyin.
- Aynı testte birim fiyat ile paket boyutlarını birlikte değiştirmeyin.
- Farklı ürünlerde farklı birim kullanıp karşılaştırmayı bozmayın.
- Birim fiyatın zorunlu olduğu pazarlarda bunu bir test değişkeni gibi ele almayın; orada zorunluluktur.

---

## Ödemenin tek seferlik olduğunu açıkça yazmak dönüşümü artırır mı?

Değişken: Tek seferlik ödeme ifadesi · Fark: ekle

Abonelik yorgunluğu yaşayan kullanıcı, her ödemenin tekrarlayacağını varsayabilir. “Tek seferlik ödeme, otomatik yenileme yok” gibi bir ifade bu tereddüdü kaldırabilir. Karşı tarafta: bu ifade abonelik seçeneğini de akla getirip karşılaştırma yükü yaratabilir, ya da tekrar satın alma ihtimalini zayıflatabilir.

**Test edilmesi gerekenler**
- İfade: Tek seferlik olduğunu belirtmek geliri artırıyor mu?
- Sonraki test: İfade kazanırsa fiyatın yanında mı, ödeme butonunun altında mı durduğu ayrı bir testte ödeme tamamlamayı değiştiriyor mu?
- Karşılaştırma yükü: Abonelik seçeneği de sunulan sayfada ifade, ziyaretçiyi iki ödeme modeli arasında kararsız bırakıp karar süresini uzatıyor mu?
- Yan etki: İfade tekrar satın alma veya abonelik geçişini azaltıyor mu?
- Segment: Yeni ziyaretçi ile daha önce satın almış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İfade geliri artırıyor mu?
- Ödeme Tamamlama Oranı: Ödemeyi bitiren oranı artıyor mu?
- Tekrar Satın Alma Oranı: İleriki dönemde tekrar alım düşmemeli.
- Abonelik Geçiş Oranı: Abonelik satıyorsanız bu oran kabul edilemez ölçüde düşmemeli.
- İade veya İtiraz Oranı: Beklenti kaynaklı itirazlar azalıyor mu?

**Yapılmaması gerekenler**
- Gerçekte tekrarlayan bir ödeme varken tek seferlik ifadesi kullanmayın.
- Aynı testte ifade ile fiyatı birlikte değiştirmeyin.
- İfadeyi ödeme koşullarının yerine geçirmeyin; koşul metni ayrıca bulunmalıdır.
- “Otomatik yenileme yok” ifadesini, aynı sayfada önceden işaretli gelen bir abonelik veya ek hizmet kutusuyla birlikte göstermeyin.
- Abonelik iptali kurallarının düzenlendiği pazarlarda ifadeyi hukuki kontrol olmadan yayınlamayın.

---

## Fiyatı vergi dahil mi, hariç mi göstermeli?

Değişken: Fiyatta verginin gösterim şekli · Fark: değiştir

Vergi hariç fiyat rakamı küçük gösterir ve kurumsal alıcının zaten hariç düşündüğü pazarlarda doğaldır. Vergi dahil fiyat ise ödenecek gerçek tutarı verir ve ödeme adımında sürpriz yaşatmaz. Bu tercih büyük ölçüde pazara ve alıcı tipine bağlıdır; birçok pazarda ise tüketiciye dahil fiyat göstermek zorunludur.

**Test edilmesi gerekenler**
- Gösterim: Vergi dahil fiyat toplam geliri nasıl etkiliyor?
- Sürpriz: Ödeme adımında tutar artışı terk yaratıyor mu?
- İkili gösterim: Hem dahil hem hariç göstermek karışıklık mı yaratıyor, netlik mi?
- Alıcı tipi: Kurumsal alıcı hariç fiyatı mı bekliyor?
- Segment: Farklı pazarlardaki ziyaretçilere farklı gösterim mi gerekiyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Gösterim geliri artırıyor mu?
- Ödeme Adımı Terk Oranı: Tutar artışı kaynaklı bırakma artmamalı.
- Dönüşüm Oranı (CR): Satın alma oranı ne yönde değişiyor?
- Fiyat Kaynaklı Destek Talebi: “Neden farklı tutar çıktı” soruları artmamalı.
- İade veya İtiraz Oranı: Tutar şaşkınlığı kaynaklı itirazlar artmamalı.

**Yapılmaması gerekenler**
- Tüketiciye vergi dahil gösterimin zorunlu olduğu pazarlarda bunu test değişkeni yapmayın; orada seçim yoktur.
- Hedef pazarın kuralını doğrulamadan varyant kurmayın (kural 11).
- Vergi hariç gösterip bunu belirten ifadeyi okunmaz küçüklükte yazmayın.
- Aynı testte vergi gösterimi ile kargo ücreti gösterimini birlikte değiştirmeyin.
- Tek pazarda ölçüp sonucu diğer pazarlara taşımayın.

---

## Pakete dahil olanların parasal değerini göstermek algılanan değeri artırır mı?

Değişken: Paket içeriğinin parasal değer gösterimi · Fark: ekle

Fiyatın yanında “içindekilerin toplam değeri” göstermek alınan şeyin büyüklüğünü somutlaştırır. Riski: karşılaştırma değeri gerçekçi değilse güven kaybı yaratır, ayrıca şişirilmiş referans değer bazı pazarlarda yanıltıcı fiyat gösterimi sayılır. Değer iddiası doğrulanabilir olmalıdır.

**Test edilmesi gerekenler**
- Varlık: Dahil olanların değerini göstermek geliri artırıyor mu?
- İnandırıcılık: Belirtilen değer gerçekçi bulunuyor mu?
- Sonraki test: Değer gösterimi kazanırsa toplam tutar ile kalem kalem döküm ayrı bir testte karşılaştırıldığında hangisi daha inandırıcı bulunuyor?
- Oran: Değer ile fiyat arasındaki fark büyüdükçe güven düşüyor mu?
- Segment: Farklı kullanıcı tipleri değer iddiasına farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Değer gösterimi geliri artırıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı artıyor mu?
- İade Oranı: Abartılı değer algısı sonradan hayal kırıklığı yaratmamalı.
- Ortalama Sepet Tutarı (AOV): Ortalama tutar düşmemeli.
- Güven Kaynaklı Destek Talebi: Değer iddiasını sorgulayan talepler artmamalı.

**Yapılmaması gerekenler**
- Ayrı satılmayan bir kalemin “ayrı fiyatı” varmış gibi bir değer üretmeyin.
- Doğrulanamayan bir referans değeri fiyatın yanına yazmayın (kural 6).
- Aynı testte değer gösterimi ile paket içeriğini birlikte değiştirmeyin.
- Referans fiyat gösteriminin düzenlendiği pazarlarda kuralı doğrulamadan yayınlamayın.
- Değer toplamına, kullanıcının zaten ücretsiz aldığı kalemleri (ör. standart kargo) parasal değer biçip eklemeyin.

---

## Üçüncü bir çekici-alternatif plan eklemek orta planın seçilme oranını artırıyor mu?

Değişken: Çekici-alternatif üçüncü plan · Fark: ekle

İki plan arasında seçim yapmak zordur çünkü karşılaştırılacak ortak bir ölçüt yoktur. Orta plana yakın fiyatlı ama daha az içerikli üçüncü bir plan eklemek, orta planı “açık ara daha iyi seçenek” gibi gösterebilir; üçüncü planın kendisi neredeyse hiç seçilmez, işlevi karşılaştırma çıpası olmaktır. Bu, yeni bir avantaj eklemez; var olan iki planın algısını üçüncüsüne göre değiştirir.

**Test edilmesi gerekenler**
- Sonraki test: Çekici-alternatif plan kazanırsa orta planın hemen yanında mı, en pahalı sırada mı durduğu ayrı bir testte orta plan seçimini değiştiriyor mu?
- Fiyat farkı: Çekici-alternatif ile orta plan arasındaki fark küçüldükçe etki güçleniyor mu?
- Gerçek talep: Çekici-alternatif planın kendisi ciddi bir oranda seçiliyor mu, yoksa beklendiği gibi arka planda mı kalıyor?
- Algı: Üç seçenek göstermek genel fiyat algısını pahalı mı gösteriyor?
- Segment: Kurumsal ve bireysel alıcı üç seçenekli yapıya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çekici-alternatif eklemek geliri artırıyor mu?
- Orta Plan Seçim Oranı: Orta planı seçen ziyaretçi oranı yükseliyor mu?
- Çekici-Alternatif Seçilme Oranı: Bu planın kendisi ciddi talep almamalı; aldıysa yapı yanlış kurulmuş demektir.
- En Pahalı Plan Satışı: Gerçek en pahalı planın satışı düşmemeli.
- Destek Talebi: “Hangi planı seçmeliyim” soruları artmamalı.

**Yapılmaması gerekenler**
- Çekici-alternatif planı satın alınamaz hâle getirmeyin veya içeriğini gerçek dışı bırakmayın; gerçek, kullanılabilir bir plan olmalı, yalnızca konumlandırması zayıf kurulur.
- Aynı testte üçüncü planı eklerken orta planın fiyatını da değiştirmeyin; seçim artışı çıpadan mı, yeni fiyattan mı geldi ayrılamaz.
- Çekici-alternatif planı gerçek maliyetinin altında fiyatlandırıp asıl planları yapay biçimde pahalı göstermeyin.
- Orta planın içeriğini test sırasında zenginleştirmeyin; tek değişken üçüncü seçeneğin varlığıdır.
- Kurumsal fiyat sayfası gizliyse bu senaryoyu `saas-b2b.md`’deki plan-varsayılanı senaryosuyla karıştırmayın; ikisi ayrı testtir.

---

## Fiyat planlarını ucuzdan pahalıya mı, pahalıdan ucuza mı sıralamalı?

Değişken: Fiyat planlarının sıralama yönü · Fark: değiştir

Planların soldan sağa hangi sırayla dizildiği, karşılaştırma sırasında hangi planın çapa görevi göreceğini belirler. Pahalı plan önce görünürse sonraki planlar daha uygun hissettirebilir; ucuz plan önce görünürse ziyaretçi bütçe eksenli düşünmeye başlar. Bu, plan sayısından ve tablo/kart biçiminden ayrı bir değişkendir; sıralama, ne gösterildiğini değil hangi sırayla görüldüğünü test eder.

**Test edilmesi gerekenler**
- Yön: Ucuzdan pahalıya mı, pahalıdan ucuza mı toplam geliri artırıyor?
- Çapa etkisi: İlk görülen plan sonraki planların algılanan değerini nasıl değiştiriyor?
- Öne çıkan plan: Sıra değişince “önerilen” plan etiketi hâlâ doğru planda mı duruyor?
- Kaydırma: Mobilde ilk görülen plan, kaydırmadan görünen tek plan oluyor mu?
- Segment: Kurumsal ve bireysel ziyaretçi farklı bir sıradan mı etkileniyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sıralama geliri artırıyor mu?
- Önerilen Plan Seçim Oranı: Öne çıkarılan planın seçilme oranı değişiyor mu?
- En Ucuz Plan Seçim Oranı: Aşağı kayma artmamalı.
- Karar Süresi: Sayfada karar verme süresi kabul edilemez ölçüde uzamamalı.
- Destek Talebi: “Hangi planı seçmeliyim” soruları artmamalı.

**Yapılmaması gerekenler**
- Aynı testte plan sırasını ve hangi planın “önerilen” olarak etiketlendiğini birlikte değiştirmeyin.
- Sıralamayı, plan içeriklerini veya fiyatlarını aynı anda değiştirerek test etmeyin.
- Pahalı planı önce göstererek ucuz planı yapay biçimde küçük veya eksik göstermeyin.
- Pahalıdan ucuza sıralamada mobilde yalnızca en pahalı planın görüneceği bir düzeni, diğer planlara geçiş ipucu vermeden yayınlamayın.
- Enterprise/kurumsal planı bu sıralamaya dahil ediyorsanız `saas-b2b.md`’deki fiyat gizleme senaryosuyla çelişmeyin.

---

## Fiyatın küsuratını üst simge olarak yazmak algılanan tutarı küçültür mü?

Değişken: Fiyat küsuratının yazım biçimi · Fark: değiştir

“₺199,90” yerine “₺199⁹⁰” gibi küsuratı küçük ve üst simge yazmak, gözün ana sayıya (199) odaklanmasını sağlayıp fiyatı daha küçük hissettirebilir. Riski, küçük yazılan kısmın bazı kullanıcılar tarafından hiç fark edilmemesi veya okunaksız bulunmasıdır.

**Test edilmesi gerekenler**
- Biçim: Üst simge küsurat mı, standart aynı boyut küsurat mı satın almayı artırıyor?
- Okunabilirlik: Küçük yazılan küsurat mobilde net okunuyor mu?
- Tutar büyüklüğü: Etki küçük tutarlarda mı, büyük tutarlarda mı daha belirgin?
- Yuvarlama algısı: Kullanıcı gerçek tutarı doğru mu tahmin ediyor, yoksa yuvarlıyor mu?
- Segment: Fiyatı kuruşuna kadar karşılaştıran fiyata duyarlı ziyaretçide küçük küsurat, fiyata bakmayan ziyaretçiye göre etkisiz mi kalıyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Fiyat formatı geliri artırıyor mu?
- Dönüşüm Oranı (CR): Fiyat formatı satın alma oranını artırıyor mu?
- Ortalama Sepet Tutarı (AOV): Format, ortalama tutar algısını bozup gerçek harcamayı düşürmemeli.
- Fiyat Okuma Netliği (oturum kaydı): Küsuratı fark etmeyen kullanıcı oranı yüksek mi?
- İade veya İtiraz Oranı: “Beklediğimden pahalı çıktı” itirazları artmamalı.

**Yapılmaması gerekenler**
- Toplam ödenecek tutarı, yalnızca ana rakamı büyük göstererek gizlemeyin; küsurat küçük olsa da her zaman okunabilir kalmalı.
- Aynı testte fiyat formatını ve fiyat seviyesini birlikte değiştirmeyin.
- Farklı ürünlerde tutarsız bir format kullanıp karşılaştırmayı zorlaştırmayın.
- Vergi veya ek ücretin küsuratını ana tutarla karıştırıp toplam tutarı belirsizleştirmeyin.
- Fiyat gösteriminin yasal olarak düzenlendiği pazarlarda kuralı doğrulamadan format değiştirmeyin (kural 11).

---

## Fiyattan önce yüksek bir referans sayı göstermek algılanan değeri artırır mı?

Değişken: Fiyattan önce gösterilen referans sayı · Fark: ekle

Bir fiyat, yanında yüksek bir referans sayı (“piyasa ortalaması ₺X”, “benzer hizmetler ₺Y’ye kadar”) olmadan gösterildiğinde ziyaretçi değeri tek başına yargılar; referans sayı önce görüldüğünde asıl fiyat ona göre daha uygun hissedilebilir. Bu, üstü çizili “eski fiyat” göstermekten farklıdır; burada referans sizin geçmiş fiyatınız değil, dış bir karşılaştırma noktasıdır ve doğruluğu ayrıca doğrulanmalıdır.

**Test edilmesi gerekenler**
- Varlık: Referans sayı göstermek satın alma oranını artırıyor mu?
- Sonraki test: Referans sayı kazanırsa kaynağını (piyasa ortalaması / bağımsız ölçüm) belirtmek ayrı bir testte inandırıcılığı artırıyor mu?
- Fark büyüklüğü: Referans ile asıl fiyat arasındaki fark büyüdükçe etki güçleniyor mu, yoksa güven mi düşüyor?
- Şüphe etkisi: Referans sayıyı gören ziyaretçiler karşılaştırmayı sorgulayıp fiyatı başka yerde aramaya mı gidiyor?
- Segment: Piyasa fiyatını zaten bilen fiyata duyarlı ziyaretçide referans sayı, fiyat bilgisi olmayan ziyaretçiye göre daha az mı etkili?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Referans sayı geliri artırıyor mu?
- Dönüşüm Oranı (CR): Referans sayı satın alma oranını artırıyor mu?
- Güven Algısı (anket): Referans sayı inandırıcı bulunuyor mu, yoksa şüphe mi uyandırıyor?
- İade veya İtiraz Oranı: “Yanıltıcı karşılaştırma” şikâyeti artmamalı.
- Ortalama Sepet Tutarı (AOV): Referans sayı ortalama tutarı düşürmemeli.

**Yapılmaması gerekenler**
- Doğrulanamayan veya uydurma bir referans sayı göstermeyin (kural 6); piyasa ortalaması veya rakip fiyatı iddiası gerçek, güncel bir kaynağa dayanmalı.
- Aynı testte referans sayının varlığını ve asıl fiyat seviyesini birlikte değiştirmeyin.
- Referans sayıyı gerçekçi olmayacak kadar büyük seçip asıl fiyatı yapay biçimde ucuz göstermeyin.
- Rakip fiyatını isim vererek gösteriyorsanız haksız rekabet veya karşılaştırmalı reklam kurallarını hedef pazarda doğrulamadan yayınlamayın (kural 11).
- Referans sayıyı güncellemiyorsanız eski veya geçersiz bir rakamda donmuş bırakmayın.
