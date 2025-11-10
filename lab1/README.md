# Отчёт о выполнении лабораторной 1  
## *Обычная версия*  

> Выполнено человеком без опыта в веб-программировании. Прошу понять и простить. Возможно, решение не впечатляющее и не самое логичное, но оно **написано** и это самое главное.

# Подготовка (создание пет-проектов)  
Проблемы начались уже на этапе подготовки. У меня нет пет-проектов или сайтов, поэтому надо срочно их создать. Первый сайт сделала простой страничкой с текстом [мирового хита](https://youtu.be/1P-pajVb_NQ?si=RBoeqjPfOqJ8o_lD). Перед этим создала 2 директории для сайтов.

<img width="1920" height="1160" alt="Screenshot from 2025-11-07 14-27-18" src="https://github.com/user-attachments/assets/60aa9096-8351-4aa1-9b59-0681e5ed84cd" />

Потом надо было написать файл с оформлением. Это было похоже на пытку.

<img width="1920" height="1160" alt="Screenshot from 2025-11-07 14-32-16" src="https://github.com/user-attachments/assets/d0ca355a-3a66-40dc-a100-c7ac8cb8bae8" />

<img width="879" height="167" alt="Screenshot from 2025-11-07 14-56-31" src="https://github.com/user-attachments/assets/fd47a8e8-0b17-4027-8327-2f7c7312674d" />

<img width="1918" height="1109" alt="Screenshot from 2025-11-07 14-54-39" src="https://github.com/user-attachments/assets/3083e894-98b8-4816-8b08-94792a50f3ee" />

Чтобы сайт работал и не выглядел как покинутое богом место, я несколько раз переписывала файл оформления и сократила текст. И это помогло! Теперь приступаем к написанию второго пет-проекта. Я решила дополнить код из [примера](https://dev.to/maxcore/basic-ultimate-guide-nginx-1ngd) в задании лабораторной работы. Сделала страницу, на которой показывается информация о запросе, то есть некий self-doxxing.

<img width="1064" height="1110" alt="Screenshot from 2025-11-07 16-41-36" src="https://github.com/user-attachments/assets/8e55f79c-e5c0-4fc5-a12b-3f139581f02a" />

Потом были проблемы с созданием виртуального окружения и устанковкой starlette...

<img width="952" height="464" alt="Screenshot from 2025-11-07 15-34-56" src="https://github.com/user-attachments/assets/b66de4e2-fbc1-4482-9694-ed067de30534" />

<img width="1859" height="1056" alt="Screenshot from 2025-11-07 15-42-17" src="https://github.com/user-attachments/assets/8c2fdd99-7bcd-4a53-bfb1-03cf714a3f34" />

<img width="1233" height="1104" alt="Screenshot from 2025-11-07 15-42-41" src="https://github.com/user-attachments/assets/395152d6-ae7d-4e31-a6f2-5181b9e0ee70" />

Они решились установкой всех пакетов, все необходимые файлы создались, осталось разхобраться с стилем страницы.

<img width="698" height="168" alt="Screenshot from 2025-11-07 16-42-33" src="https://github.com/user-attachments/assets/c7f4f325-599e-4e45-ac3b-dff7c29e7328" />

<img width="969" height="651" alt="Screenshot from 2025-11-07 16-42-13" src="https://github.com/user-attachments/assets/50ec3069-78b9-4d0a-9065-908e246e2747" />

Теперь последние шаги, чтобы site2 работал фоново под управлением systemd.

<img width="977" height="512" alt="Screenshot from 2025-11-09 14-57-08" src="https://github.com/user-attachments/assets/f3142eec-0870-4121-abe5-e26869ff9605" />

<img width="977" height="461" alt="Screenshot from 2025-11-09 14-58-47" src="https://github.com/user-attachments/assets/784a4a82-d597-4106-ad5e-5a5a00736666" />

*С замиранием сердца* проверяем, работает ли сайт

<img width="963" height="643" alt="Screenshot from 2025-11-07 16-49-17" src="https://github.com/user-attachments/assets/9aad97aa-8c34-4420-8f83-f0fb56144005" />

**ЭТО ЧТО?** Я не знаю, ~~мне страшно,~~ надо выйти отсюда. Как-то случайно я попала в настройку почты... Ладно, это не важно.

Проверяем сайт!

<img width="1920" height="1112" alt="Screenshot from 2025-11-07 16-56-58" src="https://github.com/user-attachments/assets/0372fba5-17c6-4caf-8fdd-8a48e351b0ba" />

Это реально круто. Мой первый опыт создания веб-страниц, дальше — больше!

# Основная часть работы
Наконец переходим к настройке Nginx. Проблем с установкой не возникло, потому что я работаю на линуксе.

Начнем с создания самоподписных сертификатов.

<img width="908" height="761" alt="Screenshot from 2025-11-09 15-03-32" src="https://github.com/user-attachments/assets/b8a56cec-55ac-42d0-a6c4-45fc0ab2969a" />

Теперь запускаем Nginx и проверяем, что он корректно работает после запуска (или хотя бы запускается, что уже приятно).

<img width="969" height="706" alt="Screenshot from 2025-11-09 15-07-08" src="https://github.com/user-attachments/assets/a3a85240-ba33-487d-abb0-010568ea3593" />

Пришло время создать отдельные директории для каждого из сайтов и написать в них конфигурационный файлы.

<img width="969" height="650" alt="Screenshot from 2025-11-09 15-08-10" src="https://github.com/user-attachments/assets/e357d5c1-2cf7-4599-aad3-afae3c5d0663" />
<img width="969" height="187" alt="Screenshot from 2025-11-09 15-08-44" src="https://github.com/user-attachments/assets/06f6fdd6-67e2-4d58-9935-21f8f58508ed" />

Видим вывод  
```
syntax is ok
test is successful  
```
радуемся, добавляем в `/etc/hosts` адреса для двух сайтов.

<img width="969" height="332" alt="Screenshot from 2025-11-09 15-10-55" src="https://github.com/user-attachments/assets/e6d14711-fad0-4f02-8ba0-097a373bfd10" />

<img width="1920" height="1113" alt="Screenshot from 2025-11-09 15-11-40" src="https://github.com/user-attachments/assets/48643d7f-13d5-4e66-88ef-384a59406bc3" />

Смотрим, что получиось.

<img width="1920" height="1113" alt="Screenshot from 2025-11-09 15-11-40" src="https://github.com/user-attachments/assets/0ffa7c6f-20d5-4a65-9b7f-034f114fddab" />

А получилось как раз то, что надо. Сайт работает на адресе site1.local. Теперь все эти действия выполняем для site2 и проверяем, что получилось.

<img width="1911" height="720" alt="Screenshot from 2025-11-09 15-24-37" src="https://github.com/user-attachments/assets/43ecd54e-03c8-4f48-887d-2350ed798ea6" />
<img width="1911" height="720" alt="Screenshot from 2025-11-09 15-24-46" src="https://github.com/user-attachments/assets/249dabde-c804-4c9a-8c1f-af85000772ae" />

Еще для корректной работы я создала файл .service, в котором описываются правила запуска сервера (в автоматическом режиме при запуске системы, слушает порт 8001, работает под www-data).

<img width="743" height="441" alt="Screenshot from 2025-11-09 15-23-53" src="https://github.com/user-attachments/assets/5dc44bcd-e64c-4e2e-bc0c-fce024af261d" />

А теперь начинается самое ~~страшное~~ интересное — неожиданные ошибки! Site1 переста1т работать так, как должен. Честно, я не знаю, какое из миллиона действий привело к этому результату, но скорее всего я случайно изменила location в конфигурационном файле (то есть путь к html-файлу моего сайта), и из-за этого вылезала ошибка 403. То есть Nginx просто не видел, какие файлы ему использовать.

<img width="1911" height="518" alt="Screenshot from 2025-11-09 17-38-20" src="https://github.com/user-attachments/assets/8df9370a-af41-4212-8356-dd5fcf492e7e" />

Спустя где-то полчаса бездумной замены сертификатов (я думала, что ошибка в них), тайна всё-таки стала явной. Следим за руками.

<img width="1026" height="749" alt="Screenshot from 2025-11-09 18-08-24" src="https://github.com/user-attachments/assets/4227920c-3e87-4e9b-b343-9b212d4faf5b" />

Закомментированная часть — старый код. А теперь смотрим содержание директории site1:

<img width="412" height="85" alt="Screenshot from 2025-11-09 18-07-13" src="https://github.com/user-attachments/assets/7f20b0b3-cdf8-46d9-8600-fa1d244a117b" />

Забавно! Но нашли ошибку, исправили.

<img width="357" height="72" alt="Screenshot from 2025-11-09 18-10-38" src="https://github.com/user-attachments/assets/04eddbfc-ec89-4881-82e9-7b3e54e14d38" />

Проверяем результат упорной работы.

<img width="1920" height="771" alt="Screenshot from 2025-11-09 18-11-15" src="https://github.com/user-attachments/assets/9838d1e4-32b7-4344-8f98-c48691c006bd" />

Ура! Мораль: *ошибка обычно вообще не там, где её ищешь.*
