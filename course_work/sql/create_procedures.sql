CREATE OR REPLACE FUNCTION create_battlers(
    adv_id INTEGER,
    creatures_ids INTEGER[],
    weapons_ids INTEGER[]
) RETURNS INTEGER[] AS
$$

DECLARE
    battlers_ids INTEGER[];
    i            INTEGER;
    battler_id   INTEGER;
    arr_l        INTEGER;
BEGIN

    SELECT array_length(creatures_ids, 1) INTO arr_l;
    FOR i IN 1..arr_l
        LOOP

            INSERT INTO battles_battler (creature_id, adventure_id, weapon_id)
            VALUES (creatures_ids[i], adv_id, weapons_ids[i])
            ON CONFLICT (adventure_id, creature_id) DO UPDATE SET weapon_id=weapons_ids[i]
            RETURNING id INTO battler_id;
            SELECT INTO battlers_ids array_append(battlers_ids, battler_id);
        END LOOP;
    RETURN battlers_ids;

END;

$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION create_adventure(
    adv_name VARCHAR(255),
    team_name VARCHAR(255),
    planets_ids INTEGER[],
    creatures_ids INTEGER[],
    weapons_ids INTEGER[]
) RETURNS INTEGER AS
$$
DECLARE
    universes_count INTEGER;
    adv_id          INTEGER;
    team_id         INTEGER;
    planet_id       INTEGER;
    battlers_ids    INTEGER[];
    battler_id      INTEGER;

BEGIN
    SELECT COUNT(DISTINCT planets_planet.universe_id)
    INTO universes_count
    FROM planets_planet
    WHERE planets_planet.id = ANY (planets_ids);
    IF (universes_count > 1) THEN RAISE EXCEPTION 'All planets should be from one universe'; END IF;
    SELECT COUNT(DISTINCT planets_planet.universe_id)
    INTO universes_count
    FROM creatures_creature
             JOIN planets_planet on creatures_creature.planet_id = planets_planet.id
    WHERE creatures_creature.id = ANY (creatures_ids);
    IF (universes_count > 1) THEN RAISE EXCEPTION 'All creatures should be from one universe'; END IF;

    INSERT INTO adventures_adventure(name, created_at) VALUES (adv_name, current_timestamp) RETURNING id INTO adv_id;
    INSERT INTO adventures_team(name, adventure_id) VALUES (team_name, adv_id) RETURNING id INTO team_id;

    FOREACH planet_id IN ARRAY planets_ids
        LOOP
            INSERT INTO adventures_adventureplanet (adventure_id, planet_id, is_visited)
            VALUES (adv_id, planet_id, false);
        END LOOP;

    SELECT INTO battlers_ids create_battlers(adv_id, creatures_ids, weapons_ids);
    RAISE NOTICE '%', battlers_ids;

    FOREACH battler_id IN ARRAY battlers_ids
        LOOP
            INSERT INTO adventures_teammate(team_id, battler_id) VALUES (@team_id, @battler_id);
        END LOOP;


    RETURN adv_id;

END

$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE fill_battle_members(
    _team_id INTEGER,
    _battle_id INTEGER
) AS
$$
DECLARE
    _planet_id    INTEGER;
    creatures_ids INTEGER[];
    battlers_ids  INTEGER[];
    adv_id        INTEGER;
    _battler_id   INTEGER;
BEGIN
    SELECT planet_id, adventure_id INTO _planet_id, adv_id FROM battles_battle WHERE id = _battle_id;

    DROP TABLE IF EXISTS teammates_creatures;
    CREATE TEMP TABLE teammates_creatures AS (
        SELECT battler_id, creature_id
        FROM adventures_teammate
                 JOIN battles_battler ON adventures_teammate.battler_id = battles_battler.id
        WHERE team_id = _team_id);

    SELECT ARRAY(
                   SELECT creatures_creature.id::INTEGER
                   FROM creatures_creature
                            LEFT JOIN teammates_creatures ON creatures_creature.id = teammates_creatures.creature_id
                   WHERE planet_id = _planet_id
                     AND teammates_creatures.creature_id IS NULL
                   ORDER BY random()
               --LIMIT rows_count
               )
    INTO creatures_ids;

    RAISE NOTICE 'creatures in planet %', creatures_ids;
    SELECT INTO battlers_ids create_battlers(
                                     adv_id,
                                     creatures_ids,
                                     ARRAY []::INTEGER[]);

    FOREACH _battler_id IN ARRAY battlers_ids
        LOOP
            INSERT INTO battles_battlemember (battle_id, battler_id, is_opponent)
            VALUES (_battle_id, _battler_id, round(random())::INTEGER::BOOL);
        END LOOP;

    INSERT INTO battles_battlemember (battle_id, battler_id, is_opponent)
    SELECT _battle_id, battler_id, false
    FROM teammates_creatures;

    DROP TABLE teammates_creatures;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE fill_battler_effects(_battle_id INTEGER) AS
