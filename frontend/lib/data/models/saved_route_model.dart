import 'package:json_annotation/json_annotation.dart';

part 'saved_route_model.g.dart';

@JsonSerializable()
class SavedRouteModel {
  final int id;
  @JsonKey(name: 'user_id')
  final int userId;
  final String name;
  final String origin;
  final String destination;
  @JsonKey(name: 'route_types')
  final String? routeTypes;
  final String? notes;
  @JsonKey(name: 'is_favorite')
  final bool isFavorite;
  @JsonKey(name: 'is_active')
  final bool isActive;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;

  SavedRouteModel({
    required this.id,
    required this.userId,
    required this.name,
    required this.origin,
    required this.destination,
    this.routeTypes,
    this.notes,
    required this.isFavorite,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
  });

  factory SavedRouteModel.fromJson(Map<String, dynamic> json) =>
      _$SavedRouteModelFromJson(json);

  Map<String, dynamic> toJson() => _$SavedRouteModelToJson(this);

  SavedRouteModel copyWith({
    int? id,
    int? userId,
    String? name,
    String? origin,
    String? destination,
    String? routeTypes,
    String? notes,
    bool? isFavorite,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return SavedRouteModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      name: name ?? this.name,
      origin: origin ?? this.origin,
      destination: destination ?? this.destination,
      routeTypes: routeTypes ?? this.routeTypes,
      notes: notes ?? this.notes,
      isFavorite: isFavorite ?? this.isFavorite,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}

@JsonSerializable()
class SavedRouteCreate {
  final String name;
  final String origin;
  final String destination;
  @JsonKey(name: 'route_types')
  final String? routeTypes;
  final String? notes;
  @JsonKey(name: 'is_favorite')
  final bool isFavorite;

  SavedRouteCreate({
    required this.name,
    required this.origin,
    required this.destination,
    this.routeTypes,
    this.notes,
    this.isFavorite = false,
  });

  factory SavedRouteCreate.fromJson(Map<String, dynamic> json) =>
      _$SavedRouteCreateFromJson(json);

  Map<String, dynamic> toJson() => _$SavedRouteCreateToJson(this);
}

@JsonSerializable()
class SavedRouteUpdate {
  final String? name;
  final String? origin;
  final String? destination;
  @JsonKey(name: 'route_types')
  final String? routeTypes;
  final String? notes;
  @JsonKey(name: 'is_favorite')
  final bool? isFavorite;
  @JsonKey(name: 'is_active')
  final bool? isActive;

  SavedRouteUpdate({
    this.name,
    this.origin,
    this.destination,
    this.routeTypes,
    this.notes,
    this.isFavorite,
    this.isActive,
  });

  factory SavedRouteUpdate.fromJson(Map<String, dynamic> json) =>
      _$SavedRouteUpdateFromJson(json);

  Map<String, dynamic> toJson() => _$SavedRouteUpdateToJson(this);
}

@JsonSerializable()
class SavedRouteListResponse {
  final List<SavedRouteModel> routes;
  final int total;
  @JsonKey(name: 'favorites_count')
  final int favoritesCount;

  SavedRouteListResponse({
    required this.routes,
    required this.total,
    required this.favoritesCount,
  });

  factory SavedRouteListResponse.fromJson(Map<String, dynamic> json) =>
      _$SavedRouteListResponseFromJson(json);

  Map<String, dynamic> toJson() => _$SavedRouteListResponseToJson(this);
}
