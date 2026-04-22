"""
Export all Pydantic BaseModel classes and Python Enums from a package to a single markdown file.

Usage:
    python export_pydantic_schemas.py <package_name> [output_file]

Examples:
    python export_pydantic_schemas.py my_package
    python export_pydantic_schemas.py my_package docs/models.md
"""

import sys
import importlib
import inspect
import pkgutil
from enum import Enum
from types import ModuleType

try:
    from pydantic import BaseModel
except ImportError:
    print("Error: pydantic is not installed.")
    sys.exit(1)


def _type_str(field_schema: dict, all_defs: dict) -> str:
    """Resolve a field schema to a raw type string (no backticks)."""
    # Handle $ref
    if "$ref" in field_schema:
        return field_schema["$ref"].split("/")[-1]

    # Handle anyOf / oneOf (e.g. Optional[X] becomes anyOf: [X, null])
    for key in ("anyOf", "oneOf"):
        if key in field_schema:
            parts = []
            has_null = False
            for sub in field_schema[key]:
                if sub.get("type") == "null":
                    has_null = True
                else:
                    parts.append(_type_str(sub, all_defs))
            if has_null:
                parts.append("None")
            if len(parts) == 1:
                return parts[0]
            return f"Union[{', '.join(parts)}]"

    # Handle allOf (usually a single $ref wrapped)
    if "allOf" in field_schema:
        parts = [_type_str(s, all_defs) for s in field_schema["allOf"]]
        return f"Union[{', '.join(parts)}]" if len(parts) > 1 else parts[0]

    # Handle arrays
    if field_schema.get("type") == "array":
        items = field_schema.get("items", {})
        return f"list[{_type_str(items, all_defs)}]"

    # Handle basic types
    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "null": "None",
        "object": "dict",
    }
    t = field_schema.get("type")
    if t:
        return type_map.get(t, t)

    # Handle enums (inline literal values, comma-separated to avoid pipes)
    if "enum" in field_schema:
        return ", ".join(f"'{v}'" for v in field_schema["enum"])

    return "any"


def get_type_string(field_schema: dict, all_defs: dict) -> str:
    """Resolve a field schema to a backtick-wrapped type string for markdown."""
    return f"`{_type_str(field_schema, all_defs)}`"


def get_constraints(field_schema: dict) -> str:
    """Extract validation constraints into a readable string."""
    constraint_keys = {
        "minimum": "min",
        "maximum": "max",
        "exclusiveMinimum": "exclusive min",
        "exclusiveMaximum": "exclusive max",
        "minLength": "min length",
        "maxLength": "max length",
        "minItems": "min items",
        "maxItems": "max items",
        "pattern": "pattern",
        "multipleOf": "multiple of",
    }
    parts = []
    for key, label in constraint_keys.items():
        if key in field_schema:
            parts.append(f"{label}={field_schema[key]}")
    return ", ".join(parts)


def enum_to_markdown(enum_cls: type) -> str:
    """Render a single Enum class as a markdown section."""
    import_stmt = f"from {enum_cls.__module__} import {enum_cls.__name__}"
    module_path = f"{enum_cls.__module__}.{enum_cls.__qualname__}"

    lines = []
    lines.append(f"## {enum_cls.__name__}")
    lines.append(f"**Import:** `{import_stmt}`  ")
    lines.append(f"**Module:** `{module_path}`")
    lines.append("")

    class_doc = inspect.getdoc(enum_cls) or ""
    if class_doc:
        lines.append(class_doc)
        lines.append("")

    lines.append("| Member | Value | Description |")
    lines.append("|--------|-------|-------------|")
    for member in enum_cls:
        member_doc = inspect.getdoc(member) or ""
        if member_doc == class_doc:
            member_doc = ""
        lines.append(f"| `{member.name}` | `{member.value!r}` | {member_doc} |")

    lines.append("")
    return "\n".join(lines)


