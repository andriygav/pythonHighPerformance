# pythonHighPerformance

## Базовый пример
### Описание функций для иследования
В данном пункте приведем пример простой функции на языке python. В качестве функции рассматривалась функция, которая суммирует числа от ***0** до **N***. В эксперименте сравнивается скорость работы данной функции в следующих случаях: 
* ```PythonFunc(N)``` --- функция реализована на python без предварительной компиляции; 
* ```NumbaFunc(N)``` --- функция реализована на python с использованием Numba;
* ```PyPyFunc(N)``` --- функция реализована на pypy;
* ```CythonFunc(N)``` --- функция реализована на python но предварительно скомпилирована;
* ```CythonTypedFunc(N)``` --- функция реализована на cython с типизацией объектов;
* ```CythonOpenMPFunc(N)``` --- функция реализована на cython с типизацией объектов а также распаралеливанием на OpenMP;
* ```NuitkaFunc(N)``` --- функция которая компилируется с помощью Nuitka

### Вычислительный эксперимент
Для сравнения рассматривается ***N = 100000000*** для всех моделей, а также каждая функция вызывается ***200*** раз для усреднения результата.

### Результаты
В данном простом примере получили следующие оценки времени работы функций:
| Функция  | Время |
| ------------- | ------------- |
| PythonFunc  | 4515 ms  |
| PyPyFunc  | 130 ms  |
| NumbaFunc  | 0.2 ms  |
| CythonFunc  | 3335 ms  |
| CythonTypedFunc  | 0.032 ms  |
| CythonOpenMPFunc  | 0.010 ms  |
| NuitkaFunc  | 4035 ms  |