$$
DECLARE
    _planet_id INTEGER;
BEGIN
    SELECT planet_id INTO _planet_id FROM battles_battle WHERE id = _battle_id;


    CREATE TEMP TABLE creatures_opps AS (
        SELECT battler_id, creature_id, is_opponent
        FROM battles_battlemember
                 JOIN battles_battler ON battles_battlemember.battler_id = battles_battler.id
    );
    CREATE TEMP TABLE allies AS (
        SELECT *
        FROM creatures_opps
        WHERE is_opponent = false
    );

    CREATE TEMP TABLE opponents AS (
        SELECT *
        FROM creatures_opps
        WHERE is_opponent = false
    );

    INSERT INTO battles_battlereffect (battle_id, battler_id, effect_id)
    SELECT _battle_id, battler_id, effect_id
    FROM (
             SELECT *
             FROM affects_planeteffectrule
                      INNER JOIN planets_planet ON planet_id = _planet_id
                      INNER JOIN creatures_opps ON creature_to_id = creatures_opps.creature_id
         ) as tmp;

    INSERT INTO battles_battlereffect (battle_id, battler_id, effect_id)
    SELECT _battle_id, battler_id, effect_id
    FROM (
             SELECT al_to.battler_id, effect_id
             FROM affects_creatureeffectrule
                      INNER JOIN allies al_from ON al_from.creature_id = creature_from_id
                      INNER JOIN allies al_to ON al_to.creature_id = creature_to_id
             WHERE is_to_ally = true
         ) as tmp;
    INSERT INTO battles_battlereffect (battle_id, battler_id, effect_id)
    SELECT _battle_id, battler_id, effect_id
    FROM (
             SELECT op_to.battler_id, effect_id
             FROM affects_creatureeffectrule
                      INNER JOIN allies al_from ON al_from.creature_id = creature_from_id
                      INNER JOIN opponents op_to ON op_to.creature_id = creature_to_id
             WHERE is_to_ally = false
         ) as tmp;
    INSERT INTO battles_battlereffect (battle_id, battler_id, effect_id)
    SELECT _battle_id, battler_id, effect_id
    FROM (
             SELECT al_to.battler_id, effect_id
             FROM affects_creatureeffectrule
                      INNER JOIN opponents op_from ON op_from.creature_id = creature_from_id
                      INNER JOIN allies al_to ON al_to.creature_id = creature_to_id
             WHERE is_to_ally = false
         ) as tmp;

    INSERT INTO battles_battlereffect (battle_id, battler_id, effect_id)
    SELECT _battle_id, battler_id, effect_id
    FROM (
             SELECT op_to.battler_id, effect_id
             FROM affects_creatureeffectrule
                      INNER JOIN opponents op_from ON op_from.creature_id = creature_from_id
                      INNER JOIN opponents op_to ON op_to.creature_id = creature_to_id
             WHERE is_to_ally = true
         ) as tmp;

    DROP TABLE creatures_opps;
    DROP TABLE allies;
    DROP TABLE opponents;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE make_battle_report(_battle_id INTEGER) AS
$$
DECLARE
    _allies_power    INTEGER default 0;
    _opponents_power INTEGER default 0;
