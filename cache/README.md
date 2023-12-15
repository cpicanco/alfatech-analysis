# Sobre o sistema de cache da análise de dados

Algumas consultas ao banco de dados SQL do GEIC demoram bastante. Após as consultas, os objetos construidos são salvos em formato binário por meio da biblioteca `pickle` do python. O sistema de cache economiza tempo, pois ler os objetos binários é mais rápido do que refazer as consultas.
