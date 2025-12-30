# Лабораторная работа 2.  Сравнение сервисов Amazon Web Services и Microsoft Azure. Создание единой кросс-провайдерной сервисной модели.

Во второй лабораторной работе я взяла свою модель из ЛР1 и «поверх неё разложила» Azure‑сервисы, чтобы в итоге получилась единая кросс‑провайдерная модель, где AWS и Azure живут в одних и тех же категориях: IT Tower / Service Family / Service Type. В отчёте я также кратко описываю, что это за Azure‑сервисы, зачем они вообще нужны и какие у них есть ближайшие аналоги в российских облаках (Яндекс Облако, VK Cloud, Сбер и др.), чтобы модель можно было мысленно перенести и на локальные платформы.

## 1. Общая логика: опора на модель из ЛР1

Я продолжила пользоваться принципом из 1 задания: не придумывать новых башен и семей, а аккуратно вписывать Azure в уже выработанную в ЛР1 структуру. В ЛР1 все сервисы AWS я разложила по иерархии:

- IT Tower — крупные «башни» (Compute, Storage, Cloud Services, Security и т.п.)  
- Service Family — подсемейства внутри башни (Analytics, Database, Storage&Content Delivery, Developer Tools и т.д.)  
- Service Type — конкретный сервис (Amazon S3, Amazon Redshift и т.д.)  
- Service Sub Type — подтип внутри сервиса (например, классы хранилища, серии инстансов)  
- Service Usage Type — тип потребления (Compute Hours, Data Transfer, API Requests, Storage GB‑Month и т.п.)  

В ЛР2 задача была просмотреть строки Azure‑биллинга (Meter Category, Meter Sub‑Category, Meter Name, Consumed Service и т.д.) и для каждой строки записать те же пять классификационных колонок, придерживаясь принципов ЛР1.

***

## 2. Analysis Services: аналитика в башне Cloud Services

### 2.1. Строки с Microsoft.AnalysisServices, “Tabular”, Standard / Basic / Developer

Azure Analysis Services — это управляемый аналитический движок (OLAP/табличные модели), на котором строят витрины и отчётность поверх данных из разных источников. Пользователь работает уже с моделями, а не с голыми таблицами. В российских облаках близкие по смыслу вещи можно построить на базе **Yandex DataLens + ClickHouse/Greenplum**, в VK Cloud — BI‑решения поверх ClickHouse/Greenplum, а также managed‑инстансы Microsoft Analysis Services в коммерческих дата‑центрах.  

Сначала я отфильтровала строки, где `Consumed Service = Microsoft.AnalysisServices` и `Meter Category / Meter Sub-Category` относятся к Analysis Services Tabular. Там были метрики вроде:

- Meter Sub-Category: `Tabular`  
- Meter Name: `Standard S%`, `Basic B%`, `Developer (Hours)` и т.д.

В ЛР1 все большие аналитические сервисы (Redshift, возможно EMR и прочие) я относила в IT Tower `Cloud Services` и в Service Family `Analytics`, потому что это не голый compute, а готовый аналитический сервис. Ровно так же Analysis Services — это не ВМ с SQL, а готовый OLAP/табличный движок.

Поэтому для всех строк Analysis Services я сделала:

- IT Tower: `Cloud Services`  
  Потому что сервис управляемый, платформенный, сидит поверх инфраструктуры и очень похож по уровню абстракции на Amazon Redshift.  
- Service Family: `Analytics`  
  Сервис предназначен для аналитики, моделей данных и отчётности; логично ставить его в тот же Analytics, где у меня в AWS сидели Redshift и прочие аналитические штуки.  
- Service Type: `Azure Analysis Services`  
  Здесь логика простая: в AWS я в Service Type писала конкретное имя сервиса (Amazon S3, Amazon EC2), поэтому в Azure делаю так же — тут это Azure Analysis Services.

Дальше я смотрела на SKU:

- Basic B%  
- Standard S%  
- Developer (Hours)

В ЛР1, когда у сервиса были разные SKU, я обычно отражала это в Service Sub Type (например, классы хранилища, типы инстансов). Поэтому:

