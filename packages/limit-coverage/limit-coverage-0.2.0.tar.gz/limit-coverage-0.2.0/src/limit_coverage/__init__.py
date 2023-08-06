import collections
import os
import re
import sqlite3
import typing


__version__ = "0.2.0"

FileID = typing.NewType("FileID", int)
ContextID = typing.NewType("ContextID", int)
SourceModule = typing.NewType("SourceModule", str)
TestModule = typing.NewType("TestModule", str)

MODULE_RE = re.compile(r"tests\.((?:\w+\.)*)test_(\w+)")


def modules_under_test(test_module: TestModule) -> typing.Iterator[SourceModule]:
    # TODO: take the pragmas and such
    match = MODULE_RE.fullmatch(test_module)
    if match:
        yield SourceModule("".join(match.groups()))


def get_module_contexts(
    c: sqlite3.Cursor
) -> typing.Tuple[typing.Mapping[TestModule, typing.Set[ContextID]], ContextID]:

    module_contexts: typing.MutableMapping[
        TestModule, typing.Set[ContextID]
    ] = collections.defaultdict(set)

    for id_, context in c.execute("SELECT id, context FROM context;"):
        if context == "":
            empty_context = ContextID(id_)
        else:
            module_contexts[TestModule(context.rsplit(".", 1)[0])].add(ContextID(id_))

    for context_set in module_contexts.values():
        context_set.add(empty_context)

    return module_contexts, empty_context


def get_contexts_for_module(
    module_contexts: typing.Mapping[TestModule, typing.Set[ContextID]],
    empty_context: ContextID,
) -> typing.Mapping[SourceModule, typing.Set[ContextID]]:

    contexts_for_module: typing.MutableMapping[
        SourceModule, typing.Set[ContextID]
    ] = collections.defaultdict(lambda: {empty_context})

    for test_module, contexts in module_contexts.items():
        for module in modules_under_test(test_module):
            contexts_for_module[module].update(contexts)

    return contexts_for_module


def get_cursor() -> sqlite3.Cursor:
    return sqlite3.connect(".coverage").cursor()


def get_rows_to_drop_arc(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> typing.List[int]:

    rows_to_drop: typing.List[int] = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM arc;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append(rowid)

    return rows_to_drop


def delete_arcs(c: sqlite3.Cursor, rows_to_drop: typing.List[int]):

    for rowid in rows_to_drop:
        c.execute("DELETE FROM arc WHERE rowid=?", (rowid,))


def get_rows_to_drop_lines(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> typing.List[int]:

    rows_to_drop: typing.List[int] = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM line_map;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append(rowid)

    return rows_to_drop


def delete_lines(c: sqlite3.Cursor, rows_to_drop: typing.List[int]):

    for rowid in rows_to_drop:
        c.execute("DELETE FROM line_map WHERE rowid=?", (rowid,))


def get_rows_to_drop_line_bits(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> typing.List[int]:

    rows_to_drop: typing.List[int] = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM line_bits;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append(rowid)

    return rows_to_drop


def delete_line_bits(c: sqlite3.Cursor, rows_to_drop: typing.List[int]):

    for rowid in rows_to_drop:
        c.execute("DELETE FROM line_bits WHERE rowid=?", (rowid,))


def get_whitelisted_ids(
    c: sqlite3.Cursor,
    contexts_for_module: typing.Mapping[SourceModule, typing.Set[ContextID]],
) -> typing.Mapping[FileID, typing.Set[ContextID]]:

    cwd = os.getcwd()
    source_root = os.path.join(cwd, "src") if os.path.isdir("src") else cwd

    pardir = os.pardir + os.sep
    tests = "tests" + os.sep

    whitelisted_ids: typing.MutableMapping[FileID, typing.Set[ContextID]] = {}

    for id_, path in c.execute("SELECT id, path FROM file;"):
        relpath = os.path.relpath(path, source_root)
        if relpath.startswith((pardir, tests)):
            continue
        directory, file_ = os.path.split(os.path.splitext(relpath)[0])
        names = directory.split(os.sep)
        if file_ != "__init__":
            names.append(file_)
        whitelisted_ids[FileID(id_)] = contexts_for_module[
            SourceModule(".".join(names))
        ]

    return whitelisted_ids


def _common(c):
    return get_whitelisted_ids(c, get_contexts_for_module(*get_module_contexts(c)))


def line_schema_3(c):
    delete_lines(c, get_rows_to_drop_lines(c, _common(c)))


def line_schema_7(c):
    delete_line_bits(c, get_rows_to_drop_line_bits(c, _common(c)))


SCHEMATA_LINE = {3: line_schema_3, 7: line_schema_7}


def arc_schema_3_and_7(c):

    delete_arcs(c, get_rows_to_drop_arc(c, _common(c)))


SCHEMATA_ARC = {3: arc_schema_3_and_7, 7: arc_schema_3_and_7}


def meta_schema_3(c):
    return c.execute("SELECT has_arcs FROM meta;").fetchone()[0]


def meta_schema_7(c):
    return c.execute("SELECT value FROM meta WHERE key='has_arcs';").fetchone()[0]


def get_schema(c):
    return c.execute("SELECT version FROM coverage_schema;").fetchone()[0]


SCHEMATA_META = {3: meta_schema_3, 7: meta_schema_7}


def main():

    c = get_cursor()
    schema = get_schema(c)

    if SCHEMATA_META[schema](c):

        SCHEMATA_ARC[schema](c)

    else:

        SCHEMATA_LINE[schema](c)

    c.connection.commit()
    c.connection.close()
