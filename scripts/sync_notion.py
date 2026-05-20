#!/usr/bin/env python3
"""프로젝트 보고서를 Notion DB에 동기화하는 스크립트.

변경된 보고서 파일의 frontmatter를 파싱하여 Notion DB에 생성/업데이트합니다.

Usage:
    python scripts/sync_notion.py reports/.../report-01.md [...]

Environment:
    NOTION_API_KEY          - Notion Internal Integration Token
    NOTION_PROJECT_DB_ID    - 대상 Notion ProjectDB ID
    GITHUB_REPOSITORY       - GitHub 레포 (owner/repo 형식, Actions에서 자동 설정)
    GITHUB_SERVER_URL       - GitHub 서버 URL (Actions에서 자동 설정)
"""

import os
import re
import sys
from pathlib import Path
from typing import Any

import frontmatter
from notion_client import Client

_DATA_SOURCE_IDS: dict[str, str] = {}
TRACKING_GROUP_PROPERTY_NAMES = {
    "조", "소속 조", "쿼드 조", "쿼드조", "팀", "팀명", "그룹",
    "team", "team_name", "group", "quad", "quad_name",
}
NOTION_CODE_LANGUAGES = {
    "abap", "abc", "agda", "arduino", "ascii art", "assembly", "bash", "basic",
    "bnf", "c", "c#", "c++", "clojure", "coffeescript", "coq", "css", "dart",
    "dhall", "diff", "docker", "ebnf", "elixir", "elm", "erlang", "f#",
    "flow", "fortran", "gherkin", "glsl", "go", "graphql", "groovy", "haskell",
    "hcl", "html", "idris", "java", "javascript", "json", "julia", "kotlin",
    "latex", "less", "lisp", "livescript", "llvm ir", "lua", "makefile",
    "markdown", "markup", "matlab", "mathematica", "mermaid", "nix",
    "notion formula", "objective-c", "ocaml", "pascal", "perl", "php",
    "plain text", "powershell", "prolog", "protobuf", "purescript", "python",
    "r", "racket", "reason", "ruby", "rust", "sass", "scala", "scheme",
    "scss", "shell", "smalltalk", "solidity", "sql", "swift", "toml",
    "typescript", "vb.net", "verilog", "vhdl", "visual basic", "webassembly",
    "xml", "yaml", "java/c/c++/c#",
}
CODE_LANGUAGE_ALIASES = {
    "plaintext": "plain text",
    "text": "plain text",
    "txt": "plain text",
    "console": "shell",
    "shell script": "shell",
    "sh": "shell",
    "zsh": "shell",
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "yml": "yaml",
}


