---
project_name: “phishing-site-detector"
quad_name: "team5"
members: ["20252718_김도형", "20251711_김태연", "20261686_김태은", "20261621_조성호"]
report_number: 0               
date: "2026-03-29"
status: "시작 전"
cl_level: "CL1"
field: "웹 보안"           
contributions:
  - name: "20252718_김도형"
    role: "팀장"
    tasks: "계획서 작성"
    percentage: 25
  - name: "20251711_김태연"
    role: "팀원"
    tasks: "계획서 작성"
    percentage: 25
  - name: "20261686_김태은"
    role: "팀원"
    tasks: "계획서 작성"
    percentage: 25
  - name: "20261621_조성호"
    role: "팀원"
    tasks: "계획서 작성"
    percentage: 25
---

# 2026년 ASC 프로젝트 계획서

| 항목 | 내용 |
|------|------|
| **학교명** |숭실대학교 |
| **동아리명** | ASC |
| **프로젝트명(주제)** |Phishing Site Detector |
| **프로젝트 분야** |웹 보안 |

## 프로젝트 개요

> URL 구조, 도메인 등록 정보, 웹페이지 콘텐츠 등 다중 피처를 추출하고, 머신러닝 모델(Random Forest, XGBoost)을 활용하여 피싱 사이트를 자동으로 판별하는 시스템을 개발한다. PhishTank·Tranco 등에서 수집한 데이터셋으로 모델을 학습시키고, FastAPI 기반 백엔드 서버와 Chrome Extension을 통해 사용자가 실시간으로 URL의 안전 여부를 확인할 수 있는 서비스를 제공한다.

## 기대 효과
신규 피싱 URL도 다중 피처 분석을 통해 높은 정확도로 탐지할 수 있으며, Chrome Extension을 통해 보안 지식이 없는 일반 사용자도 브라우징 중 즉시 URL 안전성을 확인할 수 있다.
---

# 프로젝트 세부 계획서

## 1. 프로젝트 목적 (추진배경, 취지 등)

-스미싱, 보이스피싱, 이메일 피싱 등 각종 사기 수법들이 정교해지면서 일반 사용자가 피싱 사이트를 판별하기 어려워졌다. 이를 방지하는 차원에서 일반 사용자도 피싱을 예방할 수 있는 접근성이 좋은 피싱 판별 시스템을 구현

## 2. 프로젝트 세부내용

-피싱 url과 정상 url에 대한 학습 데이터를 수집하고 데이터셋을 구축
-url 길이, 특수문자 수, IP 직접 사용 여부, HTTPS 여부, 서브도메인수, 도메인 유사도 탐지, 도메인 등록일 및 만료일, 등록자 정보 공개 여부, SSL 인증서 등을 판별


## 3. 프로젝트 기대효과

-신규 피싱 사이트에 대해서도 높은 정확도로 탐지
-Chrome Extension을 통해 일반 사용자의 별도 조작 없이 실시간 탐지에 따른 보안 접근성 향상

## 4. 프로젝트 수행시 문제점 (내외부 요인 기술)

-팀원 전원이 보안 분야 경험이 부족해 기초 개념 습득에 초기 시간 소요 예상
-데이터를 학습시킬 때 최신 피싱 수법을 완전히 반영하지 못할 수 있음
-실제 피싱 URL에 접근하여 콘텐츠를 수집하는 과정에서 보안 위협 가능성 존재

## 5. 프로젝트 수행시 요구사항 (프로젝트 구성원, 개발환경 등)

-구성원마다 구현 서비스를 할당
-할당한 서비스들을 하나로 합쳐야 하기 때문에 동일한 개발환경 요구

## 6. 프로젝트 수행시 활용되는 장비 및 물품

| 장비명/물품명 | 세부사양 |
|:---:|------|
| **H/W** |개인 노트북 |
| **S/W** |Python 3.9, VSCode, pandas, numpy, Chrome Extension API, Google Safe Browsing API |
| **기타(도서 등)** |PhishTank, Tranco Top 1M, VirusTotal API |

## 팀원 역할 분담

| 팀원 | 역할 | 담당 업무 |
|------|------|----------|
| 20252718_김도형 | 팀장 |모델 학습 및 성능 튜닝, 백엔드 API 개발 |
| 20251711_김태연 | 팀원 |피처 엔지니어링, Chrome Extension 개발 |
| 20261686_김태은 | 팀원 |데이터 수집/전처리, HTML 콘텐츠 크롤링 |
| 20261621_조성호 | 팀원 |교차 검증 로직, 사이트 시각적 유사도 분석 |

## 참고 자료

-DigiCert 가짜 웹사이트 식별 가이드: https://www.digicert.com/kr/blog/how-to-identify-fake-websites
-KAIST CSRC 피싱 사이트 분석: https://csrc.kaist.ac.kr/blog/2024/02/19/
-SSL 인증서 종류 (DV/OV/EV): https://m.blog.naver.com/ucert/221392978294
-인증씰 확인 방법: https://m.blog.naver.com/ucert/221406583900	
-피싱 탐지 머신러닝 사례: https://min8282.tistory.com/93


