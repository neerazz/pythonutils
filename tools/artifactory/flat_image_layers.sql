SELECT t.*,
  REPLACE(item, '"', '') as image_layer
FROM `wf-gcp-us-ae-sec-prod.appsec_github_metadata.all_docker_images` t
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(t.Image_Layers)) AS item
limit 10;

CREATE OR REPLACE TABLE `wf-gcp-us-ae-sec-prod.appsec_github_metadata.docker_images_with_layers`
AS
SELECT t.*,
  REPLACE(item, '"', '') as image_layer
FROM `wf-gcp-us-ae-sec-prod.appsec_github_metadata.all_docker_images` t
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(t.Image_Layers)) AS item;

select
count (*)
from `wf-gcp-us-ae-sec-prod.appsec_github_metadata.docker_images_with_layers`;