def model_to_markdown(model: type, all_defs: dict) -> str:
    """Render a single Pydantic model as a markdown section."""
    schema = model.model_json_schema()
    module_path = f"{model.__module__}.{model.__qualname__}"
    import_stmt = f"from {model.__module__} import {model.__name__}"

    lines = []
    lines.append(f"## {model.__name__}")
    lines.append(f"**Import:** `{import_stmt}`  ")
    lines.append(f"**Module:** `{module_path}`")
    lines.append("")

    description = schema.get("description", "").strip()
    if description:
        lines.append(description)
        lines.append("")

    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))
    local_defs = schema.get("$defs", {})
    merged_defs = {**all_defs, **local_defs}

    if properties:
        lines.append("| Field | Type | Required | Default | Constraints | Description |")
        lines.append("|-------|------|----------|---------|-------------|-------------|")

        for field_name, field_info in properties.items():
            type_str = get_type_string(field_info, merged_defs)
            required = "yes" if field_name in required_fields else "no"

            default = ""
            if "default" in field_info:
                default = f"`{field_info['default']}`"

            constraints = get_constraints(field_info)
            description = field_info.get("description", "").replace("|", "\\|")

            lines.append(
                f"| `{field_name}` | {type_str} | {required} | {default} | {constraints} | {description} |"
            )
    else:
        lines.append("*No fields defined.*")

    lines.append("")
    return "\n".join(lines)


def discover_models_and_enums(package_name: str) -> tuple[list[tuple[str, type]], list[tuple[str, type]]]:
    """Walk a package and return all Pydantic BaseModel subclasses and Enum subclasses."""
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        print(f"Error: Could not import package '{package_name}': {e}")
        sys.exit(1)

    found_models: dict[str, type] = {}
    found_enums: dict[str, type] = {}

    def walk_module(module: ModuleType):
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if not obj.__module__.startswith(package_name):
                continue
            key = f"{obj.__module__}.{obj.__qualname__}"
            if issubclass(obj, BaseModel) and obj is not BaseModel:
                found_models[key] = obj
            elif issubclass(obj, Enum) and obj is not Enum:
                found_enums[key] = obj

    def walk_package(pkg):
        walk_module(pkg)
        pkg_path = getattr(pkg, "__path__", None)
        if pkg_path is None:
            return
        for _, module_name, is_pkg in pkgutil.walk_packages(
            pkg_path, prefix=pkg.__name__ + "."
        ):
            try:
                mod = importlib.import_module(module_name)
                walk_module(mod)
                if is_pkg:
                    walk_package(mod)
            except Exception as e:
                print(f"  Warning: Could not import {module_name}: {e}", file=sys.stderr)

    walk_package(package)

    models = sorted(found_models.items(), key=lambda x: x[0])
    enums = sorted(found_enums.items(), key=lambda x: x[0])
    return models, enums


def build_shared_defs(models: list[type]) -> dict:
    """Collect all $defs across models to help resolve cross-model references."""
    all_defs = {}
    for model in models:
        schema = model.model_json_schema()
        all_defs.update(schema.get("$defs", {}))
    return all_defs


def export_markdown(package_name: str, output_path: str):
    print(f"Discovering Pydantic models and Enums in '{package_name}'...")
    discovered_models, discovered_enums = discover_models_and_enums(package_name)

    if not discovered_models and not discovered_enums:
        print("No Pydantic BaseModel subclasses or Enums found.")
        sys.exit(0)

    models = [cls for _, cls in discovered_models]
    print(f"Found {len(models)} model(s), {len(discovered_enums)} enum(s).")

    all_defs = build_shared_defs(models)

    lines = []
    lines.append(f"# Pydantic Models and Enums — `{package_name}`")
    lines.append("")
    lines.append(
        f"Auto-generated from `{package_name}`. "
        "Re-run `export_pydantic_schemas.py` after package updates."
    )
    lines.append("")

    if discovered_enums:
        lines.append("# Enums")
        lines.append("")
        for _, cls in discovered_enums:
            lines.append(enum_to_markdown(cls))
            lines.append("---")
            lines.append("")

    if discovered_models:
        lines.append("# Pydantic Models")
        lines.append("")
        for _, cls in discovered_models:
            lines.append(model_to_markdown(cls, all_defs))
            lines.append("---")
            lines.append("")

    output = "\n".join(lines)

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Written to '{output_path}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    package_name = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "models.md"

    export_markdown(package_name, output_path)