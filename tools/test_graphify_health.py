import json
from pathlib import Path
import re
import unittest

from graphify.diagnostics import diagnose_extraction
from graphify.rcfile import load_graphifyrc


ROOT = Path(__file__).resolve().parent.parent
GRAPHIFY_OUT = ROOT / "graphify-out"
GRAPH_JSON = GRAPHIFY_OUT / "graph.json"
EXTRACT_JSON = GRAPHIFY_OUT / ".graphify_extract.json"
LABELS_JSON = GRAPHIFY_OUT / ".graphify_labels.json"
REPORT_MD = GRAPHIFY_OUT / "GRAPH_REPORT.md"

FORBIDDEN_PATH_FRAGMENTS = (
    ".playwright-mcp",
    "test-results",
    "playwright-report",
)

RAW_TOKEN_LABELS = {
    "with",
    "updates",
    "jobs",
    "steps",
    "on",
    "name",
    "Review Focus",
}


class GraphifyHealthTests(unittest.TestCase):
    def test_graphify_config_files_exist_and_are_valid(self) -> None:
        ignore_path = ROOT / ".graphifyignore"
        rc_path = ROOT / ".graphifyrc"
        self.assertTrue(ignore_path.is_file(), ".graphifyignore deve existir na raiz")
        self.assertTrue(rc_path.is_file(), ".graphifyrc deve existir na raiz")

        ignore_text = ignore_path.read_text(encoding="utf-8")
        for pattern in (".playwright-mcp/", "test-results/", "404.html"):
            self.assertIn(pattern, ignore_text)

        rc = load_graphifyrc(ROOT)
        self.assertGreaterEqual(rc.get("query_budget", 0), 2000)
        self.assertGreaterEqual(rc.get("query_depth", 0), 2)
        self.assertGreaterEqual(rc.get("viz_node_limit", 0), 500)

    def test_graph_json_integrity_and_clean_corpus(self) -> None:
        self.assertTrue(GRAPH_JSON.is_file(), "graphify-out/graph.json deve existir")
        data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        nodes = data.get("nodes", [])
        links = data.get("links", [])
        self.assertGreater(len(nodes), 200, "O grafo deve conter código e documentação")
        self.assertGreater(len(links), 300, "O grafo deve conter arestas suficientes")

        node_ids = {n["id"] for n in nodes}
        self.assertEqual(len(node_ids), len(nodes), "IDs de nós não devem duplicar")

        for node in nodes:
            src = (node.get("source_file") or "").replace("\\", "/")
            for forbidden in FORBIDDEN_PATH_FRAGMENTS:
                self.assertNotIn(
                    forbidden,
                    src,
                    f"Nó {node['id']} referencia diretório temporário proibido: {src}",
                )
            self.assertNotEqual(
                src,
                "404.html",
                "A cópia legada 404.html na raiz deve ser ignorada em favor de frontend/404.html",
            )

        for edge in links:
            self.assertIn(edge["source"], node_ids, f"Origem órfã: {edge['source']}")
            self.assertIn(edge["target"], node_ids, f"Destino órfão: {edge['target']}")
            self.assertNotEqual(
                edge["source"],
                edge["target"],
                f"Auto-loop detectado em {edge['source']}",
            )

    def test_frontend_html_pages_and_hyperedges_are_represented(self) -> None:
        data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        sources = {
            (n.get("source_file") or "").replace("\\", "/")
            for n in data.get("nodes", [])
        }
        expected_pages = (
            "frontend/index.html",
            "frontend/pages/servicos.html",
            "frontend/pages/contato.html",
            "frontend/pages/projetos.html",
            "frontend/pages/sobre.html",
            "frontend/pages/fundador.html",
            "frontend/pages/blog.html",
        )
        for page in expected_pages:
            self.assertIn(page, sources, f"Página HTML ausente do grafo: {page}")

        hyperedges = data.get("hyperedges", [])
        self.assertGreaterEqual(
            len(hyperedges),
            3,
            "O grafo deve preservar hiperarestas semânticas das jornadas do site",
        )

    def test_community_labels_are_curated_in_portuguese(self) -> None:
        self.assertTrue(LABELS_JSON.is_file(), ".graphify_labels.json deve existir")
        labels = json.loads(LABELS_JSON.read_text(encoding="utf-8"))
        self.assertGreater(len(labels), 5)

        placeholder_re = re.compile(r"^Community\s+\d+$", re.IGNORECASE)
        for cid, name in labels.items():
            self.assertFalse(
                placeholder_re.match(name),
                f"Comunidade {cid} usa placeholder não curado: {name}",
            )
            self.assertNotIn(
                name,
                RAW_TOKEN_LABELS,
                f"Comunidade {cid} usa identificador cru em vez de rótulo descritivo: {name}",
            )

        data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            cname = node.get("community_name") or ""
            self.assertTrue(cname, f"Nó {node['id']} sem community_name")
            self.assertFalse(
                placeholder_re.match(cname),
                f"Nó {node['id']} tem community_name placeholder: {cname}",
            )
            self.assertNotIn(
                cname,
                RAW_TOKEN_LABELS,
                f"Nó {node['id']} tem community_name cru: {cname}",
            )

    def test_post_build_diagnostics_report_zero_corrupt_edges(self) -> None:
        data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        summary = diagnose_extraction(data, directed=False, root=str(ROOT))
        self.assertEqual(summary.get("dangling_endpoint_edges", 0), 0)
        self.assertEqual(summary.get("missing_endpoint_edges", 0), 0)
        self.assertEqual(summary.get("self_loop_edges", 0), 0)
        self.assertEqual(summary.get("exact_duplicate_edges", 0), 0)


if __name__ == "__main__":
    unittest.main()
