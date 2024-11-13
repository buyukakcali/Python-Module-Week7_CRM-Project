<u><h1><strong>KURULUM:</strong></h1></u>

<u><h3><strong>Adım 1) SQL Modülü Kurulumu:</strong></h3></u>
<br>
<br>

<strong>1-</strong> Şimdi, githubdaki projeyi indirelim, sıkıştırılmış dosyadan çıkartalım.
![SQL 1](https://github.com/user-attachments/assets/d90eab1f-8543-4c58-a3e1-c39d0ded4a25)
<br>
<br>

<strong>2-</strong> Herhangi bir veritabanı yönetim aracıyla veritabanı sunucunuza bağlanın. Amacınız, veritabanınızı hazır hale getirmek! Dilerseniz web ara yüzü ile de bu işlemi gerçekleştirebilirsiniz. Ben, Microsoft Workbench uygulamasını kullanarak nasıl yapıldığını kısaca göstereceğim.
![SQL 2](https://github.com/user-attachments/assets/7a83079d-0416-4457-aa49-c46998f1c018)
<br>
<br>

<strong>3-</strong> Uygulamanın 'Edit' menüsü altındaki SQL yazan butona(İkinci sıradaki SQL yazan buton) tıklayın. Açılan pencereden, biraz önce githubdan indirip klasöre çıkardığınız CRM Projesi klasörünün altındaki '1-SQL_Preparement' klasörünün içine gidin ve '1-CreateANDSetDatabase.sql' dosyasını seçin/açın.
![SQL 3](https://github.com/user-attachments/assets/3746fe29-9287-408e-a74a-6924e1554bba)
<br>
<br>

<strong>4-</strong> Açılan sayfada soldaki sarı şimşek işareti olan butona bir kez tıklayarak kurulumu başlatın. Bittiğinde 'SCHEMAS' yazısının sağında yer alan yenile butonuna tıklayın.
![SQL 4](https://github.com/user-attachments/assets/fbd38105-ed21-4627-b12a-f881e3ea9b94)
<br>
<br>

<strong>5-</strong> Sol widget içinde veritabanını ve altında da tabloları görmelisiniz. Eğer her şey yolundaysa, CRM Projesinin 'SQL Modülü' basariyle kurulmuş demektir.
![SQL 5](https://github.com/user-attachments/assets/9f7408d4-ab9e-4d59-b60c-4eddc00f21cd)
<br>
<br>
<br>

<u><h3><strong>Adım 2) Google Form Modülü Kurulumu (1-VIT_Project_Form formu ve ‘1-FormAnswers’ Web Projesi ):</strong></h3></u>
<br>
<br>
<u><h4><strong>Ön Not:</strong></h4></u> Öncelikle CRM projesi küçük küçük web projelerinin bir araya gelmesinden oluşmaktadır. Biz, bundan sonra kurulumu yapılacak CRM Projesinin her bir küçük web projesini proje diye adlandıracağız. Lütfen bu detayı unutmayınız.
<br>
<br>

<strong>1-</strong> Yeni bir gmail hesabı oluşturun veya mevcut gmail hesabınızla oturum açın.
![Form 1](https://github.com/user-attachments/assets/ae531a6e-2401-41d1-8f0e-67c51a0127dc)
<br>
<br>

<strong>2-</strong>- Google Drive sayfasını açın ve projeye ait her şeyi bulunduracağınız bir klasör oluşturun. <i>(Ben kendi klasörüme 'CRM_Project' ismini verdim.)</i>
![Form 2](https://github.com/user-attachments/assets/82010c27-b1a8-40e3-8255-4ca85dd698a8)
<br>
<br>

<strong>3-</strong> Yeni boş bir form oluşturun veya eski formunuzdan bir kopyayı bu klasör içinde yeniden oluşturun ve formda ayarlamanız gereken yerleri ilgili bölümün Readme dosyasında yazdığı sekliyle düzenleyin.
![Form 3](https://github.com/user-attachments/assets/43107b63-2550-4ac2-9b9f-b001999d25bf)
![Form 3 1](https://github.com/user-attachments/assets/ff67eb81-2365-4d85-9399-44d28badf443)
<br>
<br>

<strong>4-</strong> 'E-Tablolara Bağla' linkine tıklayın.
![Form 4](https://github.com/user-attachments/assets/131c5b58-a898-4305-8204-730adec3e111)
<br>
<br>

<strong>5-</strong> Gelen sayfadaki varsayılan ismi '1-VIT_Project_Form_Answers' olarak değiştirin.
![Form 5](https://github.com/user-attachments/assets/8bee2905-9d19-4d79-a05b-9aeb0a7b1e94)
<br>
<br>

<strong>6-</strong> Oluşan sheet dosyasında, 'Uzantılar' sekmesinden 'Apps Komut Dosyası' seçeneğini seçin.
<i>(Apps Script kodlarını yazacağımız/kopyalayacağımız, kısacası projemizin çoğu ayarının yapılacağı yer burasıdır.)</i>
![Form 6](https://github.com/user-attachments/assets/ea7412d6-748c-4162-a049-76ef0aef043e)
<br>
<br>

<strong>7-</strong> Projenin bu kısmını belirttiğim gibi isimlendirin. '1-FormAnswers'.
![Form 7](https://github.com/user-attachments/assets/419a7484-ec46-40ff-9f0a-49c32eac3b2a)
![Form 7 1](https://github.com/user-attachments/assets/cfe1f6f2-2efa-4a6b-bd69-1f3d233ab678)
<br>
<br>

<strong>8-</strong> Şimdi, githubdan daha önce indirdiğiniz proje klasöründe '2-Google_Form_(Application)Installation' klasörünü bulun ve içindeki kodları projenin bu '1-FormAnswers' modülüne uygun bir şekilde ekleyin, sonrasında her şeyi kaydedin.
![Form 8](https://github.com/user-attachments/assets/dd437f44-35fd-4ab1-a8c8-4cdfbb4f34b8)
![Form 8 1](https://github.com/user-attachments/assets/6b269839-3653-4d0e-8cee-be8aa8289c64)
<br>
<br>

<strong>9-</strong> Şimdi 'SetupWhiteList' fonksiyonunu açıp, veritabanı bağlantı bilgilerinizi buraya girin ve kaydedin.
![Form 9](https://github.com/user-attachments/assets/315a5fca-b951-420c-9cf3-dfeb02f1f9ad)
<br>
<br>

<strong>10-</strong> Aktif fonksiyon 'SetupWhiteList' iken 'Çalıştır' seçeneğine bir kez tıklayarak <i>Seçili İşlevi Çalıştır</i>'ın. Bu işlem hassas olan veritabanı bağlantı bilgilerini Google Apps Script'in properties bölümüne kaydedecektir.
![Form 10](https://github.com/user-attachments/assets/21d19f7d-acb9-4902-8924-e156e4362f61)
<br>

Proje ayarlarından bilgilerin eklenip eklenmediğini kontrol edebilirsiniz.
![Form 10 1](https://github.com/user-attachments/assets/d67a4f42-6bb8-437d-aaac-4861170ffe87)
<br>
<br>

<strong>11-</strong> Son olarak, projemizde 'Tetikleyiciler' menüsüne giderek 'OnFormSubmit' fonksiyonu için bir trigger oluşturacağız. Bu trigger yardımıyla, formdan her bir veri seti doldurulduğunda kodlarımız tetiklenecek ve veriler veritabanımıza (database) aktarılacak.
<i>(Trigger eklendiğinde Google sizden birtakım izinler vermenizi isteyecek. Aşağıdaki fotoğraflarda olduğu gibi bu izinleri verin.)</i>
![Form 11 0](https://github.com/user-attachments/assets/1fa74f5a-441c-48bf-8f39-44b4e98802cb)
![Form 11 1](https://github.com/user-attachments/assets/dd4c67e5-5180-4f8b-940f-1e6ec5caace5)
![Form 11 2](https://github.com/user-attachments/assets/b6416b15-f0c1-41f8-ae63-d1080f2a98f0)
![Form 11 3](https://github.com/user-attachments/assets/079c6d66-bc3c-4dc7-b426-e087def91f58)
![Form 11 4](https://github.com/user-attachments/assets/98843c07-6aca-4a59-85d2-1e60223200ec)
![Form 11 5](https://github.com/user-attachments/assets/cb10d0bc-148d-4d72-86ce-b00479fa1bfc)
![Form 11 6](https://github.com/user-attachments/assets/123ada7a-d549-4625-9290-7919b0c041d8)
![Form 11 7](https://github.com/user-attachments/assets/f8ac2165-9b54-4dbb-bdb1-22964b15753c)

<br>
Böylece CRM Projesinin başvuruların alındığı form bölümünün (1. Google alt projesi veya modülü) kurulumu tamamlanmış oldu.
<br>
<br>

<u><h3><strong>Adım 3) Google Takvim Modülü Kurulumu:</strong></h3></u>
<br>
<br>