def get_notion_client() -> Client:
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("Error: NOTION_API_KEY 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    timeout_ms = int(os.environ.get("NOTION_TIMEOUT_MS", "60000"))
    return Client(auth=api_key, timeout_ms=timeout_ms)


def get_database_id() -> str:
    db_id = os.environ.get("NOTION_PROJECT_DB_ID")
    if not db_id:
        print("Error: NOTION_PROJECT_DB_ID 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    return db_id


def build_github_url(filepath: Path) -> str:
    """보고서 파일의 GitHub URL을 생성합니다."""
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        return ""
    return f"{server}/{repo}/blob/main/{filepath}"


def parse_report(filepath: Path) -> tuple[dict, str]:
    """보고서 파일의 frontmatter와 본문을 파싱합니다."""
    post = frontmatter.loads(filepath.read_text(encoding="utf-8-sig"))
    return post.metadata, post.content


def rich_text(content: str) -> list[dict]:
    """Notion rich_text 객체를 생성합니다."""
    if len(content) > 2000:
        content = content[:2000]
    return [{"type": "text", "text": {"content": content}}]


def normalize_code_language(lang: str) -> str:
    """Notion이 허용하는 코드 블록 언어로 정규화합니다."""
    normalized = CODE_LANGUAGE_ALIASES.get(lang.strip().lower(), lang.strip().lower())
    return normalized if normalized in NOTION_CODE_LANGUAGES else "plain text"


def format_contributions(contributions: list[dict]) -> str:
    """contributions 목록을 읽기 쉬운 문자열로 변환합니다."""
    parts = []
    for c in contributions:
        name = c.get("name", "")
        role = c.get("role", "")
        tasks = c.get("tasks", "")
        pct = c.get("percentage", 0)
        parts.append(f"{name}({role}): {tasks} - {pct}%")
    return "\n".join(parts)


def build_raw_image_url(relative_path: str, report_filepath: Path) -> str:
    """상대 경로 이미지를 GitHub raw URL로 변환합니다."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        return ""
    # 보고서 파일 기준 상대 경로를 절대 경로로 변환
    image_path = (report_filepath.parent / relative_path).as_posix()
    # reports/ 이하 경로만 추출
    if "reports/" in image_path:
        idx = image_path.index("reports/")
        image_path = image_path[idx:]
    return f"https://raw.githubusercontent.com/{repo}/main/{image_path}"


def markdown_to_notion_blocks(md: str, report_filepath: Path | None = None) -> list[dict]:
    """마크다운 텍스트를 Notion 블록 리스트로 변환합니다."""
    blocks = []
    lines = md.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # 빈 줄 건너뛰기
        if not line.strip():
            i += 1
            continue

        # 코드 블록
        if line.strip().startswith("```"):
            lang = line.strip().removeprefix("```").strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 닫는 ``` 건너뛰기
            code_content = "\n".join(code_lines)
            if len(code_content) > 2000:
                code_content = code_content[:2000]
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": rich_text(code_content),
                    "language": normalize_code_language(lang),
                },
            })
            continue

        # 제목
        heading_match = re.match(r"^(#{1,3})\s*(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            blocks.append({
                "object": "block",
                "type": f"heading_{level}",
                f"heading_{level}": {"rich_text": rich_text(heading_text)},
            })
            i += 1
            continue

        # 인용문
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": rich_text("\n".join(quote_lines))},
            })
            continue

        # 비순서 목록
        if re.match(r"^[-*] ", line):
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": rich_text(lines[i][2:].strip())},
                })
                i += 1
            continue

        # 순서 목록
        if re.match(r"^\d+\. ", line):
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                text = re.sub(r"^\d+\. ", "", lines[i]).strip()
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {"rich_text": rich_text(text)},
                })
                i += 1
            continue

        # 이미지
        img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if img_match:
            url = img_match.group(2)
            if not url.startswith("http") and report_filepath:
                url = build_raw_image_url(url, report_filepath)
            if url.startswith("http"):
                blocks.append({
                    "object": "block",
                    "type": "image",
                    "image": {"type": "external", "external": {"url": url}},
                })
            i += 1
            continue

        # 구분선
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", line.strip()):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1
            continue

        # 일반 텍스트 (연속된 줄을 하나의 paragraph로)
        para_lines = []
        while i < len(lines) and lines[i].strip() and not any([
            re.match(r"^(#{1,3})\s+.+$", lines[i]),
            lines[i].startswith("> "),
            lines[i].startswith("```"),
            re.match(r"^[-*] ", lines[i]),
            re.match(r"^\d+\. ", lines[i]),
            re.match(r"^(-{3,}|\*{3,}|_{3,})$", lines[i].strip()),
            re.match(r"!\[([^\]]*)\]\(([^)]+)\)", lines[i].strip()),
        ]):
            para_lines.append(lines[i])
            i += 1
        if not para_lines:
            para_lines.append(lines[i])
            i += 1
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text("\n".join(para_lines))},
        })

    # Notion API는 한 번에 최대 100개 블록
    return blocks[:100]


def find_existing_page(
    notion: Client, database_id: str,
    project_name: str, quad_name: str, report_number: int,
) -> str | None:
    """프로젝트명+쿼드조+회차로 기존 Notion 페이지를 검색합니다. 있으면 page_id 반환."""
    response = notion.search(
        query=project_name,
        filter={"value": "page", "property": "object"},
    )
    for page in response.get("results", []):
        if page.get("parent", {}).get("database_id", "").replace("-", "") != database_id.replace("-", ""):
            continue
        props = page.get("properties", {})
        # 프로젝트명(Title) 확인
        title_prop = props.get("프로젝트명", {})
        title_texts = title_prop.get("title", [])
        title = title_texts[0]["plain_text"] if title_texts else ""
        # 쿼드 조(Select) 확인
        quad_prop = props.get("쿼드 조", {})
        quad_select = quad_prop.get("select")
        quad = quad_select["name"] if quad_select else ""
        # 보고 회차(Number) 확인
        number_prop = props.get("보고 회차", {})
        number = number_prop.get("number")
        if title == project_name and quad == quad_name and number == report_number:
            return page["id"]
    return None


def resolve_query_target_id(notion: Client, database_id: str) -> str:
    """Notion DB query에 사용할 식별자를 반환합니다."""
    if hasattr(notion.databases, "query"):
        return database_id

    cached_id = _DATA_SOURCE_IDS.get(database_id)
    if cached_id:
        return cached_id

    database = notion.databases.retrieve(database_id=database_id)
    data_sources = database.get("data_sources") or []
    if not data_sources and database.get("initial_data_source"):
        data_sources = [database["initial_data_source"]]

    for data_source in data_sources:
        data_source_id = data_source.get("id") if isinstance(data_source, dict) else None
        if data_source_id:
            _DATA_SOURCE_IDS[database_id] = data_source_id
            return data_source_id

    raise RuntimeError(
        f"Database {database_id} 에 query 가능한 data source가 없습니다. "
        "Notion API 버전과 데이터베이스 접근 권한을 확인하세요."
    )


def query_database(notion: Client, database_id: str, **kwargs: Any) -> dict[str, Any]:
    """구/신 Notion SDK 모두에서 동작하도록 데이터베이스를 조회합니다."""
    if hasattr(notion.databases, "query"):
        return notion.databases.query(database_id=database_id, **kwargs)
    return notion.data_sources.query(
        data_source_id=resolve_query_target_id(notion, database_id),
        **kwargs,
    )


def tracking_name_candidates(member_name: str) -> list[str]:
    """제출 현황 DB 검색에 사용할 이름 후보를 반환합니다."""
    name = member_name.strip()
    candidates = []

    def add(candidate: str) -> None:
        candidate = candidate.strip()
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    add(name)
    match = re.match(r"^\d{4,}[_\s-]+(.+)$", name)
    if match:
        add(match.group(1))
    elif "_" in name:
        add(name.rsplit("_", 1)[1])

    return candidates


def normalize_tracking_group(value: Any) -> str:
    """조/팀 표기를 비교 가능한 형태로 정규화합니다."""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", "", text)
    text = text.replace("_", "").replace("-", "")

    team_match = re.fullmatch(r"team(\d+)", text)
    if team_match:
        return f"{int(team_match.group(1))}조"

    number_match = re.fullmatch(r"(\d+)조?", text)
    if number_match:
        return f"{int(number_match.group(1))}조"

    alpha_match = re.fullmatch(r"([a-z])조?", text)
    if alpha_match:
        return f"{alpha_match.group(1)}조"

    return text


def notion_property_values(prop: dict[str, Any]) -> list[str]:
    """Notion property에서 비교 가능한 문자열 값을 추출합니다."""
    prop_type = prop.get("type")
    values = []

    if prop_type in {"title", "rich_text"}:
        for item in prop.get(prop_type, []):
            text = item.get("plain_text") or item.get("text", {}).get("content")
            if text:
                values.append(text)
    elif prop_type in {"select", "status"}:
        option = prop.get(prop_type)
        if option and option.get("name"):
            values.append(option["name"])
    elif prop_type == "multi_select":
        values.extend(option["name"] for option in prop.get("multi_select", []))
    elif prop_type == "number" and prop.get("number") is not None:
        values.append(str(prop["number"]))
    elif prop_type == "formula":
        formula = prop.get("formula", {})
        formula_type = formula.get("type")
        if formula_type and formula.get(formula_type) is not None:
            values.append(str(formula[formula_type]))

    return values


def tracking_page_group_values(page: dict[str, Any]) -> list[str]:
    """제출 현황 페이지의 조/팀 속성 값을 반환합니다."""
    values = []
    props = page.get("properties", {})
    for prop_name, prop in props.items():
        if prop_name not in TRACKING_GROUP_PROPERTY_NAMES:
            continue
        values.extend(notion_property_values(prop))
    return values


def tracking_page_matches_group(page: dict[str, Any], quad_name: str) -> bool:
    """제출 현황 페이지가 보고서의 조와 일치하는지 확인합니다."""
    target = normalize_tracking_group(quad_name)
    return any(
        normalize_tracking_group(value) == target
        for value in tracking_page_group_values(page)
    )


def build_properties(metadata: dict, github_url: str) -> dict:
    """frontmatter 메타데이터를 Notion properties로 변환합니다."""
    properties = {
        "프로젝트명": {"title": [{"text": {"content": metadata.get("project_name", "")}}]},
        "쿼드 조": {"select": {"name": metadata.get("quad_name", "")}},
        "조원": {"rich_text": rich_text(", ".join(metadata.get("members", [])))},
        "보고 회차": {"number": metadata.get("report_number", 1)},
        "진행 상태": {"status": {"name": metadata.get("status", "진행 중")}},
        "CL 등급": {"select": {"name": metadata.get("cl_level", "CL1")}},
    }

    # 제출일
    date = metadata.get("date")
    if date:
        properties["제출일"] = {"date": {"start": str(date)}}

    # 최종 보고서 여부
    is_final = metadata.get("is_final", False)
    properties["최종 보고서"] = {"checkbox": bool(is_final)}

    # 기여도
    contributions = metadata.get("contributions")
    if contributions and isinstance(contributions, list):
        contrib_text = format_contributions(contributions)
        properties["기여도"] = {"rich_text": rich_text(contrib_text)}

    # Git 링크
    if github_url:
        properties["Git 링크"] = {"url": github_url}

    return properties


def clear_page_content(notion: Client, page_id: str) -> None:
    """기존 페이지의 블록을 모두 삭제합니다."""
    children = notion.blocks.children.list(block_id=page_id)
    for block in children.get("results", []):
        notion.blocks.delete(block_id=block["id"])


def find_tracking_page(
    notion: Client,
    tracking_db_id: str,
    name: str,
    quad_name: str = "",
) -> str | None:
    """제출 현황 DB에서 이름과 조로 페이지를 검색합니다."""
    for candidate in tracking_name_candidates(name):
        response = query_database(
            notion,
            tracking_db_id,
            filter={"property": "이름", "title": {"equals": candidate}},
            page_size=100,
        )
        results = response.get("results", [])
        if not results:
            continue

        if quad_name:
            group_matches = [
                page for page in results
                if tracking_page_matches_group(page, quad_name)
            ]
            if len(group_matches) == 1:
                return group_matches[0]["id"]
            if len(group_matches) > 1:
                print(f"[TRACK] {name} → {quad_name} 내 동명이인 후보가 여러 명입니다.")
                return None
            if any(tracking_page_group_values(page) for page in results):
                print(f"[TRACK] {name} → {quad_name}에 해당하는 제출 현황 페이지가 없습니다.")
                return None

        if len(results) == 1:
            return results[0]["id"]

        print(f"[TRACK] {name} → 동명이인 후보가 여러 명입니다. 조 정보를 확인하세요.")
        return None
    return None


def update_tracking_checkbox(
    notion: Client,
    tracking_db_id: str,
    names: list[str],
    week: int,
    quad_name: str = "",
) -> None:
    """제출 현황 DB에서 멤버들의 W{week} 체크박스를 True로 업데이트합니다."""
    prop_name = f"PW{week}"
    for name in names:
        page_id = find_tracking_page(notion, tracking_db_id, name, quad_name)
        if page_id:
            notion.pages.update(
                page_id=page_id,
                properties={prop_name: {"checkbox": True}},
            )
            print(f"[TRACK] {name} → {prop_name} ✅")
        else:
            print(f"[TRACK] {name} → 제출 현황 DB에서 찾을 수 없음")


def sync_report(notion: Client, database_id: str, filepath: Path) -> None:
    """단일 보고서를 Notion DB에 동기화합니다."""
    metadata, content = parse_report(filepath)
    project_name = metadata.get("project_name", "")
    quad_name = metadata.get("quad_name", "")
    report_number = metadata.get("report_number", 0)

    if not project_name or not quad_name:
        print(f"[SKIP] {filepath}: project_name 또는 quad_name 누락")
        return

    github_url = build_github_url(filepath)
    properties = build_properties(metadata, github_url)
    blocks = markdown_to_notion_blocks(content, filepath)

    existing_page_id = find_existing_page(
        notion, database_id, project_name, quad_name, report_number,
    )

    if existing_page_id:
        notion.pages.update(page_id=existing_page_id, properties=properties)
        clear_page_content(notion, existing_page_id)
        if blocks:
            notion.blocks.children.append(block_id=existing_page_id, children=blocks)
        print(f"[UPDATE] {quad_name} - {project_name} (회차 {report_number})")
    else:
        notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=blocks,
        )
        print(f"[CREATE] {quad_name} - {project_name} (회차 {report_number})")

    # 제출 현황 DB 체크박스 업데이트
    week_number = os.environ.get("WEEK_NUMBER", "")
    tracking_db_id = os.environ.get("NOTION_TRACKING_DB_ID", "")
    if week_number and tracking_db_id:
        week = int(week_number)
        members = metadata.get("members", [])
        if members:
            update_tracking_checkbox(notion, tracking_db_id, members, week, quad_name)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python sync_notion.py <report_file> [...]")
        return 1

    notion = get_notion_client()
    database_id = get_database_id()

    for filepath_str in sys.argv[1:]:
        filepath = Path(filepath_str)
        if not filepath.exists():
            print(f"[SKIP] {filepath}: 파일 없음")
            continue
        try:
            sync_report(notion, database_id, filepath)
        except Exception as e:
            print(f"[ERROR] {filepath}: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
