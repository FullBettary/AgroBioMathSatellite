from sentinelhub import (SHConfig,
                         CRS,
                         BBox,
                         MimeType,
                         SentinelHubRequest,
                         bbox_to_dimensions,
                         DataCollection,
                         MosaickingOrder,
                         SentinelHubCatalog)

from scripts.evalscripts import evalscript_nature_color

class SentinelHubClient:
    def __init__(self, instance_id, sh_client_id, sh_client_secret):
        self.config = SHConfig()
        self.config.instance_id = instance_id
        self.config.sh_client_id = sh_client_id
        self.config.sh_client_secret = sh_client_secret
        self.config.save("myapp")

    def make_simple_request(self,
                            wgs84_coord,
                            time_point,
                            resolution=10,
                            size=None,
                            evalscript=evalscript_nature_color,
                            data_collection=DataCollection.SENTINEL2_L1C,
                            type_responses=MimeType.PNG,
                            ):

        if type(wgs84_coord) == 'list':
            bbox = BBox(bbox=wgs84_coord, crs=CRS.WGS84)
        else:
            bbox = wgs84_coord

        if size is None:
            size = bbox_to_dimensions(bbox, resolution=resolution)

        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=data_collection,
                    time_interval=(time_point, time_point),
                    mosaicking_order=MosaickingOrder.LEAST_CC,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", type_responses)],
            bbox=bbox,
            size=size,
            config=self.config,
        )

        data_from_request = request.get_data()
        return data_from_request[0]


    def get_info_about_exist_image(self,
                                   wgs84_coord,
                                   time_interval,
                                   collection=DataCollection.SENTINEL2_L1C,
                                   filter="eo:cloud_cover < 50",
                                   fields=None):
        if fields is None:
            fields = {"include": ["id", "properties.datetime", "properties.eo:cloud_cover"], "exclude": []}

        if type(wgs84_coord) == 'list':
            bbox = BBox(bbox=wgs84_coord, crs=CRS.WGS84)
        else:
            bbox = wgs84_coord

        catalog = SentinelHubCatalog(config=self.config)
        search_iterator = catalog.search(
            collection=collection,
            bbox=bbox,
            time=time_interval,
            filter=filter,
            fields=fields,
        )
        results = list(search_iterator)
        results.reverse()
        return results