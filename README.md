Роботизированная платформа на основе Orange Pi Zero 3. 

### Зависимости:
- python 3.10
- Ubuntu 22.04

Обновление пакетов и системы:
```
sudo apt update && sudo apt upgrade
```
### установка wiringOP:
```
sudo apt install -y git
git clone https://github.com/orangepi-xunlong/wiringOP.git -b next
cd wiringOP
sudo ./build clean
sudo ./build
```

Проверка:
```
sudo gpio readall
```
### установка gpiod
```
sudo apt install gpiod
sudo apt install -y python3-libgpiod
```
Проверка:
```
gpioinfo
```