# Техническое решение проекта «OUR Paint»

## Введение
- **Цель проекта:**  
  реализовать прототип распределённой системы для хранения и редактирования изображений.

- **Основания для разработки:**  
  учебный проект в рамках курса «Основы распределённых вычислений».

- **Команда:**  
  Валентина Богдановна, Каширский Дмитрий, Кривонос Екатерина - IT разнорабочие.


## Глоссарий
| Термин        | Определение |
|---------------|-------------|
| Графический интерфейс | Программное обеспечение, предоставляющие пользователю возможность просматривать и изменять изображение. |
| Изображение | Компьютерный файл, хранящий в себе информацию о какой-либо картинке (размер, ширина, длина) и о пикселях, из которых она состоит (цвет, расположение на картинке). |
| Карандаш | Программный инструмент для редактирования изображения, который позволяет добавлять информацию на изображение в виде пикселей. |
| Ластик | Программный инструмент для редактирования изображения, который позволяет убирать информацию на изображении в виде удаления пикселей. |
| Пользователь | Зарегистрированный клиент системы, получивший доступ к просмотру и редактированию изображений. |
| Программный инструмент | Инструмент, с помощью которых пользователи могут редактировать изображение. |
| Просмотр изображения | Возможность открыть файл и увидеть все изменения, произведённые над файлом. |
| Путь к файлу | Доступ к файлу по ссылке. При нажатии по ссылке, пользователю даётся доступ к просмотру, редактированию и сохранению изображения. |
| Редактирование изображения | Изменение информации, хранящейся в изображении. |


## Функциональные требования
Система должна предоставлять следующие функции:

* Просмотр изображений
* Редактирование изображений несколькими пользователями последовательно
  * Инструменты для редактирования изображения:
     * Карандаш
     * Ластик
* Сохранение изображений

Ограничения на предметную область:
1. Графический интерфейс поддерживает одновременное редактирование изображения не более чем 4 пользователями одновременно.
2. Возможно просматривать или изменять изображения размером до 2048 x 2048 пикселей.
3. Сохранить изображение можно будет только в формате PNG или JPG.


## Нефункциональные требования
* Доступность: 80% 
* Время отклика <= 100 мс
* Отказоустойчивость: Система остаётся работоспособной, если по какой-либо причине отключается один из пользователей, участвующих в процессе редактирования изображения. Если отключается сервер, который хранит редактируемое в данный момент изображение, то изображение не утрачивается полностью - любой пользователь, участвовавший в редактировании и не отключившийся от программы, может сохранить последние полученные от сервера данные.
* Консистентность: Изменения, которые внёс один из пользователей во время редактирования изображения также отобразятся у других пользователей, участвующих в процессе редактирования изображения.


## Пользовательские сценарии

* I. Просмотр изображения:
  + 1. В графическом интерфейсе пользователь выбирает нужный файл с изображением и нажимает на поле "открыть".
  + 2. Пользовательский интерфейс отправляет запрос на сервер для получения изображения.
  + 3. Сервер отправляет информацию об изображении пользователю.
  + 4. В графическом изображении у пользователя открывается поле/окошко, в котором он может видеть изображение.

* II. Прекратить просмотр изображения:
    + 1. Пользователь нажимает на крестик в углу графического интерфейса. 
    + 2. Изображение закрывается, и пользователь возвращается в предыдущее окошко графического интерфейса.

* III. Редактирования изображения:
    + 1. В графическом интерфейсе пользователь выбирает нужный файл с изображением и нажимает на поле "редактировать". 
    + 2. Пользовательский интерфейс отправляет запрос на сервер для получения изображения.
    + 3. Сервер отправляет информацию об изображении пользователю.
    + 4. У пользователя открывается соответствующий программный интерфейс. В интерфейсе расположено само изображение и вкладка с инструментами.
    + 5. В соответствующей вкладке пользователь выбирает один из инструментов: карандаш или ластик.
    + 6. Далее пользователь переходит во вкладку с изображением и выбирает инструмент. Зажав ЛКМ, пользователь проводит курсором по изображению. 
    + 7. Графический интерфейс отправляет на сервер информацию о выбранном инструменте и о пикселях, по которым пользователь провёл курсором.
    + 8. Сервер обрабатывает полученную информацию и, в зависимости от выбранного инструмента, обрабатывает информацию об изменениях, которым подвергнется изображение.
    + 9. Сервер обратно отправляет информацию пользователю.
    + 10. На экране у пользователя отображается обновлённое изображение.

