---
project_name: "하품 홈페이지 웹 서비스 보안 취약점 분석"
quad_name: "2조"
members: ["20245035_강준수", "20245039_김레빈", "20251790_김준수", "20252751_김홍균"]
report_number: 4
date: "2026-07-02"
status: "진행 중"
cl_level: "CL1"
contributions:
  - name: "20245035_강준수"
    role: "팀장 / 로컬 검증 범위 관리 및 보고서 정리"
    tasks: "운영 서비스에 영향을 주지 않는 로컬 PoC 검증 범위를 관리하고, 이메일 인증 우회·CSRF·IDOR 등 핵심 취약점의 재현 결과를 보고서 구조에 맞게 정리함"
    percentage: 25
  - name: "20245039_김레빈"
    role: "팀원 / 웹 취약점 PoC 검증"
    tasks: "회원가입 이메일 인증 우회, CSRF, 저장형 XSS, 비로그인 업로드 등 웹 기능 단위 취약점의 요청 흐름과 재현 조건을 확인함"
    percentage: 25
  - name: "20251790_김준수"
    role: "팀원 / 로컬 실행 환경 및 서버 설정 분석"
    tasks: "Docker MySQL, Redis, Spring Boot 로컬 실행 환경을 구성하고 세션 쿠키, 업로드 경로, 정적 리소스 공개 설정 등 서버 측 보안 설정을 확인함"
    percentage: 25
  - name: "20252751_김홍균"
    role: "팀원 / DB 상태 검증 및 영향도 분석"
    tasks: "PoC 수행 전후 DB 상태 변화를 확인하고, 마이페이지 IDOR 삭제, 인증 우회 계정 생성, 프로필 변경 등 실제 영향도를 정리함"
    percentage: 25
---

# [제 4차 프로젝트 진행 보고서] 하품 홈페이지 웹 서비스 보안 취약점 분석

- **팀원:** (팀장) 20245035_강준수, (팀원) 20245039_김레빈, 20251790_김준수, 20252751_김홍균
- **활동 기간:** 2026. 06. 24. ~ 2026. 07. 02. (1주)

## 팀 전체 진행 현황

- **이번 회차 목표:**
  3차 보고서에서 계획한 로컬 재현 절차를 실제로 수행하고, 소스 기반으로 의심했던 취약점이 HTTP 요청과 DB 상태 변화로 재현되는지 확인한다. 운영 중인 `https://hapum.org/` 서비스에는 자동화 요청, 대량 요청, 파일 업로드, 인증 우회 요청을 보내지 않고, 모든 PoC는 제공받은 소스 코드와 DB dump를 이용한 로컬 환경에서만 수행한다.

- **현재 진행률:** 80%
  주요 취약점 후보에 대한 로컬 PoC 재현을 완료하고, 이메일 인증 우회, CSRF 보호 부재, 마이페이지 IDOR, 비로그인 파일 업로드, 저장형 XSS, 쿠키 보안 속성 미흡을 실제 영향이 있는 취약점으로 정리하였다. 다음 회차에서는 수정 우선순위와 개선 전후 재검증 기준을 정리할 예정이다.

- **주요 달성 사항:**
  - Spring Boot 프로젝트를 로컬에서 빌드 및 실행하고, Docker 기반 MySQL/Redis 테스트 환경을 구성하였다.
  - 테스트용 DB dump를 `hapumdb`에 import하고 주요 테이블과 사용자 데이터를 확인하였다.
  - 이메일 인증 완료 여부를 클라이언트 hidden field에 의존하는 회원가입 우회 가능성을 확인하였다.
  - CSRF token 없이 세션 쿠키만으로 마이페이지 프로필 변경 POST 요청이 처리되는 것을 확인하였다.
  - 일반 사용자 세션으로 타인의 프로그램 신청 및 대관 예약을 삭제할 수 있는 IDOR를 확인하였다.
  - 비로그인 상태에서 Summernote 이미지 업로드 및 임시 비디오 업로드가 가능하고, 반환된 파일 URL이 공개 접근되는 것을 확인하였다.
  - 관리자 작성 HTML이 `th:utext`로 escape 없이 출력되어 저장형 XSS로 이어질 수 있음을 확인하였다.
  - `JSESSIONID`와 커스텀 쿠키에 `Secure`, `HttpOnly`, `SameSite` 속성이 부족한 것을 확인하였다.

### 로컬 환경 구성 결과

