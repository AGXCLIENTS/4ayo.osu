from __future__ import annotations

import textwrap
from typing import Any
from typing import cast
from typing import TypedDict

import app.state.services
from app._typing import _UnsetSentinel
from app._typing import UNSET

# +--------------+-----------------+------+-----+---------+----------------+
# | Field        | Type            | Null | Key | Default | Extra          |
# +--------------+-----------------+------+-----+---------+----------------+
# | id           | int             | NO   | PRI | NULL    | auto_increment |
# | mode         | tinyint(1)      | NO   | PRI | NULL    |                |
# | tscore       | bigint unsigned | NO   |     | 0       |                |
# | rscore       | bigint unsigned | NO   |     | 0       |                |
# | pp           | int unsigned    | NO   |     | 0       |                |
# | plays        | int unsigned    | NO   |     | 0       |                |
# | playtime     | int unsigned    | NO   |     | 0       |                |
# | acc          | float(6,3)      | NO   |     | 0.000   |                |
# | max_combo    | int unsigned    | NO   |     | 0       |                |
# | total_hits   | int unsigned    | NO   |     | 0       |                |
# | replay_views | int unsigned    | NO   |     | 0       |                |
# | xh_count     | int unsigned    | NO   |     | 0       |                |
# | x_count      | int unsigned    | NO   |     | 0       |                |
# | sh_count     | int unsigned    | NO   |     | 0       |                |
# | s_count      | int unsigned    | NO   |     | 0       |                |
# | a_count      | int unsigned    | NO   |     | 0       |                |
# +--------------+-----------------+------+-----+---------+----------------+

READ_PARAMS = textwrap.dedent(
    """\
        id, mode, tscore, rscore, pp, plays, playtime, acc, max_combo, total_hits,
        replay_views, xh_count, x_count, sh_count, s_count, a_count
    """,
)


class Stat(TypedDict):
    id: int
    mode: int
    tscore: int
    rscore: int
    pp: int
    plays: int
    playtime: int
    acc: float
    max_combo: int
    total_hits: int
    replay_views: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int


class StatUpdateFields(TypedDict, total=False):
    tscore: int
    rscore: int
    pp: int
    plays: int
    playtime: int
    acc: float
    max_combo: int
    total_hits: int
    replay_views: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int


async def create(
    player_id: int,
    mode: int,
    # TODO: should we allow init with values?
) -> Stat:
    """Create a new player stats entry in the database."""
    query = f"""\
        INSERT INTO stats (id, mode)
        VALUES (:id, :mode)
    """
    params: dict[str, Any] = {
        "id": player_id,
        "mode": mode,
    }
    rec_id = await app.state.services.database.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
    """
    params = {
        "id": rec_id,
    }
    stat = await app.state.services.database.fetch_one(query, params)

    assert stat is not None
    return cast(Stat, dict(stat._mapping))


async def create_all_modes(player_id: int) -> list[Stat]:
    """Create new player stats entries for each game mode in the database."""
    query = f"""\
        INSERT INTO stats (id, mode)
             VALUES (:id, :mode)
    """
    params_list = [
        {"id": player_id, "mode": mode}
        for mode in (
            0,  # vn!std
            1,  # vn!taiko
            2,  # vn!catch
            3,  # vn!mania
            4,  # rx!std
            5,  # rx!taiko
            6,  # rx!catch
            8,  # ap!std
        )
    ]
    await app.state.services.database.execute_many(query, params_list)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
    """
    params: dict[str, Any] = {
        "id": player_id,
    }
    stats = await app.state.services.database.fetch_all(query, params)
    return cast(list[Stat], [dict(s._mapping) for s in stats])


