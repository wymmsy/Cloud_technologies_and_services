## Лабораторная работа 1. Знакомство с IaaS, PaaS, SaaS сервисами в облаке на примере Amazon Web Services (AWS). Создание сервисной модели.


В первой лабораторной работе был разработан фрагмент биллинга AWS и превращение его в сервисную модель с уровнями абстракции. Основной упор был на понимание того, что именно потребляет заказчик в облаке и как это отнести к понятным категориям (Storage, Compute, Cloud Services и т.д.).​
Ход работы
Сначала был импортирован выданный CSV с полями Product Code, Usage Type, lineItem/Operation, lineItem/LineItemDescription и пустыми колонками IT Tower, Service Family, Service Type, Service Sub Type, Service Usage Type. В качестве ориентира использовался примерный файл с маппингом, где показано, как по комбинации Product Code и Usage Type можно восстановить высокоуровневую классификацию сервиса.​ Дальше в лабораторной работа шла снизу вверх, от сырых кодов в биллинге к понятной иерархии сервисов. 
***

## 1. Группировка по Product Code и выбор IT Tower / Service Family / Service Type

### 1) AmazonS3

1. Сначала я отфильтровала строки по `Product Code = AmazonS3`.  
2. Посмотрела на смысл сервиса: Amazon S3 — это объектное хранилище файлов и данных в AWS, которое в типичных схемах относится к блоку Storage.  
3. Поэтому в колонке **IT Tower** для всех строк с AmazonS3 я указала `Storage` — этим я зафиксировала, что независимо от того, какие именно операции выполнялись (хранение, запросы, штрафы), все они относятся к «башне» хранения данных.  
4. Дальше я выбрала **Service Family**. В примере сервисов у провайдера для S3/Glacier использовалась семья `Storage&Content Delivery`, которая объединяет хранилище и доставку контента. Это достаточно логично, так как S3 часто используется и как хранилище, и как источник для отдачи данных наружу. 
5. В колонке **Service Type** я написала `Amazon S3` — это имя конкретного сервиса, чтобы в дальнейшем в модели можно было различать, что именно за облачный продукт стоит за расходами.

Таким образом, для AmazonS3 я сначала зафиксировала три верхних уровня: Storage → Storage&Content Delivery → Amazon S3. А уже потом внутри этой группы разбирала, что именно делает каждая строка Usage Type.

### 2) AmazonGlacier

1. Аналогично я отфильтровала строки по `Product Code = AmazonGlacier`.  
2. Amazon Glacier — это архивное хранилище, где данные лежат долго и дёшево, но доступ к ним медленнее. Узнала, что такие хранилища называют “холодными”. А по смыслу это тоже часть блока хранения.  
3. Поэтому **IT Tower** снова был `Storage` для всех строк Glacier.  
4. **Service Family** я оставила той же — `Storage&Content Delivery`, потому что Glacier в примерах также относился к этому семейству и логически продолжает тему хранения и архивации.  
5. **Service Type** — `Amazon Glacier`, чтобы отделить его от S3, хотя они в одной башне и одной семье.
Так появилась вторая ветка в модели: Storage → Storage&Content Delivery → Amazon Glacier.

### 3) AmazonRedshift

1. Далее я взяла строки с `Product Code = AmazonRedshift`.  
2. Amazon Redshift — это аналитическое хранилище данных, управляемый сервис для аналитики и запросов по большим объёмам данных. Это уже не просто виртуальный диск, а довольно умный сервис.  
3. Поэтому **IT Tower** я выбрала `Cloud Services`, это показывает, что мы имеем дело с облачным сервисом, а не с инфраструктурой, и сервис более управляемый.
4. В качестве **Service Family** я выбрала `Analytics`, потому что Redshift используют именно для аналитики и BI‑нагрузок (запросы по большим датасетам, отчётность и т.д.).  
5. В **Service Type** записала `Amazon Redshift`, чтобы в модели была отдельная сущность для этого аналитического сервиса.

Получилась ветка Cloud Services → Analytics → Amazon Redshift.

### 4) AWSDirectoryService