- Service Sub Type:  
  - для Basic: `Basic`  
  - для Standard: `Standard`  
  - для Developer: `Developer`

Таким образом, все эти строки явно показывают, что это один и тот же сервис, но разные тарифы.

Для Service Usage Type я исходила из того, что все эти SKU фактически продаются как «часы работы инстанса» (instance hours):

- Service Usage Type:  
  - Basic: `Basic Instance Hours`  
  - Standard: `Standard Instance Hours`  
  - Developer: `Developer Instance Hours`

То есть Usage Type фиксирует, что платится за время работы конкретного уровня Analysis Services, а Sub Type — какой именно это уровень.

***

## 3. Azure Data Factory: Data Movement, Orchestration, Cloud и On‑Prem

### 3.1. Data Factory v2: Data Movement / Orchestration, Cloud IR / Self‑Hosted

Azure Data Factory — это облачный сервис интеграции данных и ETL‑пайплайнов: он вытаскивает данные из разных источников, преобразует и грузит их в хранилища/витрины. Это по сути «облачный ETL‑конструктор». В российских облаках похожую роль играют **Yandex Data Transfer + Data Proc/Functions**, а также готовые ETL‑сервисы и конструкторы в VK Cloud или локальные решения (Apache Airflow, Matillion, Fivetran и т.п., размещённые в облаке).  

Следующим блоком были Azure Data Factory v2 — строки, где `Meter Category = Azure Data Factory v2` и `Consumed Service = Microsoft.DataFactory`. Там в Meter Name встречались:

- `Data Movement Self Hosted IR`  
- `Orchestration Self Hosted IR`  
- `Data Movement Cloud IR`  
- `Orchestration Cloud IR`  
- `SSIS STD D4 v2`  
- и одна немного «общая» строка типа `%`.

В ЛР1 ETL/аналитическую интеграцию (вроде Glue, Data Pipeline и прочего) я относила к Cloud Services / Analytics, рядом с Redshift, тк это часть аналитического стека, а не, например, compute, storage.

Поэтому для всех строк Data Factory:

- IT Tower: `Cloud Services`  
- Service Family: `Analytics`  
- Service Type: `Azure Data Factory`

Дальше я разделила подтипы по типу рантайма и типу операции:

- Для `Data Movement Self Hosted IR`:  
  - Service Sub Type: `Self-Hosted Integration Runtime`  
  - Service Usage Type: `Data Movement`  
  Потому что смысл этой строки — перенос данных через self‑hosted рантайм.

- Для `Orchestration Self Hosted IR`:  
  - Service Sub Type: `Self-Hosted Integration Runtime`  
  - Service Usage Type: `Orchestration`  
  Здесь тот же самый рантайм, но деньги берутся не за перенос данных, а за сами запуски и управление пайплайнами.

- Для `Data Movement Cloud IR`:  
  - Service Sub Type: `Cloud Integration Runtime`  
  - Service Usage Type: `Data Movement`

- Для `Orchestration Cloud IR`:  
  - Service Sub Type: `Cloud Integration Runtime`  
  - Service Usage Type: `Orchestration`

Так получается ясное разделение: Sub Type — это Self‑Hosted vs Cloud IR, Usage Type — Data Movement vs Orchestration.

Для строки со «смазанным» Meter Name (просто `%`) я сделала более общий вариант:

- Service Sub Type: `Data Factory v2`  
- Service Usage Type: `General Usage`

чтобы не оставлять пустые значения и обозначить, что это категория «прочее использование» Data Factory.

### 3.2. Data Factory в категории Business Analytics: Cloud / On Prem Data Movement

Отдельно были строки в `Meter Category = Business Analytics`, `Meter Sub-Category = Data Factory`, `Meter Name`:

- `Data Movement Cloud`  
- `Data Movement On Premises`

С точки зрения модели это всё тот же Data Factory, просто биллинг вынесен в категорию Business Analytics.

Я сохранила тот же верхний уровень:

- IT Tower: `Cloud Services`  
- Service Family: `Analytics`  
- Service Type: `Azure Data Factory`

