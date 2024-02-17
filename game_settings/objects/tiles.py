from pydantic import BaseModel


class TilesType(BaseModel):
    tile_1: str
    tile_2: str


class Tiles(BaseModel):
    grass: TilesType
    stone: TilesType
    sand: TilesType


TILES = Tiles(
    grass=TilesType(
        tile_1='assets/grass-pattern1.jpg',
        tile_2='assets/grass-pattern2.jpg'
    ),
    stone=TilesType(
        tile_1='assets/stone-pattern1.jpg',
        tile_2='assets/stone-pattern2.jpg'
    ),
    sand=TilesType(
        tile_1='assets/sand-pattern1.jpg',
        tile_2='assets/sand-pattern2.jpg'
    )
)