1. Затем я сгруппировала строки по `Product Code = AWSDirectoryService`.  
2. AWS Directory Service — это сервис каталогов (Active Directory, Simple AD, AD Connector), то есть про управление пользователями, группами и аутентификацией. Это уже не хранилище и не вычисления, это сервис идентификации и безопасности.  
3. Поэтому для **IT Tower** я выбрала `Cloud Services` — это снова управляемый облачный сервис.  
4. **Service Family** поставила `Security and Identity`, потому что каталог пользователей — это часть системы безопасности и управления доступом.  
5. В **Service Type** указала `AWS Directory Service`.

Снова добавила ветку: Cloud Services → Security and Identity → AWS Directory Service.

### 5) AmazonSNS

1. Далбше `Product Code = AmazonSNS`.  
2. Amazon SNS — сервис уведомлений, он умеет отправлять сообщения по HTTP, в очереди SQS, SMS и push‑уведомления. Это прикладной облачный сервис, не инфраструктура.  
3. Поэтому **IT Tower** для него — `Cloud Services`.  
4. В **Service Family** я выбрала `Application Services`, так как у SNS  есть прикладная функциональность, он отправляет сообщения другим приложениям.  
5. В **Service Type** записала `Amazon SNS`.

Получилась ветка Cloud Services → Application Services → Amazon SNS.

### 6) AmazonML, Translate, Transcribe, Polly

Для всех AI‑сервисов логика была одинаковой:

- `AmazonML` (машинное обучение, обучение и оценка моделей)
- `translate` (Amazon Translate, перевод текста)
- `transcribe` (Amazon Transcribe, распознавание речи)
- `AmazonPolly` (синтез речи)

Для каждой группы:

1. **IT Tower** = `Cloud Services`, потому что это полностью управляемые облачные сервисы, где пользователь просто вызывает высокоуровневые операции (перевести текст, распознать аудио, сгенерировать речь).  
2. **Service Family** = `Artificial Intelligence`, так как все эти услуги так или инче относятся к машинному обучению.  
3. **Service Type** = имя конкретного сервиса: `Amazon ML`, `Amazon Translate`, `Amazon Transcribe`, `Amazon Polly`.

В модели появилась ветка Cloud Services → Artificial Intelligence → (конкретные AI‑сервисы).

### 7) AWSCodePipeline и CodeBuild

1. Для `AWSCodePipeline` и `CodeBuild` я также сначала отфильтровала строки по Product Code.  
2. Оба сервиса относятся к инструментам разработчика: CodePipeline — CI/CD конвейеры, CodeBuild — сборка кода.  
3. Поэтому у обоих:  
   - **IT Tower** = `Cloud Services`  
   - **Service Family** = `Developer Tools`
   - **Service Type** = `AWS CodePipeline` или `AWS CodeBuild`

Эта ветка описывает блок сервисов, которые помогают строить и разворачивать приложения: Cloud Services → Developer Tools → (CodePipeline/CodeBuild).

***

## 2. Детализация внутри группы: Service Sub Type и Service Usage Type

После того как для каждой группы сервисов были выбраны IT Tower, Service Family и Service Type, внутри каждой группы я разбирала `Usage Type` (и иногда `lineItem/Operation`) и уже на этой основе задавала **Service Sub Type** и **Service Usage Type**.

### 1) Внутри AmazonS3

1. Я просмотрела все значения `Usage Type` у AmazonS3. Там были маски вида `EarlyDelete-*`, `Requests%TierN`, `TagStorage-TagHrs%`.  
2. Логика была такая:  
   - если Usage Type описывает штраф за раннее удаление, то это один тип использования
   - если описывает запросы к S3 — другой
   - если описывает хранение тегов — уже третий

Примеры:

- Для `Usage Type = %EarlyDelete-GDA` я поняла, что это Early Delete для класса Glacier Deep Archive. Таким образом:  
  - **Service Sub Type** = `Glacier Deep Archive` — это конкретный класс хранения 
  - **Service Usage Type** = `Early Delete Fee` — вид потребления, штраф

- Для `Usage Type = %Requests%Tier3` (и других Tier1–Tier6) я трактовала это как платные запросы к S3. Поэтому:  
  - **Service Sub Type** = `Requests Tier3` (для каждой строки свой Tier)
  - **Service Usage Type** = `API Requests` — общий тип потребления