| 구분 | 결과 |
|---|---|
| 애플리케이션 | Spring Boot 프로젝트 빌드 성공 및 로컬 `8080` 포트 실행 |
| DB | Docker MySQL `8.0.46` 컨테이너에 `hapumdb` 생성 후 dump import |
| Redis | Docker Redis `7-alpine` 컨테이너 실행 |
| DB import | 14개 테이블 및 사용자 데이터 import 확인 |
| 실행 보정 | 로컬 PC에 JDK 17이 없어 임시 복사본의 Gradle toolchain만 JDK 21로 변경해 실행. 원본 소스는 변경하지 않음 |

초기에는 Docker Desktop이 꺼져 있었고, Windows host에서 MySQL 컨테이너 `3306` 포트로 접속할 때 인증 매칭 문제가 있었다. 검증용 MySQL 컨테이너를 `33306` 포트로 새로 띄워 TCP 접속을 확인한 뒤 애플리케이션을 연결했다.

### PoC 검증 요약

| 항목 | 로컬 재현 결과 | 영향 |
|---|---|---|
| 회원가입 이메일 인증 우회 | 인증 메일 발송/번호 확인 없이 `emailChecked=true`, `emailVerificationPassed=true`만 포함한 `/auth/doSignin` POST로 계정 생성 성공 | 이메일 소유 검증 없이 임의 계정 생성 가능 |
| CSRF 보호 부재 | 로그인 세션 쿠키만 사용하고 CSRF token 없이 `/main/mypage/update` POST 수행. 테스트 계정 프로필 값 변경 확인 | 외부 페이지를 통한 사용자 상태 변경 가능 |
| 마이페이지 IDOR | 사용자 `93` 세션으로 다른 사용자 소유 `program_subscriptions` 및 `rental_reservation` 레코드 삭제 성공 | 타 사용자 프로그램 신청/대관 예약 임의 삭제 가능 |
| 비로그인 업로드 | 쿠키 없이 `/writePost/uploadSummernoteImageFile` 이미지 업로드 성공. 반환된 `/uploads/temp/...` URL도 200 접근 가능 | 저장 공간 악용 및 악성/부적절 파일 호스팅 위험 |
| 임시 비디오 업로드 검증 부재 | 쿠키 없이 `/upload/video-temp`에 일반 텍스트 파일 업로드 성공. `/temp/videos/...` URL로 다운로드 가능 | 확장자/MIME 검증 없는 임의 파일 저장 및 공개 |
| 저장형 XSS | 관리자 공지 작성 경로로 이벤트 핸들러가 포함된 HTML 저장. 공지 상세 페이지에서 `th:utext`로 escape 없이 출력 확인 | 관리자 작성 경로 탈취, CSRF, 계정 침해와 결합 시 사용자 브라우저 내 스크립트 실행 |
| 쿠키 보안 속성 부재 | 로그인 응답의 `tempSessionId`, `JSESSIONID`에 `Secure`, `HttpOnly`, `SameSite` 속성 미확인 | XSS/네트워크/CSRF 위험 완화 실패 |

### 주요 재현 증적

### 1. 이메일 인증 우회

정상 흐름에서는 이메일 중복 확인 및 인증번호 확인을 완료해야 회원가입 버튼이 노출된다. 그러나 서버의 `UserAuthService.processSignup()`은 클라이언트가 전송한 boolean 값을 신뢰하고, Redis 등에 저장된 실제 인증 완료 상태를 다시 확인하지 않는다.

로컬 PoC 결과는 다음과 같다.

| 조건 | 결과 |
|---|---|
| `emailChecked`, `emailVerificationPassed` 생략 | HTTP 200, DB insert 없음 |
| 두 필드를 `true`로 조작 | HTTP 302 `/auth/success`, DB insert 1건 생성 |

따라서 현재 서버 검증은 실제 이메일 인증 완료 여부가 아니라 요청 파라미터에 `true`가 들어왔는지에 의존한다.

### 2. CSRF

`SecurityConfig.java`에서 CSRF가 비활성화되어 있고, 마이페이지 및 관리자 POST 요청에도 별도 CSRF token 검증이 없다. 테스트 계정으로 로그인한 뒤 세션 쿠키만 첨부하여 `/main/mypage/update`에 POST 요청을 보냈고, DB의 이름과 전화번호 값이 변경됐다.

확인 결과는 다음과 같다.

| 단계 | 결과 |
|---|---|
| 변경 전 | 테스트 계정의 기존 이름/전화번호 확인 |
| CSRF token 없는 POST | HTTP 302 `/main/mypage/{id}` |
| 변경 후 | DB 값이 POST 요청 값으로 변경됨 |

### 3. IDOR

`MypageController`의 삭제 요청은 로그인 사용자의 세션은 확인하지만, 삭제 대상 리소스가 해당 사용자 소유인지 검증하지 않는다.

