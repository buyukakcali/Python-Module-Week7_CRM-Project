<u><h1><strong>KURULUM:</strong></h1></u>

<u><h3><strong>Adım 1) SQL Modülü Kurulumu:</strong></h3></u>
<br>
<br>

<strong>1-</strong> Şimdi, githubdaki projeyi indirelim, sıkıştırılmış dosyadan çıkartalım.
![SQL 1](https://github.com/user-attachments/assets/51c66e3a-e594-4e32-bb31-d1ee4c9b0283)
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
![Form 1](https://github.com/user-attachments/assets/b5c81767-4eba-462a-bc15-54498f57914a)
<br>
<br>

<strong>2-</strong>- Google Drive sayfasını açın ve projeye ait her şeyi bulunduracağınız bir klasör oluşturun. <i>(Ben kendi klasörüme 'CRM_Project' ismini verdim.)</i>
![Form 2](https://github.com/user-attachments/assets/bc827c4f-f30c-4cf2-a02e-1c41845596b7)
<br>
<br>

<strong>3-</strong> Yeni boş bir form oluşturun veya eski formunuzdan bir kopyayı bu klasör içinde yeniden oluşturun ve formda ayarlamanız gereken yerleri ilgili bölümün Readme dosyasında yazdığı sekliyle düzenleyin.
![Form 3 1](https://github.com/user-attachments/assets/d91f2364-caaf-4e7a-b984-71b0b254629d)
![Form 3 2](https://github.com/user-attachments/assets/a603d592-e7d8-4629-8612-bd795aac4fb6)
<br>
<br>

<strong>4-</strong> 'Link to Sheets' linkine tıklayın.
![Form 4](https://github.com/user-attachments/assets/c68154bc-0d1d-4461-a738-de965efffd77)
<br>
<br>

<strong>5-</strong> Gelen sayfadaki varsayılan ismi '1-VIT_Project_Form_Answers' olarak değiştirin.
![Form 5](https://github.com/user-attachments/assets/b3824a83-f85b-4a27-945d-0f16e2990605)
<br>
<br>

<strong>6-</strong> Oluşan sheet dosyasında, 'Extensions' sekmesinden 'Apps Script' seçeneğini seçin.
<i>(Apps Script kodlarını yazacağımız/kopyalayacağımız, kısacası projemizin çoğu ayarının yapılacağı yer burasıdır.)</i>
![Form 6](https://github.com/user-attachments/assets/9066dea7-c011-4c76-b618-a3eee18130de)
<br>
<br>

<strong>7-</strong> Projenin bu kısmını belirttiğim gibi isimlendirin. '1-FormAnswers'.
![Form 7](https://github.com/user-attachments/assets/8141ebc4-401f-4a37-83a7-022d87390288)
<br>
<br>

<strong>8-</strong> Şimdi, githubdan daha önce indirdiğiniz proje klasöründe '2-Google_Form_(Application)Installation' klasörünü bulun ve içindeki kodları projenin bu '1-FormAnswers' modülüne uygun bir şekilde ekleyin, sonrasında her şeyi kaydedin.
![Form 8 1](https://github.com/user-attachments/assets/a6d56162-1677-47aa-b3da-62edc1ce276e)
![Form 8 2](https://github.com/user-attachments/assets/2bd53b06-5a46-4342-bbcc-25b82fd10658)
<br>
<br>

<strong>9-</strong> Şimdi 'SetupWhiteList' fonksiyonunu açıp, veritabanı bağlantı bilgilerinizi buraya girin ve kaydedin.
![Form 9](https://github.com/user-attachments/assets/c39ec552-294f-4153-b842-ef0034607334)
<br>
<br>

<strong>10-</strong> Aktif fonksiyon 'SetupWhiteList' iken 'Run' seçeneğine bir kez tıklayarak <i>seçili işlevi çalıştır (Run the selected function)</i>'ın. 
![Form 10 1](https://github.com/user-attachments/assets/a5cc833e-b61d-4d8a-af05-8d41f52d3371)
<br>

Fonksiyonu çalıstırdığınızda, bir izin sayfası açılacaktır. Fotoğraflardaki gibi bu izini verin.
![Form 10 2](https://github.com/user-attachments/assets/25483e2b-4b16-4ef4-9f66-bac7a1317b93)
![Form 10 3](https://github.com/user-attachments/assets/f67acd6e-5d45-46a8-8a85-4c7984b0c3d2)
![Form 10 4](https://github.com/user-attachments/assets/4a394bc2-76c4-486d-8f01-4b9326f5bce3)
![Form 10 5](https://github.com/user-attachments/assets/c36260b7-0369-4a01-aef9-512248855f8a)
![Form 10 6](https://github.com/user-attachments/assets/75fe4aa2-dda1-4bb6-85e5-a1fb25a34e76)
<br>

Bu işlem hassas olan veritabanı bağlantı bilgilerini Google Apps Script'in properties bölümüne kaydedecektir. Proje ayarlarından bilgilerin eklenip eklenmediğini kontrol edebilirsiniz.
![Form 10 7](https://github.com/user-attachments/assets/1b40c0a6-fbc5-434d-9af8-cb4d9b53f044)
<br>
<br>

<strong>11-</strong> Son olarak, projemizde 'Triggers' menüsüne giderek 'OnFormSubmit' fonksiyonu için bir trigger oluşturacağız. Bu trigger yardımıyla, formdan her bir veri seti doldurulduğunda kodlarımız tetiklenecek ve veriler veritabanımıza (database) aktarılacak.
<i>(Trigger eklendiğinde Google sizden birtakım izinler vermenizi isteyecek. Aşağıdaki fotoğraflarda olduğu gibi bu izinleri verin.)</i>
![Form 11 1](https://github.com/user-attachments/assets/15fb675a-af36-4f9f-b111-5d4f0cc944ee)
![Form 11 2](https://github.com/user-attachments/assets/f0958faa-ea31-41e6-a289-9d24f422a0ae)
![Form 11 3](https://github.com/user-attachments/assets/1b5bc104-67d9-43d7-bf11-156b0fb7d06e)
![Form 11 4](https://github.com/user-attachments/assets/fb0d511f-feb1-4ec3-bba8-619b030ec7b6)
![Form 11 5](https://github.com/user-attachments/assets/45a98b8c-06b2-4328-a5b2-b91da33b799c)
![Form 11 6](https://github.com/user-attachments/assets/ad8eaaa1-a917-4a58-80c9-3e82eb3c49dc)
![Form 11 7](https://github.com/user-attachments/assets/7c17a3d8-5467-4514-904b-1c55079a479f)
<br>

Böylece CRM Projesinin başvuruların alındığı form bölümünün (1. Google alt projesi veya modülü) kurulumu tamamlanmış oldu.
<br>
<br>

<u><h3><strong>Adım 3) Google Takvim Modülü Kurulumu:</strong></h3></u>
<br>
<br>
