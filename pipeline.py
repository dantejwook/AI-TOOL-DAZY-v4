from pathlib import Path
import zipfile, os
from core.expand import expand_document
from core.embedding import embed_texts
from core.clustering import cluster

def run_pipeline(
    files,
    use_expand=True,
    make_zip=True,
    output_dir="output_docs",
    log_cb=None,
    progress_cb=None,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    expanded = [
        expand_document(f) if use_expand else {"embedding_text": f.name}
        for f in files
    ]

    vectors = embed_texts([e["embedding_text"] for e in expanded])
    labels = cluster(vectors)

    clusters = {}
    for f, l in zip(files, labels):
        clusters.setdefault(l, []).append(f)

    for i, (label, group_files) in enumerate(clusters.items(), 1):
        group_dir = output_dir / f"group_{label}"
        group_dir.mkdir(exist_ok=True)
        for f in group_files:
            (group_dir / f.name).write_bytes(f.getvalue())
        if progress_cb:
            progress_cb(int(i / len(clusters) * 100))

    if not make_zip:
        return None

    zip_path = output_dir.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for root, _, fs in os.walk(output_dir):
            for f in fs:
                p = Path(root) / f
                z.write(p, arcname=p.relative_to(output_dir))
    return zip_path
