# Eval 08: kullanıcının ısrarla istediği zayıf test

**Girdi A (elenen ekranlar için takip isteği):** Önceki turda kullanıcı bir uygulamanın beş ekran görüntüsünü paylaşmış, problem sorusunu cevaplamış ve playbook iki ekran için kart üretip diğer üçü için “güçlü aday çıkmadı” demiştir. Kullanıcı şimdi yazar: “Sana başka ekranlar da atmıştım, onlara da test yaz.”

**Beklenen davranış:**
1. Yönlendirme `design` olur ve istek **açık istek** sayılır (kural 9): elenen her ekran için bir test üretilir; mekanizma kapısından ya da ICE eşiğinden geçmediği için reddedilmez, sessizce atlanmaz.
2. Problem sorusu tekrar sorulmaz.
3. Sohbet bir kez, tek satırla söyler: playbook bu testleri eşiğin altında sıralamıştı.
4. Zayıf her kartın altında “Stronger alternative:” ile başlayan bir not vardır (Türkçe kartta karşılığı) ve daha güçlü testi adıyla anar. Bu not, kart altı notlarının “A'yı değiştirme tavsiyesi verilmez” kuralının tek istisnasıdır.
5. Zayıflık dürüstçe yazılır: mekanizma cümlesi “zayıf” diye işaretlenir, kanıt etiketi “sezgi”dir ve “bu düşük güvenli, çünkü …” cümlesi eksik değildir (kural 10).
6. scenario-critic çağrısında hangi testlerin açıkça istendiği söylenir; zayıf mekanizma bu yüzden `FIX` döngüsüne girmez. Diğer denetimler aynen geçerlidir: tek değişken, tek birincil KPI, bağımsız guardrail, kişisel verinin maskelenmesi.
7. Aynı ekrana düşen iki test varsa her birinin “Yapılmaması gerekenler” kutusunda diğerini adıyla anan bir madde bulunur.

**Düşme koşulları:**
- “Bu ekranlarda güçlü bir test yok” denip üretimin reddedilmesi.
- Zayıf testin güçlüymüş gibi sunulması (zayıflık cümlesi ya da “Stronger alternative:” notu yok).
- İstek üzerine üretilen testin dark pattern ya da koruma zayıflatma içermesi: kural 6 açık isteğe rağmen geçerlidir ve o varyant yine reddedilir.
- Problem sorusunun yeniden sorulması.

**Girdi B (tek bir zayıf test için ısrar):** Kullanıcı ürün sayfasının ekran görüntüsünü paylaşmış ve “Buton rengini yeşil yapıp test etmek istiyorum, tasarla.” demiştir. Sayfada butonun görülmesini engelleyen gözlemlenebilir bir sorun yoktur.

**Beklenen davranış:**
1. Test üretilir (açık istek); kart yapılır.
2. Sohbette tek satır: mekanizma zayıf, çünkü butonun fark edilmediğine dair sayfada bir engel görünmüyor. Kartın altında daha güçlü alternatifi adlandıran “Stronger alternative:” notu.
3. Birincil KPI buton tıklaması değil, tamamlanan sonuçtur (sipariş); tıklama ikincil kalır.

**Düşme koşulları:**
- Testin reddedilmesi ya da yerine sorulmadan başka bir test üretilmesi.
- Zayıflığın söylenmemesi.
