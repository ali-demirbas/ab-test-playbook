# Fiyatlandırma ve fiyat sunumu

Yolculuk aşaması: fiyatın görüldüğü an. Hem abonelik fiyat sayfası hem e-ticarette fiyat gösterimi bu dosyadadır. Ticari strateji kararları (plan varsayılanı, kurumsal fiyatın gizlenmesi, deneme süresi) `saas-b2b.md`, indirim ve taksit sunumu `product-detail.md` içindedir; burada fiyatın kendisinin nasıl çerçevelendiği ele alınır.

**Bu dosyadaki tüm senaryolarda birincil metrik gelir bazlıdır.** Fiyatı ucuz göstermek veya seçenek azaltmak dönüşüm oranını neredeyse her zaman artırır ama geliri düşürebilir; bu yüzden Ziyaretçi Başına Gelir (RPV) birincil, dönüşüm oranı ikincil metriktir (`knowledge/methodology.md` → Dönüşüm oranı geliri gizleyebilir). Her KPI listesinde en az bir madde bozulmaması gereken guardrail’dir.

---

## Kaç fiyat planı gösterilmeli?

Az sayıda plan kararı hızlandırır ve karşılaştırma yükünü azaltır. Çok sayıda plan farklı ihtiyaçları karşılar ama seçim felcine yol açabilir ve ziyaretçiyi hiçbirini seçmemeye itebilir. Plan sayısını değiştirmek aynı zamanda hangi planın ortada kaldığını da değiştirir; bu, seçim dağılımını fiyattan bağımsız olarak kaydırır.

**Test edilmesi gerekenler**
- Sayı: Plan sayısını azaltmak toplam geliri artırıyor mu?
- Dağılım: Hangi plan ne oranda seçiliyor, ortadaki plan avantaj sağlıyor mu?
- Kaybedilen ihtiyaç: Kaldırılan planı seçenler başka plana mı geçiyor, yoksa kayboluyor mu?
- Aşağı kayma: Az seçenek ziyaretçiyi daha ucuz plana mı yönlendiriyor?
- Segment: Bireysel ve kurumsal ziyaretçi farklı sayıda seçeneğe mi ihtiyaç duyuyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Plan sayısı geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Oranı: Herhangi bir planı seçen ziyaretçi oranı artıyor mu?
- İptal veya Plan Düşürme Oranı: Yanlış plana yönlenen kullanıcı sonradan düşmemeli.
- Destek Talebi Sayısı: “Hangi planı almalıyım” soruları artmamalı.

**Yapılmaması gerekenler**
- Aynı testte plan sayısı ile plan fiyatlarını birlikte değiştirmeyin.
- Dönüşüm oranı arttı diye gelire bakmadan kazandı demeyin.
- Kaldırdığınız planın mevcut abonelerini test kapsamına almayın.
- Plan sayısını değiştirirken plan içeriklerini de yeniden paketlemeyin.
- Seçenek azaltmayı, aslında satmak istediğiniz planı tek çıkış yolu hâline getirmek için kullanmayın.

---

## Planları karşılaştırma tablosunda mı, ayrı kartlarda mı sunmalı?

Karşılaştırma tablosu farkları satır satır görünür kılar ve ayrıntılı değerlendirme yapan ziyaretçiye hitap eder. Ayrı kartlar her planı kendi başına bir teklif gibi sunar, hızlı karar verdirir ama farkları gizler. Tablo aynı zamanda ucuz planda eksik olan her şeyi de görünür kılar; bu hem ikna edici hem caydırıcı olabilir.

**Test edilmesi gerekenler**
- Biçim: Tablo mu, kart mı daha yüksek gelir getiriyor?
- Ayrıntı: Kaç satırlık karşılaştırma faydalıyken kaçında yorucu hâle geliyor?
- Eksiklik vurgusu: Ucuz planda eksik olanları göstermek yukarı mı itiyor, caydırıyor mu?
- Varsayılan görünüm: Tablo katlanmış mı gelmeli, açık mı?
- Cihaz: Mobilde tablo yatay kaydırmaya düşüyor mu, kart daha mı iyi çalışıyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sunum biçimi geliri artırıyor mu?
- Ortalama Plan Değeri: Seçilen planın ortalama tutarı düşmemeli.
- Plan Seçim Oranı: Karar veren ziyaretçi oranı artıyor mu?
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

