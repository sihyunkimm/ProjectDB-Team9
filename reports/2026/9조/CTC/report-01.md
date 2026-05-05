---
project_name: "CTC"
quad_name: "9조"
members:
  ["20231717_김시현", "20231741_이예빈", "20251895_곽범준", "20252752_류태현"]
report_number: 1
date: "2026-05-05"
status: "진행 중"
cl_level: "CL1"
contributions:
  - name: "20231717_김시현"
    role: "팀장"
    tasks: "보고서 초안 작성, 역할 조율"
    percentage: 25
  - name: "20231741_이예빈"
    role: "팀원"
    tasks: "FindTheGap 대상 조사"
    percentage: 25
  - name: "20251895_곽범준"
    role: "팀원"
    tasks: "버그바운티 writeup 및 참고 자료 조사"
    percentage: 25
  - name: "20252752_류태현"
    role: "팀원"
    tasks: "FindTheGap 외 버그바운티 대상 조사"
    percentage: 25
---

# 제 1차 프로젝트 진행 보고서 CTC

- **팀원:** (팀장) 20231717_김시현, (팀원) 20231741_이예빈, 20251895_곽범준, 20252752_류태현
- **활동 기간:** 2026. 04. 01. ~ 2026. 05. 05. (중간고사 기간 제외 2주)

---

## 팀 전체 진행 현황

- **이번 회차 목표:** FindTheGap에 등록된 NC소프트 대상의 정책을 확인하고, 서비스 구조와 주요 기능을 빠르게 파악한 뒤 실제 점검이 가능한 후보 영역을 정리한다.
- **현재 진행률:** 10% (초기 조사 및 범위 정리 단계)
- **주요 달성 사항:** 대상 회사와 분석 방향을 NC소프트로 확정했으며, 공개 프로그램의 기본 정책과 허용 범위를 우선 검토했다.

---

## 개인별 기여 내역

| 팀원             | 역할 | 수행 작업                                | 산출물 링크              | 기여도 |
| ---------------- | ---- | ---------------------------------------- | ------------------------ | ------ |
| 20231717\_김시현 | 팀장 | 보고서 초안 작성, 역할 조율              | 보고서 초안              | 25%    |
| 20231741\_이예빈 | 팀원 | FindTheGap NC 프로그램 정책 및 범위 조사 | 본 보고서 참고 자료 섹션 | 25%    |
| 20251895\_곽범준 | 팀원 | 버그바운티 writeup 및 참고 자료 조사     |                          | 25%    |
| 20252752\_류태현 | 팀원 | FindTheGap 외 버그바운티 대상 조사       |                          | 25%    |

---

## 이슈 및 해결 방안

- **문제 상황:** FindTheGap에서 공개 버그바운티를 진행하고 있는 회사가 NC소프트 하나뿐이어서 다른 버그바운티에 대해 조사해야 했다.
- **해결 현황:** 다른 적당한 대안을 조사해보았으나 NC소프트가 가장 적합하다고 결정했다.

---

## 다음 회차 목표

- NC소프트 대상의 세부 기능별 점검 시나리오 정리
- 실제 테스트 전 점검 체크리스트 작성
- 보고서에 넣을 근거 자료와 캡처 항목 정리

---

## 참고 자료

### FindTheGap NC 프로그램 정책 문서 요약

> 출처: FindTheGap 플랫폼 NC 공개 버그바운티 프로그램 페이지 (hacker.findthegap.co.kr)
> 조회일: 2026-05-05

---

#### 1. 프로그램 기본 정보

| 항목                  | 내용                                               |
| --------------------- | -------------------------------------------------- |
| 운영 기간             | 2025.04.01 ~ 2027.03.31                            |
| 프로그램 유형         | 공개(Public) — 파인더갭 가입 해커 누구나 참여 가능 |
| 주요 기술 범위        | Web / Game / Client SW                             |
| 최대 포상금           | 5,000,000원                                        |
| 평가 기준             | 파인더갭 자체 기준                                 |
| 누적 제보 수          | 61건 (유효 11건, 유효율 약 18%)                    |
| 리포트 평가 평균 시간 | 226시간                                            |
| 담당자 응답 평균 시간 | 151시간                                            |

---

#### 2. 포상금 기준표

| 심각도   | 점수     | 포상금                    |
| -------- | -------- | ------------------------- |
| Critical | 90 ~ 100 | 2,000,000원 ~ 5,000,000원 |
| High     | 70 ~ 89  | 1,000,000원 ~ 2,000,000원 |
| Medium   | 40 ~ 69  | 200,000원 ~ 1,000,000원   |
| Low      | 20 ~ 39  | 50,000원 ~ 200,000원      |
| Info     | 0 ~ 19   | 0원                       |

**취약점 예시별 심각도 분류**

| 취약점 예시                                                   | 심각도          |
| ------------------------------------------------------------- | --------------- |
| 임의코드 실행, 웹쉘 업로드 및 실행, SQL Injection (완전 제어) | Critical ~ High |
| 불충분한 인가/인증, SQL Injection (제한적)                    | High ~ Medium   |
| Stored XSS                                                    | Medium ~ Low    |
| 단순 정보 노출                                                | Info            |
| **Reflected XSS**                                             | **포상 제외**   |

---

#### 3. 범위 내 타겟 (In-Scope)

**[Web] plaync.com 계열**

