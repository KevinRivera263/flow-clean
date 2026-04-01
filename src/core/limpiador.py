import json
import os
import shutil
import tempfile
import zipfile


def _safe_read_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _safe_write_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _replace_connection_reference(obj, old_ref: str, new_ref: str):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                _replace_connection_reference(value, old_ref, new_ref)
            elif isinstance(value, str) and value == old_ref:
                obj[key] = new_ref
    elif isinstance(obj, list):
        for item in obj:
            _replace_connection_reference(item, old_ref, new_ref)


def _remove_authentication_blocks(obj):
    if isinstance(obj, dict):
        # Si es una acción tipo OpenApiConnection, quitar authentication
        if obj.get("type") == "OpenApiConnection" and "inputs" in obj:
            if isinstance(obj["inputs"], dict) and "authentication" in obj["inputs"]:
                del obj["inputs"]["authentication"]

        for value in obj.values():
            if isinstance(value, (dict, list)):
                _remove_authentication_blocks(value)

    elif isinstance(obj, list):
        for item in obj:
            _remove_authentication_blocks(item)


def _clean_connection_references(definition: dict):
    refs = definition.get("connectionReferences", {})
    if not isinstance(refs, dict):
        return 0

    changes = 0
    new_refs = {}

    for key, value in refs.items():
        new_key = key.replace("shared_sharepointonline-1", "shared_sharepointonline")

        if isinstance(value, dict):
            if value.get("source") == "Invoker":
                value["source"] = "Embedded"
                changes += 1

            api_info = value.get("api", {})
            if isinstance(api_info, dict):
                api_id = api_info.get("id", "")
                if "shared_sharepointonline-1" in api_id:
                    api_info["id"] = api_id.replace(
                        "shared_sharepointonline-1",
                        "shared_sharepointonline"
                    )
                    changes += 1

        new_refs[new_key] = value
        if new_key != key:
            changes += 1

    definition["connectionReferences"] = new_refs
    return changes


def clean_flow_zip(zip_path: str):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"No se encontró el archivo: {zip_path}")

    temp_dir = tempfile.mkdtemp(prefix="flowclean_")
    extract_dir = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    changes_log = []

    # Se obtienen los archivos comunes del paquete legacy
    definition_path = os.path.join(extract_dir, "definition.json")
    apis_map_path = os.path.join(extract_dir, "apisMap.json")
    connections_map_path = os.path.join(extract_dir, "connectionsMap.json")

    definition = _safe_read_json(definition_path)
    if definition:
        _replace_connection_reference(
            definition,
            "shared_sharepointonline-1",
            "shared_sharepointonline"
        )
        changes_log.append("Referencias shared_sharepointonline-1 reemplazadas en definition.json")

        _remove_authentication_blocks(definition)
        changes_log.append("Bloques authentication removidos de acciones OpenApiConnection")

        ref_changes = _clean_connection_references(definition)
        if ref_changes > 0:
            changes_log.append(f"Connection references ajustadas: {ref_changes}")

        _safe_write_json(definition_path, definition)

    apis_map = _safe_read_json(apis_map_path)
    if apis_map:
        _replace_connection_reference(
            apis_map,
            "shared_sharepointonline-1",
            "shared_sharepointonline"
        )
        _safe_write_json(apis_map_path, apis_map)
        changes_log.append("apisMap.json actualizado")

    connections_map = _safe_read_json(connections_map_path)
    if connections_map:
        _replace_connection_reference(
            connections_map,
            "shared_sharepointonline-1",
            "shared_sharepointonline"
        )
        _safe_write_json(connections_map_path, connections_map)
        changes_log.append("connectionsMap.json actualizado")

    base_name = os.path.splitext(os.path.basename(zip_path))[0]
    output_zip = os.path.join(os.path.dirname(zip_path), f"{base_name}_cleaned.zip")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zip_out:
        for root, _, files in os.walk(extract_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, extract_dir)
                zip_out.write(full_path, arcname)

    shutil.rmtree(temp_dir, ignore_errors=True)

    return {
        "success": True,
        "output_zip": output_zip,
        "changes": changes_log
    }