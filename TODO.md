SHORT TERM
==========

Fichero CSV de esteban tiene: time,freq,mag,rev,seq,tamb,tsky,wdBm

* Migracion fácil de tablas
- date_id, time_id
- units_id -> Usando el código 2 = Timestamp by "Subscriber", reading source "Imported"

* Migración con dificultad alta
- tess_id

1) Buscar la MAC cuya valiided viene en la fecha del payload en la tabla nam_to_mac_t
  - Solo debería haber una. Si hay más es un error
2) Buscar uno o varios tess_id,location_id con el rango de fechas envolciendo a la fecha dada y la mac dada
   - si hay varios es un error




# Deteccion de ambiguedad de estado
select mac_address,tess_id,valid_state, count(valid_state)
FROM tess_t
WHERE valid_state = 'Current'
group by mac_address
having count(valid_state) >1

mac_address     tess_id   valid_state count(valid_state)
24:A1:60:2F:98:B3 1889    Current     2
5C:CF:7F:76:6A:3C 193     Current     3
60:1:94:2E:CE:EB  716     Current     2
98:F4:AB:B2:7C:3D 1994    Current     3
A0:20:A6:32:44:DE 718     Current     3
CC:50:E3:16:81:1D 578     Current     2
CC:50:E3:2E:5B:C8 494     Current     4
E8:DB:84:83:67:FA 2113    Current     2


# renombado alternado de stars383

name      mac_address       valid_since         valid_until         valid_state
-------------------------------------------------------------------------------
stars383  CC:50:E3:2E:5B:C8 2019-09-23T18:51:26 2020-11-06 09:40:48 Expired
stars383  5C:CF:7F:76:6A:3C 2020-11-06 09:40:48 2020-11-06 12:10:25 Expired
stars383  CC:50:E3:2E:5B:C8 2020-11-06 12:10:25 2020-11-06 13:47:58 Expired
stars383  5C:CF:7F:76:6A:3C 2020-11-06 13:47:58 2020-11-07 12:02:36 Expired
stars383  CC:50:E3:2E:5B:C8 2020-11-07 12:02:36 2020-11-09 10:54:50 Expired
stars383  5C:CF:7F:76:6A:3C 2020-11-09 10:54:50 2022-04-27 13:43:19 Expired
stars383  98:F4:AB:B2:7B:29 2022-04-27 13:43:19 2999-12-31T23:59:59 Current

El fotometro tiene esta historia
tess_id   mac_address       zero_point  filter    valid_since         valid_until         valid_state location_id
100       5C:CF:7F:76:6A:3C 20.4        UV/IR-cut 2018-05-27T10:30:55 2018-07-13T15:20:24 Expired     9
193       5C:CF:7F:76:6A:3C 20.51       UV/IR-cut 2018-07-13T15:20:24 2020-11-06 13:47:58 Expired     9
1690      5C:CF:7F:76:6A:3C 20.51       UV/IR-cut 2020-11-06 13:47:58 22020-11-09 10:54:50 Expired    9
1692      5C:CF:7F:76:6A:3C 20.51       UV/IR-cut 2020-11-09 10:54:50 2999-12-31T23:59:59 Current     9


## Correcciones 1
-- -----------------
-- 24:A1:60:2F:98:B3
-- -----------------

UPDATE tess_t 
SET valid_until = '2022-03-07 11:20:54', valid_state = 'Expired'
WHERE tess_id = 1889;

-- -----------------
-- 5C:CF:7F:76:6A:3C
-- -----------------

UPDATE tess_t 
SET valid_until = '2020-11-06 13:47:58', valid_state = 'Expired', location_id = 9
WHERE tess_id = 193;
UPDATE tess_t 
SET valid_until = '2020-11-09 10:54:50', valid_state = 'Expired', location_id = 9
WHERE tess_id = 1690;

UPDATE tess_t 
SET  location_id = 9
WHERE tess_id = 1692;

-- -----------------
-- 60:1:94:2E:CE:EB
-- -----------------

UPDATE tess_t 
SET valid_until = '2020-12-10 09:06:06', valid_state = 'Expired'
WHERE tess_id = 716;

-- -----------------
-- 98:F4:AB:B2:7C:3D
-- -----------------

UPDATE tess_t 
SET valid_until = '2022-03-31 12:09:51', valid_state = 'Expired'
WHERE tess_id = 1994;
UPDATE tess_t 
SET valid_until = '2022-04-06 09:14:03', valid_state = 'Expired'
WHERE tess_id = 2136;

-- -----------------
-- A0:20:A6:32:44:DE
-- -----------------

UPDATE tess_t 
SET valid_until = '2022-03-31 12:02:45', valid_state = 'Expired'
WHERE tess_id = 718;
UPDATE tess_t 
SET valid_until = '2022-04-01 12:10:24', valid_state = 'Expired'
WHERE tess_id = 2135;

-- -----------------
-- CC:50:E3:16:81:1D
-- -----------------

UPDATE tess_t 
SET valid_until = '2021-04-15 13:47:27', valid_state = 'Expired'
WHERE tess_id = 578;

UPDATE tess_t 
SET  location_id = 93
WHERE tess_id = 1775;

-- -----------------
-- CC:50:E3:2E:5B:C8
-- -----------------

UPDATE tess_t 
SET valid_until = '2020-11-06 12:10:25', valid_state = 'Expired'
WHERE tess_id = 494;
UPDATE tess_t 
SET valid_until = '2020-11-07 12:02:36', valid_state = 'Expired'
WHERE tess_id = 1689;
UPDATE tess_t 
SET valid_until = '2021-01-18 16:51:10', valid_state = 'Expired'
WHERE tess_id = 1691;

-- -----------------
-- E8:DB:84:83:67:FA
-- -----------------

UPDATE tess_t 
SET valid_until = '2022-05-30 02:35:34', valid_state = 'Expired', zero_point = 20.37
WHERE tess_id = 2113;

UPDATE tess_t 
SET zero_point = 20.37
WHERE tess_id = 2192;
