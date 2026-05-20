import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_notion.py"
SPEC = importlib.util.spec_from_file_location("project_sync_notion", MODULE_PATH)
sync_notion = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync_notion)


class LegacyDatabases:
    def __init__(self) -> None:
        self.calls = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        return {"results": [{"id": "legacy-page"}]}


class LegacyNotion:
    def __init__(self) -> None:
        self.databases = LegacyDatabases()


class NewDatabases:
    def __init__(self, response) -> None:
        self.response = response
        self.retrieve_calls = []

    def retrieve(self, **kwargs):
        self.retrieve_calls.append(kwargs)
        return self.response


class NewDataSources:
    def __init__(self) -> None:
        self.calls = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        return {"results": [{"id": "new-page"}]}


class NewNotion:
    def __init__(self, response) -> None:
        self.databases = NewDatabases(response)
        self.data_sources = NewDataSources()


class TrackingDatabases:
    def __init__(self, pages_by_name) -> None:
        self.pages_by_name = pages_by_name
        self.calls = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        name = kwargs["filter"]["title"]["equals"]
        pages = self.pages_by_name.get(name)
        if not pages:
            return {"results": []}
        if isinstance(pages, str):
            return {"results": [{"id": pages, "properties": {}}]}
        if isinstance(pages, dict):
            return {"results": [pages]}
        return {"results": pages}


class TrackingPages:
    def __init__(self) -> None:
        self.update_calls = []

    def update(self, **kwargs):
        self.update_calls.append(kwargs)


class TrackingNotion:
    def __init__(self, pages_by_name) -> None:
        self.databases = TrackingDatabases(pages_by_name)
        self.pages = TrackingPages()


def tracking_page(page_id, group=None, group_property="조"):
    properties = {}
    if group:
        properties[group_property] = {
            "type": "select",
            "select": {"name": group},
        }
    return {"id": page_id, "properties": properties}


class QueryDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        sync_notion._DATA_SOURCE_IDS.clear()

    def test_legacy_sdk_uses_databases_query(self) -> None:
        notion = LegacyNotion()

        response = sync_notion.query_database(notion, "db-123", page_size=1)

        self.assertEqual(response["results"][0]["id"], "legacy-page")
        self.assertEqual(
            notion.databases.calls,
            [{"database_id": "db-123", "page_size": 1}],
        )

    def test_new_sdk_uses_data_sources_query(self) -> None:
        notion = NewNotion({"data_sources": [{"id": "ds-123", "name": "Main"}]})

        response = sync_notion.query_database(notion, "db-123", page_size=1)

        self.assertEqual(response["results"][0]["id"], "new-page")
        self.assertEqual(
            notion.databases.retrieve_calls,
            [{"database_id": "db-123"}],
        )
        self.assertEqual(
            notion.data_sources.calls,
            [{"data_source_id": "ds-123", "page_size": 1}],
        )

    def test_new_sdk_caches_resolved_data_source(self) -> None:
        notion = NewNotion({"data_sources": [{"id": "ds-123", "name": "Main"}]})

        sync_notion.query_database(notion, "db-123", page_size=1)
        sync_notion.query_database(notion, "db-123", page_size=2)

        self.assertEqual(len(notion.databases.retrieve_calls), 1)
        self.assertEqual(
            notion.data_sources.calls,
            [
                {"data_source_id": "ds-123", "page_size": 1},
                {"data_source_id": "ds-123", "page_size": 2},
            ],
        )

    def test_new_sdk_requires_data_source_metadata(self) -> None:
        notion = NewNotion({})

        with self.assertRaises(RuntimeError):
            sync_notion.query_database(notion, "db-123", page_size=1)