Fiyatı erken göstermek beklentiyi netleştirir ve bütçesi uymayan ziyaretçinin vaktini almaz. Faydayı önce anlatmak, fiyat görüldüğünde algılanan değeri yükseltir. Erken fiyat pahalı algılanan üründe kayıp yaratabilir; geç fiyat ise güvensizlik ve “fiyatı gizliyorlar” hissi doğurabilir.

**Test edilmesi gerekenler**
- Sıra: Fiyat faydadan önce mi, sonra mı gösterilmeli?
- Görünürlük: Fiyat puntosunu büyütmek algıyı nasıl değiştiriyor?
- Nitelik: Erken fiyat gelen talebin niteliğini yükseltiyor mu?
- Güven: Fiyatı geciktirmek gizleme algısı yaratıyor mu?
- Segment: Fiyata duyarlı ve değere duyarlı ziyaretçi farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Sıralama geliri artırıyor mu?
- Ortalama Sepet veya Plan Tutarı: Ortalama tutar düşmemeli.
- Dönüşüm Oranı (CR): Satın alan ziyaretçi oranı ne yönde değişiyor?
- Hemen Çıkma Oranı: Erken fiyat çıkışı kabul edilemez ölçüde artırmamalı.
- Talep Kalitesi: Geç fiyat, ödeme gücü olmayan talebi çoğaltmamalı.

**Yapılmaması gerekenler**
- Fiyatı geciktirmeyi, kullanıcı taahhüde girene kadar saklamak için kullanmayın.
- Aynı testte fiyat konumu ile fiyat rakamını birlikte değiştirmeyin.
- Toplam fiyatın bir kısmını (kargo, vergi, kurulum) sonraya bırakıp “fiyat öne alındı” demeyin.
- Yasal olarak fiyatın belirli bir aşamada gösterilmesi gereken pazarlarda kuralı doğrulamadan sıralama değiştirmeyin.
- Fiyat büyütülürken para birimi veya vergi ifadesini küçültmeyin.

---

## Abonelik fiyatını aylık birime bölerek göstermek işe yarar mı?

Yıllık bir tutarı aylık karşılığıyla göstermek rakamı küçültür ve giriş engelini düşürür. Buna karşılık toplam taahhüdü belirsizleştirir, kullanıcı ödeme anında beklemediği bir tutarla karşılaşabilir ve bu iptal ile itiraza dönüşebilir. Belirleyici olan, toplam tutarın aynı ekranda ne kadar net durduğudur.

**Test edilmesi gerekenler**
- Çerçeve: Aylık birim gösterimi geliri artırıyor mu?
- Netlik: Toplam yıllık tutar aynı anda ne kadar görünür olmalı?
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
- Dönüşüm arttı diye iptal ve iade tarafına bakmadan kazandı demeyin.

---

## Birim fiyat göstermek karşılaştırmayı kolaylaştırıp geliri artırır mı?

Birim başına fiyat (kilogram, adet, kullanıcı, ay) farklı boyuttaki paketleri karşılaştırılabilir kılar ve büyük paketin avantajını görünür yapar. Riski: birim fiyat küçük paketi pahalı gösterir ve ziyaretçiyi bütçesini aşan bir pakete iter; ayrıca fiyat alanını kalabalıklaştırıp asıl tutarın okunmasını zorlaştırabilir.

