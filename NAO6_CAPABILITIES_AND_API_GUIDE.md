# NAO6 Kapsamlı Yetenek ve API Rehberi

Bu döküman, **SoftBank Robotics / Aldebaran NAO6** insansı robotunun tüm donanımsal ve yazılımsal yeteneklerini, sunduğu API servislerini (`NAOqi 2.8` / `qi` framework) ve bu servislerle nelerin yapılabileceğini kategori kategori detaylandırır.

---

## 📌 İçindekiler
1. [NAOqi Mimarisi ve Temel Mantık](#1-naoqi-mimarisi-ve-temel-mantık)
2. [Hareket, Duruş ve Kinematik (Motion)](#2-hareket-duruş-ve-kinematik-motion)
3. [Ses, Konuşma ve Jestler (Audio & Speech)](#3-ses-konuşma-ve-jestler-audio--speech)
4. [Görme, Kameralar ve Görsel Algı (Vision & Perception)](#4-görme-kameralar-ve-görsel-algı-vision--perception)
5. [Dokunma, Sensörler ve LED Aydınlatma (Sensors & LEDs)](#5-dokunma-sensörler-ve-led-aydınlatma-sensors--leds)
6. [Merkezi Sinir Sistemi: ALMemory ve Olaylar (Events)](#6-merkezi-sinir-sistemi-almemory-ve-olaylar-events)
7. [Otonom Davranışlar ve Canlılık (Autonomous Life)](#7-otonom-davranışlar-ve-canlılık-autonomous-life)
8. [Sistem, Ağ ve Davranış Yönetimi (System & Behaviors)](#8-sistem-ağ-ve-davranış-yönetimi-system--behaviors)
9. [Canlı API Sorgulama Aracı (Robot Inspector)](#9-canlı-api-sorgulama-aracı-robot-inspector)

---

## 1. NAOqi Mimarisi ve Temel Mantık

NAO robotunun işletim sistemi ve ara yazılımı **NAOqi** olarak adlandırılır. NAOqi üzerinde her yetenek bir **servis** (modül) olarak çalışır.

Python üzerinden bir yeteneğe erişmek için iki adım izlenir:
```python
import core.connection as cc

conn = cc.get_connection()
# 1. İlgili servisi al
motion = conn.get_service("ALMotion")
tts = conn.get_service("ALTextToSpeech")

# 2. Servisin fonksiyonlarını çağır
tts.say("Merhaba!")
```

---

## 2. Hareket, Duruş ve Kinematik (Motion)

Robotun 25 serbestlik derecesine (DoF) sahip motorlarını, dengesini ve yürüme algoritmalarını yöneten servislerdir.

### 2.1. `ALMotion`
Robotun motor ve eklem yönetiminin ana merkezidir.
* **Motor Sertliği (Stiffness):** Motorlara güç vermek (`wakeUp()` / `setStiffnesses("Body", 1.0)`) veya motorları serbest bırakmak (`rest()` / `setStiffnesses("Body", 0.0)`).
* **Doğrudan Eklem Kontrolü:** Baş (`HeadYaw`, `HeadPitch`), omuzlar, dirsekler, bilekler ve bacak açılarını derece/radyan cinsinden oynatma:
  * `setAngles(names, angles, fractionMaxSpeed)`: Anlık açı komutu.
  * `angleInterpolation(names, keys, times, isAbsolute)`: Zaman çizelgesine bağlı yumuşak ve akıcı eklem hareketleri (dans, selam verme vb.).
* **Eller:** Parmakları açıp kapatma (`openHand("RHand")`, `closeHand("RHand")`).
* **Yürüme & Gezinme (Omnidirectional Walking):**
  * `moveTo(x, y, theta)`: Robotun belirlenen metre ve açı kadar yürümesi (örn. 0.5 metre ileri, 0.2 metre sola, 90 derece dön).
  * `moveToward(x_speed, y_speed, theta_speed)`: Sürekli hız vektörüyle yürüme (joystick veya klavye ile kontrol için idealdir).
  * `stopMove()`: Yürümeyi anında güvenli bir şekilde durdurur.
* **Tüm Vücut Dengesi (Whole Body Balancer):** Robot bir ayağını kaldırdığında düşmemek için ağırlık merkezini diğer ayağa otomatik kaydırır (`wbEnable(True)`).
* **Çarpışma Koruması (Anti-Collision & Fall Manager):**
  * Robot kollarını hareket ettirirken kendi gövdesine veya bacaklarına çarpmasını yazılımsal olarak engeller (`setCollisionProtectionEnabled`).
  * Robot dengesini kaybedip düşmeye başladığında motorları serbest bırakıp kendini koruma pozisyonuna alır (`setSmartStiffnessEnabled(True)`).

### 2.2. `ALRobotPosture`
Robotun dengeli ve standart duruşlara geçmesini sağlar:
* `goToPosture("StandInit", 1.0)`: Standart hazırda bekleme ayakta duruşu.
* `goToPosture("Sit", 1.0)`: Oturma pozisyonuna geçiş.
* `goToPosture("Crouch", 1.0)`: Çömelme (motorları dinlendirme) pozisyonu.
* `goToPosture("LyingBelly", 1.0)` / `goToPosture("LyingBack", 1.0)`: Karın üstü / sırt üstü yatış.
* `getPostureFamily()`: Robotun şu an ayakta mı, oturuyor mu yoksa düşmüş mü olduğunu döner.

### 2.3. `ALTracker`
Robotun belirli bir hedefi otomatik olarak gözleriyle, başıyla veya tüm vücuduyla takip etmesini sağlar.
* **Hedef Tipleri:** `"Face"` (İnsan yüzü), `"RedBall"` (Kırmızı top), `"Sound"` (Gelen ses), `"LandMark"` (QR/İşaretçi), `"People"` (İnsan).
* **Takip Modları:**
  * `Head`: Sadece başını çevirerek hedefi takip eder.
  * `WholeBody`: Baş yetmediğinde vücudunu da hedefe doğru çevirir.
  * `Move`: Hedef uzaklaştıkça hedefe doğru adım atarak yaklaşır.

---

## 3. Ses, Konuşma ve Jestler (Audio & Speech)

### 3.1. `ALTextToSpeech` (TTS)
Robotun konuşmasını sağlar.
* `say("Metin")`: Verilen metni seslendirir.
* `setLanguage("Turkish")` / `setLanguage("English")`: Konuşma dilini değiştirir.
* `setParameter("pitchShift", 1.1)`: Ses inceliğini/kalınlığını değiştirir.
* `setParameter("speed", 90)`: Konuşma hızını ayarlar.
* `setVolume(0.8)`: Ses seviyesini (0.0 - 1.0) belirler.

### 3.2. `ALAnimatedSpeech` (Beden Dilli Konuşma)
Robot konuşurken cümlenin vurgusuna göre ellerini, kollarını ve başını hareket ettirerek canlı bir insan gibi konuşur.
* `say("^start(animations/Stand/Gestures/Hey_1) Merhaba arkadaşlar! ^wait(animations/Stand/Gestures/Hey_1) Bugün nasılsınız?")`
* Metin içerisine animasyon etiketleri yerleştirerek konuşma ile hareketi kusursuz senkronize edebilirsiniz.

### 3.3. `ALAudioPlayer`
Robotun hoparlörlerinden ses dosyaları çalar.
* `playFile("/home/nao/sounds/laugh.mp3")`: Dahili MP3/WAV dosyalarını çalar.
* `playSine(frequency, gain, pan, duration)`: Test tonu/bip sesi üretir.

### 3.4. `ALSoundLocalization`
Robotun kafasında 4 adet yönsel mikrofon bulunur.
* Bir ses duyulduğunda sesin geldiği açıyı (Yatay ve dikey açı cinsinden) tespit eder.
* Bu veri `ALMemory` üzerindeki `ALSoundLocalization/SoundLocated` anahtarına yazılır. Robot sesin geldiği yöne kafasını çevirebilir.

### 3.5. `ALSpeechRecognition`
Kullanıcının söylediği belirli kelimeleri algılar.
* `setVocabulary(["evet", "hayir", "otur", "kalk"], False)`
* `subscribe("SesDinleyici")`: Kullanıcı bu kelimelerden birini söylediğinde `WordRecognized` olayı tetiklenir.

---

## 4. Görme, Kameralar ve Görsel Algı (Vision & Perception)

NAO6'nın alın ve ağız bölgesinde 2 adet HD kamera yer alır:
* **Üst Kamera (Top Camera - 0):** Karşıya ve insan yüzlerine bakar.
* **Alt Kamera (Bottom Camera - 1):** Ayak uçlarına, zemine ve engellere bakar.

### 4.1. `ALVideoDevice`
Kameradan canlı görüntü karesi çekip OpenCV gibi görüntü işleme kütüphanelerine aktarır.
* Çözünürlükler: `kQQVGA` (160x120), `kQVGA` (320x240), `kVGA` (640x480), `k4VGA` (1280x960).
* Renk Formatları: `kRGBColorSpace`, `kBGRColorSpace` (OpenCV formatı).
* `subscribeCamera("my_cam", 0, 2, 13, 30)` -> `getImageRemote(sub)` ile ham pixel dizisi alınır.

### 4.2. `ALFaceDetection` & `ALFaceCharacteristics`
* **Yüz Tespiti:** Görüş açısındaki tüm insan yüzlerinin koordinatlarını döner.
* **Yüz Öğrenme & Tanıma:** `learnFace("Aliihsan")` ile belirli yüzleri robotun hafızasına kaydedebilir, robot o kişiyi gördüğünde adıyla hitap etmesini sağlayabilirsiniz.
* **Yüz Analizi:** Kişinin tahmini yaşı, cinsiyeti ve **gülümseme derecesi** (smile degree) tespit edilir.

### 4.3. `ALPeoplePerception` & `ALMovementDetection`
* Robotun çevresinde bir insanın varlığını 3 boyutlu koordinat olarak algılar.
* Odadaki herhangi bir görsel hareketi anında tespit eder.

### 4.4. `ALBarcodeReader` & `ALLandMarkDetection`
* Standart barkod ve QR kodları okur, metin içeriğini çıkarır.
* Aldebaran görsel işaretçilerini (Landmark / AprilTag benzeri) tanıyarak hedefe göre konum hesabı yapar.

---

## 5. Dokunma, Sensörler ve LED Aydınlatma (Sensors & LEDs)

### 5.1. `ALTouch` (Dokunmatik Sensörler)
Robotun gövdesinde kapasitif dokunmatik alanlar ve mekanik anahtarlar bulunur:
* **Baş Sensörleri:** Ön (`Front`), Orta (`Middle`), Arka (`Rear`).
* **El Sensörleri:** Sol ve Sağ el üstü (`LHand/Touch/Back`, `RHand/Touch/Back`).
* **Ayak Tamponları (Bumpers):** Sol/Sağ ayak, iç/dış tamponlar. Ayağı bir sehpaya veya duvara çarptığında hemen hisseder.
* **Göğüs Düğmesi:** Basıldığında pil durumunu söyler veya özel event tetikler.

### 5.2. `ALLeds` (RGB Göz, Kulak ve Göğüs Işıkları)
Robotun ruh halini, konuşma veya dinleme durumunu ifade etmek için LED'ler kontrol edilir:
* `fadeRGB("FaceLeds", 0.0, 1.0, 0.0, 0.5)`: Gözleri yeşile çevirir (Onay/Başarı).
* `fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 0.5)`: Gözleri kırmızıya çevirir (Hata/Tehlike).
* `rotateEyes(0x0000FF, 1.0, 3.0)`: Göz halkasındaki LED'leri mavi renkte döndürür (Düşünme animasyonu).
* `rasta(duration)`: Rengarenk gökkuşağı animasyonu.
* **Kulak LED'leri:** 9 segmentli dairesel LED'ler, genelde şarj seviyesini veya ses yüksekliğini göstermek için kullanılır.

### 5.3. `ALSensors` (Dahili Ataletsel ve Ultrasonik Sensörler)
* **Sonar (Ultrasonik Mesafe Sensörü):** Göğsündeki 2 verici ve 2 alıcı ile 0.25m - 2.5m arasındaki engellerin mesafesini ölçer.
* **IMU (Ataletsel Ölçüm Birimi):** Jiroskop ve ivmeölçerler sayesinde robotun eğim açısını (Pitch, Roll) ve ivmesini milisaniyelik okur.
* **FSR (Ayak Tabanı Basınç Sensörleri):** Her ayakta 4'er adet basınç sensörü bulunur. Ağırlığın topukta mı parmak ucunda mı olduğunu ölçer.

### 5.4. `ALBattery` & `ALBodyTemperature`
* Batarya doluluk yüzdesi, şarj kablosunun takılı olup olmadığı.
* 25 adet eklemin motor sıcaklıkları (aşırı ısınmada robot kendini korumaya alır).

---

## 6. Merkezi Sinir Sistemi: `ALMemory` ve Olaylar (Events)

`ALMemory`, robot üzerindeki tüm sensör verilerinin, olayların ve durumların tutulduğu merkezi kara tahtadır (Blackboard).

Örnek olarak robotun kafasına dokunulduğunu yakalamak:
```python
memory = conn.get_service("ALMemory")

# 1. Anlık sensör değerini okuma:
is_head_touched = memory.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value")

# 2. Olaylara (Events) abone olma (Callback):
# "FrontTactilTouched", "FaceDetected", "WordRecognized", "RightBumperPressed" vb.
```

---

## 7. Otonom Davranışlar ve Canlılık (Autonomous Life)

Robotun cansız bir heykel gibi durmasını engelleyen, ona "canlı" hissi veren otonom servisler:

* **`ALBasicAwareness`**: Odadaki bir insanı, hareketi veya sesi fark ettiğinde başını gayriihtiyari o yöne çevirir ve göz teması kurar.
* **`ALBackgroundMovement`**: Robot ayakta dururken hafif hafif ağırlık merkezini değiştirir ve nefes alma hareketleri yapar.
* **`ALAutonomousBlinking`**: Göz LED'lerini insan gözü kırpması gibi doğal aralıklarla hafifçe söndürüp yakar.
* **`ALAutonomousLife`**: Otonom yaşam döngüsünü açıp kapatır (`setState("disabled")` veya `"solitary"`).

---

## 8. Sistem, Ağ ve Davranış Yönetimi (System & Behaviors)

* **`ALBehaviorManager`**: Choregraphe içinde tasarlanıp robota yüklenmiş kutu davranışlarını (danslar, oyunlar, sunumlar) Python'dan tetikler:
  * `runBehavior("dans_koreografisi")`
* **`ALConnectionManager`**: WiFi ağlarını tarar, şifreli ağlara bağlanır veya robotu Access Point moduna alır.
* **`ALSystem`**: Robotun adını, IP adresini, disk kullanımını öğrenme; robotu kapatma (`shutdown()`) veya yeniden başlatma (`reboot()`).

---

## 9. Canlı API Sorgulama Aracı (Robot Inspector)

Robotunuz veya Choregraphe sanal robotunuz açıkken projenize eklenen **`inspect_robot.py`** aracını kullanarak robotun içindeki tüm servisleri ve metotları canlı canlı terminalden inceleyebilirsiniz:

### 1. Robottaki Tüm Aktif Servisleri Listeleme:
```powershell
.\nao_python.bat inspect_robot.py
```

### 2. Belirli Bir Servisin Tüm Fonksiyonlarını Görme:
```powershell
.\nao_python.bat inspect_robot.py ALMotion
.\nao_python.bat inspect_robot.py ALTextToSpeech
.\nao_python.bat inspect_robot.py ALLeds
```

### 3. Belirli Bir Fonksiyonun Ne İşe Yaradığını ve Parametrelerini Görme:
```powershell
.\nao_python.bat inspect_robot.py ALMotion moveTo
.\nao_python.bat inspect_robot.py ALTextToSpeech say
.\nao_python.bat inspect_robot.py ALLeds fadeRGB
```

Bu döküman ve `inspect_robot.py` aracı sayesinde NAO6'nın sunduğu tüm yeteneklere istediğiniz an başvurabilir, geliştireceğiniz projelerde robotun tüm potansiyelinden yararlanabilirsiniz!
