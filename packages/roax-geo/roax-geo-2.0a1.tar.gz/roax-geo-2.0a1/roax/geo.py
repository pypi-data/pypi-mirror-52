"""Module that provides schema for GeoJSON data structures."""

import geojson
import geomet.wkt as wkt
import geomet.wkb as wkb
import roax.schema as s


class _Object(s.type):
    """Base class for all GeoJSON objects."""

    def __init__(
        self,
        *,
        python_type,
        content_type="application/json",
        props={},
        required=set(),
        additional=False,
        **kwargs,
    ):
        super().__init__(python_type=python_type, content_type=content_type, **kwargs)
        self.schema = s.dict(
            {
                "type": s.str(enum={self.__class__.__name__}),
                "bbox": s.list(items=s.float(), min_items=4),
                **props,
            },
            required={"type"}.union(required),
            additional=additional,
        )

    def validate(self, value):
        super().validate(value)
        return self.schema.validate(value.__geo_interface__)

    @property
    def json_schema(self):
        return self.schema.json_schema

    def json_encode(self, value):
        self.validate(value)
        return value.__geo_interface__

    def json_decode(self, value):
        self.schema.validate(value)  # validate first to get nicer error messages
        return self.python_type.to_instance(value)

    def str_encode(self, value):
        return wkt.dumps(self.json_encode(value))

    def str_decode(self, value):
        try:
            return self.json_decode(self.schema.strip(wkt.loads(value)))
        except Exception as e:
            raise s.SchemaError(
                f"invalid WKT representation of {self.__class__.__name__}"
            ) from e

    def bin_encode(self, value):
        return wkb.dumps(self.json_encode(value))

    def bin_decode(self, value):
        try:
            return self.json_decode(self.schema.strip(wkb.loads(value)))
        except Exception as e:
            raise s.SchemaError(
                f"invalid WKB representation of {self.__class__.__name__}"
            ) from e


class _Geometry(_Object):
    """Base class for all geometry objects."""

    def __init__(self, python_type, coordinates_schema, **kwargs):
        super().__init__(
            python_type=python_type,
            props={"coordinates": coordinates_schema},
            required={"coordinates"},
            **kwargs,
        )


class Point(_Geometry):
    """A geographical point."""

    def __init__(self, **kwargs):
        super().__init__(geojson.Point, _PointCoordinates(), **kwargs)


class _PointCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=s.float(), min_items=2, max_items=2, **kwargs)

    def validate(self, value):
        super().validate(value)
        if value[0] < -180.0 or value[0] > 180.0:
            raise s.SchemaError("invalid longitude; must be -180.0 ≤ longitude ≤ 180.0")
        if value[1] < -90.0 or value[1] > 90.0:
            raise s.SchemaError("invalid latitude; must be -90.0 ≤ latitude ≤ 90.0")


class LineString(_Geometry):
    """A connected sequence of points."""

    def __init__(self, **kwargs):
        super().__init__(geojson.LineString, _LineStringCoordinates(), **kwargs)


class _LineStringCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_PointCoordinates(), **kwargs)


class Polygon(_Geometry):
    """
    A linear ring and zero or more interior linear rings.

    Parameters:
    • min_rings: Minimum number of linear rings.
    • max_rings: Maximum number of linear rings.
    """

    def __init__(self, min_rings=1, max_rings=None, **kwargs):
        if min_rings < 1:
            raise ValueError("min rings must be ≥ 1")
        if max_rings is not None and max_rings < min_rings:
            raise ValueError("max_rings must be ≥ min_rings")
        super().__init__(
            geojson.Polygon,
            _PolygonCoordinates(min_items=min_rings, max_items=max_rings),
            **kwargs,
        )


class _PolygonCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_LinearRingCoordinates(), **kwargs)


class _LinearRingCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_PointCoordinates(), min_items=4, **kwargs)

    def validate(self, value):
        super().validate(value)
        if value[0] != value[-1]:
            raise s.SchemaError(
                "last point in linear ring must be the same as the first point"
            )


class MultiPoint(_Geometry):
    """A collection of points."""

    def __init__(self, **kwargs):
        super().__init__(geojson.MultiPoint, _MultiPointCoordinates(), **kwargs)


class _MultiPointCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_PointCoordinates(), **kwargs)


class MultiLineString(_Geometry):
    """A collection of line strings."""

    def __init__(self, **kwargs):
        super().__init__(
            geojson.MultiLineString, _MultiLineStringCoordinates(), **kwargs
        )


class _MultiLineStringCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_LineStringCoordinates(), **kwargs)


class MultiPolygon(_Geometry):
    """A collection of polygons."""

    def __init__(self, **kwargs):
        super().__init__(geojson.MultiPolygon, _MultiPolygonCoordinates(), **kwargs)


class _MultiPolygonCoordinates(s.list):
    def __init__(self, **kwargs):
        super().__init__(items=_PolygonCoordinates(), **kwargs)


class GeometryCollection(_Object):
    """A collection of geometries."""

    def __init__(self, **kwargs):
        super().__init__(
            python_type=geojson.GeometryCollection,
            props={"geometries": s.list(Geometry().schema)},
            required={"geometries"},
            **kwargs,
        )


class Geometry(s.one_of):
    """One of: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon."""

    def __init__(self, **kwargs):
        super().__init__(
            {
                Point(),
                MultiPoint(),
                LineString(),
                MultiLineString(),
                Polygon(),
                MultiPolygon(),
            },
            **kwargs,
        )
        self.schema = s.one_of([sch.schema for sch in self.schemas], **kwargs)


class Feature(_Object):
    """A spatially bounded thing."""

    def __init__(self, **kwargs):
        super().__init__(
            python_type=geojson.Feature,
            props={
                "geometry": Geometry(nullable=True).schema,
                "properties": s.dict(props={}, additional=True, nullable=True),
                "id": s.one_of({s.str(), s.int(), s.float()}),
            },
            required={"geometry", "properties"},
            **kwargs,
        )


class FeatureCollection(_Object):
    """A collection of features."""

    def __init__(self, props={}, required=set(), **kwargs):
        super().__init__(
            python_type=geojson.FeatureCollection,
            props={"features": s.list(Feature().schema), **props},
            required={"features"}.union(set(required)),
            **kwargs,
        )