- Для `Usage Type = %TagStorage-TagHrs%` это оплата за хранение тегов:  
  - **Service Sub Type** = `Tag Storage`
  - **Service Usage Type** = `Tag Hours` 

Главный принцип: Sub Type показывает, что именно внутри сервиса, а Usage Type — какой ресурс или операция оплачивается (хранение, запрос, штраф и т.д.).

### 2) Внутри AmazonGlacier

1. Для AmazonGlacier Usage Type были `ProvisionedCapacityUnit`, `TimedStorage-ByteHrs`, `Requests-Tier1/3`, `EarlyDelete`.  
2. Логика:

- `ProvisionedCapacityUnit` — заранее купленная ёмкость запросов:  
  - Sub Type = `Provisioned Capacity`
  - Usage Type = `Provisioned Capacity Unit`

- `TimedStorage-ByteHrs` — хранение данных в байтах*часах (байты умноженные на часы):  
  - Sub Type = `Archive Storage`
  - Usage Type = `Storage Byte-Hours`

- `Requests-Tier1/3` — запросы восстановления или доступа:  
  - Sub Type = `Requests Tier1` / `Requests Tier3`
  - Usage Type = `Requests`

- `EarlyDelete` — штраф за удаление до окончания срока:  
  - Sub Type = `Archive Storage`
  - Usage Type = `Early Delete Fee`

Здесь видно, что один и тот же подтип (Archive Storage) может давать как обычное хранение, так и штрафы.

### 3) Внутри AmazonRedshift

1. В Redshift Usage Type вида `Node:ra`, `Node:dc`, `Node:ds` показывали разные типы узлов кластера.  
2. Поэтому:  
   - Sub Type = `RA Node` / `DC Node` / `DS Node`
   - Usage Type = `Node Usage` — плата за работу узлов

3. Для `Usage Type = %DataScanned%` было понятно, что это объём данных, который сканируется запросами:  
   - Sub Type = `Query Processing` (или `Data Scanned`)
   - Usage Type = `Data Scanned`

4. Для `Usage Type = %RMS%` (служебные услуги Redshift) я выбрала:  
   - Sub Type = `Redshift Managed Services`
   - Usage Type = `Service Fee`

Так в модели раздельно видны затраты на «железо» (узлы), на «работу запросов» (сканирование данных) и на «служебные сервисы».

### 4) Внутри AWSDirectoryService

1. В Directory Service я ориентировалась на то, какой тип каталога или коннектора используется.  
2. Например:

- `Usage Type = %MicrosoftAD-DC-Usage` — управляемый Microsoft AD:  
  - Sub Type = `Microsoft AD`
  - Usage Type = `Domain Controller Usage`

- `Usage Type = %SimpleAD-Usage` — Simple AD:  
  - Sub Type = `Simple AD`
  - Usage Type = `Directory Usage` 

- `Usage Type = %Small-Directory-Usage` — маленький каталог:  
  - Sub Type = `Small Directory`
  - Usage Type = `Directory Usage`  

- `Usage Type = %Large-ADConnector-Usage` — крупный AD Connector:  
  - Sub Type = `AD Connector Large`
  - Usage Type = `Connector Usage`

- `Tax%` — налоги:  
  - Sub Type = `Directory Service`
  - Usage Type = `Tax`

Здесь Sub Type показывает, какой именно продукт каталога используется, а Usage Type — что именно считается, это может быть использование каталога, использование коннектора или налог.

### 5) Внутри AmazonSNS

1. В SNS Usage Type сразу показывали каналы доставки и тип расхода: DeliveryAttempts-HTTP, DeliveryAttempts-SQS, SMS-Price, SMS-Sent, DeliveryAttempts-APNS.  
2. Поэтому:

- `DeliveryAttempts-HTTP`:  
  - Sub Type = `HTTP Delivery`
  - Usage Type = `Delivery Attempts`

- `DeliveryAttempts-SQS`:  
  - Sub Type = `SQS Delivery`
  - Usage Type = `Delivery Attempts`

- `SMS-Price%`:  
  - Sub Type = `SMS`
  - Usage Type = `SMS Price`

- `SMS-Sent%`:  
  - Sub Type = `SMS` 
  - Usage Type = `SMS Sent`

