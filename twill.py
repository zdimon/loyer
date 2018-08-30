# ставим юзер агент как у нашего любимого браузера
agent "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
# идем на сайт
go "https://auth.zakon.kz/"
# форма авторизации имеет номер 1. по нему и будем обращаться (чтобы это узнать есть команда showforms)
# теперь заполним ее
# спрашиваем логин и пароль
#getinput "login: "
# вставляем логин введенный с клавиатуры
formvalue 1 Login 0595586181
# спрашиваем пароль
#getpassword "password: "
formvalue 1 Password 5634290166
# ставим галочку "запомнить"
#formvalue 1 remember_me 1
# сабмитим форму (жмем кнопку "вход")
# тут передается не номер формы, а имя кнопки
submit _submit
# сохраняем куки в файл
save_cookies jj_cookies.txt
#Запускаем скрипт так:
#twill-sh jj_login.twill
