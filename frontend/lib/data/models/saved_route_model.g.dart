// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'saved_route_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SavedRouteModel _$SavedRouteModelFromJson(Map<String, dynamic> json) =>
    SavedRouteModel(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      name: json['name'] as String,
      origin: json['origin'] as String,
      destination: json['destination'] as String,
      routeTypes: json['route_types'] as String?,
      notes: json['notes'] as String?,
      isFavorite: json['is_favorite'] as bool,
      isActive: json['is_active'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$SavedRouteModelToJson(SavedRouteModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'name': instance.name,
      'origin': instance.origin,
      'destination': instance.destination,
      'route_types': instance.routeTypes,
      'notes': instance.notes,
      'is_favorite': instance.isFavorite,
      'is_active': instance.isActive,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

SavedRouteCreate _$SavedRouteCreateFromJson(Map<String, dynamic> json) =>
    SavedRouteCreate(
      name: json['name'] as String,
      origin: json['origin'] as String,
      destination: json['destination'] as String,
      routeTypes: json['route_types'] as String?,
      notes: json['notes'] as String?,
      isFavorite: json['is_favorite'] as bool? ?? false,
    );

Map<String, dynamic> _$SavedRouteCreateToJson(SavedRouteCreate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'origin': instance.origin,
      'destination': instance.destination,
      'route_types': instance.routeTypes,
      'notes': instance.notes,
      'is_favorite': instance.isFavorite,
    };

SavedRouteUpdate _$SavedRouteUpdateFromJson(Map<String, dynamic> json) =>
    SavedRouteUpdate(
      name: json['name'] as String?,
      origin: json['origin'] as String?,
      destination: json['destination'] as String?,
      routeTypes: json['route_types'] as String?,
      notes: json['notes'] as String?,
      isFavorite: json['is_favorite'] as bool?,
      isActive: json['is_active'] as bool?,
    );

Map<String, dynamic> _$SavedRouteUpdateToJson(SavedRouteUpdate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'origin': instance.origin,
      'destination': instance.destination,
      'route_types': instance.routeTypes,
      'notes': instance.notes,
      'is_favorite': instance.isFavorite,
      'is_active': instance.isActive,
    };

SavedRouteListResponse _$SavedRouteListResponseFromJson(
        Map<String, dynamic> json) =>
    SavedRouteListResponse(
      routes: (json['routes'] as List<dynamic>)
          .map((e) => SavedRouteModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      total: (json['total'] as num).toInt(),
      favoritesCount: (json['favorites_count'] as num).toInt(),
    );

Map<String, dynamic> _$SavedRouteListResponseToJson(
        SavedRouteListResponse instance) =>
    <String, dynamic>{
      'routes': instance.routes,
      'total': instance.total,
      'favorites_count': instance.favoritesCount,
    };
