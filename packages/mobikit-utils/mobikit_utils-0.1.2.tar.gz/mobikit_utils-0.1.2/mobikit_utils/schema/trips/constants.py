from mobikit_utils.schema.meta.meta import get_name

base_name = get_name(__name__)
pk = "id"
trip_id = "trip_id"
start_coords = "start_point"
start_timestamp = "start_tm"
end_coords = "end_point"
end_timestamp = "end_tm"
render_polyline = "linestring"
columns = [
    pk,
    trip_id,
    start_coords,
    start_timestamp,
    end_coords,
    end_timestamp,
    render_polyline,
]
