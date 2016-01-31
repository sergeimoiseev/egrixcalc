Сервер создаю и настраиваю с помощью инструкций отсюда:
https://www.phusionpassenger.com/library/walkthroughs/deploy/python/aws/standalone/oss/trusty/deploy_app.html#login-to-your-server-create-a-user-for-the-app

На виртуальной машине пользователь, под которым будет работать программа создан командой
sudo adduser egrixcalc
пароль пользователя - 32167

установка SSH key

sudo mkdir -p ~egrixcalc/.ssh
sudo sh -c "cat $HOME/.ssh/authorized_keys >> ~egrixcalc/.ssh/authorized_keys"
sudo chown -R egrixcalc: ~egrixcalc/.ssh
sudo chmod 700 ~egrixcalc/.ssh
sudo sh -c "chmod 600 ~egrixcalc/.ssh/*"

установка git-а
sudo apt-get install -y git

создаем директорию для кода

sudo mkdir -p /var/www/egrixcalcapp
sudo chown egrixcalc: /var/www/egrixcalcapp

Вот так брать код с git-а:
cd /var/www/egrixcalcapp
sudo -u egrixcalc -H git clone git://github.com/username/myapp.git code

приложение-пример взял так:
cd /var/www/egrixcalcapp
sudo -u egrixcalc -H git clone --branch=end_result https://github.com/phusion/passenger-python-flask-demo.git code

Your app's code now lives on the server at /var/www/myapp/code

Install app dependencies
sudo pip install flask
(пришлось сначала поствить pip через apt-get)


Create a Passenger config file

cd /var/www/myapp/code
sudo nano Passengerfile.json

{
  // Tell Passenger that this is a Python app.
  // Replace "passenger_wsgi.py" with your app's WSGI entry point file.
  "app_type": "wsgi",
  "startup_file": "passenger_wsgi.py",
  // Run the app in a production environment. The default value is "development".
  "environment": "production",
  // Run Passenger on port 80, the standard HTTP port.
  "port": 80,
  // Tell Passenger to daemonize into the background.
  "daemonize": true,
  // Tell Passenger to run the app as the given user. Only has effect
  // if Passenger was started with root privileges.
  "user": "egrixcalc"
}

Finally, fix the permissions on the file:
sudo chown egrixcalc: Passengerfile.json

Start Passenger Standalone
cd /var/www/myapp/code
sudo passenger start


По адресу 
http://54.213.157.107/

теперь видна страничка, сгенерированная моим сервером
----
Deploying application updates
with Passenger in Standalone mode
(ssh -i your_ec2_key.pem egrixcalc@54.213.157.107)

мне придется каждый раз входить через java-приложение в firefox
и менять пользователя

 Prepare application

2.1 Install app dependencies
3 Restart application

Passenger may still be serving an old instance of your application. Now that all application updates have been prepared, tell Passenger to restart your application so that the updates take effect.

passenger-config restart-app $(pwd)

создаю свой главный репозиторий (рабочий репозиторий буду push-ать в него, а из него уже в git
а из git-а - на сервер)

Sergei@embedder-pc MINGW64 ~/Dropbox/Work/EgrixCalc
$ cd egrixcalc.git/

Sergei@embedder-pc MINGW64 ~/Dropbox/Work/EgrixCalc/egrixcalc.git
$ git --bare init
Initialized empty Git repository in C:/Users/Sergei/Dropbox/Work/EgrixCalc/egrixcalc.git/

дальше добавляю в репозиторий файлы и использую GitGUI для работы с кодом

на гитхабе сделал репозиторий-обменник
https://github.com/sergeimoiseev/egrixcalc.git

на сервер в папке www code
создаю репозиторий, чтобы проще было использовать / передавать скрипты и т.д.

egrixcalc@ip-172-31-25-197:/var/www/egrixcalcapp/code$ git --bare init                                                          
Initialized empty Git repository in /var/www/egrixcalcapp/code/

добавляю новый ремоут - egrixcalc_github:
git remote add egrixcalc_github https://github.com/sergeimoiseev/egrixcalc.git

