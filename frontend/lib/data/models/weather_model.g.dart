// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'weather_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

WeatherCurrentResponse _$WeatherCurrentResponseFromJson(
        Map<String, dynamic> json) =>
    WeatherCurrentResponse(
      location: json['location'] as String,
      tempCelsius: (json['temp_celsius'] as num).toDouble(),
      tempFahrenheit: (json['temp_fahrenheit'] as num).toDouble(),
      feelsLikeCelsius: (json['feels_like_celsius'] as num).toDouble(),
      condition: json['condition'] as String,
      description: json['description'] as String,
      humidity: (json['humidity'] as num).toInt(),
      windSpeed: (json['wind_speed'] as num).toDouble(),
      visibilityKm: (json['visibility_km'] as num).toDouble(),
    );

Map<String, dynamic> _$WeatherCurrentResponseToJson(
        WeatherCurrentResponse instance) =>
    <String, dynamic>{
      'location': instance.location,
      'temp_celsius': instance.tempCelsius,
      'temp_fahrenheit': instance.tempFahrenheit,
      'feels_like_celsius': instance.feelsLikeCelsius,
      'condition': instance.condition,
      'description': instance.description,
      'humidity': instance.humidity,
      'wind_speed': instance.windSpeed,
      'visibility_km': instance.visibilityKm,
    };

WeatherQuery _$WeatherQueryFromJson(Map<String, dynamic> json) => WeatherQuery(
      location: json['location'] as String,
    );

Map<String, dynamic> _$WeatherQueryToJson(WeatherQuery instance) =>
    <String, dynamic>{
      'location': instance.location,
    };