검증 결과는 다음과 같다.

| 요청 | 로그인 사용자 | 삭제 대상 소유자 | 삭제 전 | 삭제 후 |
|---|---:|---:|---:|---:|
| `/main/mypage/programDelete/{id}` | 93 | 1 | 1 | 0 |
| `/main/mypage/rentalDelete/{id}` | 93 | 72 | 1 | 0 |

또한 회원 탈퇴 처리인 `/main/mypage/out/{id}`에는 `user.getId() != user.getId()`라는 항상 false인 비교식이 있어, path variable의 사용자 id 검증이 사실상 동작하지 않는다.

### 4. 비로그인 파일 업로드

파일 업로드 컨트롤러는 `/admin/**` 또는 `/main/mypage/**` 하위 경로가 아니므로 현재 interceptor 보호 범위에 들어가지 않는다. Spring Security에서도 모든 요청이 `permitAll()` 처리되어 있어 비로그인 상태에서도 접근 가능했다.

검증 결과는 다음과 같다.

| 엔드포인트 | 테스트 파일 | 결과 |
|---|---|---|
| `/writePost/uploadSummernoteImageFile` | PNG 이미지 | JSON `responseCode=success`, `/uploads/temp/...png` 200 접근 |
| `/upload/video-temp` | 일반 텍스트 파일 | `/temp/videos/...` 저장 및 200 다운로드 |

특히 비디오 임시 업로드는 확장자, MIME type, 파일 내용 검증 없이 `originalFilename`을 포함해 저장한다.

### 5. 저장형 XSS

템플릿 여러 곳에서 DB에 저장된 HTML을 `th:utext`로 출력한다. 관리자 공지 작성 경로는 `Jsoup.parseBodyFragment()`를 사용하지만 sanitize가 아니라 HTML 파싱 및 일부 video 경로 치환만 수행한다.

확인된 출력 지점 예시는 다음과 같다.

- `main/notification-detail.html`: `${notification.content}`
- `main/news/newsDetail.html`: `${news.content}`
- `main/programDetail.html`: `${program.content}`
- `main/organizationView.html`: `${organizationPost.content}`

로컬 관리자 테스트 계정으로 공지 content에 이벤트 핸들러가 포함된 HTML을 저장했고, 상세 페이지 응답에서 해당 이벤트 핸들러가 escape 없이 포함되는 것을 확인했다.

### 원인 정리

1. 인증/인가 정책이 Spring Security가 아니라 일부 interceptor 경로에 분산되어 있다.
2. `SecurityConfig`에서 CSRF, form login, HTTP Basic이 비활성화되어 있고 모든 요청이 허용된다.
3. 회원가입의 이메일 인증 완료 여부를 서버 상태가 아니라 클라이언트 hidden field로 판단한다.
4. 마이페이지 삭제 요청이 리소스 소유자 검증 없이 path variable id를 그대로 사용한다.
5. 업로드 엔드포인트가 인증 경로 밖에 있고, 파일 타입/확장자/저장 위치/공개 URL 정책이 충분히 제한되지 않는다.
6. 사용자 또는 관리자 입력 HTML을 sanitize하지 않고 `th:utext`로 출력한다.
7. 세션 쿠키와 커스텀 쿠키에 기본 보안 속성이 부족하다.

### 개선 우선순위

1. Spring Security 중심으로 인증/인가 정책을 재구성하고 기본 deny 방식으로 전환한다.
2. CSRF 보호를 다시 활성화하고 모든 상태 변경 요청에 token 검증을 적용한다.
3. 회원가입 이메일 인증은 Redis 등 서버 저장 상태를 기준으로 검증하고, hidden field 값은 신뢰하지 않는다.
4. 마이페이지 삭제/수정 요청은 항상 세션 사용자 id와 리소스 소유자 id를 서버에서 비교한다.
5. `/main/mypage/out/{id}`의 잘못된 비교식을 수정하고 path variable 대신 세션 사용자 id를 기준으로 처리한다.
6. 업로드 엔드포인트를 인증된 작성자/관리자에게만 허용하고, 확장자/MIME/content allowlist, 파일 크기 제한, 저장 경로 분리를 적용한다.
7. HTML 입력은 `Jsoup.clean()`과 `Safelist`로 허용 태그/속성만 남긴 뒤 저장한다. 가능하면 일반 사용자 출력은 `th:text`를 기본으로 사용한다.
8. `Secure`, `HttpOnly`, `SameSite=Lax` 또는 `Strict` 쿠키 속성을 설정한다.
9. 소스와 산출물에 포함된 운영 비밀값은 즉시 교체하고, `.env` 또는 서버 환경변수/Secret Manager로 분리한다.