**Test edilmesi gerekenler**
- Varlık: Birim fiyat göstermek geliri artırıyor mu?
- Yönlenme: Ziyaretçi daha büyük pakete mi kayıyor?
- Okunabilirlik: İki fiyatın yan yana durması asıl tutarı gölgeliyor mu?
- Birim seçimi: Hangi birim (adet, ağırlık, kullanıcı, ay) daha anlaşılır?
- Kategori: Birim fiyatın etkisi tüm kategorilerde aynı mı?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Birim fiyat geliri artırıyor mu?
- Ortalama Sepet Tutarı: Büyük pakete kayma tutarı artırıyor mu?
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

Abonelik yorgunluğu yaşayan kullanıcı, her ödemenin tekrarlayacağını varsayabilir. “Tek seferlik ödeme, otomatik yenileme yok” gibi bir ifade bu tereddüdü kaldırabilir. Karşı tarafta: bu ifade abonelik seçeneğini de akla getirip karşılaştırma yükü yaratabilir, ya da tekrar satın alma ihtimalini zayıflatabilir.

**Test edilmesi gerekenler**
- İfade: Tek seferlik olduğunu belirtmek geliri artırıyor mu?
- Konum: İfade fiyatın yanında mı, ödeme butonunun altında mı daha etkili?
- Ton: Olumlu ifade mi (“tek seferlik”) yoksa olumsuzlama mı (“abonelik yok”) daha çok işe yarıyor?
- Yan etki: İfade tekrar satın alma veya abonelik geçişini azaltıyor mu?
- Segment: Yeni ziyaretçi ile daha önce satın almış kullanıcı farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): İfade geliri artırıyor mu?
- Ödeme Adımı Tamamlama Oranı: Ödemeyi bitiren oranı artıyor mu?
- Tekrar Satın Alma Oranı: İleriki dönemde tekrar alım düşmemeli.
- Abonelik Geçiş Oranı: Abonelik satıyorsanız bu oran kabul edilemez ölçüde düşmemeli.
- İade veya İtiraz Sayısı: Beklenti kaynaklı itirazlar azalıyor mu?

**Yapılmaması gerekenler**
- Gerçekte tekrarlayan bir ödeme varken tek seferlik ifadesi kullanmayın.
- Aynı testte ifade ile fiyatı birlikte değiştirmeyin.
- İfadeyi ödeme koşullarının yerine geçirmeyin; koşul metni ayrıca bulunmalıdır.
- Kısa vadeli dönüşüm arttı diye tekrar alım tarafına bakmadan kazandı demeyin.
- Abonelik iptali kurallarının düzenlendiği pazarlarda ifadeyi hukuki kontrol olmadan yayınlamayın.

---

## Fiyatı vergi dahil mi, hariç mi göstermeli?

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
- İade veya İtiraz Sayısı: Tutar şaşkınlığı kaynaklı itirazlar artmamalı.

**Yapılmaması gerekenler**
- Tüketiciye vergi dahil gösterimin zorunlu olduğu pazarlarda bunu test değişkeni yapmayın; orada seçim yoktur.
- Hedef pazarın kuralını doğrulamadan varyant kurmayın (kural 11).
- Vergi hariç gösterip bunu belirten ifadeyi okunmaz küçüklükte yazmayın.
- Aynı testte vergi gösterimi ile kargo ücreti gösterimini birlikte değiştirmeyin.
- Tek pazarda ölçüp sonucu diğer pazarlara taşımayın.

---

## Pakete dahil olanların parasal değerini göstermek algılanan değeri artırır mı?

Fiyatın yanında “içindekilerin toplam değeri” göstermek alınan şeyin büyüklüğünü somutlaştırır. Riski: karşılaştırma değeri gerçekçi değilse güven kaybı yaratır, ayrıca şişirilmiş referans değer bazı pazarlarda yanıltıcı fiyat gösterimi sayılır. Değer iddiası doğrulanabilir olmalıdır.

