import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from openpyxl import Workbook

import file_handler


class FileHandlerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.output_dir_patch = patch.object(file_handler, "OUTPUT_DIR", self.temp_path)
        self.output_dir_patch.start()
        self.addCleanup(self.output_dir_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def create_input_workbook(self, headers, rows):
        filepath = self.temp_path / "input.xlsx"
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(headers)
        for row in rows:
            worksheet.append(row)
        workbook.save(filepath)
        workbook.close()
        return filepath

    def create_tournament_state(self, winners=None, current_group_index=0):
        controller = SimpleNamespace(
            filename="films",
            state_filename="Quarti films",
        )
        return SimpleNamespace(
            controller=controller,
            current_girone_index=current_group_index,
            vincitori=winners or [],
        )

    def test_round_name_for_participant_count(self):
        cases = {
            1: "VINCITORE",
            2: "Finale",
            3: "Semifinale",
            8: "Quarti",
            16: "Ottavi",
            32: "Sedicesimi",
            33: "Turno",
        }

        for participant_count, expected_round in cases.items():
            with self.subTest(participant_count=participant_count):
                self.assertEqual( file_handler.round_by_participant_count(participant_count), expected_round )

    def test_generated_workbook_name_keeps_base_tournament_name(self):
        cases = {
            "Quarti films": "films",
            "semifinale_films": "films",
            "films": "films",
        }

        for workbook_stem, expected_name in cases.items():
            with self.subTest(workbook_stem=workbook_stem):
                self.assertEqual( file_handler.get_tournament_name_from_workbook(workbook_stem), expected_name )

    def test_loader_accepts_blank_link_and_builds_google_images_url(self):
        filepath = self.create_input_workbook(
            ["NOME", "LINK", "GIRONE"],
            [["Film One", None, 1]],
        )

        tournament = file_handler.load_file_gironi(filepath)

        self.assertIsNotNone(tournament)
        participant_name, image_search_url = tournament["groups"][1][0]
        self.assertEqual(participant_name, "Film One")
        query = parse_qs(urlparse(image_search_url).query)
        self.assertEqual(query["tbm"], ["isch"])
        self.assertEqual(query["q"], ["Film One"])

    def test_loader_rejects_workbook_missing_required_header(self):
        filepath = self.create_input_workbook(
            ["NOME", "LINK"],
            [["Example", "https://example.com"]],
        )

        self.assertIsNone(file_handler.load_file_gironi(filepath))

    def test_save_and_load_state_uses_active_workbook_name(self):
        winners = [(1, ("Winner", "https://winner.example"))]
        saved_state = self.create_tournament_state(winners, current_group_index=2)

        file_handler.save_stato(saved_state)
        expected_path = self.temp_path / "saved status Quarti films.json"
        self.assertTrue(expected_path.exists())

        restored_state = self.create_tournament_state()
        file_handler.load_stato(restored_state)

        self.assertEqual(restored_state.current_girone_index, 2)
        self.assertEqual(restored_state.vincitori, winners)

    def test_load_state_accepts_legacy_four_value_winners(self):
        state_path = self.temp_path / "saved status Quarti films.json"
        state_path.write_text(
            json.dumps(
                {
                    "current_girone_index": 1,
                    "vincitori": [[1, "Winner", "https://winner.example", 3]],
                }
            ),
            encoding="utf-8",
        )
        tournament = self.create_tournament_state()

        file_handler.load_stato(tournament)

        self.assertEqual(tournament.current_girone_index, 1)
        self.assertEqual(
            tournament.vincitori,
            [(1, ("Winner", "https://winner.example"))],
        )

if __name__ == "__main__":
    unittest.main()
