import 'package:json_annotation/json_annotation.dart';

part 'transit_model.g.dart';

@JsonSerializable()
class TripUpdate {
  @JsonKey(name: 'trip_id')
  final String tripId;
  @JsonKey(name: 'route_id')
  final String routeId;
  @JsonKey(name: 'start_time')
  final String? startTime;
  @JsonKey(name: 'start_date')
  final String? startDate;
  @JsonKey(name: 'stop_time_updates')
  final List<StopTimeUpdate> stopTimeUpdates;

  TripUpdate({
    required this.tripId,
    required this.routeId,
    this.startTime,
    this.startDate,
    required this.stopTimeUpdates,
  });

  factory TripUpdate.fromJson(Map<String, dynamic> json) =>
      _$TripUpdateFromJson(json);

  Map<String, dynamic> toJson() => _$TripUpdateToJson(this);
}

@JsonSerializable()
class StopTimeUpdate {
  @JsonKey(name: 'stop_id')
  final String stopId;
  @JsonKey(name: 'stop_name')
  final String? stopName;
  @JsonKey(name: 'arrival_time')
  final DateTime? arrivalTime;
  @JsonKey(name: 'departure_time')
  final DateTime? departureTime;
  final int? delay;

  StopTimeUpdate({
    required this.stopId,
    this.stopName,
    this.arrivalTime,
    this.departureTime,
    this.delay,
  });

  factory StopTimeUpdate.fromJson(Map<String, dynamic> json) =>
      _$StopTimeUpdateFromJson(json);

  Map<String, dynamic> toJson() => _$StopTimeUpdateToJson(this);
}

@JsonSerializable()
class RouteQuery {
  final String origin;
  final String destination;
  @JsonKey(name: 'departure_time')
  final DateTime? departureTime;
  @JsonKey(name: 'max_routes')
  final int maxRoutes;
  @JsonKey(name: 'prefer_less_crowded')
  final bool preferLessCrowded;
  @JsonKey(name: 'include_weather')
  final bool includeWeather;
  @JsonKey(name: 'weather_location')
  final String? weatherLocation;

  RouteQuery({
    required this.origin,
    required this.destination,
    this.departureTime,
    this.maxRoutes = 3,
    this.preferLessCrowded = false,
    this.includeWeather = false,
    this.weatherLocation,
  });

  factory RouteQuery.fromJson(Map<String, dynamic> json) =>
      _$RouteQueryFromJson(json);

  Map<String, dynamic> toJson() => _$RouteQueryToJson(this);
}

@JsonSerializable()
class RouteSegment {
  @JsonKey(name: 'route_id')
  final String routeId;
  @JsonKey(name: 'route_name')
  final String routeName;
  @JsonKey(name: 'origin_stop')
  final StopInfo originStop;
  @JsonKey(name: 'destination_stop')
  final StopInfo destinationStop;
  @JsonKey(name: 'departure_time')
  final DateTime? departureTime;
  @JsonKey(name: 'arrival_time')
  final DateTime? arrivalTime;
  @JsonKey(name: 'duration_minutes')
  final int? durationMinutes;
  @JsonKey(name: 'num_stops')
  final int numStops;

  RouteSegment({
    required this.routeId,
    required this.routeName,
    required this.originStop,
    required this.destinationStop,
    this.departureTime,
    this.arrivalTime,
    this.durationMinutes,
    required this.numStops,
  });

  factory RouteSegment.fromJson(Map<String, dynamic> json) =>
      _$RouteSegmentFromJson(json);

  Map<String, dynamic> toJson() => _$RouteSegmentToJson(this);
}

@JsonSerializable()
class StopInfo {
  @JsonKey(name: 'stop_id')
  final String stopId;
  @JsonKey(name: 'stop_name')
  final String stopName;
  @JsonKey(name: 'stop_lat')
  final double? stopLat;
  @JsonKey(name: 'stop_lon')
  final double? stopLon;

  StopInfo({
    required this.stopId,
    required this.stopName,
    this.stopLat,
    this.stopLon,
  });

  factory StopInfo.fromJson(Map<String, dynamic> json) =>
      _$StopInfoFromJson(json);

  Map<String, dynamic> toJson() => _$StopInfoToJson(this);
}

@JsonSerializable()
class RouteOption {
  final List<RouteSegment> segments;
  @JsonKey(name: 'total_duration_minutes')
  final int totalDurationMinutes;
  @JsonKey(name: 'num_transfers')
  final int numTransfers;
  @JsonKey(name: 'departure_time')
  final DateTime departureTime;
  @JsonKey(name: 'arrival_time')
  final DateTime arrivalTime;
  @JsonKey(name: 'estimated_crowding')
  final String? estimatedCrowding;

  RouteOption({
    required this.segments,
    required this.totalDurationMinutes,
    required this.numTransfers,
    required this.departureTime,
    required this.arrivalTime,
    this.estimatedCrowding,
  });

  factory RouteOption.fromJson(Map<String, dynamic> json) =>
      _$RouteOptionFromJson(json);

  Map<String, dynamic> toJson() => _$RouteOptionToJson(this);
}

@JsonSerializable()
class RouteResponse {
  final RouteQuery query;
  final List<RouteOption> routes;
  final DateTime timestamp;
  final dynamic weather; // Can be WeatherCurrentResponse or null

  RouteResponse({
    required this.query,
    required this.routes,
    required this.timestamp,
    this.weather,
  });

  factory RouteResponse.fromJson(Map<String, dynamic> json) =>
      _$RouteResponseFromJson(json);

  Map<String, dynamic> toJson() => _$RouteResponseToJson(this);
}
