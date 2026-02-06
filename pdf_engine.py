
import fitz
import json

def edit_pdf(input_path, output_path, edits_json):
    doc = fitz.open(input_path)
    edits = json.loads(edits_json)

    for item in edits:
        page = doc[item["page"]]

        if item["type"] == "add_text":
            page.insert_text(
                (item["x"], item["y"]),
                item["text"],
                fontsize=item.get("size", 16),
            )

        if item["type"] == "replace_text":
            text_instances = page.search_for(item["search"])

            for inst in text_instances:
                page.insert_text(inst.tl, item["replace"], fontsize=12)

        if item["type"] == "highlight":
            rects = page.search_for(item["text"])
            for r in rects:
                page.add_highlight_annot(r)

    doc.save(output_path)