А на уровне Sub Type и Usage Type ещё раз зафиксировала, где крутится интеграционный рантайм:

- `Data Movement Cloud`:  
  - Service Sub Type: `Cloud Data Movement`  
  - Service Usage Type: `Data Movement`

- `Data Movement On Premises`:  
  - Service Sub Type: `On-Premises Data Movement`  
  - Service Usage Type: `Data Movement`

Таким образом, можно будет отдельно смотреть cloud и on‑prem движение данных.

---

## 4. Azure Database for PostgreSQL / MySQL: управляемые базы в семействе Database

Azure Database for PostgreSQL / MySQL — это управляемые базы данных с конкретной СУБД (PostgreSQL или MySQL), где провайдер берёт на себя обновления, бэкапы и часть администрирования. По сути это аналог Amazon RDS, только в Azure. В российских облаках аналогами являются **Яндекс Managed Service for PostgreSQL/MySQL**, **VK Cloud Managed Databases**, похожие managed‑БД у других провайдеров.  

Дальше я перешла к строкам с управляемыми базами данных:

- Meter Category: `Azure Database for PostgreSQL`  
- Consumed Service: `Microsoft.DBforPostgreSQL` и `Microsoft.DBforMySQL`

В ЛР1 все управляемые СУБД (Amazon RDS) у меня были в IT Tower `Cloud Services`, Service Family `Database`. Это платформенные сервисы, где администрирование, патчи и часть инфраструктуры скрыты от пользователя. Поэтому:

- IT Tower: `Cloud Services`  
- Service Family: `Database`  
- Service Type:  
  - для MySQL: `Azure Database for MySQL`  
  - для PostgreSQL: `Azure Database for PostgreSQL`

Дальше я смотрела на Meter Sub-Category и Meter Name: там, как правило, фигурируют типы производительности (Basic, General Purpose, vCore) и компоненты (`Compute`, `Storage`, `Backup Storage`). В тех строках, которые были только про compute‑часть, я сделала:

- Service Sub Type: `Compute` (или, если явно указана общая категория, `General Purpose`)  
- Service Usage Type: `vCore Hours` или обобщённо `Database Instance Hours`

Так модели видно, что это именно часы работы инстанса БД.

***

## 5. Azure Redis Cache: кэш как часть Database

Azure Redis Cache — это управляемый кластер Redis в облаке: ключ‑значение хранилище в памяти, которое используют как быстрый кэш для БД и API. Аналоги в российских облаках — **Яндекс Managed Service for Redis**, **VK Cloud Managed Redis** и подобные услуги у других провайдеров.  

Затем я прошла блок Redis Cache:

- Meter Category: `Redis Cache`  
- Meter Sub-Category: `C%`  
- Meter Name: варианты с `C%` / `Cache`  
- Consumed Service: `Microsoft.Cache`

В ЛР1 кэш‑сервисы обычно висели рядом с базами (как in‑memory базы), поэтому логично поместить Redis в `Cloud Services / Database`. Так я и сделала:

- IT Tower: `Cloud Services`  
- Service Family: `Database`  
- Service Type: `Azure Redis Cache`

Meter Sub-Category `C%` — это серия кластера; в AWS я серии EC2 отражала в Service Sub Type (например, M5, C5).

- Service Sub Type: `C-Series`

Там, где были различные варианты `C%`, я всё равно оставила это как `C-Series`, чтобы не создавать лишние подтипы, но можно было бы и уточнить (C1, C2 и т.д.).

Usage Type практически везде означал, что мы платим за время работы кэш‑инстанса:

- Service Usage Type: `Cache Instance Hours`

Отдельные строки, где Meter Name выглядел просто как `Cache` или немного по‑другому, я всё равно считала за часы работы кэша и не вводила новые Usage Type, чтобы не распылять аналитику.

***

## 6. Azure Compute и Azure Batch: башня Compute и серии VM

### 6.1. Azure Batch Reservation

