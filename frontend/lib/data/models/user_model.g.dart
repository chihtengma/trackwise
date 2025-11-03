// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserModel _$UserModelFromJson(Map<String, dynamic> json) => UserModel(
      id: (json['id'] as num).toInt(),
      email: json['email'] as String,
      username: json['username'] as String,
      fullName: json['full_name'] as String?,
      profilePicture: json['profile_picture'] as String?,
      isActive: json['is_active'] as bool,
      isSuperuser: json['is_superuser'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$UserModelToJson(UserModel instance) => <String, dynamic>{
      'id': instance.id,
      'email': instance.email,
      'username': instance.username,
      'full_name': instance.fullName,
      'profile_picture': instance.profilePicture,
      'is_active': instance.isActive,
      'is_superuser': instance.isSuperuser,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

UserCreate _$UserCreateFromJson(Map<String, dynamic> json) => UserCreate(
      email: json['email'] as String,
      username: json['username'] as String,
      fullName: json['full_name'] as String?,
      password: json['password'] as String,
    );

Map<String, dynamic> _$UserCreateToJson(UserCreate instance) =>
    <String, dynamic>{
      'email': instance.email,
      'username': instance.username,
      'full_name': instance.fullName,
      'password': instance.password,
    };

UserUpdate _$UserUpdateFromJson(Map<String, dynamic> json) => UserUpdate(
      email: json['email'] as String?,
      username: json['username'] as String?,
      fullName: json['full_name'] as String?,
      password: json['password'] as String?,
      profilePicture: json['profile_picture'] as String?,
      isActive: json['is_active'] as bool?,
    );

Map<String, dynamic> _$UserUpdateToJson(UserUpdate instance) =>
    <String, dynamic>{
      'email': instance.email,
      'username': instance.username,
      'full_name': instance.fullName,
      'password': instance.password,
      'profile_picture': instance.profilePicture,
      'is_active': instance.isActive,
    };

TokenResponse _$TokenResponseFromJson(Map<String, dynamic> json) =>
    TokenResponse(
      accessToken: json['access_token'] as String,
      tokenType: json['token_type'] as String? ?? 'bearer',
      user: json['user'] == null
          ? null
          : UserModel.fromJson(json['user'] as Map<String, dynamic>),
      isNewUser: json['is_new_user'] as bool?,
    );

Map<String, dynamic> _$TokenResponseToJson(TokenResponse instance) =>
    <String, dynamic>{
      'access_token': instance.accessToken,
      'token_type': instance.tokenType,
      'user': instance.user,
      'is_new_user': instance.isNewUser,
    };