**Test edilmesi gerekenler**
- Varlık: Dahil olanların değerini göstermek geliri artırıyor mu?
- İnandırıcılık: Belirtilen değer gerçekçi bulunuyor mu?
- Biçim: Toplam tutar mı, kalem kalem döküm mü daha etkili?
- Oran: Değer ile fiyat arasındaki fark büyüdükçe güven düşüyor mu?
- Segment: Farklı kullanıcı tipleri değer iddiasına farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Değer gösterimi geliri artırıyor mu?
- Dönüşüm Oranı (CR): Satın alma oranı artıyor mu?
- İade Oranı: Abartılı değer algısı sonradan hayal kırıklığı yaratmamalı.
- Ortalama Sepet veya Plan Tutarı: Ortalama tutar düşmemeli.
- Güven Kaynaklı Destek Talebi: Değer iddiasını sorgulayan talepler artmamalı.

**Yapılmaması gerekenler**
- Ayrı satılmayan bir kalemin “ayrı fiyatı” varmış gibi bir değer üretmeyin.
- Doğrulanamayan bir referans değeri fiyatın yanına yazmayın (kural 6).
- Aynı testte değer gösterimi ile paket içeriğini birlikte değiştirmeyin.
- Referans fiyat gösteriminin düzenlendiği pazarlarda kuralı doğrulamadan yayınlamayın.
- Dönüşüm arttı diye iade tarafına bakmadan kazandı demeyin.

---

## Üçüncü bir çekici-alternatif plan eklemek orta planın seçilme oranını artırıyor mu?

İki plan arasında seçim yapmak zordur çünkü karşılaştırılacak ortak bir ölçüt yoktur. Orta plana yakın fiyatlı ama daha az içerikli üçüncü bir plan eklemek, orta planı “açık ara daha iyi seçenek” gibi gösterebilir — üçüncü planın kendisi neredeyse hiç seçilmez, işlevi karşılaştırma çıpası olmaktır. Bu, yeni bir avantaj eklemez; var olan iki planın algısını üçüncüsüne göre değiştirir.

**Test edilmesi gerekenler**
- Konum: Çekici-alternatif plan orta planın hemen yanında mı, en pahalı sırada mı daha güçlü çalışıyor?
- Fiyat farkı: Çekici-alternatif ile orta plan arasındaki fark küçüldükçe etki güçleniyor mu?
- Gerçek talep: Çekici-alternatif planın kendisi ciddi bir oranda seçiliyor mu, yoksa beklendiği gibi arka planda mı kalıyor?
- Algı: Üç seçenek göstermek genel fiyat algısını pahalı mı gösteriyor?
- Segment: Kurumsal ve bireysel alıcı üç seçenekli yapıya farklı mı tepki veriyor?

**Takip edilecek ana KPI’lar**
- Ziyaretçi Başına Gelir (RPV): Çekici-alternatif eklemek geliri artırıyor mu?
- Orta Plan Seçim Oranı: Orta planı seçen ziyaretçi oranı yükseliyor mu?
- Çekici-Alternatif Seçilme Oranı: Bu planın kendisi ciddi talep almamalı — aldıysa yapı yanlış kurulmuş demektir.
- En Pahalı Plan Satışı: Gerçek en pahalı planın satışı düşmemeli.
- Destek Talebi: “Hangi planı seçmeliyim” soruları artmamalı.

**Yapılmaması gerekenler**
- Çekici-alternatif planı satın alınamaz hâle getirmeyin veya içeriğini gerçek dışı bırakmayın — gerçek, kullanılabilir bir plan olmalı, yalnızca konumlandırması zayıf kurulur.
- Aynı testte plan sayısı ile plan fiyatlarını birlikte değiştirmeyin.
- Çekici-alternatif planı gerçek maliyetinin altında fiyatlandırıp asıl planları yapay biçimde pahalı göstermeyin.
- Orta planın içeriğini test sırasında zenginleştirmeyin; tek değişken üçüncü seçeneğin varlığıdır.
- Kurumsal fiyat sayfası gizliyse bu senaryoyu `saas-b2b.md`’deki plan-varsayılanı senaryosuyla karıştırmayın — ikisi ayrı testtir.