## 개인별 기여 내역

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20245035_강준수 | 팀장 / 로컬 검증 범위 관리 및 보고서 정리 | 운영 서비스에 영향을 주지 않는 로컬 PoC 검증 범위를 관리하고, 이메일 인증 우회·CSRF·IDOR 등 핵심 취약점의 재현 결과를 보고서 구조에 맞게 정리함 | [PR #63](https://github.com/ssu-asc/ProjectDB/pull/63), 본 보고서 내 팀 전체 진행 현황, PoC 검증 요약, 개선 우선순위 | 25% |
| 20245039_김레빈 | 웹 취약점 PoC 검증 | 회원가입 이메일 인증 우회, CSRF, 저장형 XSS, 비로그인 업로드 등 웹 기능 단위 취약점의 요청 흐름과 재현 조건을 확인함 | [PR #63](https://github.com/ssu-asc/ProjectDB/pull/63), 본 보고서 내 이메일 인증 우회, CSRF, 업로드, 저장형 XSS 재현 증적 | 25% |
| 20251790_김준수 | 로컬 실행 환경 및 서버 설정 분석 | Docker MySQL, Redis, Spring Boot 로컬 실행 환경을 구성하고 세션 쿠키, 업로드 경로, 정적 리소스 공개 설정 등 서버 측 보안 설정을 확인함 | [PR #63](https://github.com/ssu-asc/ProjectDB/pull/63), 본 보고서 내 로컬 환경 구성 결과 및 쿠키 보안 속성 점검 결과 | 25% |
| 20252751_김홍균 | DB 상태 검증 및 영향도 분석 | PoC 수행 전후 DB 상태 변화를 확인하고, 마이페이지 IDOR 삭제, 인증 우회 계정 생성, 프로필 변경 등 실제 영향도를 정리함 | [PR #63](https://github.com/ssu-asc/ProjectDB/pull/63), 본 보고서 내 IDOR, DB 변경 결과, 원인 정리 | 25% |

## 이슈 및 해결 방안

- **문제 상황:**
  1. 운영 중인 서비스에 직접 PoC를 수행하면 실제 사용자 데이터 변경, 파일 저장, 서비스 장애 위험이 있다.
  2. 테스트용 DB dump에도 개인정보성 데이터가 포함될 수 있어 증적 작성 시 원문 사용자 식별 정보 노출을 피해야 한다.
  3. 일부 취약점은 Spring Security 비활성화, interceptor 범위 제한, 쿠키 속성 미흡 등 공통 구조와 연결되어 있어 단일 기능 수정만으로는 완전한 해결이 어렵다.
  4. 로컬 환경에서 JDK 버전과 DB 접속 포트 문제 등 실행 환경 차이가 있어 원본 소스 변경 없이 임시 실행 보정이 필요했다.

- **해결 현황:**
  운영 서버에는 공격성 요청을 보내지 않고 로컬 격리 환경에서만 PoC를 수행하였다. DB 상태 변화는 테스트 계정과 레코드 count 중심으로 확인하고, 보고서에는 원본 개인정보, 운영 비밀번호, 세션 값, DB dump의 실제 사용자 식별 정보는 포함하지 않았다. 실행 환경 문제는 원본 소스가 아닌 임시 복사본 설정만 조정하여 검증했다.

## 다음 회차 목표

- 실제 영향도가 높은 이메일 인증 우회, IDOR, CSRF, 비로그인 업로드 차단 순서로 수정안을 구체화한다.
- 수정 전/후 재현 결과를 비교할 수 있는 재검증 체크리스트를 작성한다.
- Spring Security 기반 인증/인가 정책과 CSRF token 적용 범위를 정리한다.
- 마이페이지 삭제/수정 요청의 소유권 검증 로직을 엔드포인트별로 점검한다.
- 업로드 기능의 인증, 파일 타입 검증, 크기 제한, 저장 경로, 공개 URL 정책을 정리한다.
- 저장형 XSS 방지를 위한 HTML sanitize 정책과 세션 쿠키 보안 속성 적용안을 정리한다.
- 발표자료에는 로컬 테스트 계정과 전후 count 중심의 증적만 포함한다.

## 참고 자료

- 프로젝트 계획서 `report-00.md`
- 1차 프로젝트 진행 보고서 `report-01.md`
- 2차 프로젝트 진행 보고서 `report-02.md`
- 3차 프로젝트 진행 보고서 `report-03.md`
- OWASP Web Security Testing Guide
- OWASP Cross-Site Request Forgery Prevention Cheat Sheet
- OWASP Cross-Site Scripting Prevention Cheat Sheet
- Spring Security Reference
