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