* IV. Сохранение изображения
   + 1. В графическом интерфейсе пользователь выбирает вкладку "Сохранить изображение" и выбирает один из предложенных форматов (PNG/JPG). Также в другом окне пользователь указывает путь, по которому на устройстве будет сохранен файл с изображением.
    + 2. Сервер собирает информацию об изначальном виде изображения и о внесённых в него изменениях.
    + 3. При помощи определённого алгоритма сервер обрабатывает и преобразует полученную информацию в файл формата PNG или JPG, затем отправляет его обратно пользователю.
    + 4. Устройство пользователя принимает файл и сохраняет его по указанному ранее пути.

##  Архитектура системы

* API Gateway - входная точка в систему, отвечает за маршрутиризацию криентских запросов.
* Server Manager - отвечает за наблюдение за состоянием серверов и распределение пользователей по ним. 
* Processing Server - Отвечает за обработку изменений в изображениях.
* Change Information Handler - Обрабатывает и распределяет информацию об изменениях, внесённых в изображение в процессе редактирования.
* Log Broker - брокер логов, обеспечивающий ассинхронную передачу данных о действиях, произошедших на сервирах, в Logs DB
* Logs DB - База данных, хранящая логи том, что происходило на серверах во время сессий.

**Диаграмма компонентов:**
<https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Rasp.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20%E2%80%94%201%22%20id%3D%22AjQ_Fv6i8eFsjXY3NpaH%22%3E7Vxbc6o6FP41PnYPhIvyWC%2B9zLRz3NueOdvHKKlmNoIDWHX%2F%2BpNAgkCwUgsSZugDJYsQzLdWvqy1Euhpo83h0Yfb9atnI6cHFPvQ08Y9AIBimuQflRxjiUr%2BYsnKxzaTnQQz%2FBcxocKkO2yjIFMx9DwnxNuscOm5LlqGGRn0fW%2BfrfbuOdmnbuEKCYLZEjpMCk7S%2F7AdrmPpAPRP8ieEV2v%2BZNW04isbyCuzngRraHv7lEib9LSR73lhfLY5jJBD0eO4xPc9nLma%2FFwfuWGZG3bD%2FevzwsHrhXI3f3DmP63N6x1r5QM6O9Zh9mPDI0fA93aujWgjSk8b7tc4RLMtXNKre6J0IluHG4eUVHIq%2Fij%2BBOSH6JASsR%2F5iLwNCv0jqcKuDhhezGKS8v4EP1CYbJ2CXudCyFS%2BSpo%2BoUJOGDBfAAmIIBEsrHt6HA6j4yA6GtFx3CNQDEB0VCNJXHPC6hA90ZOHqIKSun2YqmZmG0w9Iq8fAmuYVQJ08Mol50uiBOQTAQUfE5u%2BZxc22Lbp7YXazOq7BoVaJRWq1aVPXdDnvwHBKQ%2FsBVOHwTYmnHd8oHBVAZWqZ7HSNBGrQQFUg7qgMloDla43DJXZGqgMo2GoBvLNOsnsccyVL7GUataFkiWg9AhDtIfH9k0BArpq03OAKno%2B99NnIjiHcQPjVjclozi1wBPK44Rc%2B5763dT4HBgEeEnACELoh6I4hV%2FW5NABh7%2FZFXo%2Bp%2FIfBiuND6lq4yMvuKSLv9OF%2BC5g8PLpvqjEbzyrqcDb%2BUt02ZEgnVuhsISxITsTbIiKTynWKFAsl%2FnIgSH%2ByAYuRdpmT5h6mHQtsau%2BlZsPrJzBxB1nd6VDilxDg%2FzEoucaipERGoqML%2Bn2N%2BxRnHN%2FTWZvpK2nt7epaJoE%2Fhe4ICHqlVzpowD%2FhYuoPWo5W9qxqKvGsGeMC23p84GU54IkkGVP6aVjxSKOUH4oCg9GmRZ4UHetlfAq3vt7gOrRm9ZCHqmPRoyORpqlETHKaQmN8HF0PY1wzgDSc4YYtcvPGf36SMPsSKNZ0ui3lTT4QLqeNCRmCQlTC2aJjLYBCoZcfRltVcwtzJD%2FgZcoEOCSPrmQx1crSN0YZgG%2BtSUXuDJT8E59j4AbYHdF5BRrOVKDFshh13TCGYh5mZZA13h2hlNd%2B6BrPCENxICUo6W8Qheu5MCtr%2BVG68BoGDfRKR%2BtoUs8TaA8u%2B%2BevyF%2BgueS0hN0yZQgJYpGwXxxWxTF%2BFPAqZrQJglTTtmMOav5WZTCQ6JTGDRPXSkOic4q6mJkA8qmVfmo7UKbap1oXbTHaG1E2pAmGUBVpFPBwMygL386FYhp8Lr544tLLMU5FfB5UuUbDKKVZRClY5A6LFIT40vJGYQPoW8zyB1dkdFM6TlDTF%2B1gjOap4wun1qP0yHmTCSnDD6CqnA6dMVqm9NRItMqI4H0m2cQ0DFILQwi5r8kZxA%2BhCpxOnSeDOLLDNIziOgk3pZBLq7O3ppBSic%2BOgaph0HEdKbkDMKHUCUMYgDpvQ5N9BJbwRnNU0YXttRDGeLKkdyUkYygKigDqP2s03GnSc8gJV55lJFB6kuWlqaQLllaD4WceRVFXgo5t%2BR6DYWoitW27euaGGi%2BeHSHBWGAP3KscRNUJdudot9skeoa%2Brz9pn%2B%2BL7db5W6KdsUE5urXdCT%2FBl692rUqnoVqDf3qN1u6uib9IzOT6B2T1GKQYiKzJUxS5RKWwm9tDZFwO5bpZQE1%2F7mUog8RqEW72ev7EIEhBihjSEwDBm18XUBEuOBjBIUI1%2Fa%2BgFEYUBBsFY6zAHOwhlt6ujw6mODja5etcxEj%2BbJIBHD5ZxXh%2B88uJM0gJg%2Fir3CpRkWAa2o2SVQUi1i3jEWMa98l%2FHKyR7JscVlPgUe4nadQ8YwjxhyTD8SeJaePkIyVSqKNZFm6PU7CtZvzW7%2B0BDqyaJYsxLBCerKobCN%2BS8ni2iRn67fPKh1ZNEsWYlJMerKoLI9Jd7%2FxvTvykgMPKSWIOmhpinxMukSV3QBhcB64SBhGRxj1WKOY1Jn9fJGYLpLhU8mqM9Ab3KlCiqfvfsfVT59P1yb%2FAw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E>

