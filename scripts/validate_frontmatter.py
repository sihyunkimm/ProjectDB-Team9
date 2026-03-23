#!/usr/bin/env python3
"""프로젝트 보고서 frontmatter 검증 스크립트.

reports/ 디렉토리 내 모든 report-*.md 파일의 YAML frontmatter를 검증합니다.
특정 파일만 검증하려면 인자로 경로를 전달하세요.

Usage:
    python scripts/validate_frontmatter.py                              # 전체 검증
    python scripts/validate_frontmatter.py reports/.../report-01.md     # 특정 파일 검증
"""

import re
import sys
from pathlib import Path

import frontmatter

REQUIRED_FIELDS = [
    "project_name", "quad_name", "members", "report_number",
    "date", "status", "cl_level", "contributions",
]
VALID_STATUSES = {"시작 전", "진행 중", "보류", "완료"}
VALID_CL_LEVELS = {"CL1", "CL2", "CL3", "CL4"}
CONTRIBUTION_REQUIRED_KEYS = {"name", "role", "tasks", "percentage"}


def validate_file(filepath: Path) -> list[str]:
    """단일 보고서 파일의 frontmatter를 검증하고 에러 목록을 반환합니다."""
    errors = []

    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        return [f"frontmatter 파싱 실패: {e}"]

    metadata = post.metadata

    # 필수 필드 검사
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            errors.append(f"필수 필드 누락: '{field}'")

    # status 유효값 검사
    status = metadata.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"유효하지 않은 status: '{status}' (허용: {', '.join(sorted(VALID_STATUSES))})"
        )

    # cl_level 유효값 검사
    cl_level = metadata.get("cl_level")
    if cl_level and cl_level not in VALID_CL_LEVELS:
        errors.append(
            f"유효하지 않은 cl_level: '{cl_level}' (허용: {', '.join(sorted(VALID_CL_LEVELS))})"
        )

    # members 타입 검사
    members = metadata.get("members")
    if members is not None and not isinstance(members, list):
        errors.append(f"'members' 필드는 리스트여야 합니다 (현재: {type(members).__name__})")

    # report_number 타입 및 범위 검사
    report_number = metadata.get("report_number")
    if report_number is not None:
        if not isinstance(report_number, int):
            errors.append(f"'report_number' 필드는 정수여야 합니다 (현재: {type(report_number).__name__})")
        elif not (0 <= report_number <= 8):
            errors.append(f"'report_number'는 1~8 범위여야 합니다 (현재: {report_number})")

    # date 타입 검사
    date = metadata.get("date")
    if date is not None and not isinstance(date, str):
        errors.append(f"'date' 필드는 문자열이어야 합니다 (현재: {type(date).__name__})")

    # contributions 검증
    contributions = metadata.get("contributions")
    if contributions is not None:
        if not isinstance(contributions, list):
            errors.append(f"'contributions' 필드는 리스트여야 합니다 (현재: {type(contributions).__name__})")
        else:
            total_percentage = 0
            contribution_names = []

            for i, contrib in enumerate(contributions):
                if not isinstance(contrib, dict):
                    errors.append(f"contributions[{i}]는 딕셔너리여야 합니다")
                    continue

                # 필수 키 검사
                for key in CONTRIBUTION_REQUIRED_KEYS:
                    if key not in contrib:
                        errors.append(f"contributions[{i}]에 필수 키 누락: '{key}'")

                # percentage 검사
                pct = contrib.get("percentage")
                if pct is not None:
                    if not isinstance(pct, (int, float)):
                        errors.append(
                            f"contributions[{i}]의 'percentage'는 숫자여야 합니다 (현재: {type(pct).__name__})"
                        )
                    elif not (0 <= pct <= 100):
                        errors.append(
                            f"contributions[{i}]의 'percentage'는 0~100 범위여야 합니다 (현재: {pct})"
                        )
                    else:
                        total_percentage += pct

                # tasks 빈 문자열 검사
                tasks = contrib.get("tasks")
                if tasks is not None and isinstance(tasks, str) and tasks.strip() == "":
                    errors.append(
                        f"contributions[{i}]의 'tasks'가 비어 있습니다 (구체적 작업 내용 필수)"
                    )

                # name 수집
                name = contrib.get("name")
                if name is not None:
                    contribution_names.append(name)

            # 기여도 합계 검사
            if total_percentage != 100:
                errors.append(
                    f"contributions의 percentage 합계가 100이어야 합니다 (현재: {total_percentage})"
                )

            # members와 contributions의 name 일치 검사
            if isinstance(members, list):
                members_set = set(members)
                contrib_set = set(contribution_names)
                missing_in_contrib = members_set - contrib_set
                extra_in_contrib = contrib_set - members_set
                if missing_in_contrib:
                    errors.append(
                        f"contributions에 누락된 팀원: {', '.join(sorted(missing_in_contrib))}"
                    )
                if extra_in_contrib:
                    errors.append(
                        f"contributions에 members에 없는 이름: {', '.join(sorted(extra_in_contrib))}"
                    )

    # 최종 보고서 검증 (is_final: true)
    is_final = metadata.get("is_final")
    if is_final:
        if status and status != "완료":
            errors.append(
                f"최종 보고서(is_final: true)의 status는 '완료'여야 합니다 (현재: '{status}')"
            )

    # 경로 검증: reports/{YYYY}/{조명}/{프로젝트명}/report-XX.md
    parts = filepath.parts
    try:
        reports_idx = list(parts).index("reports")
        remaining = parts[reports_idx:]
        # reports / YYYY / 조명 / 프로젝트명 / report-XX.md
        if len(remaining) < 5:
            errors.append(
                f"경로가 'reports/{{YYYY}}/{{조명}}/{{프로젝트명}}/report-XX.md' 패턴이어야 합니다"
            )
        else:
            year = remaining[1]
            filename = remaining[-1]
            if not re.match(r"^\d{4}$", year):
                errors.append(f"경로의 연도가 올바르지 않습니다: '{year}'")
            if not re.match(r"^report-\d{2}\.md$", filename):
                errors.append(f"파일명이 'report-XX.md' 패턴이어야 합니다 (현재: '{filename}')")
    except ValueError:
        pass  # reports 디렉토리 외부 파일은 경로 검증 건너뜀

    return errors


def find_report_files(paths: list[str] | None = None) -> list[Path]:
    """검증할 보고서 파일 목록을 반환합니다."""
    if paths:
        return [Path(p) for p in paths if Path(p).suffix == ".md"]

    repo_root = Path(__file__).resolve().parent.parent
    reports_dir = repo_root / "reports"
    if not reports_dir.exists():
        return []
    return list(reports_dir.rglob("report-*.md"))


def main() -> int:
    files = find_report_files(sys.argv[1:] if len(sys.argv) > 1 else None)

    if not files:
        print("검증할 보고서 파일이 없습니다.")
        return 0

    has_errors = False

    for filepath in files:
        errors = validate_file(filepath)
        if errors:
            has_errors = True
            print(f"\n[FAIL] {filepath}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[PASS] {filepath}")

    if has_errors:
        print("\n검증 실패: 위 오류를 수정해주세요.")
        return 1

    print(f"\n전체 {len(files)}개 파일 검증 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
