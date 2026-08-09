from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_compile():
    failures = []
    for path in (ROOT / "app").rglob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")
    assert not failures, "\n".join(failures)


def test_scan_worker_uses_existing_ingestion_method():
    worker = (ROOT / "app/workers/scan_worker.py").read_text(encoding="utf-8")
    service = (ROOT / "app/services/scan_ingestion_service.py").read_text(encoding="utf-8")
    assert "self.service.process_scan(" in worker
    assert "async def process_scan(" in service


def test_embedding_setting_is_declared():
    config = (ROOT / "app/core/config.py").read_text(encoding="utf-8")
    client = (ROOT / "app/shared/ai/embedding_client.py").read_text(encoding="utf-8")
    assert "AZURE_OPENAI_EMBEDDING_DEPLOYMENT" in client
    assert "AZURE_OPENAI_EMBEDDING_DEPLOYMENT:" in config
