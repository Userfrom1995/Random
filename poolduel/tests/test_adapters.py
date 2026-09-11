import tempfile
import unittest

from poolduel.harness.adapters import (DirectAdapter, OdysseyAdapter,
                                       PgAgroalAdapter, PgBouncerAdapter,
                                       PgCatAdapter, PgPoolAdapter)
from poolduel.harness.cells import get_cell


class AdapterTest(unittest.TestCase):
    def test_ports_distinct_and_direct_is_pg(self):
        ports = {PgAgroalAdapter().port, PgBouncerAdapter().port,
                 PgPoolAdapter().port, OdysseyAdapter().port,
                 PgCatAdapter().port, DirectAdapter().port}
        self.assertEqual(len(ports), 6)
        self.assertEqual(DirectAdapter().port, 5432)

    def test_config_text_per_cell_pool_size(self):
        cell = get_cell("M1-5")
        self.assertEqual(cell["pool_size"], 20)
        text = PgBouncerAdapter().config_text(cell)
        self.assertIn("default_pool_size = 20", text)
        self.assertIn("pool_mode = transaction", text)
        text = PgAgroalAdapter().config_text(cell)
        self.assertIn("max_connections = 20", text)
        self.assertIn("pipeline = transaction", text)

    def test_prepared_twin_mapping(self):
        cell = get_cell("M1-3")
        text = PgBouncerAdapter().config_text(cell)
        self.assertIn("max_prepared_statements = 200", text)
        simple = get_cell("M1-2")
        text = PgBouncerAdapter().config_text(simple)
        self.assertIn("max_prepared_statements = 0", text)

    def test_pgpool_children_and_no_forbidden_corner(self):
        heavy = get_cell("M1-4")
        ad = PgPoolAdapter()
        self.assertEqual(ad.num_children(heavy), 200)
        self.assertEqual(ad.max_pool(heavy), 1)
        self.assertLessEqual(ad.effective_backends(heavy), 300)
        text = ad.config_text(heavy)
        self.assertIn("num_init_children = 200", text)

    def test_setup_writes_files(self):
        cell = get_cell("M1-2")
        with tempfile.TemporaryDirectory() as tmp:
            for ad in (PgAgroalAdapter(), PgBouncerAdapter(),
                       PgPoolAdapter(), OdysseyAdapter(), PgCatAdapter()):
                work = tmp + "/" + ad.NAME
                ad.setup(work, cell)
                cfg = ad.config_text(cell)
                self.assertTrue(cfg)

    def test_no_adapter_timeout_attributes(self):
        # Adapters must not own warmup/retry/timeout knobs.
        for cls in (PgAgroalAdapter, PgBouncerAdapter, PgPoolAdapter,
                    OdysseyAdapter, PgCatAdapter):
            for attr in ("timeout", "warmup", "retries", "retry"):
                self.assertNotIn(attr, cls.__dict__)


if __name__ == "__main__":
    unittest.main()