class CodeLanguageTests(unittest.TestCase):
    def test_known_language_is_preserved(self) -> None:
        self.assertEqual(sync_notion.normalize_code_language("python"), "python")

    def test_text_alias_maps_to_plain_text(self) -> None:
        self.assertEqual(sync_notion.normalize_code_language("text"), "plain text")

    def test_unknown_language_falls_back_to_plain_text(self) -> None:
        self.assertEqual(sync_notion.normalize_code_language("foobar"), "plain text")

    def test_markdown_parser_uses_normalized_language(self) -> None:
        blocks = sync_notion.markdown_to_notion_blocks("```text\nhello\n```")

        self.assertEqual(blocks[0]["type"], "code")
        self.assertEqual(blocks[0]["code"]["language"], "plain text")

    def test_markdown_parser_handles_heading_without_space(self) -> None:
        blocks = sync_notion.markdown_to_notion_blocks("###배운점\n본문")

        self.assertEqual(blocks[0]["type"], "heading_3")
        self.assertEqual(
            blocks[0]["heading_3"]["rich_text"][0]["text"]["content"],
            "배운점",
        )


class FrontmatterParsingTests(unittest.TestCase):
    def test_parse_report_handles_utf8_bom(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bom.md"
            path.write_text(
                "\ufeff---\nproject_name: GhostRelay\nquad_name: 4조\nreport_number: 0\n---\nbody\n",
                encoding="utf-8",
            )

            metadata, content = sync_notion.parse_report(path)

        self.assertEqual(metadata["project_name"], "GhostRelay")
        self.assertEqual(metadata["quad_name"], "4조")
        self.assertEqual(content.strip(), "body")


class TrackingCheckboxTests(unittest.TestCase):
    def test_tracking_name_candidates_include_name_without_student_id(self) -> None:
        self.assertEqual(
            sync_notion.tracking_name_candidates("20252718_김도형"),
            ["20252718_김도형", "김도형"],
        )

    def test_find_tracking_page_falls_back_to_name_without_student_id(self) -> None:
        notion = TrackingNotion({"김도형": "page-kim"})

        page_id = sync_notion.find_tracking_page(
            notion,
            "tracking-db",
            "20252718_김도형",
        )

        self.assertEqual(page_id, "page-kim")
        queried_names = [
            call["filter"]["title"]["equals"]
            for call in notion.databases.calls
        ]
        self.assertEqual(queried_names, ["20252718_김도형", "김도형"])

    def test_find_tracking_page_uses_group_when_duplicate_names_exist(self) -> None:
        notion = TrackingNotion(
            {
                "김도형": [
                    tracking_page("page-team4", "4조"),
                    tracking_page("page-team5", "5조"),
                ],
            }
        )

        page_id = sync_notion.find_tracking_page(
            notion,
            "tracking-db",
            "20252718_김도형",
            "team5",
        )

        self.assertEqual(page_id, "page-team5")

    def test_find_tracking_page_returns_none_for_ambiguous_duplicate_names(self) -> None:
        notion = TrackingNotion(
            {
                "김도형": [
                    tracking_page("page-team4", "4조"),
                    tracking_page("page-team5", "5조"),
                ],
            }
        )

        page_id = sync_notion.find_tracking_page(
            notion,
            "tracking-db",
            "20252718_김도형",
        )

        self.assertIsNone(page_id)

    def test_find_tracking_page_rejects_single_wrong_group_match(self) -> None:
        notion = TrackingNotion({"김도형": tracking_page("page-team4", "4조")})

        page_id = sync_notion.find_tracking_page(
            notion,
            "tracking-db",
            "20252718_김도형",
            "team5",
        )

        self.assertIsNone(page_id)

    def test_update_tracking_checkbox_uses_fallback_tracking_page(self) -> None:
        notion = TrackingNotion(
            {
                "김도형": [
                    tracking_page("page-team4", "4조"),
                    tracking_page("page-team5", "5조"),
                ],
            }
        )

        sync_notion.update_tracking_checkbox(
            notion,
            "tracking-db",
            ["20252718_김도형"],
            2,
            "team5",
        )

        self.assertEqual(
            notion.pages.update_calls,
            [
                {
                    "page_id": "page-team5",
                    "properties": {"PW2": {"checkbox": True}},
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
