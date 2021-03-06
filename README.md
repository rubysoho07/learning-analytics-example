# Learning Analytics Example

PyCon Korea 2018 컨퍼런스 중 '파이썬으로 학생 들여다보기' 세션의 샘플 코드입니다. <br>
(Sample code for 'Looking into Student Experience with Python' of PyCon Korea 2018.) 

(Reference: https://www.pycon.kr/2018/program/32 - In Korean)

## 학습 데이터 저장 방법 샘플 코드 (Sample Code of How to Store Learning Data)

### xAPI

1. Actor, Verb, Object - Elements of Statement(Statement의 요소): https://gist.github.com/rubysoho07/062df1cf32a72a0bbc3ebd77c5111312
2. Statement - Describing Learning Activities(학습 활동 표현): https://gist.github.com/rubysoho07/33729dec4dcfbb0ef37d05dbe31f9df4

### Caliper

1. Actor, Action, Object - Elements of Event(Event의 요소): https://gist.github.com/rubysoho07/393057852a1457fb7d826ae3d21cf2c5
2. Event - Describing Learning Activities(학습 활동 표현): https://gist.github.com/rubysoho07/810d7b0e4c2b94fb1a8fb1af625a6c6c

## 학습 데이터 저장 및 분석 예제 실행하기

### 테스트 환경 (Test Environment)

* Python 3.6.5
* Ubuntu 18.04 LTS
* MongoDB 3.6

### 예제 실행 방법 (How to Run Example)

0. 소스를 먼저 받으세요. (Git이 설치되어 있지 않다면, 우측의 `Clone or download` -> `Download ZIP`을 눌러서 압축 파일을 받습니다. 파일을 받으면 적당한 곳에 압축을 풀어줍니다.) 
   <br> Clone this repository. (If Git is not installed, click `Clone or download` -> `Download ZIP` to download zip archive. Unzip the file where you want to)
```bash
$ git clone https://github.com/rubysoho07/learning-analytics-example.git
```
1. 데이터 저장을 위해 MongoDB를 설치해 주세요. 사용하는 플랫폼에 맞추어 설치하면 됩니다. <br>
   Install MongoDB to store learning data. Check your operating system before installation. <br>
(Reference: https://docs.mongodb.com/manual/administration/install-community/)
2. pip으로 필요한 패키지를 설치합니다. (기왕이면 `virtualenv`를 이용하여 별도의 환경을 구성하는 것이 좋습니다.)
   <br> Install prerequisites with pip. (If possible, I want to recommend to make a virtual environment with `virtualenv`.) 
```bash
$ cd learning-analytics-example
$ pip install -r requirements.txt
```
3. MongoDB 서버를 실행합니다. / Run MongoDB Server.
4. 테스트용 데이터를 MongoDB에 import 합니다. (Localhost에 설치함을 가정) <br>
   Import test data to MongoDB. (Supposed that MongoDB was installed in localhost.)
```bash
$ mongoimport --host='localhost:27017' -d 'LRS' -c 'CaliperEvents' --file='caliper_gradeevent_sample.json'
```
5. Flask 어플리케이션을 실행합니다. / Run a Flask application.
```bash
$ python main.py
In folder /home/yungon/workspace/learning-analytics-example
/home/yungon/.pyenv/versions/la-example/bin/python -m flask run
 * Serving Flask app "main.py"
 * Environment: development
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
``` 
6. 웹 브라우저에서 `http://localhost:5000`으로 접속합니다. <br>
   Connect to `http://localhost:5000` on your web browser.

## 사용한 것들 (Used in This Project)

* Flask
* PyMongo
* Caliper Python 1.1
* Billboard.js

## 참고자료 (References)

* xAPI Specification (ADL): https://github.com/adlnet/xAPI-Spec 
* Caliper v1.1 Specification (IMS Global): https://www.imsglobal.org/sites/default/files/caliper/v1p1/caliper-spec-v1p1/caliper-spec-v1p1.html 
* TinCan Python(xAPI): https://github.com/RusticiSoftware/TinCanPython 
* Caliper Sensor API(Python): https://github.com/IMSGlobal/caliper-python