Azure Batch — сервис, который массово запускает вычислительные задачи (batch‑jobs) на пуле виртуальных машин: удобно для рендеринга, расчётов, бэкенд‑обработки. Аналоги в российских облаках — запуск задач на пуле ВМ или в Kubernetes, например через **Yandex Managed Service for Kubernetes + Jobs**, аналогичные решения в VK Cloud.  

Отдельно стояла строка с:

- Meter Category: `Cloud Services`  
- Meter Sub-Category: `Reservation`  
- Meter Name: `%License`  
- Consumed Service: `Microsoft.Batch`

Здесь смысл такой: Azure Batch — это сервис, который запускает задачи, а в этих строках биллинга показана просто его «зарезервированная» часть. В ЛР1 все compute‑ресурсы и связанные лицензии я собирала в башню `Compute`. Поэтому:

- IT Tower: `Compute`  
- Service Family: `Compute`  
- Service Type: `Azure Batch`  
- Service Sub Type: `Reserved Batch` или `Batch Reservation`  
- Service Usage Type: `License` / `Reservation License`

То есть это специфический тип потребления compute‑сервиса: лицензия или резервация.

### 6.2. Cloud Services A/D/F/G/H/N‑series, Compute Hours

Здесь речь про обычные Azure‑виртуалки (разные серии A/D/F/G/H/N) — аналоги EC2‑инстансов. В российских облаках это стандартные вычислительные ВМ: **Яндекс Compute Cloud**, **VK Cloud Compute** и т.п.  

Дальше шёл массив строк:

- Meter Category: `Cloud Services`  
- Meter Sub-Category: `A%`, `D%`, `F%`, `G%`, `H%`, `N%`  
- Meter Name: `Compute Hours`  
- Consumed Service: `Compute`

Это явные аналоги EC2 — вычислительные часы разных серий VM. В ЛР1 были EC2 и похожие вещи:

- IT Tower: `Compute`  
- Service Family: `Compute`  
- Service Type: `Amazon EC2` (или агрегированно Compute, если нужно было укрупнение)

Для Azure я сделала:

- IT Tower: `Compute`  
- Service Family: `Compute`  
- Service Type: `Azure Compute`

А серии вынесла в Service Sub Type:

- A% → `A-Series`  
- D% → `D-Series`  
- F% → `F-Series`  
- G% → `G-Series`  
- H% → `H-Series`  
- N% → `N-Series`

Во всех этих строках Usage Type одинаковый:

- Service Usage Type: `Compute Hours`

Таким образом, можно сравнивать общие compute‑часы между AWS и Azure, не привязываясь к конкретным буквенным обозначениям, но сохраняя их в Sub Type для детализации.

***

## 7. Azure Scheduler: инструмент управления (Management Tools)

Azure Scheduler — это сервис, который по расписанию запускает задачи/HTTP‑запросы. Сейчас его функциональность в Azure частично заменена Logic Apps, но идея та же: «крон» в облаке. Аналоги в российских облаках — запуск по расписанию через **Yandex Functions + Trigger по расписанию**, **VK Cloud Functions / Cron‑задачи** и т.п.  

Следующий блок — `Scheduler`:

- Meter Category: `Scheduler`  
- Meter Sub-Category: `Scheduler`  
- Meter Name:  
  - `Free Scheduler Units`  
  - `Standard Scheduler Units`  
  - `Free Unit`  
  - `Standard Unit`  
- Consumed Service: `Microsoft.Scheduler`

Здесь я вспомнила свою схему ЛР1, в которой я все системные или управляющие сервисы (мониторинг, планировщики, EventBridge, CloudWatch и т.п.) относила в `Cloud Services / Management Tools`.

Поэтому:

- IT Tower: `Cloud Services`  
- Service Family: `Management Tools`  
- Service Type: `Azure Scheduler`

Sub Type логично оставить общим:

- Service Sub Type: `Scheduler`

В Usage Type я разделила бесплатные и стандартные единицы, чтобы сохранить смысл:

- Строки с `Free Scheduler Units` и `Free Unit`:  
  - Service Usage Type: `Free Scheduler Units`

- Строки с `Standard Scheduler Units` и `Standard Unit`:  
  - Service Usage Type: `Standard Scheduler Units`

