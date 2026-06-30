#!/usr/bin/env python3
"""ProjectDB의 중복 페이지를 정리합니다.

(프로젝트명, 쿼드 조, 보고 회차)가 동일한 페이지를 한 그룹으로 묶고, 각 그룹에서
last_edited_time이 가장 최근인 1개만 남기고 나머지는 archived=true(휴지통)로 보냅니다.
휴지통 항목은 Notion에서 30일 내 복구할 수 있습니다.

기본은 dry-run(아무것도 변경하지 않음). 실제로 archive 하려면 --apply 를 붙입니다.

Usage:
    python scripts/dedupe_notion.py            # dry-run
    python scripts/dedupe_notion.py --apply    # 실제 archive

Environment:
    NOTION_API_KEY          - Notion Internal Integration Token
    NOTION_PROJECT_DB_ID    - 대상 Notion ProjectDB ID
"""

import sys
from collections import defaultdict
from typing import Any, Iterator

from sync_notion import get_database_id, get_notion_client, query_database


def page_group_key(page: dict[str, Any]) -> tuple[str, str, Any]:
    """페이지를 (프로젝트명, 쿼드 조, 보고 회차)로 식별합니다."""
    props = page.get("properties", {})
    title_texts = props.get("프로젝트명", {}).get("title", [])
    project = title_texts[0]["plain_text"] if title_texts else ""
    quad_select = props.get("쿼드 조", {}).get("select")
    quad = quad_select["name"] if quad_select else ""
    number = props.get("보고 회차", {}).get("number")
    return (project, quad, number)


def iter_all_pages(notion: Any, database_id: str) -> Iterator[dict[str, Any]]:
    """ProjectDB의 모든(아카이브되지 않은) 페이지를 순회합니다."""
    cursor: str | None = None
    while True:
        kwargs: dict[str, Any] = {"page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        response = query_database(notion, database_id, **kwargs)
        for page in response.get("results", []):
            yield page
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    notion = get_notion_client()
    database_id = get_database_id()

    groups: dict[tuple[str, str, Any], list[dict[str, Any]]] = defaultdict(list)
    total = 0
    for page in iter_all_pages(notion, database_id):
        total += 1
        groups[page_group_key(page)].append(page)

    print(f"[INFO] 총 {total}개 페이지, {len(groups)}개 그룹")

    archived = 0
    to_archive = 0
    for key in sorted(groups, key=lambda k: (str(k[0]), str(k[1]), k[2] if k[2] is not None else -1)):
        pages = groups[key]
        if len(pages) <= 1:
            continue
        # 가장 최근 편집본을 keep, 나머지 archive
        pages.sort(key=lambda p: p.get("last_edited_time", ""), reverse=True)
        keep, dups = pages[0], pages[1:]
        to_archive += len(dups)
        project, quad, number = key
        print(f"[DUP] {quad} - {project} (회차 {number}): {len(pages)}개 → 1개 유지, {len(dups)}개 archive")
        print(f"        keep   : {keep['id']} (edited {keep.get('last_edited_time')})")
        for dup in dups:
            print(f"        archive: {dup['id']} (edited {dup.get('last_edited_time')})")
            if apply:
                notion.pages.update(page_id=dup["id"], archived=True)
                archived += 1

    if apply:
        print(f"[DONE] {archived}개 페이지 archive 완료")
    else:
        print(f"[DRY-RUN] archive 예정 {to_archive}개. 실제 실행하려면 --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
