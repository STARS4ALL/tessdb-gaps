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


# Errores

## Fichero database_2019_11_29.csv
Antes de 
[2022-06-20 18:47:59] sqlite3 /var/dbase/tess.db < stars19.sql
[2022-06-20 18:48:01] sqlite3 /var/dbase/tess.db < stars1.sql

Salen mogollon de integroity erros

[2022-06-20 18:50:13] sqlite3 /var/dbase/tess.db < stars297.sql
Error: near line 4169: columns date_id, time_id, tess_id are not unique

## Fichero database_2020_12_23.csv

[2022-06-20 18:58:44] sqlite3 /var/dbase/tess.db < stars301.sql
Error: near line 118577: columns date_id, time_id, tess_id are not unique

[2022-06-20 19:06:27] sqlite3 /var/dbase/tess.db < stars468.sql
Error: near line 115462: columns date_id, time_id, tess_id are not unique

## Fichero database_2021_01_31.csv

## Fichero database_2021_06_25.csv

[2022-06-20 19:31:27] sqlite3 /var/dbase/tess.db < stars477.sql
Error: near line 56039: columns date_id, time_id, tess_id are not unique
Error: near line 123134: columns date_id, time_id, tess_id are not unique

## Fichero database_2021_08_15_2.csv

[2022-06-21 09:49:46] sqlite3 /var/dbase/tess.db < stars539.sql
Error: near line 115413: columns date_id, time_id, tess_id are not unique

## Fichero database_2021_08_15.csv

[2022-06-21 10:03:42] sqlite3 /var/dbase/tess.db < stars222.sql
Error: near line 151085: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:07:36] sqlite3 /var/dbase/tess.db < stars36.sql
Error: near line 112221: columns date_id, time_id, tess_id are not unique
Error: near line 112228: columns date_id, time_id, tess_id are not unique
Error: near line 859947: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:08:35] sqlite3 /var/dbase/tess.db < stars394.sql
Error: near line 150679: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:13:17] sqlite3 /var/dbase/tess.db < stars475.sql
Error: near line 146962: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:13:57] sqlite3 /var/dbase/tess.db < stars485.sql
Error: near line 98172: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:15:41] sqlite3 /var/dbase/tess.db < stars525
./loader.sh: línea 7: stars525: No existe el fichero o el directorio
[2022-06-21 10:15:43] sqlite3 /var/dbase/tess.db < .sql
./loader.sh: línea 7: .sql: No existe el fichero o el directorio

[2022-06-21 10:17:15] sqlite3 /var/dbase/tess.db < stars550.sql
Error: near line 879477: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:18:19] sqlite3 /var/dbase/tess.db < stars6
./loader.sh: línea 7: stars6: No existe el fichero o el directorio
[2022-06-21 10:18:21] sqlite3 /var/dbase/tess.db < 09.sql
./loader.sh: línea 7: 09.sql: No existe el fichero o el directorio

[2022-06-21 10:20:42] sqlite3 /var/dbase/tess.db < stars639.sql
Error: near line 150315: columns date_id, time_id, tess_id are not unique

## Fichero database_2021_10_24.csv 

[2022-06-21 10:30:32] sqlite3 /var/dbase/tess.db < stars369.sql
Error: near line 37069: columns date_id, time_id, tess_id are not unique
Error: near line 37286: columns date_id, time_id, tess_id are not unique
Error: near line 37293: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:35:12] sqlite3 /var/dbase/tess.db < stars529.sql
Error: near line 36544: columns date_id, time_id, tess_id are not unique
Error: near line 37335: columns date_id, time_id, tess_id are not unique
Error: near line 37545: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:35:26] sqlite3 /var/dbase/tess.db < stars530.sql
Error: near line 28249: columns date_id, time_id, tess_id are not unique
Error: near line 34962: columns date_id, time_id, tess_id are not unique
Error: near line 35179: columns date_id, time_id, tess_id are not unique
Error: near line 35186: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:35:32] sqlite3 /var/dbase/tess.db < stars531.sql
Error: near line 37300: columns date_id, time_id, tess_id are not unique
Error: near line 37517: columns date_id, time_id, tess_id are not unique
Error: near line 40184: columns date_id, time_id, tess_id are not unique