async def fetch_one(player_id: int, mode: int) -> Stat | None:
    """Fetch a player stats entry from the database."""
    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
           AND mode = :mode
    """
    params: dict[str, Any] = {
        "id": player_id,
        "mode": mode,
    }
    stat = await app.state.services.database.fetch_one(query, params)

    return cast(Stat, dict(stat._mapping)) if stat is not None else None


async def fetch_count(
    player_id: int | None = None,
    mode: int | None = None,
) -> int:
    query = """\
        SELECT COUNT(*) AS count
          FROM stats
         WHERE id = COALESCE(:id, id)
           AND mode = COALESCE(:mode, mode)
    """
    params: dict[str, Any] = {
        "id": player_id,
        "mode": mode,
    }
    rec = await app.state.services.database.fetch_one(query, params)
    assert rec is not None
    return cast(int, rec._mapping["count"])


async def fetch_many(
    player_id: int | None = None,
    mode: int | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[Stat]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = COALESCE(:id, id)
           AND mode = COALESCE(:mode, mode)
    """
    params: dict[str, Any] = {
        "id": player_id,
        "mode": mode,
    }

    if page is not None and page_size is not None:
        query += """\
            LIMIT :limit
           OFFSET :offset
        """
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size

    stats = await app.state.services.database.fetch_all(query, params)
    return cast(list[Stat], [dict(s._mapping) for s in stats])


async def update(
    player_id: int,
    mode: int,
    tscore: int | _UnsetSentinel = UNSET,
    rscore: int | _UnsetSentinel = UNSET,
    pp: int | _UnsetSentinel = UNSET,
    plays: int | _UnsetSentinel = UNSET,
    playtime: int | _UnsetSentinel = UNSET,
    acc: float | _UnsetSentinel = UNSET,
    max_combo: int | _UnsetSentinel = UNSET,
    total_hits: int | _UnsetSentinel = UNSET,
    replay_views: int | _UnsetSentinel = UNSET,
    xh_count: int | _UnsetSentinel = UNSET,
    x_count: int | _UnsetSentinel = UNSET,
    sh_count: int | _UnsetSentinel = UNSET,
    s_count: int | _UnsetSentinel = UNSET,
    a_count: int | _UnsetSentinel = UNSET,
) -> Stat | None:
    """Update a player stats entry in the database."""
    update_fields: StatUpdateFields = {}
    if not isinstance(tscore, _UnsetSentinel):
        update_fields["tscore"] = tscore
    if not isinstance(rscore, _UnsetSentinel):
        update_fields["rscore"] = rscore
    if not isinstance(pp, _UnsetSentinel):
        update_fields["pp"] = pp
    if not isinstance(plays, _UnsetSentinel):
        update_fields["plays"] = plays
    if not isinstance(playtime, _UnsetSentinel):
        update_fields["playtime"] = playtime
    if not isinstance(acc, _UnsetSentinel):
        update_fields["acc"] = acc
    if not isinstance(max_combo, _UnsetSentinel):
        update_fields["max_combo"] = max_combo
    if not isinstance(total_hits, _UnsetSentinel):
        update_fields["total_hits"] = total_hits
    if not isinstance(replay_views, _UnsetSentinel):
        update_fields["replay_views"] = replay_views
    if not isinstance(xh_count, _UnsetSentinel):
        update_fields["xh_count"] = xh_count
    if not isinstance(x_count, _UnsetSentinel):
        update_fields["x_count"] = x_count
    if not isinstance(sh_count, _UnsetSentinel):
        update_fields["sh_count"] = sh_count
    if not isinstance(s_count, _UnsetSentinel):
        update_fields["s_count"] = s_count
    if not isinstance(a_count, _UnsetSentinel):
        update_fields["a_count"] = a_count

    query = f"""\
        UPDATE stats
           SET {",".join(f"{k} = COALESCE(:{k}, {k})" for k in update_fields)}
         WHERE id = :id
           AND mode = :mode
    """
    values = {"id": player_id, "mode": mode} | update_fields
    await app.state.services.database.execute(query, values)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
           AND mode = :mode
    """
    params: dict[str, Any] = {
        "id": player_id,
        "mode": mode,
    }
    stats = await app.state.services.database.fetch_one(query, params)
    return cast(Stat, dict(stats._mapping)) if stats is not None else None


# TODO: delete?