## Технические сценарии

* I. Обновление информации об изображении, привязанному к определённому серверу.
  + 1. Processing Server отправляет изображение Change Information Handler.
  + 2. Change Information Handler отправляет запрос в Server Manager на получение списка клиентов привязанных к Processing Server.
  + 3. Server Manager возвращает этот список Change Information Handler.
  + 4. Change Information Handler отправляет изображение и список пользователей в API Gateway.
  + 5. API Gateway присылает созданное изображение всем клиентам, указанным в списке.

**Диграмма:**
https://mermaid.live/edit#pako:eNqdk8Fq20AQhl9lmbNqLEuOJR0CJYU2h0Cg9BJ0WayJLBrtuiupbWoMUXIIOQVy6bGv4Ia6MaV1XmH2jTqyk2LjhprqpP1n9_t2pN0R9HWCEEGB7ypUfXyRydTIPFaCn6E0ZdbPhlKV4k2BptiMnx_ui5eyxA_ydLP4Gs17NOJAKpmi2azvDaRKUeyrY21yWWZaiVdSJSd_m3todB-L4oG5rK9nz3Z3nwZGgr7Q1J7RlL7RxF7SRNCM7mhOXzmc0Hcu_KKZvV6SnwaxZb0tJn9mwD1j5rYWtqZ75tT0gxX2ojHZ2p43cI7mdNvMmHJUczBb2taB_-rjhil3dNts2149bnvVy5Itulj5c1t_HI7_q8EVF5sXR2l754ZjQj_XHOBAarIEotJU6ECO3GwzhFFjj6EcYI4xRPyaSPM2hliNeQ0fqyOt88dlRlfpAKJjeVLwqBomvN-H2_AnNagSNHu6UiVEnY4fLigQjeAjRK7bbvneju-2g8ALOkG358Apx77X8jgP3V6HK0FvZ-zAp4W43Qp9P2j7buh2g9Drdn0HMMlKbQ6Wt3JxOce_Acg4oWo