[2022-06-21 10:35:45] sqlite3 /var/dbase/tess.db < stars539.sql
Error: near line 37377: columns date_id, time_id, tess_id are not unique
Error: near line 37594: columns date_id, time_id, tess_id are not unique

## Fichero database_2021_11_04.csv

[2022-06-21 10:51:59] sqlite3 /var/dbase/tess.db < stars221.sql
Error: near line 48759: columns date_id, time_id, tess_id are not unique

[2022-06-21 11:00:59] sqlite3 /var/dbase/tess.db < stars525
./loader.sh: línea 7: stars525: No existe el fichero o el directorio
[2022-06-21 11:01:01] sqlite3 /var/dbase/tess.db < .sql
./loader.sh: línea 7: .sql: No existe el fichero o el directorio

[2022-06-21 11:01:42] sqlite3 /var/dbase/tess.db < stars539.sql
Error: near line 62948: columns date_id, time_id, tess_id are not unique

[2022-06-21 11:03:09] sqlite3 /var/dbase/tess.db < stars6
./loader.sh: línea 7: stars6: No existe el fichero o el directorio
[2022-06-21 11:03:11] sqlite3 /var/dbase/tess.db < 09.sql
./loader.sh: línea 7: 09.sql: No existe el fichero o el directorio

## Fichero database_2021_11_14.csv

[2022-06-21 11:24:40] sqlite3 /var/dbase/tess.db < stars525
./loader.sh: línea 7: stars525: No existe el fichero o el directorio
[2022-06-21 11:24:42] sqlite3 /var/dbase/tess.db < .sql
./loader.sh: línea 7: .sql: No existe el fichero o el directorio

[2022-06-21 11:26:45] sqlite3 /var/dbase/tess.db < stars6
./loader.sh: línea 7: stars6: No existe el fichero o el directorio
[2022-06-21 11:26:47] sqlite3 /var/dbase/tess.db < 09.sql
./loader.sh: línea 7: 09.sql: No existe el fichero o el directorio

## Fichero database_2022_01_17.csv

Nada

## Fichero database_2022_04_12.csv


## Fichero database_2020_02_19.csv

