# DOCS
Після імпорту репозиторія треба зробити віртуальне оточення **(_venv_)** та встановити залежности **(_requirements.txt_)**.
В папці з проектом треба через VSC в терміналі або СMD (попередньо треба відкрити папку з проектом за допомогою **cd**) ->

### Створити оточення ->
```
python -m venv venv
```
### Активувати оточення ->
```
venv\Scripts\activate (for win)
source venv/bin/activate (for linux | macOS)
```
### Встановити залежності ->
```
pip install -r requirements.txt
```

# test1
Для запуску треба перейти в терміналі в папку test1 з проектом за допомогою **cd test1**.
### В терміналі викликати ->
```
uvicorn main:app --reload
```
Відбуваеться запуск сервера FastAPI на localhost ->
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\Northern Lights\\Documents\\JoinUP_test\\test1']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [22112] using WatchFiles
api_data engine
DB & table successfully created.
INFO:     Started server process [10052]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
Після цього через браузер можна перейти на localhost (http://127.0.0.1:8000) і далі в шляху прописати /api/{cui}
```
http://127.0.0.1:8000/api/30991878
```
Запис в базу відбуається автоматично, message інформує.
### P.S. Передбачається, що MS SQL вже встановлений і запущений на localhost.
### З початку йде підключеня на master і там створюється база api_data. Після підключення до api_data.

# test2
Достатньо в VSC просто запустити сам файл через Run File