* II. Открытие сессии для редактирования нового изображения.
  + 1. Клиент отправляет запрос в AGI Gateway с параметрами: логин клиента, длина/ширина изображения.
  + 2. API Gateway перенаправляет запрос в Servic Manager.
  + 3. Server Managar собирает информацию о состоянии серверов: какие сервера активны и какие не заняты другими пользователями.
  + Если не существует активного свободного сервера:
    - 4. Server Manager отправляет информацию об этом в API Gateway.
    - 5. API Gateway отправляет информацию о недоступности сервера клиенту.
  + B. Если существует активный свободный сервер:
    - 4. Server Manager отправляет запрос на открытие сессии в свободный Processing Server.
    - 5. Processing Server создаёт новое изображение указанной длины и ширины.
    - 6. Processing Server отправляет информацию о создании изображения в Server Manager.
    - 7. Server Manager помечает Processing Server как занятый.
    - 8. Server Manager сохраняет информацию о том, что пользователем под таким-то логином открыл данную сессию и теперь привязан к такому-то серверу.
    - 9. Server Manager отправляет информацию об открытии сервера в API Gateway.
    - 10. API Gateway отправляет информацию об открытии сервера клиенту.
    - 11. Обновление информации об изображении, привязанному к определённому серверу (сценарий I).

**Диграмма:**
https://mermaid.live/edit#pako:eNq9lM9u00AQxl9lNScQxoprO3F8qISKBD1UqoS4IF9W8daxqNdhbQMlipREiB44VJzgVKlvkFYNREDDK8y-EWMnVHUS_qgHfLB3Z3Z-33z2evvQSUMBPmTiRSFkRzyMeaR4EkhGV4-rPO7EPS5z9jQTKlsPP9jfZY94Ll7xo_XkE6FeCsX2uOSRUOv5nS6XkWC78iBVCc_jVLLHXIaHm9buq7QjsmzJXOSrnu5vb99owmf4ESf4Qw9xrkcMr3DCaDTGr3qo39NzhlOmRzjVI7rPcLYg3SAQr973LZF1CFHrDoh6hufEGTKqudJvyyF-x4l-VzJIoWSSIAnM9QmpltFKZogX1X2OFwupOnndwL82dBubf9NmeKrH-lh_0GPC4fkqc8XThN2h4JdyZTnDzzitrE8NRkXj5VuhBZeU_MbK8rHJ8NK8-xuT9b3xafVN65NlV5tEZ-zeho9zXfJnI5s2VrVh_28bYECk4hD8XBXCgETQn1ZOoV82GEDeFYkIwKdhyNXzAAI5oBr6556lafKrTKVF1AX_gB9mNCt6IVlaHhXXUSVkKNROWsgcfNu2mhUF_D68Bt-yGqZjNx2r4Xm2t-W5LQOOKOzYpk3xttXaoozXag4MeFMJN8y243gNx2pbrte2Xdc1QIRxnqq9xZFVnVyDn6S0Ruw

* III. Запрос списка открытых сессий.

  + 1. Клиент отправляет запрос в API Gateway на получение списка открытых сессий.
  + 2. API Gateway отправляет запрос Server Manager на получение списка открытых сессий.
  + 3. Server Manager собирает информацию о том, какие сервера на данный момент выделены под сессии (на каждый сервер - одна сессия).
  + 4. Server Manager отправляет список активных сессий в API Gateway.
  + 5. API Gateway отправляет список активных сессий пользователю.

