# 프로젝트 보고서 제출 가이드

## 제출 절차

### 1. Fork & Clone

이 레포를 본인 GitHub 계정으로 Fork한 뒤 Clone합니다.

```bash
git clone https://github.com/<your-username>/ProjectDB.git
cd ProjectDB
```

### 2. 브랜치 생성

```bash
git checkout -b project/<조명>/<프로젝트명>/report-<회차>
# 예: git checkout -b project/A조/web-scanner/report-01
```

### 3. 디렉토리 및 파일 생성

디렉토리 네이밍 규칙:

```
reports/{YYYY}/{쿼드조명}/{프로젝트명}/
```

- **YYYY**: 연도 (예: `2026`)
- **쿼드조명**: 소속 쿼드 조 (예: `A조`, `B조`)
- **프로젝트명**: 소문자, 공백은 하이픈으로 (예: `web-scanner`, `fuzzer-dev`)

```bash
mkdir -p reports/2026/A조/web-scanner
cp templates/report-template.md reports/2026/A조/web-scanner/report-01.md
```

최종 보고서의 경우:

```bash
cp templates/final-report-template.md reports/2026/A조/web-scanner/report-08.md
```

### 4. 보고서 작성

YAML frontmatter를 반드시 작성합니다.

#### 필수 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| `project_name` | 프로젝트명 | `Web Scanner` |
| `quad_name` | 쿼드 조 | `A조` |
| `members` | 팀원 목록 (리스트) | `["20241234_홍길동", ...]` |
| `report_number` | 보고 회차 (1~8) | `1` |
| `date` | 제출일 | `2026-04-01` |
| `status` | 진행 상태 | `진행 중` |
| `cl_level` | CL 등급 | `CL1` |
| `contributions` | 팀원별 기여도 | (아래 참조) |

#### status 유효값

`시작 전`, `진행 중`, `보류`, `완료`

#### cl_level 유효값

`CL1`, `CL2`, `CL3`, `CL4`

#### contributions 작성법

```yaml
contributions:
  - name: "20241234_홍길동"
    role: "백엔드 개발"
    tasks: "API 서버 구축 및 DB 스키마 설계"
    percentage: 30
  - name: "20241235_김철수"
    role: "프론트엔드 개발"
    tasks: "React UI 컴포넌트 구현"
    percentage: 25
```

- 모든 `members`에 대해 작성 (빠진 사람 없어야 함)
- `percentage` 합계는 반드시 100
- `tasks`는 빈 문자열 불가 (구체적 작업 내용 필수)

### 5. 로컬 검증

```bash
pip install -r scripts/requirements.txt
python scripts/validate_frontmatter.py
```

### 6. Commit & Push

```bash
git add reports/2026/A조/web-scanner/report-01.md
git commit -m "Add report: A조/web-scanner report-01"
git push origin project/A조/web-scanner/report-01
```

### 7. Pull Request

GitHub에서 PR을 생성합니다. PR 템플릿을 채워주세요.

## 추가 파일

- 스크린샷, 다이어그램은 `assets/` 디렉토리에 저장
- 보고서 본문에서 상대 경로로 참조: `![screenshot](assets/architecture.png)`
- 상대 경로 이미지는 Notion 동기화 시 GitHub raw URL로 자동 변환되므로, 외부 URL을 직접 쓸 필요 없음

## 주의사항

- frontmatter 검증 CI가 통과해야 merge 가능
- 기여도(`contributions`)는 팀 내 합의 후 작성
- 최종 보고서(`is_final: true`)는 반드시 `status: "완료"`로 작성