- `DeliveryAttempts-APNS%`:  
  - Sub Type = `APNS Delivery`
  - Usage Type = `Delivery Attempts`

Так мы чётко разделяем, где платим за попытки доставки, а где за сами SMS, и какими каналами сообщения идут.

### 6) Внутри AmazonML

1. Для AmazonML Usage Type в обеих строках был `%AMLBoxUsage`, но в Operation появлялись `TrainModel` и `EvaluateModel`.  
2. Я использовала Operation, чтобы разделить фазы ML‑процесса:  
   - строка с TrainModel:  
     - Sub Type = `Model Training`
     - Usage Type = `ML Box Usage`
   - строка с EvaluateModel:  
     - Sub Type = `Model Evaluation`
     - Usage Type = `ML Box Usage`  

Это показывает, что расходуется один и тот же ресурс (ML Box), но на разных этапах — обучение и оценка.

### 7) Внутри Translate, Transcribe и Polly

**Translate:**

- Usage Type = `%TranslateText`
  - Sub Type = `Text Translation`
  - Usage Type = `Characters Translated` (или аналог, явно связанный с объёмом текста).  

**Transcribe:**

- `%StreamingAudio` + Operation StreamingAudio:  
  - Sub Type = `Streaming Transcription`
  - Usage Type = `Streaming Audio Minutes`

- `%TranscribeAudio` + Operation TranscribeAudio:  
  - Sub Type = `Batch Transcription`
  - Usage Type = `Audio Minutes`

**Polly:**

- Для AmazonPolly (при общем Usage Type):  
  - Sub Type = `Text-to-Speech`
  - Usage Type = `Speech Requests` / `Audio Generation`

Здесь я увидела одну идею: Sub Type различает задачу (например, перевод текста, стримовое распознавание, пакетное, синтез речи) и Usage Type — “единицу измерения” (символы, минуты аудио, количество запросов).

### 8) Внутри CodePipeline и CodeBuild

**CodePipeline:**

- `Tax%`:  
  - Sub Type = `CodePipeline Service`
  - Usage Type = `Tax`

- `%trialPipeline%`:  
  - Sub Type = `Trial Pipeline`
  - Usage Type = `Pipeline Usage`

**CodeBuild:**

- Общий Usage Type сборки:  
  - Sub Type = `Build`
  - Usage Type = `Build Usage` (или `Build Minutes`)

Видно, что в Developer Tools платим либо за использование пайплайна или сборки, либо за налог, что позволяет потом отдельно проанализировать стоимость CI/CD.

***

## 3. Основная выявленная закономерность и итог

Во всей работе соблюдалось основное правило: **один и тот же Product Code всегда относится к одним и тем же IT Tower и Service Family**.  
- Если строки про S3 — это всегда Storage / Storage&Content Delivery.  
- Если строки про Redshift — это всегда Cloud Services / Analytics.  
- Если строки про Translate или ML — всегда Cloud Services / Artificial Intelligence и т.д.

Благодаря такой закономерность модель получилась устойчивой. К ней можно вернуться и добавить новые Usage Type, но верхние уровни (такие как башня, семейство, сервис) останутся такими же. 

В итоге весь набор строк из слепка биллинга был переведён из низкоуровневых кодов в понятную модель с уровнями: IT Tower → Service Family → Service Type → Service Sub Type → Service Usage Type. Для каждого сервиса были осмысленно выбраны башня и семейство (Storage, Analytics, Developer Tools, Artificial Intelligence, Security and Identity и т.д.), ну а Usage Type аккуратно разложен на подтипы и виды потребления (хранение, запросы, штрафы, минуты вычислений, сообщения, налоги).​
Аналитически эта работа дала понимание, какие именно ресурсы реально потребляются. Также стало видно, что, например, по S3 значимая часть затрат может приходиться не “чисто на хранение”, как я могла бы подумать, а на запросы и Early Delete, а по аналитике на типы узлов и объём сканируемых данных. ПРи помощи получившийся модели мы можем смотреть на биллинг как бы “от большего к меньшему”, начиная от крупных башен (Storage, Cloud Services) и заканчивая конкретными типами использования (Requests Tier3, Early Delete Fee, Model Training и т.п.).