**Диграмма:**
https://mermaid.live/edit#pako:eNq1U81O20AQfpXVnE0UY5s4PiAhkCgHJKSql8qXVTw4Fng3Xdu0NIoE_T1w4MiZNwgRkSIg5hV234ixk1ZYCUcseez5Zvb7ZnZnh9CTEUIAGX4pUPRwL-Gx4mkoGD0DrvKklwy4yNmnDFW2Cu8cHbB9nuNXfr4a_IjqDBU75ILHqFbju30uYmQH4liqlOeJFOwDF9HputwjJXuYZUvORbyuaWN7-1URAdM3eqyfzYUuzSXTcz1m-lmX-tH8NH_1lICZnjJzSeCM7APF6TOhjDt67_XcXJnfFTQlikltSz1Z6L3SIdVmd-8q3JQi7eZukPZtxWIuGInMza_qVz_psflD_ozpsuKlsswPstd1KbM3pJrMa9p8o6LmGdwuuyz1w7qtqw-umQYWxCqJIMhVgRakSBNRuTCsCELI-5hiCKQPEVcnIYRiRGtoNj5Lmf5bpmQR9yE45qcZecUgIsnlSP9HFYoI1a4sRA6B0_GdmgWCIXyDwLbbLdfZcu227zv-pu91LDgn2HVaDuFdu7NJEb-zNbLgey3cbnVd12-7dtf2_K7jeZ4FGCW5VIeLq1XfsNELPbB87w

* IV. Запрос на подключение к сессии.

  + 1. Клиент отправляет запрос на подключение к определённому серверу в API Gateway.
  + 2. API Gateway перенаправляет запрос в Server Manager.
  + 3. Server Manager смотрит, занят ли сервер, к которому запрашивают подключение.
  + A. Если сервер не занят (сессия успела закончится):
    - 4. Server Manager отправляет информацию о закрытии сервера API Gateway.
    - 5. API Gateway отправляет информацию о закрытии сервера клиенту.
  + B. Если сервер занят:
    - 4. Server Manager смотрит, кто из пользователей открыл сессию.
    - 5. Server Manager отправляет в API Gateway запрос на подключение к сессии с информацией о том, кто запросил это подключение и кто открыл сессию на сервере.
    - 6. API Gateway отправляет пользователю, открывшему сессию на сервере, запрос на подключение к сессии пользователя, запросившего подключение к серверу.
  + C. Создатель сессии отклонил запрос или не ответил на него в течении определённого времени.
    - 7. API Gateway получает и отправляет информацию об отклоненному запросе клиенту, запросившему подключение к серверу.
  + D. Создатель сессии принял запрос.
    - 7. API Gateway получает и отправляет информацию об принятом запросе клиенту, запросившему подключение к серверу.
    - 8. API Gateway отправляет информацию об принятии запроса в Server Manager.
    - 9. Server Manager добавляет пользователя в список участников сессии, открытой на этом сервере.
    - 10. Обновление информации об изображении, привязанному к определённому серверу (сценарий I).

**Диграмма:**
https://mermaid.live/edit#pako:eNqVk89K60AUxl9lOOtaG5PaJAtBFNSFIIgbyWZojmnQzNRJ4r1aCgre687tXV98gSoWxD_tK5y8kadpFUPrwixCznfy_c6XmUwP2jpE8CHF0xxVGzdjGRmZBErw1ZUmi9txV6pMHKRo0nl5fW9HbMkMf8nz-eY-mjM0YlcqGaGZ7290pIpQ7KgjbRKZxVqJbanCk0Xv7hndxjSdMaf9MtPS2tqXEL6gfzSgcXFJo-JK0BsNBI1pRI_0TC_FbXFDQxafaDhFfLEyqBr4p6yqm3HVzIz7T_eMuhTseSuuJ4_0SoPiL9dPgkaiuKIhaw_lfUatQhaE_GZ4dVHuGD1m7J_l6ffwjAG9LFqDclG_dUANIhOH4GcmxxokyBs3KaE3YQWQdTDBADgVhNIcBxCoPnt4Cw-1Tj5sRudRB_wjeZJylXdDnj778z5VgypEs6FzlYFve55TUsDvwW_wLatRd-xVx2q4ru2uuM1WDc5Zduy6zbpntVa447ZW-zW4KAc36p7juA3H8qym69nNJvMwjDNtdqcnoDwI_Xepaz9l

