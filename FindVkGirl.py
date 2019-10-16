import vk_api, time
import time, codecs
import os, sys, shutil, requests
import os.path

timestamp = int(time.time())

# Заходим ВКонтакте под своим логином (с выключенной в настройках двухфакторной авторизацией)
# В строку vk_session = vk_api.VkApi('', '') в кавычках нужно поставить ваш логи и пароль ВК
vk_session = vk_api.VkApi('', '')
vk_session.auth()
vk = vk_session.get_api()

# Пишем возраст от и до людей которых надо спарсить
vozrast=20
vozrastmax=21

# Номер города (посмотрите его в поиске ВК в адресной строке при выборе в поиске города)
citynumber=123

# 1 - девушки, 2 - парни
psex=1

# Открываем файл для записи результатов
ff=codecs.open('girls.html', 'w', encoding='utf8')

# Перебор возрастов
while(vozrast<=vozrastmax):
    mesac=1
    # Перебор месяцев рождения
    while(mesac<=12):
        # Пауза для API
        time.sleep(4)
        # Пишем какую группу людей качаем
        print('Возраст: '+str(vozrast)+', месяц рождения: '+str(mesac))
        # Получаем 1000 юзеров - их ID, фото, время последнего визита, семейное положение
        z=vk.users.search(count=1000, fields='id, photo_max_orig, has_photo, last_seen, relation', city=citynumber, sex=psex, age_from=vozrast, age_to=vozrast, birth_month=mesac)
        mesac=mesac+1
        for x in z['items']:
            # Если указано семейное положение
            if('relation' in x):
                # Если у юзера есть фото а семейное положение = 1 (Не замужем) также можно поставить 6 (В активном поиске)
                if((x['has_photo']==1) and (x['relation']==1)):
                    # Если отображается дата последнего визита
                    if('last_seen' in x):
                        xxx=timestamp-int(x['last_seen']['time'])
                        # Если время со дня последнего визита в ВК не более месяца
                        if(xxx<2592000):
                            # Записываем в файл girls.html строчку
                            s='<a href="https://vk.com/id'+str(x['id'])+'" target="_blank" style="width: 302px; height: 302px;display: inline-block;"><div style="display: inline-block; background: url('+str(x['photo_max_orig'])+'); width: 300px; height: 300px; background-size: cover; background-position: center center;"></div></a>'+'\n'
                            ff.write(s)
                            print('https://vk.com/id'+str(x['id']))
    vozrast=vozrast+1

ff.close()
print('Готово!')