Error: near line 46274: columns date_id, time_id, tess_id are not unique
Error: near line 46281: columns date_id, time_id, tess_id are not unique
Error: near line 46288: columns date_id, time_id, tess_id are not unique
Error: near line 46295: columns date_id, time_id, tess_id are not unique
Error: near line 46302: columns date_id, time_id, tess_id are not unique
Error: near line 46309: columns date_id, time_id, tess_id are not unique
Error: near line 46316: columns date_id, time_id, tess_id are not unique
Error: near line 46323: columns date_id, time_id, tess_id are not unique
Error: near line 46330: columns date_id, time_id, tess_id are not unique
Error: near line 46337: columns date_id, time_id, tess_id are not unique
Error: near line 46344: columns date_id, time_id, tess_id are not unique
Error: near line 46351: columns date_id, time_id, tess_id are not unique
Error: near line 46358: columns date_id, time_id, tess_id are not unique
Error: near line 46365: columns date_id, time_id, tess_id are not unique
Error: near line 46372: columns date_id, time_id, tess_id are not unique
Error: near line 46379: columns date_id, time_id, tess_id are not unique
Error: near line 46386: columns date_id, time_id, tess_id are not unique
Error: near line 46393: columns date_id, time_id, tess_id are not unique
Error: near line 46400: columns date_id, time_id, tess_id are not unique
Error: near line 46407: columns date_id, time_id, tess_id are not unique
Error: near line 46414: columns date_id, time_id, tess_id are not unique
Error: near line 46421: columns date_id, time_id, tess_id are not unique
Error: near line 46428: columns date_id, time_id, tess_id are not unique
Error: near line 46435: columns date_id, time_id, tess_id are not unique
Error: near line 46442: columns date_id, time_id, tess_id are not unique
Error: near line 46449: columns date_id, time_id, tess_id are not unique
Error: near line 46456: columns date_id, time_id, tess_id are not unique
Error: near line 46463: columns date_id, time_id, tess_id are not unique
Error: near line 46470: columns date_id, time_id, tess_id are not unique
Error: near line 46477: columns date_id, time_id, tess_id are not unique
Error: near line 46484: columns date_id, time_id, tess_id are not unique
Error: near line 46491: columns date_id, time_id, tess_id are not unique
Error: near line 46498: columns date_id, time_id, tess_id are not unique
Error: near line 46505: columns date_id, time_id, tess_id are not unique
Error: near line 46512: columns date_id, time_id, tess_id are not unique
Error: near line 46519: columns date_id, time_id, tess_id are not unique
Error: near line 46526: columns date_id, time_id, tess_id are not unique
Error: near line 46533: columns date_id, time_id, tess_id are not unique
Error: near line 46540: columns date_id, time_id, tess_id are not unique
Error: near line 46547: columns date_id, time_id, tess_id are not unique
Error: near line 46554: columns date_id, time_id, tess_id are not unique
Error: near line 46561: columns date_id, time_id, tess_id are not unique
Error: near line 46568: columns date_id, time_id, tess_id are not unique
Error: near line 46575: columns date_id, time_id, tess_id are not unique
Error: near line 46582: columns date_id, time_id, tess_id are not unique
Error: near line 46589: columns date_id, time_id, tess_id are not unique
Error: near line 46596: columns date_id, time_id, tess_id are not unique
Error: near line 46603: columns date_id, time_id, tess_id are not unique
Error: near line 46610: columns date_id, time_id, tess_id are not unique
Error: near line 46617: columns date_id, time_id, tess_id are not unique
Error: near line 46624: columns date_id, time_id, tess_id are not unique
Error: near line 46631: columns date_id, time_id, tess_id are not unique
Error: near line 46638: columns date_id, time_id, tess_id are not unique
Error: near line 46645: columns date_id, time_id, tess_id are not unique
Error: near line 46652: columns date_id, time_id, tess_id are not unique
Error: near line 46659: columns date_id, time_id, tess_id are not unique
Error: near line 46666: columns date_id, time_id, tess_id are not unique
Error: near line 46673: columns date_id, time_id, tess_id are not unique
Error: near line 46680: columns date_id, time_id, tess_id are not unique
Error: near line 46687: columns date_id, time_id, tess_id are not unique
Error: near line 46694: columns date_id, time_id, tess_id are not unique
Error: near line 46701: columns date_id, time_id, tess_id are not unique
Error: near line 46708: columns date_id, time_id, tess_id are not unique
Error: near line 46715: columns date_id, time_id, tess_id are not unique
Error: near line 46722: columns date_id, time_id, tess_id are not unique
Error: near line 46729: columns date_id, time_id, tess_id are not unique
Error: near line 46736: columns date_id, time_id, tess_id are not unique
Error: near line 46743: columns date_id, time_id, tess_id are not unique
Error: near line 46750: columns date_id, time_id, tess_id are not unique
Error: near line 46757: columns date_id, time_id, tess_id are not unique
Error: near line 46764: columns date_id, time_id, tess_id are not unique
Error: near line 46771: columns date_id, time_id, tess_id are not unique
Error: near line 46778: columns date_id, time_id, tess_id are not unique
Error: near line 46785: columns date_id, time_id, tess_id are not unique
Error: near line 46792: columns date_id, time_id, tess_id are not unique
Error: near line 46799: columns date_id, time_id, tess_id are not unique
Error: near line 46806: columns date_id, time_id, tess_id are not unique
Error: near line 46813: columns date_id, time_id, tess_id are not unique
Error: near line 46820: columns date_id, time_id, tess_id are not unique
Error: near line 46827: columns date_id, time_id, tess_id are not unique
Error: near line 46834: columns date_id, time_id, tess_id are not unique
Error: near line 46841: columns date_id, time_id, tess_id are not unique
Error: near line 46848: columns date_id, time_id, tess_id are not unique
Error: near line 46855: columns date_id, time_id, tess_id are not unique
Error: near line 46862: columns date_id, time_id, tess_id are not unique
Error: near line 46869: columns date_id, time_id, tess_id are not unique
Error: near line 46876: columns date_id, time_id, tess_id are not unique
Error: near line 46883: columns date_id, time_id, tess_id are not unique
Error: near line 46890: columns date_id, time_id, tess_id are not unique
Error: near line 46897: columns date_id, time_id, tess_id are not unique
Error: near line 46904: columns date_id, time_id, tess_id are not unique
Error: near line 46911: columns date_id, time_id, tess_id are not unique
Error: near line 46918: columns date_id, time_id, tess_id are not unique
Error: near line 46925: columns date_id, time_id, tess_id are not unique
Error: near line 46932: columns date_id, time_id, tess_id are not unique
Error: near line 46939: columns date_id, time_id, tess_id are not unique
Error: near line 46946: columns date_id, time_id, tess_id are not unique
Error: near line 46953: columns date_id, time_id, tess_id are not unique
Error: near line 46960: columns date_id, time_id, tess_id are not unique
Error: near line 46967: columns date_id, time_id, tess_id are not unique
Error: near line 46974: columns date_id, time_id, tess_id are not unique
Error: near line 46981: columns date_id, time_id, tess_id are not unique
Error: near line 46988: columns date_id, time_id, tess_id are not unique
Error: near line 46995: columns date_id, time_id, tess_id are not unique
Error: near line 47002: columns date_id, time_id, tess_id are not unique
Error: near line 47009: columns date_id, time_id, tess_id are not unique
Error: near line 47016: columns date_id, time_id, tess_id are not unique
Error: near line 47023: columns date_id, time_id, tess_id are not unique
Error: near line 47030: columns date_id, time_id, tess_id are not unique
Error: near line 47037: columns date_id, time_id, tess_id are not unique
Error: near line 47044: columns date_id, time_id, tess_id are not unique
Error: near line 47051: columns date_id, time_id, tess_id are not unique
Error: near line 47058: columns date_id, time_id, tess_id are not unique
Error: near line 47065: columns date_id, time_id, tess_id are not unique
Error: near line 47072: columns date_id, time_id, tess_id are not unique
Error: near line 47079: columns date_id, time_id, tess_id are not unique
Error: near line 47086: columns date_id, time_id, tess_id are not unique
[2022-06-22 08:15:39] sqlite3 /var/dbase/tess.db < stars1.sql (ANTES DE STARS UNO, MIRAR)


[2022-06-22 08:18:26] sqlite3 /var/dbase/tess.db < stars286.sql
Error: near line 35522: columns date_id, time_id, tess_id are not unique

[2022-06-22 08:22:19] sqlite3 /var/dbase/tess.db < stars375-East
./loader.sh: línea 7: stars375-East: No existe el fichero o el directorio
[2022-06-22 08:22:21] sqlite3 /var/dbase/tess.db < Ta.sql
./loader.sh: línea 7: Ta.sql: No existe el fichero o el directorio

[2022-06-22 08:25:49] sqlite3 /var/dbase/tess.db < stars75.sql
Error: near line 2524: columns date_id, time_id, tess_id are not unique


## Fichero database_2021_03_26.csv
Nada

## Fichero database_2021_05_22.csv
Nada

# Aumento de la BBDD

aumento de hoy en la BD 12376713216-10635986944 = 1740726272 / 10635986944 = 16,37% mas

-rw-r--r--.  1 rfg  rfg  12376713216 jun 21 11:45 tess.db
-rw-r--r--.  1 rfg  rfg  10635986944 jun 20 12:01 tess.db-20220620

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