Таким образом, в аналитике видно, сколько потреблялось платных Scheduler Units, а сколько — бесплатных.

***

## 8. Azure CDN: трафик в башне Storage

Azure CDN — это сеть доставки контента: кэширование статики ближе к пользователям, уменьшение задержек и нагрузки на основное хранилище. Аналоги — **Yandex CDN**, **VK Cloud CDN**, CDN‑сервисы у других российских провайдеров.  

Блок CDN состоял из двух типов строк:

1. Meter Category: `CDN`, Meter Sub-Category: `CDN`, Meter Name: `Standard CDN Data Transfer%`  
2. Meter Category: `Content Delivery Network`, Meter Sub-Category: `Azure CDN%`, Meter Name: `%Data Transfer`

В ЛР1 S3 и CloudFront я относила к `Storage` и в подсемейство `Storage&Content Delivery`, потому что основная идея — это хранение и доставка контента, а не вычисления. Чтобы сравнение AWS/Azure было честным, Azure CDN я точно так же поместила в Storage.

Для обеих строк:

- IT Tower: `Storage`  
- Service Family: `Storage&Content Delivery`  
- Service Type: `Azure CDN`

Дальше:

- Для Standard CDN строки:  
  - Service Sub Type: `Standard CDN`  
  - Service Usage Type: `Data Transfer`

- Для общей Data Transfer строки:  
  - Service Sub Type: `Azure CDN` (общее)  
  - Service Usage Type: `Data Transfer`

То есть везде Usage Type показывает трафик, а Sub Type — конкретный уровень CDN или просто сам факт, что это Azure CDN.

***

## 9. Azure Data Box: физическое устройство для переноса данных

Azure Data Box — это физическое устройство от Microsoft, которое привозят к заказчику, он заливает туда данные, устройство отправляют в дата‑центр Azure и там данные загружаются в облако. Аналогия в мире AWS — Snowball. В российских реалиях похожие услуги бывают у крупных дата‑центров (перенос больших объёмов данных на дисках/кассетах), а в публичных облаках это обычно решают сочетанием «офлайн‑доставки» и ускоренных каналов.  

Была строка, связанная с Data Box:

- Meter Category: `Data Box`  
- Consumed Service: `Microsoft.DataBox`

В AWS‑модели все сервисы переноса/архивного хранения (S3, Glacier, Snowball и т.п.) я хранила в `Storage / Storage&Content Delivery`. Data Box по сути — «коробочка» для переноса больших объёмов данных, то есть расширение стека хранения.

Поэтому:

- IT Tower: `Storage`  
- Service Family: `Storage&Content Delivery`  
- Service Type: `Azure Data Box`  
- Service Sub Type: `Data Box Device`  
- Service Usage Type: `Device Usage` или `Transfer Service`

Так в аналитике видно, что это не место хранения, а сервис физического переноса.

***

## 10. Azure Key Vault: безопасность и управление секретами

Azure Key Vault — это сервис для хранения ключей шифрования, секретов, сертификатов и управления доступом к ним. Его используют, чтобы не хранить пароли/ключи в коде и централизованно управлять шифрованием. Аналоги в российских облаках — **Yandex Lockbox + Managed KMS**, решения по управлению секретами в VK Cloud, а также HashiCorp Vault, развёрнутый в российских дата‑центрах.  

Строки по Key Vault имели:

- Meter Category: `Key Vault`  
- Consumed Service: `Microsoft.KeyVault`

В ЛР1 все сервисы управления идентификацией/секретами (IAM, KMS, Directory Service) я складывала в семейство `Security and Identity` внутри `Cloud Services`. Поэтому:

- IT Tower: `Cloud Services`  
- Service Family: `Security and Identity`  
- Service Type: `Azure Key Vault`

Дальше я смотрела на Meter Name: там обычно отражаются либо операции (Requests, Operations), либо хранение ключей/сертификатов. Чтобы не перегружать модель, я сделала обобщённый вариант:

- Service Sub Type: `Key Vault`  
- Service Usage Type: `Operations`

Если бы были отдельные строки явно про storage, можно было бы добавить второй Usage Type типа `Key Storage`, но в рамках этой выборки достаточно обобщить.