BEGIN

    CREATE TEMP TABLE battlers_with_creatures_and_weapons AS (
        SELECT creatures_creature.id    as creature_id,
               battles_battler.id       as battler_id,
               creatures_creature.power as creature_power,
               affects_weapon.power     as weapon_power,
               is_opponent

        FROM battles_battlemember
                 INNER JOIN battles_battler ON battles_battlemember.battler_id = battles_battler.id
                 INNER JOIN creatures_creature ON battles_battler.creature_id = creatures_creature.id
                 LEFT JOIN affects_weapon on battles_battler.weapon_id = affects_weapon.id
        WHERE battle_id = _battle_id
    );

    CREATE TEMP TABLE battler_applied_effects AS (
        SELECT is_opponent, power_affect
        FROM battles_battlemember
                 LEFT JOIN battles_battlereffect ON battles_battlemember.battler_id = battles_battlereffect.battler_id
                 INNER JOIN affects_effect ON effect_id = affects_effect.id
        WHERE battles_battlemember.battle_id = _battle_id
    );


    _allies_power := _allies_power + (SELECT COALESCE(SUM(weapon_power), 0)
                                      FROM battlers_with_creatures_and_weapons
                                      WHERE is_opponent = false);
    RAISE NOTICE 'Al pwr %', _allies_power;
    _allies_power := _allies_power + (SELECT COALESCE(SUM(creature_power), 0)
                                      FROM battlers_with_creatures_and_weapons
                                      WHERE is_opponent = false);
    RAISE NOTICE 'Al pwr %', _allies_power;
    _allies_power := _allies_power +
                     (SELECT COALESCE(SUM(power_affect), 0) FROM battler_applied_effects WHERE is_opponent = false);
    RAISE NOTICE 'Al pwr %', _allies_power;

    _opponents_power := _opponents_power + (SELECT COALESCE(SUM(weapon_power), 0)
                                            FROM battlers_with_creatures_and_weapons
                                            WHERE is_opponent = true);
    RAISE NOTICE 'Op pwr %', _opponents_power;
    _opponents_power := _opponents_power + (SELECT COALESCE(SUM(creature_power), 0)
                                            FROM battlers_with_creatures_and_weapons
                                            WHERE is_opponent = true);
    RAISE NOTICE 'Op pwr %', _opponents_power;
    _opponents_power := _opponents_power +
                        (SELECT COALESCE(SUM(power_affect), 0) FROM battler_applied_effects WHERE is_opponent = true);
    RAISE NOTICE 'Op pwr %', _opponents_power;
    IF (_allies_power < 0 OR _allies_power IS NULL) THEN _allies_power := 0; END IF;
    IF (_opponents_power < 0 OR _opponents_power IS NULL) THEN _opponents_power := 0; END IF;

    INSERT INTO battles_battlereport (battle_id, allies_power, opponents_power)
    VALUES (_battle_id, _allies_power, _opponents_power);

    DROP TABLE battler_applied_effects;
    DROP TABLE battlers_with_creatures_and_weapons;

END;

$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION adventure_step(adv_id INTEGER) RETURNS INTEGER AS
$$
DECLARE
    battle_planet_id       INTEGER;
    adventure_planet_id    INTEGER;
    _battle_id             INTEGER;
    _team_id               INTEGER;
    _adventure_finished_at TIMESTAMP;
    _allies_power          INTEGER;
    _opponents_power       INTEGER;
    _count_unvisited       INTEGER;
    _adventure_started_at  TIMESTAMP;
BEGIN
    SELECT planet_id, id
    INTO battle_planet_id, adventure_planet_id
    FROM adventures_adventureplanet
    WHERE adventures_adventureplanet.adventure_id = adv_id
      AND is_visited = False
    ORDER BY random()
    LIMIT 1;

    SELECT finished_at INTO _adventure_finished_at FROM adventures_adventure WHERE id = adv_id;

    IF (battle_planet_id IS NULL) THEN RETURN NULL; END IF;
    IF (_adventure_finished_at IS NOT NULL) THEN RAISE EXCEPTION 'Adventure % already finished', adv_id; END IF;
    IF (_adventure_started_at IS NULL) THEN
        UPDATE adventures_adventure SET started_at=current_timestamp WHERE id = adv_id;
    END IF;
    UPDATE adventures_adventureplanet SET is_visited= True WHERE id = adventure_planet_id;

    INSERT INTO battles_battle (adventure_id, planet_id, created_at)
    VALUES (adv_id, battle_planet_id, current_timestamp)
    RETURNING id INTO _battle_id;

    SELECT id::INTEGER INTO _team_id FROM adventures_team WHERE adventure_id = adv_id;

    RAISE NOTICE 'team-id: % battle-id: %', _team_id, _battle_id;

    CALL fill_battle_members(_team_id, _battle_id);
    CALL fill_battler_effects(_battle_id);
    CALL make_battle_report(_battle_id);

    SELECT allies_power, opponents_power
    INTO _allies_power, _opponents_power
    FROM battles_battlereport
    WHERE battle_id = _battle_id;
    SELECT COUNT(*) INTO _count_unvisited FROM adventures_adventureplanet WHERE is_visited = False and adventure_id=adv_id;

    IF (_allies_power < _opponents_power) THEN
        UPDATE adventures_adventure SET finished_at=current_timestamp, is_successful=False WHERE id = adv_id;
        RETURN _battle_id;
    END IF;

    IF (_count_unvisited = 0) THEN
        UPDATE adventures_adventure SET finished_at=current_timestamp, is_successful= True WHERE id = adv_id;
    END IF;

    RETURN _battle_id;


END;
$$ LANGUAGE plpgsql;
