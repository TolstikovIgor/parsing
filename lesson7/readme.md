## Урок 7. Selenium в Python
#### Домашнее задание
Написать программу, которая собирает посты из группы https://vk.com/tokyofashion

Будьте внимательны к сайту!

Делайте задержки, не делайте частых запросов!

1) В программе должен быть ввод, который передается в поисковую строку по постам группы
2) Соберите данные постов:
    - Дата поста
    - Текст поста
    - Ссылка на пост(полная)
    - Ссылки на изображения(если они есть)
    - Количество лайков, "поделиться" и просмотров поста
3) Сохраните собранные данные в MongoDB
4) Скролльте страницу, чтобы получить больше постов(хотя бы 2-3 раза)
5) (Дополнительно, необязательно) Придумайте как можно скроллить "до конца" до тех пор пока посты не перестанут добавляться

Чем пользоваться?

Selenium, можно пользоваться lxml, BeautifulSoup

Советы

Пример изменения Selenium через Options - https://geekbrains.ru/lessons/113978?tab=homeworks#!#comment-719568

Посмотрите комментарий по задаче - https://geekbrains.ru/lessons/113978#!#comment-718362
