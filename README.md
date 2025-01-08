# Outline Delay Fix (for windows)

### En

When using the Outline VPN client in Windows, you may experience a problem: a 5-40 second delay before opening pages and executing requests. However, the Internet speed measured by http://speedtest.net is normal and after the delay is over, the page loads quickly.

This may be related to the InterfaceMetric value of outline interface on Windows. This bat script will check whether the interface is configured correctly. And if it finds a problem, it will fix it.

Related issue: https://github.com/Jigsaw-Code/outline-apps/issues/1235

---

### Ru

При использовании VPN клиента Outline в windows может наблюдаться проблема: задержка 5-40 секунд перед открытием страниц и выполнением запросов. При этом скорость интернета по замеру http://speedtest.net в норме, а после задержки страница загружается быстро.

Это может быть связано со значением InterfaceMetric вашего интерфейса outline. Данный bat-скрипт проверит, корректно ли настроен интерфейс. И если обнаружит проблему - исправит ее.

Обсуждение этой проблемы: https://github.com/Jigsaw-Code/outline-apps/issues/1235

## Usage

### Build run (recommended)

1. #### Go to [Releases](https://github.com/lowfc/outline-delay-fix/releases);
2. #### Download the latest release and unzip it to a folder convenient for you;
3. #### Go to the app folder;
4. #### Right-click on the outline-delay-fix.exe and select "Run as administrator";
5. #### Follow the instructions.

### Run with python

Use python 3.10 or newer

1. #### Download the project via the github web, or using 'git clone`;
2. #### Go to the root directory of the project and open the terminal **_ as an administrator_**;
3. #### Create venv:
```shell
python3 -m venv venv
```
4. #### Activate venv:
```shell
.\venv\Scripts\activate
```
5. #### Install dependencies:
```shell
pip install -r requirements.txt
```
6. #### Run and follow the instructions:
```shell
python main.py
```

## Использование

### Запуск сборки (рекомендуется)

1. #### Перейдите на [страницу релизов](https://github.com/lowfc/outline-delay-fix/releases);
2. #### Скачайте последний релиз и распакуйте в удобную для вас папку;
3. #### Перейдите в папку с приложением;
4. #### Нажмите правой кнопкой мыши по файлу outline-delay-fix.exe и выберите "Запуск от имени администратора";
5. #### Следуйте инструкциям.

### Запуск с помощью python

Используйте python версии 3.10 или выше

1. #### Скачайте проект через веб интерфейс github, или с помощью `git clone`;
2. #### Перейдите в корневую директорию проекта и откройте терминал **_от имени администратора_**;
3. #### Создайте venv:
```shell
python3 -m venv venv
```
4. #### Активируйте venv:
```shell
.\venv\Scripts\activate
```
5. #### Установите зависимости:
```shell
pip install -r requirements.txt
```
6. #### Запустите и следуйте инструкциям:
```shell
python main.py
```