* V. Внесение изменения в изображение. (Для избежания конфликтов в программе пользователи редактируют изображение по очереди. Когда пользователь заканчивает редактировать изображение и подтвержает окончание своей очереди, он освобождает роль редактора изображения. В этот момент любой другой пользователь может занять роль редактора и начать изменять изображение. Пользователь без роли редактора не может вносить изменения в изображения, но может наблюдать за тем, что делает редактор.)

  + 1. Пользователь как-либо редактирует изображение в свойм клиентском приложении.
  + 2. Клиентское приложение отправляет информацию об изменении API Gateway.
  + 3. API Gateway отправляет эту информацию Change Information Handler.
  + 4. Change Information Handler отправляет эту информацию на нужный Processing Server.
  + 5. Processing Server обрабатывает изменения и применяет их к изображению.
  + 6. Обновление информации об изображении, привязанному к определённому серверу (сценарий I).

**Диграмма:**
https://mermaid.live/edit#pako:eNqFUsFKw0AQ_ZVlLr2kJWk2bbKHglTQHgoF8SK5LMk0DTa7dbNRayl48hu8-gdeigr6D-kfuU2rtNTgwsLOm_feDLOzgEjGCAxyvClQRHia8kTxLBTEnBlXOo3SGReaXOao8mP4ZDQgZ1zjHZ8fJy9Q3aIiQy54guo4359wkSAZiLFUGdepFOSci3j6F3ekZIR5vvPc5quemr3eXhOMlM_lW_lZrsqv6r6Xqy15j2Qk9aXrHeo1xvCwv3qTQ17zv1Ze1k-V_nX9aDw-yKDRAAsSlcbAtCrQggyNahPCYlMhBD3BDENg5hlzdR1CKJZGY6Z4JWX2I1OySCbAxnyam6iYxWY0u8__RRWKGFVfFkIDo-1OULkAW8A9MMexW9TtUMf2fddv-17XgrmBqdtyDR443bbJ-N3O0oKHqrDdCij1beoEjucHrud5FmCcaqmG2yWsdnH5Ddfo9Jc

* VI. Занятие роли редактора | Получение права на редактирование изображение.

  + 1. Клиент отправляет запрос API Gateway на получение права редактировать изображение.
  + 2. API Gateway передаёт запрос Server Manager.
  + 3. Server Manager смотрит, занята ли роль редактора на определённом сервере.
  
  + A. Роль редактора занята:
    - 4. Server Manager отправляет API Gateway информацию о том, что роль редактора занята.
    - 5. API Gateway перенаправляет информацию пользователю.
  + B. Роль редактора не занята.
    - 4. Server Manager выдаёт роль редактора пользователю, запросившему права на редактирование изобраения и сохраняет информацию об этом внутри себя.
    - 5. Server Manager отправляет API Gateway информацию о том, что роль редактора была успешно выдана.
    - 6. API Gateway перенаправляет эту информацию пользователю.

**Диграмма:**
https://mermaid.live/edit#pako:eNqdktFKwzAUhl8lnOs62zXd2lwMREG8GAjijfQmrMeuaNOZpuocA4eIj-AD-AJjMBCG2yukb2TWqmxMb8xVzn_yf-ckOSPoZRECgxxvChQ9PEp4LHkaCmLWgEuV9JIBF4qc5yjzXfng9IQcc4V3fLibPEN5i5J0ueAxyjpfcfY6nQ0jI_pVT_WqfNTLckL0h54SvdJLvSifyhc9N8K7npPqwFTPas6G39C2K_0LuI3Y6fCtnBjEvHzer7l6ZqyL33qpbvinAyyIZRIBU7JAC1KUKV-HMFqzQlB9TDEEZrYRl1chhGJsPOY9L7Is_bbJrIj7wC75dW6iYhCZ6l9f96NKFBHKw6wQChhtNe2KAmwE98Acx25Qt0Ud2_ddv-l7bQuGRqZuwzV64LSbJuO3W2MLHqrCdiOg1LepEzieH7ie51mAUaIy2a1HqJqk8SevEO8g

