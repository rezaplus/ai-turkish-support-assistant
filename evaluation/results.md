# Evaluation Results

API: `http://localhost:8000/api/v1/ask`  
Final result: **12/12 passed**

| ID | Type | Question | Expected status | Actual status | Expected keyword | Expected version | Actual answer | Sources | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | normal | Paketim şehir merkezindeki adresime verildikten sonra yaklaşık kaç iş gününde gelir? | answered | answered | 1-3 iş günü | 1 | Paketim şehir merkezindeki adresime verildikten sonra 1-3 iş gününde gelir. | 01-kargo-teslimat.md v1 (Teslimat takibi) | PASS |
| 2 | normal | Ürünümün üretim hatalarına karşı garanti süresi ne kadar? | answered | answered | 2 yıl | 1 | Elektronik ürünler teslim tarihinden itibaren 2 yıl üretim hatalarına karşı garantidir. | 04-garanti.md v1 (Garanti kapsamı) | PASS |
| 3 | normal | Telefon uygulamasında cihazı eşleştirirken istenen kod kaç haneli oluyor? | answered | answered | altı haneli | 1 | İstenen kod altı haneli oluyor. | 05-kurulum.md v1 (Cihaz eşleştirme) | PASS |
| 4 | normal | Kartla ödeme yaparken 3D Secure doğrulaması gerekli mi? | answered | answered | zorunludur | 1 | Evet, kartlı ödemelerde güvenlik için 3D Secure doğrulaması zorunludur. | 06-odeme.md v1 (3D Secure doğrulama) | PASS |
| 5 | normal | Yanlış şifreyi art arda girersem hesabım ne kadar süreyle kilitli kalır? | answered | answered | 30 dakika | 1 | Üst üste 5 hatalı şifre denemesinden sonra hesap 30 dakika kilitlenir. | 07-uyelik.md v1 (Hesap kilitlenmesi) | PASS |
| 6 | normal | Aynı alışverişte iki farklı indirim kuponunu birlikte kullanabilir miyim? | answered | answered | yalnızca bir kupon | 1 | Hayır, bir siparişte yalnızca bir kupon kullanılabilir. Bu nedenle aynı alışverişte iki farklı indirim kuponunu birlikte kullanamazsınız. | 08-kampanya.md v1 (Kupon kullanımı) | PASS |
| 7 | normal | Kargo çıkmadan önce iptal ettiğim kartlı siparişin parası en geç ne zaman geri gelir? | answered | answered | 1-3 iş günü | 1 | İptal edilen kartlı siparişlerin ödemesi 1-3 iş günü içinde karta iade edilir. | 09-iptal.md v1 (Ödeme iadesi) | PASS |
| 8 | unknown | Ürünün suya dayanıklılık derecesi nedir? | insufficient_information | insufficient_information | — | — | Bu soruyu yanıtlamak için mevcut dokümanlarda yeterli bilgi bulunmuyor. | — | PASS |
| 9 | unknown | Destek ekibine hafta sonu telefonla hangi saatlerde ulaşabilirim? | insufficient_information | insufficient_information | — | — | Bu soruyu yanıtlamak için mevcut dokümanlarda yeterli bilgi bulunmuyor. | — | PASS |
| 10 | unknown | Cihazın kutudan çıkan batarya kapasitesi kaç mAh? | insufficient_information | insufficient_information | — | — | Bu soruyu yanıtlamak için mevcut dokümanlarda yeterli bilgi bulunmuyor. | — | PASS |
| 11 | conflict | Teslim aldığım ürünü geri göndermek için kaç gün içinde başvuru yapmalıyım? | answered | answered | 30 gün | 2 | Teslim tarihinden itibaren 30 gün içinde iade talebi oluşturmalısınız. | 02-iade-guncel.md v2 (İade süresi) | PASS |
| 12 | conflict | İade işlemlerinde hangi prosedür geçerlidir ve iade süresi nedir? | answered | answered | 30 gün | 2 | İade işlemi, teslim tarihinden itibaren 30 gün içinde yapılabilmektedir. Ürün kullanılmamış, aksesuarları ve faturasıyla birlikte olmalıdır. Süre, kargo takip kaydındaki teslim tarihinden itibaren hesaplanır ve resmi tatile denk gelirse talep bir sonraki iş gününün sonuna kadar kabul edilir. | 02-iade-guncel.md v2 (İade süresi) | PASS |
