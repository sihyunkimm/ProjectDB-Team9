import importlib.util
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


if __name__ == "__main__":
    unittest.main()