* VII. Освобождение роли редактора | Сдача прав на редактирование изображение.

  + 1. Клиент подаёт API Gateway запрос о передаче очереди редактировать изображение.
  + 2. API Gateway передаёт информацию об этом Server Manager
  + 3. Server Manager снимает роль редактора с пользователя, запросившего снятие прав на редактирование изображения и сохраняет информацию об этом внутри себя.
  + 4. Server Manager отправляет API Gateway информацию о том, что роль редактора была успешно снята.
  + 5. API Gateway перенаправляет эту информацию всем пользователю.

**Диграмма:**
https://mermaid.live/edit#pako:eNqVks1Kw0AUhV9luOtYM2bSJLMoiIK4KAjiRrIZmmsaNJM6SdRaClZw7dIH8AVKoSBI7StM3shpotJSXTiruefwnXvnZwS9LELgkON1ibKHh4mIlUhDScwaCFUkvWQgZEHOclT5trx_ckyORIG3YrhtnqK6QUW6QooYVePXOTudzhrIiX7RU72sHvRHNSF6oaekmuhF9Vw96jc9J7U11bMmYY00OZs9_hm1CW9N9WrQpZ5XT7tNop4Z9P23KepT_UmABbFKIuCFKtGCFFUqViWMVlkhFH1MMQRutpFQlyGEcmwYc4fnWZZ-Yyor4z7wC3GVm6ocRKb713P9qAplhOogK2UBnHm0XacAH8EdcErtFnPajNq-7_h7vutZMDQyc1qO0QPq7RnH99pjC-7rxnYrYMy3GQ2o6weO6zILMEqKTHWbb1P_nvEnEz_lfQ

## План разработки и тестирования

- **MVP (необходимый минимум):**
1. Написание клиентского приложения для редактирования изображения с минимальным набором функций и инструментов.
2. Реализация API Gateway, Server Manager, Change Information Handler
3. Подключение всего двух серверов (Processing Server).
4. Проведение тестов, добавление частичной отказоустойчивости (отказ первого сервера не затрагивает второй сервер; при падении сервера пользователь может сохранить последние полученные данные).
5. Сценарий IV на подключение к сессии урезан и не включает в себя запрос разрешения на подключение к сессии: пользователь подключается к сессии сразу без согласия её создателя.

**DoD (MVP):**
* Работоспособность:
  + Система обеспечивает одновременную работу как минимум для 3 пользователей на одной сессии.
  + Поддержка как минимум 2 разных сессий на разных серверах в одно и то же время.

* Отказоустойчивость:
  + При падении одного Processing Server не затрагивает другие сессии.
  + При падении сервера изображение не устрачивается полностью: пользователи могут сохранить последние полученные от сервера данные.

* Пользовательские сценарии:
  + Пользовательские сценарии реализованы в соответствии с их описанием.


- **Расширенная часть:**
1. Реализация логов (Log Broker, Logs DB).
2. Полная реализация сценария IV, как он описан в пункте "7. Пользовательские сценарии".
3. Добавление дополнительных инструментов для редактирования изображения (ведро/фигуры/поворот...)
4. Возможность загрузки изображение из вне для дальнейшего редактирования.
5. Улучшение отказоустойчивости: когда сервер падает, сессия автоматически переносится на другой.
6. Масштабируемость на 3 и более серверов.
7. Поддержка редактирования одного изображения 4+ людьми.

**DoD (Расширенная часть):**

* Работоспособность:
  + Система обеспечивает одновременную работу как минимум до 8 пользователей на одной сессии.
  + Поддержка до 4 разных сессий на разных серверах в одно и то же время.

* Отказоустойчивость:
  + При падении одного Processing Server не затрагивает другие сессии.
  + При падении сервера сессия переносится на другой свободный сервер без потери данных об изображении. Если свободного сервера нет, программа отправляет последнюю версию изображения пользователям.

* Пользовательские сценарии:
  + Все пользовательские сценарии реализованы в соответствии с их описанием.
