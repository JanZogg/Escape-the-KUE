from Panorama import Hotspot


def create_hotspots(items_room, doors_room):
    return [
        # Die Punkte sind Panorama-Koordinaten, nicht die vom Screen
        Hotspot(
            points=[
                (2432, 531),
                (2478, 531),
                (2478, 560),
                (2432, 560)
            ],
            room_index=items_room[0], #room1_item1
            hotspot_type="item",
            reference_index=0
        ),
        Hotspot(
            points=[
                (3087, 670),
                (3120, 670),
                (3120, 699),
                (3087, 699)
            ],
            room_index=items_room[1], #room1_item2
            hotspot_type="item",
            reference_index=1
        ),
        Hotspot(
            points=[
                (3429, 327),
                (3540, 338),
                (3540, 585),
                (3429, 605)
            ],
            room_index = doors_room[0],
            hotspot_type="door",
            reference_index = 0
        ),
        Hotspot(
            points=[
                (3281, 370),
                (3372, 370),
                (3372, 506),
                (3281, 506)
            ],
            room_index=items_room[2], #room2_item1
            hotspot_type="item",
            reference_index=2
        ),
        Hotspot(
            points=[
                (2761, 289),
                (2875, 274),
                (2875, 515),
                (2761, 493)
            ],
            room_index=doors_room[1],
            hotspot_type="door",
            reference_index=1
        ),
        Hotspot(
            points=[
                (3870, 498),
                (3941, 506),
                (3936, 524),
                (3865, 517)
            ],
            room_index=items_room[3], #room2_item2
            hotspot_type="item",
            reference_index=3
        ),
        Hotspot(
            points=[
                (2213, 337),
                (2231, 337),
                (2241, 353),
                (2231, 371),
                (2213, 371),
                (2204, 353)
            ],
            room_index=items_room[4], #room2_item3
            hotspot_type="item",
            reference_index=4
        ),
        Hotspot(
            points=[
                (3651, 279),
                (3753, 291),
                (3753, 496),
                (3651, 496)
            ],
            room_index=doors_room[2],
            hotspot_type="door",
            reference_index=2
        ),
        Hotspot(
            points=[
                (458, 246),
                (685, 246),
                (685, 404),
                (458, 404)
            ],
            room_index=items_room[5], #room3_item1
            hotspot_type="item",
            reference_index=5
        ),
        Hotspot(
            points=[
                (1220, 452),
                (1320, 452),
                (1320, 479),
                (1220, 479)
            ],
            room_index=items_room[6], #room3_item2
            hotspot_type="item",
            reference_index=6
        ),
        Hotspot(
            points=[
                (2098, 305),
                (2190, 305),
                (2190, 436),
                (2098, 436)
            ],
            room_index=items_room[7], #room3_item3
            hotspot_type="item",
            reference_index=7
        ),
        Hotspot(
            points=[
                (569, 448),
                (593, 445),
                (615, 454),
                (615, 471),
                (589, 474),
                (569, 464)
            ],
            room_index=items_room[8], #room3_item4
            hotspot_type="item",
            reference_index=8
        ),
        Hotspot(
            points=[
                (3570, 310),
                (3634, 310),
                (3634, 415),
                (3570, 415)
            ],
            room_index=items_room[9], #room3_item5
            hotspot_type="item",
            reference_index=9
        ),
        Hotspot(
            points=[
                (3115, 298),
                (3204, 312),
                (3197, 528),
                (3115, 555)
            ],
            room_index=doors_room[3],
            hotspot_type="door",
            reference_index=3
        ),
        Hotspot(
            points=[
                (3250, 240),
                (3456, 218),
                (3479, 314),
                (3288, 323)
            ],
            room_index=items_room[10], #room4_item1
            hotspot_type="item",
            reference_index=10
        ),
        Hotspot(
            points=[
                (2147, 466),
                (2176, 466),
                (2176, 511),
                (2147, 511)
            ],
            room_index=items_room[11], #room4_item2
            hotspot_type="item",
            reference_index=11
        ),
        Hotspot(
            points=[
                (3600, 432),
                (3634, 432),
                (3634, 494),
                (3600, 494)
            ],
            room_index=items_room[12], #room4_item3
            hotspot_type="item",
            reference_index=12
        ),
        Hotspot(
            points=[
                (3450, 358),
                (3496, 358),
                (3496, 428),
                (3450, 428)
            ],
            room_index=items_room[13], #room4_item4
            hotspot_type="item",
            reference_index=13
        ),
        Hotspot(
            points=[
                (1691, 307),
                (1834, 307),
                (1834, 412),
                (1691, 412)
            ],
            room_index=items_room[14], #room4_item5
            hotspot_type="item",
            reference_index=14
        ),
        Hotspot(
            points=[
                (1915, 316),
                (2026, 316),
                (2026, 407),
                (1915, 407)
            ],
            room_index=items_room[15], #room4_item6
            hotspot_type="item",
            reference_index=15
        ),
        Hotspot(
            points=[
                (2660, 316),
                (2707, 316),
                (2707, 359),
                (2660, 359)
            ],
            room_index=items_room[16], #room4_item7
            hotspot_type="item",
            reference_index=16
        ),
            Hotspot(
            points=[
                (3572, 314),
                (3687, 304),
                (3687, 551),
                (3572, 547)
            ],
            room_index=doors_room[4],
            hotspot_type="door",
            reference_index=4
        ),
        Hotspot(
            points=[
                (1644, 250),
                (1744, 250),
                (1744, 358),
                (1644, 358)
            ],
            room_index=items_room[17], #room5_item1
            hotspot_type="item",
            reference_index=17
        ),
        Hotspot(
            points=[
                (2914, 180),
                (3075, 180),
                (3075, 252),
                (2914, 252)
            ],
            room_index=items_room[18], #room5_item2
            hotspot_type="item",
            reference_index=18
        ),
        Hotspot(
            points=[
                (1961, 232),
                (2042, 232),
                (2042, 328),
                (1961, 328)
            ],
            room_index=items_room[19], #room5_item3
            hotspot_type="item",
            reference_index=19
        ),
        Hotspot(
            points=[
                (2547, 355),
                (2582, 355),
                (2582, 425),
                (2547, 425)
            ],
            room_index=items_room[20], #room5_item4
            hotspot_type="item",
            reference_index=20
        ),
        Hotspot(
            points=[
                (1682, 362),
                (1705, 362),
                (1705, 380),
                (1682, 380)
            ],
            room_index=items_room[21], #room5_item5
            hotspot_type="item",
            reference_index=21
        ),
            Hotspot(
            points=[
                (2768, 298),
                (2883, 288),
                (2875, 557),
                (2764, 560)
            ],
            room_index=doors_room[5],
            hotspot_type="door",
            reference_index=5
        ),
        Hotspot(
            points=[
                (805, 753),
                (864, 753),
                (864, 778),
                (805, 778)
            ],
            room_index=items_room[22], #room6_item1
            hotspot_type="item",
            reference_index=22
        ),
        Hotspot(
            points=[
                (3343, 390),
                (3413, 390),
                (3413, 497),
                (3343, 497)
            ],
            room_index=items_room[23], #room6_item2
            hotspot_type="item",
            reference_index=23
        ),
        Hotspot(
            points=[
                (3213, 392),
                (3313, 392),
                (3313, 486),
                (3213, 486)
            ],
            room_index=items_room[24], #room6_item3
            hotspot_type="item",
            reference_index=24
        ),
        Hotspot(
            points=[
                (3069, 403),
                (3195, 403),
                (3195, 482),
                (3069, 482)
            ],
            room_index=items_room[25], #room6_item4
            hotspot_type="item",
            reference_index=25
        ),
        Hotspot(
            points=[
                (1862, 470),
                (1891, 470),
                (1891, 495),
                (1862, 495)
            ],
            room_index=items_room[26], #room6_item5
            hotspot_type="item",
            reference_index=26
        ),
        Hotspot(
            points=[
                (2181, 580),
                (2205, 580),
                (2205, 593),
                (2181, 593)
            ],
            room_index=items_room[27], #room6_item6
            hotspot_type="item",
            reference_index=27
        ),
        Hotspot(
            points=[
                (1896, 599),
                (1928, 599),
                (1928, 625),
                (1896, 625)
            ],
            room_index=items_room[28], #room6_item7
            hotspot_type="item",
            reference_index=28
        ),
        Hotspot(
            points=[
                (899, 271),
                (1008, 271),
                (1008, 471),
                (899, 471)
            ],
            room_index=items_room[29], #room6_item8
            hotspot_type="item",
            reference_index=29
        )
    ]
