# Learning Analytics Example

PyCon Korea 2018 컨퍼런스 중 '파이썬으로 학생 들여다보기' 세션의 샘플 코드입니다. 

(참고: https://www.pycon.kr/2018/program/32)

## TODO List

* [ ] xAPI 기반의 학습 데이터 생성 샘플 코드 (Gist로 제공 예정)
* [ ] Caliper 기반의 학습 데이터 생성 샘플 코드 (Gist로 제공 예정)
* [x] Flask + PyMongo + Caliper-Python 설치
* [x] 로그인/로그아웃 기능 + Caliper 기반의 데이터 생성
* [x] 글 읽기 기능 + Caliper 기반의 데이터 생성
* [x] 태그 기능 + Caliper 기반의 데이터 생성
* [x] 평가 시작 기능 + Caliper 기반의 데이터 생성
* [x] 평가 종료 및 결과 표시 기능 + Caliper 기반의 데이터 생성
* [ ] Caliper 데이터를 바탕으로 한 1일 단위의 학습활동 대시보드
* [ ] Caliper 데이터를 바탕으로 한 유사 그룹과의 성적 비교 대시보드
* [ ] 발표한 내용을 청중이 스스로 재현할 수 있도록 README.md 파일 보강
* [ ] 테스트

## 필요한 패키지 설치

1. 데이터 저장을 위해 MongoDB를 설치해 주세요. 사용하는 플랫폼에 맞추어 설치하면 됩니다.
(참고자료: https://docs.mongodb.com/manual/administration/install-community/)
2. pip으로 필요한 패키지를 설치합니다.
```bash
$ pip install -r requirements.txt
```

## 참고자료

* xAPI Specification (ADL): https://github.com/adlnet/xAPI-Spec 
* Caliper v1.1 Specification (IMS Global): https://www.imsglobal.org/sites/default/files/caliper/v1p1/caliper-spec-v1p1/caliper-spec-v1p1.html 
* TinCan Python(xAPI): https://github.com/RusticiSoftware/TinCanPython 
* Caliper Sensor API(Python): https://github.com/IMSGlobal/caliper-python
