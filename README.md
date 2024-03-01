#  Игра на Pygame "Dungeon Runner"  #

##  О проекте  ##
Игра в жанре RPG на сделанная на питоне с использованием библиотеки Pygame. Данные хранятся в базе данных sqlite3. Уровни сделаны в программе Tiled.
("Kingdom of Elfrieden is the largest in the world.", 2000),
            ("All energy people use is extracting from magical crystals.", 2000),
            ("A lot of magical crystals quarried in the dungeon Aincrad.", 2000),
            ("One day a lot of miners didn't came back from the dungeon.", 2000),
            ("The survivors said, that they was murdered by monsters.", 2000),
            ("No one knew where these creatures came from", 2000),
            ("and none were prepared for there attack.", 2000),
            ("The King is sending you as the strongest warrior to the dungeon.", 2000),
            ("You must kill all monsters!", 2000),
## Предистория ##
Королевство Ельфриден самое большое в мире людей.
Магическая энергия, которая используется людьми добывается в подземелье Аинкард.
Однажды много шахтёров не вернулись из шахты.
Те, кто сумел вернуться утверждали, что их убили монстры.
Никто не знал, откуда появились эти монстры, и никто не был готов к их атаке.
Король посылает вас, как самого сильного война, чтобы вы очистили подземелье от этих чудовищ.
Вы должны убить всех монстров!

##  Как запустить  ##
Для запуска необходимо скачать файлы проекта и в зависимости от операционной системы
запустить "Dungeon Runner for Windows.exe" если у вас Windows
и "Dungeon Runner for Linux.exe" если у вас Unix-подобная операционная система.

##  Функционал  ##
###  Главное меню  ###
Play - играть  
Settings - настройки  
Quit - выход

###  Запуск игры  ###
Три поля для игры, если игра начата, то в этом поле будет continue, если нет new game.  
При начале новой игры будет показан опенинг, который пропускается клавишей `[esc]`. Если продолжить игру, то загрузится уровень, на которым вы сохранились.  
По нажатию на кнопки back или клавиши `[esc]` можно вернуться на главное меню.  

###  Игра  ###
Игра состоит из пяти уровней, на последнем босс. Игрок может атаковать мечом или магией, если у него есть достаточно маны, чтобы применить заклинание.  
Для прохождения уровня необходимо убить всех монстров и подойти ко входу на следующий уровень. 
Управление:  
• `[w][a][s][d] или [↑][←][↓][→]` - Движение игрока.  
• `[ПРОБЕЛ]` - атака мечом.  
• `[1]` - Божественное благословение.  
• `[2]` - Каменная стена.  
• `[3]` - Ледяные оковы.  
• `[4]` - Огненный взрыв.  
• `[5]` - Разряд молнии.  
• `[6]` - Дух тьмы.  
• `[esc]` - пауза.

Магия применится на месте вашего курсора.

###  Статистика  ###
После прохождения последнего уровня будет показана статистика.  
* Kills - убито монстров  
* Deaths - сколько раз ты умер во время прохождения игры  

##  Технологии  ##
Технологии, которые были использованы при создании приложения:  
• Pygame  
• SQLite  
• Tiled  
• Работа с простыми таблицами (csv)


## Ссылки на ресурсы ##
* [Тайлы для уровней](https://szadiart.itch.io/rpg-worlds-ca)
* [Главный персонаж](https://merchant-shade.itch.io/16x16-puny-characters)
* [Слайм](https://elthen.itch.io/2d-pixel-art-small-slime-sprites)
* [Кобра](https://elthen.itch.io/2d-pixel-art-cobra-sprites)
* [Каменный голем](https://elthen.itch.io/2d-pixel-art-mini-golem-sprites)
* [Минотавр](https://elthen.itch.io/2d-pixel-art-minotaur-sprites)
* [Эффект лечения](https://pimen.itch.io/holy-spell-effect)
* [Каменная стена](https://pimen.itch.io/earth-spell-effect-2)
* [Ледяные оковы](https://pimen.itch.io/ice-spell-effect-01)
* [Огненный взрыв](https://pimen.itch.io/fire-spell-effect-02)
* [Разряд молнии](https://pimen.itch.io/thunder-spell-effect-02)
* [Дух тьмы](https://pimen.itch.io/dark-spell-effect)
