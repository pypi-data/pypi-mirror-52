# lanelet2-parser: Parser for Lanelet2

## Tutorial
#### Creating Lanelet2Parser instance
```
>>> from lanelet2_parser import Lanelet2Parser
>>> lanelet2_parser = Lanelet2Parser()
```

#### Parse OSM File
```
>>> osm_data = lanelet2_parser.parse(osm_map_file_path)
```

##### OSM Data Format
```
OSM
- version: Float
- nodes: List<Node>
- ways: List<Way>
- relations: List<Relation>

Node
- id: Int
- lat: Decimal
- lon: Decimal
- ele: Decimal
- tags: List<Tag>
- visible: Bool

Way
- id: Int
- nodes: List<Node>
- tags: List<Tag>
- visible: Bool

Relation
- id: Int
- members: List<Member>
- tags: List<Tag>
- visible: Bool

Tag
- key: String
- value: String

Member
- type: String
- ref: Int
- role: String
```
#### Convert Lanelet2 format from OSM
```
>>> lanelet2_data = lanelet2_parser.convert_to_lanelet2(osm_data)
```


##### Lanelet2 Data Format
```
Lanelet2
- version: Float
- points: List<Node>
- line_strings: List<LineString>
- lanelets: List<Lanelet>
- areas: List<Area>
- polygons: List<Polygon>
- regulatory_elements: List<RegulatoryElement>
- line_string_relations: Dict<line_string_id: LineStringRelation>
- lanelet_relations: Dict<lanelet_id: LaneletRelation>

Point
- id: Int
- lat: Decimal
- lon: Decimal
- ele: Decimal
- x: Decimal
- y: Decimal
- z: Decimal
- attibutes: List<Attribute>

LineString
- id: Int
- points: List<Point>
- attibutes: List<Attribute>

Lanelet
- id: Int
- left_bound: LineString
- right_bound: LineString
- center_line: LineString
- attibutes: List<Attribute>
- regulatory_element: List<RegulatoryElement>

RegulatoryElement
- id: Int
- subtype: String
- attibutes: List<Attribute>
- parameters: List<Parameter>

Parameter
- refers: LineString or Lanelet
- ref_line: LineString
- right_of_way: Lanelet
- param_yield: Lanelet
- cancels: Lanelet
- cancel_line: LineString

LineStringRelation
- prev_ids: List<Int>
- next_ids: List<Int>

LaneletStringRelation
- prev_ids: List<Int>
- next_ids: List<Int>
```