| 구분   | 자산명                    | 도메인                                                                    |
| ------ | ------------------------- | ------------------------------------------------------------------------- |
| Domain | PlayNC 메인               | `www.plaync.com`                                                          |
| Domain | 게임 포털 (커뮤니티 제외) | `{게임명}.plaync.com`                                                     |
| Domain | **로그인**                | `login.plaync.com`                                                        |
| Domain | **내 정보**               | `id.plaync.com`                                                           |
| Domain | **보안**                  | `*security*.plaync.com`                                                   |
| Domain | **백업 인증**             | `*backupauth*.plaync.com`                                                 |
| API    | QR 로그인                 | `qr.plaync.com`                                                           |
| Domain | 전화번호 로그인           | `phoneauth*.plaync.com`                                                   |
| API    | 3rd Party 로그인          | `thirdparty.plaync.com`                                                   |
| API    | 본인인증                  | `cert.plaync.com`                                                         |
| API    | NC ID                     | `ncid.plaync.com`                                                         |
| Domain | **N샵**                   | `store.plaync.com/store/{게임코드}`                                       |
| Domain | **월렛**                  | `store.plaync.com/wallet/*`                                               |
| API    | **코인 충전**             | `orderform.plaync.com`                                                    |
| API    | N코인                     | `ncoin.plaync.com`                                                        |
| Domain | 글로벌 샵                 | `*shop*.plaync.com`                                                       |
| Domain | **캐릭터 선물하기**       | `gifting.plaync.com`                                                      |
| API    | **스토어 API**            | `store-bff.plaync.com`                                                    |
| Domain | 포인트샵                  | `store.plaync.com/point/{게임코드}`                                       |
| API    | 월렛패스                  | `walletpass.plaync.com`                                                   |
| API    | 프로모션                  | `promotion.plaync.com`, `event.plaync.com`                                |
| Domain | 앰버서더 (댓글 제외)      | `creators*.plaync.com`                                                    |
| Domain | 고객센터                  | `help.plaync.com`                                                         |
| API    | 챗봇                      | `chatbot.plaync.com`                                                      |
| Domain | 서비스 동의               | `consent.plaync.com`                                                      |
| Domain | NC Family Zone            | `pcbang.plaync.com`                                                       |
| API    | 퍼플 PC 프로그램          | `purple-store.plaync.com`, `purple-api.plaync.com`, `emoticon.plaync.com` |
| Domain | 퍼플on 플레이             | `purpleon.plaync.com`                                                     |
| API    | 통합검색                  | `*search*.plaync.com`                                                     |
| Domain | 확률정보                  | `probability.plaync.com`                                                  |
| Domain | 개발자센터                | `developers.plaync.com`                                                   |

**[Web] nc.com 계열**

| 구분   | 자산명                  | 도메인                     |
| ------ | ----------------------- | -------------------------- |
| API    | 퍼플 모바일앱 (PC URL)  | `api.g.nc.com`             |
| API    | 퍼플 모바일앱 (PC URL)  | `nccr-api.global.nc.com`   |
| API    | 퍼플 모바일앱 설정      | `mobileappconfig.g.nc.com` |
| Domain | NC 메인 (메인 페이지만) | `www.nc.com`               |

**[Mobile App]**

| 구분    | 자산명                                    |
| ------- | ----------------------------------------- |
| Android | 퍼플 모바일앱 (Android) — 2025.12.01 추가 |
| iOS     | 퍼플 모바일앱 (iOS) — 2025.12.01 추가     |

**[Client SW]**

| 구분      | 자산명                                            |
| --------- | ------------------------------------------------- |
| Client SW | 퍼플 PC 프로그램 (Windows 버전) — 2025.12.01 추가 |

---

#### 4. 범위 외 타겟 (Out-of-Scope)

| 구분                 | 내용                                                                |
| -------------------- | ------------------------------------------------------------------- |
| PlayNC 커뮤니티/채팅 | 커뮤니티 게시판, 퍼플 TALK(채팅) 전체 제외                          |
| 해외 자회사 사이트   | NC 국내 사이트만 허용, 해외 자회사 제외                             |
| 미명시 도메인        | 위 범위 내 타겟 목록 외 모든 도메인                                 |
| Third-Party          | NC 관리범위가 아닌 Third-Party 라이브러리 취약점 (상황에 따라 제외) |
| NC 메인 하위         | `www.nc.com` 내 기업/지속가능경영/소식/IR/채용 페이지               |

---

#### 5. 포상 제외 항목

- Reflected XSS (명시적으로 포상 제외)
- Self XSS (공격자 자신에게만 영향)
- Open Redirect / URL Redirection
- 일반적인 기능의 CSRF (회원정보·관리자 기능 외)
- 보안 헤더 단순 미설정 (CSP, XFO 등)
- SSL/TLS, DNS 설정 단순 지적
- 취약한 버전의 오픈소스 단순 지적
- 에러메시지, 내부 IP 단순 노출 (이를 이용한 유의미한 공격 성공 시에는 포상 대상)
- DoS / 자동 스캔 / 브루트포스
- 루팅된 기기에서만 동작하는 취약점
- 개념증명(PoC) 미비 또는 재현 불가 취약점
- 중복 제보

---

#### 6. 점검 시 필수 준수사항

1. **파인더갭 공식 VPN 필수 사용** (`ftg.openvpn.com`)  
   → 미사용 시 민형사상 면책 불가, IP·계정 차단 발생 시 복구 불가

2. **테스트 문구 필수 삽입**
   - 한국어: `NC 보안 테스트 버그바운티`
   - 영어: `NC Bugbounty TEST`

3. **XSS 테스트 시 `alert()` 대신 `console.log()` 사용**  
   → 일반 사용자 노출 방지

4. **실제 유저 계정·재화 대상 테스트 절대 금지**

5. **자동화 스캔 도구 사용 금지** (탐지 시 프로그램 참가 제한)

6. **결제 테스트 시 환불 불가 상품 사전 확인 필수**

7. **파인더갭 인증서 설치 필요** (미설치 시 VPN 통신 불가)

8. **Burp Suite Config 파일** 파인더갭에서 제공 (빠른 환경 구성 가능)
