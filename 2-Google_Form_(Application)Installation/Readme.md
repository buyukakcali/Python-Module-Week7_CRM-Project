Code.gs dosyasi diger tum fonksiyonlari icinde bulunduran kurulum dosyasidir.
Sadece bu dosyayi app script kodunuz olarak kullanabilir ve uygulamanin bu bolumunu eksiksiz yuklemis olabilirsiniz.
Diger moduller (dosyalar) github uzerinden kodlari okumak isteyen kisiler icin kolaylik olmasi yonuyle olusturulmustur...

Asagidaki duzenlemeleri olusturacaginiz google forma uygulamaniz gerekmektedir:

Mail Adresi Dogrulama:
regex yok: Metin ve E-Posta secilir.
Ozel Hata Metni: Girdiginiz metin bir e-posta adresi degil!

Telefon Dogrulama
regex : ^(?:\+)[1-9]\d{1,14}$
Ozel Hata Metni: Lütfen geçerli bir uluslararası telefon numarası girin. Numara '+'' ile başlamalıdır.
