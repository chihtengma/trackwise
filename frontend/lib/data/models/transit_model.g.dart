// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'transit_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

TripUpdate _$TripUpdateFromJson(Map<String, dynamic> json) => TripUpdate(
      tripId: json['trip_id'] as String,
      routeId: json['route_id'] as String,
      startTime: json['start_time'] as String?,
      startDate: json['start_date'] as String?,
      stopTimeUpdates: (json['stop_time_updates'] as List<dynamic>)
          .map((e) => StopTimeUpdate.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$TripUpdateToJson(TripUpdate instance) =>
    <String, dynamic>{
      'trip_id': instance.tripId,
      'route_id': instance.routeId,
      'start_time': instance.startTime,
      'start_date': instance.startDate,
      'stop_time_updates': instance.stopTimeUpdates,
    };

StopTimeUpdate _$StopTimeUpdateFromJson(Map<String, dynamic> json) =>
    StopTimeUpdate(
      stopId: json['stop_id'] as String,
      stopName: json['stop_name'] as String?,
      arrivalTime: json['arrival_time'] == null
          ? null
          : DateTime.parse(json['arrival_time'] as String),
      departureTime: json['departure_time'] == null
          ? null
          : DateTime.parse(json['departure_time'] as String),
      delay: (json['delay'] as num?)?.toInt(),
    );

Map<String, dynamic> _$StopTimeUpdateToJson(StopTimeUpdate instance) =>
    <String, dynamic>{
      'stop_id': instance.stopId,
      'stop_name': instance.stopName,
      'arrival_time': instance.arrivalTime?.toIso8601String(),
      'departure_time': instance.departureTime?.toIso8601String(),
      'delay': instance.delay,
    };

RouteQuery _$RouteQueryFromJson(Map<String, dynamic> json) => RouteQuery(
      origin: json['origin'] as String,
      destination: json['destination'] as String,
      departureTime: json['departure_time'] == null
          ? null
          : DateTime.parse(json['departure_time'] as String),
      maxRoutes: (json['max_routes'] as num?)?.toInt() ?? 3,
      preferLessCrowded: json['prefer_less_crowded'] as bool? ?? false,
      includeWeather: json['include_weather'] as bool? ?? false,
      weatherLocation: json['weather_location'] as String?,
    );

Map<String, dynamic> _$RouteQueryToJson(RouteQuery instance) =>
    <String, dynamic>{
      'origin': instance.origin,
      'destination': instance.destination,
      'departure_time': instance.departureTime?.toIso8601String(),
      'max_routes': instance.maxRoutes,
      'prefer_less_crowded': instance.preferLessCrowded,
      'include_weather': instance.includeWeather,
      'weather_location': instance.weatherLocation,
    };

RouteSegment _$RouteSegmentFromJson(Map<String, dynamic> json) => RouteSegment(
      routeId: json['route_id'] as String,
      routeName: json['route_name'] as String,
      originStop:
          StopInfo.fromJson(json['origin_stop'] as Map<String, dynamic>),
      destinationStop:
          StopInfo.fromJson(json['destination_stop'] as Map<String, dynamic>),
      departureTime: json['departure_time'] == null
          ? null
          : DateTime.parse(json['departure_time'] as String),
      arrivalTime: json['arrival_time'] == null
          ? null
          : DateTime.parse(json['arrival_time'] as String),
      durationMinutes: (json['duration_minutes'] as num?)?.toInt(),
      numStops: (json['num_stops'] as num).toInt(),
    );

Map<String, dynamic> _$RouteSegmentToJson(RouteSegment instance) =>
    <String, dynamic>{
      'route_id': instance.routeId,
      'route_name': instance.routeName,
      'origin_stop': instance.originStop,
      'destination_stop': instance.destinationStop,
      'departure_time': instance.departureTime?.toIso8601String(),
      'arrival_time': instance.arrivalTime?.toIso8601String(),
      'duration_minutes': instance.durationMinutes,
      'num_stops': instance.numStops,
    };

StopInfo _$StopInfoFromJson(Map<String, dynamic> json) => StopInfo(
      stopId: json['stop_id'] as String,
      stopName: json['stop_name'] as String,
      stopLat: (json['stop_lat'] as num?)?.toDouble(),
      stopLon: (json['stop_lon'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$StopInfoToJson(StopInfo instance) => <String, dynamic>{
      'stop_id': instance.stopId,
      'stop_name': instance.stopName,
      'stop_lat': instance.stopLat,
      'stop_lon': instance.stopLon,
    };

RouteOption _$RouteOptionFromJson(Map<String, dynamic> json) => RouteOption(
      segments: (json['segments'] as List<dynamic>)
          .map((e) => RouteSegment.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalDurationMinutes: (json['total_duration_minutes'] as num).toInt(),
      numTransfers: (json['num_transfers'] as num).toInt(),
      departureTime: DateTime.parse(json['departure_time'] as String),
      arrivalTime: DateTime.parse(json['arrival_time'] as String),
      estimatedCrowding: json['estimated_crowding'] as String?,
    );

Map<String, dynamic> _$RouteOptionToJson(RouteOption instance) =>
    <String, dynamic>{
      'segments': instance.segments,
      'total_duration_minutes': instance.totalDurationMinutes,
      'num_transfers': instance.numTransfers,
      'departure_time': instance.departureTime.toIso8601String(),
      'arrival_time': instance.arrivalTime.toIso8601String(),
      'estimated_crowding': instance.estimatedCrowding,
    };

RouteResponse _$RouteResponseFromJson(Map<String, dynamic> json) =>
    RouteResponse(
      query: RouteQuery.fromJson(json['query'] as Map<String, dynamic>),
      routes: (json['routes'] as List<dynamic>)
          .map((e) => RouteOption.fromJson(e as Map<String, dynamic>))
          .toList(),
      timestamp: DateTime.parse(json['timestamp'] as String),
      weather: json['weather'],
    );

Map<String, dynamic> _$RouteResponseToJson(RouteResponse instance) =>
    <String, dynamic>{
      'query': instance.query,
      'routes': instance.routes,
      'timestamp': instance.timestamp.toIso8601String(),
      'weather': instance.weather,
    };
