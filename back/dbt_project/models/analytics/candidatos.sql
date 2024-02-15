SELECT
    tipo
    , mes
    , vuelta
    , ine_provincia
    , distrito_electoral
    , ine_municipio
    , codigo_candidatura
    , orden_candidato
    , tipo_candidato
    , trim(nombre) || ' ' || trim(coalesce(primer_apellido , '')) || ' ' || trim(coalesce(segundo_apellido , '')) AS nombre
    , sexo
    , dni
    , CASE elegido
    WHEN 'S' THEN
        TRUE
    WHEN 'N' THEN
        FALSE
    ELSE
        NULL
    END AS elegido
FROM
    {{ source('raw' , 'candidatos') }}
    -- { ref("orders_augmented") }
    -- raw.candidatos
