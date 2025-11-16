# Отчет о выполнении лабораторной работы 1
## _Версия со звездочкой_

Для начала нужно выбрать, какой сайт взламывать. А что может быть лучше, чем напомнить любимой школе о себе? Поэтому я выбрала [сайт школы](https://schc315.mskobr.ru/). Прочитав отчеты других о том, что они нашли уязвимости с первой попытки, мне хотелось повторить их успех, а заодно проверить, насколько хорошо работают информационный ресурсы Москвы ~~на что идут налоги у всей страны~~.

Для начала я скачала ffuf и wordlist с потенциальными адресами панели администратора.  
<img width="1026" height="749" alt="Screenshot from 2025-11-15 16-50-57" src="https://github.com/user-attachments/assets/0ed6cfea-0d0c-459f-822c-f63b89376d7b" />

<img width="1920" height="1160" alt="Screenshot from 2025-11-16 16-44-35" src="https://github.com/user-attachments/assets/4971c03d-3c88-4701-a12d-fea1b30e8b69" />

Далее я запустила перебор страниц и отфильтровала выдачу, чтобы ошибка 403 не показывалась.  

<img width="1105" height="677" alt="Screenshot from 2025-11-15 19-25-30" src="https://github.com/user-attachments/assets/21a78f75-4ed4-4856-9686-92fb1e3aa6e7" />

Как видим, ни один из 5366 адресов никуда нас не привел. Но может получится с адресом скачивания сайта?  

Делаем еще один path-wordlist для адресов, связанных с скачиванием и запускаем ffuf.  

<img width="952" height="799" alt="Screenshot from 2025-11-15 20-31-31" src="https://github.com/user-attachments/assets/2e781786-7d5f-4dfc-9502-803f0e0164b4" />

<img width="1174" height="682" alt="Screenshot from 2025-11-15 20-32-34" src="https://github.com/user-attachments/assets/99bcf54e-abd4-4a19-b567-7e37f170de72" />

И опять ничего. От кого защищают этот сайт? Неужели мамочки настолько сильно хотят отдать ребенка в эту школу, что способны взломать сайт?  

В последствии я нашла на сайте ссылки, ведущие на официальные документы. Ссылка работала с помощью get_file.php, куда передавался id и name файла. Может тут повезет?  

<img width="585" height="48" alt="Screenshot from 2025-11-16 16-32-04" src="https://github.com/user-attachments/assets/463fc379-8fd6-4580-b631-c1d56622ae17" />

<img width="1911" height="364" alt="Screenshot from 2025-11-16 16-32-23" src="https://github.com/user-attachments/assets/56dc34eb-9945-48f4-93b4-94082a1cb39e" />

Опять ошибка! И все дальнейшие действия с этим адресом приводили к ошибке 404 в nginx.  

<img width="1911" height="149" alt="Screenshot from 2025-11-16 16-33-13" src="https://github.com/user-attachments/assets/7d47f8aa-03cb-4daa-9c40-65e4a9d30ce8" />

В итоге я не обнаружила никаких уязвимостей, зато нашла свое фото из 5 класса. Даааа, знала бы эта девочка, чем мне предстоит заниматься через каких-то 7 лет... Но это уже совсем другая история)  

<img width="154" height="181" alt="Screenshot from 2025-11-15 20-40-11" src="https://github.com/user-attachments/assets/703c9b0e-02bf-4249-a938-9d6dab3ecddf" />