удалю все из папки egrixcalcapp
cd /var/www/egrixcalcapp
sudo -u egrixcalc -H git clone git://github.com/sergeimoiseev/egrixcalc.git

все заново
на github создал пустой репозиторий

в c:\Users\Sergei\Projects\egrixcalc\
скопировал пример архивом отсюда https://github.com/phusion/passenger-python-flask-demo
распаковал в c:\Users\Sergei\Projects\egrixcalc\
- там сделал репозиторий, изменения скоммитил, отправил https://github.com/sergeimoiseev/egrixcalc.git
-успешно

выполнил 
sudo -u egrixcalc -H git clone git://github.com/sergeimoiseev/egrixcalc.git
теперь все в папке
/var/www/egrixcalcapp/egrixcalc/egrixcalc$ ls
app.py  LICENSE.md  README.md  templates
/var/www/egrixcalcapp/egrixcalc/egrixcalc$ ls -a        
.  ..  app.py  .git  .gitignore  LICENSE.md  README.md  templates

----
при каждом обновлении нужно 
1. удалить весь код
ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp$ sudo rm -rf egrixcalc/
2. склонировать новый код с гитхаба
ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp/egrixcalc$ sudo -u egrixcalc -H git clone git://github.com/sergeimoiseev/egrixcalc.git

получаем:
ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp/egrixcalc$ ls -a
.  ..  app.py  .git  .gitignore  LICENSE.md  passenger_wsgi.py  README.md  templates
 - все как должно быть

запускаем:
cd /var/www/egrixcalcapp/egrixcalc
sudo passenger start
-
ошибка
ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp/egrixcalc$ sudo passenger start
=============== Phusion Passenger Standalone web server started ===============
PID file: /var/www/egrixcalcapp/egrixcalc/passenger.3000.pid
Log file: /var/www/egrixcalcapp/egrixcalc/passenger.3000.log
Environment: development
Accessible via: http://0.0.0.0:3000/

You can stop Phusion Passenger Standalone by pressing Ctrl-C.
Problems? Check https://www.phusionpassenger.com/library/admin/standalone/troubleshooting/
===============================================================================
App 5130 stderr: stdin: is not a tty
App 5130 stdout: 


и на странице http://54.213.157.107/ ничего не обновляется
(вероятно, названия папок не те)
файла Passengerfile.json просто нет


-----
все удалил, заново взял с гитхаба - уже с файлом Passengerfile.json
поменял права 
sudo chown egrixcalc: Passengerfile.json
и в папке с кодом запустил
sudo passenger start

- работает - страничка видна
------------------
-правки в коде--
редактирую локальный репозиторий
изменения пушнул в гитхабовский репозиторий
с сервера получаю изменения командой
sudo git fetch origin
sudo git reset --hard origin/master

(ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp/egrixcalc$ sudo git reset --hard origin/master                                                                    
HEAD is now at 8641d6a editing html to test server code updating procedure)
-получилось вроде бы

перезапускаю веб-приложение командой

sudo passenger-config restart-app $(pwd)

(ubuntu@ip-172-31-25-197:/var/www/egrixcalcapp/egrixcalc$ sudo passenger-config restart-app $(pwd)
Restarting /var/www/egrixcalcapp/egrixcalc/public (production))
 - получилось - веб-страничка обновляется


03.01.2016
создал локальный репозиторий взяв с гита текущий
 командой
git clone --branch=master https://github.com/sergeimoiseev/egrixcalc.git code

файлы теперь в папке c:\Users\Sergei\Projects\EgrixCalc\code\

настраиваю быстрый слив на Гитхаб

просто установил AutoHotkey и настроил "lll" на логин
а "ppp" на подстановку пароля к гитхабу - работает

по туториалу flask отредактировал app.py (старый - в app_old.py)
и еще несколько файлов - получился примитивный блог с одним пользователем.
отредактировал C:\Users\Sergei\Projects\egrixcalc\passenger_wsgi.py
работает и локально с flask и на амазоновском сервере 
(и там локально без passenger, и там на внешнем IP c passanger)

эту папку копирую в dropbox - как выжный этап.