---

## 11. Microsoft Sentinel и Log Analytics: безопасность и аналитика логов

Microsoft Sentinel — облачный SIEM‑сервис: собирает логи, события безопасности, строит корреляции, помогает обнаруживать инциденты. Работает поверх Log Analytics. Российские аналоги — SIEM‑решения вроде **СёрчИнформ SIEM, Positive Technologies MaxPatrol SIEM, Solar JSOC и др.**, которые можно развернуть в российских облаках или дата‑центрах.  

Внизу таблицы были строки с:

- Meter Category: `Sentinel`  
- Meter Name: `Free Trial`, `Analysis`  
- Consumed Service: `microsoft.operationalinsights`

Sentinel — это облачный SIEM‑сервис безопасности, который использует Log Analytics как backend. В ЛР1 всё подобное у меня жило в `Cloud Services / Security and Identity`.

Поэтому для обоих вариантов:

- IT Tower: `Cloud Services`  
- Service Family: `Security and Identity`  
- Service Type: `Microsoft Sentinel`

Дальше, по Meter Name:

- `Free Trial`:  
  - Service Sub Type: `Sentinel Trial`  
  - Service Usage Type: `Free Trial`

- `Analysis`:  
  - Service Sub Type: `Sentinel Analytics`  
  - Service Usage Type: `Analytics Data`

Таким образом, видно, какие расходы относятся к пробному периоду, а какие — к реальному анализу данных.

---

## 12. Итоги

В результате ЛР2 у меня появилось:

- Заполненный файл Azure с теми же колонками, что и AWS‑таблица из ЛР1.  
- Каждая строка Azure‑биллинга получила:  
  - IT Tower (Compute, Storage, Cloud Services и т.п.), совместимые с AWS.  
  - Service Family (Analytics, Database, Storage&Content Delivery, Management Tools, Security and Identity, Compute и др.), которые совпадают с семействами ЛР1.  
  - Service Type — конкретное имя Azure‑сервиса (Azure Analysis Services, Azure Data Factory, Azure Redis Cache, Azure CDN, Azure Scheduler, Azure Batch, Azure Database for PostgreSQL/MySQL, Azure Key Vault, Azure Data Box, Microsoft Sentinel и т.д.).  
  - Service Sub Type — уровни SKU или типы использования (Standard/Basic/Developer, A‑/D‑/F‑/G‑/H‑/N‑Series, Cloud vs On‑Prem, Self‑Hosted vs Cloud IR и т.п.).  
  - Service Usage Type — понятные типы потребления (Compute Hours, Cache Instance Hours, Data Movement, Orchestration, Data Transfer, Instance Hours, Operations, Analytics Data, Free Trial, Scheduler Units и т.д.).

Все решения по Azure принимались через призму ЛР1:

- Аналитика (Analysis Services, Data Factory) ушла в `Cloud Services / Analytics`, как и Redshift.  
- Управляемые базы (PostgreSQL, MySQL) и кэш (Redis) оказались в `Cloud Services / Database`, как и RDS/ElastiCache.  
- Compute‑часть (VM‑серии, Batch) ушла в башню `Compute`, как и EC2.  
- Хранение и доставка (CDN, Data Box) попали в `Storage / Storage&Content Delivery`, как и S3/CloudFront.  
- Сервисы управления и безопасности (Scheduler, Key Vault, Sentinel) попали в `Cloud Services / Management Tools` и `Cloud Services / Security and Identity`, как соответствующие AWS‑аналоги.  

Благодаря этому можно строить кросс‑провайдерные отчёты не по сырому «Meter Category» или «Consumed Service», а по своей унифицированной модели. Например, сравнивать суммарные расходы на `Compute`, `Storage&Content Delivery`, `Analytics`, `Database`, `Security and Identity` сразу по двум вендорам, не задумываясь о том, как именно провайдер назвал тот или иной сервис в биллинге. Одновременно из текста видно, какие российские облачные сервисы примерно соответствуют каждому Azure‑сервису, так что модель легко переносится и в российский контекст.