Весь код доступен по [ссылке](https://github.com/andriygav/cythonExample/blob/master/example/SimpleExample.ipynb) и [ссылке](https://github.com/andriygav/cythonExample/blob/master/example/SimpleExamplePypy.ipynb).

## Пример на основе CountVectorizer с пакета sklearn
### Описание функций для иследования
В данном пункте сравним скорости работы простого векторного представления предложений. В качестве базового решения выбран ```CountVectorizer``` из пакета ```sklearn```.

На основе ```CountVectorizer``` был написан сообвественый класс ```Vectorizer``` на python. Данный класс повторяет базовые возможности класса ```CountVectorizer```, такие как ```fit``` и ```transform```. Код доступен по [ссылке](https://github.com/andriygav/cythonExample/blob/master/example/CountVectorizer.ipynb) и [ссылке](https://github.com/andriygav/cythonExample/blob/master/example/CountVectorizerPypy.ipynb).

Сревнение производительности проводится для класса ```Vectorizer``` который работает в следующих случаях:
* ```Vectorizer``` --- простая реалзиция на python без компиляции;
* ```PyPyVectorizer``` --- компииляция функции на pypy3;
* ```CythonVectorizer``` --- простая компиляция класса при помощи cython без использования типизации;
* ```CythonTypedVectorizer``` --- простая компиляция класса при помощи cython c использованием типизации;
* ```NuitkaVectorizer``` --- простая компиляцияя функции при помощи nuitka.


### Вычислительный эксперимент
В эксперименте сравнивается время метода ```fit```, а также метода ```transform``` для всех моделей. Для оценки времени производится усреднение по нескольким независимым вызовам данных методов. Каждый раз вызов метода ```fit``` производится на новом объекте рассматриваемого класса. Метод ```transform``` вызывается также каждый раз на новом объекте рассматриваемого класса после вызова метода ```fit```.
### Результаты
Оценка времени выполнялась для выборки, которая состояла из ***79582*** строк (***16.8mb*** текста). Всего в данном тексте содержится ***76777*** различных токенов, которые были найдены всемы моделями и добавлены в словарь.

Для чистоты эксперимента время представленное в таблице является устредненным по ***200*** вызовам функции ```fit``` и **200** вызовам функции ```transform```.

| Функция  | Время ```fit``` | Время ```transform``` |
| ------------- | ------------- | ------------- |
| Vectorizer  | 492 ms | 1602 ms |
| PyPyVectorizer  | 376 ms | 3167 ms |
| CythonVectorizer  | 456 ms | 1513 ms |
| CythonTypedVectorizer  | 441 ms | 1510 ms |
| NuitkaVectorizer  | 572 ms | 1597 ms |


## Общие замечания и выводы
### Об Cython
После проведенных экспериментов данный компилятор показал себя очень хорошо. Он легкий в использовании легко использовать даже в ```jupyter-notebook``` при помощи команды ```%%cython```.

Как видно из синтетического примера данный компилятор работает очень хорошо когда типы в функциях являются строго фиксируемыми. Как видно из результатов в базовом примере, ***jit*** компилятор ***pypy*** выполняет детский пример намного быстрее, чем после компиляции при помощи ***cython***. Но после добавления типизации ***cython*** версия все равно оказалась намного быстрее.

Также весь исходный код доступен по [ссылке](https://github.com/andriygav/pythonHighPerformance/tree/master/example/CountVectorizer/Cython), [ссылке](https://github.com/andriygav/pythonHighPerformance/tree/master/example/SimpleExample/Cython). Данный код легко собирается выполнив команду:
```
python setup.py build_ext --inplace
```

### Об OpenMP в Cython
Данный функционал является очень полезным. Простой вызов ```prange``` вместо ```range``` и код уже паралелится на чистом OpenMP без дополнительных затрат на ```pickle``` для сериалиции.

Правда для нас как для иследователей и людей которые занимаются анализом данныз и не видят ***python*** без ```numpy``` и всех его плюсов с умножением матриц и других полезных операций данная функция недоступна. Один из важнейших минусов работы OpenMP в ***cython*** является то, что он позволяет паралелить только куски кода которые написаны на C++. А весь код который в себе содержит ***python*** объекты нужно оборачивать в ***GIL*** блокировку. Одним словом вещь хорошая если ваш код написан в большинстве на C++, или же вы не используете ***python*** объекты.

### Об PyPy
Данный транслятор языка ***python*** показал себя намного лучше чем обычный ***python*** и даже лучше чем простые компиляции ***python*** кода при помощи ***cython*** и ***nuitka***. Причем его скорость была сопоставима со скоростью уже скомпилированого кода в котором была задана типизация, а в некоторых случаях даже быстрее.

### Об Nuitka
Достаточно неплохой компилятор для компиляции ***python*** кода. Позволяет как получать исходный код на C++, получать исполняемые модули .so для дальнейшего подключения в ***python*** например.

К сожалению на практике показал самый плохой результат из всех представленых выше. Его скорость была лишь немного выше чем в просто ***python*** транслятора, который выполняется на лету, не говоря уже про ***pypy*** транслятор.

Также весь исходный код доступен по [ссылке](https://github.com/andriygav/pythonHighPerformance/tree/master/example/CountVectorizer/Nuitka), [ссылке](https://github.com/andriygav/pythonHighPerformance/tree/master/example/SimpleExample/Nuitka). Данный код легко собирается выполнив команду:
```
python -m nuitka\
  --module FileName.py\
  --include-package=FileName\
  --follow-import-to=FileName\
  --show-modules\
  --remove-output\
  --output-dir=FileNamePack
```

### Об Numba
Очень классная штука, единственный минус что не компилирует исходник, а является ***jit*** компиляцией. Так же как и ***cython*** имеет свои особености что код под нее нужно переписывать. Имеет встроенную автоматическую процедуру распаралеливания кода.

Базовый пример показал, что данный транслятор намного быстрее всех других.

## Список источников
* Kurt W. Smith. Cython: A Guide for Python Programmers. Sebastopol: O’Reilly, 2015.
* Gorelick M., Ozsvald I. Hight Performance Python. Sebastopol: O’Reilly, 2014.
