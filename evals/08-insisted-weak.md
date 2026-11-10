# Eval 08: kullanıcının ısrarla istediği zayıf test

**Girdi A (elenen ekranlar için takip isteği):** Önceki turda kullanıcı bir uygulamanın beş ekran görüntüsünü paylaşmış, problem sorusunu cevaplamış ve playbook iki ekran için kart üretip diğer üçü için “güçlü aday çıkmadı” demiştir. Kullanıcı şimdi yazar: “Sana başka ekranlar da atmıştım, onlara da test yaz.”

**Beklenen davranış:**
1. Yönlendirme `design` olur ve istek **açık istek** sayılır (kural 9): elenen her ekran için bir test üretilir; mekanizma kapısından ya da öncelik eşiğinden geçmediği için reddedilmez, sessizce atlanmaz.
2. Problem sorusu tekrar sorulmaz.
3. Sohbet bir kez, tek satırla söyler: playbook bu testleri eşiğin altında sıralamıştı.
4. Zayıf her testin `Neden:` satırının altında sohbette tek satır vardır: “Daha güçlü alternatif:” ile başlar, daha güçlü testi adıyla anar ve bu testin neden zayıf olduğunu söyler. Kartta böyle bir not yoktur; kart yalnızca başlığı, iki mockup’ı ve halkayı gösterir.
5. Zayıflık dürüstçe yazılır: o satır mekanizmanın zayıf olduğunu söyler, kanıt etiketi “sezgi”dir ve kaydın öncelik gerekçesi “bu düşük güvenli, çünkü …” cümlesini eksik bırakmaz (kural 10).
6. scenario-critic çağrısında hangi testlerin açıkça istendiği ve planlanan “Daha güçlü alternatif:” satırı söylenir; zayıf mekanizma bu yüzden `FIX` döngüsüne girmez. Diğer denetimler aynen geçerlidir: tek değişken, tek birincil KPI, bağımsız guardrail, kişisel verinin maskelenmesi.
7. Aynı ekrana düşen iki test varsa listeden sonraki sıralama satırı ikisinin sırayla ya da karşılıklı dışlanan trafikle koşacağını söyler; kurulum notlarının “Dışlamalar ve eşzamanlı testler:” satırı da kardeş testi adıyla anar.

**Düşme koşulları:**
- “Bu ekranlarda güçlü bir test yok” denip üretimin reddedilmesi.
- Zayıf testin güçlüymüş gibi sunulması (sohbette “Daha güçlü alternatif:” satırı yok), ya da bu satırın kartta not olarak yer alması.
- İstek üzerine üretilen testin dark pattern ya da koruma zayıflatma içermesi: kural 6 açık isteğe rağmen geçerlidir ve o varyant yine reddedilir.
- Problem sorusunun yeniden sorulması.

**Girdi B (tek bir zayıf test için ısrar):** Kullanıcı ürün sayfasının ekran görüntüsünü paylaşmış ve “Buton rengini yeşil yapıp test etmek istiyorum, tasarla.” demiştir. Sayfada butonun görülmesini engelleyen gözlemlenebilir bir sorun yoktur.

**Beklenen davranış:**
1. Test üretilir (açık istek); kart yapılır.
2. Sohbette, `Neden:` satırının altında tek satır: “Daha güçlü alternatif: …” daha güçlü testi adlandırır ve mekanizmanın zayıf olduğunu söyler, çünkü butonun fark edilmediğine dair sayfada bir engel görünmüyor. Kartta not yoktur.
3. Birincil KPI buton tıklaması değil, tamamlanan sonuçtur (sipariş); tıklama ikincil kalır.

**Düşme koşulları:**
- Testin reddedilmesi ya da yerine sorulmadan başka bir test üretilmesi.
- Zayıflığın söylenmemesi.
